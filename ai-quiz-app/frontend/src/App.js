import React, { useState } from "react";

function App() {
  const [topic, setTopic] = useState("");
  const [question, setQuestion] = useState(null);
  const [selected, setSelected] = useState(null);
  const [result, setResult] = useState("");

  const fetchQuestion = async () => {
    const res = await fetch(`http://localhost:8000/quiz?topic=${encodeURIComponent(topic)}`);
    const data = await res.json();
    setQuestion(data);
    setSelected(null);
    setResult("");
  };

  const handleAnswer = (idx) => {
    setSelected(idx);
    if (idx === question.answer) {
      setResult("✅ Correct!");
    } else {
      setResult(`❌ Incorrect! Correct answer: ${question.options[question.answer]}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-xl mx-auto bg-white p-6 rounded-2xl shadow-lg">
        <h1 className="text-2xl font-bold mb-4 text-center">🧠 AI Quiz App</h1>
        <input
          className="w-full p-2 border rounded mb-4"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter a topic"
        />
        <button
          onClick={fetchQuestion}
          className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 mb-4"
        >
          Get Question
        </button>

        {question && (
          <>
            <h2 className="text-lg font-semibold mb-2">{question.question}</h2>
            <ul>
              {question.options.map((opt, idx) => (
                <li key={idx}>
                  <button
                    onClick={() => handleAnswer(idx)}
                    className={`w-full text-left p-2 my-1 rounded ${
                      selected === idx
                        ? idx === question.answer
                          ? "bg-green-200"
                          : "bg-red-200"
                        : "bg-gray-100 hover:bg-gray-200"
                    }`}
                  >
                    {idx + 1}. {opt}
                  </button>
                </li>
              ))}
            </ul>
            {result && <div className="mt-4 font-semibold">{result}</div>}
          </>
        )}
      </div>
    </div>
  );
}

export default App;