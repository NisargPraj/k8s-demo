import unittest
from app import app

class FlaskTestCase(unittest.TestCase):

    # Ensure that the homepage loads correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)

    # Ensure that the 'create' page behaves correctly
    def test_create_page(self):
        tester = app.test_client(self)
        response = tester.get('/create')
        self.assertEqual(response.status_code, 200)
    
    # Ensure that a 404 is returned for an invalid page
    def test_404(self):
        tester = app.test_client(self)
        response = tester.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
