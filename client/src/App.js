import { useEffect } from "react";
import ChatLayout from "./Components/ChatLayout";
import { connectWithSocketServer } from "./socketConnection";

function App() {
  useEffect(() => {
    connectWithSocketServer();
  } ,[])
  return (
    <div>
      <ChatLayout />
    </div>
  );
}

export default App;
