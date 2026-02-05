def calculate_usdt_arbitrage_potential(
    selling_price: float,
    buying_price: float,
    cycles: int,
    iterations: int,
    initial_capital: float
) -> tuple:
    """
    Calculate potential capital and earnings from USDT arbitrage cycles.

    Args:
        selling_price (float): Price at which you sell USDT (higher price).
        buying_price (float): Price at which you buy USDT (lower price).
        cycles (int): Number of buy/sell cycles per iteration.
        iterations (int): Number of iterations to repeat cycles.
        initial_capital (float): Starting capital in USD.

    Returns:
        tuple: (final_capital, total_earnings) both in USD.
    """
    capital = initial_capital
    total_earnings = 0.0

    if buying_price <= 0 or selling_price <= 0:
        raise ValueError("Prices must be positive numbers.")
    if buying_price >= selling_price:
        raise ValueError("Buying price must be less than selling price for profit.")

    for iteration in range(1, iterations + 1):
        for cycle in range(1, cycles + 1):
            # Earnings per cycle = capital * (price difference) / buying_price
            earnings = capital * (selling_price - buying_price) / buying_price
            capital += earnings
            total_earnings += earnings

        print(f"Iteration {iteration}: Capital = ${capital:.4f}, Earnings so far = ${total_earnings:.4f}")

    return capital, total_earnings


# Example usage:
if __name__ == "__main__":
    selling_price = float(input("Enter selling price of USDT (higher price): "))
    buying_price = float(input("Enter buying price of USDT (lower price): "))
    cycles = int(input("Enter number of cycles per iteration: "))
    iterations = int(input("Enter number of iterations: "))
    initial_capital = float(input("Enter initial capital in USD: "))

    final_capital, total_earnings = calculate_usdt_arbitrage_potential(
        selling_price, buying_price, cycles, iterations, initial_capital
    )

    print("\n=== Final Results ===")
    print(f"Final capital (capital + earnings): ${final_capital:.4f}")
    print(f"Total earnings: ${total_earnings:.4f}")

