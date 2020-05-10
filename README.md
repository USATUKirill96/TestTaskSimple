### Технические требования

* Python 3.7 
```
sudo apt install python3.7
```
* Python 3 venv
```
sudo apt install python3.7-venv
```
* Python3.7-dev 

Данный пакет необходим для успешной установки psycopg2
```
sudo apt install python3.7-dev
```
* [Docker] 

### Создание и настройка виртуального окружения
```
python3.7 -m venv env
source env/bin/activate
pip install -r requirements.txt
```


### Запуск окружения сторонних сервисов

```
sudo docker-compose up -d
```
Опциональный флаг -d предназначен для запуска процесса в фоне. С целью отслеживания процессов запустите команду в другом
 окне без флага.

### Подготовка и запуск проекта
Следующие действия выполняются из виртуального окружения. Перейдите в папку с проектом командой
```
cd smenasimple
```

* Выполнение миграций
```
python manage.py migrate
```
* Заполнение базы данных информацией для тестов
```
python manage.py loaddata initial_data.json
```
* Регистрация пользователя для доступа к панели администратоа
```
python manage.py createsuperuser
```
#### Запуск асинхронного воркера
Необходимо выполнить его из виртуального окружения, создав дополнительное окно
```
python manage.py rqworker default
```
#### Запуск тестов
```
python manage.py test
```
### Запуск сервера для тестирования
```
python manage.py runserver
```

[Docker]: https://www.docker.com/get-started