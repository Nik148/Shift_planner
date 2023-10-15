# Shift_planner
Бекэнд сервис для планировщика смен

После запуска сервиса документацию можно посмотреть по url: http://localhost:8000/docs
## Инструкция к запуску сервиса
### Docker:
```
docker-compose build
docker-compose up
```
### Запуск в локальной системе:
Подготовка к запуску:
```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```
Запуск сервиса:
```
python main.py
```
### Тестирование
```
pytest test
```
