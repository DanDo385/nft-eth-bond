import json
from web3 import Web3

# Setup Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Load the metadata from the JSON file created by interact.py
with open('../build/metadata.json', 'r') as json_file:
    metadata = json.load(json_file)

# Load contract ABI and address from build folder
with open('../build/compiled_code.json', 'r') as file:
    compiled_sol = json.load(file)
    abi = compiled_sol['contracts']['BondNFT.sol']['BondNFT']['abi']

with open('../build/deployed_contract_address.json', 'r') as file:
    deployed_info = json.load(file)
    contract_address = deployed_info['contract_address']

contract = w3.eth.contract(address=contract_address, abi=abi)

# Set the default account (the account that will mint the NFT)
w3.eth.default_account = w3.eth.accounts[0]

# TokenURI should point to the actual metadata location, e.g., IPFS
tokenURI = metadata['image']  # Assuming the image URL in metadata is used as TokenURI

# Interacting with the smart contract to mint an NFT
tx_hash = contract.functions.mintBondNFT(w3.eth.default_account, tokenURI).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"NFT minted successfully with transaction receipt: {tx_receipt.transactionHash.hex()}")
