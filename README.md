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
python3.7 -m venv env
```

```
source env/bin/activate
```

```
pip install -r requirements.txt
```

### Запуск окружения сторонних сервисов

```
sudo docker-compose up -d
```




[Docker]: https://www.docker.com/get-started