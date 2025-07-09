const { Server } = require('socket.io');
const { v4: uuid } = require('uuid');
// const { executeLLM } = require('./llm-util');
const { ragChat } = require('./ragChat.js');

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

// const userMessageHandler = async (socket, data) => {
//   const { message } = data;
//   const aiContent = await executeLLM(message.content);
//   const systemMessage = {
//     content: aiContent,
//     id: uuid(),
//     type: 'system',
//   };

//   socket.emit('system-message', systemMessage);
// };
const userMessageHandler = async (socket, data) => {
  const { message } = data;

  try {
    // ⬇️ Call RAG flow instead of plain LLM
    const aiContent = await ragChat(message.content);

    const systemMessage = {
      content: aiContent,
      id: uuid(),
      type: 'system',
    };

    socket.emit('system-message', systemMessage);
  } catch (error) {
    console.error('Error in userMessageHandler:', error);

    socket.emit('system-message', {
      content: "Sorry, something went wrong processing your message.",
      id: uuid(),
      type: 'system',
    });
  }
};

module.exports = { registerSocketServer };
