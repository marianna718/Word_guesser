
import random


word_bank = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew']
attempts = 10

def main():

    attempts_now = attempts
    word = random.choice(word_bank)
    word_not_guessed = len(word) * "_"
    guessed_letters = []
    wrong_letters = []

    while attempts_now > 0:
        print(f"word: {word_not_guessed}")
        print(f"attempts left: {attempts_now}")
        guess = input("guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter.")
            continue
        if guess in guessed_letters or guess in wrong_letters:
            print("You already tried that letter.")
            continue
        if guess in word:
            print("Good guess!")
            guessed_letters.append(guess)
            word_not_guessed = "".join([c if c in guessed_letters else "_" for c in word])
            print(f"you guessed: {word_not_guessed}")
        else:
            print("Sorry, that letter is not in the word.")
            wrong_letters.append(guess)
            print(f"you guessed: {word_not_guessed}")
            attempts_now -= 1

        if "_" not in word_not_guessed:
            print(f"Congratulations! You guessed the word: {word}")
            break
        if attempts_now == 0:
            print(f"Sorry, you lost. The word was: {word}")
            break


if __name__ == "__main__":
    main()
