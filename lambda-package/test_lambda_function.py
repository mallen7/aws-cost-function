import unittest
from unittest.mock import patch
from awscostfunction import lambda_handler  # Replace with your script's name
import json
from datetime import datetime

class TestLambdaFunction(unittest.TestCase):

    def setUp(self):
        # Mock today's date if needed
        self.mocked_today = datetime(2024, 1, 3)

    @patch('main.get_secret')
    @patch('main.get_cost_data')
    @patch('requests.post')
    def test_lambda_handler(self, mock_post, mock_get_cost_data, mock_get_secret):
        # Mock the secret values
        mock_get_secret.return_value = {
            'pushover_user_key': 'mocked_key',
            'pushover_app_token': 'mocked_token'
        }

        # Mock the AWS Cost Explorer response
        mock_get_cost_data.return_value = {
            'ResultsByTime': [{
                'Groups': [
                    {
                        'Keys': ['Service1'],
                        'Metrics': {'UnblendedCost': {'Amount': '123.45', 'Unit': 'USD'}}
                    },
                    {
                        'Keys': ['Service2'],
                        'Metrics': {'UnblendedCost': {'Amount': '67.89', 'Unit': 'USD'}}
                    }
                ]
            }]
        }

        # Mocking datetime.now() to return a fixed date
        with patch('main.datetime') as mock_datetime:
            mock_datetime.now.return_value = self.mocked_today
            response = lambda_handler({}, {})  # Empty event and context

        # Assertions to validate the function behavior
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Service1', response['body'])
        self.assertIn('Service2', response['body'])
        self.assertIn('Total: $191.34', response['body'])

        # In your test_lambda_function.py
        self.assertIn('Service1', json.loads(response['body']))
        self.assertIn('Service2', json.loads(response['body']))
        self.assertIn('Total: $191.34', json.loads(response['body']))

        # Asserting that the Pushover API was called
        mock_post.assert_called_once()

if __name__ == '__main__':
    unittest.main()
