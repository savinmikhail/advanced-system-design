#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Топовые папки-блоки главы 3
BLOCK_DIRS=(
  "00_performance"
  "01_sharding"
  "02_distributed-transactions"
  "03_cache"
  "04_trade_offs"
  "05_outro"
)

echo "==> 1. Собираем block_full.*.md по блокам (отдельно free и boosty)"

for dir in "${BLOCK_DIRS[@]}"; do
  BLOCK_PATH="${ROOT_DIR}/${dir}"
  [ -d "${BLOCK_PATH}" ] || continue

  # Бесплатная версия блока — агрегируем все readme.md
  OUT_FILE_FREE="${BLOCK_PATH}/block_full.md"
  echo "  - ${dir} (free)   -> ${OUT_FILE_FREE}"
  : > "${OUT_FILE_FREE}"

  find "${BLOCK_PATH}" -type f -iname 'readme.md' -print0 \
    | sort -z \
    | while IFS= read -r -d '' f; do
        {
          echo
          cat "${f}"
          echo
        } >> "${OUT_FILE_FREE}"
      done

  # Платная версия блока — агрегируем все readme.boosty.md (если есть)
  OUT_FILE_BOOSTY="${BLOCK_PATH}/block_full.boosty.md"
  echo "  - ${dir} (boosty) -> ${OUT_FILE_BOOSTY}"
  : > "${OUT_FILE_BOOSTY}"

  find "${BLOCK_PATH}" -type f -iname 'readme.boosty.md' -print0 \
    | sort -z \
    | while IFS= read -r -d '' f; do
        {
          echo
          cat "${f}"
          echo
        } >> "${OUT_FILE_BOOSTY}"
      done
done

echo "==> 2. Пересобираем отдельные сценарии free/boosty (с фиксом путей картинок)"

python3 << 'PY'
from pathlib import Path
import re

root = Path(__file__).resolve().parent

order_dirs = [
    Path('.'),
    Path('00_performance'),
    Path('01_sharding'),
    Path('02_distributed-transactions'),
    Path('03_cache'),
    Path('04_trade_offs'),
]

img_re = re.compile(r"!\[(.*?)\]\(([^)]+)\)")


def collect_files(readme_name: str, root_readme_name: str) -> list[Path]:
    files: list[Path] = []

    root_readme = root / root_readme_name
    if root_readme.exists():
        files.append(root_readme)

    for base in order_dirs[1:]:
        base_path = (root / base).resolve()
        if not base_path.exists():
            continue
        for p in sorted(base_path.rglob(readme_name)):
            files.append(p)

    return files


def write_chapter(files: list[Path], out_path: Path) -> None:
    with out_path.open('w', encoding='utf-8') as out:
        for idx, path in enumerate(files):
            if idx > 0:
                out.write("\n\n---\n\n")

            text = path.read_text(encoding='utf-8')
            for line in text.splitlines():
                stripped = line.strip()
                m = img_re.fullmatch(stripped)
                if m:
                    alt, rel_img = m.groups()
                    # Пересчитываем путь картинки относительно корня репо
                    if rel_img.startswith('/'):
                        new_path = rel_img.lstrip('/')
                    else:
                        new_path = (path.parent / rel_img).resolve().relative_to(root).as_posix()
                    out.write(f"![{alt}]({new_path})\n")
                else:
                    out.write(line + "\n")


# Бесплатная версия (только readme.md)
free_files = collect_files('readme.md', 'README.md')
free_out = root / 'chapter3_free.md'
write_chapter(free_files, free_out)
print(f"written {free_out}")

# Платная версия (только readme.boosty.md)
boosty_files = collect_files('readme.boosty.md', 'README.boosty.md')
boosty_out = root / 'chapter3_boosty.md'
write_chapter(boosty_files, boosty_out)
print(f"written {boosty_out}")
PY

echo "==> 3. (опционально) Обновляем DOCX"

if [ -x "${ROOT_DIR}/.venv/bin/python" ]; then
  # Бесплатный сценарий
  "${ROOT_DIR}/.venv/bin/python" md_to_docx.py chapter3_free.md chapter3_free.docx
  echo "written ${ROOT_DIR}/chapter3_free.docx"

  # Платный сценарий
  "${ROOT_DIR}/.venv/bin/python" md_to_docx.py chapter3_boosty.md chapter3_boosty.docx
  echo "written ${ROOT_DIR}/chapter3_boosty.docx"
else
  echo "  .venv не найден или python не исполняемый, DOCX не обновлён"
fi

echo "Готово."
