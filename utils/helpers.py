# I use Python mainly for test logic, utilities, and validations.

def generate_random_email():
    return f"user_{random.randint(1000, 9999)}@test.com"

def get_current_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
