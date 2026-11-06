#!/usr/bin/env python3
"""slug-generator: turn titles and headings into clean URL slugs.

Reads text from command-line arguments or stdin (one title per line) and
prints one slug per line. Accents are stripped, punctuation becomes the
separator, and repeated separators collapse into one.

Examples:
    $ python slug_generator.py "Hello, World! My First Post"
    hello-world-my-first-post

    $ printf 'Café & Crème\n' | python slug_generator.py
    cafe-creme

    $ python slug_generator.py --separator _ --max-length 20 "A very long title here"
    a_very_long_title_he

Usage:
    slug_generator.py [options] [TITLE ...]
    echo "title" | slug_generator.py [options]

Options:
    -s, --separator SEP   Separator between words (default: -)
    -l, --max-length N    Truncate the slug to at most N characters
                          (truncation never leaves a trailing separator)
    --keep-case           Keep original capitalisation (default: lowercase)
    -h, --help            Show this help and exit

Exit codes: 0 = ok, 1 = bad usage, 2 = empty input.
"""

import argparse
import re
import sys
import unicodedata

DEFAULT_SEPARATOR = "-"


def slugify(text, separator=DEFAULT_SEPARATOR, max_length=None, keep_case=False):
    """Convert *text* to a URL slug."""
    if not keep_case:
        text = text.lower()
    # Strip accents: café -> cafe, crême -> creme.
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    # Anything that is not a letter or digit becomes a separator.
    text = re.sub(r"[^a-zA-Z0-9]+", separator, text)
    # Collapse repeats and trim the edges.
    text = re.sub(re.escape(separator) + r"+", separator, text)
    text = text.strip(separator)
    if max_length is not None and len(text) > max_length:
        text = text[:max_length].rstrip(separator)
    return text


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Turn titles into clean URL slugs."
    )
    parser.add_argument("titles", nargs="*", help="Title(s) to slugify.")
    parser.add_argument(
        "-s", "--separator", default=DEFAULT_SEPARATOR,
        help="Separator between words (default: -).",
    )
    parser.add_argument(
        "-l", "--max-length", type=int, default=None,
        help="Truncate the slug to at most N characters.",
    )
    parser.add_argument(
        "--keep-case", action="store_true",
        help="Keep original capitalisation.",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    if args.max_length is not None and args.max_length < 1:
        print("error: --max-length must be at least 1", file=sys.stderr)
        return 1
    if len(args.separator) != 1:
        print("error: --separator must be a single character", file=sys.stderr)
        return 1

    if args.titles:
        lines = args.titles
    else:
        lines = [line.rstrip("\n") for line in sys.stdin]

    lines = [line for line in lines if line.strip()]
    if not lines:
        print("error: no input — pass titles or pipe text on stdin",
              file=sys.stderr)
        return 2

    for line in lines:
        print(slugify(line, args.separator, args.max_length, args.keep_case))
    return 0


if __name__ == "__main__":
    sys.exit(main())
