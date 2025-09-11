#!/bin/bash

# Dokumentacja projektu Django
# Generuje: strukturę katalogów, metadane plików i zawartość tekstowych plików
# Pomija: pliki binarne, duże pliki (>100KB), środowiska wirtualne i cache

# Konfiguracja
OUTPUT_FILE="django_project_docs.txt"
MAX_SIZE_KB=100
EXCLUDE_DIRS=("__pycache__" ".git" "venv" ".venv" "env" "node_modules" "static" "media" "migrations")
EXCLUDE_EXTS=("pyc" "png" "jpg" "jpeg" "gif" "ico" "pdf" "zip" "tar.gz" "log" "sqlite3" "mo" "pot" "bin" "class" "jar")

# Nagłówek dokumentacji
echo "DOKUMENTACJA PROJEKTU DJANGO" > "$OUTPUT_FILE"
echo "Wygenerowano: $(date)" >> "$OUTPUT_FILE"
echo "======================================" >> "$OUTPUT_FILE"

# 1. Struktura katalogów
echo -e "\nSTRUKTURA PROJEKTU:" >> "$OUTPUT_FILE"
if command -v tree &> /dev/null; then
    tree -a -I "$(IFS=\|; echo "${EXCLUDE_DIRS[*]}")" >> "$OUTPUT_FILE"
else
    find . -type d | grep -vE "$(IFS=\|; echo "${EXCLUDE_DIRS[*]/#/./}")" >> "$OUTPUT_FILE"
fi

# 2. Metadane plików
echo -e "\n\nMETADANE PLIKÓW:" >> "$OUTPUT_FILE"
echo "Permisje | Rozmiar | Właściciel | Grupa | Data modyfikacji | Ścieżka" >> "$OUTPUT_FILE"
find . -type f -not -path "*$(printf "%s*" "${EXCLUDE_DIRS[@]/#/./}")" -not -name "*.$ext" | while read -r file; do
    ext="${file##*.}"
    if [[ ! " ${EXCLUDE_EXTS[@]} " =~ " ${ext} " ]]; then
        stat -c "%A | %s | %U | %G | %y | %n" "$file" >> "$OUTPUT_FILE"
    fi
done

# 3. Zawartość plików
echo -e "\n\nZAWARTOŚĆ PLIKÓW:" >> "$OUTPUT_FILE"
find . -type f -not -path "*$(printf "%s*" "${EXCLUDE_DIRS[@]/#/./}")" -not -name "*.$ext" | while read -r file; do
    ext="${file##*.}"
    if [[ " ${EXCLUDE_EXTS[@]} " =~ " ${ext} " ]] || \
       [ $(stat -c %s "$file") -gt $((MAX_SIZE_KB*1024)) ] || \
       file -b --mime-encoding "$file" | grep -q binary; then
        continue
    fi

    echo -e "\n===== $file =====" >> "$OUTPUT_FILE"
    echo "[Rozmiar: $(du -h "$file" | cut -f1)]" >> "$OUTPUT_FILE"
    echo "[Kodowanie: $(file -b --mime-encoding "$file")]" >> "$OUTPUT_FILE"
    echo "--------------------------------------" >> "$OUTPUT_FILE"
    cat -n "$file" >> "$OUTPUT_FILE"
    echo -e "\n===== KONIEC PLIKU =====" >> "$OUTPUT_FILE"
done

echo "Dokumentacja zapisana w: $OUTPUT_FILE"
