# From here we "publish" classes and exceptions
from FortiCare.fortiCare import FortiCare, Asset, AssetEntitlement
from FortiCare.fortiCare import FCRBaseException, FCRStatusException, FCRRegistrationCodeNotFoundException, FCRRegistrationTooManyDevices

from FortiCare.rateLimit import RateLimitNoLimit, RateLimit
from FortiCare.rateLimit import RateLimitException, TimeOutException
