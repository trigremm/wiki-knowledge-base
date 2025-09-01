# asmo.d/utils/py_utils/add_file_path_comment.py
"""
Add a file-path comment as the first line of supported source files.

Key features:
- Works with stdin, explicit file list, or entire directory tree.
- Uses absolute paths internally to avoid "root_dir/root_dir/..." duplication.
- If --directory is set and --root is not, root defaults to directory.
- Removes existing path comment(s) on top (up to --max-remove), then inserts a fresh one.
- Preserves original newline style (LF/CRLF).
- Supports dry-run mode and verbose logging.
"""

import argparse
import os
import sys
from typing import Dict
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Union

# ---------------------------
# Configuration
# ---------------------------
SUPPORTED_EXTENSIONS = [".py", ".yaml", ".yml", ".js", ".ts", ".html", ".vue", ".mk", ".hurl"]
SUPPORTED_FILENAMES = ["Dockerfile", "Makefile"]
DEFAULT_IGNORE_DIRS = {
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
}

# Safety limit on how many initial lines we will scan/remove as "existing path comment"
DEFAULT_MAX_REMOVE = 3


# ---------------------------
# Helpers: Path & comment detection
# ---------------------------
def get_comment_syntax(file_name: str, file_ext: str) -> Union[str, Tuple[str, str], None]:
    """Return appropriate comment token or (open, close) for HTML/Vue."""
    if file_name in SUPPORTED_FILENAMES or file_ext in [".py", ".yaml", ".yml", ".mk", ".hurl"]:
        return "#"
    if file_ext in [".js", ".ts"]:
        return "//"
    if file_ext in [".html", ".vue"]:
        return ("<!--", "-->")
    return None


def should_process_file(file_name: str, file_ext: str) -> bool:
    """Check if file should be processed at all."""
    return (file_name in SUPPORTED_FILENAMES) or (file_ext in SUPPORTED_EXTENSIONS)


def _looks_like_file_path(content: str) -> bool:
    """Heuristic check if content is a plausible file path we generate."""
    if not content or len(content) > 300:
        return False

    # Disallow some characters that do not belong to normal paths
    for ch in ["<", ">", "|", '"', "*", "?"]:
        if ch in content:
            return False

    # Normalize separators for inspection
    last = content.replace("\\", "/").split("/")[-1]

    # exactly our known filenames without extension
    if last in SUPPORTED_FILENAMES:
        return True

    # Or a supported extension anywhere
    root, ext = os.path.splitext(last)
    if ext.lower() in SUPPORTED_EXTENSIONS:
        return True

    # In practice we only mark generated comments, so be conservative
    return False


def is_file_path_comment(line: str, comment_syntax: Union[str, Tuple[str, str]]) -> bool:
    """Check whether a given trimmed line equals the "header path comment" shape."""
    s = line.strip()
    if not s:
        return False

    if isinstance(comment_syntax, tuple):
        open_tok, close_tok = comment_syntax
        if s.startswith(open_tok) and s.endswith(close_tok):
            inner = s[len(open_tok) : -len(close_tok)].strip()
            return _looks_like_file_path(inner)
    else:
        if s.startswith(comment_syntax):
            inner = s[len(comment_syntax) :].strip()
            return _looks_like_file_path(inner)

    return False


def posix_relpath(path: str, start: str) -> str:
    """Relative path with POSIX-style forward slashes (stable across OS)."""
    rel = os.path.relpath(path, start)
    return rel.replace("\\", "/")


def detect_newline(text: str) -> str:
    """Return newline style used in text; default to '\n'."""
    # Find first newline occurrence
    idx = text.find("\n")
    if idx == -1:
        return "\n"
    # Check preceding \r
    if idx > 0 and text[idx - 1] == "\r":
        return "\r\n"
    return "\n"


