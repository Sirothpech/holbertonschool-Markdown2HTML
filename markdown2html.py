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
import re

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
            return "\n</{0}>\n<h{1}>{2}</h{1}>\n".format(convert_line.list_type, count, process_inline_formatting(line.replace('#' * count, '').strip()))
        return "<h{0}>{1}</h{0}>\n".format(count, process_inline_formatting(line.replace('#' * count, '').strip()))
    # Check for list item
    elif line.lstrip().startswith('- ') or line.lstrip().startswith('* '):
        convert_line.list_type = "ul" if line.lstrip().startswith('- ') else "ol"
        if not convert_line.in_list:
            convert_line.in_list = True
            return "<{0}>\n    <li>{1}</li>".format(convert_line.list_type, process_inline_formatting(line[2:].strip()))
        return "\n    <li>{}</li>".format(process_inline_formatting(line[2:].strip()))
    # Check if inside a list
    elif line.strip() == '' and convert_line.in_list:
        convert_line.in_list = False
        return "\n</{0}>\n".format(convert_line.list_type)
    # Check for paragraph
    elif line.strip() != '' and not convert_line.in_paragraph:
        convert_line.in_paragraph = True
        return "<p>\n{}".format(process_inline_formatting(line.strip()))
    elif line.strip() == '' and convert_line.in_paragraph:
        convert_line.in_paragraph = False
        return "\n</p>\n"
    elif line.strip() != '' and convert_line.in_paragraph:
        return "\n<br/>\n{}".format(process_inline_formatting(line.strip()))
    # Default: treat as a paragraph
    return "{}\n".format(process_inline_formatting(line.strip()))

def process_inline_formatting(text):
    """
    Process inline formatting (bold, italic, underline) in the given text.
    """
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    return text

# Initialize the in_list, list_type, and in_paragraph attributes
convert_line.in_list = False
convert_line.list_type = None
convert_line.in_paragraph = False

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
        # Ferme le paragraphe à la fin du fichier s'il y en a un ouvert
        if convert_line.in_paragraph:
            html.write("\n</p>\n")

    # Termine le script avec le code de sortie 0
    sys.exit(0)

