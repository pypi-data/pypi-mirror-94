#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""SP SAML Login Handler."""

import os
import sys
import boto3
import getpass
import logging

import inquirer
from blessed import Terminal
from botocore.configloader import load_config
from botocore.exceptions import ConfigNotFound
from botocore.session import Session, get_session
from awscli.customizations.configure.writer import ConfigFileWriter

from bombaat.utils import ask
from bombaat.saml import SAMLParser
from bombaat.utils import read_yaml
from bombaat.utils import MorningSun
from bombaat.errors import ProfileNotFound
from bombaat.utils import get_cloud_profiles
from bombaat.utils import datetime_utc_to_local
from bombaat.configure import write_credentials
from bombaat.configure import configure_default_profile

logger = logging.getLogger(__name__)

class Login(object):
    """Class to initiate AWS authentication with SAML token."""

    def __init__(self):
        self._session = get_session()
        self.cloud_profiles = get_cloud_profiles()
        self._config_writer = ConfigFileWriter()

    def main(self) -> None:
        selected_profile = self._get_login_profile()
        profile_details = self.cloud_profiles['login_urls'][selected_profile]
        _session = Session(profile=selected_profile)
        config = _session.get_scoped_config()
        login_url = profile_details['login_url']
        if config.get('username') is None:
            msg = (f'Username not found for the profile {selected_profile}, '
                'you can run `bombaat configure` to reconfigure the profile.')
            logger.error(msg)
            sys.exit(1)
        username = config['username']
        password = getpass.getpass(f'Enter password for the user {username}: ')
        get_saml = SAMLParser(login_url, username, password).run()
        aws_roles = get_saml['roles_arn']
        role_chosen = self._choose_role(aws_roles)
        cred = self._assume_role(role_chosen, get_saml['principal_arn'][0],
                                                    get_saml['saml_response'])
        new_values = cred['Credentials']
        write_credentials(_session, new_values, selected_profile)
        configure_default_profile()
        time = new_values['Expiration']
        time = datetime_utc_to_local(time)

        cloud_profile_friendly_name = profile_details['name']
        logger.info((f'Login successful! Your access for '
                f'{cloud_profile_friendly_name} expires at {time}!'))

    def _get_login_profile(self) -> str:
        try:
            config_file = self._session.get_config_variable('config_file')
            _config = load_config(config_file)
        except ConfigNotFound:
            _config = {'profiles': {}}

        available_profiles = list(_config['profiles'].keys())
        account_names = list(self.cloud_profiles['login_urls'].keys())
        login_profiles = list(set(available_profiles).intersection(
                                                                account_names))
        if len(login_profiles) == 0:
            logger.warning('\nNo cloud profile found, you can run'
                    ' `bombaat configure` command to setup a new profile.')
            sys.exit(1)
        msg = 'Select the cloud profile you would like to login'
        _answers = ask(msg, login_profiles)
        if _answers:
            _choice = _answers.get('choice').strip()
            return _choice

    @staticmethod
    def _choose_role(aws_roles: str) -> str:
        """Prompt user to choose role.

        :param role_arn: role amazon resource name
        :return: role arn selected by an user
        """
        if len(aws_roles) == 0:
            logger.warning('You do not have access to this cloud account.')
            sys.exit(1)

        if len(aws_roles) == 1:
            return aws_roles[0]

        short_names = [role.split('/')[1] for role in aws_roles]
        msg = 'Choose the role you would like to connect'
        _answers = ask(msg, short_names)
        if _answers:
            _choice = _answers.get('choice').strip().lower()
            for role in aws_roles:
                if _choice in role.lower(): return role
        else:
            # KeyboardInterrupts
            sys.exit(1)

    @staticmethod
    def _assume_role(role_arn: str,
                       principal_arn: str,
                       saml_response: str) -> dict:
        """Get temporary security credentials.

        Returns a set of temporary security credentials for users who have been
        authenticated via a SAML authentication response.

        :param role_arn: role amazon resource name
        :param principal_arn: principal name
        :param saml_response: SAML object to assume role with
        :param duration: session duration (default: 3600)
        :return: AWS session token
        """
        conn = boto3.client('sts')
        aws_session_token = conn.assume_role_with_saml(
            RoleArn=role_arn,
            PrincipalArn=principal_arn,
            SAMLAssertion=saml_response,
            DurationSeconds=28800,
        )
        return aws_session_token
