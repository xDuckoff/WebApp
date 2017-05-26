Deploment Vasilek
=================

1. ������� �����������
----------------------

    $ git clone git@gitlab.informatics.ru:Syomochkin/Project51-2017.git

2. ������� ����������� ���������
--------------------------------

    $ virtualenv --python=python2.7 venv
    $ source venv/bin/activate

3. ���������� ����������� ������
--------------------------------

    $ pip install -r requirements.txt

4. ��������� ������������
-------------------------

- FLASK-������

    $ export FLASK_APP=run.py
    $ export DATABASE_URL=sqlite:////tmp/db.sqlite
    $ export SOCKET_MODE=True

- ��������� HEROKU-������

    ������� � ��������� ���� .env �� ������ .env.example

- �������� HEROKU-������

    Settings > Config Variables > Reveal Config Vars

    FLASK_APP = run.py

    DATABASE_URL = postgres://root:root@localhost:3306/test


5. ��������� ��
---------------

- FLASK-������

    $ flask db upgrade

- ��������� HEROKU-������

    $ heroku local upgrade

- �������� HEROKU-������

    $ heroku run upgrade

6. ��������� ����������
-----------------------

- FLASK-������

    $ flask run

- ��������� HEROKU-������

    $ heroku local web

- �������� HEROKU-������

    Resources

    ��������� web ���������� 

7. ������������ � ����������
----------------------------

�������� ��������-������� � ��������� �� ������: http://localhost:5000/