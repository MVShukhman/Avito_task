from configdb import *
import datetime
import json
import psycopg2


def get_connection():
    conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER,
                            password=POSTGRES_PASSWORD, host='localhost', port=POSTGRES_PORT)
    return conn


def insert_booking(date_from, date_to, room_id):
    try:
        if datetime.datetime.strptime(date_from, API_DATE_FORMAT) > \
                datetime.datetime.strptime(date_to, API_DATE_FORMAT):
            return 'Error', 'Incorrect departure date!'
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"select id from \"Rooms\" where id = {room_id}")
        if not len(cursor.fetchall()):
            return 'Error', 'This room doesn\'t exist!'
        cursor.execute(
            f"insert into \"Bookings\" (room_id, date_from, date_to) values ({room_id}, \'{date_from}\', \'{date_to}\')"
            f" returning id"
        )
        conn.commit()
        booking_id = cursor.fetchall()[0][0]
        conn.close()
        return 'BookingID', booking_id

    except ValueError:
        return 'Error', 'Incorrect format!'
    except Exception as e:
        return 'Error', e


def delete_row(mode, row_id):
    tablename = "Bookings" if mode == 0 else "Rooms"
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"delete from \"{tablename}\" where id = {booking_id}")
        conn.commit()
        conn.close()
        return 'Msg', 'Success!'
    except Exception as e:
        return 'Error', e


def get_bookings(room_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"select id, date_from, date_to from \"Bookings\" where room_id = {room_id} order by date_from")
        columns = ('id', 'date_from', 'date_to')
        response = cursor.fetchall()

        results = []
        for row in response:
            results.append(dict(zip(columns, row)))
            results[-1]['date_from'] = results[-1]['date_from'].strftime(API_DATE_FORMAT)
            results[-1]['date_to'] = results[-1]['date_to'].strftime(API_DATE_FORMAT)

        conn.close()
        return 'Bookings', json.dumps(results, indent=2)
    except Exception as e:
        return 'Error', e


def insert_room(description, cost):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        add_date = datetime.datetime.now().strftime(API_DATE_FORMAT)
        cursor.execute(
            f"insert into \"Rooms\" (description, cost, added) values (\'{description}\', {cost}, \'{add_date}\')"
            f" returning id"
        )
        conn.commit()
        booking_id = cursor.fetchall()[0][0]
        conn.close()
        return 'RoomID', booking_id

    except ValueError:
        return 'Error', 'Incorrect format!'
    except Exception as e:
        return 'Error', e


def get_rooms(mode):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if mode == 0:
            cursor.execute(f"select * from \"Rooms\" order by added")
        elif mode == 1:
            cursor.execute(f"select * from \"Rooms\" order by added desc")
        elif mode == 2:
            cursor.execute(f"select * from \"Rooms\" order by cost")
        elif mode == 3:
            cursor.execute(f"select * from \"Rooms\" order by cost desc")
        columns = ('description', 'cost', 'id', 'added')
        response = cursor.fetchall()

        results = []
        for row in response:
            results.append(dict(zip(columns, row)))
            results[-1]['added'] = results[-1]['added'].strftime(API_DATE_FORMAT)

        conn.close()
        return 'Rooms', json.dumps(results, indent=2)
    except Exception as e:
        return 'Error', e