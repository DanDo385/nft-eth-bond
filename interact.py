from web3 import Web3
import datetime
import json

def calculate_ytm(price, face_value, coupon_rate, years):
    annual_coupon = face_value * (coupon_rate / 100)
    return ((annual_coupon + ((face_value - price) / years)) / ((face_value + price) / 2)) * 100

def calculate_dv01(price, face_value, coupon_rate, years, ytm):
    """ Calculate the DV01 of a bond.
        price: Current price of the bond
        face_value: Par value of the bond (assuming $100)
        coupon_rate: Annual coupon rate in percentage
        years: Years to maturity
        ytm: Yield to Maturity in percentage
    """
    # Calculate the modified duration as an approximation
    ytm_decimal = ytm / 100
    coupon_decimal = coupon_rate / 100
    duration = (1 + ytm_decimal) / ytm_decimal - (1 + ytm_decimal + years * (face_value - price) / price) / (coupon_decimal * (1 + ytm_decimal) ** years - ytm_decimal + years * (1 + ytm_decimal) ** (years - 1) * (face_value - price) / price)
    dv01 = duration * price / 10000  # DV01 calculation
    return dv01

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

# Calculate and display the Yield to Maturity
face_value = 100  # Assuming the face value of the bond is $100
ytm = calculate_ytm(random_price, face_value, coupon_rate, maturity_years)
print(f"Yield to Maturity: {ytm:.2f}%")

# Calculate and display the DV01
dv01 = calculate_dv01(random_price, face_value, coupon_rate, maturity_years, ytm)
print(f"DV01 (Dollar Value of One Basis Point Change): ${dv01:.4f}")