# ---------------------------
# Core processing
# ---------------------------
def process_single_file(
    file_path: str,
    root_dir_abs: str,
    *,
    verbose: bool = False,
    dry_run: bool = False,
    max_remove: int = DEFAULT_MAX_REMOVE,
    trim_leading_blank: bool = True,
) -> str:
    """
    Process a single file. Returns one of: 'updated', 'unchanged', 'skipped', 'error'.
    """
    try:
        if not os.path.isfile(file_path):
            if verbose:
                print(f"File not found: {file_path}", file=sys.stderr)
            return "error"

        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()

        if not should_process_file(file_name, file_ext):
            print(f"Warning: Unsupported file type for '{file_path}', skipping.")
            return "skipped"

        comment_syntax = get_comment_syntax(file_name, file_ext)
        if not comment_syntax:
            print(f"Warning: No comment syntax for '{file_path}', skipping.")
            return "skipped"

        # Read file preserving newlines
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            data = f.read()

        if data == "":
            # Empty file — nothing to do
            print(f"Warning: Empty file '{file_path}', skipping.")
            return "skipped"

        newline = detect_newline(data)
        lines = data.splitlines(keepends=False)  # strip EOLs; we’ll add newline when writing

        # Remove up to max_remove existing file-path comments at the very top
        removed = 0
        while lines and removed < max_remove and is_file_path_comment(lines[0], comment_syntax):
            lines.pop(0)
            removed += 1

        # Optional trim leading blank lines (common when we removed a header)
        if trim_leading_blank:
            while lines and lines[0].strip() == "":
                lines.pop(0)

        # Create new header comment with relative posix path
        rel_path = posix_relpath(file_path, root_dir_abs)
        if isinstance(comment_syntax, tuple):
            open_tok, close_tok = comment_syntax
            new_header = f"{open_tok} {rel_path} {close_tok}"
        else:
            new_header = f"{comment_syntax} {rel_path}"

        # If the first line already equals our new header (idempotent), nothing to do
        if lines and lines[0].strip() == new_header.strip():
            return "unchanged"

        # Insert header
        new_lines = [new_header] + lines

        if dry_run:
            # Don't write; just report what would change
            return "updated"

        # Write back preserving newline style
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(newline.join(new_lines))
            # Ensure trailing newline if original had it; we cannot know reliably for last line,
            # but typical source files end with a newline — keep consistent:
            f.write(newline)

        return "updated"

    except Exception as e:
        print(f"Error processing '{file_path}': {e}", file=sys.stderr)
        return "error"


def collect_files_from_directory(root_dir_abs: str, ignore_dirs: Iterable[str]) -> List[str]:
    """
    Walk directory tree and collect absolute paths of processable files.
    - Returns absolute paths only.
    - Ignores directories by simple name match (case-sensitive).
    """
    ignore_set = set(ignore_dirs)
    files: List[str] = []

    for dirpath, dirnames, filenames in os.walk(root_dir_abs):
        # prune ignored dirs in-place
        dirnames[:] = [d for d in dirnames if d not in ignore_set]

        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if should_process_file(filename, ext):
                files.append(os.path.join(dirpath, filename))

    return files


def process_files(
    file_list: List[str],
    root_dir: str,
    *,
    verbose: bool = False,
    dry_run: bool = False,
    max_remove: int = DEFAULT_MAX_REMOVE,
    trim_leading_blank: bool = True,
) -> Dict[str, int]:
    """Process a list of files, return stats dict."""
    if not file_list:
        print("No files to process.")
        return {"updated": 0, "unchanged": 0, "skipped": 0, "error": 0}

    root_dir_abs = os.path.abspath(root_dir)

    # Normalize to absolute paths
    abs_files: List[str] = []
    for p in file_list:
        abs_files.append(p if os.path.isabs(p) else os.path.abspath(p))

    # Stats
    stats = {"updated": 0, "unchanged": 0, "skipped": 0, "error": 0}

    for file_path in abs_files:
        result = process_single_file(
            file_path,
            root_dir_abs,
            verbose=verbose,
            dry_run=dry_run,
            max_remove=max_remove,
            trim_leading_blank=trim_leading_blank,
        )
        stats[result] = stats.get(result, 0) + 1

        rel_for_print = posix_relpath(file_path, root_dir_abs)
        if result == "updated":
            # print(f"✅ Updated: {rel_for_print}")
            pass
        elif result == "error":
            print(f"❌ Error:   {rel_for_print}")
        elif verbose and result == "skipped":
            print(f"⏭️  Skipped: {rel_for_print}")
        elif verbose and result == "unchanged":
            print(f"➖ Unchanged: {rel_for_print}")

    return stats


