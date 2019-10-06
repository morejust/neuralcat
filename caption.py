import random


ATTEMPTS = 50
DEFAULT_CAPTION = "AI made this. Cat trained this AI. Mew the world."


def _get_random_word(
    max_word_length=6,
    min_word_length=2,
):
    seed = 'уеэоаыяиюйцукенгшщзхёэждлорпавыфячсмитьбю'

    word_length = random.randint(min_word_length, max_word_length)
    word = "".join(random.choices(seed, k=word_length))
    return word


def _get_random_cyrillic_text(
    max_words=20,
    min_words=7
):
    nwords = random.randint(min_words, max_words)

    words = [_get_random_word() for _ in range(nwords)]

    words[random.randint(0, len(words) - 1)] = "cat"

    return " ".join(words)


def translate(text):
    from googletrans import Translator
    translator = Translator()

    res = translator.translate(text, dest='en', src='mk')
    return res.text


def _check_valid_translation(text):
    # if "." in text:
    #     return True
    seed = 'йцукенгшщзхъёэждлорпавыфячсмитьбю'
    for s in seed:
        if s in text:
            return False

    return True


def generate_caption():
    for _ in range(ATTEMPTS):
        text = _get_random_cyrillic_text()
        print("TEXT:", text)
        translated = translate(text)
        print("Translated:", translated)
        if _check_valid_translation(translated):
            return translated
    return DEFAULT_CAPTION


if __name__ == "__main__":
    print(generate_caption())
