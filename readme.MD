1. Put data file (PDF) into folder data/
2. Install dependencies:
	pip install -r requirements.txt
	
3. ingest docs into Chroma DB:
	python -m app.ingest
	
4. Install Ollama
	sudo snap install Ollam
	
	# pull the model
	ollama pull llama3


5. Run the assistant:
	python -m app.main 
