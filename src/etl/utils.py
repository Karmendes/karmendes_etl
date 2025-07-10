from datetime import datetime
import re
import os
from typing import List
import yaml



def load_yaml(path: str):
    try:
        with open(path, "r") as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        raise ValueError(f"Error loading YAML file '{path}': {str(e)}") from e


def list_files_with_timestamp(
    folder: str,
    from_dt: datetime,
    to_dt: datetime,
    timestamp_format: str
) -> List[str]:
    matched_files = []

    # Remove special characters to approximate a regex for the datetime
    regex_friendly = timestamp_format \
        .replace("%Y", r"\d{4}") \
        .replace("%m", r"\d{2}") \
        .replace("%d", r"\d{2}") \
        .replace("%H", r"\d{2}") \
        .replace("%M", r"\d{2}") \
        .replace("%S", r"\d{2}") \
        .replace(" ", r"\s?")  # allow optional space

    pattern = re.compile(regex_friendly)

    for filename in os.listdir(folder):
        match = pattern.search(filename)
        if not match:
            continue

        timestamp_str = match.group()

        try:
            timestamp = datetime.strptime(timestamp_str, timestamp_format)
        except ValueError:
            continue

        if from_dt <= timestamp <= to_dt:
            matched_files.append(os.path.join(folder, filename))

    return sorted(matched_files)