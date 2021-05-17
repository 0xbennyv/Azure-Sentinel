import datetime
import logging
import json
import requests
from datetime import datetime, timedelta
from configparser import ConfigParser
from app.azure_sentinel_connector import post_data

customer_id = os.environ['workspaceId'] 
shared_key = os.envviron['workspaceKey']
log_type = os.envviron['tableName']

def get_alerts():
    config = ConfigParser()
    config.read('app/config.ini')
    uri = f"{config['sophos']['data_region']}/common/v1/alerts"
    h = {
        "Authorization": f"Bearer {config['sophos']['jwt']}",
        "Accept": "application/json",
        "X-Tenant-ID": f"{config['sophos']['tenant_id']}"
        }
    
    now = datetime.now() - timedelta(minutes=15)
    expires = datetime.strftime(now, '%Y-%m-%dT%H:%M:%S')
    p = {
        "from": f"{expires}"
    }
    r = requests.get(uri, headers=h, params=p)
    # Post Data to Sentinel
    post_data(customer_id, shared_key, r.text, log_type)