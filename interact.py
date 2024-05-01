import numpy as np
from scipy.optimize import newton
import random
import datetime
import subprocess
from web3 import Web3
import json

def bond_price(yield_rate, coupon_rate, face_value, years_to_maturity, coupons_per_year):
    # Generate cash flows for each period, including the final face value payment
    cash_flows = np.array([coupon_rate * face_value] * years_to_maturity + [face_value])
    # Generate times for each cash flow, ensuring the final face value is accounted for
    times = np.array([i + 1 for i in range(years_to_maturity)] + [years_to_maturity])
    discount_factors = (1 + yield_rate) ** times
    return np.sum(cash_flows / discount_factors)

def calculate_bond_metrics(ytm, coupon_rate, face_value, years_to_maturity, coupons_per_year, market_price):
    basis_point = 0.0001
    price_up = bond_price(ytm + basis_point, coupon_rate, face_value, years_to_maturity, coupons_per_year)
    price_down = bond_price(ytm - basis_point, coupon_rate, face_value, years_to_maturity, coupons_per_year)
    dv01 = (price_up - price_down) / 2 / 100  # DV01 calculation adjusted

    price_up2 = bond_price(ytm + 2 * basis_point, coupon_rate, face_value, years_to_maturity, coupons_per_year)
    price_down2 = bond_price(ytm - 2 * basis_point, coupon_rate, face_value, years_to_maturity, coupons_per_year)
    convexity = (price_up2 - 2 * market_price + price_down2) / (market_price * basis_point ** 2) / 100

    return dv01, convexity

# Initialize Web3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.eth.default_account = w3.eth.accounts[0]

# User inputs
coupon_rate = float(input("Please enter the coupon rate (as a percentage, e.g., 5.5): "))
maturity_years = int(input("Please enter the maturity date of the bond (in years): "))
mint_nft = input("Do you want to mint this bond as an NFT? (y/n): ").lower()

# Bond and market specifics
market_price = round(random.uniform(99.80, 100.00), 2)
face_value = 100  # Standard face value
coupons_per_year = 1  # Assuming annual coupons

# Calculations
ytm = newton(lambda y: bond_price(y, coupon_rate / 100, face_value, maturity_years, coupons_per_year) - market_price, coupon_rate / 100)
dv01, convexity = calculate_bond_metrics(ytm, coupon_rate / 100, face_value, maturity_years, coupons_per_year, market_price)

# Payment schedule
today = datetime.date.today()
payment_schedule = [today.replace(year=today.year + i + 1) for i in range(maturity_years)]  # Exclude today

# Output results
print(f"\nBond Price: {market_price} (Randomly generated)")
print(f"Coupon Rate: {coupon_rate}%")
print(f"Yield to Maturity: {ytm * 100:.2f}%")
print(f"DV01 (Dollar Value of One Basis Point): ${dv01 * 10000:.2f}")
print(f"Convexity: {convexity:.2f}")
print("\nBond Payment Schedule:")
for date in payment_schedule:
    print(date.strftime("%m/%d/%Y"))

if mint_nft == 'y':
    print("Minting the bond as an NFT...")
    subprocess.run(["python", "mint.py"])  # Calling the mint.py script
else:
    print("No NFT minting requested.")
