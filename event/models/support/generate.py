from secrets import token_urlsafe


def gen_unique_number():
    return token_urlsafe(10)
