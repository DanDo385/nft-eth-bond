import numpy as np
from scipy.optimize import newton
import random
import datetime

# Function to calculate the present value of bond cash flows given a yield
def bond_price(yield_rate, coupon_rate, face_value, years_to_maturity, coupons_per_year):
    cash_flows = np.array([coupon_rate * face_value] * (years_to_maturity * coupons_per_year) + [face_value])
    times = np.array([1 + i for i in range(years_to_maturity * coupons_per_year)] + [years_to_maturity])
    discount_factors = (1 + yield_rate) ** times
    return np.sum(cash_flows / discount_factors)

# Calculate YTM using the Newton-Raphson method
def calculate_ytm(market_price, coupon_rate, face_value, years_to_maturity, coupons_per_year):
    ytm_func = lambda y: bond_price(y, coupon_rate, face_value, years_to_maturity, coupons_per_year) - market_price
    return newton(ytm_func, coupon_rate)

# Calculate DV01
def calculate_dv01(ytm, coupon_rate, face_value, years_to_maturity, coupons_per_year):
    ytm += 0.0001  # increase by one basis point
    price_up = bond_price(ytm, coupon_rate, face_value, years_to_maturity, coupons_per_year)
    ytm -= 0.0002  # decrease by two basis points from original
    price_down = bond_price(ytm, coupon_rate, face_value, years_to_maturity, coupons_per_year)
    return (price_up - price_down) / 2 * 100  # multiply by 100 to scale the DV01

# Calculate Convexity
def calculate_convexity(ytm, coupon_rate, face_value, years_to_maturity, coupons_per_year, market_price):
    basis_point = 0.0001
    price_up = bond_price(ytm + 2 * basis_point, coupon_rate, face_value, years_to_maturity, coupons_per_year)
    price_down = bond_price(ytm - 2 * basis_point, coupon_rate, face_value, years_to_maturity, coupons_per_year)
    convexity = (price_up - 2 * market_price + price_down) / (market_price * basis_point ** 2)
    return convexity

# Main script execution
random_price = round(random.uniform(99.80, 100.00), 2)  # Random market price
coupon_rate = float(input("Please enter the coupon rate (as a percentage, e.g., 5.5): "))
maturity_years = int(input("Please enter the maturity date of the bond (in years): "))
today = datetime.date.today()
payment_schedule = [today.replace(year=today.year + i) for i in range(maturity_years + 1)]

# Display the bond details and payment schedule
print(f"\nBond Price: {random_price} (Randomly generated)")
print(f"Coupon Rate: {coupon_rate}%\n")
print("Bond Payment Schedule:")
for date in payment_schedule:
    print(date.strftime("%m/%d/%Y"))

# Yield to Maturity and DV01
face_value = 100
coupons_per_year = 1
ytm = calculate_ytm(random_price, coupon_rate / 100, face_value, maturity_years, coupons_per_year)
dv01 = calculate_dv01(ytm, coupon_rate / 100, face_value, maturity_years, coupons_per_year)
convexity = calculate_convexity(ytm, coupon_rate / 100, face_value, maturity_years, coupons_per_year, random_price)
print(f"\nYield to Maturity: {ytm * 100:.2f}%")
print(f"DV01 (Dollar Value of One Basis Point Change x 100): ${dv01:.2f}")
print(f"Convexity: {convexity:.4f}")
