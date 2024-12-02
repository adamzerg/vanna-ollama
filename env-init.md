conda create -n vanna-env python=3.10.12
conda activate vanna-env
pip install vanna[chromadb,ollama,sqlite3] pandas
pip install --upgrade certifi


# Config API
http://192.168.1.82:8080/api/dify/receive

# run fastapi
uvicorn dify_vanna_api:app --host 0.0.0.0 --reload --port 8080

# Prompt
{{shots}}
Output table in Markdown format