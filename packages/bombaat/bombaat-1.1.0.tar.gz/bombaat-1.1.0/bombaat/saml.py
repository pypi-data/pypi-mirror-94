#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""IDP SAML Response Handler."""

import os
import sys
import time
import base64
import logging

from urllib.parse import unquote
from urllib.parse import parse_qs
from xml.etree import ElementTree as ET
from typing import List, Tuple, Generator

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

-from bombaat.utils import print_msg
-from bombaat.driver import check_driver
-from bombaat.errors import SAMLParserError
-from bombaat.driver import get_driver_file
-from bombaat.errors import SSOConnectionError

__author__ = 'rboodher@juniper.net'

logger = logging.getLogger(__name__)

class SAMLParser(object):
    """Class to initiate SAML login with Azure AD Services."""

    def __init__(self, login_url: str, username: str, password: str) -> None:
        """Initialize SAML settings.

        :param str login_url: Should be taken from Azure Enterprise Applications
                              section. Also available in MS myapps portal.
        :param str username:  SSO username for an user.
        :param str password:  SSO password for an user.
        :return: None
        """
        self.login_url = login_url
        self.username = username
        self.password = password

        for exec_path in get_driver_file():
            if 'chromedriver' in str(exec_path).lower():
                self.executable_path = str(exec_path)
            elif 'chromium' in str(exec_path).lower():
                self.binary_location = str(exec_path)
            elif 'chrome' in str(exec_path).lower():
                self.binary_location = str(exec_path)

    def run(self) -> tuple:
        """Main function."""
        saml = self._create_driver(self.login_url)
        if saml:
            arns = self._get_arn(saml['saml_response'])
            final = {**arns, **saml}
            return final

    def _create_driver(self, login_url: str,
                                        headless: bool = True) -> Generator:
        """Create and configure a chrome webdriver object."""

        options = Options()
        options.add_argument('--log-level=ALL')
        options.binary_location = self.binary_location
        options.add_experimental_option('w3c', False)

        if headless:
            options.add_argument('--headless')

        caps = DesiredCapabilities.CHROME.copy()
        caps['loggingPrefs'] = {'performance': 'ALL'}

        print_msg('connecting to SSO service...\r')
        try:
            driver = webdriver.Chrome(executable_path=self.executable_path,
                                    options=options, desired_capabilities=caps)
            driver.get(self.login_url)
            time.sleep(2)
            print_msg('processing the authentication request...\r')
            self._process_login(driver,'idSIButton9','i0116',self.username)
            username_error = self._verify_credentials(driver, 'usernameError')
            time.sleep(2)
            if not username_error:
                self._process_login(driver,'idSIButton9','i0118', self.password)
            else:
                logger.error('Incorrect username! You can update username '
                                'by running the command `bombaat configure`')
                sys.exit(1)
            password_error = self._verify_credentials(driver, 'passwordError')
            time.sleep(1)
            if not password_error:
                #self._process_login(driver, button_id='idSIButton9')
                saml = self._get_saml(driver)
                driver.quit()
                return saml
            else:
                logger.error('The password you entered is incorrect! '
                                                        'Please try again.')
                sys.exit(1)
        except Exception as err:
            logger.error('Failed to process SSO authentication, '
                                                    'Please try again later.')
            driver.quit()
            sys.exit(1)

    def _process_login(self, driver: Generator, button_id: str,
                        element_id: str = None, key_name: str = None) -> None:
        """Process user credentials."""
        try:
            if element_id:
                element = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, element_id)))
                element.send_keys(key_name)
                button = driver.find_element_by_id(button_id).click()
                time.sleep(1)
            else:
                button = driver.find_element_by_id(button_id).click()
        except TimeoutException as err:
            logger.error('Your request has been timed out! '
                                            'please try again later!')
            sys.exit(1)

    @staticmethod
    def _verify_credentials(driver: Generator, id: str) -> None:
        """Verify user credentials."""
        print_msg('verifying Single Sign On login credentials...\r')
        try:
            if driver.find_element_by_id(id):
                driver.quit()
                return True
        except:
            pass

    def _get_saml(self, driver: Generator, sleeptime: float = 0.5) -> str:
        """Get SAML Response from WebDriver Obj."""

        saml_url = 'https://signin.aws.amazon.com/saml'

        print_msg('waiting for SAML response from single sign on...\r')
        while True:
            saml_response = {}
            time.sleep(sleeptime)
            for line in driver.get_log('performance'):
                try:
                    if 'samlresponse' in str(line).lower() and \
                                                saml_url in str(line).lower():
                        saml = [k[0].split(',')[0][:-1] \
                                  for k in parse_qs(line['message']).values()]
                        saml_response['saml_response'] = unquote(saml[0])
                        return saml_response
                except Exception as err:
                    raise SAMLParserError(
                     'Unable to parse SAML Response from SSO: %s' % (str(err),))

    def _get_arn(self, saml: str) -> List:
        """Get AWS Roles and Principal ARN from SAML Response."""

        attribute = '{urn:oasis:names:tc:SAML:2.0:assertion}Attribute'
        attribute_name = 'https://aws.amazon.com/SAML/Attributes/Role'
        attribute_val = '{urn:oasis:names:tc:SAML:2.0:assertion}AttributeValue'

        arns = {}
        for attrib in ET.fromstring(base64.b64decode(saml)).iter(attribute):
            if (attrib.get('Name') == attribute_name):
                for value in attrib.iter(attribute_val):
                     if arns.get('roles_arn') is None:
                         arns['roles_arn'] = [value.text.split(',')[0]]
                     else:
                         arns['roles_arn'].append(value.text.split(',')[0])

                     # Principal ARN for Identity Provider in AWS is same for
                     # all roles, all attribute value will have role arn and
                     # principal arn, so keeping only one.
                     if arns.get('principal_arn') is None:
                         arns['principal_arn'] = [value.text.split(',')[1]]
                     else:
                         val = value.text.split(',')[1]
                         if val not in arns['principal_arn']:
                             arns['principal_arn'].append(val)
        return arns
