import datetime

# Prompt for maturity date of the bond (in years)
try:
    maturity_years = int(input("Please enter the maturity date of the bond (in years): "))
except ValueError:
    print("Error: Please enter a valid integer for maturity years.")
    exit(1)

# Current date
today = datetime.date.today()

# Create payment schedule
payment_schedule = [today.replace(year=today.year + i) for i in range(maturity_years + 1)]

# Display the payment schedule
print("\nBond Payment Schedule:")
for date in payment_schedule:
    print(date.strftime("%m/%d/%Y"))
