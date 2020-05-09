### Технические требования

* Python 3.7 
```
sudo apt install python3.7
```
* Python3.7-dev 
```
sudo apt install python3.7-dev
```
* [Docker] 

### Создание и настройка виртуального окружения
```
python3.7 -m venv env;
source env/bin/activate;
pip install -r requirements.txt;
cd smenasimple
```


### Запуск окружения сторонних сервисов

```
sudo docker-compose up -d
```
Опциональный флаг -d предназначен для запуска процесса в фоне. С целью отслеживания процессов запустите команду в другом
 окне без флага.

### Подготовка и запуск проекта
Следующие действия выполняются из виртуального окружения

* Выполнение миграций
```
python manage.py migrate
```
* Заполнение базы данных информацией для тестов
```
python manage.py loaddata initial_data.json
```
#### Запуск асинхронного воркера
```
python manage.py rqworker default
```
#### Запуск тестов
```
python manage.py test
```

[Docker]: https://www.docker.com/get-started