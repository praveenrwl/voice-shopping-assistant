import React, { useState } from "react";

const InputBox = ({ setMessages, messages }) => {
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages([...messages, userMsg]);
    setInput("");

    const res = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    });

    const data = await res.json();
    const botMsg = { sender: "bot", text: data.reply };

    // Speak bot reply
    const utter = new SpeechSynthesisUtterance(data.reply);
    speechSynthesis.speak(utter);

    setMessages((prev) => [...prev, botMsg]);
  };

  const handleVoiceInput = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
    };
  };

  return (
    <div className="w-full max-w-xl flex items-center gap-2">
      <button
        className="bg-yellow-400 px-4 py-2 rounded-xl"
        onClick={handleVoiceInput}
      >
        🎙
      </button>
      <input
        className="flex-1 p-2 border rounded-lg"
        placeholder="Type or speak..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
      />
      <button className="bg-blue-500 text-white px-4 py-2 rounded-xl" onClick={sendMessage}>
        Send
      </button>
    </div>
  );
};

export default InputBox;
