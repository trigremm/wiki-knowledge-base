#!/bin/bash
# Script to generate a text file containing the contents of specified files from a directory
#
# Usage:
#   ./script.sh -p <path> [-o output_file] [-i ignore_pattern] [-e include_extensions] [-x exclude_extensions]
#
# Options:
#   -p <path>              Required. Directory path to scan
#   -o <output_file>       Optional. Output file path (default: prompt.txt)
#   -i <ignore_pattern>    Optional. Additional directories/files to ignore
#   -e <extensions>        Optional. File extensions to include (comma-separated, e.g., 'py,js,ts')
#   -x <extensions>        Optional. File extensions to exclude (comma-separated, e.g., 'css,scss')
#
# Examples:
#   # Basic usage - scan directory with default settings
#   ./script.sh -p /path/to/project
#
#   # Specify output file and add custom ignore pattern
#   ./script.sh -p /path/to/project -o custom_output.txt -i temp_files
#
#   # Include only specific extensions
#   ./script.sh -p /path/to/project -e py,js,ts
#
#   # Exclude specific extensions
#   ./script.sh -p /path/to/project -x css,scss
#
#   # Combine include and exclude patterns
#   ./script.sh -p /path/to/project -e py,js,ts -x test.py,spec.js

path=""
output_file="prompt.txt"  # Set default output file
declare -a additional_ignores
declare -a include_extensions
declare -a exclude_extensions

# Default ignore list (directories/files to skip)
DEFAULT_IGNORE=(
    .idea
    .vscode
    .DS_Store
    .git
    .venv
    .docker_volumes
    asmo.d
    __pycache__
    migrations
    node_modules
    dist
    build
)

# Default file extensions to include
DEFAULT_EXTENSIONS=(
    "Dockerfile"
    "*.yml"
    "*.yaml"
    "*.toml"
    "*.py"
    "*.hurl"
    "package.json"
    "tsconfig.json"
    "*.js"
    "*.ts"
    "*.vue"
)

# Use getopts to parse command line arguments
while getopts ":p:i:o:e:x:" opt; do
  case $opt in
    p)
      path="$OPTARG"
      ;;
    i)
      additional_ignores+=("$OPTARG")
      ;;
    o)
      output_file="$OPTARG"
      ;;
    e)
      # Add extension to include (comma-separated)
      IFS=',' read -ra EXTS <<< "$OPTARG"
      for ext in "${EXTS[@]}"; do
        include_extensions+=("*.$ext")
      done
      ;;
    x)
      # Add extension to exclude (comma-separated)
      IFS=',' read -ra EXTS <<< "$OPTARG"
      for ext in "${EXTS[@]}"; do
        exclude_extensions+=("*.$ext")
      done
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Validate required path argument
if [ -z "$path" ]; then
    echo "Error: Path argument (-p) is required"
    echo "Usage: $0 -p <path> [-o output_file] [-i ignore_pattern] [-e include_extensions] [-x exclude_extensions]"
    exit 1
fi

# If no include extensions specified, use defaults
if [ ${#include_extensions[@]} -eq 0 ]; then
    include_extensions=("${DEFAULT_EXTENSIONS[@]}")
fi

# Create parent directories if they don't exist
if [[ "$output_file" == */* ]]; then
    mkdir -p "$(dirname "$output_file")"
fi

# Initialize the output file
> "$output_file"

# Combine default and additional ignores
ignores=("${DEFAULT_IGNORE[@]}" "${additional_ignores[@]}")

# Build the find command
find_cmd="find \"$path\""

# Add ignore directories
for ignore in "${ignores[@]}"; do
    find_cmd+=" -type d -name \"$ignore\" -prune -o"
done

# Start the file pattern section
find_cmd+=" \("

# Add include patterns
first=true
for ext in "${include_extensions[@]}"; do
    if [ "$first" = true ]; then
        find_cmd+=" -name \"$ext\""
        first=false
    else
        find_cmd+=" -o -name \"$ext\""
    fi
done
find_cmd+=" \)"

# Add exclude patterns if any
for ext in "${exclude_extensions[@]}"; do
    find_cmd+=" ! -name \"$ext\""
done

# Complete the find command
find_cmd+=" -type f -print0 | xargs -0 -I {} sh -c '"
find_cmd+="echo \"{}:\" >> \"$output_file\"; "
find_cmd+="cat \"{}\" >> \"$output_file\"; "
find_cmd+="echo \"\" >> \"$output_file\"; "
find_cmd+="echo \"\" >> \"$output_file\""
find_cmd+="'"

# Execute the dynamically built find command
eval $find_cmd

# Print summary
echo "Content of specified files from $path have been written to $output_file"
echo "Ignored directories and files: ${ignores[*]}"
echo "Included extensions: ${include_extensions[*]}"
echo "Excluded extensions: ${exclude_extensions[*]}"
