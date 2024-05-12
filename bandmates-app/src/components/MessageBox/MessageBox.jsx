import React, { useState } from 'react';
import { FaRegWindowMinimize } from "react-icons/fa";
import './MessageBox.css';

const MessageBox = () => {
  const [collapsed, setCollapsed] = useState(false);

  const toggleCollapse = () => {
    setCollapsed(!collapsed);
  };

  return (
    <div className={`message-container ${collapsed ? 'collapsed' : ''}`}>
      <div className="message-header">
        <h3>Messages</h3>
        <button onClick={toggleCollapse}>
          <FaRegWindowMinimize />
        </button>
      </div>
      {!collapsed && (
        <>
          <div className="message-body">
            {/* Message threads or conversation history will be displayed here */}
          </div>
          <div className="message-input">
            <textarea placeholder="Type your message..."></textarea>
            <button>Send</button>
          </div>
        </>
      )}
    </div>
  );
}

export default MessageBox;
