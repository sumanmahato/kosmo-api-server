import { io } from 'socket.io-client';

export const connectWithSocketServer = () => {
  const socket = io('http://localhost:5000');

  socket.on('connect', () => {
    console.log('connected with socket server');
    console.log(socket.id);
  });
};
