import unittest

import speedtest_http


class Speedtest_httpTestCase(unittest.TestCase):

    def setUp(self):
        self.app = speedtest_http.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Index', rv.data.decode())

    def test_lineplot_today(self):
        rv = self.app.get('/lineplot_today')
        self.assertIn('from midnight', rv.data.decode())

    def test_heatmap(self):
        rv = self.app.get('/heatmap_last30days')
        self.assertIn('last 30 days', rv.data.decode())

    def test_density_all(self):
        rv = self.app.get('/density_all')
        self.assertIn('density per day', rv.data.decode())

    def test_lineplot_selectable(self):
        rv = self.app.get('/lineplot_selectable')
        self.assertIn('Selectable window', rv.data.decode())

if __name__ == '__main__':
    unittest.main()
