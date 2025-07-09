#!/usr/bin/env python3                                                                                          ─╯
import re
import requests
import argparse

regex = r'(?<=(\"|\'|\`))\/[a-zA-Z0-9_?&=\/\-\#\.]*(?=(\"|\'|\`))'

def process_url(url):
    results = set()
    try:
        response = requests.get(url)
        matches = re.finditer(regex, response.text)
        for match in matches:
            results.add(match.group(0))
    except requests.exceptions.RequestException as e:
        pass
    return results

def main():
    parser = argparse.ArgumentParser(description="Extract Endpoints for JS-files bookmarklet-cli version.")
    parser.add_argument("-f", "--file", required=True, help="File containing list of JS-URLs/URLs")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as file:
            urls = file.read().splitlines()
            for url in urls:
                extracted_urls = process_url(url)
                for extracted_url in extracted_urls:
                    print(extracted_url)
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")

if __name__ == "__main__":
    main()
