import unittest

import speedtest_http


class Speedtest_httpTestCase(unittest.TestCase):

    def setUp(self):
        self.srv = speedtest_http.srv.test_client()

    def test_index(self):
        rv = self.srv.get('/')
        self.assertIn('Index', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
