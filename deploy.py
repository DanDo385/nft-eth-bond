from web3 import Web3
import json

# Load the compiled contract ABI and bytecode
with open('compiled_code.json', 'r') as file:
    compiled_sol = json.load(file)

abi = compiled_sol['contracts']['Interaction.sol']['Interaction']['abi']
bytecode = compiled_sol['contracts']['Interaction.sol']['Interaction']['evm']['bytecode']['object']

# Connect to local Ethereum node (Ganache)
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Set the default account
w3.eth.default_account = w3.eth.accounts[0]

# Create the contract in Python
MyContract = w3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
tx_hash = MyContract.constructor().transact()

# Wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Save the contract address to a JSON file
contract_address = tx_receipt.contractAddress
with open('deployed_contract_address.json', 'w') as file:
    json.dump({'contract_address': contract_address}, file)

print(f"Contract deployed at address: {contract_address}")
