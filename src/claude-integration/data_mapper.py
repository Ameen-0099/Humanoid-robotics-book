def map_assistance_request_to_api_format(assistance_request):
    """
    Maps an Assistance Request entity to the format expected by the Claude API.

    Args:
        assistance_request: A dictionary representing the assistance request.
                            Expected to have a 'prompt' key and a 'history' key.

    Returns:
        A dictionary in the format expected by the Claude API.
    """
    # This is a placeholder for the actual mapping logic.
    # The format will depend on the Claude API specifics.
    return {
        'prompt': assistance_request.get('prompt', ''),
        'history': assistance_request.get('history', [])
    }

if __name__ == '__main__':
    # Example usage:
    request = {
        'prompt': 'What is the capital of France?',
        'history': [
            {'role': 'user', 'content': 'Hello!'},
            {'role': 'assistant', 'content': 'Hi there!'}
        ]
    }
    api_request = map_assistance_request_to_api_format(request)
    print(api_request)
