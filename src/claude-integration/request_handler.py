from api_client import ApiClient
import logging

logger = logging.getLogger(__name__)

def handle_assist_request(request_data):
    """
    Handles a request to the /assist endpoint.

    Args:
        request_data: A dictionary containing the request data.
                      Expected to have a 'prompt' key.

    Returns:
        A dictionary containing the response from the Claude API,
        or an error message.
    """
    if 'prompt' not in request_data:
        logger.error("Missing 'prompt' in request data")
        return {'error': 'Missing "prompt" in request data'}

    # Initialize the API client
    try:
        client = ApiClient()
    except ValueError as e:
        logger.error(f"Failed to initialize ApiClient: {e}")
        return {'error': str(e)}

    # Make the API call
    # The endpoint and payload format will depend on the Claude API specifics.
    # This is a placeholder for the actual implementation.
    response_data = client.post('completions', request_data) # Assuming a 'completions' endpoint

    if 'error' in response_data:
        logger.error(f"API request failed: {response_data.get('details')}")
        return response_data

    return response_data

if __name__ == '__main__':
    # Example usage:
    # This would be called by your web server or application framework
    mock_request = {'prompt': 'Explain the theory of relativity in simple terms.'}
    response = handle_assist_request(mock_request)
    print(response)
