from parser_utils import extract_text
import os

uploads_dir = "uploads"
for f in os.listdir(uploads_dir):
    path = os.path.join(uploads_dir, f)
    if os.path.isfile(path):
        try:
            txt = extract_text(path)
            print(f"File: {f} | Extracted length: {len(txt)}")
            if len(txt) > 0:
                print(f"First 100 chars: {txt[:100]}")
        except Exception as e:
            print(f"File: {f} | Error: {e}")
