import random
import datetime
from web3 import Web3
import json

def calculate_ytm(price, face_value, coupon_rate, years):
    annual_coupon = face_value * (coupon_rate / 100)
    return ((annual_coupon + ((face_value - price) / years)) / ((face_value + price) / 2)) * 100

def calculate_dv01(price, face_value, coupon_rate, years, ytm):
    ytm_decimal = ytm / 100
    coupon_decimal = coupon_rate / 100
    duration = (1 + ytm_decimal) / ytm_decimal - (1 + ytm_decimal + years * (face_value - price) / price) / (coupon_decimal * (1 + ytm_decimal) ** years - ytm_decimal + years * (1 + ytm_decimal) ** (years - 1) * (face_value - price) / price)
    dv01 = duration * price / 10000  # Calculate DV01
    return dv01 * 100  # Multiply DV01 by 100 for scaling

# Setup web3 connection to Ganache
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.eth.default_account = w3.eth.accounts[0]  # Set the default account

# Random price generation between 99.80 and 100.00, rounded to two decimals
random_price = round(random.uniform(99.80, 100.00), 2)

# Prompt for coupon rate
coupon_rate = float(input("Please enter the coupon rate (as a percentage, e.g., 5.5): "))

# Prompt for maturity date of the bond (in years)
maturity_years = int(input("Please enter the maturity date of the bond (in years): "))

# Ask if the user wants to mint the bond as an NFT
mint_nft = input("Do you want to mint this bond as an NFT? (y/n): ").lower()

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
print(f"DV01 (Dollar Value of One Basis Point Change x 100): ${dv01:.2f}")

if mint_nft == 'y':
    # Call smart contract function to mint NFT
    print("Minting the bond as an NFT...")
    # Assume function mintNFT() exists and mint the NFT
    # You need to add the actual code that interacts with your smart contract here
    # Example:
    # tx_hash = contract.functions.mintNFT(parameters_if_any).transact()
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print("NFT minted successfully!")
else:
    print("No NFT minting requested.")
