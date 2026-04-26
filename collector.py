import os

# ✅ указываешь что включать
INCLUDE_PATHS = [
    "app",  # папка (возьмёт всё внутри)
    ".env",
    ".gitignore",
    "docker-compose.yml",
    "Dockerfile",
    ".dockerignore"
]


def is_text_file(filepath: str) -> bool:
    """Проверяет, является ли файл текстовым"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            f.read(1024)
        return True
    except Exception:
        return False


def collect_included_files(root_dir: str):
    """Собирает только указанные файлы и директории"""
    collected_files = []

    for path in INCLUDE_PATHS:
        full_path = os.path.join(root_dir, path)

        if os.path.isfile(full_path):
            if is_text_file(full_path):
                collected_files.append(full_path)

        elif os.path.isdir(full_path):
            for dirpath, _, filenames in os.walk(full_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if is_text_file(file_path):
                        collected_files.append(file_path)

    return collected_files


def merge_files(file_paths, output_file: str):
    """Объединяет файлы в один"""
    with open(output_file, "w", encoding="utf-8") as outfile:
        for path in sorted(file_paths):
            outfile.write(f"\n# ===== FILE: {path} =====\n\n")
            try:
                with open(path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())
                    outfile.write("\n")
            except Exception as e:
                outfile.write(f"# ERROR reading file: {e}\n")


def main():
    root_directory = os.path.dirname(os.path.abspath(__file__))
    output_file = "merged_output.txt"

    files = collect_included_files(root_directory)

    print(f"Собрано файлов: {len(files)}")

    merge_files(files, output_file)

    print(f"Готово! Результат сохранён в {output_file}")


if __name__ == "__main__":
    main()
