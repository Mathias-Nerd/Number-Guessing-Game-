import random


def generate_secret_number(low=1, high=100):
    """Generate and return a random number between 1 and 100."""
    rand_num = random.randint(low, high)
    print(f"randomly generated number: {rand_num}")
    return rand_num


def compare_guess(guess, secret_number):
    """Compare a player's guess with the secret number and return the result."""
    if guess < secret_number:
        return "Too low"
    elif guess > secret_number:
        return "Too high"
    else:
        return "Correct"
        
        
def choose_difficulty():
    """Ask the player to choose a difficulty and return its game settings."""
    print("Choose difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    choice = input("Enter your choice: ")

    if choice == "1":
        print(f"Level: easy")
        return 1, 50, 8
    elif choice == "2":
        print(f"Level: medium")
        return 1, 100, 10
    elif choice == "3":
        print(f"Level: difficult")
        return 1, 500, 15
    else:
        print("Invalid choice.")
        return choose_difficulty()
        
        
def get_valid_guess(low, high):
    """Get and return an integer guess within the specified range."""
    while True:
        try:
            guess = int(input(f"Enter your guess ({low}-{high}): "))

            if low <= guess <= high:
                return guess

            print(f"Please enter a number between {low} and {high}.")

        except ValueError:
            print("Invalid input. Please enter an integer.")
            
            


def give_hint(secret_number, low, high):
    """Generate and return a hint about the secret number."""
    if random.choice([True, False]):
        if secret_number % 2 == 0:
            return "Hint: The number is even."
        else:
            return "Hint: The number is odd."
    else:
        midpoint = (low + high) // 2

        if secret_number <= midpoint:
            return f"Hint: The number is between {low} and {midpoint}."
        else:
            return f"Hint: The number is between {midpoint + 1} and {high}."


def calculate_score(max_attempts, attempts):
    """Calculate and return a score based on the number of attempts used."""
    return (max_attempts - attempts + 1) * 100


def get_rating(attempts):
    """Return a star rating based on the number of attempts used."""
    if attempts <= 3:
        return "⭐⭐⭐"
    elif attempts <= 6:
        return "⭐⭐"
    else:
        return "⭐"           
            
            
def choose_game_mode():
    """Ask the player to choose a game mode and return the valid choice."""
    while True:
        print("\nChoose game mode:")
        print("1. Single Player")
        print("2. Multiplayer")

        mode = input("Enter your choice: ")

        if mode in ("1", "2"):
            return mode

        print("Invalid game mode. Please choose 1 or 2.")
        
        
        
        
        
            
              
#level1() 
#→ generate secret number
#→ ask player for a guess
#→ compare guess with secret number
#→ display the result
#→ finish


def level1():
    """Run the basic version of the number guessing game."""
    secret_number = generate_secret_number()

    guess = int(input("Guess the number: "))

    result = compare_guess(guess, secret_number)

    print(result)
    
    
"""   
level2()
→ generate secret number
→ set attempts = 0
→ get guess
→ increase attempts
→ compare guess
→ display result and attempt count
→ if correct → show attempts → finish
→ if wrong → ask for another guess
"""

def level2():
    """Run the number guessing game with repeated guesses and attempt tracking."""
    secret_number = generate_secret_number()
    attempts = 0

    while True:
        guess = int(input("Guess the number: "))
        attempts += 1

        result = compare_guess(guess, secret_number)

        print(f"{result}\nAttempt: {attempts}")

        if result == "Correct":
            print(f"Congratulations! You got it in {attempts} attempts.")
            break
            
            
"""
level3()
→ choose difficulty
→ generate secret number
→ set attempts = 0
→ get valid guess
→ increase attempts
→ display attempt count
→ compare guess
→ if correct → win
→ if wrong → check maximum attempts
→ if attempts remain → repeat
→ otherwise → Game Over
"""

def level3():
    """Run the number guessing game with difficulty, validation, and attempt limits."""
    low, high, max_attempts = choose_difficulty()
    print(f"Your maximum attempts is {max_attempts}.")
    secret_number = generate_secret_number(low, high)
    attempts = 0

    while attempts < max_attempts:
        guess = get_valid_guess(low, high)
        attempts += 1

        print(f"Attempt: {attempts}")

        result = compare_guess(guess, secret_number)
        print(result)

        if result == "Correct":
            print(f"Congratulations! You got it in {attempts} attempts.")
            break


    print("Game Over!")
    print(f"The secret number was {secret_number}.")
    
    
"""
level4()
→ choose difficulty
→ choose game mode
→ play the game
→ give hints after every 3 wrong guesses
→ calculate score
→ show rating
→ update best score
→ ask for another round
→ finish
"""

def level4():
    """Run the full challenge version of the number guessing game."""
    best_score = 0

    while True:
        low, high, max_attempts = choose_difficulty()
        mode = choose_game_mode()

        if mode == "1":
            secret_number = generate_secret_number(low, high)
            attempts = 0
            wrong_guesses = 0

            while attempts < max_attempts:
                guess = get_valid_guess(low, high)
                attempts += 1

                print(f"Attempt: {attempts}")

                result = compare_guess(guess, secret_number)
                print(result)

                if result == "Correct":
                    score = calculate_score(max_attempts, attempts)
                    rating = get_rating(attempts)

                    print(f"Congratulations! You scored {score} points.")
                    print(f"Rating: {rating}")

                    if score > best_score:
                        best_score = score
                        print("New best score!")

                    break

                wrong_guesses += 1

                if wrong_guesses % 3 == 0:
                    print(give_hint(secret_number, low, high))

            else:
                print("Game Over!")
                print(f"The secret number was {secret_number}.")

        elif mode == "2":
            secret_number = generate_secret_number(low, high)

            attempts = 0
            wrong_guesses = 0
            player1_attempts = 0
            player2_attempts = 0

            while attempts < max_attempts:

                # Player 1
                print("\nPlayer 1's turn")
                guess = get_valid_guess(low, high)
                player1_attempts += 1

                result = compare_guess(guess, secret_number)
                print(result)

                if result == "Correct":
                    score = calculate_score(max_attempts, attempts + 1)
                    rating = get_rating(attempts + 1)

                    print("Player 1 wins!")
                    print(f"Attempts: {player1_attempts}")
                    print(f"Score: {score}")
                    print(f"Rating: {rating}")

                    if score > best_score:
                        best_score = score
                        print("New best score!")

                    break

                wrong_guesses += 1

                if wrong_guesses % 3 == 0:
                    print(give_hint(secret_number, low, high))

                # Player 2
                print("\nPlayer 2's turn")
                guess = get_valid_guess(low, high)
                player2_attempts += 1

                result = compare_guess(guess, secret_number)
                print(result)

                if result == "Correct":
                    score = calculate_score(max_attempts, attempts + 1)
                    rating = get_rating(attempts + 1)

                    print("Player 2 wins!")
                    print(f"Attempts: {player2_attempts}")
                    print(f"Score: {score}")
                    print(f"Rating: {rating}")

                    if score > best_score:
                        best_score = score
                        print("New best score!")

                    break

                wrong_guesses += 1

                if wrong_guesses % 3 == 0:
                    print(give_hint(secret_number, low, high))

                # One complete attempt consists of both players guessing.
                attempts += 1

            else:
                print("\nGame Over!")
                print(f"The secret number was {secret_number}.")
                print(f"Player 1 attempts: {player1_attempts}")
                print(f"Player 2 attempts: {player2_attempts}")

        print(f"\nBest score: {best_score}")

        # Validate play-again choice
        while True:
            play_again = input("Play another round? (y/n): ").lower()

            if play_again in ("y", "n"):
                break

            print("Invalid choice. Please enter y or n.")

        if play_again == "n":
            break

def main():
    level = 4
    if level == 1:
        level1()
    elif level == 2:
        level2()
    elif level == 3:
        level3()
    else:
        level4()
        
    #level4()
        
main()