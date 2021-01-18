# Запуск проекта
Предполагалось, что проект будет собираться и запускаться с помощью docker-compose, но в последний момент что-то пошло не так. Проект будем разворачивать локально, но когда найду причину проблем с докером, обновлю инструкцию. Для разворачивания нужно: 
1. Установить зависимости из requirements.txt: 
```
pip3 install -r requirements.txt
```
2. Запустить скрипт для создания таблиц ```db/initdb.sql``` (предварительно нужно создать саму БД Postgres с параметрами, указанными в ```app/configdb.py```)
3. Запустить само приложение:
```
python3 app.py
```

# Запросы к API
1. [GET] Получить список номеров отеля
```
http://localhost:8000/get_rooms/{mode}
```
где ``` mode ``` - параметр от 0 до 3, задающий порядок сортировки.
0 - по возрастанию цены
1 - по убыванию цены
2 - по возрастанию даты добавления
3 - по убыванию даты добавления
Пример:
```
http://localhost:8000/get_rooms/2
```
2. [GET] Получить список бронирований для номера отеля
```
http://localhost:8000/get_bookinds/{room_id}
```
где ```room_id``` - id номера. 
Бронирования выводятся по возрастанию даты заезда. 
Пример:
```
http://localhost:8000/get_bookings/34
```
3. [POST] Создать новый номер в отеле. Параметры ```description, cost``` передаются в ```body```, url: ```http://localhost:8000/create_room```.
Пример запроса:
```
curl --location --request POST 'localhost:8000/create_room' \
--header 'Content-Type: application/json' \
--data-raw '{
    "description": "vip paradise",
    "cost": 4302
}'
```
Возвращает ID успешно созданного номера. 

4. [POST] Забронировать номер. Параметры ```date_from, date_to, room_id``` передаются в ```body```, url: ```http://localhost:8000/create_booking```.
Пример запроса:
```
curl --location --request POST 'localhost:8000/create_booking' \
--header 'Content-Type: application/json' \
--data-raw '{
    "room_id": 1,
    "date_from": "2021-02-09",
    "date_to": "2021-02-12"
}'
```
Возвращает ID бронирования. 
Дата должна быть формата "YYYY-MM-DD", в случае не соответствия формату возвращается ошибка. Также возвращается ошибка при некорректной даты отъезда (раньше чем дата заезда).
5. [POST] Удалить номер из базы. Параметры ```mode```, ```raw_id``` (в данном случае это id номера) передаются в ```body```, url: ```http://localhost:8000/delete```. ```mode``` - параметр, в зависимости от которого метод применяется к таблице бронирований (0) или к таблице номеров (1). 
Также удаляются оформленные в этот номер бронирования. Пример:
```
curl --location --request POST 'localhost:8000/delete' \
--header 'Content-Type: application/json' \
--data-raw '{
    "raw_id": 1,
    "mode": 0
}'
```
6. [POST] Удалить бронирование из базы. Параметры ```mode```, ```raw_id``` (в данном случае это id бронирования) передаются в ```body```, url: ```http://localhost:8000/delete```. ```mode``` - параметр, в зависимости от которого метод применяется к таблице бронирований (0) или к таблице номеров (1). 
Пример:
```
curl --location --request POST 'localhost:8000/delete' \
--header 'Content-Type: application/json' \
--data-raw '{
    "raw_id": 2324,
    "mode": 1
}'
```
