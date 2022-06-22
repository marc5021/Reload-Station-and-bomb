import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


userAgent = {"User-agent": "pppopo"}

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

def WeaponAPI(NFCid):
    weaponURL = "https://api.autoball.dk/api/players/weapons/"+NFCid
    return weaponURL

def RefillAPI(NFCid):
    refillURL = "https://api.autoball.dk/api/players/weapons/"+NFCid+"/refill"
    return refillURL


def RefillReq(NFCid):
    Response = session.post(RefillAPI(NFCid), headers=userAgent)
    return Response

def WeaponReq(NFCid):
    Response = session.get(WeaponAPI(NFCid), headers=userAgent)
    return Response