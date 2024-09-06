from web3 import Web3
from django.conf import settings


class Web3Helper():
    '''
        Web3 Helper to connect with Infura account using web3 library
        and fetch the required details.
    '''
    @staticmethod
    def fetch_ethereum_balance(address):
        # Fetching Ethereum balance using wallet address.
        infura_key = settings.INFURA_KEY
        infura_url = f"https://mainnet.infura.io/v3/{infura_key}"
        web3 = Web3(Web3.HTTPProvider(infura_url))
        balance = web3.eth.get_balance(address)
        return balance
