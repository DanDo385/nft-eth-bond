# mint.py
import json
from web3 import Web3

# Load the metadata from the JSON file created by interact.py
with open('metadata.json', 'r') as json_file:
    metadata = json.load(json_file)

# Setup Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Load contract ABI and address
with open('compiled_code.json', 'r') as file:
    compiled_sol = json.load(file)
    # Adjust the following lines according to your contract's structure in the JSON file
    abi = compiled_sol['contracts']['BondNFT.sol']['BondNFT']['abi']

with open('deployed_contract_address.json', 'r') as file:
    deployed_info = json.load(file)
    contract_address = deployed_info['contract_address']

contract = w3.eth.contract(address=contract_address, abi=abi)

# Set the default account (the account that will mint the NFT)
w3.eth.default_account = w3.eth.accounts[0]

# Example URL to the metadata - this should be an actual URL to the JSON metadata, typically on IPFS
tokenURI = "https://ipfs.io/ipfs/QmbeU85nfYFxt34fv8LRo3q6yY8tyJjfv4Xj5A5eKgR5jr"

# Interacting with the smart contract to mint an NFT
tx_hash = contract.functions.mintBondNFT(w3.eth.default_account, tokenURI).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"NFT minted successfully with transaction receipt: {tx_receipt.transactionHash.hex()}")
