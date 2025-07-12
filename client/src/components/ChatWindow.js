import React from "react";

const ChatWindow = ({ messages }) => (
  <div className="w-full max-w-xl bg-white rounded-xl p-4 shadow-md mb-4 overflow-y-auto h-96">
    {messages.map((msg, i) => (
      <div
        key={i}
        className={`my-2 ${
          msg.sender === "user" ? "text-right" : "text-left"
        }`}
      >
        <span
          className={`inline-block px-3 py-2 rounded-xl ${
            msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200"
          }`}
        >
          {msg.text}
        </span>
      </div>
    ))}
  </div>
);

export default ChatWindow;
