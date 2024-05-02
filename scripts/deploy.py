from web3 import Web3
import json
import os

# Load compiled contract
with open('./build/compiled_code.json', 'r') as file:
    compiled_sol = json.load(file)

contract_interface = compiled_sol['contracts']['BondNFT.sol']['BondPriceGenerator']

# Connect to local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.eth.default_account = w3.eth.accounts[0]

# Deploy contract
BondNFT = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['evm']['bytecode']['object'])
tx_hash = BondNFT.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Save the contract address to a JSON file in the build folder
with open('./build/deployed_contract_address.json', 'w') as file:
    json.dump({'contract_address': tx_receipt.contractAddress}, file)

print(f"Contract deployed at address: {tx_receipt.contractAddress}")
