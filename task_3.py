import sys
import re


LEVELS_RE = re.compile(r'(INFO|DEBUG|ERROR|WARNING)', re.IGNORECASE)


def parse_log_line(line: str) -> dict:
    """
    Parse a single log line robustly.
    Handles cases like:
      2024-01-22 12:45:05 DEBUG Checking system health.
      2024-01-22 12:45:05 DEBUGChecking system health.
    Returns dict with keys: date, time, level, message.
    Raises ValueError on irrecoverable format problems.
    """
    line = line.rstrip("\n")
    if not line.strip():
        raise ValueError("Empty line")

    # Try to split out date and time (first two whitespace-separated tokens)
    parts = line.strip().split(None, 2)  # maxsplit=2 to keep rest intact
    if len(parts) < 3:
        raise ValueError(f"Invalid log line (no date/time/rest): {line}")

    date, time, rest = parts  # rest contains level+message (maybe glued)
    # Find the logging level anywhere in rest (case-insensitive).
    m = LEVELS_RE.search(rest)
    if not m:
        raise ValueError(f"Log level not found in line: {line}")

    level = m.group(1).upper()
    # message is whatever follows the matched level
    message = rest[m.end():].lstrip(" :.-")  # strip common leading separators/spaces

    return {"date": date, "time": time, "level": level, "message": message}

def load_logs(file_path: str) -> list:
    """Load the log file and return a list of parsed log entries."""
    logs = []
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue  # skip empty lines
                try:
                    logs.append(parse_log_line(line))
                except ValueError as e:
                    print(f"⚠ Warning: {e}")  # incorrect format
                    continue
    except FileNotFoundError:
        print(f"❌ File '{file_path}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"❌ Permission denied for file '{file_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

    return logs

def filter_logs_by_level(logs: list, level: str) -> list:
    level = level.upper()
    return [log for log in logs if log["level"] == level]

def count_logs_by_level(logs: list) -> dict:
    counts = {}
    for log in logs:
        lvl = log["level"]
        counts[lvl] = counts.get(lvl, 0) + 1
    return counts

def display_log_counts(counts: dict):
    print("Logging Level     | Count")
    print("------------------|-------")

    for level in ["INFO", "DEBUG", "ERROR", "WARNING"]:
        print(f"{level:<17} | {counts.get(level, 0)}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python task_3.py path/to/logfile.log [level]")
        sys.exit(1)

    file_path = sys.argv[1]
    level_arg = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level_arg:
        level = level_arg.upper()
        print(f"\nLog details for level '{level}':")

        filtered = filter_logs_by_level(logs, level)
        if not filtered:
            print("No log entries for this level.")
            return

        for log in filtered:
            print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()
