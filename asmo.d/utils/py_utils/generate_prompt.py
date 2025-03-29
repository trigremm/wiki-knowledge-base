import argparse
import os
from pathlib import Path

DEFAULT_IGNORE = {
    ".idea",
    ".vscode",
    ".DS_Store",
    ".git",
    ".venv",
    ".docker_volumes",
    "asmo.d",
    "__pycache__",
    "migrations",
    "node_modules",
    "dist",
    "build",
}

DEFAULT_EXTENSIONS = [
    "Dockerfile",
    "*.yml",
    "*.yaml",
    "*.toml",
    "*.py",
    "*.hurl",
    "package.json",
    "tsconfig.json",
    "*.js",
    "*.ts",
    "*.vue",
]


def match_pattern(file: Path, patterns):
    for pattern in patterns:
        if pattern == file.name:
            return True
        if pattern.startswith("*") and file.suffix == pattern[1:]:
            return True
    return False


def should_include(file: Path, include_patterns, exclude_patterns):
    if include_patterns and not match_pattern(file, include_patterns):
        return False
    if exclude_patterns and match_pattern(file, exclude_patterns):
        return False
    return True


def collect_files(path, ignores, include_patterns, exclude_patterns):
    collected = []
    for root, dirs, files in os.walk(path):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if d not in ignores]
        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(path)
            if should_include(file_path, include_patterns, exclude_patterns):
                collected.append(file_path)
    return collected


def main():
    parser = argparse.ArgumentParser(
        description="Collect files and generate a text output"
    )
    parser.add_argument("-p", "--path", required=True, help="Directory path to scan")
    parser.add_argument("-o", "--output", default="prompt.txt", help="Output file")
    parser.add_argument(
        "-i",
        "--ignore",
        default="",
        help="Additional ignore patterns (comma-separated)",
    )
    parser.add_argument(
        "-e",
        "--include",
        default="",
        help="Include extensions (comma-separated, e.g., 'py,js')",
    )
    parser.add_argument(
        "-x", "--exclude", default="", help="Exclude extensions (comma-separated)"
    )

    args = parser.parse_args()
    path = Path(args.path).resolve()

    if not path.is_dir():
        print(f"Error: {path} is not a valid directory")
        return

    output_file = Path(args.output)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    ignores = DEFAULT_IGNORE.union(
        {p.strip() for p in args.ignore.split(",") if p.strip()}
    )
    include_patterns = [
        f"*.{ext.strip()}" for ext in args.include.split(",") if ext.strip()
    ] or DEFAULT_EXTENSIONS
    exclude_patterns = [
        f"*.{ext.strip()}" for ext in args.exclude.split(",") if ext.strip()
    ]

    collected_files = collect_files(path, ignores, include_patterns, exclude_patterns)

    with output_file.open("w", encoding="utf-8") as out:
        for file_path in collected_files:
            out.write(f"{file_path}:\n")
            try:
                out.write(file_path.read_text(encoding="utf-8") + "\n\n")
            except Exception as e:
                out.write(f"# Error reading {file_path}: {e}\n\n")

    print(f"Wrote content from {len(collected_files)} files to {output_file}")
    print(f"Ignored: {', '.join(ignores)}")
    print(f"Included patterns: {', '.join(include_patterns)}")
    print(f"Excluded patterns: {', '.join(exclude_patterns)}")


if __name__ == "__main__":
    main()
