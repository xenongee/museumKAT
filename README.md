## Дипломный проект MuseumKAT

Проект MuseumKAT представляет собой веб-приложение, разработанное на Python с использованием фреймворка Flask 1.1.2. Это дипломный проект, который я разработал в 2020 году.


## Инструкция по развертыванию проекта (WSL, Ubuntu)

**Шаги развертывания:**

1.  **Обновление системы и установка зависимостей:**
    Откройте терминал WSL и выполните команды:
    ```bash
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv mariadb-server
    sudo apt install -y build-essential python3-dev libxml2-dev libxslt1-dev libmysqlclient-dev
    ```

2.  **Настройка базы данных MariaDB:**
    Запустите и включите службу MariaDB, затем создайте базу данных и пользователя:
    ```bash
    sudo systemctl start mariadb
    sudo systemctl enable mariadb

    # Удаляем БД, если она осталась от предыдущих попыток. Если БД не настраивалась ранее, то пропустите этот шаг
    sudo mysql -u root -e "DROP DATABASE IF EXISTS \`museumkat_db\`;"

    # Создаем БД и пользователя
    sudo mysql -u root -e "CREATE DATABASE \`museumkat_db\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE USER IF NOT EXISTS 'museum-admin'@'localhost' IDENTIFIED BY 'museumpassword'; GRANT ALL PRIVILEGES ON \`museumkat_db\`.* TO 'museum-admin'@'localhost'; FLUSH PRIVILEGES;"
    ```

3.  **Настройка виртуального окружения Python:**
    Перейдите в каталог проекта, если вы не в нём, и создайте виртуальное окружение:
    ```bash
    cd ~/Projects/museumKAT # Замените на ваш путь к проекту
    python3 -m venv mvenv

    source mvenv/bin/activate
    # или
    . mvenv/bin/activate
    ```

    Убедитесь, что вы находитесь в активированном виртуальном окружении - в начале строки терминала должно быть `(mvenv)`. Установите зависимости Python:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Импорт дампа базы данных:**
    ```bash
    cd ~/Projects/museumKAT
    sudo mysql -u root museumkat_db < museumkat_db_dump.sql
    ```
    На этом этапе база данных содержит все таблицы и данные из дампа.

5.  **Запуск Flask приложения:**
    Запустите сервер разработки:
    ```bash
    cd ~/Projects/museumKAT/app
    python3 manage.py runserver
    ```
    Приложение должно быть доступно по адресу `http://127.0.0.1:5000/` в вашем веб-браузере.


## Полный скрипт развертывания
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv mariadb-server
sudo apt install -y build-essential python3-dev libxml2-dev libxslt1-dev libmysqlclient-dev
sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo mysql -u root -e "CREATE DATABASE \`museumkat_db\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE USER 'museum-admin'@'localhost' IDENTIFIED BY 'museumpassword'; GRANT ALL PRIVILEGES ON \`museumkat_db\`.* TO 'museum-admin'@'localhost'; FLUSH PRIVILEGES;"
python3 -m venv mvenv
. mvenv/bin/activate
pip install -r requirements.txt
sudo mysql -u root museumkat_db < museumkat_db_dump.sql
cd app
python3 manage.py runserver
```
