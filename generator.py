import random
import string
import time

def generate_user_id() -> str:
    return "".join(random.choices(string.digits, k=8))

def generate_gmail(count: int) -> list:
    emails = []
    base = "earnwork"
    for _ in range(count):
        unique_suffix = str(int(time.time() * 1000))[-4:]
        random_num = random.randint(100, 999)
        emails.append(f"{base}{random_num}{unique_suffix}@gmail.com")
    return emails
