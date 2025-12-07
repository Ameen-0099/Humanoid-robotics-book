from ui_renderer import prompt_file_modification_authorization, prompt_command_execution_authorization

def request_file_modification_authorization(file_path, proposed_changes):
    """
    Requests user authorization for file modifications.

    Args:
        file_path: The path of the file to be modified.
        proposed_changes: A description of the proposed changes.

    Returns:
        True if the user authorizes the changes, False otherwise.
    """
    return prompt_file_modification_authorization(file_path, proposed_changes)

def request_command_execution_authorization(command):
    """
    Requests user authorization for command execution.

    Args:
        command: The command to be executed.

    Returns:
        True if the user authorizes the command, False otherwise.
    """
    return prompt_command_execution_authorization(command)

if __name__ == '__main__':
    # Example usage is now in ui_renderer.py
    pass
