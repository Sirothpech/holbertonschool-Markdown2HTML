# Markdown to HTML

## Tasks

### 0. Start a script

Write a script `markdown2html.py` that takes 2 string arguments:

1. The name of the Markdown file.
2. The output file name.

**Requirements:**

- If the number of arguments is less than 2: print in STDERR `Usage: ./markdown2html.py README.md README.html` and exit 1.
- If the Markdown file doesn’t exist: print in STDERR `Missing <filename>` and exit 1.
- Otherwise, print nothing and exit 0.

```bash
guillaume@vagrant:~/$ ./markdown2html.py
Usage: ./markdown2html.py README.md README.html
guillaume@vagrant:~/$ echo $?
1
guillaume@vagrant:~/$ ./markdown2html.py README.md README.html 
Missing README.md
guillaume@vagrant:~/$ echo $?
1
guillaume@vagrant:~/$ echo "Test" > README.md
guillaume@vagrant:~/$ ./markdown2html.py README.md README.html 
guillaume@vagrant:~/$ 
```

### 1. Headings

Improve `markdown2html.py` by parsing Headings Markdown syntax for generating HTML:

**Syntax:**
- Markdown:

  ```markdown
  # Heading level 1
  ## Heading level 2
  ### Heading level 3
  #### Heading level 4
  ##### Heading level 5
  ###### Heading level 6
  ```

- HTML generated:

  ```html
  <h1>Heading level 1</h1>
  <h2>Heading level 1</h2>
  <h3>Heading level 1</h3>
  <h4>Heading level 1</h4>
  <h5>Heading level 1</h5>
  <h6>Heading level 1</h6>
  ```

```bash
guillaume@vagrant:~/$ cat README.md
# My title
## My title2
# My title3
#### My title4
### My title5

guillaume@vagrant:~/$ ./markdown2html.py README.md README.html 
guillaume@vagrant:~/$ cat README.html 
<h1>My title</h1>
<h2>My title2</h2>
<h1>My title3</h1>
<h4>My title4</h4>
<h3>My title5</h3>
```

### 2. Unordered listing

Improve `markdown2html.py` by parsing Unordered listing syntax for generating HTML:

**Syntax:**
- Markdown:

  ```markdown
  - Hello
  - Bye
  ```

- HTML generated:

  ```html
  <ul>
      <li>Hello</li>
      <li>Bye</li>
  </ul>
  ```

```bash
guillaume@vagrant:~/$ cat README.md
# My title
- Hello
- Bye

guillaume@vagrant:~/$ ./markdown2html.py README.md README.html 
guillaume@vagrant:~/$ cat README.html 
<h1>My title</h1>
<ul>
<li>Hello</li>
<li>Bye</li>
</ul>
```

### 3. Ordered listing

Improve `markdown2html.py` by parsing Ordered listing syntax for generating HTML:

**Syntax:**
- Markdown:

  ```markdown
  * Hello
  * Bye
  ```

- HTML generated:

  ```html
  <ol>
      <li>Hello</li>
      <li>Bye</li>
  </ol>
  ```

```bash
guillaume@vagrant:~/$ cat README.md
# My title
* Hello
* Bye

guillaume@vagrant:~/$ ./markdown2html.py README.md README.html 
guillaume@vagrant:~/$ cat README.html 
<h1>My title</h1>
<ol>
<li>Hello</li>
<li>Bye</li>
</ol>
```

### 4. Simple text

Improve `markdown2html.py` by parsing paragraph syntax for generating HTML:

**Syntax:**
- Markdown:

  ```markdown
  Hello

  I'm a text
  with 2 lines
  ```

- HTML generated:

  ```html
  <p>
      Hello
  </p>
  <p>
      I'm a text
          <br />
      with 2 lines
  </p>
  ```

```bash
guillaume@vagrant:~/$ cat README.md
# My title
- Hello
- Bye

Hello

I'm a text
with 2 lines

guillaume@vagrant:~/$ ./markdown2html.py README.md README.html 
guillaume@vagrant:~/$ cat README.html 
<h1>My title</h1>
<ul>
<li>Hello</li>
<li>Bye</li>
</ul>
<p>
Hello
</p>
<p>
I'm a text
<br/>
with 2 lines
</p>
```

### 5. Bold and emphasis text

Improve `markdown2html.py` by parsing bold syntax for generating HTML:

**Syntax:**
- Markdown:

  ```markdown
  **Hello**
  __Hello__
  ```

- HTML generated:

  ```html
  <b>Hello</b>
  <em>Hello</em>
  ```

```bash
guillaume@vagrant:~/$ cat README.md
# My title
- He**l**lo
- Bye

Hello

I'm **a** text
with __2 lines__

**Or in bold**

guillaume@vagrant:~/$ ./markdown2html.py README.md README.html 
guillaume@vagrant:~/$ cat README.html 
<h1>My title</h1>
<ul>
<li>He<b>l</b>lo</li>
<li>Bye</li>
</ul>
<p>
Hello
</p>
<p>
I'm <b>a</b> text
<br/>
with <em>2 lines</em>
</p>
<p>
<b>Or in bold</b>
</p>
```

### 6. ... but why??

Improve `markdown2html.py` by parsing bold syntax for generating HTML:

**Syntax:**
- Markdown:

  ```markdown
  [[Hello]]
  ((Hello Chicago))
  ```

- HTML generated:

  ```html
  8b1a9953c4611296a827abf8c47804d7
  Hello hiago
  ```

```bash
guillaume@vagrant:~/$ cat README.md
# My title
- He**l**lo
- Bye

Hello

I'm **a** text
with __2 lines__

((I will live in Caracas))

But it's [[private]]

So cool!

guillaume@vagrant:~/$ ./markdown2html.py README.md README.html 
guillaume@vagrant:~/$ cat README.html 
<h1>My title</h1>
<ul>
<li>He<b>l</b>lo</li>
<li>Bye</li>
</ul>
<p>
Hello
</p>
<p>
I'm <b>a</b

> text
<br/>
with <em>2 lines</em>
</p>
<p>
I will live in araas
</p>
<p>
But it's 2c17c6393771ee3048ae34d6b380c5ec
</p>
<p>
So cool!
</p>
```