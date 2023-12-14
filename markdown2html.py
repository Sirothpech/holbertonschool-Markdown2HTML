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

def convert_line(line):
    """
    Convert Markdown line to HTML.
    """
    # Check for heading
    if line.lstrip().startswith('#'):
        count = line.lstrip().count('#')
        # Close list if inside one
        if convert_line.in_list:
            convert_line.in_list = False
            return "\n</{0}>\n<h{1}>{2}</h{1}>\n".format(convert_line.list_type, count, line.replace('#' * count, '').strip())
        return "<h{0}>{1}</h{0}>\n".format(count, line.replace('#' * count, '').strip())
    # Check for list item
    elif line.lstrip().startswith('- ') or line.lstrip().startswith('* '):
        convert_line.list_type = "ul" if line.lstrip().startswith('- ') else "ol"
        if not convert_line.in_list:
            convert_line.in_list = True
            return "<{0}>\n    <li>{1}</li>".format(convert_line.list_type, line[2:].strip())
        return "\n    <li>{}</li>".format(line[2:].strip())
    # Check if inside a list
    elif line.strip() == '' and convert_line.in_list:
        convert_line.in_list = False
        return "\n</{0}>\n".format(convert_line.list_type)
    # Default: treat as a paragraph
    return "{}\n".format(line.strip())

# Initialize the in_list and list_type attributes
convert_line.in_list = False
convert_line.list_type = None

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
            # Convert line
            line = convert_line(line)
            # Écrit la ligne convertie dans le fichier HTML
            html.write(line)

        # Ferme la balise ul/ol à la fin du fichier s'il y en a une ouverte
        if convert_line.in_list:
            html.write("\n</{0}>\n".format(convert_line.list_type))

    # Termine le script avec le code de sortie 0
    sys.exit(0)
