#!/usr/bin/env python3
"""ReadRegex.py

Reads a source text file and extracts only text that matches the configured regex.
Writes matched content to /Users/ashishmokashi/Documents/Python/content/output_regex.txt.
"""
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict

try:
    import mysql.connector as mysql_connector
except Exception:
    mysql_connector = None

CONFIG_FILENAME = "config.json"
DEFAULT_INPUT_PATH = Path("/Users/ashishmokashi/Documents/Python/content/Chemistry Questions.txt")
OUTPUT_PATH = Path("/Users/ashishmokashi/Documents/Python/content/output_regex.txt")


def load_config(cfg_path: Path) -> dict:
    if not cfg_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {cfg_path}")
    with cfg_path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def normalize_matches(matches):
    processed = []
    for match in matches:
        if isinstance(match, tuple):
            processed.append("".join(str(item) for item in match))
        else:
            processed.append(str(match))
    return processed


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    config_path = script_dir / CONFIG_FILENAME

    try:
        config = load_config(config_path)
    except Exception as exc:
        print(f"Failed to load configuration: {exc}")
        return 1

    regex_pattern = config.get("regex")
    if not regex_pattern:
        print(f"Missing 'regex' value in {config_path}")
        return 1

    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
    else:
        input_path = DEFAULT_INPUT_PATH

    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        print("Provide a source text file path as the first argument, or create the default source file at:")
        print(f"  {DEFAULT_INPUT_PATH}")
        return 1

    try:
        text = input_path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"Failed to read input file: {exc}")
        return 1

    try:
        compiled = re.compile(regex_pattern, flags=re.MULTILINE | re.DOTALL)
    except re.error as exc:
        print(f"Invalid regex pattern in config: {exc}")
        return 1

    # Use finditer to support named groups
    matches = list(compiled.finditer(text))
    extracted = []
    for m in matches:
        gd: Dict[str, Any] = m.groupdict()
        if gd:
            extracted.append({
                'SubjectName': (gd.get('SubjectName') or '').strip(),
                'ChapterName': (gd.get('ChapterName') or '').strip(),
                'Question': (gd.get('Question') or '').strip(),
                'AnswerOption': (gd.get('AnswerOptions') or '').strip(),
            })
        else:
            groups = m.groups()
            if len(groups) >= 4:
                extracted.append({
                    'SubjectName': (groups[0] or '').strip(),
                    'ChapterName': (groups[1] or '').strip(),
                    'Question': (groups[2] or '').strip(),
                    'AnswerOption': (groups[3] or '').strip(),
                })
            elif len(groups) == 3:
                extracted.append({
                    'SubjectName': (groups[0] or '').strip(),
                    'Question': (groups[1] or '').strip(),
                    'AnswerOption': (groups[2] or '').strip(),
                })
            elif len(groups) == 2:
                extracted.append({
                    'Question': (groups[0] or '').strip(),
                    'AnswerOption': (groups[1] or '').strip(),
                })
            elif len(groups) == 1:
                extracted.append({'Question': (groups[0] or '').strip()})
            else:
                extracted.append({'Question': m.group(0).strip()})

    # write output file (optional) and insert into DB
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        with OUTPUT_PATH.open("w", encoding="utf-8") as out_file:
            if not extracted:
                out_file.write("")
                print(f"No regex matches found. Created empty output file: {OUTPUT_PATH}")
            else:
                for item in extracted:
                    # write a readable line
                    out_file.write(json.dumps(item, ensure_ascii=False) + "\n")
                print(f"Wrote {len(extracted)} extracted items to: {OUTPUT_PATH}")
    except Exception as exc:
        print(f"Failed to write output file: {exc}")
        return 1

    # Database insert
    db_cfg = config.get('db', {})
    db_host = db_cfg.get('host', '127.0.0.1')
    db_user = db_cfg.get('user', 'root')
    db_pass = db_cfg.get('password', '')
    db_name = db_cfg.get('database', None)

    if mysql_connector is None:
        print('MySQL connector not available (mysql-connector-python). Skipping DB inserts.')
        return 0

    if not db_name:
        print('No database name provided in config under "db.database". Skipping DB inserts.')
        return 0

    try:
        conn = mysql_connector.connect(host=db_host, user=db_user, password=db_pass, database=db_name)
    except Exception as exc:
        print(f"Failed to connect to MySQL: {exc}")
        return 1

    try:
        cursor = conn.cursor()
        insert_sql = (
            "INSERT INTO Questions (SubjectName, ChapterName, Question, AnswerOption)"
            " VALUES (%s, %s, %s, %s)"
        )
        inserted = 0
        for item in extracted:
            subj = item.get('SubjectName') or None
            chap = item.get('ChapterName') or None
            ques = item.get('Question') or None
            ans = item.get('AnswerOption') or item.get('AnswerOptions') or None
            try:
                cursor.execute(insert_sql, (subj, chap, ques, ans))
                inserted += 1
            except Exception as e:
                print(f"Failed to insert row: {e} -- data: {item}")
        conn.commit()
        print(f"Inserted {inserted} rows into Questions table.")
    finally:
        try:
            cursor.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
