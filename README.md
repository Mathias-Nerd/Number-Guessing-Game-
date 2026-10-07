# Number Guessing Game — Expanded Challenge
Python Project Documentation
## Project GoalBuild a competitive command-line game where the player tries to guess a randomly generated number within a set range, receiving "too high" or "too low" hints after each attempt.
## Requirements
1. The computer picks a random number within a configurable range (e.g., 1–100).
2. The player enters guesses and receives directional hints after each attempt.
3. Track and display the number of attempts after every guess.
4. Validate user input so they can only enter valid integers within the range.
Example:
Input:
> Guess a number between 1 and 100: 50

Expected output:
> Too high! Try a lower number.
> Attempts: 1

## Project Levels
## Level 1 — Basic
Generate a random number between 1 and 100.
Get a single guess from the user.
Compare the guess to the number and print "Too high!", "Too low!", or "Correct!".

## Level 2 — Intermediate
Wrap the game in a loop so the player keeps guessing until they get it right.
Keep track of the total number of attempts.
Display the attempt count after every guess.
Congratulate the player and show total attempts when they guess correctly.

## Level 3 — Problem Solving
Implement strict input validation (handle non-integer input like "abc", empty input, and out-of-range numbers).
Allow the user to choose the difficulty/range before playing (e.g., Easy: 1–50, Medium: 1–100, Hard: 1–500).
Set a maximum number of attempts based on difficulty and end the game with a "Game Over" message if the player runs out of guesses.

### Example(with attempt limit):
### Input:
> Guess a number between 1 and 100: 50


### Expected output:
> Too high! Try a lower number.
> Attempts: 1
> You have 9 attempts remaining.


## Level 4 — Challenge
Add a "Hint System": After every 3 wrong guesses, offer the player a hint (e.g., "The number is even/odd" or "The number is between X and Y").
Add a scoring system: Fewer attempts = higher score. Display a rating (e.g., ⭐⭐⭐ for 1–3 attempts, ⭐⭐ for 4–6, ⭐ for 7+).
Implement a "Multiplayer Mode":
3.a. Two players take turns guessing the same number; first to guess correctly wins.
3.b. Track each player's attempts separately.
Allow the player to play multiple rounds and track their best score across all rounds without restarting the program.

## Skills Practiced
random module, while loop control flow, conditional branching (if/elif/else), input validation with try/except, attempt counter management, difficulty scaling logic, scoring algorithms, and multiplayer turn-based state management.
