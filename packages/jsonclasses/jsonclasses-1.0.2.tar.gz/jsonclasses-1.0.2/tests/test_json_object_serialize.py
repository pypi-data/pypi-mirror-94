import unittest
from jsonclasses import jsonclass, JSONObject, types
from datetime import datetime, date


class TestJSONObjectSerialize(unittest.TestCase):

    def test_serialize_str_to_str(self):
        @jsonclass(class_graph='test_serialize_1')
        class Contact(JSONObject):
            name: str
            address: str
        contact = Contact(name="John", address="Flamingo Road")
        self.assertEqual(contact.tojson(), {'name': 'John', 'address': 'Flamingo Road'})

    def test_serialize_int_to_int(self):
        @jsonclass(class_graph='test_serialize_2')
        class Point(JSONObject):
            x: int
            y: int
        point = Point(x=5, y=6)

        self.assertEqual(point.tojson(), {'x': 5, 'y': 6})

    def test_serialize_float_to_float(self):
        @jsonclass(class_graph='test_serialize_3')
        class Point(JSONObject):
            x: float
            y: float
        point = Point(x=5.5, y=6.6)
        self.assertEqual(point.tojson(), {'x': 5.5, 'y': 6.6})

    def test_serialize_bool_to_bool(self):
        @jsonclass(class_graph='test_serialize_4')
        class Status(JSONObject):
            active: bool
            enabled: bool
        status = Status(active=True, enabled=False)
        self.assertEqual(status.tojson(), {'active': True, 'enabled': False})

    def test_serialize_datetime_to_iso_str(self):
        @jsonclass(class_graph='test_serialize_5')
        class Timer(JSONObject):
            expired_at: datetime
        timer = Timer(**{'expiredAt': '2020-08-29T06:38:34.242000'})
        self.assertEqual(timer.tojson(), {'expiredAt': '2020-08-29T06:38:34.242Z'})

    def test_serialize_date_to_iso_str(self):
        @jsonclass(class_graph='test_serialize_6')
        class Countdown(JSONObject):
            day: date
        countdown = Countdown(**{'day': '2020-08-29'})
        self.assertEqual(countdown.tojson(), {'day': '2020-08-29T00:00:00.000Z'})

    def test_serialize_none_into_null(self):
        @jsonclass(class_graph='test_serialize_7')
        class Point(JSONObject):
            x: int
            y: int
        point = Point()
        point.x = 5
        self.assertEqual(point.tojson(), {'x': 5, 'y': None})

    def test_serialize_auto_camelize_keys(self):
        @jsonclass(class_graph='test_serialize_8')
        class Article(JSONObject):
            article_title: str
            article_content: str
        article = Article()
        article.article_title = "title"
        article.article_content = "content"
        self.assertEqual(
            article.tojson(),
            {'articleTitle': 'title', 'articleContent': 'content'}
        )

    def test_serialize_keep_snakecase_keys_if_explicitly_addressed(self):
        @jsonclass(class_graph='test_serialize_9', camelize_json_keys=False)
        class Article(JSONObject):
            article_title: str
            article_content: str
        article = Article()
        article.article_title = "title"
        article.article_content = "content"
        self.assertEqual(
            article.tojson(),
            {'article_title': 'title', 'article_content': 'content'}
        )

    def test_serialize_remove_writeonly_keys(self):
        @jsonclass(class_graph='test_serialize_10')
        class User(JSONObject):
            email: str
            password: str = types.str.writeonly
        user = User()
        user.email = 'a@bb.com'
        user.password = '123456'
        self.assertEqual(
            user.tojson(),
            {'email': 'a@bb.com'}
        )

    def test_serialize_do_not_remove_writeonly_keys_if_explicitly_specified(self):
        @jsonclass(class_graph='test_serialize_11')
        class User(JSONObject):
            email: str
            password: str = types.str.writeonly
        user = User()
        user.email = 'a@bb.com'
        user.password = '123456'
        self.assertEqual(
            user.tojson(ignore_writeonly=True),
            {'email': 'a@bb.com', 'password': '123456'}
        )
