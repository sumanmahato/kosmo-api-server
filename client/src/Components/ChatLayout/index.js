import { useEffect, useRef, useState } from "react";
import { v4 as uuid } from "uuid";

import useSocket from "../../customHooks/useSocket";
import "./chat-layout.css";

export default function ChatLayout() {
  const [messageBuffer, setMessageBuffer] = useState([]);
  const userMessageRef = useRef(null);
  const messageContainerRef = useRef(null);
  const [loader, setLoader] = useState(false);

  const handleSystemMessage = (data) => {
    console.log("Received system message:", data);
    setLoader(false);
    const updatedMessageBuffer = [...messageBuffer];
    updatedMessageBuffer.push(data);
    setMessageBuffer(updatedMessageBuffer);
  };

  const { actions } = useSocket({ handleSystemMessage });

  const handleSend = () => {
    if (!userMessageRef.current.value) return;

    const message = {
      type: "user",
      content: userMessageRef.current.value,
      id: uuid(),
    };

    const updatedMessageBuffer = [...messageBuffer];
    updatedMessageBuffer.push(message);
    setMessageBuffer(updatedMessageBuffer);
    userMessageRef.current.value = "";

    // send message to server
    setLoader(true);
    actions.sendUserMessage(message);
  };

  const handleKeyPress = (e) => {
    if (e.code === "Enter") {
      handleSend();
    }
  };

  useEffect(() => {
    messageContainerRef.current.scroll({
      top: messageContainerRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [messageBuffer]);

  return (
    <div className="chat-layout">
      <div className="chat-layout__message-container" ref={messageContainerRef}>
        {messageBuffer.map((item) => (
          <div
            className={`flex-container flex-container--${
              item.type === "user" ? "right" : "left"
            }`}
          >
            <div
              key={item.id}
              className={`chat-layout__message chat-layout__message--${item.type}`}
            >
              {item.content?.message || item.content}
              {item.content?.resources?.map(d => <div>{d}</div>)}
            </div>
          </div>
        ))}
        {loader && (
          <div className="chat-layout__message">Loading Response...</div>
        )}
      </div>
      <div className="chat-layout__action_items">
        <input
          ref={userMessageRef}
          name="user-message"
          type="text"
          placeholder="Send a message..."
          className="chat-layout__action-items-input"
          onKeyDown={handleKeyPress}
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
