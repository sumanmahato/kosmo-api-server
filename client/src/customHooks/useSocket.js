import { socket } from '../socket';

const useSocket = ({ handleSystemMessage = () => {} }) => {
  const sendUserMessage = (message) => {
    socket.emit('user-message', {
      message,
    });
  };

  socket.on('system-message', handleSystemMessage);

  return {
    actions: {
      sendUserMessage,
    },
    socket,
  };
};

export default useSocket;
