# Withdraw funds from fluxmonitor

View how much LINK you have and withdraw from your flux monitor contracts!

### Highlights

- A `link-minimum-balance` so you only withdraw those with high enough LINK.
- Based off your contracts folder in `reference-data-directory`.
- A `dry-run` default feature so you can view before withdrawing. 
- Withdraw in one command!

Using your reference data directory! It also has a quick way for you to just view how much LINK you have. There is a minimum balance flag so that it will only withdraw or show you want to withdraw if the minimum is higher than that.

## Setup

1. Python
You'll need [python installed](https://www.python.org/downloads/).

2. Clone this repo

```bash
git clone <this-repo>
cd flux-link
```

3. Install requirements
```
pip install -r requirements.txt
```
3. Environment variables

Required:
- `MAINNET_RPC_URL`
You'll need at least a `MAINNET_RPC_URL`. This is the http endpoint to access the ETH network. You can get one from a service like Infura or Alchemy. 

Optional:
- `NODE_ADDRESS`: The address of your node.
- `ADMIN_ADDRESS`: The wallet associated with your node, and where you will be withdrawing to. 
- `RDD`: You reference data directory of mainnet contracts.

If you're unfamiliar with setting environment variables, feel free to follow the sample in the provided `.env` file. 


## Useage
```bash
python link_withdrawl.py --help

Usage: link_withdrawl.py [OPTIONS]

  Checks how much LINK you have to withdraw from smartcontracts. And can
  withdraw.

Options:
  --node-address TEXT             The address of the node
  --recipent-address TEXT         The address you want to return the LINK to
  --rdd-contracts-directory TEXT  rdd directory)
  --link-minimum-balance INTEGER  If you are withdrawing
  --private-key TEXT              If you are withdrawing
  --rpc-url TEXT                  RPC connection
  --gas-price INTEGER             Optional if you don't want to use the
                                  Chainlink Fast gas feed

  --dry-run / --withdraw          If want want to actually withdraw or not
  --regular / --slow-mode         Not active yet...
  --log-level [info|debug]        Log Level
  --help                          Show this message and exit.
```
To see how much LINK you could pull.

## Viewing LINK amounts

```bash
python link_withdrawl.py --link-minimum-balance 0 --node-address 0x165Ff6730D449Af03B4eE1E48122227a3328A1fc --rdd-contracts-directory /Users/patrick/code/reference-data-directory/mainnet/contracts/
```
**Note - `dry-run` is default to true, so it won't pull any LINK out unless you add the flag `--withdraw`

You'll get an output like:

```
INFO:root:Getting LINK amounts for node address 0x165Ff6730D449Af03B4eE1E48122227a3328A1fc
INFO:root:Address 0x955bbbB41b6FCe89aD3CdE8f74F964e99036BD52 has 202.34 LINK
INFO:root:Address 0x8e1BB728b37832754A260D99B5467fE6d164c068 has 1.9 LINK
INFO:root:Address 0xb58b218365CD12AD765bA8A9F88E881D2b2a01C2 has 703.03 LINK
.
.
INFO:root:Address 0xB8169f6D97c66c50Ef27B7b1b3FB2875d2b036a4 has 110.25 LINK
INFO:root:Address 0xA3eAeC3AB66048E6F3Cf23D81881a3fcd9A3D2ED has 322.09 LINK
INFO:root:Total 3953.060000000001 LINK
```

## Withdrawing

Assuming you have an `RDD` environment variable. 

```bash
python link_withdrawl.py --link-minimum-balance 0 --node-address 0x165Ff6730D449Af03B4eE1E48122227a3328A1fc --recipent-address 888888888888 --private-key 777777777777777 --withdraw

INFO:root:Getting LINK amounts for node address 0x165Ff6730D449Af03B4eE1E48122227a3328A1fc
INFO:root:Address 0x955bbbB41b6FCe89aD3CdE8f74F964e99036BD52 has 202.34 LINK
INFO:root:Using 230000000000 for gas.
INFO:root:Sending transaction...
INFO:root:Withdrawing LINK with tx hash: 0x2ce084e9e307b7b3d3ed95dd88a194c001766716ef1cbae9582971f7f8faf5fc
.
.
.
```
You don't have to set gas price, as it will grab from the chainlink contract. However, sometimes it might make sense to add the gas price anyway. Be sure to add the gas price in gwei if you do with the `--gas-price` flag. 

You can then pop the tx hash into something like Etherscan. 

Adding the environment variables or defaults makes like easier.

# Testing

```bash
pytest
```

Hope you enjoy!
