#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $EUID -ne 0 ]]; then
  sudo bash "$SCRIPT_DIR/install-ada-wing.sh"
  exit $?
fi

cp "$SCRIPT_DIR/ada-wing" /usr/local/bin/ada-wing
chmod +x /usr/local/bin/ada-wing
cp "$SCRIPT_DIR/ada-wing-gui.py" /usr/local/bin/ada-wing-gui.py
chmod +x /usr/local/bin/ada-wing-gui.py
cp "$SCRIPT_DIR/ada-wing-gui" /usr/local/bin/ada-wing-gui
chmod +x /usr/local/bin/ada-wing-gui
mkdir -p "$HOME/.local/share/applications"
cp "$SCRIPT_DIR/ada-wing-gui.desktop" "$HOME/.local/share/applications/ada-wing-gui.desktop"
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true

echo "تم تثبيت ADA-WING والواجهة الرسومية ADA-WING GUI كبرنامج مستقل. يمكنك تشغيل الواجهة من قائمة التطبيقات أو عبر الأمر ada-wing-gui."