import random
import time


def load_words(file_name):
    """Load words from the dictionary.txt file into a list."""
    try:
        dictionary = open(file_name, mode="r").read().split()
        return dictionary
    except FileNotFoundError:
        print("Dictionary file not found.")


def select_random_word(word_length, dictionary):
    """Select a random word from a new list containing words of specific length."""
    valid_words = [word for word in dictionary if len(word) == word_length]
    return random.choice(valid_words)


def select_difficulty():
    """Prompt user to choose hard mode and word length."""
    while True:
        try:
            mode = int(input("Hard mode? (1|0): "))
            if mode in [1, 0]:
                word_length = int(input("Select word length (4|5|6): "))
                if word_length in [4, 5, 6]:
                    return word_length, mode
                else:
                    print("Invalid input.")
            else:
                print("Invalid input.")
        except ValueError:
            print("Invalid input.")


def view_winners():
    """Prompt user for choice and display past winners if they exist."""
    while True:
        try:
            result = int(input("View Winners? (1|0): "))
            if result == 1:
                with open("winners.txt", mode="r") as file:
                    return file.read()
            elif result == 0:
                return ""
            else:
                print("Invalid input.")
        except FileNotFoundError:
            return "No past winners.\n"
        except ValueError:
            print("Invalid input.")


def letters(past_guesses):
    """Return a list of all letters marked as '*' or '+' so far."""
    letters = []
    for guess in past_guesses:
        for index, character in enumerate(guess[0].replace(" ", "")):  # Remove spaces between symbols in clue.
            if character in ["*", "+"]:
                letter = guess[1][index]  # Set letter variable to letter of the same index as the character.
                letters.append(letter) if letter not in letters else None
    return letters


def validate_hard_mode(guess, past_guesses):
    """Return true or false based on condition of hard mode."""
    if not letters(past_guesses):  # Return true if letters is empty to avoid error.
        return True
    else:
        for letter in letters(past_guesses):
            if letter not in list(guess):  # Cast current guess as list.
                return False
        return True


def help_vocabulary(dictionary, past_guesses, word_length, answer):
    """Provide all tenative solutions which satisfy clues provided so far."""
    possible_solutions, indexes = [], []
    words = [word for word in dictionary if len(word) == word_length]

    # Append indexes of all occurances of '*' in all guesses.
    for guess in past_guesses:
        for index, character in enumerate(guess[0].replace(" ", "")):
            if character in ["*"]:
                indexes.append(index)

    # Using the indexes, append all possible solutions to clues provided so far.
    for word in words:
        match = True
        for index in indexes:
            if word[index] != answer[index]:
                match = False
                break
        if match:
            possible_solutions.append(word)

    print(f"Possible solutions: {str(possible_solutions)[1:-1]}")


def provide_clue(guess, answer, letters):
    """Compare current guess to answer and provide feedback to the user."""
    clue = ''
    for index, letter in enumerate(guess):  # Loop through each letter in guess and compare to answer.
        count = guess.count(letter)  # Set count to the number of occurances of letter in guess.
        if (count < 2) or (count >= 2 and answer.count(letter) >= 2):  # Handle multiple instances of the same letter if it occurs.
            if letter == answer[index]:
                clue += "* "
            elif letter in answer:
                clue += "+ "
            else:
                clue += "_ "
                letters.append(letter) if letter not in letters else None  # Append to list containing letters the user has used which are not part of the answer.
        else:
            clue += "_ "
    return clue, guess, letters


def get_guess(dictionary, word_length, mode, past_guesses, turns):
    """Get the user's guess and ensure it is valid."""
    start = time.time()
    guess = input(f"\nGuess word of length {word_length}, you have 30 seconds: ")
    end = time.time()


    if (end - start) < 30:  # Check whether user exceeded 30 seconds to input guess.
        if guess == "exit" or guess == "hint" or guess == "help":
            return guess
        elif (turns == 6 or mode == 0) or (mode == 1 and turns < 6 and validate_hard_mode(guess, past_guesses)):  # Bypass this condition if hard mode is off, otherwise check that guess complies with hard mode.
            if len(guess) == word_length:
                if guess.lower() in dictionary:
                    return guess
                else:
                    print("Word does not exist in dictionary.")
            else:
                print("Invalid length.")
        else:
            print("You must include all previous letters marked as '*' or '+' in your guess.")
    else:
        print("Time limit exceeded 30 seconds.")


def handle_turn(answer, dictionary, past_guesses, letters, word_length, mode, turns):
    """Handle a player's turn, return input to main game loop."""
    guess = get_guess(dictionary, word_length, mode, past_guesses, turns)

    if guess == "exit" or guess == "hint" or guess == "help":  # If user gives up, requests a hint, or requests help with vocabulary.
        return guess
    elif guess == answer:  # If user guesses correctly.
        return guess
    elif guess:  # If user provides a guess which is incorrect.
        past_guesses.append(provide_clue(guess, answer, letters))

    # Print to the user the clue along with the corresponding guess, and letters not included.
    for guess in past_guesses:
        print(guess[0], "|", guess[1])
    print("Letters not in answer: ", end="")
    print(*letters, sep=", ")


def main():
    """Handle the main game loop."""
    print("\n------ SETUP ------")
    past_guesses, letters, turns, hint = [], [], 6, 1
    word_length, hard_mode = select_difficulty()
    dictionary = load_words("dictionary.txt")
    answer = select_random_word(word_length, dictionary)
    print(view_winners())

    print("------ WORDLE ------")
    name = input("Input name: ")
    print("Type 'exit' to give up.\nType 'hint' for a hint.\nType 'help' for help with vocabulary.")
    print("Wordle begins in 8 seconds...")
    time.sleep(8)

    start_time = time.time()  # Save time at beginning of the game.

    while turns != 0:
        turn = handle_turn(answer, dictionary, past_guesses, letters, word_length, hard_mode, turns)
        if not turn:  # If user guesses incorrectly.
            turns -= 1
        elif turn == "exit":  # If user decides to give up.
            print(f"You gave up.\nAnswer: {answer}")
            break
        elif turn == "hint":  # If user requests a hint.
            turns -= 1
            if hint != 0:
                hint -= 1
                print(f"Hint: {random.choice([letter for letter in answer])}")
            else:
                print("You have used your hint already.")
        elif turn == "help":  # If user requests help with vocabulary.
            turns -= 1
            help_vocabulary(dictionary, past_guesses, word_length, answer)
        elif turn == answer:  # If user wins the game, write name and time to 'winners.txt'.
            print(f"You win.\nAnswer: {answer}")
            with open("winners.txt", mode="a") as file:
                end_time = time.time()  # Save time at end of the game.
                total_time = end_time - start_time
                file.write(f"Name: {name}, Time: {total_time:.2f}\n")
            break
    else:  # If the user runs out of turns.
        print(f"You lose, no turns remaining.\nAnswer: {answer}")


if __name__ == "__main__":
    main()
