conda create -n vanna-env python=3.10.12
conda activate vanna-env
pip install vanna[chromadb,ollama,sqlite3] pandas
pip install --upgrade certifi
