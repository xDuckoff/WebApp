.. Chatocode documentation master file, created by
   sphinx-quickstart on Thu May 11 11:59:53 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Документация
============

Развертывание приложения
------------------------

1. Скачать репозиторий и создать виртуальное окружение:

  .. code::

    git clone git@gitlab.com:project51/WebApp.git
    cd WebApp
    virtualenv --python=python2.7 venv
    source venv/bin/activate

3. Установить необходимые модули

  .. code::

    pip install -r requirements.txt


4. Настроить конфигурацию

  На основании файла ``.env.example`` создать новый файл под названием ``.env``.
  В созданном файле исправить значения переменных (если это требуется). Выполнить код:

  .. code::

    source .env

5. Установить и настроить PostgreSQL

  Сначала надо `установить PostgreSQL <https://www.postgresql.org/download/linux/ubuntu/>`_.
  Затем надо создать и ...

  После этого надо мигрировать модель данных в Postgres:

  - через *Flask*

    .. code::

      flask db upgrade

  - через *Heroku*

    .. code::

      heroku local upgrade


6. Запустить приложение


  - через *Flask*

  .. code::

    flask run

  - через *Heroku*

  .. code::

    heroku local web


7. Подключиться к приложению

  Открыть в браузере ссылку ``http://localhost:5000/``


Ежедневная работа
-----------------

Тут надо написать последовательность команд, которые надо выполять перед началом работы


Тестирование кода
-----------------

Список команд и требований,

		
API
---

**application.models**

.. automodule:: application.models
    :members:

    **Chat**

    .. automodule:: application.models.Chat
        :members:

    **Code**

    .. automodule:: application.models.Code
        :members:

    **Message**

    .. automodule:: application.models.Message
        :members:

**application.router module**

.. automodule:: application.router
    :members:
    :undoc-members:
    :show-inheritance:


**application.forms**

.. automodule:: application.forms
    :members:
    :undoc-members:
    :show-inheritance:


**application.chat**

.. automodule:: application.chat
    :members:
    :undoc-members:
    :show-inheritance:

.. automodule:: application.chat.router
    :members:
    :undoc-members:
    :show-inheritance:




