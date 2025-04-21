import argparse
from utils.logging_config import setup_logging


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Distributed Text Mining Pipeline")
    parser.add_argument("--input", required=True, help="Input file path")
    parser.add_argument(
        "--job",
        choices=["wordcount", "sentiment"],
        required=True,
        help="Job type to run",
    )
    args = parser.parse_args()
    # TODO: dispatch to job modules


if __name__ == "__main__":
    main()
