#!/usr/bin/env bash
# Assemble "Czech Coder.bundle" from the generated keylayout + icon + Info.plist.
# A bundle (not a loose .keylayout) is required so macOS lists the layout under
# the Czech language group and shows the menu-bar icon.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

NAME="Czech Coder"
BUNDLE="$NAME.bundle"
BADGE="${BADGE:-CZ}"
RES="$BUNDLE/Contents/Resources"

rm -rf "$BUNDLE"
mkdir -p "$RES"
python3 src/gen_keylayout.py "$RES/$NAME.keylayout"
python3 src/gen_icon.py "$BADGE" "$RES/$NAME.icns"
cp src/Info.plist "$BUNDLE/Contents/Info.plist"
echo "built $BUNDLE (badge: $BADGE)"
