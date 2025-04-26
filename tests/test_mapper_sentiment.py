import subprocess
import tempfile
from pathlib import Path

def test_mapper_sentiment_basic():
    # Подготовка временного входного файла
    with tempfile.NamedTemporaryFile("w+", delete=False) as f:
        f.write("I love sunshine and joy\n")
        f.seek(0)
        input_path = f.name

    # Запуск маппера с перенаправлением stdin
    result = subprocess.run(
        ["python3", "mapper_sentiment.py"],
        stdin=open(input_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Проверка: вывод должен содержать doc_0 и числовой скор
    output = result.stdout.strip()
    assert output.startswith("doc_0\t")
    doc_id, score = output.split('\t')
    float(score)  # проверяем, что score — число
