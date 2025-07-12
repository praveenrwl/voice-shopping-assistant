import React, { useState } from "react";
import ChatWindow from "./components/ChatWindow";
import InputBox from "./components/InputBox";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! How can I help you today?" },
  ]);

  return (
    <div className="App flex flex-col items-center p-6 min-h-screen bg-gray-100">
      <h1 className="text-3xl font-bold mb-4">🛍️ AI Shopping Assistant</h1>
      <ChatWindow messages={messages} />
      <InputBox setMessages={setMessages} messages={messages} />
    </div>
  );
}

export default App;
