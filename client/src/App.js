import ChatLayout from './Components/ChatLayout';
import useSocketConnection from './customHooks/useSocketConnection';

function App() {
  useSocketConnection();

  return (
    <div>
      <ChatLayout />
    </div>
  );
}

export default App;
