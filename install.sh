#!/usr/bin/env bash
# Install the Czech Coder keyboard layout for the current macOS user.
set -euo pipefail

NAME="Czech Coder"
BUNDLE="$NAME.bundle"
DEST="$HOME/Library/Keyboard Layouts"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ "$(uname)" != "Darwin" ]]; then
  echo "This installer is for macOS. On Linux use: setxkbmap -layout cz -variant coder" >&2
  exit 1
fi

if [[ ! -d "$HERE/$BUNDLE" ]]; then
  echo "Missing $BUNDLE. Run 'make' first (needs python3 and Pillow)." >&2
  exit 1
fi

mkdir -p "$DEST"
rm -rf "$DEST/$BUNDLE"
cp -R "$HERE/$BUNDLE" "$DEST/"
echo "Installed to: $DEST/$BUNDLE"
echo
echo "Next:"
echo "  1. Log out and back in (or restart)."
echo "  2. System Settings > Keyboard > Input Sources > + > Czech > 'Czech Coder'."
echo "  3. Switch to it from the input menu in the menu bar."
