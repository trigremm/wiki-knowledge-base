#!/bin/bash
# https://github.com/trigremm/wiki_best_practices/blob/main/bonus.d/utils.d/generate_prompt.sh

path=""
output_file="prompt.txt"  # Set default output file
declare -a additional_ignores

# Default ignore list
DEFAULT_IGNORE=(
    .git
    .DS_Store
    .vscode
    .idea
    .venv
    .docker_volumes
    __pycache__
    node_modules
    dist
    build
)

# Use getopts to parse command line arguments
while getopts ":p:i:o:" opt; do
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

# Create parent directories if they don't exist (only if output file is not in current directory)
if [[ "$output_file" == */* ]]; then
    mkdir -p "$(dirname "$output_file")"
fi

# Initialize the output file
> "$output_file"

# Combine default and additional ignores
ignores=("${DEFAULT_IGNORE[@]}" "${additional_ignores[@]}")

# Build the find command
find_cmd="find \"$path\""

for ignore in "${ignores[@]}"; do
    find_cmd+=" -type d -name \"$ignore\" -prune -o"
done

find_cmd+=" \( -name \"*.py\" -o -name \"*.js\" -o -name \"*.ts\" -o -name \"*.vue\" "
find_cmd+="-o -name \"*.yaml\" -o -name \"*.yml\" -o -name \"Dockerfile\" -o -name \"*.toml\" "
find_cmd+="-o -name \"package.json\" -o -name \"tsconfig.json\" -o -name \"*.hurl\" \) -type f -print0 | xargs -0 -I {} sh -c '"
find_cmd+="echo \"{}:\" >> \"$output_file\"; "
find_cmd+="cat \"{}\" >> \"$output_file\"; "
find_cmd+="echo \"\" >> \"$output_file\"; "
find_cmd+="echo \"\" >> \"$output_file\""
find_cmd+="'"

# Execute the dynamically built find command
eval $find_cmd

echo "Content of specified files from $path have been written to $output_file"
echo "Ignored directories and files: ${ignores[*]}"
