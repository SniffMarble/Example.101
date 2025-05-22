#!/usr/bin/env bash
set -euo pipefail

# 1. Add and configure GitHub CLI repo/key
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) \
    signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] \
    https://cli.github.com/packages stable main" \
  | sudo tee /etc/apt/sources.list.d/github-cli.list >/dev/null

# 2. Update and install gh
sudo apt update
sudo apt install -y gh

# 3. Authenticate GitHub CLI (interactive)
gh auth login --with-web

# 4. Install correct Tabby (AMD64)
ARCH=$(dpkg --print-architecture)
if [[ "$ARCH" != "amd64" ]]; then
  echo "Expected amd64 but got $ARCH" >&2
  exit 1
fi
# Fetch latest AMD64 .deb via GitHub API
RELEASE_JSON=$(curl -fsSL https://api.github.com/repos/Eugeny/tabby/releases/latest)
DEB_URL=$(echo "$RELEASE_JSON" \
  | grep -Eo 'https://[^"]+tabby-[^"]+-linux-amd64\.deb' \
  | head -n1)
wget -O tabby.deb "$DEB_URL"
sudo dpkg -i tabby.deb || sudo apt -f install -y
rm tabby.deb

# 5. Install Wave Terminal (AMD64 .deb)
WAVE_URL="https://releases.warp.dev/linux/deb/warp-terminal_latest_amd64.deb"
wget -O wave.deb "$WAVE_URL"
sudo dpkg -i wave.deb || sudo apt -f install -y
rm wave.deb

# 6. Set up Python venv for project dependencies
PY_VENV_DIR="$HOME/venvs/dev"
python3 -m venv "$PY_VENV_DIR"
# shellcheck disable=SC1090
source "$PY_VENV_DIR/bin/activate"
pip install --upgrade pip
pip install colorama progress matplotlib opencv-python numpy \
  python-dotenv pandas PySide6 toml vtk pyserial pyperclip pygame notify-py

# 7. Optional: install flatpak support for GUI apps
sudo apt install -y flatpak gnome-software-plugin-flatpak
flatpak remote-add --if-not-exists flathub \
  https://dl.flathub.org/repo/flathub.flatpakrepo

echo "✅ All tools installed and configured successfully!"
