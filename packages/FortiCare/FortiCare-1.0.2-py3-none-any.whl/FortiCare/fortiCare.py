# vim: tabstop=8 softtabstop=0 expandtab shiftwidth=4 smarttab

import requests, json, re 
import PyPDF2
import logging
import pprint
import validators
import datetime
from datetime import timezone
from dateutil import tz
from time import gmtime, strftime
from tabulate import tabulate

from FortiCare import rateLimit

class FCRBaseException(Exception):
    """Wrapper to catch the unexpected"""

    def __init__(self, msg):
        super(FCRBaseException, self).__init__(msg)

class FCRStatusException(FCRBaseException):
    def __init__(self, status, m, fullResponse):
        msg = "Wrong status after request:\n- Status: {}\n- Message: {}".format(status,m)
        super(FCRStatusException, self).__init__(msg)
        self._fullResponse = fullResponse

    def fullResponse(self):
        return self._fullResponse

class FCRRegistrationCodeNotFoundException(FCRBaseException):
    def __init__(self):
        super(FCRRegistrationCodeNotFoundException, self).__init__("Registation code not found in PDF file")

class FCRRegistrationTooManyDevices(FCRBaseException):
    def __init__(self):
        super(FCRRegistrationTooManyDevices, self).__init__("Max devices limit in one registration request exceeded")

class AssetEntitlement(object):
    """
    Support class for asset entitlement 
    """
    def __init__(self, level, levelDesc, type, typeDesc, startDate, endDate):
        self._level = level
        self._levelDesc = levelDesc
        self._type = type
        self._typeDesc = typeDesc
        self._startDate = startDate
        self._endDate = endDate

    @property
    def type(self):
        return self._type
    
    @property
    def typeDesc(self):
        return self._typeDesc

    @property
    def level(self):
        return self._level

    @property
    def levelDesc(self):
        return self._levelDesc
    
    @property
    def startDate(self):
        return self._startDate

    @property
    def endDate(self):
        return self._endDate
    
    def getNumberOfValidityDays(self):
        sub = self.endDate - datetime.datetime.now(tz=timezone.utc)
        return sub.days


