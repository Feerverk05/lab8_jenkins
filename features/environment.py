"""Хуки behave: браузер Chrome у headless-режимі для кожного сценарію.

У Jenkins (Docker) немає графічного інтерфейсу, тому за замовчуванням браузер
запускається без вікна. Локально вікно можна побачити так:  HEADLESS=false behave

Змінні середовища (задаються в Dockerfile / Jenkinsfile):
  HEADLESS           true/false, за замовчуванням true
  CHROME_BIN         шлях до браузера (у контейнері — /usr/bin/chromium)
  CHROMEDRIVER_PATH  шлях до драйвера; якщо не задано — драйвер завантажує webdriver-manager
"""
import os
import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Корінь репозиторію в sys.path, щоб кроки могли імпортувати пакет pages/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

try:  # allure-behave потрібен лише для скриншотів у звіті
    import allure
    from allure_commons.types import AttachmentType
except ImportError:
    allure = None  # pylint: disable=invalid-name


def _is_headless():
    return os.environ.get("HEADLESS", "true").lower() != "false"


def _chrome_options():
    options = Options()
    if _is_headless():
        options.add_argument("--headless=new")         # без графічного інтерфейсу
    options.add_argument("--no-sandbox")               # потрібно для запуску в Docker
    options.add_argument("--disable-dev-shm-usage")    # мала /dev/shm у контейнері
    options.add_argument("--window-size=1920,1080")    # повний розмір сторінки без вікна
    # Вимикаємо менеджер паролів: його вікно перекриває сторінку після входу
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--disable-features=PasswordLeakDetection")
    if os.environ.get("CHROME_BIN"):
        options.binary_location = os.environ["CHROME_BIN"]
    return options


def before_all(context):
    # Драйвер готуємо один раз на весь запуск
    context.driver_path = os.environ.get("CHROMEDRIVER_PATH") or ChromeDriverManager().install()


def before_scenario(context, scenario):  # pylint: disable=unused-argument
    service = Service(context.driver_path)
    context.driver = webdriver.Chrome(service=service, options=_chrome_options())


def after_step(context, step):
    if step.status == "failed" and allure is not None:
        allure.attach(
            context.driver.get_screenshot_as_png(),
            name=f"Скриншот: {step.name}",
            attachment_type=AttachmentType.PNG,
        )


def after_scenario(context, scenario):  # pylint: disable=unused-argument
    context.driver.quit()  # браузер закривається навіть після невдалого сценарію
