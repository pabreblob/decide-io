from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from base import mods


class PostProcTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            'type': 'IDENTITY',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5 },
                { 'option': 'Option 2', 'number': 2, 'votes': 0 },
                { 'option': 'Option 3', 'number': 3, 'votes': 3 },
                { 'option': 'Option 4', 'number': 4, 'votes': 2 },
                { 'option': 'Option 5', 'number': 5, 'votes': 5 },
                { 'option': 'Option 6', 'number': 6, 'votes': 1 },
            ]
        }

        expected_result = [
            { 'option': 'Option 1', 'number': 1, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 5', 'number': 5, 'votes': 5, 'postproc': 5 },
            { 'option': 'Option 3', 'number': 3, 'votes': 3, 'postproc': 3 },
            { 'option': 'Option 4', 'number': 4, 'votes': 2, 'postproc': 2 },
            { 'option': 'Option 6', 'number': 6, 'votes': 1, 'postproc': 1 },
            { 'option': 'Option 2', 'number': 2, 'votes': 0, 'postproc': 0 },
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    def test_weighted(self):
        data = {
            'type': 'WEIGHTED',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5,'weight':1},
                { 'option': 'Option 2', 'number': 2, 'votes': 0,'weight':1},
                { 'option': 'Option 3', 'number': 3, 'votes': 3,'weight':1},
                { 'option': 'Option 4', 'number': 4, 'votes': 2,'weight':2},
                { 'option': 'Option 5', 'number': 5, 'votes': 5,'weight':1.5},
                { 'option': 'Option 6', 'number': 6, 'votes': 1,'weight':1},
            ]
        }

        expected_result = [
            {'option': 'Option 5', 'number': 5, 'votes': 5,'weight':1.5,'postproc':7.5},
            {'option': 'Option 1', 'number': 1, 'votes': 5,'weight':1,'postproc': 5},
            {'option': 'Option 4', 'number': 4, 'votes': 2,'weight':2,'postproc': 4},
            {'option': 'Option 3', 'number': 3, 'votes': 3,'weight':1,'postproc': 3},
            {'option': 'Option 6', 'number': 6, 'votes': 1,'weight':1,'postproc': 1},
            {'option': 'Option 2', 'number': 2, 'votes': 0,'weight':1,'postproc': 0},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_random(self):
        data = {
            'type': 'RANDOM',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5},
                { 'option': 'Option 2', 'number': 2, 'votes': 0},
                { 'option': 'Option 3', 'number': 3, 'votes': 3},
                { 'option': 'Option 4', 'number': 4, 'votes': 2},
                { 'option': 'Option 5', 'number': 5, 'votes': 5},
                { 'option': 'Option 6', 'number': 6, 'votes': 1},
            ]
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertGreaterEqual(values[0]['percentageAccumulated'],values[0]['randomNumber'])

    def test_random2(self):
        data = {
            'type': 'RANDOM',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5},
                { 'option': 'Option 2', 'number': 2, 'votes': 0},
                { 'option': 'Option 3', 'number': 3, 'votes': 0},
                { 'option': 'Option 4', 'number': 4, 'votes': 0},
                { 'option': 'Option 5', 'number': 5, 'votes': 0},
                { 'option': 'Option 6', 'number': 6, 'votes': 0},
            ]
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values[0]['option'],'Option 1')

    def test_random3(self):
        data = {
            'type': 'RANDOM',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5},
                { 'option': 'Option 2', 'number': 2, 'votes': 4},
                { 'option': 'Option 3', 'number': 3, 'votes': 3},
                { 'option': 'Option 4', 'number': 4, 'votes': 4},
                { 'option': 'Option 5', 'number': 5, 'votes': 2},
                { 'option': 'Option 6', 'number': 6, 'votes': 0},
            ]
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values[0]['option'],'Option 6')

    def test_random4(self):
        data = {
            'type': 'RANDOM',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5},
                { 'option': 'Option 2', 'number': 2, 'votes': 0},
                { 'option': 'Option 3', 'number': 3, 'votes': 0},
                { 'option': 'Option 4', 'number': 4, 'votes': 0},
                { 'option': 'Option 5', 'number': 5, 'votes': 0},
                { 'option': 'Option 6', 'number': 6, 'votes': 0},
            ]
        }

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertGreaterEqual(values[0]['percentageAccumulated'],values[0]['randomNumber'])

    def test_borda1(self):
        data={
            'type':'BORDA',
            'options':{
                'choices':['a','b','c','d','e'],
                'votes':[['d', 'b', 'e', 'c', 'a'],
                         ['a', 'd', 'b', 'c', 'e'],
                         ['a', 'd', 'e', 'c', 'b']]
            }
        }

        expected = {'a': 11, 'b': 8, 'c': 6, 'd': 13, 'e': 7}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected)

    def test_borda2(self):
        data={
            'type':'BORDA',
            'options':{
                'choices':['a','b','c','d','e'],
                'votes':[['d', 'b', 'c', 'a', 'e'],
                         ['e', 'd', 'c', 'b', 'a'],
                         ['b', 'c', 'd', 'a', 'e'],
                         ['a', 'e', 'd', 'c', 'b'],
                         ['b', 'e', 'd', 'c', 'a']]
            }
        }

        expected = {'a': 11, 'b': 17, 'c': 14, 'd': 18, 'e': 15}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected)

    def test_borda3(self):
        data={
            'type':'BORDA',
            'options':{
                'choices':['a','b','c','d','e'],
                'votes':[['d', 'b', 'e', 'c', 'a'],
                         ['a', 'd', 'b', 'c', 'e'],
                         ['a', 'd', 'e', 'c', 'b']]
            }
        }

        expected = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values, expected)

