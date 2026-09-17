from datetime import date
import os
import tweepy

GLYPH_HEIGHT = 9
HALF_WIDTH = 5

SYMBOLS = [" ", " ", "/", "\\", "|", "+", "<", ">", "-", "*", "."]
CENTER_SYMBOLS = ["|", "+", "*", " ", "<", ">"]


def next_random(n):
    return ((n * 9301) + 49297) % 233280


def mirror_text(text):
    mirror = {
        "/": "\\",
        "\\": "/",
        "<": ">",
        ">": "<",
    }

    return "".join(mirror.get(char, char) for char in reversed(text))


def generate_noise(day=None):
    if day is None:
        day = date.today()

    # YYYYMMDD — same seed used by the AppleScript version
    seed = (day.year * 10000) + (day.month * 100) + day.day

    output_lines = []

    for _ in range(GLYPH_HEIGHT):
        left_side = ""

        for _ in range(HALF_WIDTH):
            seed = next_random(seed)
            symbol_index = seed % len(SYMBOLS)
            left_side += SYMBOLS[symbol_index]

        seed = next_random(seed)
        center_index = seed % len(CENTER_SYMBOLS)
        center_char = CENTER_SYMBOLS[center_index]

        right_side = mirror_text(left_side)

        output_lines.append(left_side + center_char + right_side)

    return "\n".join(output_lines)

def post_to_x(text):
    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_KEY_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )

    response = client.create_tweet(text=text)
    return response

if __name__ == "__main__":
    noise = generate_noise()
    print(noise)
    post_to_x(noise)