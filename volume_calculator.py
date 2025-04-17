def calculate_transaction_volume(initial_amount, growth_rate, movements):
    total_volume = 0
    current_amount = initial_amount

    for _ in range(movements):
        total_volume += current_amount
        current_amount *= (1 + growth_rate)

    return {
        'total_movements': movements,
        'total_volume': round(total_volume, 2)
    }

# Get user input
initial_amount = float(input("Enter the initial amount (USD): "))  # Convert to float
growth_rate = float(input("Enter the growth rate (as a decimal, e.g., 0.06 for 6%): "))  # Convert to float
movements = int(input("Enter the number of movements: "))  # Convert to int

result = calculate_transaction_volume(initial_amount, growth_rate, movements)
print(f"Total Movements: {result['total_movements']}, Total Volume: ${result['total_volume']}")

