# Jenkins з Python, Chromium і Allure для запуску UI-тестів у контейнері
FROM jenkins/jenkins:lts

USER root

# Дзеркало Debian можна змінити, якщо основне тимчасово віддає 404:
#   docker build --build-arg DEBIAN_MIRROR=http://ftp.de.debian.org/debian -t my-jenkins .
ARG DEBIAN_MIRROR=http://deb.debian.org/debian
RUN sed -i "s|^URIs: http://deb.debian.org/debian$|URIs: ${DEBIAN_MIRROR}|" /etc/apt/sources.list.d/debian.sources \
    && rm -f /etc/apt/apt.conf.d/docker-clean

# Python для тестів; Chromium і ChromeDriver з репозиторію Debian
# (працюють і на Intel, і на Apple Silicon — на відміну від Google Chrome, якого немає для Linux ARM).
# Кеш apt зберігається між збірками: якщо збірка впаде, завантажені пакети не доведеться качати знову.
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update -o Acquire::Retries=5 \
    && apt-get install -y -o Acquire::Retries=5 --no-install-recommends \
        python3 python3-pip python3-venv \
        chromium chromium-driver fonts-liberation

# Allure Commandline — будує HTML-звіт із allure-results
ARG ALLURE_VERSION=2.30.0
RUN curl -fLs -o /tmp/allure.tgz \
        https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/${ALLURE_VERSION}/allure-commandline-${ALLURE_VERSION}.tgz \
    && tar -zxf /tmp/allure.tgz -C /opt/ \
    && ln -s /opt/allure-${ALLURE_VERSION} /opt/allure \
    && ln -s /opt/allure/bin/allure /usr/local/bin/allure \
    && rm /tmp/allure.tgz

# Тести беруть браузер і драйвер звідси (див. features/environment.py)
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver

USER jenkins

# Плагіни: Pipeline, Git, Stage View і Allure
RUN jenkins-plugin-cli --plugins workflow-aggregator git pipeline-stage-view allure-jenkins-plugin