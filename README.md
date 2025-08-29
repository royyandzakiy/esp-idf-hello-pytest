python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

pytest
pytest -s test_hello.py --embedded-services idf
