#!/usr/bin/env python3
import sys
from pathlib import Path

# Можно переопределить через аргумент: python estimate_times.py 120
WPM = int(sys.argv[1]) if len(sys.argv) > 1 else 130

root = Path(__file__).resolve().parent

ORDER_DIRS = [
  Path('.'),
  Path('00_performance'),
  Path('01_sharding'),
  Path('02_distributed-transactions'),
  Path('03_cache'),
  Path('04_trade_offs'),
  Path('05_outro'),
]

def count_words(path: Path) -> int:
  text = path.read_text(encoding='utf-8')
  return sum(len(line.split()) for line in text.splitlines())

def gather_files(readme_name: str, root_readme_name: str) -> list[Path]:
  files: list[Path] = []

  root_readme = root / root_readme_name
  if root_readme.exists():
      files.append(root_readme)

  for base in ORDER_DIRS[1:]:
      base_path = (root / base).resolve()
      if not base_path.exists():
          continue
      for p in sorted(base_path.rglob(readme_name)):
          files.append(p)

  return files


def report_for_files(files: list[Path], label: str) -> None:
  total_words = 0
  per_block: dict[str, int] = {}

  print(f"=== {label} ===")
  print("Per file:")
  print("-" * 72)

  for path in files:
      rel = path.relative_to(root)
      words = count_words(path)
      minutes = words / WPM if WPM > 0 else 0.0
      total_words += words

      # блок = первый сегмент пути (или 'root' для README.*)
      parts = rel.parts
      block = parts[0] if len(parts) > 1 else 'root'
      per_block[block] = per_block.get(block, 0) + words

      print(f"{str(rel):60} {words:6d} words  ~{minutes:5.1f} min")

  print()
  print("Per block:")
  print("-" * 72)
  for block, words in per_block.items():
      minutes = words / WPM if WPM > 0 else 0.0
      print(f"{block:30} {words:6d} words  ~{minutes:5.1f} min")

  print()
  total_minutes = total_words / WPM if WPM > 0 else 0.0
  total_hours = total_minutes / 60
  print(f"Total: {total_words} words  ~{total_minutes:.1f} min (~{total_hours:.2f} h)")
  print("\n")


def main() -> None:
  print(f"WPM (words per minute): {WPM}\n")

  # Бесплатная версия (readme.md)
  free_files = gather_files('readme.md', 'README.md')
  report_for_files(free_files, "FREE (readme.md)")

  # Платная версия (readme.boosty.md)
  boosty_files = gather_files('readme.boosty.md', 'README.boosty.md')
  if boosty_files:
      report_for_files(boosty_files, "PAID / BOOSTY (readme.boosty.md)")
  else:
      print("=== PAID / BOOSTY (readme.boosty.md) ===")
      print("Нет файлов readme.boosty.md, считать пока нечего.\n")

if __name__ == "__main__":
  main()
