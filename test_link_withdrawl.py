# import link_withdrawl
import os
from web3 import Web3
import link_withdrawl
from abis import AccessControlledAggregator

TEST_FLUX_CONTRACT_ADDRESS = '0x8e1BB728b37832754A260D99B5467fE6d164c068'
TEST_NODE_ADDRESS = '0x165Ff6730D449Af03B4eE1E48122227a3328A1fc'


def test_get_chainlink_gas_price():
    w3 = Web3(Web3.HTTPProvider(os.getenv("MAINNET_RPC_URL")))
    gas_price = link_withdrawl.get_chainlink_gas_price(w3)
    assert isinstance(gas_price, int)


def test_calculate_link_from_flux_contract():
    # This test assumes I never pull from this contract...
    w3 = Web3(Web3.HTTPProvider(os.getenv("MAINNET_RPC_URL")))
    flux_contract = w3.eth.contract(
        address=TEST_FLUX_CONTRACT_ADDRESS, abi=AccessControlledAggregator)
    link_from_flux = link_withdrawl.calculate_link_from_flux_contract(
        flux_contract, TEST_NODE_ADDRESS, 0)
    assert link_from_flux > 0
    assert link_from_flux < 5


def test_withdraw_link():
    pass
