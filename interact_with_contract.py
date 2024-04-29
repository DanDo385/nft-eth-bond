from web3 import Web3
import json
import sys

# Load the compiled contract ABI
with open('compiled_code.json', 'r') as file:
    compiled_sol = json.load(file)

# ABI and Bytecode
abi = compiled_sol['contracts']['Interaction.sol']['Interaction']['abi']

# Connect to local Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Set the default account
w3.eth.default_account = w3.eth.accounts[0]

# The contract's address (This needs to be replaced with the actual deployed address)
contract_address = 'REPLACE_WITH_YOUR_CONTRACT_ADDRESS'

# Creating an instance of the deployed contract
contract = w3.eth.contract(address=contract_address, abi=abi)

# Input from the command line
if len(sys.argv) != 2:
    print("Usage: python3 interact_with_contract.py <number>")
    sys.exit(1)

new_number = int(sys.argv[1])

# Call the setMyNumber function
tx_hash = contract.functions.setMyNumber(new_number).transact()
w3.eth.wait_for_transaction_receipt(tx_hash)

# Call the getMyNumber function
result = contract.functions.getMyNumber().call()

print(f'The number stored in the smart contract is now: {result}')
