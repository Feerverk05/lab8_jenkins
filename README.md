# Лабораторна робота №8 — CI/CD Pipeline (Jenkins + Docker + behave + Allure)

UI-тести Swag Labs (behave + Selenium + Page Object) і Pipeline as Code для Jenkins.

## Структура
```
├── Dockerfile            # Jenkins + Python + Chromium + Allure
├── Jenkinsfile           # Pipeline: Checkout → Static Code Analysis → Install → Run UI Tests → Allure
├── requirements.txt      # selenium, behave, webdriver-manager, allure-behave, pylint
├── pyproject.toml        # налаштування Pylint (поріг якості fail-under = 8.0)
├── behave.ini
├── config.py
├── features/
│   ├── environment.py    # headless Chrome: --headless --no-sandbox --disable-dev-shm-usage --window-size
│   ├── login.feature
│   ├── cart.feature
│   └── steps/
│       ├── login_steps.py
│       └── cart_steps.py
└── pages/                # Page Object: LoginPage, InventoryPage, CartPage
```

## Jenkins у Docker
```bash
docker build -t my-jenkins .
docker run -d -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home --name jenkins my-jenkins
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
Manage Jenkins → Tools → Allure Commandline: name `allure`, без автоустановки, шлях `/opt/allure`.

## Локальний запуск тестів
```bash
pip3 install -r requirements.txt
behave                      # headless за замовчуванням
HEADLESS=false behave       # з вікном браузера
pylint features pages config.py
```
