import argparse
import os
import re
import shutil
import subprocess

from collections import defaultdict


TARGET_FILE_NAME = "result-book.pdf"
HEADERS_PATH = "./headers"  # path where save temporary files with titles


def create_dir_and_save_file(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)


def create_headers(posts, tex_files):
    for i, post in enumerate(posts):
        title = str(post["title"])
        title_data = f"\\section{{{title}}}"

        tex_file = f"{i}.tex"
        tex_file_path = os.path.join(HEADERS_PATH, tex_file)
        tex_files.append(tex_file_path)
        with open(tex_file_path, "w") as f:
            f.write(title_data)


def parse_files(lang_code=""):
    """
    @param lang_code In md can be ru|en etc. i.e. "en" in case file.en.md
    """
    # extract weights from header
    weight_re = re.compile(r"^weight:\s*(\d+)\s*$", re.MULTILINE)
    title_re = re.compile(r"^\s*title\s*:\s*(.*)$", re.MULTILINE)

    # Initialize dictionary to store posts by folder and weight
    posts = defaultdict(lambda: defaultdict(list))

    lang_substr = ""
    if lang_code:
        lang_substr = f".{lang_code}"

    # Loop through all folders and files
    for root, dirs, files in os.walk("."):
        # Skip hidden folders
        if os.path.basename(root).startswith("."):
            continue

        # Check for root _index.{lang_code}.md file
        if os.path.basename(root) == ".":
            root_file = os.path.join(root, f"_index{lang_substr}.md")
            if os.path.isfile(root_file):
                with open(root_file, "r") as f:
                    contents = f.read()
                match = weight_re.search(contents)
                if match is None:
                    weight = 0
                else:
                    weight = int(match.group(1))
                match = title_re.search(contents)
                if match is None:
                    title = "NO TITLE"
                else:
                    title = match.group(1)
                posts[os.path.basename(root)][weight].append(
                    {"path": root_file, "weight": weight, "title": title}
                )

        for file in files:
            # Skip files that don't end in ".{lang_code}.md"
            if not file.endswith(f"{lang_substr}.md"):
                continue

            path = os.path.join(root, file)

            # Read file contents
            with open(path, "r") as f:
                contents = f.read()

            # Extract weight from header
            match = weight_re.search(contents)
            if match is None:
                weight = 0
            else:
                weight = int(match.group(1))

            match = title_re.search(contents)
            if match is None:
                title = "NO TITLE"
            else:
                title = match.group(1)

            # Add post to dictionary
            folder = os.path.basename(root)
            posts[folder][weight].append(
                {"path": path, "weight": weight, "title": title}
            )

    # Sort posts by folder and weight
    sorted_posts = []
    sorted_posts_paths = []
    for folder, weights in sorted(posts.items(), key=lambda x: min(x[1])):
        for weight in sorted(weights):
            sorted_posts.extend(posts[folder][weight])
            post_path = posts[folder][weight][0]["path"]
            sorted_posts_paths.append(post_path)

    return sorted_posts, sorted_posts_paths


# return output from bash pipe cmd as decoded string
def run_cmd(cmd):
    bash_cmd = cmd
    process = subprocess.Popen(bash_cmd.split(), stdout=subprocess.PIPE)
    output = process.stdout.read()
    return output.decode("utf-8")


def sort_list(a_list):
    list_with_indices = []
    for item in a_list:
        index = re.sub("[^0-9]", "", item)
        list_with_indices.append([item, index])
    list_with_indices.sort(key=lambda x: x[1])  # sort by index

    sorted_list = []
    for item in list_with_indices:
        sorted_list.append(item[0])
    return sorted_list


# get chapters first if they exist as directories
# then Scenes, or just Chapters if they are md files.
def get_list_of_files(md_book_path, extension, chapter_folders=False, md_file_path=""):
    sorted_markdown_list = []

    if md_file_path:
        if md_file_path.endswith("." + extension):
            md_file_path = os.path.join(md_book_path, md_file_path)
            sorted_markdown_list.append(md_file_path)
            return sorted_markdown_list
    if chapter_folders:
        chapters_list = [
            item
            for item in os.listdir(md_book_path)
            if os.path.isdir(os.path.join(md_book_path, item))
        ]
        chapters_list = sort_list(chapters_list)

        for chapter in chapters_list:
            chapter_markdown_files = []
            all_files = os.listdir(md_book_path + "/" + chapter)
            for a_file in all_files:
                if a_file.endswith("." + extension):
                    # path + "/" + chapter + "/" +
                    chapter_markdown_files.append(a_file)
            chapter_markdown_files = sort_list(chapter_markdown_files)
            for index in range(len(chapter_markdown_files)):
                current_path = chapter_markdown_files[index]
                chapter_markdown_files[index] = (
                    md_book_path + "/" + chapter + "/" + current_path
                )
            sorted_markdown_list.extend(chapter_markdown_files)
    else:
        # process only MD files make sure they are numbered
        all_files = os.listdir(md_book_path)
        for a_file in all_files:
            if a_file.endswith("." + extension):
                sorted_markdown_list.append(a_file)

        sorted_markdown_list = sort_list(sorted_markdown_list)
        for index in range(len(sorted_markdown_list)):
            current_path = sorted_markdown_list[index]
            sorted_markdown_list[index] = md_book_path + "/" + current_path

    return sorted_markdown_list


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--root-path", help="Root path for book files", required=True
    )
    parser.add_argument(
        "-c",
        "--using-chapter-folders",
        help="Are you using folders for chapters?",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--file-type",
        default="md",
        help="File extension. Default: md",
    )
    parser.add_argument(
        "-l",
        "--language",
        default="",
        help="Use language code if exists in md file name. (In case only use this language.) i.e. file: file.en.md -> --language en",
    )
    parser.add_argument(
        "-f",
        "--file-path",
        help="Are you using folders for chapters?",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help="Path to result pdf. i.e. my-book.pdf",
    )

    # TODO
    parser.add_argument("-b", "--book-title")
    parser.add_argument("-d", "--book-description")

    args = parser.parse_args()
    print("ARGS:", args)

    if args.book_title:
        book_title = args.book_title
    if args.book_description:
        book_description = args.book_description

    file_list = get_list_of_files(
        args.root_path, args.file_type, args.using_chapter_folders, args.file_path
    )

    sorted_posts, sorted_posts_paths = parse_files()
    file_list = sorted_posts_paths

    if not file_list:
        print(
            "No markdown files found, if you're using folder chapters use -c, else do not use -c"
        )
        exit()

    # add title headers for each file
    tex_files = []

    create_dir_and_save_file(HEADERS_PATH)
    create_headers(sorted_posts, tex_files)

    file_list_with_breaks = []
    for i, file in enumerate(file_list):
        file_list_with_breaks.append(tex_files[i])
        file_list_with_breaks.append(file)
    file_list_with_breaks.pop(0)

    if args.root_path[-1] != "/" or args.root_path[-1] != "\\":
        args.root_path = args.root_path + "/"

    if args.output_file:
        output_file = args.output_file
    else:
        output_file = f"{args.root_path}/{TARGET_FILE_NAME}"

    default_pandoc_cmd = f"""pandoc --pdf-engine=xelatex
        --verbose
        --standalone
        --listings
        --template=template.tex
        --toc --toc-depth=6
        --file-scope
        -o {output_file} """

    files_string = " ".join(file_list_with_breaks)

    cmd_command = default_pandoc_cmd + files_string
    print("Executing: " + cmd_command)
    run_cmd(cmd_command)
    create_dir_and_save_file(HEADERS_PATH)


if __name__ == "__main__":
    main()
