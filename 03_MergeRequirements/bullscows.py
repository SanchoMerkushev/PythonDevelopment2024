from collections import Counter
from random import choice
from urllib.request import urlopen
import argparse
import cowsay as cw


def bullscows(guess: str, secret: str) -> (int, int):
    bulls = 0
    cows = 0
    for i in range(len(guess)):
        if guess[i] == secret[i]:
            bulls += 1
    guess_count = Counter(guess)
    secret_count = Counter(secret)
    for c in secret_count:
        cows += min(secret_count[c], guess_count[c])
    return bulls, cows


def gameplay(ask: callable, inform: callable, words: list[str]) -> int:
    secret = choice(words)
    amount_try = 0
    while True:
        guess = ask("Введите слово: ", words)
        amount_try += 1
        b, c = bullscows(guess, secret)
        if b == len(guess):
            print("SUCCESS WITH", amount_try, "attempts!")
            break
        inform("Быки: {}, Коровы: {}", b, c)


def ask(prompt: str, valid: list[str] = None) -> str:
    guess = input(cw.cowsay(prompt, cow=cw.get_random_cow()) + "\n")
    while valid and guess not in valid:
        print("Word not from valid, try again")
        guess = input(cw.cowsay(prompt, cow=cw.get_random_cow()) + "\n")
    return guess


def inform(format_string: str, bulls: int, cows: int) -> None:
    inf_str = format_string.format(bulls, cows)
    print(cw.cowsay(inf_str, cow=cw.get_random_cow()))


parser = argparse.ArgumentParser()
parser.add_argument("dictionary", help="sourse of words")
parser.add_argument("length", help="length", type=int, default=5)
args = parser.parse_args()
if args.dictionary.split(":")[0] in ["http", "https"]:
    with urlopen(args.dictionary) as input_url:
        possible_words = input_url.read().decode('utf-8').splitlines()
else:
    with open(args.dictionary) as input_file:
        possible_words = input_file.read().splitlines()
possible_words = list(filter(lambda w: len(w) == args.length, possible_words))
gameplay(ask, inform, possible_words)
