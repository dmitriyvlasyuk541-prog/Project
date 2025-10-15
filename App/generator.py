import secrets
import json
import re
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).parent / "wordlists_human.json"


def load_data():
    """Загрузка словаря."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def add_random_digits(username, max_digits=5):
    """Добавляет до 5 цифр в случайные места."""
    num_digits = secrets.randbelow(max_digits + 1)
    for _ in range(num_digits):
        pos = secrets.randbelow(len(username) + 1)
        username = username[:pos] + str(secrets.choice(range(10))) + username[pos:]
    username = re.sub(r"^[0-9]+", "", username)
    return username


def is_valid_username(name):
    """Фильтрация слишком коротких логинов."""
    return len(name) >= 5 and re.search(r"[a-zA-Z]", name)


def gen_username(data):
    """Создаёт человеческий ник."""
    patterns = [
        "prefix+name", "name+suffix", "word+suffix",
        "name.word", "name+word", "prefix+word+suffix"
    ]
    p = secrets.choice(patterns)
    n = secrets.choice(data["names"])
    w = secrets.choice(data["words"])
    pre = secrets.choice(data["prefixes"])
    suf = secrets.choice(data["suffixes"])
    sep = secrets.choice(["", "_", ".", "-"])

    if p == "prefix+name":
        base = f"{pre}{sep}{n}"
    elif p == "name+suffix":
        base = f"{n}{sep}{suf}"
    elif p == "word+suffix":
        base = f"{w}{sep}{suf}"
    elif p == "name.word":
        base = f"{n}.{w}"
    elif p == "name+word":
        base = f"{n}{sep}{w}"
    elif p == "prefix+word+suffix":
        base = f"{pre}{sep}{w}{sep}{suf}"
    else:
        base = f"{n}{sep}{suf}"

    username = add_random_digits(base.lower())
    return username if is_valid_username(username) else gen_username(data)


def gen_password(length=14, use_symbols=True):
    """Генерация надёжного пароля."""
    base = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    symbols = "!@#$%^&*"
    alphabet = base + symbols if use_symbols else base
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_pairs(qty=10, length=14, use_symbols=True):
    """Создаёт список [username, password, created]."""
    data = load_data()
    result = []
    for _ in range(qty):
        username = gen_username(data)
        password = gen_password(length, use_symbols)
        result.append([username, password, datetime.utcnow().isoformat() + "Z"])
    return result
