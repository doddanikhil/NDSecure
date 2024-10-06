from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    print(f"Generated Fernet key: {key.decode()}")
    print("Add this key to your .env file as ENCRYPTION_KEY=<generated_key>")

if __name__ == "__main__":
    generate_key()