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
import hashlib

def md5_hash(content):
    """
    Convert the content to MD5 hash (lowercase).
    """
    md5 = hashlib.md5()
    md5.update(content.encode('utf-8'))
    return md5.hexdigest()

def remove_character(content, char):
    """
    Remove all occurrences of the specified character (case insensitive).
    """
    return content.replace(char.lower(), '').replace(char.upper(), '')

def convert_line(line):
    """
    Convert Markdown line to HTML.
    """
    # Check for ((...))
    if '((' in line:
        # Recherche toutes les occurrences du motif '((...))' dans la ligne
        matches = re.findall(r'\(\((.*?)\)\)', line)

        # Si des occurrences sont trouvées
        if matches:
            # Parcourt toutes les occurrences et remplace par la version modifiée
            for match in matches:
                modified_content = remove_character(match, 'c')
                line = line.replace(f"(({match}))", f"{modified_content}")
            
            # Ajoute la balise <p> autour de la ligne modifiée
            line = f"<p>\n{line.strip()}\n</p>\n"
        
        # Renvoie la ligne modifiée
        return line

    # Check for [[...]]
    elif '[[' in line:
        # Recherche toutes les occurrences du motif '[[...]]' dans la ligne
        matches = re.findall(r'\[\[(.*?)\]\]', line)

        # Si des occurrences sont trouvées
        if matches:
            # Parcourt toutes les occurrences et remplace par la version MD5
            for match in matches:
                line = line.replace(f"[[{match}]]", md5_hash(match))

            # Ajoute la balise <p> autour de la ligne modifiée
            line = f"<p>\n{line.strip()}\n</p>\n"

        # Renvoie la ligne modifiée
        return line

    # Check for heading
    elif line.lstrip().startswith('#'):
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
    return ""

def process_inline_formatting(text):
    """
    Process inline formatting (bold, italic) in the given text.
    """
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Underline
    text = re.sub(r'__(.*?)__', r'<em>\1</em>', text)
    return text

if __name__ == "__main__":
    # Initialize the in_list, list_type, and in_paragraph attributes
    convert_line.in_list = False
    convert_line.list_type = None
    convert_line.in_paragraph = False

    # Check command line arguments
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.exists(markdown_file):
        sys.stderr.write(f"Missing {markdown_file}\n")
        sys.exit(1)

    # Open the Markdown file and read all lines
    with open(markdown_file, 'r') as md, open(html_file, 'w') as html:
        # Process each line of the Markdown file
        for line in md:
            # Convert line
            line = convert_line(line)
            # Write the converted line to the HTML file
            html.write(line)

        # Close the ul/ol tag at the end of the file if one is open
        if convert_line.in_list:
            html.write("\n</{0}>\n".format(convert_line.list_type))
        # Close the paragraph at the end of the file if one is open
        if convert_line.in_paragraph:
            html.write("\n</p>\n")

    # Exit the script with exit code 0
    sys.exit(0)
