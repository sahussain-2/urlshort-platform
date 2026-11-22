import json
import os
import sys
import urllib.error
import urllib.request

HEALTH_URL = os.getenv("HEALTH_URL", "http://127.0.0.1:8000/health")


def main() -> int:
    try:
        with urllib.request.urlopen(HEALTH_URL, timeout=5) as response:
            body = json.load(response)
            if response.status == 200 and body.get("status") == "ok":
                print(f"OK {HEALTH_URL}")
                return 0
            print(f"FAIL {HEALTH_URL} status={response.status} body={body}")
            return 1
    except (urllib.error.URLError, TimeoutError, ValueError) as error:
        print(f"FAIL {HEALTH_URL} error={error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
