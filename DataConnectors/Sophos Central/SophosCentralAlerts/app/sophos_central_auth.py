import requests
import logging
import json
import datetime


def whoami(jwt):
    uri = 'https://api.central.sophos.com/whoami/v1'
    h = {
        'Authorization': f'Bearer {jwt}'
        }
    r = requests.get(uri, headers=h)
    if r.status_code == 200:
        j = json.loads(r.text)
        tenant_id = j['id']
        tenant_type = j['idType']
        data_region = j['apiHosts']['dataRegion']
        return tenant_id, tenant_type, data_region
    else:
        logging.error("Unable to obtain whoami details")

def auth(client_id, client_secret):
    logging.info("Obtaining Sophos Central JWT")
    uri = "https://id.sophos.com/api/v2/oauth2/token"

    d = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'token'
        }
    r = requests.post(uri, data=d)

    if r.status_code == 200:
        j = json.loads(r.text)
        jwt = j['access_token']
        expires_in = datetime.datetime.now() + datetime.timedelta(seconds = j['expires_in'])
        tenant_id, tenant_type, data_region = whoami(jwt)
        return jwt, tenant_id, tenant_type, data_region, expires_in
        
    else:
        logging.error("Authentication failed")
        return False