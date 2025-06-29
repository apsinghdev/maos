run:
	PYTHONPATH=src uvicorn api.main:app --host 127.0.0.1 --port 6000 --reload