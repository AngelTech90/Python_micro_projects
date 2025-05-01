def calculate_growth_rate(selling_price, buying_price):
    return ((selling_price - buying_price) / buying_price) * 100

def calculate_transaction_volume(initial_amount, growth_rate, movements):
    total_volume = 0
    current_amount = initial_amount

    for _ in range(movements):
        total_volume += current_amount
        current_amount *= (1 + growth_rate / 100)  # Convert growth rate to a decimal

    return {
        'total_movements': movements,
        'total_volume': round(total_volume, 2),
        'incomes': round(current_amount, 2)
    }

# Get selling and buying prices from user
selling_price = float(input("Enter the selling price (USD): "))  # Convert to float
buying_price = float(input("Enter the buying price (USD): "))  # Convert to float

# Calculate earnings percentage
earnings_percentage = calculate_growth_rate(selling_price, buying_price)
print(f"Percentage of Earnings: {earnings_percentage:.2f}%")

# Get user input for initial amount and movements with validation
try:
    initial_amount = float(input("Enter the initial amount (USD): "))  # Convert to float
    movements = int(input("Enter the number of movements: "))  # Convert to int
except ValueError:
    print("Invalid input. Please enter numeric values.")
    exit(1)

# Calculate transaction volume
result = calculate_transaction_volume(initial_amount, earnings_percentage, movements)

# Calculate real earnings
real_earnings = round(result['incomes'] - initial_amount, 2)
print(f"Total Movements: {result['total_movements']}, Total Volume: ${result['total_volume']}, Total Incomes: ${real_earnings}")

