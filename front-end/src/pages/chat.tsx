import { useState } from "react";

const Chat = () => {
  const [outputString, setOutputString] = useState("");
  const [queryStr, setQueryStr] = useState("");

  const handleGeneratePrompt = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/generate_prompt", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query_str: queryStr }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setOutputString(data.output_string);
    } catch (error) {
      console.error("Error generating prompt:", error);
    }
  };

  return (
    <div className="max-w-md mx-auto my-8">
      <input
        className="w-full p-2 mb-4 border border-gray-300 rounded-md"
        type="text"
        placeholder="Enter user input..."
        value={queryStr}
        onChange={(e) => setQueryStr(e.target.value)}
      />

      <button
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        onClick={handleGeneratePrompt}
      >
        Generate Prompt
      </button>

      {outputString && (
        <div className="mt-4 p-2 bg-gray-100 border border-gray-300 rounded-md">
          <strong>Generated Prompt:</strong>
          <p className="mt-2">{outputString}</p>
        </div>
      )}
    </div>
  );
};

export default Chat;
