import { useEffect } from 'react';
import { socket } from '../socket';

const useSocketConnection = () => {
  useEffect(() => {
    socket.on('connect', () => {
      console.log('connected with socket server');
      console.log(socket.id);
    });
  }, []);
};

export default useSocketConnection;