# ---------------------------
# CLI
# ---------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Insert a file-path comment at the top of source files",
        epilog="""Examples:
  # Process specific files
  %(prog)s -f file1.py file2.js

  # Process entire directory (root defaults to directory)
  %(prog)s -d backend/app

  # Directory but explicit root for shorter relative paths
  %(prog)s -d backend/app --root backend/app

  # Use with git (modified files)
  git ls-files --modified | %(prog)s --stdin --root backend/app

  # Dry run (no writes)
  %(prog)s -d backend/app --dry-run -v
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Inputs
    parser.add_argument("-f", "--files", nargs="*", default=[], help="Specific files to process")
    parser.add_argument("--stdin", action="store_true", help="Read additional files from stdin")
    parser.add_argument("-d", "--directory", help="Process all supported files in directory recursively")

    # Config
    parser.add_argument(
        "--root",
        default=None,
        help="Root directory for relative paths; defaults to --directory if set, else current dir",
    )
    parser.add_argument(
        "--ignore-dirs",
        nargs="*",
        default=sorted(DEFAULT_IGNORE_DIRS),
        help="Directory names to ignore when using --directory",
    )
    parser.add_argument(
        "--max-remove", type=int, default=DEFAULT_MAX_REMOVE, help="Max number of existing header lines to remove"
    )
    parser.add_argument(
        "--no-trim-leading-blank-lines", action="store_true", help="Do not trim blank lines after removing old header"
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not write changes, only report")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Collect file paths
    all_files: List[str] = []

    # From explicit list
    if args.files:
        all_files.extend(args.files)

    # From stdin
    if args.stdin:
        stdin_files = [line.strip() for line in sys.stdin if line.strip()]
        all_files.extend(stdin_files)

    # From directory
    directory_abs = None
    if args.directory:
        if not os.path.isdir(args.directory):
            print(f"Error: Directory '{args.directory}' does not exist", file=sys.stderr)
            sys.exit(1)
        directory_abs = os.path.abspath(args.directory)
        all_files.extend(collect_files_from_directory(directory_abs, args.ignore_dirs))

    if not all_files:
        print("Error: No files to process.", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Determine effective root
    if args.root:
        root_dir = args.root
    elif directory_abs:
        root_dir = directory_abs
    else:
        root_dir = os.getcwd()

    # Deduplicate while preserving order
    seen = set()
    unique_abs_files: List[str] = []
    for p in all_files:
        ap = p if os.path.isabs(p) else os.path.abspath(p)
        if ap not in seen:
            seen.add(ap)
            unique_abs_files.append(ap)

    # Process
    stats = process_files(
        unique_abs_files,
        root_dir,
        verbose=args.verbose,
        dry_run=args.dry_run,
        max_remove=max(0, args.max_remove),
        trim_leading_blank=not args.no_trim_leading_blank_lines,
    )

    total = sum(stats.values())
    print("\n📊 Summary:")
    print(f"   Updated:   {stats.get('updated', 0)}")
    print(f"   Unchanged: {stats.get('unchanged', 0)}")
    print(f"   Skipped:   {stats.get('skipped', 0)}")
    print(f"   Errors:    {stats.get('error', 0)}")
    print(f"   Total:     {total}")


if __name__ == "__main__":
    main()
