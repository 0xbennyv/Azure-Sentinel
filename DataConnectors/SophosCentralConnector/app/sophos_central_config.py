import datetime
import logging
import os
from configparser import ConfigParser
from app.sophos_central_auth import auth

class AppConfiguration():

    def checkconfiguration(self):
        if os.path.exists('app/config.ini'):
            logging.info('Checking Token Expiry')
            self.config.read('app/config.ini')
            now = datetime.datetime.now()
            expires = datetime.datetime.strptime(self.config['sophos']['expires'], '%Y-%m-%d %H:%M:%S.%f')
            if expires > now:
                logging.info('Token is still good')
            else:
                logging.info('JWT Expired')
                self.renewjwt()
        else:
            self.newconfiguration()

    def newconfiguration(self):
        logging.info('Creating new config file')
        # Get the SOPHOS Central Credentials
        jwt, tenant_id, tenant_type, data_region, expires_in = auth(os.environ['client_id'], os.environ['client_secret'])
        # Create new config
        self.config.read('app/config.ini')
        self.config.add_section('sophos')
        self.config.set('sophos', 'jwt', f'{jwt}')
        self.config.set('sophos', 'expires', f'{expires_in}')
        self.config.set('sophos', 'tenant_id', f'{tenant_id}')
        self.config.set('sophos', 'tenant_type', f'{tenant_type}')
        self.config.set('sophos', 'data_region', f'{data_region}')
        with open('app/config.ini', 'w') as f:
            logging.info('Writing config file')
            self.config.write(f)
    
    def renewjwt(self):
        logging.info('Getting new JWT')
        # Get the SOPHOS Central Credentials
        jwt, tenant_id, tenant_type, data_region, expires_in = auth(os.environ['client_id'], os.environ['client_secret'])
        # Update config
        self.config.read('app/config.ini')
        self.config.set('sophos', 'jwt', f'{jwt}')
        self.config.set('sophos', 'expires', f'{expires_in}')
        with open('app/config.ini', 'w') as f:
            logging.info('Updating config file')
            self.config.write(f)

    def __init__(self):
        self.config = ConfigParser()
