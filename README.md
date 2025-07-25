### How to setup

Client setup

```bash
cd client
npm install
npm start # Client is running in port 3000
```

Server setup
```bash
cd server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Building the Vector Store
```bash
python app/scripts/build_vectorstore.py
```

Running the Server
```bash
python main.py  
```

Ollama Setup
Ensure Ollama is running.
You can replace or use your own LLM by changing the MODEL value in:
```bash
/server/app/models/ollama_wrapper.py
```

