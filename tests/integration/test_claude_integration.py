import unittest
from unittest.mock import patch
import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/claude-integration')))

from main import main

class TestClaudeIntegration(unittest.TestCase):

    @patch('builtins.input', side_effect=['Hello', 'exit'])
    @patch('main.handle_assist_request')
    @patch('main.render_response')
    def test_integration_flow(self, mock_render_response, mock_handle_assist_request, mock_input):
        # Mock the API response
        mock_handle_assist_request.return_value = {'completion': 'Hi there!'}

        # Run the main function
        main()

        # Assert that the response was rendered
        mock_render_response.assert_called_with({'completion': 'Hi there!'})

if __name__ == '__main__':
    unittest.main()
