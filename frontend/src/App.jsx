import { useState , useEffect} from 'react'

import './App.css'

function App() {
  const [message,setMessage] = useState(0);
  const [messages,setMessages] = useState([]);
  const [sessionId,setSessionId] = useState(null);

  useEffect(()=>{
    if(!sessionId) return;
    const intervalId = setInterval(async()=>{
      try {
        const response = await fetch(
          `http://localhost:8000/api/chat/sessions/${sessionId}/`,
          { method: 'GET' }
        );
        const data = await response.json();
        setMessages(data.messages);
      } catch (err) {
        console.error("Error fetching messages:", err);
      }
}, 1000);

    return () => clearInterval(intervalId);
  }, [sessionId]);


  const sendMessage = async (e) => {
    if(e.key === 'Enter'){
      let setMessage=("");
      setMessages([...messages,{role:"user",content:message}])}}
    

  return (
    <div className="wrapper">
      <div className="chat-wrapper">
        <div className="chat-history">
          <div>
            {messages.map((message, index) => (
            <div
            key={index} 
            className={`message ${message.role === 'user' ? 'user' : ''}`}>
          {message.role=="user" ? "Me: ": "AI: "}: {message.content}
          </div>
            ))}
          </div>
        </div>
        </div>
        <input type="text" placeholder='Type a message...' value={message} 
        onChange={(e)=>setMessage(e.target.value)}
        onKeyUp={sendMessage}
        />
      </div>
  
  );
} 

export default App
