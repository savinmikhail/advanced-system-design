#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Топовые папки-блоки главы 3
BLOCK_DIRS=(
  "01_performance"
  "02_sanity_check"
  "03_sharding"
  "04_cache"
  "05_distributed-transactions"
  "06_tradeoffs"
  "07_outro"
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
    Path('01_performance'),
    Path('02_sanity_check'),
    Path('03_sharding'),
    Path('04_cache'),
    Path('05_distributed-transactions'),
    Path('06_tradeoffs'),
    Path('07_outro'),
]

img_re = re.compile(r"!\[(.*?)\]\(([^)]+)\)")
heading_re = re.compile(r"^(#{1,6})\s+(.+)$")


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


def slugify(title: str, counters: dict[str, int]) -> str:
    # GitHub‑подобный якорь: в нижнем регистре, пробелы -> '-', без лишней пунктуации
    base = title.strip().lower()
    base = re.sub(r"[^\w\s-]", "", base)
    base = re.sub(r"\s+", "-", base)
    base = re.sub(r"-+", "-", base)

    count = counters.get(base, 0)
    if count:
        slug = f"{base}-{count}"
    else:
        slug = base
    counters[base] = count + 1
    return slug


def write_chapter(files: list[Path], out_path: Path) -> None:
    toc_entries: list[tuple[int, str, str]] = []
    body_chunks: list[str] = []
    anchor_counters: dict[str, int] = {}

    for idx, path in enumerate(files):
        if idx > 0:
            body_chunks.append("\n\n---\n\n")

        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()

            # Собираем заголовки для оглавления
            h = heading_re.match(stripped)
            if h:
                hashes, title = h.groups()
                level = len(hashes)
                anchor = slugify(title, anchor_counters)
                toc_entries.append((level, title.strip(), anchor))

            m = img_re.fullmatch(stripped)
            if m:
                alt, rel_img = m.groups()
                # Пересчитываем путь картинки относительно корня репо
                if rel_img.startswith("/"):
                    new_path = rel_img.lstrip("/")
                else:
                    new_path = (path.parent / rel_img).resolve().relative_to(root).as_posix()
                body_chunks.append(f"![{alt}]({new_path})\n")
            else:
                body_chunks.append(line + "\n")

    with out_path.open("w", encoding="utf-8") as out:
        if toc_entries:
            out.write("## Оглавление\n\n")
            for level, title, anchor in toc_entries:
                indent = "  " * (level - 1)
                out.write(f"{indent}- [{title}](#{anchor})\n")
            out.write("\n---\n\n")

        for chunk in body_chunks:
            out.write(chunk)


# Бесплатная версия (только readme.md)
free_files = collect_files("readme.md", "README.md")
free_out = root / "chapter3_free.md"
write_chapter(free_files, free_out)
print(f"written {free_out}")

# Платная версия (только readme.boosty.md)
boosty_files = collect_files("readme.boosty.md", "README.boosty.md")
boosty_out = root / "chapter3_boosty.md"
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
