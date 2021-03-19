import click
from web3 import Web3
# import asyncio
import json
import os
import logging as log
from dotenv import load_dotenv
from abis import AccessControlledOffChainAggregator
load_dotenv()

@click.command(help='Checks how much LINK you have to withdraw from OCR contracts.')
@click.option('--rdd-ocr-file', default=os.getenv('RDD_OCR_FILE'), help='rdd ocr file)')
@click.option('--ocr-address', default=os.getenv('OCR_ADDRESS'), help='address of OCR node)')
@click.option('--rpc-url', help='RPC connection if you don\'t have a environment variable.')
@click.option('--log-level', default='info', type=click.Choice(['info', 'debug']), help='Log Level')

def run(rdd_ocr_file, ocr_address, rpc_url, log_level):
    set_log_level(log_level)
    w3 = Web3(Web3.HTTPProvider(rpc_url)) if rpc_url else Web3(Web3.HTTPProvider(os.getenv('MAINNET_RPC_URL')))
    check_all_ocr_contracts(rdd_ocr_file, ocr_address, w3)
    
def check_all_ocr_contracts(rdd_ocr_file, ocr_address, w3):
    total = 0
    with open(rdd_ocr_file) as json_file:
        data = json.load(json_file)
        for feed in data:
            feed_name = feed['name']
            feed_address = feed['contractAddress']
            total += check_single_contract(feed_name, feed_address, ocr_address, w3)
    log.info("Total LINK to be withdrawn: {} LINK".format(total))
    return

def check_single_contract(feed_name, feed_address, ocr_address, w3):
    ocr_aggregator = w3.eth.contract(address=feed_address, abi=AccessControlledOffChainAggregator)
    amount_wei_available = ocr_aggregator.functions.owedPayment(ocr_address).call()
    if amount_wei_available != 0:
        amount_available = amount_wei_available / 1000000000000000000
        log.info("{} @ {} has {} LINK".format(
            feed_name, feed_address, amount_available
        ))
        return amount_available
    return 0

def set_log_level(log_level):
    if(log_level.lower() == 'info'):
        log.basicConfig(level=log.INFO)
    else:
        log.basicConfig(level=log.DEBUG)
    log.debug("Log level set to {}".format(log_level))

if __name__ == '__main__':
    run()
