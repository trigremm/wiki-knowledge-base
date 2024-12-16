# bonus.d/utils.d/add_file_path_comment.py
# https://github.com/trigremm/wiki_best_practices/blob/main/bonus.d/utils.d/add_file_path_comment.py
import argparse
import os

default_ignore_files = [
    "manage.py",
]
default_ignore_dirs = [
    "migrations",
    "node_modules",
    "dist",
    "build",
    ".docker_volumes",
    ".git",
    ".venv",
]

process_extensions = [
    ".py",
    ".html",
    ".js",
    ".ts",
    ".vue",
    ".yaml",
    ".yml",
    ".hurl",
]


def get_comment_syntax(file_name, file_extension):
    if file_name in ["Dockerfile", "Makefile"] or file_extension in [
        ".py",
        ".yaml",
        ".yml",
        ".hurl",
    ]:
        return "#"
    elif file_extension in [".js", ".ts"]:
        return "//"
    elif file_extension in [".html", ".vue"]:
        return ("<!--", "-->")
    else:
        return None


def add_file_path_comment(root_dir: str, ignore_files: list, ignore_dirs: list) -> None:
    for root, _, files in os.walk(root_dir):
        if any(ignored_dir in root.split(os.sep) for ignored_dir in ignore_dirs):
            continue

        for file in files:
            file_name, file_extension = os.path.splitext(file)
            file_extension = file_extension.lower()

            if file_extension in process_extensions or file in [
                "Dockerfile",
                "Makefile",
            ]:
                if file in ignore_files:
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, root_dir)
                comment_syntax = get_comment_syntax(file, file_extension)

                if not comment_syntax:
                    print(f"Skipping file '{file}' due to unknown comment syntax")
                    continue

                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # Skip empty files
                if not lines or all(line.strip() == "" for line in lines):
                    continue

                # Remove existing file path comments
                while lines and (
                    (
                        isinstance(comment_syntax, tuple)
                        and lines[0].strip().startswith(comment_syntax[0])
                        and lines[0].strip().endswith(comment_syntax[1])
                    )
                    or (
                        not isinstance(comment_syntax, tuple)
                        and lines[0].strip().startswith(comment_syntax)
                        and (
                            (file in ["Dockerfile", "Makefile"] and lines[0].strip().endswith(file))
                            or any(lines[0].strip().endswith(ext) for ext in process_extensions)
                        )
                    )
                ):
                    lines.pop(0)

                # Remove empty lines at the start
                while lines and lines[0].strip() == "":
                    lines.pop(0)

                # Prepare the new comment
                if isinstance(comment_syntax, tuple):
                    new_comment = f"{comment_syntax[0]} {relative_path} {comment_syntax[1]}\n"
                else:
                    new_comment = f"{comment_syntax} {relative_path}\n"

                # Add the new comment if it's not already there
                if not lines or lines[0].strip() != new_comment.strip():
                    lines.insert(0, new_comment)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add file path comments to project files.")
    parser.add_argument(
        "project_directory",
        nargs="?",
        default=".",
        help="The root directory of the project",
    )
    parser.add_argument(
        "--ignore-files",
        nargs="*",
        default=default_ignore_files,
        help="List of files to ignore",
    )
    parser.add_argument(
        "--ignore-dirs",
        nargs="*",
        default=default_ignore_dirs,
        help="List of directories to ignore",
    )

    args = parser.parse_args()

    add_file_path_comment(args.project_directory, args.ignore_files, args.ignore_dirs)
