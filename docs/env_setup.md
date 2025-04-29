# Distributed Text Mining Project

## Development Setup

1. Create virtual environment (requires Python 3.9):
```bash
python3.9 -m venv venv
source venv/bin/activate  # Linux/MacOS
# OR
venv\Scripts\activate.bat  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install package in development mode:
```bash
pip install -e .
```

## Running the Pipeline
```bash
python src/run_pipeline.py --input <path> --job <wordcount|sentiment>
```