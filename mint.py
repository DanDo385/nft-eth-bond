# mint.py
import json
from web3 import Web3

# Load the metadata from the JSON file created by interact.py
with open('metadata.json', 'r') as json_file:
    metadata = json.load(json_file)

# Setup Web3 (Assuming you have the ABI and contract address)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
contract_address = 'YOUR_CONTRACT_ADDRESS_HERE'
abi = json.loads('YOUR_CONTRACT_ABI_HERE')
contract = w3.eth.contract(address=contract_address, abi=abi)

# You need to set the default account and private key if needed
w3.eth.default_account = w3.eth.accounts[0]

# Convert metadata to a tokenURI (perhaps uploading the metadata to IPFS and getting a URI, or using a service like Pinata)
tokenURI = "URL_TO_THE_METADATA"  # This should be the actual URL to the JSON metadata in IPFS or other service

# Interacting with the smart contract to mint an NFT
tx_hash = contract.functions.mintBondNFT(w3.eth.default_account, tokenURI).transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"NFT minted successfully with transaction receipt: {tx_receipt.transactionHash.hex()}")
