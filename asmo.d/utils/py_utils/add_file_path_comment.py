# asmo.d/utils/py_utils/add_file_path_comment.py
"""
Add file path comments to files with best features from both versions.
Combines flexibility of stdin/files with smart directory processing.
"""

import argparse
import os
import sys
from typing import List
from typing import Tuple
from typing import Union

# Configuration
SUPPORTED_EXTENSIONS = [".py", ".yaml", ".yml", ".js", ".ts", ".html", ".vue", ".mk", ".hurl"]
SUPPORTED_FILENAMES = ["Dockerfile", "Makefile"]
DEFAULT_IGNORE_DIRS = [
    "migrations",
    "node_modules",
    "dist",
    "build",
    ".docker_volumes",
    "docker_volumes",
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    "venv",
    "env",
]


def get_comment_syntax(file_name: str, file_ext: str) -> Union[str, Tuple[str, str], None]:
    """Get appropriate comment syntax for file."""
    # Hash style: # comment
    if file_name in SUPPORTED_FILENAMES or file_ext in [".py", ".yaml", ".yml", ".mk", ".hurl"]:
        return "#"

    # Slash style: // comment
    elif file_ext in [".js", ".ts"]:
        return "//"

    # HTML style: <!-- comment -->
    elif file_ext in [".html", ".vue"]:
        return ("<!--", "-->")

    return None


def should_process_file(file_name: str, file_ext: str) -> bool:
    """Check if file should be processed."""
    return file_name in SUPPORTED_FILENAMES or file_ext in SUPPORTED_EXTENSIONS


def is_file_path_comment(line: str, comment_syntax: Union[str, Tuple[str, str]]) -> bool:
    """
    Advanced check if line is a file path comment.
    Combines logic from both scripts for better accuracy.
    """
    line = line.strip()
    if not line:
        return False

    if isinstance(comment_syntax, tuple):
        # HTML-style comments: <!-- path -->
        if line.startswith(comment_syntax[0]) and line.endswith(comment_syntax[1]):
            content = line[len(comment_syntax[0]) : -len(comment_syntax[1])].strip()
            return _looks_like_file_path(content)
    else:
        # Regular comments: # path or // path
        if line.startswith(comment_syntax):
            content = line[len(comment_syntax) :].strip()
            return _looks_like_file_path(content)

    return False


def _looks_like_file_path(content: str) -> bool:
    """
    Enhanced file path detection combining both approaches.
    """
    if not content or len(content) > 200:
        return False

    # Check for invalid path characters
    invalid_chars = ["<", ">", "|", '"', "*", "?"]
    if any(char in content for char in invalid_chars):
        return False

    # Get filename (last part of path)
    file_name = content.split("/")[-1].split("\\")[-1]

    # Known files without extension
    if file_name in SUPPORTED_FILENAMES:
        return True

    # Files with supported extensions
    if "." in content:
        ext = os.path.splitext(content)[1].lower()
        if ext in SUPPORTED_EXTENSIONS:
            return True

    return False


def process_single_file(file_path: str, root_dir: str) -> str:
    """
    Process single file with enhanced error handling and logic.
    Returns: 'updated', 'unchanged', 'skipped', or 'error'
    """
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1].lower()

    # Check if file should be processed
    if not should_process_file(file_name, file_ext):
        return "skipped"

    # Get comment syntax
    comment_syntax = get_comment_syntax(file_name, file_ext)
    if not comment_syntax:
        return "skipped"

    # Get relative path
    try:
        rel_path = os.path.relpath(file_path, root_dir)
    except ValueError:
        rel_path = file_path

    try:
        # Read file
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Skip empty files
        if not lines or all(line.strip() == "" for line in lines):
            return "skipped"

        # Remove existing file path comments (enhanced removal)
        len(lines)
        removed_count = 0

        # Remove multiple existing comments if present
        while lines and removed_count < 3 and is_file_path_comment(lines[0], comment_syntax):  # Safety limit
            lines.pop(0)
            removed_count += 1

        # Remove leading empty lines
        while lines and lines[0].strip() == "":
            lines.pop(0)

        # Create new comment
        if isinstance(comment_syntax, tuple):
            new_comment = f"{comment_syntax[0]} {rel_path} {comment_syntax[1]}\n"
        else:
            new_comment = f"{comment_syntax} {rel_path}\n"

        # Check if update is needed
        if not lines or lines[0].strip() != new_comment.strip():
            lines.insert(0, new_comment)

            # Write back to file
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)

            return "updated"
        else:
            return "unchanged"

    except Exception as e:
        print(f"Error processing '{file_path}': {e}", file=sys.stderr)
        return "error"


