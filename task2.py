import random
import time


def load_words(file_name):
    """Load words from the dictionary.txt file into a list."""
    dictionary = open(file_name, mode="r").read().split()
    return dictionary


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
                word_length = int(input(f"Select word length (4|5|6): "))
                if word_length in [4, 5, 6]:
                    return int(word_length), mode
                else:
                    print("Invalid input.")
            else:
                print("Invalid input.")
        except ValueError:
            print("Invalid input.")


def view_winners():
    """Prompt user for input and display past winners if they exist."""
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


def get_guess(dictionary, word_length):
    """Get the user's guess and ensure it is valid."""
    start = time.time()
    guess = input(f"Guess word of length {word_length}: ")
    end = time.time()

    if (end - start) < 30: # Check whether user exceeded 30 seconds to input guess.
        if guess == "exit" or guess == "hint":
            return guess
        elif len(guess) == word_length:
            if guess.lower() in dictionary:
                return guess
            else:
                print("Word does not exist in dictionary.")
        else:
            print("Invalid length.")
    else:
        print("Time exceeded 30 seconds.")


def provide_clue(guess, answer, letters):
    """Compare guess to answer and provide feedback to the user."""
    clue = ''
    for index, letter in enumerate(guess): # Loop through each letter in guess and compare to answer.
        count = guess.count(letter)
        if (count < 2) or (count > 2 and answer.count(letter) > 2):
            if letter == answer[index]:
                clue += "* "
            elif letter in answer:
                clue += "+ "
            else:
                clue += "_ "
                letters.append(letter) if letter not in letters else None
        else:
            clue += "_ "
    return clue, guess, letters


def handle_turn(answer, dictionary, past_guesses, letters, word_length):
    """Handle a player's turn."""
    guess = get_guess(dictionary, word_length)
    if guess == "exit" or guess == "hint": # If user gives up or requests a hint.
        return guess
    elif guess == answer: # If user guesses correctly.
        return guess
    elif not guess: # If user does not provide a guess.
        for turn in past_guesses:
            print(turn[0], "|", turn[1])
    else: # If user guesses incorrectly.
        past_guesses.append(provide_clue(guess, answer, letters)) 
        for turn in past_guesses:
            print(turn[0], "|", turn[1])
        print("Letters not in answer: ", end="")
        print(*letters, sep=", ",)
            

def main():
    """Handle the main game loop."""
    print("\n------ SETUP ------")
    PAST_GUESSES, LETTERS, TURNS, HINT = [], [], 6, 1
    WORD_LENGTH, HARD_MODE = select_difficulty()
    dictionary = load_words("dictionary.txt")
    answer = select_random_word(WORD_LENGTH, dictionary)
    print(view_winners())

    print("------ WORDLE ------")
    name = input("Input name: ")
    print("Type 'exit' to give up, type 'hint' for a hint.")
    print("Wordle begins in 5 seconds...")
    time.sleep(5)
    start_time = time.time()

    while TURNS != 0:
        turn = handle_turn(answer, dictionary, PAST_GUESSES, LETTERS, WORD_LENGTH)
        if not turn:
            TURNS -= 1
        elif turn == "exit":
            print(f"You gave up.\nAnswer: {answer}")
            break
        elif turn == "hint":
            TURNS -= 1
            if HINT != 0:
                HINT -= 1
                print(f"Hint: {random.choice([letter for letter in answer])}")
            else:
                print("You have used your hint already.")
        elif turn == answer:
            print(f"You win.\nAnswer: {answer}")
            with open("winners.txt", mode="a") as file:
                end_time = time.time()
                total_time = end_time - start_time
                file.write(f"Name: {name}, Time: {total_time:.2f}\n")
            break
    else:
        print(f"You lose, no turns remaining.\nAnswer: {answer}")


if __name__ == "__main__":
    main()