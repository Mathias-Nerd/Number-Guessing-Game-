MAX_PLAYER = 5

def get_number_of_players():
    """
    Asks how many people will play in multiplayer mode.
    The number must be a whole number from 2 to MAX_PLAYERS (5).
    """
    while True:
        answer = input(
            f"How many players? (2-{MAX_PLAYERS}): "
        )

        try:
            count = int(answer)

            if 2 <= count <= MAX_PLAYERS:
                return count

            print(
                f"Number of players must be between 2 and {MAX_PLAYERS}."
            )

        except ValueError:
            print("Invalid input. Enter a whole number.")


  # number_of_players = get_number_of_players()
