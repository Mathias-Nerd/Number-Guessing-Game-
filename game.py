#Group 2
# Guess number game
import random

def generate_secret_number(low=1, high=100):
    """
    returns a random secret number
    """
    rand_num = random.randint(low, high)
    return rand_num


def compare_guess(guess, secret_number):
    """
    Compares the player's guess with the secret number and return any of 'too high', 'too low' or 'correct'
    """
    if guess > secret_number:
        return "Too high! try a lower number"
    elif guess < secret_number:
        return "Too low! try a higher number"
    else:
        return "Correct"


def choose_difficulty():
    """
    returns low, high and maximum attempt
    """
    print("Difficulty options\n1. Easy\n2. Medium\n3. Hard")
    while True:
        choice = int(input("Choose difficulty level: "))
        if choice == 1:
            return 1, 50, 5
        elif choice == 2:
            return 1, 100, 7
        elif choice == 3:
            return 1, 500, 10
        else:
            print("Invalid choice. Pick from [1. Easy, 2. Medium, 3. Hard]")
            continue


def get_valid_guess(low, high):
    """
    It returns a valid guess and attempt
    """
    while True:
        guess = input("Guess a number: ")
        try:
            guess = int(guess)
            # guess >= low and guess <= high
            # low <= guess and guess <= high
            if low <= guess <= high:
                return guess
            else:
                print(f"Out of range. Enter between {low}-{high}")
        except:
            print("Invalid input.")
            



#level1
def level1():
    """
    runs the simplest version of the number guessing game.
    """
    secret_number = generate_secret_number()
    guess = int(input("Guess a number: "))
    result = compare_guess(guess, secret_number)
    print(result)

def level2():
    """
    Allow the player to keep guessing 
    """
    secret_number = generate_secret_number()
    attempt = 0
    while True:
        guess = int(input("Guess a number: "))
        attempt += 1
        result = compare_guess(guess, secret_number)
        print(f"{result}. Attempt: {attempt}")
        if guess == secret_number:
            print(f"You win. Total attempts: {attempt}")
            break

def level3():
    low, high, max_attempt = choose_difficulty()
    print(f"You have {max_attempt} attempt.")
    secret_number = generate_secret_number()
    print(f"Secret number: {secret_number}")
    attempt = 0
    while attempt < max_attempt:
        guess = get_valid_guess(low, high)
        attempt += 1
        result = compare_guess(guess, secret_number)
        if attempt != max_attempt:
            print(result)
            if guess != secret_number:
                print(f"You have {max_attempt-attempt} attempt left")
        else:
            print(f"Game Over! Secret number is: {secret_number}")
        
        
        if result == "Correct":
            print(f"Congratulations! You got it in {attempt} attempts.")
            break

level3()