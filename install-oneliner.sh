#!/bin/bash
# One-liner installer for thefuck + MY/EN extra triggers
# (babi batak jimbet anjir kimak puki pantat shit damn wtf).
#
# Usage (fresh PC):
#   curl -sSL https://raw.githubusercontent.com/9M2PJU/thefuck/master/install-oneliner.sh | bash
# Then restart shell (or `source ~/.bashrc`) and type e.g. `git brnch` -> `babi`.
set -e
REPO_URL="${THEFUCK_REPO_URL:-https://github.com/9M2PJU/thefuck.git}"
DEST="${THEFUCK_DIR:-$HOME/thefuck}"
BIN="$HOME/.local/bin/thefuck"

if [ ! -d "$DEST/.git" ]; then
  echo "Cloning $REPO_URL -> $DEST"
  git clone --depth 1 "$REPO_URL" "$DEST"
else
  echo "Updating $DEST"
  git -C "$DEST" pull --ff-only || true
fi

echo "Installing runtime deps"
pip install --break-system-packages -q colorama six psutil decorator pyte 2>/dev/null \
  || pip install -q colorama six psutil decorator pyte

mkdir -p "$HOME/.local/bin"
cat > "$BIN" <<EOF
#!/bin/bash
exec python3 -c "import sys; sys.path.insert(0, '$DEST'); from thefuck.entrypoints.main import main; sys.argv=['thefuck']+sys.argv[1:]; main()" "\$@"
EOF
chmod +x "$BIN"
echo "Installed $BIN"
echo "Version: $($BIN --version 2>&1 || true)"

# Pick rc file for current shell
RC=""
case "${SHELL:-/bin/bash}" in
  *zsh) RC="$HOME/.zshrc" ;;
  *fish) RC="$HOME/.config/fish/config.fish" ;;
  *) RC="$HOME/.bashrc" ;;
esac
LINE='eval "$(thefuck --alias)"'
if [ -f "$RC" ] && grep -qF "$LINE" "$RC"; then
  echo "Alias already in $RC"
else
  echo "$LINE" >> "$RC"
  echo "Added '$LINE' to $RC"
fi
echo "Done. Restart shell or run: source $RC"
