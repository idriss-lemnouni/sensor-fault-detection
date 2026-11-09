import argparse
import csv
from datetime import datetime
import json
from pathlib import Path
from statistics import median

WINDOWS = [
    ("2013-12-10 06:25:00", "2013-12-12 05:35:00"),
    ("2013-12-15 17:50:00", "2013-12-17 17:00:00"),
    ("2014-01-27 14:20:00", "2014-01-29 13:30:00"),
    ("2014-02-07 14:55:00", "2014-02-09 14:05:00"),
]


def evaluate(rows, history_size):
    history = []
    reports = {name: dict(tp=0, fp=0, fn=0, tn=0) for name in ("step", "robust")}
    last = None
    for row in rows:
        timestamp = row["timestamp"]
        when = datetime.fromisoformat(timestamp)
        if last is not None and when <= last:
            raise ValueError("Le CSV doit être trié et sans doublons.")
        last = when
        value = float(row["value"])
        if len(history) == history_size:
            center = median(history)
            mad = median(abs(point - center) for point in history)
            predictions = {"step": abs(value - history[-1]) > 5,
                           "robust": abs(value - center) > max(3, 4 * 1.4826 * mad)}
            labeled = any(start <= timestamp <= end for start, end in WINDOWS)
            for name, alarm in predictions.items():
                reports[name][("t" if alarm == labeled else "f") + ("p" if alarm else "n")] += 1
        history.append(value)
        if len(history) > history_size:
            history.pop(0)
    return reports


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()
    with args.csv.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) <= 24:
        parser.error("Au moins 25 mesures sont nécessaires.")
    scores = evaluate(rows, 24)
    assert all(sum(report.values()) == len(rows) - 24 for report in scores.values())
    print(json.dumps({"readings": len(rows), "warmup": 24, "point_counts": scores}, indent=2))
