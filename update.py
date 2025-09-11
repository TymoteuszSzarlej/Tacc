import os
import subprocess
from datetime import datetime

# 🛠️ Krok 1: Wykonaj git pull w każdym podfolderze (repozytorium)
def git_pull_all_repos(base_path='.'):
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path) and os.path.exists(os.path.join(folder_path, '.git')):
            print(f"🔄 Wykonuję git pull w: {folder_path}")
            subprocess.run(['git', '-C', folder_path, 'pull'], check=False)

# 📄 Krok 2: Pobierz ostatnią wersję z pliku versions.txt
def get_last_version(file_path='./Tacc/MAIN/versions.txt'):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if not lines:
            return None
        return lines[-1].strip()

# 🧮 Krok 3: Oblicz nową wersję
def generate_new_version(last_version):
    current_year = datetime.now().year % 100  # np. 2025 → 25
    if last_version:
        year_part, num_part = last_version.split('.')
        if int(year_part) == current_year:
            new_num = int(num_part) + 1
        else:
            new_num = 0
    else:
        new_num = 0
    return f"{current_year:02d}.{new_num:02d}"

# 📝 Krok 4: Zapisz nową wersję i opis do plików
def append_to_files(new_version, description, version_file='./Tacc/MAIN/versions.txt', changes_file='./TACC/MAIN/changes.txt'):
    with open(version_file, 'a') as vf:
        vf.write(new_version + '\n')
    with open(changes_file, 'a') as cf:
        cf.write(description + '\n')
    with open('./Tacc/MAIN/release_dates.txt', 'a') as file:
        file.write(datetime.now().strftime('%Y-%m-%d') + '\n')

    print(f"✅ Zapisano wersję: {new_version}")
    print(f"🗒️ Opis: {description}")

# 🚀 Główna logika
if __name__ == "__main__":
    git_pull_all_repos()
    last_version = get_last_version()
    new_version = generate_new_version(last_version)
    description = input("✍️ Podaj opis aktualizacji: ")
    append_to_files(new_version, description)
