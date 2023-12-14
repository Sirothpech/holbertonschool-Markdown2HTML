#!/usr/bin/python3
"""
Script that takes 2 string arguments:
  - The name of the Markdown file.
  - The output file name.
Requirements:
  - If the number of arguments is less than 2:
    print in STDERR "Usage: ./markdown2html.py README.md README.html" and exit 1.
  - If the Markdown file doesn’t exist:
    print in STDERR "Missing <filename>" and exit 1.
  - Otherwise, print nothing and exit 0.
"""
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    md_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.isfile(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        sys.exit(1)

    # Process Markdown to HTML here (additional code needed for other tasks)

    sys.exit(0)
