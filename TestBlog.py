import unittest
from project.models.model import db, app
from project.models.model import User, Category, Entry
import json

class Testing(unittest.TestCase):
    def setUp(self):
        self.app =app.test_client()
        self.app.testing =True
        db.create_all()
        db.session.add(User("testblog", "testblog@gmail.com", "123456"))
        db.session.commit()

        db.session.add(Category('Design'))
        db.session.commit()
        pass

    def check_username(self):
        result = self.app.post('/account/checkusername', data=dict(username='testblog'))
        self.assertEquals(result.status_code,200)
        data = result.data.decode()
        self.assertIn('201', data)

        result = self.app.post('/account/checkusername', data=dict(username='test123'))
        self.assertEquals(result.status_code, 200)
        data = result.data.decode()
        self.assertIn('200', data)

    def check_email(self):
        result = self.app.post('/account/checkemail', data=dict(email='testblog@gmail.com'))
        self.assertEquals(result.status_code, 200)
        data = result.data.decode()
        self.assertIn('201', data)

        result = self.app.post('/account/checkemail', data=dict(email='testblog1@gmail.com'))
        self.assertEquals(result.status_code, 200)
        data = result.data.decode()
        self.assertIn('200', data)

    def test_register(self):
        result = self.app.post('/register', data=dict(username='testblog1', email='testblog1@gmail.com', password='123456'))
        self.assertEquals(result.status_code, 200)
        data = result.data.decode()
        self.assertIn('200', data)

    def test_login(self):
        result = self.app.post('/login', data=dict(username='testblog', password='123456'), follow_redirects=True)
        self.assertEquals(result.status_code, 200)
        data = result.data.decode()
        self.assertIn('testblog', data)

    def test_inset_post(self):
        cat = Category.query.filter(Category.title == 'Design').first()
        result = self.app.post('/post/add', data=dict(categoryId=cat.id, title='test post add', content='test post add content', description='abc test', publish=True, tags='tags1,tags2'), follow_redirects=True)
        self.assertEquals(result.status_code, 200)
        data = result.data.decode()
        self.assertIn('test post add', data)
        self.assertIn('abc test', data)
        self.assertIn('tags1', data)
        self.assertIn('tags2', data)

    def tearDown(self):
        db.drop_all()

if __name__=='main':
    unittest.main()