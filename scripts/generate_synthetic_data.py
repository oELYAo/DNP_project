import json
import random

def random_text():
    words = ["hello", "world", "test", "data", "sample", "python", "mrjob", "mapreduce"]
    return " ".join(random.choices(words, k=random.randint(5, 15)))

def main(n=1000, out="synthetic_input.json"):
    with open(out, "w") as f:
        for i in range(n):
            doc = {"id": str(i), "text": random_text()}
            f.write(json.dumps(doc) + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=1000)
    parser.add_argument("--out", type=str, default="synthetic_input.json")
    args = parser.parse_args()
    main(args.n, args.out)