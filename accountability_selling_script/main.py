from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('accountability_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_decimal_input(prompt, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            user_input = input(prompt).strip()
            decimal_value = Decimal(user_input)
            quantized_value = decimal_value.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
            return quantized_value
        except (ValueError, InvalidOperation):
            print(f"Invalid input! Please enter a valid decimal number (max 4 decimal places).")
            if attempt == max_attempts - 1:
                print("Too many invalid attempts. Using default value 0.0000")
                return Decimal('0.0000')
    return Decimal('0.0000')

def get_string_input(prompt):
    return input(prompt).strip()

def calculate_commission(capital_ves):
    commission_rate = Decimal('0.00003')  # 0.003%
    return (capital_ves * commission_rate).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)

def main():
    print("=== ACCOUNTABILITY SCRIPT ===")
    print("This script will run endlessly for trading calculations.")
    print("Use Ctrl+C to exit at any time.\n")
    
    capital_ves = None
    buying_price = None
    commission_pay = None
    final_value = None
    start_var = None
    first_iteration = True
    
    try:
        while True:
            print("\n" + "="*50)
            print(f"ITERATION - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*50)
            
            start_var = get_string_input("Enter start variable (string): ")
            logger.info(f"Start variable set to: {start_var}")
            
            if first_iteration:
                print("\n--- INITIAL SETUP ---")
                capital_ves = get_decimal_input("Enter capital VES amount: $")
                logger.info(f"Initial capital VES set to: ${capital_ves}")
                first_iteration = False
            else:
                change_capital = input("\nDo you want to change capital VES value? (yes/no): ").strip().lower()
                if change_capital in ['yes', 'y']:
                    capital_ves = get_decimal_input("Enter new capital VES amount: $")
                    logger.info(f"Capital VES updated to: ${capital_ves}")
                elif change_capital in ['no', 'n']:
                    selling_price = get_decimal_input("Enter selling price for final calculation: $")
                    commission_pay = calculate_commission(capital_ves)
                    
                    if selling_price > 0:
                        final_value = (capital_ves - commission_pay) / selling_price
                        final_value = final_value.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
                        
                        print(f"\n--- FINAL CALCULATION ---")
                        print(f"Capital VES: ${capital_ves}")
                        print(f"Commission Pay: ${commission_pay}")
                        print(f"Selling Price: ${selling_price}")
                        print(f"Final Value: {final_value}")
                        
                        logger.info(f"Final calculation - Capital: ${capital_ves}, Commission: ${commission_pay}, "
                                  f"Selling Price: ${selling_price}, Final Value: {final_value}")
                    else:
                        print("Error: Selling price must be greater than 0")
                        logger.error("Invalid selling price (must be > 0)")
                    
                    continue
            
            buying_price = get_decimal_input("Enter buying price: $")
            logger.info(f"Buying price set to: ${buying_price}")
            
            commission_pay = calculate_commission(capital_ves)
            
            print(f"\n--- CURRENT VALUES ---")
            print(f"Start Variable: {start_var}")
            print(f"Capital VES: ${capital_ves}")
            print(f"Buying Price: ${buying_price}")
            print(f"Commission Pay (0.003%): ${commission_pay}")
            
            available_capital = capital_ves - commission_pay
            print(f"Available Capital (after commission): ${available_capital}")
            
            # Calculate potential units WITH commission
            if buying_price > 0:
                potential_units_with_commission = available_capital / buying_price
                potential_units_with_commission = potential_units_with_commission.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
                print(f"Potential units/shares to buy (with commission): {potential_units_with_commission}")
                
                # Calculate potential units WITHOUT commission
                potential_units_without_commission = capital_ves / buying_price
                potential_units_without_commission = potential_units_without_commission.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
                print(f"Potential units/shares to buy (without commission): {potential_units_without_commission}")
                
                logger.info(f"Transaction summary - Available: ${available_capital}, "
                          f"Potential units (with commission): {potential_units_with_commission}, "
                          f"Potential units (without commission): {potential_units_without_commission}")
            else:
                print("Error: Buying price must be greater than 0")
                logger.error("Invalid buying price (must be > 0)")
            
            print(f"\nPress Enter to continue to next iteration...")
            input()
            
    except KeyboardInterrupt:
        print(f"\n\nScript terminated by user.")
        logger.info("Script terminated by user (Ctrl+C)")
    except Exception as e:
        print(f"An error occurred: {e}")
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()

