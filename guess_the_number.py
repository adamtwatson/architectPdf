#!/usr/bin python3

import random
import sys

if __name__ == '__main__':
    guesses = []
    guess_counts = 5
    lowest_number = 0
    highest_number = 10

    print('Want to play a game? Enter Y or N and press enter')
    user_response = ''
    acceptable_responses = ['y', 'n']
    max_errors = 3
    error_count = 0
    while user_response.lower() not in acceptable_responses and error_count < max_errors:
        user_response = input()
        if user_response.lower() not in acceptable_responses:
            print(f'{user_response} is not a valid selection, please try again.')
            error_count += 1
            continue
        if user_response.lower() == 'n':
            print('Okay, have a good day!')
            sys.exit()
    if error_count == max_errors:
        print('Sorry you did not provide a valid response...')
        sys.exit()

    number_picked = random.randint(lowest_number, highest_number)
    print(f'I am thinking of a number between {lowest_number} and {highest_number}, can you guess which number, '
          f'in less than {guess_counts} guesses?')
    guess = ''
    while guess != number_picked and len(guesses) < guess_counts:
        try:
            guess = input()
            guess = int(guess)
        except ValueError:
            print(f'{guess} is not a number.')
            continue
        if guess in guesses:
            print(f'{guess} already guessed, please guess another number.')
            print(f'Your current guesses {", ".join(str(g) for g in guesses)}')
            continue
        if guess > number_picked:
            print(f'The number is lower than {guess}')
        if guess < number_picked:
            print(f'The number is more than {guess}')
        guesses.append(guess)
        print(f'Your current guesses {", ".join(str(g) for g in guesses)}')

    if guess == number_picked:
        print(f'Congratulations you found the number in {len(guesses)} guesses')
    elif len(guesses) >= guess_counts:
        print(f'Sorry you lose. The number was {number_picked}')
    else:
        print(f'Something went wrong.')
