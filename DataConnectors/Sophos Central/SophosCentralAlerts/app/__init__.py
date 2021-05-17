import logging
import os
from datetime import datetime
from configparser import ConfigParser
import azure.functions as func
from app.sophos_central_auth import auth
from app.sophos_central_alerts import get_alerts
from app.sophos_central_config import AppConfiguration

appconfig = AppConfiguration()

def main(sophoscentralconnector: func.TimerRequest) -> None:
    appconfig.checkconfiguration()
    get_alerts()
