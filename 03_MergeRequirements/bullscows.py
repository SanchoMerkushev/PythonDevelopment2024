from collections import Counter

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

