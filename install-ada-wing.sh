#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ $EUID -ne 0 ]]; then
  sudo bash "$SCRIPT_DIR/install-ada-wing.sh"
  exit $?
fi

if command -v apt-get >/dev/null 2>&1; then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y python3-tk
fi

if [[ -n "${SUDO_USER:-}" ]]; then
  TARGET_USER="$SUDO_USER"
  TARGET_HOME="$(getent passwd "$TARGET_USER" | cut -d: -f6)"
else
  TARGET_USER="$(whoami)"
  TARGET_HOME="$HOME"
fi

install -m 755 "$SCRIPT_DIR/ada-wing" /usr/local/bin/ada-wing
install -m 755 "$SCRIPT_DIR/ada-wing-gui.py" /usr/local/bin/ada-wing-gui.py
install -m 755 "$SCRIPT_DIR/ada-wing-gui" /usr/local/bin/ada-wing-gui

mkdir -p "$TARGET_HOME/.local/bin" "$TARGET_HOME/.local/share/applications"
install -m 755 "$SCRIPT_DIR/ada-wing" "$TARGET_HOME/.local/bin/ada-wing"
install -m 755 "$SCRIPT_DIR/ada-wing-gui.py" "$TARGET_HOME/.local/bin/ada-wing-gui.py"
install -m 755 "$SCRIPT_DIR/ada-wing-gui" "$TARGET_HOME/.local/bin/ada-wing-gui"
install -m 644 "$SCRIPT_DIR/ada-wing-gui.desktop" "$TARGET_HOME/.local/share/applications/ada-wing-gui.desktop"
update-desktop-database "$TARGET_HOME/.local/share/applications" 2>/dev/null || true

echo "تم تثبيت ADA-WING والواجهة الرسومية ADA-WING GUI كبرنامج مستقل. يمكنك تشغيل الواجهة من قائمة التطبيقات أو عبر الأمر ada-wing-gui."