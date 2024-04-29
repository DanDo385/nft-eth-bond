from scipy.optimize import newton
import numpy as np
from web3 import Web3
import datetime
import json

# Bond details
face_value = 100  # Assuming standard face value
coupon_rate = 0.07
years_to_maturity = 10
market_price = 99.90
annual_coupon_payment = face_value * coupon_rate
coupons_per_year = 1

# Function to calculate bond price given a yield
def bond_price(yield_rate):
    coupon_pv = annual_coupon_payment * ((1 - (1 + yield_rate) ** (-years_to_maturity * coupons_per_year)) / yield_rate)
    par_value_pv = face_value / ((1 + yield_rate) ** (years_to_maturity * coupons_per_year))
    return coupon_pv + par_value_pv

# Calculate YTM using newton's method to find the root where bond price equals market price
ytm = newton(lambda y: bond_price(y) - market_price, coupon_rate)

# Calculate DV01
basis_point = 0.0001
price_up = bond_price(ytm + basis_point)
price_down = bond_price(ytm - basis_point)
dv01 = (price_up - price_down) / 2

# Setup web3 connection to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.eth.default_account = w3.eth.accounts[0]  # Set the default account

# Load the contract ABI and Address
with open('deployed_contract_address.json', 'r') as file:
    deployed_info = json.load(file)
contract_address = deployed_info['contract_address']

with open('compiled_code.json', 'r') as file:
    compiled_sol = json.load(file)
abi = compiled_sol['contracts']['BondPriceGenerator.sol']['BondPriceGenerator']['abi']

# Create the contract instance with Web3
contract = w3.eth.contract(address=contract_address, abi=abi)

# Trigger random number generation
tx_hash = contract.functions.requestRandomPrice().transact({'from': w3.eth.default_account})
w3.eth.wait_for_transaction_receipt(tx_hash)

# Fetch the random price from the contract
random_price = contract.functions.randomPrice().call()

# Display bond details
print(f"\nRandom Bond Price: {random_price} (from smart contract)")
print(f"Coupon Rate: {coupon_rate * 100}%")
print(f"Yield to Maturity: {ytm * 100:.2f}%")
print(f"DV01: ${dv01:.4f}")
