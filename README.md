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

python main.py  # Server is running in port 5002
```


- Make sure ollama is running
- You can replace/use your own LLM by changing MODEL value in /server/app/models/ollama_wrapper.py

