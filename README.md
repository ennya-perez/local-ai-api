# Local AI Microservice (FastAPI + Ollama)

Microservicio en Python que expone una API RESTful para consumir el modelo **Qwen 2.5 7B** corriendo de forma 100% privada y local.

## Requisitos previos

1. Having installed [Ollama](https://ollama.com/).
2. Download the model executing in bash:
   ```bash
   ollama pull qwen2.5:7b

### Instalation and execution
Clone the repo:

```Bash
git clone [https://github.com/ennya-perez/local-ai-api](https://github.com/ennya-perez/local-ai-api.git)
cd local-ai-api
```
Create virtual enviroment and install dependencies:
```Bash
python -m venv venv
source .venv/bin/activate  # In Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Run the API:

```Bash
uvicorn main:app --reload
See interactive docs at http://127.0.0.1:8000/docs.
```