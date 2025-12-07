from authorization import request_file_modification_authorization, request_command_execution_authorization

def handle_authorize_request(request_data):
    """
    Handles a request to the /authorize endpoint.

    Args:
        request_data: A dictionary containing the request data.
                      Expected to have an 'action' key ('file_modification' or 'command_execution'),
                      and other relevant data based on the action.

    Returns:
        A dictionary containing the authorization status.
    """
    if 'action' not in request_data:
        return {'error': 'Missing "action" in request data'}

    action = request_data['action']

    if action == 'file_modification':
        if 'file_path' not in request_data or 'proposed_changes' not in request_data:
            return {'error': 'Missing "file_path" or "proposed_changes" for file_modification action'}
        
        authorized = request_file_modification_authorization(
            request_data['file_path'],
            request_data['proposed_changes']
        )
        return {'authorized': authorized}

    elif action == 'command_execution':
        if 'command' not in request_data:
            return {'error': 'Missing "command" for command_execution action'}

        authorized = request_command_execution_authorization(request_data['command'])
        return {'authorized': authorized}

    else:
        return {'error': f'Invalid action: {action}'}

if __name__ == '__main__':
    # Example usage:
    # This would be called by your web server or application framework
    mock_file_mod_request = {
        'action': 'file_modification',
        'file_path': 'example.py',
        'proposed_changes': 'Refactor the "calculate" function.'
    }
    response = handle_authorize_request(mock_file_mod_request)
    print(response)

    mock_command_exec_request = {
        'action': 'command_execution',
        'command': 'git status'
    }
    response = handle_authorize_request(mock_command_exec_request)
    print(response)
