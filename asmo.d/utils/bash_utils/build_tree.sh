#!/bin/bash
# https://github.com/trigremm/wiki_best_practices/blob/main/bonus.d/utils.d/build_tree.sh

# Default ignore list
DEFAULT_IGNORE=(
    .git
    .DS_Store
    .vscode
    .idea
    .docker_volumes
    __pycache__
    node_modules
    dist
    build
)

# Function to join array elements with a separator
join_by() {
    local IFS="$1"
    shift
    echo "$*"
}

# Parse command line arguments
DIRECTORY="${1:-.}"  # Use current directory if not specified
shift

# Combine default ignore list with any additional items from command line
IGNORE=("${DEFAULT_IGNORE[@]}" "$@")

# Create the ignore pattern
IGNORE_PATTERN=$(join_by '|' "${IGNORE[@]}")

# Run tree command with ignore pattern
tree -I "$IGNORE_PATTERN" "$DIRECTORY"
