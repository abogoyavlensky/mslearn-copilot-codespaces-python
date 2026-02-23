import urllib.request
import urllib.error
import sys

BASE_URL = "http://localhost:8000"


def health_check(base_url: str = BASE_URL) -> None:
    url = f"{base_url}/health"
    try:
        with urllib.request.urlopen(url) as response:
            body = response.read().decode()
            print(f"Status: {response.status}")
            print(f"Response: {body}")
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}")
        sys.exit(1)


if __name__ == "__main__":
    base_url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL
    health_check(base_url)
