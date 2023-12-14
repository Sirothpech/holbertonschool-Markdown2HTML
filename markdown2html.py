#!/usr/bin/env python3
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
  - Improve the script by parsing Headings Markdown syntax for generating HTML.
    Syntax: (you can assume it will be strictly this syntax)
    Markdown     HTML generated
    # Title       <h1>Title</h1>
    ## Title      <h2>Title</h2>
    ### Title     <h3>Title</h3>
    #### Title    <h4>Title</h4>
    ##### Title   <h5>Title</h5>
    ###### Title  <h6>Title</h6>
"""

import sys
import os

def convert_headings(line):
    """
    Convert Markdown headings to HTML headings.
    """
    count = line.count('#')
    if count > 0:
        line = line.replace('#' * count, '').strip()
        return f"<h{count}>{line}</h{count}>\n"
    return line

if __name__ == "__main__":
    # Vérifie si le nombre d'arguments est correct
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Vérifie si le fichier Markdown existe
    if not os.path.exists(markdown_file):
        sys.stderr.write(f"Missing {markdown_file}\n")
        sys.exit(1)

    # Ouvre le fichier Markdown et lit toutes les lignes
    with open(markdown_file, 'r') as md, open(html_file, 'w') as html:
        # Parcourt chaque ligne du fichier Markdown
        for line in md:
            # Convert headings
            line = convert_headings(line)
            # Additional code for other conversions

            # Écrit la ligne convertie dans le fichier HTML
            html.write(line)

    # Termine le script avec le code de sortie 0
    sys.exit(0)