def collect_files_from_directory(root_dir: str, ignore_dirs: List[str]) -> List[str]:
    """Collect all processable files from directory."""
    files = []

    for root, dirs, filenames in os.walk(root_dir):
        # Remove ignored directories from search
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        # Skip if current directory is in ignore list
        if any(ignored in root.split(os.sep) for ignored in ignore_dirs):
            continue

        for filename in filenames:
            file_path = os.path.join(root, filename)
            file_ext = os.path.splitext(filename)[1].lower()

            if should_process_file(filename, file_ext):
                files.append(file_path)

    return files


def process_files(file_list: List[str], root_dir: str, verbose: bool = False) -> None:
    """Process list of files with detailed reporting."""
    if not file_list:
        print("No files to process.")
        return

    print(f"Processing {len(file_list)} files...")

    # Counters for summary
    stats = {"updated": 0, "unchanged": 0, "skipped": 0, "error": 0}

    for file_path in file_list:
        # Convert to absolute path
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(os.path.join(root_dir, file_path))

        # Check if file exists
        if not os.path.exists(file_path):
            if verbose:
                print(f"File not found: {file_path}")
            stats["error"] += 1
            continue

        # Process file
        result = process_single_file(file_path, root_dir)
        stats[result] += 1

        if verbose or result == "updated":
            rel_path = os.path.relpath(file_path, root_dir)
            if result == "updated":
                print(f"✅ Updated: {rel_path}")
            elif result == "error":
                print(f"❌ Error: {rel_path}")
            elif verbose and result == "skipped":
                print(f"⏭️  Skipped: {rel_path}")

    # Print summary
    total = sum(stats.values())
    print(f"\n📊 Summary:")
    print(f"   Updated: {stats['updated']}")
    print(f"   Unchanged: {stats['unchanged']}")
    print(f"   Skipped: {stats['skipped']}")
    print(f"   Errors: {stats['error']}")
    print(f"   Total: {total}")


def main():
    parser = argparse.ArgumentParser(
        description="Add file path comments to source files",
        epilog="""Examples:
  # Process specific files
  %(prog)s -f file1.py file2.js

  # Process entire directory
  %(prog)s -d ./src

  # Use with git (modified files)
  git ls-files --modified | %(prog)s --stdin

  # Use with find
  find . -name "*.py" | %(prog)s --stdin

  # Combine stdin and files
  echo "extra.py" | %(prog)s --stdin -f main.py
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Input options (can be combined)
    parser.add_argument("-f", "--files", nargs="*", default=[], help="Specific files to process")
    parser.add_argument("--stdin", action="store_true", help="Read additional files from stdin")
    parser.add_argument("-d", "--directory", help="Process all supported files in directory recursively")

    # Configuration options
    parser.add_argument("--root", default=".", help="Root directory for relative paths (default: current dir)")
    parser.add_argument(
        "--ignore-dirs", nargs="*", default=DEFAULT_IGNORE_DIRS, help="Directories to ignore when using --directory"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Collect all files to process
    all_files = []

    # Add files from --files
    if args.files:
        all_files.extend(args.files)

    # Add files from stdin
    if args.stdin:
        stdin_files = [line.strip() for line in sys.stdin if line.strip()]
        all_files.extend(stdin_files)

    # Add files from directory
    if args.directory:
        if not os.path.isdir(args.directory):
            print(f"Error: Directory '{args.directory}' does not exist", file=sys.stderr)
            sys.exit(1)

        dir_files = collect_files_from_directory(args.directory, args.ignore_dirs)
        all_files.extend(dir_files)

    # Validate input
    if not all_files:
        print("Error: No files to process.", file=sys.stderr)
        print("Use -f, --stdin, or -d to specify files.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Remove duplicates while preserving order
    seen = set()
    unique_files = []
    for f in all_files:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)

    # Process files
    process_files(unique_files, args.root, args.verbose)


if __name__ == "__main__":
    main()
