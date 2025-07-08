import { useEffect, useRef, useState } from 'react';
import './chat-layout.css';

export default function ChatLayout() {
  const [messageBuffer, setMessageBuffer] = useState([]);
  const userMessageRef = useRef(null);
  const messageContainerRef = useRef(null);

  const handleSend = () => {
    if (!userMessageRef.current.value) return;
    console.log(userMessageRef.current.value);
    const messages = [...messageBuffer];
    messages.push({
      type: messageBuffer.length % 2 === 0 ? 'user' : 'system',
      message: userMessageRef.current.value,
    });
    setMessageBuffer(messages);
    userMessageRef.current.value = '';
  };

  useEffect(() => {
    messageContainerRef.current.scroll({
      top: messageContainerRef.current.scrollHeight,
      behavior: 'smooth',
    });
  }, [messageBuffer]);

  return (
    <div className="chat-layout">
      <div className="chat-layout__message-container" ref={messageContainerRef}>
        {messageBuffer.map((item) => (
          <div
            className={`chat-layout__message chat-layout__message--${item.type}`}
          >
            {item.message}
          </div>
        ))}
      </div>
      <div className="chat-layout__action_items">
        <input
          ref={userMessageRef}
          name="user-message"
          type="text"
          placeholder='Send a message...'
          className="chat-layout__action-items-input"
        />
        <button
          type="button"
          className="chat-layout__action-items-send-button"
          onClick={handleSend}
        >
          Send
        </button>
      </div>
    </div>
  );
}
