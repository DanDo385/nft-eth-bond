from web3 import Web3
import datetime
import json

# Setup web3 connection to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Load the contract ABI and Address
with open('deployed_contract_address.json', 'r') as file:
    deployed_info = json.load(file)
contract_address = deployed_info['contract_address']

with open('compiled_code.json', 'r') as file:
    compiled_sol = json.load(file)
abi = compiled_sol['contracts']['BondPriceGenerator.sol']['BondPriceGenerator']['abi']

# Create the contract instance with Web3
contract = w3.eth.contract(address=contract_address, abi=abi)

# Fetch the random price from the contract
random_price = contract.functions.randomPrice().call()

# Prompt for coupon rate
coupon_rate = float(input("Please enter the coupon rate (as a percentage, e.g., 5.5): "))

# Prompt for maturity date of the bond (in years)
maturity_years = int(input("Please enter the maturity date of the bond (in years): "))

# Current date
today = datetime.date.today()

# Create payment schedule
payment_schedule = [today.replace(year=today.year + i) for i in range(maturity_years + 1)]

# Display bond details
print(f"\nBond Price: {random_price} (Randomly generated)")
print(f"Coupon Rate: {coupon_rate}%")

# Display the payment schedule
print("\nBond Payment Schedule:")
for date in payment_schedule:
    print(date.strftime("%m/%d/%Y"))
