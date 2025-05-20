import random

def generate_fake_venezuela_number():
    # Venezuela country code
    country_code = "+58"
    
    # Generate a random mobile prefix (4XX)
    mobile_prefix = "4" + str(random.randint(0, 99)).zfill(2)
    
    # Generate the remaining 7 digits
    number_part = ''.join([str(random.randint(0, 9)) for _ in range(7)])
    
    # Combine to form the full phone number
    fake_number = f"{country_code} {mobile_prefix} {number_part}"
    
    return fake_number

# Generate and print a fake Venezuelan phone number
print("Fake Venezuelan Phone Number:", generate_fake_venezuela_number())