class Asset(object):
    """
    Device parameteters
    """
    def __init__(self,serialNumber, registrationDate, sku, productModel, description=''):
        '''
        Create an asset class
        '''
        self._serialNumber = serialNumber     
        self._registrationDate = registrationDate
        self._description = description   
        self._sku = sku
        self._productModel = productModel
        self._entitlements = []

    @property
    def sku(self):
        return self._sku
    
    @property
    def productModel(self):
        return self._productModel

    @property
    def serialNumber(self):
        return self._serialNumber

    @property
    def registrationDate(self):
        return self._registrationDate
    
    @property
    def description(self):
        return self._description
    
    @property
    def entitlements(self):
        return self._entitlements

    def addEntitlement(self, entitlement:AssetEntitlement):
        self._entitlements.append(entitlement)

    def __str__(self):
        '''
        Return string of asset details as a tabulate
        '''
        details = ""
        details += f'Model: {self.productModel}\n'
        details += f'Serial Number: {self.serialNumber }\n'
        details += f'SKU: {self.sku}\n'
        details += 'Registration Date: {}\n'.format(
            self.registrationDate.astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M:%S %z"))
        details += f'Asset Description: {self.description}\n'
        details += 'Entitlements:\n'
        headers = ["Type", "Level", "Start Date", "End Date", "Remaining Days", "Description"]
        data = []
        for element in self.entitlements:
            data.append([element.type,
                        element.level, 
                        element.startDate.astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M %z"),
                        element.endDate.astimezone(tz.tzlocal()).strftime("%Y-%m-%d %H:%M %z"),
                        element.getNumberOfValidityDays(),
                        element.typeDesc])
        details += tabulate(data, headers=headers)

        return details.rstrip() + '\n'


class FortiCare():
    '''
    Main class to interract with support.fortinet.com API
    '''
    versionLib = '1.0'
    resourceBase = "ES/FCWS_RegistrationService.svc/REST"

    maxBatchRegister = 10

    def __init__(self, token, ratelimit=True): 
        self._token = token
        self._baseUrl = 'https://support.fortinet.com'
        self._reqUrl = "{}/{}".format(self._baseUrl, self.resourceBase)
        self._proxy = None 

        if ratelimit:
            self.rl = rateLimit.RateLimit(token)
        else:
            self.rl = rateLimit.RateLimitNoLimit()

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print(f'exc_type: {exc_type}')
            print(f'exc_value: {exc_value}')
            # print(f'exc_traceback: {exc_traceback}')

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self,val):
        if not self._checkToken(val):
            raise FCRBaseException('Token is not valid')

        self._token = val

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, val):
        if not validators.url(val):
            raise FCRBaseException('Proxy is not valid')

        self._proxy = {
            'http'  : val,
            'https' : val,
        }

    def _sendAndReceive(self, restFunction, **kwargs):
        s = requests.session()
        if self.proxy:
            s.proxies=self.proxy
            logging.debug("API request Proxy:\n%s", pprint.pformat(s.proxies))
        if self.rl.updateStats():
            logging.debug("Rate Limit body:\n%s", pprint.pformat(self.rl.fileBody))
            r = s.post("{}/{}".format(self._reqUrl, restFunction), **kwargs)
        else:
             raise rateLimit.RateLimitException("Request limit exceed, try again later")

        if kwargs['json']:
            logging.debug("API request:\n%s", pprint.pformat(kwargs['json']))

        if r.status_code == 200:
            response = r.json()
            logging.debug("API response:\n%s", pprint.pformat(response))

            if not response['Status'] == 0:
                self.rl.updateError()
                raise FCRStatusException(response['Status'], response['Message'], response)
            else:
                return response
        else:
            r.raise_for_status()

    def GetRegistrationCodeFromPDF(self, pdfpath):
        """
        Use the PDF provided by Fortinet to register your assets
        Parameters
        ----------
        pdfpath : string
            Path of the pdf file provided by fortinet
        """    
        file = open(pdfpath, 'rb')
        fileReader = PyPDF2.PdfFileReader(file)
        page = fileReader.getPage(0)
        page_content = page.extractText()
        k = re.search(r"([A-Z0-9]*-){4}[A-Z0-9]{6}", page_content)
        if k:
            found = k.group()
            return(found)
        else:
            raise FCRRegistrationCodeNotFoundException()

    def GetAssets(self, serialNumber=None, expire=datetime.datetime.now() + datetime.timedelta(days=36500)):
        """
        Returns product LIST based on product serialNumber search pattern or support package expiration date
        Parameters
        ----------
        serialNumber : string
            Serial number of assets
        expire : datetime
            Date and time
        """
        payload = {
            "Token" : self._token, 	
            "Version" :	self.versionLib	
        }

        if serialNumber:
            payload["Serial_Number"] = serialNumber
        
        if expire:
            payload['Expire_Before'] = expire.strftime('%Y-%m-%dT%H:%M:%S')
        
        jsonAssets = self._sendAndReceive("REST_GetAssets", json=payload)
        AssetsList = []
        if jsonAssets['Assets']:
            for asset in jsonAssets['Assets']: 
                assetObj = Asset(asset['Serial_Number'],
                                datetime.datetime.strptime(asset['Registration_Date'], '%Y-%m-%dT%H:%M:%S')
                                                          .replace(tzinfo=tz.tzutc()),
                                asset['SKU'],
                                asset['ProductModel'],
                                asset['Description'])
                for element in asset['Entitlements']:
                    ent = AssetEntitlement(element['Level'],
                                            element['Level_Desc'],
                                            element['Type'],
                                            element['Type_Desc'],
                                            datetime.datetime.strptime(element['Start_Date'], '%Y-%m-%dT%H:%M:%S')
                                                                      .replace(tzinfo=tz.tzutc()),
                                            datetime.datetime.strptime(element['End_Date'], '%Y-%m-%dT%H:%M:%S')
                                                                      .replace(tzinfo=tz.tzutc()) )
                    assetObj.addEntitlement(ent)
                AssetsList.append(assetObj)
        
        return AssetsList

    def GetAsset(self, serialNumber=None):
        """
        Returns an asset via serialNumber
        Parameters
        ----------
        serialNumber : string
            Serial number of assets
        """
        payload = {
            "Token" : self._token, 	
            "Version" :	self.versionLib,
            "Serial_Number" : serialNumber
        }
            
        jsonAsset = self._sendAndReceive("REST_GetAssetDetails", json=payload)
        assetObj = Asset(jsonAsset['AssetDetails']['Serial_Number'],
                        datetime.datetime.strptime(jsonAsset['AssetDetails']['Registration_Date'], '%Y-%m-%dT%H:%M:%S')
                                                  .replace(tzinfo=tz.tzutc()),
                        jsonAsset['AssetDetails']['SKU'],
                        jsonAsset['AssetDetails']['ProductModel'],
                        jsonAsset['AssetDetails']['Description'])
        for element in jsonAsset['AssetDetails']['Entitlements']:
            ent = AssetEntitlement(element['Level'],
                                    element['Level_Desc'],
                                    element['Type'],
                                    element['Type_Desc'],
                                    datetime.datetime.strptime(element['Start_Date'], '%Y-%m-%dT%H:%M:%S')
                                                              .replace(tzinfo=tz.tzutc()),
                                    datetime.datetime.strptime(element['End_Date'], '%Y-%m-%dT%H:%M:%S')
                                                              .replace(tzinfo=tz.tzutc()))
            assetObj.addEntitlement(ent)
        return assetObj

    def UpdateAssetDescription(self, serialNumber, description=''):
        """
        Change the description of an asset
        Parameters
        ----------
        serialNumber : string
            Serial number of assets
        description : string
            Descriptio of the device
        """
        payload = {
            'Token' : self.token,
            'Version' : self.versionLib,
            "Serial_Number" : serialNumber,
            'Description' : description
        }
        resp = self._sendAndReceive("REST_UpdateDescription", json=payload)
        
    def RegisterDevices(self, serialNumbers=[], gov=False):
        """
        Register hardware devices
        Parameters
        ----------
        serialNumbers: list of strings
            Serial numbers of devices to register
        gov : boolean
            For devices used by government account
        """

        if len(serialNumbers) > self.maxBatchRegister:
            raise FCRRegistrationTooManyDevices()

        payload = {
            'Token' : self.token,
            'Version' : self.versionLib,
            'RegistrationUnits' :[]
        }

        for serial in serialNumbers:
            element = {
                'Serial_Number' : serial,
                'Is_Government' : 'false'
            }

            if gov:
                element['Is_Government'] = 'true'

            payload['RegistrationUnits'].append(element)

        jsonAsset = self._sendAndReceive("REST_RegisterUnits", json=payload)

    def RegisterLicense(self, code, ip=None, gov=False):
        """
        Register VM license via the code provided by Fortinet
        Parameters
        ----------
        code : string
            Registration code provided by Fortinet 
        ip : string
            IP to associate at the assets to register 
        gov : boolean
            For devices used by government account
        """
        payload = {
            'Token' : self.token,
            'Version' : self.versionLib,
            'License_Registration_Code' : code, 
            'Is_Government' : 'false'
        }
        if gov:
            payload['Is_Government'] = 'true'
        if ip:
            payload['Additional_Info'] = ip

        jsonAsset = self._sendAndReceive("REST_RegisterLicense", json=payload)
        serialNumber = jsonAsset['AssetDetails']['Serial_Number']
        return serialNumber
    
    def DownloadLicense(self, serialNumber):
        """
        Download the licence associateted to an asset serial number
        Parameters
        ----------
        serialNumber : string
            Serial number of assets
        """
        payload = {
            'Token' : self.token,
            'Version' : self.versionLib,
            'Serial_Number' : serialNumber, 
        }

        response = self._sendAndReceive("REST_DownloadLicense", json=payload)
        return response['License_File']
    
    def _checkToken(self, token:str) -> bool:
        '''
        Check the validity of a token
        Parameters
        ----------
        token : str     
            the token to check 
        '''
        k = re.search(r"([A-Z0-9]{4}-{0,1}){8}", token)
        # I really dislike the python ternary stuff so I go old school
        if k:
            return True
        else:
            return False
        

