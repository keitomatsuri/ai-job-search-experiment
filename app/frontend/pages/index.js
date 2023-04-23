import { useState } from "react";
import axios from "axios";

const Home = () => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async (event) => {
    event.preventDefault();

    if (input.trim() === "") {
      return;
    }

    setMessages((prevMessages) => [
      ...prevMessages,
      { role: "user", content: input },
    ]);
    setInput("");

    try {
      const response = await axios.post("http://localhost:5000/ask", {
        question: input,
        history: messages,
      });

      setMessages((prevMessages) => [
        ...prevMessages,
        { role: "assistant", content: response.data.answer },
      ]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="container mx-auto p-4 min-h-screen h-full flex flex-col">
      <h1 className="text-3xl mb-6">AI求人検索</h1>
      <div className="bg-gray-100 p-6 rounded-xl flex-grow flex flex-col">
        <div className="overflow-y-scroll flex-grow">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`my-2 p-4 rounded-xl ${
                message.role === "user"
                  ? "bg-blue-500 text-white"
                  : "bg-gray-300"
              }`}
            >
              <strong>{message.role === "user" ? "あなた" : "AI"}:</strong>{" "}
              {message.content}
            </div>
          ))}
        </div>
        <form onSubmit={sendMessage} className="mt-4 flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="メッセージを入力してください"
            className="flex-grow p-4 border-2 rounded-xl focus:outline-none focus:border-blue-500"
          />
          <button
            type="submit"
            className="ml-4 bg-blue-500 text-white px-6 py-2 rounded-xl hover:bg-blue-600"
          >
            送信
          </button>
        </form>
      </div>
    </div>
  );
};

export default Home;
