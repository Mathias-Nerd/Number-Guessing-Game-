import random
import json
import os
import getpass


def generate_secret_number(low=1, high=100):
    """
    Returns a random secret number.
    """
    rand_num = random.randint(low, high)
    return rand_num


def compare_guess(guess, secret_number):
    """
    Compares the player's guess with the secret number
    and returns 'Too high', 'Too low', or 'Correct'.
    """
    if guess > secret_number:
        return "Too high! Try a lower number."
    elif guess < secret_number:
        return "Too low! Try a higher number."
    else:
        return "Correct"


def choose_difficulty():
    """
    Returns the low range, high range and maximum attempts
    based on the selected difficulty.
    """
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
    the guess is hidden from the other player.
    """
    while True:

        # Single-player mode
        if mode == "1":
            guess = input(
                f"Guess a number ({low}-{high}): "
            )

        # Multiplayer mode
        else:
            guess = getpass.getpass(
                f"Guess a number ({low}-{high}): "
            )

        try:
            guess = int(guess)

            if low <= guess <= high:
                return guess

            else:
                print(
                    f"Out of range. Enter a number between {low}-{high}."
                )

        except ValueError:
            print("Invalid input. Enter a whole number.")


def calculate_score(attempts, max_attempt):
    """
    Calculates a player's score.
    Fewer attempts result in a higher score.
    """
    score = ((max_attempt - attempts + 1) / max_attempt) * 100

    if score < 0:
        score = 0

    return round(score)


def get_rating(score):
    """
    Returns a star rating based on the player's score.
    """
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
            return (
                f"Hint: The number is between "
                f"{midpoint + 1} and {high}."
            )


def display_leaderboard(leaderboard):
    """
    Displays the current leaderboard.
    """
    print("\n========== LEADERBOARD ==========")

    if not leaderboard:
        print("No scores recorded yet.")

    else:
        sorted_leaderboard = sorted(
            leaderboard.items(),
            key=lambda item: item[1],
            reverse=True
        )

        for position, (name, score) in enumerate(
            sorted_leaderboard,
            start=1
        ):
            print(f"{position}. {name} - {score} points")

    print("=================================")


def game():
    """
    Runs the full challenge version of the number guessing game.
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
            json.dump(
                leaderboard,
                file,
                indent=4
            )

    else:

        with open(leaderboard_file, "r") as file:
            leaderboard = json.load(file)

    # -----------------------------
    # CHOOSE GAME MODE
    # -----------------------------

    mode = choose_game_mode()

    if mode == "1":
        number_of_players = 1

    else:
        number_of_players = 2

    # -----------------------------
    # GET PLAYER NAMES
    # -----------------------------

    player_names = []

    for player_number in range(
        1,
        number_of_players + 1
    ):

        while True:

            name = input(
                f"Enter Player {player_number} name: "
            ).strip()

            if name:
                player_names.append(name)
                break

            print("Name cannot be empty.")

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

        print(
            f"\nYou have {max_attempt} attempts."
        )

        print(
            f"The number is between {low} and {high}."
        )

        # -----------------------------
        # GENERATE SECRET NUMBER
        # -----------------------------

        secret_number = generate_secret_number(
            low,
            high
        )

        # Each player has their own
        # attempt counter
        attempts = [0] * number_of_players

        # Count wrong-guess pairs
        wrong_guesses = 0

        # Stores the winning player
        winner = None

        # Player 0 starts
        current_player = 0

        # -----------------------------
        # SINGLE PLAYER
        # -----------------------------

        if number_of_players == 1:

            while attempts[0] < max_attempt:

                guess = get_valid_guess(
                    low,
                    high,
                    mode
                )

                attempts[0] += 1

                result = compare_guess(
                    guess,
                    secret_number
                )

                print(result)

                print(
                    f"Attempt: "
                    f"{attempts[0]}/{max_attempt}\n"
                )

                # -------------------------
                # PLAYER WINS
                # -------------------------

                if result == "Correct":

                    winner = 0

                    print(
                        f"\nCongratulations "
                        f"{player_names[0]}!"
                    )

                    break

                # -------------------------
                # WRONG GUESS
                # -------------------------

                wrong_guesses += 1

                # Give hint after every
                # 3 wrong guesses
                if wrong_guesses % 3 == 0:

                    print(
                        "\n" +
                        give_hint(
                            secret_number,
                            low,
                            high,
                            wrong_guesses
                        )
                    )

                # Attempts remaining
                if attempts[0] < max_attempt:

                    print(
                        f"Attempts remaining: "
                        f"{max_attempt - attempts[0]}"
                    )

        # -----------------------------
        # MULTIPLAYER
        # -----------------------------

        else:

            # Counts wrong guesses within
            # the current pair.
            pair_wrong_guesses = 0

            while winner is None:

                # Both players have used
                # all their attempts
                if (
                    attempts[0] >= max_attempt
                    and attempts[1] >= max_attempt
                ):
                    break

                # If current player has used
                # all attempts, move to other player
                if attempts[current_player] >= max_attempt:

                    current_player = 1 - current_player
                    continue

                print(
                    f"\n{player_names[current_player]}'s turn"
                )

                guess = get_valid_guess(
                    low,
                    high,
                    mode
                )

                attempts[current_player] += 1

                result = compare_guess(
                    guess,
                    secret_number
                )

                print(result)

                print(
                    f"Attempt: "
                    f"{attempts[current_player]}/{max_attempt}"
                )

                # -------------------------
                # PLAYER WINS
                # -------------------------

                if result == "Correct":

                    winner = current_player

                    print(
                        f"\nCongratulations "
                        f"{player_names[winner]}! The secret number is {secret_number}."
                        
                    )

                    break

                # -------------------------
                # PLAYER GUESSED WRONG
                # -------------------------

                pair_wrong_guesses += 1

                # Increase wrong_guesses
                # only after both players
                # have guessed wrong.
                if pair_wrong_guesses == 2:

                    wrong_guesses += 1

                    pair_wrong_guesses = 0

                    # Give hint after every
                    # 3 pairs of wrong guesses
                    if wrong_guesses % 3 == 0:

                        print(
                            "\n" +
                            give_hint(
                                secret_number,
                                low,
                                high,
                                wrong_guesses
                            )
                        )

                # Move to the other player
                current_player = 1 - current_player

        # -----------------------------
        # ROUND RESULTS
        # -----------------------------

        print(
            "\n========== ROUND RESULTS =========="
        )

        if winner is not None:

            print(
                f"Winner: "
                f"{player_names[winner]}"
            )

        else:

            print("Game Over!")

            print(
                f"The secret number was "
                f"{secret_number}."
            )

        # -----------------------------
        # CALCULATE WINNER'S SCORE ONLY
        # -----------------------------

        if winner is not None:

            winner_name = player_names[winner]

            winner_attempts = attempts[winner]

            score = calculate_score(
                winner_attempts,
                max_attempt
            )

            rating = get_rating(
                score
            )

            print(
                f"\n{winner_name}"
            )

            print(
                f"Attempts: "
                f"{winner_attempts}"
            )

            print(
                f"Score: "
                f"{score} points"
            )

            print(
                f"Rating: "
                f"{rating}"
            )

            # -----------------------------
            # UPDATE LEADERBOARD
            # -----------------------------

            if winner_name not in leaderboard:

                leaderboard[winner_name] = score

                print(
                    f"\n{winner_name} has been added "
                    f"to the leaderboard with "
                    f"{score} points."
                )

            elif score > leaderboard[winner_name]:

                old_score = leaderboard[winner_name]

                leaderboard[winner_name] = score

                print(
                    f"\nNew best score "
                    f"for {winner_name}!"
                )

                print(
                    f"Previous best: "
                    f"{old_score}"
                )

                print(
                    f"New best: "
                    f"{score}"
                )

            # -----------------------------
            # SAVE LEADERBOARD
            # -----------------------------

            with open(leaderboard_file, "w") as file:

                json.dump(
                    leaderboard,
                    file,
                    indent=4
                )

        # -----------------------------
        # NO WINNER
        # -----------------------------

        else:

            print(
                "\nNo winner. "
                "No score was calculated."
            )

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

                display_leaderboard(
                    leaderboard
                )

            elif choice == "3":

                playing = False

                break

            else:

                print(
                    "Invalid choice. "
                    "Pick 1, 2 or 3."
                )

    # -----------------------------
    # FINAL LEADERBOARD
    # -----------------------------

    print("\n")

    display_leaderboard(
        leaderboard
    )

    print("\nThanks for playing!")


game()