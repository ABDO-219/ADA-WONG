#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $EUID -ne 0 ]]; then
  sudo bash "$SCRIPT_DIR/install-ada-wing.sh"
  exit $?
fi

cp "$SCRIPT_DIR/ada-wing" /usr/local/bin/ada-wing
chmod +x /usr/local/bin/ada-wing
mkdir -p "$HOME/.local/share/applications"
cp "$SCRIPT_DIR/ada-wing.desktop" "$HOME/.local/share/applications/ada-wing.desktop"
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true

echo "تم تثبيت ADA-WING. يمكنك تشغيله من القائمة أو عبر الأمر ada-wing."