const OLLAMA_API_ENDPOINT = 'http://localhost:11434/api/generate';
const MODEL = 'tinyllama';

async function* generateResponseStream(model, prompt) {
  try {
    const response = await fetch(OLLAMA_API_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify({
        model,
        prompt
      })
    });

    if (!response.ok) {
      throw new Error('error ah gya')
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const {done, value} = await reader.read()
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");

      for (let line of lines) {
        if (line.trim() !== "") {
          try {
            const parsed = JSON.parse(line);
            if (parsed.response) {
              yield parsed.response
            }
          } catch (e) {
            console.log(e)
          }
        }
      }
    }
  } catch(error) {
    console.log(error)
  }
}

async function executeLLM(prompt) {
  let fullResponse = '';
  for await(const responsePart of generateResponseStream(MODEL, prompt)) {
    fullResponse += responsePart;
  }

  return fullResponse;
}

module.exports = {
  executeLLM
}