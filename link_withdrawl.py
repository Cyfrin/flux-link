import click
from pathlib import Path
from web3 import Web3
import web3
# import asyncio
import os
import logging as log
from dotenv import load_dotenv
from abis import AccessControlledAggregator, PriceFeedABI
import time
load_dotenv()


@click.command(help='Checks how much LINK you have to withdraw from smartcontracts. And can withdraw.')
@click.option('--node-address', default=os.getenv('NODE_ADDRESS'),  help='The address of the node')
@click.option('--recipent-address', default=os.getenv('ADMIN_ADDRESS'), help='The address you want to return the LINK to')
@click.option('--rdd-contracts-directory', default=os.getenv('RDD'), help='rdd directory)')
@click.option('--link-minimum-balance', default=0, help='If you are withdrawing')
@click.option('--private-key', help='If you are withdrawing')
@click.option('--rpc-url', help='RPC connection if you don\'t have a environment variable.')
@click.option('--gas-price', default=None, type=int, help='Optional if you don\'t want to use the Chainlink Fast gas feed')
@click.option('--dry-run/--withdraw', default=True, help='If want want to actually withdraw or not')
@click.option('--regular-speed/--slow-mode', default=True, help='Enters debugger ipdb mode for sending transactions. `quit()` to exit. ')
@click.option('--log-level', default='info', type=click.Choice(['info', 'debug']), help='Log Level')
def link_withdrawl(node_address, recipent_address, rdd_contracts_directory, link_minimum_balance,
                   private_key, rpc_url, gas_price, dry_run, regular_speed, log_level):
    set_log_level(log_level)
    w3 = Web3(Web3.HTTPProvider(rpc_url)
              ) if rpc_url else Web3(Web3.HTTPProvider(os.getenv('MAINNET_RPC_URL')))
    total_amount_withdrawn = get_link_and_withdraw_from_flux_contracts(
        node_address, rdd_contracts_directory, link_minimum_balance, w3, recipent_address, private_key, gas_price,
        regular_speed, dry_run)
    log.info("All set! {} LINK total".format(total_amount_withdrawn))


def get_link_and_withdraw_from_flux_contracts(node_address, rdd_contracts_directory, link_minimum_balance,
                                              w3, recipent_address, private_key, gas_price, regular_speed, dry_run):
    p = Path(rdd_contracts_directory)
    contract_paths = list(p.glob('**/*'))
    total_withdrawable_link = 0
    log.info("Getting LINK amounts for node address {}".format(node_address))
    for contract_path in contract_paths:
        contract_address = contract_path.name.split('.json')[0]
        flux_contract = w3.eth.contract(
            address=contract_address, abi=AccessControlledAggregator)
        link_amount_from_flux_contract = calculate_link_from_flux_contract(
            flux_contract, node_address, link_minimum_balance)
        if dry_run is False and link_amount_from_flux_contract >= link_minimum_balance:
            withdraw_link(flux_contract, w3, node_address,
                          recipent_address, private_key, gas_price, regular_speed, amount=link_amount_from_flux_contract)
        total_withdrawable_link = total_withdrawable_link + link_amount_from_flux_contract
    log.info("Total " + str(total_withdrawable_link) + " LINK")
    return total_withdrawable_link


def withdraw_link(flux_contract, w3, node_address, recipent_address, private_key, gas_price, regular_speed, amount=0):
    if amount <= 0:
        return None
    if regular_speed is False:
        import ipdb
        ipdb.set_trace()
    if gas_price is None:
        gas_price = get_chainlink_gas_price(w3)
    nonce = w3.eth.getTransactionCount(recipent_address)
    transaction = flux_contract.functions.withdrawPayment(node_address, recipent_address, w3.toWei(amount, 'ether')
                                                          ).buildTransaction({'chainId': 1,
                                                                              'gasPrice': gas_price,
                                                                              'from': recipent_address,
                                                                              'nonce': nonce})
    signed_txn = w3.eth.account.sign_transaction(
        transaction, private_key=private_key)
    log.info("Sending transaction...")
    tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    log.info("Withdrawing LINK with tx hash: {}".format(tx_hash.hex()))
    # adding just to not have to deal with nonce stuff
    tx_hash.wait(2)
    return tx_hash.hex()


def get_chainlink_gas_price(w3):
    gasPriceAddress = '0x169E633A2D1E6c10dD91238Ba11c4A708dfEF37C'
    contract = w3.eth.contract(address=gasPriceAddress, abi=PriceFeedABI)
    latestData = contract.functions.latestRoundData().call()
    log.info("Using {} for gas.".format(latestData[1]))
    return latestData[1]


def calculate_link_from_flux_contract(flux_contract, node_address, link_minimum_balance):
    try:
        amount_to_withdraw = flux_contract.functions.withdrawablePayment(
            node_address).call() / 1000000000000000000
        if amount_to_withdraw > link_minimum_balance:
            log.info("Address {} has {} LINK".format(
                flux_contract.address, amount_to_withdraw))
            return amount_to_withdraw
    except web3.exceptions.ContractLogicError:
        log.debug("Address {} had a logic error.".format(
            flux_contract.address))
        return 0
    return 0


def set_log_level(log_level):
    if(log_level.lower() == 'info'):
        log.basicConfig(level=log.INFO)
    else:
        log.basicConfig(level=log.DEBUG)
    log.debug("Log level set to {}".format(log_level))


if __name__ == '__main__':
    link_withdrawl()
