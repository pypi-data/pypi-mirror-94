# vim: tabstop=8 softtabstop=0 expandtab shiftwidth=4 smarttab

import hashlib
import os,sys,tempfile
import datetime
import dateutil.parser
import json
import time
from filelock import FileLock, Timeout

class RateLimitException(Exception):
    """Wrapper to catch the unexpected"""

    def __init__(self, msg):
        super(RateLimitException, self).__init__(msg)

class TimeOutException(Exception):
    """Wrapper to catch the unexpected"""

    def __init__(self, msg):
        super(TimeOutException, self).__init__(msg)

class RateLimitNoLimit(object):
    fileBody = {}

    def updateError(self):
        return True

    def updateStats(self) -> bool:
        return True

class RateLimit(RateLimitNoLimit):

    fileBody = {
        'creationDate' : datetime.datetime.now().isoformat(),
        'lastOKRequests' : [datetime.datetime.now().isoformat()],
        'lastUsageDate' : datetime.datetime.now().isoformat(),
        'lastErrorDate' : datetime.datetime.now().isoformat(),
        'lastKORequests' : []
    }

    maxAllowedErrors  = 10
    maxCallsPerMinute = 100
    maxCallsPerHour   = 1000

    def __init__(self, token:str, path=tempfile.gettempdir()):
        self._token = token 
        self._workPath = path
        self._hash = hashlib.sha1(token.encode('utf-8'))
        self._fileName = f'{self._hash.hexdigest()}.json'
        self._filePath = f'{self._workPath}/{self._fileName}'
        self._fileLock = f'{self._workPath}/{self._fileName}.lock'
        self.lock = FileLock(self._fileLock, timeout=5)
        if os.path.exists(self._filePath):
            try:
                self.lock.acquire(timeout=5)
                try:
                    with open(self._filePath) as json_file:
                        self.fileBody = json.load(json_file)
                        json_file.close()
                finally:    
                    self.lock.release()    
            except Timeout:
                raise TimeOutException("File Locked from another process")
        else:
            self._updateFile()
    
    def _removeOldFileEntries(self):
        self.fileBody['lastOKRequests'] = self._getFilterDateArray(3600, self.fileBody['lastOKRequests'])
        self.fileBody['lastKORequests'] = self._getFilterDateArray(3600, self.fileBody['lastKORequests'])

    def _updateFile(self):
        with open(self._filePath, "w") as json_file:
            self._removeOldFileEntries()
            json_file.write(json.dumps(self.fileBody))
            json_file.close

    def _getFilterDateArray(self, seconds, dataset):
        filteredRequest = filter(lambda t : (datetime.datetime.now() - dateutil.parser.isoparse(t)).seconds < seconds, 
                                dataset)
        filteredDates = list(filteredRequest)
        return filteredDates

    def updateError(self):
        try:
            self.lock.acquire(timeout=1)
            try:
                timeStamp = datetime.datetime.now()
                if not self.fileBody['lastKORequests']:
                    self.fileBody['lastKORequests'].append(timeStamp.isoformat())
                    self._updateFile()
                    return True

                filteredDates = self._getFilterDateArray(3600, self.fileBody['lastKORequests'])
                if len(filteredDates) >= self.maxAllowedErrors:
                    return False
                else:
                    self.fileBody['lastKORequests'].append(timeStamp.isoformat())
                    self._updateFile()
                    return True
            finally:
                self.lock.release()
        except Timeout:
            return False



    def _updateStatsHour(self) -> bool:
        filteredDates = self._getFilterDateArray(3600, self.fileBody['lastOKRequests'])
        if len(filteredDates) > self.maxCallsPerHour:
            return False
        else:
            return True


    def updateStats(self) -> bool:
        try:
            self.lock.acquire(timeout=1)
            try:
                timeStamp = datetime.datetime.now()
                if not self._updateStatsHour():
                    return False
                filteredDates = self._getFilterDateArray(60, self.fileBody['lastOKRequests'])
                if len(filteredDates) > self.maxCallsPerMinute:
                    return False
                else:
                    self.fileBody['lastOKRequests'].append(timeStamp.isoformat())
                    self.fileBody['lastUsageDate'] = timeStamp.isoformat() 
                    self._updateFile()
                    return True
            finally:
                self.lock.release()
        except Timeout:
            return False
