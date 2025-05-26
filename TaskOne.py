import requests
import json
import sys

# EC2 metadata base URL (IMDSv2)
TOKEN_URL = "http://169.254.169.254/latest/api/token"
METADATA_URL = "http://169.254.169.254/latest/meta-data/"

def get_token():
    """Get the token required for accessing EC2 metadata (IMDSv2)"""
    try:
        response = requests.put(TOKEN_URL, headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"}, timeout=2)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error retrieving token: {e}")
        sys.exit(1)

def get_metadata(token, path=""):
    """Recursively get metadata from EC2 metadata service"""
    url = METADATA_URL + path
    headers = {"X-aws-ec2-metadata-token": token}
    try:
        response = requests.get(url, headers=headers, timeout=2)
        response.raise_for_status()
        if path.endswith("/"):
            # It's a directory: recurse into each item
            result = {}
            for item in response.text.strip().splitlines():
                result[item.strip("/")] = get_metadata(token, path + item)
            return result
        else:
            return response.text
    except Exception as e:
        return f"Error retrieving metadata: {e}"

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Query EC2 instance metadata")
    parser.add_argument("--key", type=str, help="Optional metadata key to retrieve")
    args = parser.parse_args()

    token = get_token()

    if args.key:
        # Retrieve specific key
        metadata = get_metadata(token, args.key.strip("/") + "/")  # add '/' to ensure directory is handled
    else:
        # Retrieve all metadata
        metadata = get_metadata(token)

    print(json.dumps(metadata, indent=4))

if __name__ == "__main__":
    main()
