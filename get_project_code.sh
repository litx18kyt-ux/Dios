#!/bin/bash
OUTPUT_FILE="complete_project_code.txt"
echo "=== PROJECT FOLDER STRUCTURE ===" > "$OUTPUT_FILE"
tree -I "node_modules|.git|.next|dist|build|venv|__pycache__|.vscode" >> "$OUTPUT_FILE" 2>/dev/null || find . -maxdepth 3 -not -path '*/.*' -not -path './node_modules*' >> "$OUTPUT_FILE"
echo -e "\n\n=== FILE CONTENTS ===" >> "$OUTPUT_FILE"

find . -type f \
  ! -path '*/.*' \
  ! -path '*/node_modules/*' \
  ! -path '*/venv/*' \
  ! -path '*/dist/*' \
  ! -path '*/build/*' \
  ! -path '*/__pycache__/*' \
  ! -name "*.png" ! -name "*.jpg" ! -name "*.jpeg" ! -name "*.ico" ! -name "*.svg" ! -name "*.lock" ! -name "package-lock.json" \
  ! -name "$OUTPUT_FILE" \
  | while read -r file; do
    echo -e "\n\n====================================" >> "$OUTPUT_FILE"
    echo "FILE: $file" >> "$OUTPUT_FILE"
    echo -e "====================================\n" >> "$OUTPUT_FILE"
    cat "$file" >> "$OUTPUT_FILE"
done

echo "Done! Sara code '$OUTPUT_FILE' me save ho gaya hai."
