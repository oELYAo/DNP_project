import subprocess
import tempfile
import os
import json

def test_mapper_sentiment_basic():
    # Создаём временный JSON-файл с doc_id и text
    data = {"doc_id": "doc_0", "text": "I love sunshine and joy"}
    
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write(json.dumps(data) + "\n")
        f.seek(0)
        input_path = f.name

    # Запускаем маппер с перенаправлением stdin
    result = subprocess.run(
        ["python3", "src/mapreduce/mapper_sentiment.py"],
        stdin=open(input_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output = result.stdout.strip()
    
    # Проверка: начинается с doc_0 и содержит таб + число
    assert output.startswith("doc_0\t")
    parts = output.split("\t")
    assert len(parts) == 2
    assert parts[0] == "doc_0"
    assert isinstance(int(parts[1]), int)

    os.unlink(input_path)
