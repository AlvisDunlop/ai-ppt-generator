import os
import sys
import json


def ppt_theme_list(api_key: str):
    # The gamma/generation model does not expose separate theme selection.
    # Return a single default entry so callers receive a valid list.
    return [{"style_name_list": ["默认"], "style_id": 0, "tpl_id": 0}]


if __name__ == "__main__":
    api_key = os.getenv("SKILLBOSS_API_KEY")
    if not api_key:
        print("Error: SKILLBOSS_API_KEY must be set in environment.")
        sys.exit(1)
    try:
        results = ppt_theme_list(api_key)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print(f"error type：{exc_type}")
        print(f"error message：{exc_value}")
        sys.exit(1)
