import datetime
import logging
import json
import requests
import re

logAnalyticsUri = os.environ.get('logAnalyticsUri')
if ((logAnalyticsUri in (None, '') or str(logAnalyticsUri).isspace())):    
    logAnalyticsUri = 'https://' + customerId + '.ods.opinsights.azure.com'

pattern = r"https:\/\/([\w\-]+)\.ods\.opinsights\.azure.([a-zA-Z\.]+)$"
match = re.match(pattern,str(logAnalyticsUri))
if(not match):
    raise Exception("Invalid Log Analytics Uri.")
    
def post_data(customer_id, shared_key, body, log_type):
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = logAnalyticsUri + resource + "?api-version=2016-04-01"

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }
    try:
        response = requests.post(uri, data=body, headers=headers)
    except Exception as err:
        logging.info(f"Error during sending logs to Azure Sentinel: {err}")
    else:
        if (response.status_code >= 200 and response.status_code <= 299):
            logging.info("logs have been successfully sent to Azure Sentinel.")
        else:
            loggin.info(f"Error during sending logs to Azure Sentinel. Response code: {response.status_code}")


if (len(response) > 0):
    post_data(customer_id, shared_key, body, log_type)
else:
    logging.info("No records were found.")