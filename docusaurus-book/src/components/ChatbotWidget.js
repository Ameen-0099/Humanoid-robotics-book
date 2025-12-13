import React, { useState, useRef, useEffect } from 'react';
import ReactDOM from 'react-dom';
import styles from './ChatbotWidget.module.css';
import { API_CHATBOT } from '../utils/api'; // Import the centralized API endpoint

const ChatbotWidget = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [messages, setMessages] = useState(() => {
        if (typeof window !== 'undefined') { // Check if window (and thus localStorage) is defined
            const savedMessages = localStorage.getItem('chat_messages');
            return savedMessages ? JSON.parse(savedMessages) : [];
        }
        return []; // Return empty array during SSG
    });
    const [userInput, setUserInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [includeSelectedText, setIncludeSelectedText] = useState(false);
    const [highlightedText, setHighlightedText] = useState(''); // New state for captured text
    const messagesEndRef = useRef(null);

    useEffect(() => {
        if (typeof window !== 'undefined') {
            localStorage.setItem('chat_messages', JSON.stringify(messages));
        }
    }, [messages]);

    // State to ensure portal is only rendered on the client side
    const [isClient, setIsClient] = useState(false);
    useEffect(() => {
        setIsClient(true);
    }, []);

    // Effect to listen for text selections on the page
    useEffect(() => {
        const handleSelection = () => {
            const selection = window.getSelection().toString().trim();
            if (selection) {
                setHighlightedText(selection);
                setUserInput(selection); // Automatically fill the input box
                setIncludeSelectedText(true); // Automatically check the box
                console.log("DEBUG: Text selected and stored:", selection);
            }
        };

        document.addEventListener('mouseup', handleSelection);
        return () => {
            document.removeEventListener('mouseup', handleSelection);
        };
    }, []);

    // Auto-scroll to the bottom of messages
    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    const handleUserInput = (e) => {
        setUserInput(e.target.value);
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!userInput.trim()) return;

        const currentSelectedText = includeSelectedText ? highlightedText : null;
        console.log("DEBUG: Sending with selected text:", currentSelectedText);
        
        const newMessages = [
            ...messages,
            { 
                sender: 'user', 
                text: userInput, 
                selectedText: currentSelectedText
            }
        ];
        setMessages(newMessages);
        setUserInput('');
        setIsLoading(true);
        setIncludeSelectedText(false); // Reset checkbox
        // Don't clear highlightedText here, user might want to ask another question about it

        try {
            const requestBody = {
                question: userInput,
                selected_text: currentSelectedText || undefined,
            };

            const response = await fetch(API_CHATBOT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody),
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();

            const botMessage = {
                sender: 'bot',
                text: data.answer,
                sources: data.source_documents || [],
            };
            setMessages([...newMessages, botMessage]);
        } catch (error) {
            console.error('Error fetching chatbot response:', error);
            const errorMessage = {
                sender: 'bot',
                text: `Sorry, an error occurred: ${error.message}`,
            };
            setMessages([...newMessages, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };
    
    const handleClearChat = () => {
        setMessages([]);
        if (typeof window !== 'undefined') {
            localStorage.removeItem('chat_messages');
        }
    };
    
    const toggleChat = () => {
        setIsOpen(!isOpen);
    };

    const chatbotUI = (
        <div className={styles.chatbotContainer}>
            <button className={styles.chatToggleButton} onClick={toggleChat} aria-label={isOpen ? 'Close Chat' : 'Open Chat'}>
                {isOpen ? 'X' : 'Open Chat'}
            </button>
            {isOpen && (
                <div className={styles.chatWindow}>
                    <div className={styles.chatHeader}>
                        <h2>Humanoid Robotics Book AI</h2>
                        <button className={styles.clearChatButton} onClick={handleClearChat} aria-label="Clear Chat">
                            Clear Chat
                        </button>
                    </div>
                    <div className={styles.chatMessages}>
                        {messages.map((msg, index) => (
                            <div key={index} className={`${styles.message} ${styles[msg.sender]}`}>
                                <p>{msg.text}</p>
                                {msg.selectedText && <p className={styles.selectedTextDisplay}><i>(Context: "{msg.selectedText}")</i></p>}
                                {msg.sources && msg.sources.length > 0 && (
                                    <div className={styles.sources}>
                                        <strong>Sources:</strong>
                                        <ul>
                                            {msg.sources.map((source, i) => (
                                                <li key={i}>{source.filename} ({source.title})</li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        ))}
                        {isLoading && (
                            <div className={styles.loadingContainer}>
                                <div className={styles.loadingSpinner}></div>
                            </div>
                        )}
                        <div ref={messagesEndRef} /> {/* For auto-scrolling */}
                    </div>
                    <div className={styles.chatOptions}>
                        <label>
                            <input
                                type="checkbox"
                                checked={includeSelectedText}
                                onChange={(e) => setIncludeSelectedText(e.target.checked)}
                                disabled={isLoading}
                            />
                            Include selected text
                        </label>
                    </div>
                    <form className={styles.chatInputForm} onSubmit={handleSendMessage}>
                        <input
                            type="text"
                            value={userInput}
                            onChange={handleUserInput}
                            placeholder="Ask a question..."
                            disabled={isLoading}
                        />
                        <button type="submit" disabled={isLoading}>Send</button>
                    </form>
                </div>
            )}
        </div>
    );

    if (isClient) {
        return ReactDOM.createPortal(chatbotUI, document.body);
    } else {
        return null;
    }
};

export default ChatbotWidget;
