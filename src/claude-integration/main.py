from request_handler import handle_assist_request
from ui_renderer import render_response
from data_mapper import map_assistance_request_to_api_format
from session_context import SessionContext
from logger import setup_logger

def main():
    """
    Main function for the Claude Code integration.
    """
    logger = setup_logger()
    context = SessionContext()

    while True:
        # In a real application, this would be triggered by a user action
        # in the development environment.
        user_prompt = input("You: ")
        if user_prompt.lower() in ['exit', 'quit']:
            break

        logger.info(f"User prompt: {user_prompt}")
        context.add_to_history('user', user_prompt)

        # Map the user prompt to the API request format
        assistance_request = {
            'prompt': user_prompt,
            'history': context.get_history()
        }
        api_request_data = map_assistance_request_to_api_format(assistance_request)
        logger.info(f"API request: {api_request_data}")

        # In a real application, this would be an asynchronous call
        # to avoid blocking the UI while waiting for the API response.
        response_data = handle_assist_request(api_request_data)
        logger.info(f"API response: {response_data}")

        # Add assistant's response to history
        if 'error' not in response_data:
            # Assuming the response has a 'completion' key
            assistant_response = response_data.get('completion', '')
            context.add_to_history('assistant', assistant_response)

        # Render the response
        render_response(response_data)

if __name__ == '__main__':
    main()
