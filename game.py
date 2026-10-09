import random
import json
import os
import getpass



def generate_secret_number(low=1, high=100):
    """Returns a random secret number."""
    rand_num = random.randint(low, high)
    return rand_num


def compare_guess(guess, secret_number):
    """Compares the player's guess with the secret number and returns 'Too high', 'Too low', or 'Correct'."""
    if guess > secret_number:
        return "Too high! Try a lower number."
    elif guess < secret_number:
        return "Too low! Try a higher number."
    else:
        return "Correct"


def choose_difficulty():
    """ Returns the low range, high range and maximum attempts based on the selected difficulty."""
    print("\nDifficulty options")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:
        choice = input("Choose difficulty level: ")

        if choice == "1":
            return 1, 50, 5

        elif choice == "2":
            return 1, 100, 7

        elif choice == "3":
            return 1, 500, 8

        else:
            print("Invalid choice. Pick from [1, 2, 3].")


def get_valid_guess(low, high, mode):
    """
    Returns a valid integer guess within the given range.
    Invalid guesses do not count as attempts.

    In single-player mode, input() is used so the guess
    is visible.

    In multiplayer mode, getpass.getpass() is used so
    the guess is hidden from the other players.
    """
    while True:

        # Single-player mode
        if mode == "1":
            guess = input(f"Guess a number ({low}-{high}): ")

        # Multiplayer mode
        else:
            guess = getpass.getpass(f"Guess a number ({low}-{high}): ")

        try:
            guess = int(guess)

            if low <= guess <= high:
                return guess

            else:
                print(f"Out of range. Enter a number between {low}-{high}.")

        except ValueError:
            print("Invalid input. Enter a whole number.")


def calculate_score(attempts, max_attempt):
    """ Calculates a player's score. Fewer attempts result in a higher score."""
    score = ((max_attempt - attempts + 1) / max_attempt) * 100

    if score < 0:
        score = 0

    return round(score)


def get_rating(score):
    """ Returns a star rating based on the player's score."""
    if score <= 20:
        return "⭐"
    elif score <= 40:
        return "⭐⭐"
    elif score <= 60:
        return "⭐⭐⭐"
    elif score <= 80:
        return "⭐⭐⭐⭐"
    else:
        return "⭐⭐⭐⭐⭐"


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



def give_hint(secret_number, low, high, wrong_guess):
    """Generate and return a hint about the secret number."""
    if wrong_guess == 3:

        if secret_number % 2 == 0:
            return "Hint: The number is even."

        else:
            return "Hint: The number is odd."

    else:

        midpoint = (low + high) // 2

        if secret_number <= midpoint:
            return f"Hint: The number is between {low} and {midpoint}."

        else:
            return (f"Hint: The number is between{midpoint + 1} and {high}.")


def display_leaderboard(leaderboard):
    """
    Displays the current leaderboard.
    """
    print("\n========== LEADERBOARD ==========")

    if not leaderboard:
        print("No scores recorded yet.")

    else:
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda item: item[1], reverse=True )

        for position, (name, score) in enumerate(sorted_leaderboard,start=1):
            print(f"{position}. {name} - {score} points")

    print("=================================")


