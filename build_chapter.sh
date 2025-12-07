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
)

echo "==> 1. Собираем full-ридми по блокам"

for dir in "${BLOCK_DIRS[@]}"; do
  BLOCK_PATH="${ROOT_DIR}/${dir}"
  [ -d "${BLOCK_PATH}" ] || continue

  OUT_FILE="${BLOCK_PATH}/block_full.md"
  echo "  - ${dir} -> ${OUT_FILE}"

  : > "${OUT_FILE}"  # очистить файл

  # Находим все readme.md внутри блока и склеиваем
  find "${BLOCK_PATH}" -type f -iname 'readme.md' -print0 \
    | sort -z \
    | while IFS= read -r -d '' f; do
        rel="${f#${ROOT_DIR}/}"
        {
          echo "<!-- ${rel} -->"
          echo
          cat "${f}"
          echo
          echo '---'
          echo
        } >> "${OUT_FILE}"
      done
done

echo "==> 2. Пересобираем chapter3_full.md (с фиксом путей картинок)"

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

files = []

# Сначала корневой README.md
root_readme = root / 'README.md'
if root_readme.exists():
    files.append(root_readme)

# Затем все readme.md внутри блоков (в отсортированном порядке)
for base in order_dirs[1:]:
    base_path = (root / base).resolve()
    if not base_path.exists():
        continue
    for p in sorted(base_path.rglob('readme.md')):
        files.append(p)

img_re = re.compile(r"!\[(.*?)\]\(([^)]+)\)")

out_path = root / 'chapter3_full.md'
with out_path.open('w', encoding='utf-8') as out:
    for idx, path in enumerate(files):
        rel_path = path.relative_to(root).as_posix()
        if idx > 0:
            out.write("\n\n---\n\n")
        out.write(f"<!-- {rel_path} -->\n\n")

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

print(f"written {out_path}")
PY

echo "==> 3. (опционально) Обновляем DOCX"

if [ -x "${ROOT_DIR}/.venv/bin/python" ]; then
  "${ROOT_DIR}/.venv/bin/python" md_to_docx.py chapter3_full.md chapter3_full.docx
  echo "written ${ROOT_DIR}/chapter3_full.docx"
else
  echo "  .venv не найден или python не исполняемый, DOCX не обновлён"
fi

echo "Готово."
