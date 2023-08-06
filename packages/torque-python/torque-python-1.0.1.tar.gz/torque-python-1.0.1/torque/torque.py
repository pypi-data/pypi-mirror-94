import requests
from typing import Optional
from .torque_user import TorqueUser
from .version import __version__


class TorqueConfig:
    def __init__(self, api_url: Optional[str] = None):
        self.api_url = api_url or 'https://api.torque.cloud'


class CustomerConfig:
    def __init__(self, api_secret_key: str):
        if api_secret_key is None:
            raise AssertionError(f"CustomerConfig is missing 'api_secret_key'.")
        if not api_secret_key:
            raise AssertionError(f"'api_secret_key' provided to CustomerConfig cannot be empty string.")
        self.api_secret_key = api_secret_key


class Torque:
    def __init__(self, torque_config: TorqueConfig, customer_config: CustomerConfig):
        self.torque_config = torque_config
        self.api_secret_key = customer_config.api_secret_key

    def get_torque_user(self, auth_token: str, torque_user_id: str) -> TorqueUser:
        request_url = f'{self.torque_config.api_url}/m2m/v1/user/{torque_user_id}/auth'
        response = requests.post(
            request_url,
            headers={
                'Torque-API-Secret-Key': self.api_secret_key,
                'Torque-Python-Package-Version': __version__,
                'Authorization': 'Bearer ' + auth_token
            }
        )
        if response.status_code == 200:
            data = response.json()
            torque_user_data = data['user']
            return TorqueUser(
                torque_id=torque_user_data['id'],
                email=torque_user_data['email'],
                given_name=torque_user_data['given_name'],
                family_name=torque_user_data['family_name'],
                custom_data=torque_user_data['customer_specific_data']
            )
        raise AssertionError(f"Request to Torque API on '{request_url}' responded with status code '{response.status_code}' with message: {response.text or '<<empty response>>'}")
