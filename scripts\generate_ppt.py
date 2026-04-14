import os
import sys
import time

import requests
import json
import argparse

API_BASE = "https://api.heybossai.com/v1"


def ppt_generate(api_key: str, query: str, num_cards: int = 8, export_as: str = "pdf", web_content: str = None):
    """Generate PPT using gamma/generation model"""
    headers = {
        "Authorization": "Bearer %s" % api_key,
        "Content-Type": "application/json",
    }
    inputs = {
        "inputText": query,
        "format": "presentation",
        "numCards": num_cards,
        "exportAs": export_as,
    }
    if web_content:
        inputs["inputText"] = web_content + "\n\n" + query
    params = {
        "type": "ppt",
        "inputs": inputs,
    }
    response = requests.post(f"{API_BASE}/pilot", headers=headers, json=params)
    result = response.json()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PPT")
    parser.add_argument("--query", "-q", type=str, required=True, help="PPT topic")
    parser.add_argument("--num_cards", "-n", type=int, default=8, help="Number of slides (default: 8)")
    parser.add_argument("--export_as", "-e", type=str, default="pdf", choices=["pdf", "pptx"], help="Export format")
    parser.add_argument("--web_content", "-wc", type=str, default=None, help="Web content")
    args = parser.parse_args()

    api_key = os.getenv("SKILLBOSS_API_KEY")
    if not api_key:
        print("Error: SKILLBOSS_API_KEY must be set in environment.")
        sys.exit(1)

    try:
        start_time = int(time.time())
        result = ppt_generate(api_key, args.query, args.num_cards, args.export_as, args.web_content)
        end_time = int(time.time())

        inner = result.get("result", {})
        if inner.get("status") == "completed":
            print(json.dumps({
                "status": inner["status"],
                "gammaUrl": inner.get("gammaUrl"),
                "exportUrl": inner.get("exportUrl"),
                "generationId": inner.get("generationId"),
                "run_time": end_time - start_time,
                "is_end": True,
            }, ensure_ascii=False, indent=2))
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
