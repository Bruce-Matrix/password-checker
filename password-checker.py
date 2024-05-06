import random
import string

def check_password_strength(password):
    """
    This function checks the strength of a password based on various criteria.

    Args:
        password (str): The password string to be checked.

    Returns:
        tuple: A tuple containing:
            - strength (str): A string indicating the password strength (e.g., "Weak", "Moderate", "Strong").
            - suggestions (list): A list of suggestions for improvement (optional).
    """
    strength = "Weak"
    suggestions = []

    # Check password length
    if len(password) < 8:
        suggestions.append("Password should be at least 8 characters long.")
    elif len(password) >= 12:
        strength = "Strong"
    else:
        strength = "Moderate"

    # Check for character types
    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_numbers = any(char.isdigit() for char in password)
    has_symbols = any(char in "!@#$%^&*()" for char in password)

    # Adjust criteria for Strong password
    if strength == "Strong":
        if not (has_uppercase and has_lowercase and has_numbers and has_symbols):
            suggestions.append("Strong passwords should include uppercase, lowercase, numbers, and symbols.")

    # Adjust criteria for Moderate password
    elif strength == "Moderate":
        if not (has_uppercase or has_lowercase) or not (has_numbers or has_symbols):
            suggestions.append("Moderate passwords should include characters from at least two different types.")

    # Check for dictionary words or common patterns
    # (Replace this section with a more robust dictionary check if needed)
    if password.lower() in ["password", "123456", "qwerty"]:
        suggestions.append("Password should not be a common word or easily guessable pattern.")

    return strength, suggestions

def generate_strong_password(length=12):
    """
    Generate a strong random password.

    Args:
        length (int): Length of the password. Default is 12.

    Returns:
        str: A strong random password.
    """
    # Define character sets for password generation
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    symbols = "!@#$%^&*()"

    # Combine character sets
    all_characters = uppercase_letters + lowercase_letters + digits + symbols

    # Generate random password
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

def main():
    """
    This function prompts the user to check the strength of a password, generate a strong password, or quit.
    """
    while True:
        print("Choose an option:")
        print("1. Check the strength of a password")
        print("2. Generate a strong password")
        print("3. Quit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            password = input("Enter your password: ")
            strength, suggestions = check_password_strength(password)

            if strength == "Strong":
                print("Your password is STRONG already. You don't need me.")
                break

            if strength == "Moderate":
                print("Your password is MODERATE.")
            else:
                print(f"Password Strength: {strength}")
                if suggestions:
                    print("Suggestions for improvement:")
                    for suggestion in suggestions:
                        print("- " + suggestion)
                else:
                    print("No suggestions for improvement.")
        elif choice == "2":
            length = int(input("Enter the length of the password you want to generate: "))
            password = generate_strong_password(length)
            print("Generated strong password:", password)
            print("This is a strong password. Make sure not to share it with anyone!")
            break
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter '1', '2', or '3'.")

if __name__ == "__main__":
    main()
