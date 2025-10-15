# browser.py
import threading
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


def _run_browser(urls, headless=False):
    """
    Внутренняя функция, которая запускает Chrome в режиме инкогнито.
    Выполняется в отдельном потоке, чтобы не зависал GUI.
    """

    # Если передана строка, превращаем её в список
    if isinstance(urls, str):
        urls = [urls]
    if not urls:
        raise ValueError("Не передан URL для открытия")

    # === Настройки Chrome ===
    options = ChromeOptions()
    options.add_argument("--incognito")  # режим инкогнито
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("detach", True)  # не закрывать окно после завершения скрипта

    # Если нужно — без графического интерфейса
    if headless:
        options.add_argument("--headless=new")

    # === Путь к драйверу ===
    # chromedriver.exe должен лежать в корне проекта, рядом с main.py
    driver_path = Path(__file__).parent / "chromedriver.exe"
    if not driver_path.exists():
        raise FileNotFoundError(f"Не найден драйвер: {driver_path}")

    # === Запуск браузера ===
    service = ChromeService(executable_path=str(driver_path))
    driver = webdriver.Chrome(service=service, options=options)

    # Открываем первую вкладку
    driver.maximize_window()
    driver.get(urls[0])
    print(f"✅ Открыто: {urls[0]}")

    # Небольшая пауза, чтобы вкладка успела прогрузиться
    time.sleep(1)

    # Открываем остальные вкладки
    for url in urls[1:]:
        driver.execute_script(f"window.open('{url}', '_blank');")
        print(f"✅ Открыто: {url}")
        time.sleep(0.8)

    print("🌐 Все вкладки успешно открыты в режиме инкогнито.")



def open_in_incognito(urls, headless=False):
    """
    Публичная функция, запускающая Chrome в отдельном потоке.
    Используется из интерфейса (ui.py).
    """
    thread = threading.Thread(target=_run_browser, args=(urls, headless), daemon=True)
    thread.start()
