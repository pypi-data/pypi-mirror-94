#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Cloud Profile Management"""

import os
import logging
from distutils.util import strtobool

from blessed import Terminal
from botocore.configloader import load_config
from botocore.exceptions import ProfileNotFound
from botocore.session import Session, get_session
from awscli.customizations.configure.writer import ConfigFileWriter

from bombaat.utils import ask
from bombaat.utils import read_yaml
from bombaat.utils import MorningSun
from bombaat.driver import check_driver
from bombaat.driver import download_driver
from bombaat.utils import get_cloud_profiles

logger = logging.getLogger(__name__)

class Configure(object):
    """Configure cloud profiles."""

    # If you want to add new values to prompt, update this list here.
    VALUES_TO_PROMPT = [
      # (logical_name, config_name, prompt_text)
      ('username', 'Enter Azure SSO username (email)'),
      ('default', "Do you want to make it the 'default' profile? (True/False)"),
    ]

    def __init__(self) -> None:
        super(Configure, self).__init__()

        if not check_driver():
            logger.warning('\nConfiguration files missing, please run '
                '`bombaat update all` to install latest configuration files.')

        self._cloud_profile = self._get_cloud_account_name()
        self._session = Session(profile=self._cloud_profile)
        self._config_writer = ConfigFileWriter()

    def main(self) -> None:
        """Main function."""
        new_values = {}
        try:
            config = self._session.get_scoped_config()
        except ProfileNotFound:
            config = {}
        for config_name, prompt_text in self.VALUES_TO_PROMPT:
            current_value = config.get(config_name)
            new_value = self._get_value(current_value, prompt_text)
            if new_value is not None and new_value != current_value and \
                                                      config_name == 'default':
                if new_value.lower() == 'true':
                    available_profiles = self._session.available_profiles
                    for profile in available_profiles:
                        self._session = Session(profile=profile)
                        profile_config = self._session.get_scoped_config()
                        default_val = profile_config.get('default')
                        if default_val is not None and \
                                                bool(strtobool(default_val)):
                            update_default_values = {}
                            update_default_values['default'] = False
                            self._update_config_file(
                                                update_default_values, profile)
                    new_values[config_name] = bool(strtobool(new_value))
                else:
                    new_values[config_name] = False
            if new_value is not None and new_value != current_value and \
                                                    config_name == 'username':
                new_values[config_name] = new_value

        self._update_config_file(new_values, self._cloud_profile)
        configure_default_profile()

    def _get_cloud_account_name(self) -> str:
        """Get cloud profile from user.

        :param str file_name: yaml config file which has cloud profiles.
        :return: Cloud account name chosen by user.

        Yaml file should be in the following format:
        Example:
                login_urls:
                  devcloud:
                    name: 'Friendly Cloud Name'
                    login_url: 'login url collected from Azure AD'
                  qacloud:
                    name: 'Friendly Cloud Name'
                    login_url: 'login url collected from Azure AD'
                  prodcloud:
                    name: 'Friendly Cloud Name'
                    login_url: 'login url collected from Azure AD'

        You can add 'n' number of account information.
        """
        account_names = get_cloud_profiles()
        friendly_names = list()
        for account in account_names['login_urls']:
            friendly_names.append(account_names['login_urls'][account]['name'])
        msg = 'Choose the cloud account you would like to configure'
        _answers = ask(msg, friendly_names)
        if _answers:
            choice = _answers.get('choice').strip()
            for key, val in account_names['login_urls'].items():
                if val['name'] == choice:
                    return key

    def _get_value(self, current_value, prompt_text='') -> str:
        """Manage user inputs.

        :param str current_value: value currently configured
        :param str prompt_text: a string
        :return:
        """
        response = input(f'{prompt_text} [{current_value}]: ')
        if not response:
            # If the user hits enter, we return a value of None
            # instead of an empty string.  That way we can determine
            # whether or not a value has changed.
            response = None
        return response

    def _update_config_file(self, new_values, profile) -> int:
        """Setup config file.

        :param dict new_values: dictionary containing config values
        :param str profile: Name of the cloud profile
        :return:
        """
        config_filename = os.path.expanduser(
            self._session.get_config_variable('config_file'))
        if new_values:
            new_values['__section__'] = ('profile {}'.format(profile))
            self._config_writer.update_config(new_values, config_filename)
        return 0


def write_credentials(session, new_values, profile=None) -> None:
    """Credentials Writer."""

    credential_values = {}
    if 'AccessKeyId' in new_values:
        credential_values['aws_access_key_id'] = new_values.pop('AccessKeyId')
    if 'SecretAccessKey' in new_values:
        credential_values['aws_secret_access_key'] = new_values.pop(
                                                            'SecretAccessKey')
    if 'SessionToken' in new_values:
        credential_values['aws_security_token'] = new_values.pop('SessionToken')

    if credential_values:
        if profile is not None:
            credential_values['__section__'] = profile
        credentials_filename = os.path.expanduser(
            session.get_config_variable('credentials_file'))
        config_writer = ConfigFileWriter()
        config_writer.update_config(credential_values,
                                          credentials_filename)


def configure_default_profile() -> None:
    """Configure default profile."""

    session = get_session()
    config_file = session.get_config_variable('config_file')
    config = load_config(config_file)
    cloud_profiles = get_cloud_profiles()

    available_profiles = list(config['profiles'].keys())
    account_names = list(cloud_profiles['login_urls'].keys())
    login_profiles = list(set(available_profiles).intersection(account_names))

    new_values = dict()
    for profile in login_profiles:
        if config['profiles'][profile].get('default') is not None:
            if bool(strtobool(config['profiles'][profile]['default'])):
                profile_values = session.full_config['profiles'][profile]
                if 'aws_access_key_id' in profile_values:
                    new_values['AccessKeyId'] = profile_values.pop(
                                                          'aws_access_key_id')
                if 'aws_secret_access_key' in profile_values:
                    new_values['SecretAccessKey'] = profile_values.pop(
                                                      'aws_secret_access_key')
                if 'aws_security_token' in profile_values:
                    new_values['SessionToken'] = profile_values.pop(
                                                         'aws_security_token')
                write_credentials(session, new_values)
