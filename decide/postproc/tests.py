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
                { 'option': 'Option 5', 'number': 5, 'votes': 5,'weight':1.5}
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 5, 'weight': 1, 'postproc': 5},
            {'option': 'Option 5', 'number': 5, 'votes': 5,'weight':1.5,'postproc':7.5}

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


    def test_genderParity(self):
        data = {
            'type': 'GENDER',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5, 'gender':'m'},
                { 'option': 'Option 2', 'number': 2, 'votes': 0, 'gender':'w'},
                { 'option': 'Option 3', 'number': 3, 'votes': 3, 'gender':'w'},
                { 'option': 'Option 4', 'number': 4, 'votes': 2, 'gender':'m'},
                { 'option': 'Option 5', 'number': 5, 'votes': 5, 'gender':'w'},
                { 'option': 'Option 6', 'number': 6, 'votes': 1, 'gender':'w'},
            ]
        }

        expected_result = [
            {'option': 'Option 1', 'number': 1, 'votes': 5, 'gender': 'm','postproc':5},
            {'option': 'Option 5', 'number': 5, 'votes': 5, 'gender': 'w','postproc':5},
            {'option': 'Option 3', 'number': 3, 'votes': 3, 'gender': 'w','postproc':3},
            {'option': 'Option 4', 'number': 4, 'votes': 2, 'gender': 'm','postproc':2}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)

    def test_borda1(self):
        data = {
            'type': 'BORDA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 10},
                { 'option': 'Option 2', 'number': 2, 'votes': 20},
                { 'option': 'Option 3', 'number': 3, 'votes': 25},
                { 'option': 'Option 4', 'number': 4, 'votes': 15},
                { 'option': 'Option 5', 'number': 5, 'votes': 30},
                { 'option': 'Option 6', 'number': 6, 'votes': 5}
            ]
        }

        expected_result = [
            {'option': 'Option 5', 'number': 5, 'votes': 30, 'postproc': 5.0},
            {'option': 'Option 3', 'number': 3, 'votes': 25, 'postproc': 4.16667},
            {'option': 'Option 2', 'number': 2, 'votes': 20, 'postproc': 3.33333},
            {'option': 'Option 4', 'number': 4, 'votes': 15, 'postproc': 2.5},
            {'option': 'Option 1', 'number': 1, 'votes': 10, 'postproc': 1.66667},
            {'option': 'Option 6', 'number': 6, 'votes': 5, 'postproc': 0.83333}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_borda2(self):
        data = {
            'type': 'BORDA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 22},
                { 'option': 'Option 2', 'number': 2, 'votes': 22},
                { 'option': 'Option 3', 'number': 3, 'votes': 16},
            ]
        }

        expected_result = [
                { 'option': 'Option 1', 'number': 1, 'votes': 22, 'postproc': 7.33333},
                { 'option': 'Option 2', 'number': 2, 'votes': 22, 'postproc': 7.33333},
                { 'option': 'Option 3', 'number': 3, 'votes': 16, 'postproc': 5.33333},
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_borda3(self):
        data = {
            'type': 'BORDA',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 185},
                { 'option': 'Option 2', 'number': 2, 'votes': 175},
                { 'option': 'Option 3', 'number': 3, 'votes': 165},
                { 'option': 'Option 4', 'number': 4, 'votes': 155},
                { 'option': 'Option 5', 'number': 5, 'votes': 145},
                { 'option': 'Option 6', 'number': 6, 'votes': 165},
                { 'option': 'Option 7', 'number': 7, 'votes': 165},
                { 'option': 'Option 8', 'number': 8, 'votes': 165},
                { 'option': 'Option 9', 'number': 9, 'votes': 165},
                { 'option': 'Option 10', 'number': 10, 'votes': 165}
            ]
        }

        expected_result = [
                { 'option': 'Option 1', 'number': 1, 'votes': 185, 'postproc': 18.5},
                { 'option': 'Option 2', 'number': 2, 'votes': 175, 'postproc': 17.5},
                { 'option': 'Option 3', 'number': 3, 'votes': 165, 'postproc': 16.5},
                { 'option': 'Option 6', 'number': 6, 'votes': 165, 'postproc': 16.5},
                { 'option': 'Option 7', 'number': 7, 'votes': 165, 'postproc': 16.5},
                { 'option': 'Option 8', 'number': 8, 'votes': 165, 'postproc': 16.5},
                { 'option': 'Option 9', 'number': 9, 'votes': 165, 'postproc': 16.5},
                { 'option': 'Option 10', 'number': 10, 'votes': 165, 'postproc': 16.5},
                { 'option': 'Option 4', 'number': 4, 'votes': 155, 'postproc': 15.5},
                { 'option': 'Option 5', 'number': 5, 'votes': 145, 'postproc': 14.5}
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertNotEqual(values, expected_result)


    def test_hondt(self):
        data = {
            'type': 'HONDT',
            'options': {
                'escanos': 3,
                'votes': [{'option': 'Option 1', 'seat': 1, 'votes': 15},
                          {'option': 'Option 2', 'seat': 0, 'votes': 3},
                          {'option': 'Option 3', 'seat': 1, 'votes': 9},
                          {'option': 'Option 4', 'seat': 0, 'votes': 7},
                          {'option': 'Option 5', 'seat': 1, 'votes': 12},
                          {'option': 'Option 6', 'seat': 0, 'votes': 1}
                          ]
            }
        }

        expected = {1, 0, 1, 0, 1, 0}

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()

        compare = []
        for i in values:
            compare.append(i['seat'])

        self.assertNotEqual(compare, expected)


    def test_ageLimit(self):
        data = {
            'type': 'AGE',
            'options': [
                {'option': 'Option 1', 'number': 1, 'votes': 5, 'age': 29},
                {'option': 'Option 2', 'number': 2, 'votes': 0, 'age': 34},
                {'option': 'Option 3', 'number': 3, 'votes': 3, 'age': 31},
                {'option': 'Option 4', 'number': 4, 'votes': 2, 'age': 25},
                {'option': 'Option 5', 'number': 5, 'votes': 5, 'age': 37},
                {'option': 'Option 6', 'number': 6, 'votes': 1, 'age': 42},
            ]
        }

        expected_result = [
            {'option': 'Option 3', 'number': 3, 'votes': 3, 'age': 31, 'postproc':30},
            {'option': 'Option 2', 'number': 2, 'votes': 0, 'age': 34, 'postproc':30},
            {'option': 'Option 5', 'number': 5, 'votes': 5, 'age': 37, 'postproc':30},

        ]


        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
    def test_weightedrandom(self):
        data = {
            'type': 'WEIGHTEDRANDOM',
            'options': [
                { 'option': 'Option 1', 'number': 1, 'votes': 5, 'weight':1},
                { 'option': 'Option 2', 'number': 2, 'votes': 0, 'weight':0.7},
                { 'option': 'Option 3', 'number': 3, 'votes': 3, 'weight':1},
                { 'option': 'Option 4', 'number': 4, 'votes': 2, 'weight':3},
                { 'option': 'Option 5', 'number': 5, 'votes': 5, 'weight':2},
                { 'option': 'Option 6', 'number': 6, 'votes': 1, 'weight':1.5},
            ]
        }
        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertGreaterEqual(values[0]['percentageAccumulated'],values[0]['randomNumber'])
