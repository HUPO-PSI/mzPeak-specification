#!/usr/bin/env bash
# Convert one or more .drawio files to SVG using the draw.io desktop CLI.
#
# Usage: scripts/drawio2svg.sh [-e] [-b BORDER] FILE.drawio [FILE2.drawio ...]
#   -e         embed the diagram source in the SVG so it stays editable in draw.io
#   -b BORDER  border around the diagram in pixels (default: 0)
#
# Output is written next to each input as FILE.svg.
# Set DRAWIO to the draw.io executable if it is not found automatically.
set -euo pipefail

embed=()
border=0
while getopts "eb:h" opt; do
    case "$opt" in
        e) embed=(--embed-diagram) ;;
        b) border="$OPTARG" ;;
        h|*) sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
    esac
done
shift $((OPTIND - 1))

if [ $# -eq 0 ]; then
    echo "error: no input files" >&2
    exit 1
fi

find_drawio() {
    if [ -n "${DRAWIO:-}" ]; then echo "$DRAWIO"; return; fi
    local c
    for c in drawio draw.io \
        "/c/Program Files/draw.io/draw.io.exe" \
        "$LOCALAPPDATA/Programs/draw.io/draw.io.exe" \
        "/Applications/draw.io.app/Contents/MacOS/draw.io"; do
        if command -v "$c" >/dev/null 2>&1 || [ -x "$c" ]; then
            echo "$c"; return
        fi
    done
    return 1
}

bin=$(find_drawio) || { echo "error: draw.io not found; set DRAWIO=/path/to/draw.io" >&2; exit 1; }

status=0
for in in "$@"; do
    if [ ! -f "$in" ]; then
        echo "skip: $in not found" >&2
        status=1
        continue
    fi
    out="${in%.drawio}.svg"
    if "$bin" --export --format svg --border "$border" "${embed[@]}" --output "$out" "$in"; then
        echo "wrote $out"
    else
        echo "failed: $in" >&2
        status=1
    fi
done
exit $status
