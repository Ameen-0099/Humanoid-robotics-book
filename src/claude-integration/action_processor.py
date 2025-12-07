from authorization import request_file_modification_authorization, request_command_execution_authorization
import subprocess
import logging

logger = logging.getLogger(__name__)

def handle_file_modification_action(action_data):
    """
    Handles a file modification action from the Assistance Response.

    Args:
        action_data: A dictionary containing the data for the file modification.
                     Expected to have 'file_path' and 'proposed_changes' keys.

    Returns:
        A dictionary indicating the result of the action.
    """
    if 'file_path' not in action_data or 'proposed_changes' not in action_data:
        error_msg = "Missing 'file_path' or 'proposed_changes' for file_modification action"
        logger.error(error_msg)
        return {'error': error_msg}

    file_path = action_data['file_path']
    proposed_changes = action_data['proposed_changes']

    # Request authorization from the user
    if request_file_modification_authorization(file_path, proposed_changes):
        # In a real implementation, you would apply the changes to the file here.
        # For now, we'll just simulate success.
        logger.info(f"Applying changes to {file_path}...")
        return {'status': 'success', 'message': f'File {file_path} modified successfully.'}
    else:
        logger.info("File modification denied by user.")
        return {'status': 'denied', 'message': 'File modification denied by user.'}

def handle_command_execution_action(action_data):
    """
    Handles a command execution action from the Assistance Response.

    Args:
        action_data: A dictionary containing the data for the command execution.
                     Expected to have a 'command' key.

    Returns:
        A dictionary indicating the result of the action.
    """
    if 'command' not in action_data:
        error_msg = "Missing 'command' for command_execution action"
        logger.error(error_msg)
        return {'error': error_msg}

    command = action_data['command']

    # Request authorization from the user
    if request_command_execution_authorization(command):
        try:
            # Execute the command
            logger.info(f"Executing command: {command}")
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            logger.info(f"Command output: {result.stdout}")
            return {
                'status': 'success',
                'stdout': result.stdout,
                'stderr': result.stderr
            }
        except subprocess.CalledProcessError as e:
            logger.error(f"Command execution failed: {e}")
            return {
                'status': 'error',
                'message': 'Command execution failed.',
                'stdout': e.stdout,
                'stderr': e.stderr
            }
    else:
        logger.info("Command execution denied by user.")
        return {'status': 'denied', 'message': 'Command execution denied by user.'}


if __name__ == '__main__':
    # Example usage:
    mock_file_action = {
        'file_path': 'example.py',
        'proposed_changes': 'Refactor the "calculate" function.'
    }
    result = handle_file_modification_action(mock_file_action)
    print(result)

    mock_command_action = {
        'command': 'ls -l'
    }
    result = handle_command_execution_action(mock_command_action)
    print(result)
