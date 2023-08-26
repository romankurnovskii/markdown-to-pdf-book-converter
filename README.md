Generate e-books, manuals, handbooks or other comprehensive documents from a collection of Markdown files.

[Example](https://romankurnovskii.com/handbooks/python-handbook.pdf) of result pdf.

## Features:

- Using Pandoc for conversion from Markdown to PDF
- LaTeX templates for beautiful and highly customizable PDF outputs
- Automated chapter/section creation from separate Markdown files
- Supports Docker for cross-platform compatibility
- Easy to integrate into CI/CD pipelines for automated document generation


## Usage

```sh
git clone https://github.com/romankurnovskii/markdown-to-pdf-book-converter.git
cd markdown-to-pdf-book-converter
```

1. Build docker image:

```sh
docker build -t rk-latex-image .
```

2. Set path to book:

```sh
export HOST_TEMPLATE_PATH="$PWD" # path to template.tex
export HOST_BOOK_PATH="./example-book-markdown-folder"
```

3. Update title, author, etc in template `template.tex` if needed


4. Run docker image with mounted path to docker image:

```
docker run -it \
    -v ${HOST_TEMPLATE_PATH}:/opt/template \
    -v ${HOST_BOOK_PATH}:/opt/template/book \
    rk-latex-image
```

5. Create book:

```sh
# use all markdown files. Will create book at the same markdown path 
python3 -m export_book --using-chapter-folders --root-path book

# set output pdf
python3 -m export_book --using-chapter-folders --root-path book --output-file book/my-book.pdf

# create pdf from specific markdown files
python3 -m export_book --using-chapter-folders --root-path . -f ./book/top-questions/_index.ru.md
python3 -m export_book --using-chapter-folders --root-path . -f ./book/file1.md ./book/file2.md

# all markdown files in one folder
python3 -m export_book --root-path book --output-file my-book.pdf

# all markdown files in one folder AND one language (en)
python3 -m export_book --root-path book --language en --output-file book/trading-indicators-handbook.pdf
```

Some other commands for creating .pdf

```sh
pandoc --pdf-engine xelatex \
--listings \
-V title="My Title" -V author="John Smith" -V date="2022-09-22" \
--template=template.tex \
 $(find . -name '*.ru.md') \
-o book.pdf

pandoc --pdf-engine xelatex \
--variable mainfont="M+ 1p" \
--variable sansfont="M+ 1p" \
--variable monofont="M+ 1m" \
-V geometry:"top=1cm, bottom=2cm, left=1cm, right=1cm" \
--file-scope \
--highlight-style=tango \
-s \
--toc-depth=3 \
--variable=toc-title:" " \
--listings \
--standalone \
--self-contained \
--from=markdown \
--template=template.tex \
 $(find . -name '*.ru.md') \
-o book.pdf
```