def game():
    """
    Runs the full challenge version of the number guessing game.

    Single player and multiplayer share ONE game loop.
    Single player is simply a game with 1 player, so the
    same code handles 1 to 5 players without duplication.
    """

    # -----------------------------
    # CLEAR SCREEN
    # -----------------------------

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    leaderboard_file = "leaderboard.json"

    # -----------------------------
    # LOAD OR CREATE LEADERBOARD
    # -----------------------------

    if not os.path.exists(leaderboard_file):

        leaderboard = {}

        with open(leaderboard_file, "w") as file:
            json.dump(leaderboard, file, indent=4)

    else:

        with open(leaderboard_file, "r") as file:
            leaderboard = json.load(file)

    # -----------------------------
    # CHOOSE GAME MODE
    # -----------------------------

    mode = choose_game_mode()

    # -----------------------------
    # DECIDE NUMBER OF PLAYERS
    # -----------------------------

    # Single player  -> exactly 1 player.
    # Multiplayer    -> exactly 2 players for the scope of this project.
    if mode == "1":
        number_of_players = 1

    else:
        number_of_players = 2

    # -----------------------------
    # GET PLAYER NAMES
    # -----------------------------

    player_names = []

    # Loop once per player (runs only once in single player)
    for player_number in range(1,number_of_players + 1):

        while True:

            name = input(f"Enter Player {player_number} name: ").strip()

            # Name must not be empty
            if not name:
                print("Name cannot be empty.")

            # Names must be unique, otherwise two players would share one leaderboard entry
            elif name in player_names:
                print("That name is already taken. Choose another.")

            else:
                player_names.append(name)
                break

    # -----------------------------
    # PLAY MULTIPLE ROUNDS
    # -----------------------------

    playing = True

    while playing:

        # -----------------------------
        # CLEAR SCREEN FOR NEW ROUND
        # -----------------------------

        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        print("\n================================")
        print("           NEW ROUND")
        print("================================")

        # -----------------------------
        # CHOOSE DIFFICULTY
        # -----------------------------

        low, high, max_attempt = choose_difficulty()

        # Single player sees "You have ...", multiplayer
        # sees "Each player has ..."
        if number_of_players == 1:
            print(f"\nYou have {max_attempt} attempts.")

        else:
            print(f"\nEach player has {max_attempt} attempts.")

        print(f"The number is between {low} and {high}.")

        # -----------------------------
        # GENERATE SECRET NUMBER
        # -----------------------------

        secret_number = generate_secret_number(low, high)



        # -----------------------------
        # INITIALIZE GAME STATE
        # -----------------------------

        # Each player has their own attempt counter.
        # Example with 2 players: [0, 0]
        attempts = [0] * number_of_players

        # Counts how many FULL rounds of wrong guesses have happened (a full round = every player guessed once and all of them were wrong). Used to trigger hints.
        wrong_guesses = 0

        # Counts wrong guesses inside the CURRENT full round. When it reaches number_of_players, one full round of wrong guesses is complete, then it resets to 0. (In single player, every wrong guess is a full round.)
        round_wrong_guesses = 0

        # Stores the index of the winning player
        winner = None

        # Player 0 starts
        current_player = 0

        # -----------------------------
        # MAIN GAME LOOP (it loops based on the number of players you have)
        # -----------------------------

        # The loop stops when someone wins, or when the current player has used all attempts. Everyone takes turns in the same order, so when the player at the start of the order is out of attempts, every player is out.
        while (winner is None and attempts[current_player] < max_attempt ):

            # Only show whose turn it is when more than one
            # player is playing
            if number_of_players > 1:
                print(f"\n{player_names[current_player]}'s turn")

            guess = get_valid_guess(low, high, mode)

            attempts[current_player] += 1

            result = compare_guess(guess, secret_number)

            print(result)

            print(f"Attempt: {attempts[current_player]}/{max_attempt}")

            # -------------------------
            # PLAYER WINS
            # -------------------------

            if result == "Correct":

                winner = current_player

                print(f"\nCongratulations {player_names[winner]}! The secret number is {secret_number}.")

                break

            # -------------------------
            # PLAYER GUESSED WRONG
            # -------------------------

            round_wrong_guesses += 1

            # Once every player has guessed wrong, one full round of wrong guesses is complete.
            if round_wrong_guesses == number_of_players:

                wrong_guesses += 1

                round_wrong_guesses = 0

                # Give a hint after every 3 full rounds of wrong guesses
                if wrong_guesses % 3 == 0:

                    print("\n" + give_hint(secret_number,low, high, wrong_guesses))

            # Show remaining attempts for the player who just guessed (single player only, to keep  multiplayer output short)
            if (number_of_players == 1 and attempts[current_player] < max_attempt):

                print(f"Attempts remaining: {max_attempt - attempts[current_player]}\n")

            # Move to the next player. The % operator wraps back to player 0 after the last player. With 1 player this always stays on player 0.
            current_player = (current_player + 1) % number_of_players

        # -----------------------------
        # ROUND RESULTS
        # -----------------------------

        print("\n========== ROUND RESULTS ==========")

        if winner is not None:

            print(f"Winner: {player_names[winner]}")

            # -----------------------------
            # CALCULATE WINNER'S SCORE ONLY
            # -----------------------------
            winner_name = player_names[winner]

            winner_attempts = attempts[winner]

            score = calculate_score(winner_attempts, max_attempt)

            rating = get_rating(score)

            print(f"\n{winner_name}")

            print(f"Attempts: {winner_attempts}")

            print(f"Score: {score} points")

            print(f"Rating:{rating}")

            # -----------------------------
            # UPDATE LEADERBOARD
            # -----------------------------

            if winner_name not in leaderboard:

                leaderboard[winner_name] = score

                print(f"\n{winner_name} has been added to the leaderboard with {score} points.")

            elif score > leaderboard[winner_name]:

                old_score = leaderboard[winner_name]

                leaderboard[winner_name] = score

                print(f"\nNew best score for {winner_name}!")

                print(f"Previous best: {old_score}")

                print(f"New best: {score}"
                )

            # -----------------------------
            # SAVE LEADERBOARD
            # -----------------------------

            with open(leaderboard_file, "w") as file:

                json.dump(leaderboard, file, indent=4 )

        else:
        # -----------------------------
        # NO WINNER
        # -----------------------------
            print("Game Over!")

            print(f"The secret number was {secret_number}.")

            print("\nNo winner. No score was calculated.")


        



        # -----------------------------
        # AFTER-ROUND MENU
        # -----------------------------

        while True:

            print("\n========== MENU ==========")
            print("1. Play another round")
            print("2. View leaderboard")
            print("3. Exit")

            choice = input(
                "Choose an option: "
            )

            if choice == "1":

                break

            elif choice == "2":

                display_leaderboard(leaderboard)

            elif choice == "3":

                playing = False

                break

            else:
                print("Invalid choice. Pick 1, 2 or 3.")

    # -----------------------------
    # FINAL LEADERBOARD
    # -----------------------------

    print("\n")

    display_leaderboard(leaderboard)

    print("\nThanks for playing!")


game()