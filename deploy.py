from web3 import Web3
import json

# Load the compiled contract data
with open('compiled_code.json') as file:
    compiled_sol = json.load(file)

# Get ABI and bytecode
abi = compiled_sol['contracts']['BondNFT.sol']['BondNFT']['abi']
bytecode = compiled_sol['contracts']['BondNFT.sol']['BondNFT']['evm']['bytecode']['object']

# Connect to local Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.eth.default_account = w3.eth.accounts[0]  # Set the default account

# Create the contract in Web3
BondNFT = w3.eth.contract(abi=abi, bytecode=bytecode)

# Deploy the contract
tx_hash = BondNFT.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Save the deployed contract address
contract_address = tx_receipt.contractAddress
with open('deployed_contract_address.json', 'w') as file:
    json.dump({'contract_address': contract_address}, file)

print(f"Contract deployed at address: {contract_address}")
