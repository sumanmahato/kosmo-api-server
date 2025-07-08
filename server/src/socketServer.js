const { Server } = require('socket.io');
const { v4: uuid } = require('uuid');
const { executeLLM } = require('./llm-util');

const registerSocketServer = (server) => {
  const io = new Server(server, {
    cors: {
      origin: '*',
      methods: ['GET', 'POST'],
    },
  });

  io.on('connection', (socket) => {
    console.log(`user connected ${socket.id}`);

    socket.on('user-message', (data) => {
      userMessageHandler(socket, data);
    });
  });
};

const userMessageHandler = async (socket, data) => {
  const { message } = data;
  const aiContent = await executeLLM(message.content);
  const systemMessage = {
    content: aiContent,
    id: uuid(),
    type: 'system',
  };

  socket.emit('system-message', systemMessage);
};

module.exports = { registerSocketServer };
