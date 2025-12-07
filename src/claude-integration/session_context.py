class SessionContext:
    def __init__(self):
        self.history = []

    def add_to_history(self, role, content):
        """
        Adds a message to the conversation history.

        Args:
            role: The role of the speaker (e.g., 'user', 'assistant').
            content: The content of the message.
        """
        self.history.append({'role': role, 'content': content})

    def get_history(self):
        """
        Returns the conversation history.
        """
        return self.history

    def clear_history(self):
        """
        Clears the conversation history.
        """
        self.history = []

if __name__ == '__main__':
    # Example usage:
    context = SessionContext()
    context.add_to_history('user', 'Hello, Claude!')
    context.add_to_history('assistant', 'Hello! How can I help you today?')
    
    print(context.get_history())
    
    context.clear_history()
    print(context.get_history())
