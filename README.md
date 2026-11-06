# slug-generator

Turn titles and headings into clean URL slugs — from the terminal, with
Python's standard library only. No dependencies, no setup.

## What it does

- Lowercases and strips accents (`Café` → `cafe`)
- Turns punctuation and spaces into a separator (`Hello, World!` → `hello-world`)
- Collapses repeated separators and trims the edges
- Reads titles from arguments or stdin, one slug per line

## Usage

```bash
python slug_generator.py "Hello, World! My First Post"
# hello-world-my-first-post

printf 'Café & Crème\n' | python slug_generator.py
# cafe-creme

python slug_generator.py "One Title" "Second Title Here"
# one-title
# second-title-here
```

## Options

| Flag | What it does |
| --- | --- |
| `-s, --separator SEP` | Separator between words (default: `-`) |
| `-l, --max-length N` | Truncate the slug to at most N characters (never leaves a trailing separator) |
| `--keep-case` | Keep original capitalisation |
| `-h, --help` | Show help and exit |

```bash
python slug_generator.py --separator _ --max-length 20 "A very long title here"
# a_very_long_title_he

python slug_generator.py --keep-case "Hello World"
# Hello-World
```

## Exit codes

- `0` — ok
- `1` — bad usage (bad `--max-length` or `--separator`)
- `2` — empty input

## Requirements

Python 3.8+. Standard library only.
