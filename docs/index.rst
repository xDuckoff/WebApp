.. Chatocode documentation master file, created by
   sphinx-quickstart on Thu May 11 11:59:53 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Документация Василька
=====================

Как установить ВасилЁк
======================

FIXME!

Развертывание Василька
======================

1. Скачать репозиторий
----------------------

    $ git clone git@gitlab.informatics.ru:Syomochkin/Project51-2017.git

2. Создать виртуальное окружения
--------------------------------

    $ virtualenv --python=python2.7 venv
	
    $ source venv/bin/activate

3. Установить необходимые модули
--------------------------------

    $ pip install -r requirements.txt

4. Настроить конфигурацию
-------------------------

- FLASK-сервер

    $ export FLASK_APP=run.py
	
    $ export DATABASE_URL=sqlite:////tmp/db.sqlite
	
    $ export SOCKET_MODE=True

- Локальный HEROKU-сервер

    Создать и заполнить файл .env на основе .env.example

- Удалённый HEROKU-сервер

    Settings > Config Variables > Reveal Config Vars

    FLASK_APP = run.py

    DATABASE_URL = postgres://root:root@localhost:3306/test


5. Настроить БД
---------------

- FLASK-сервер

    $ flask db upgrade

- Локальный HEROKU-сервер

    $ heroku local upgrade

- Удалённый HEROKU-сервер

    $ heroku run upgrade

6. Запустить приложение
-----------------------

- FLASK-сервер

    $ flask run

- Локальный HEROKU-сервер

    $ heroku local web

- Удалённый HEROKU-сервер

    Resources

    Поставить web включённым 

7. Подключиться к приложению
----------------------------

Откройте интернет-браузер и перейдите по адресу: http://localhost:5000/

Ежедневная работа
=================
FIXME!

Тесты
=====
FIXME!
		
Для разработчиков
=================

application.chat package
------------------------

**application.chat.router module**

.. automodule:: application.chat.router
    :members:
    :undoc-members:
    :show-inheritance:


**Module contents**

.. automodule:: application.chat
    :members:
    :undoc-members:
    :show-inheritance:

application package
-------------------

**application.forms module**

.. automodule:: application.forms
    :members:
    :undoc-members:
    :show-inheritance:

**application.models module**

.. automodule:: application.models
    :members:
    :undoc-members:
    :show-inheritance:

**application.router module**

.. automodule:: application.router
    :members:
    :undoc-members:
    :show-inheritance:


**Module contents**

.. automodule:: application
    :members:
    :undoc-members:
    :show-inheritance:



