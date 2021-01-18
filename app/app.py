import db_module
import json
import tornado.web


class CreateBookingHandler(tornado.web.RequestHandler):
    def post(self):
        b = self.request.body
        json_string = b.decode('utf-8').replace("'", '"')
        data = json.loads(json_string)
        date_from = data['date_from']
        date_to = data['date_to']
        room_id = data['room_id']
        response = db_module.insert_booking(date_from, date_to, room_id)
        self.write({response[0]: response[1]})


class CreateRoomHandler(tornado.web.RequestHandler):
    def post(self):
        self.write('FUCK')
        b = self.request.body
        json_string = b.decode('utf-8').replace("'", '"')
        data = json.loads(json_string)
        description = data['description']
        cost = data['cost']
        response = db_module.insert_room(description, cost)
        self.write({response[0]: response[1]})


class DeleteHandler(tornado.web.RequestHandler):
    def post(self):
        b = self.request.body
        json_string = b.decode('utf-8').replace("'", '"')
        data = json.loads(json_string)
        index = data['id']
        mode = data['mode']
        response = db_module.delete_row(mode=mode, row_id=index)
        self.write({response[0]: response[1]})


class GetRoomsHandler(tornado.web.RequestHandler):
    def get(self, mode):
        response = db_module.get_rooms(int(mode))
        self.write(response[1])


class GetBookingsHandler(tornado.web.RequestHandler):
    def get(self, room_id):
        response = db_module.get_bookings(int(room_id))
        self.write({response[0]: json.loads(response[1])})


def make_app():
    return tornado.web.Application([
        (r"/create_booking", CreateBookingHandler),
        (r"/create_room", CreateRoomHandler),
        (r"/get_bookings/([0-9]+)", GetBookingsHandler),
        (r"/get_rooms/([0-9]+)", GetRoomsHandler),
        (r"/delete", DeleteHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
