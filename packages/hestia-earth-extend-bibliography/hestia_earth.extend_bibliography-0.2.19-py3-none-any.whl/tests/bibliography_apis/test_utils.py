import unittest
import re

from hestia_earth.extend_bibliography.bibliography_apis.utils import actor_id, actor_name, biblio_title


class FakeAuthor():
    def __init__(self):
        self.scopus_author_id = ''


class TestBibliographyUtils(unittest.TestCase):
    def test_actor_id(self):
        actor = {'scopusID': 'scopus_author_id'}
        self.assertEqual(actor_id(actor), actor.get('scopusID'))

        # no scopus, generate random value
        actor = {'scopusID': None}
        self.assertTrue(re.match(r'H-\d{10}$', actor_id(actor)))

    def test_actor_name(self):
        actor = {'lastName': 'Last Name'}
        self.assertEqual(actor_name(actor), 'Last Name')
        actor['firstName'] = 'First'
        self.assertEqual(actor_name(actor), 'F Last Name')
        actor['name'] = 'Full Name'
        self.assertEqual(actor_name(actor), actor['name'])

    def test_biblio_title(self):
        self.assertEqual(biblio_title(None), None)
        self.assertEqual(biblio_title('A random title'), 'A random title')
        self.assertEqual(biblio_title('A RANDOM TITLE'), 'A Random Title')


if __name__ == '__main__':
    unittest.main()
