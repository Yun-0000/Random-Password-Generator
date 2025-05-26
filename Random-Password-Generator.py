import string
import secrets
import sys


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please type y or n.")


def get_user_choices():
    # length
    while True:
        try:
            length = int(input("Desired password length (8‑128): "))
            if 8 <= length <= 128:
                break
            raise ValueError
        except ValueError:
            print("  Length must be an integer between 8 and 128.")

    # character classes
    use_lower   = ask_yes_no("Include lower‑case letters?")
    use_upper   = ask_yes_no("Include UPPER‑case letters?")
    use_digits  = ask_yes_no("Include digits?")
    use_symbols = ask_yes_no("Include symbols (punctuation)?")

    if not any([use_lower, use_upper, use_digits, use_symbols]):
        print("Error: you must select at least one character type.")
        sys.exit(1)

    return length, use_lower, use_upper, use_digits, use_symbols

def generate_password(length: int,
                      use_lower: bool,
                      use_upper: bool,
                      use_digits: bool,
                      use_symbols: bool) -> str:
    pool = ""
    if use_lower:
        pool += string.ascii_lowercase
    if use_upper:
        pool += string.ascii_uppercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation

    # Ensure at least one char from each chosen class (optional but nice)
    password_chars = []
    if use_lower:
        password_chars.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        password_chars.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        password_chars.append(secrets.choice(string.digits))
    if use_symbols:
        password_chars.append(secrets.choice(string.punctuation))

    # Fill the rest of the password length
    while len(password_chars) < length:
        password_chars.append(secrets.choice(pool))

    # Shuffle so required characters aren’t all at the front
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def main():
    length, use_lower, use_upper, use_digits, use_symbols = get_user_choices()
    pwd = generate_password(length, use_lower, use_upper, use_digits, use_symbols)
    print("\nGenerated password:")
    print(pwd)

    # Optional clipboard copy
    try:
        import pyperclip
        pyperclip.copy(pwd)
        print("(Password copied to clipboard)")
    except ImportError:
        pass  # silently ignore if pyperclip not available

if __name__ == "__main__":
    main()
