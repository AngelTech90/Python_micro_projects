import random 



def generate_password(password_range):
    
    chars_password = "09?¡!¿12345678+*-.,:;_mnbvcxzñlkjhgfdsapoiuytrewqQWERTYUIOPÑLKJHGFDSAMNBVCXZ/|%&()="
    
    password = ''.join(random.choice(chars_password) for _ in range(password_range))
    
    return password
    
    
password_range = int(input("Give me your password range: "))

print(generate_password(password_range))