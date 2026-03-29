#!/usr/bin/env bash
set -euo pipefail

BOOTSTRAP_URL="${BOOTSTRAP_URL:-https://evanbei.com/.well-known/node-bootstrap.json}"
NODE_NAME="${1:-${NODE_NAME:-}}"
INSTALL_DIR="${INSTALL_DIR:-/opt/aiorigins}"
STATE_DIR="${STATE_DIR:-/var/lib/aiorigins}"
LOG_FILE="${LOG_FILE:-/tmp/aiorigins-boot.log}"

log() {
  echo "[AI Origins Boot] $*" | tee -a "$LOG_FILE"
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    log "Missing command: $1"
    exit 1
  }
}

pick_fetcher() {
  if command -v curl >/dev/null 2>&1; then
    FETCHER="curl -fsSL"
  elif command -v wget >/dev/null 2>&1; then
    FETCHER="wget -qO-"
  else
    log "Need curl or wget"
    exit 1
  fi
}

ensure_dirs() {
  sudo mkdir -p "$INSTALL_DIR" "$STATE_DIR"
  sudo chown "$(id -u)":"$(id -g)" "$INSTALL_DIR" "$STATE_DIR"
}

pick_node_name() {
  if [ -n "$NODE_NAME" ]; then
    echo "$NODE_NAME"
    return
  fi

  if [ -n "${HOSTNAME:-}" ]; then
    echo "$HOSTNAME"
    return
  fi

  echo "node-$(date +%s)"
}

parse_json_field() {
  python3 -c 'import json,sys; data=json.load(sys.stdin); v=data.get(sys.argv[1], ""); print(json.dumps(v, ensure_ascii=False) if isinstance(v,(dict,list)) else v)' "$1"
}

main() {
  : > "$LOG_FILE"

  require_cmd bash
  require_cmd sudo
  require_cmd python3
  require_cmd uname
  require_cmd hostname
  pick_fetcher

  log "Starting one-command enrollment"
  log "Bootstrap URL: $BOOTSTRAP_URL"

  if ! ping -c 1 -W 2 1.1.1.1 >/dev/null 2>&1 && ! ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1; then
    log "Network check failed"
    exit 1
  fi
  log "Network OK"

  ensure_dirs

  TMP_BOOT="$(mktemp)"
  eval "$FETCHER \"$BOOTSTRAP_URL\"" > "$TMP_BOOT"
  log "Bootstrap downloaded"

  CORE_URL="$(cat "$TMP_BOOT" | parse_json_field core_url)"
  JOIN_URL="$(cat "$TMP_BOOT" | parse_json_field join_url)"
  DISPLAY_URL="$(cat "$TMP_BOOT" | parse_json_field display_url)"
  WG_ENABLED="$(cat "$TMP_BOOT" | parse_json_field wireguard_enabled)"
  VERSION="$(cat "$TMP_BOOT" | parse_json_field version)"

  NODE_NAME="$(pick_node_name)"
  ARCH="$(uname -m)"
  HOST="$(hostname)"

  log "Bootstrap version: ${VERSION:-unknown}"
  log "Node name: $NODE_NAME"
  log "Host: $HOST"
  log "Arch: $ARCH"

  cat > "$INSTALL_DIR/node.env" <<EOF
NODE_NAME=$NODE_NAME
HOSTNAME=$HOST
ARCH=$ARCH
BOOTSTRAP_URL=$BOOTSTRAP_URL
CORE_URL=$CORE_URL
JOIN_URL=$JOIN_URL
DISPLAY_URL=$DISPLAY_URL
WIREGUARD_ENABLED=$WG_ENABLED
INSTALLED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

  if [ -n "$JOIN_URL" ]; then
    TMP_JOIN="$(mktemp)"
    JSON_PAYLOAD=$(printf '{"node_name":"%s","hostname":"%s","arch":"%s"}' "$NODE_NAME" "$HOST" "$ARCH")

    if command -v curl >/dev/null 2>&1; then
      curl -fsSL -X POST "$JOIN_URL"         -H "Content-Type: application/json"         -d "$JSON_PAYLOAD" > "$TMP_JOIN" || true
    else
      wget -qO-         --header="Content-Type: application/json"         --post-data="$JSON_PAYLOAD"         "$JOIN_URL" > "$TMP_JOIN" || true
    fi

    if [ -s "$TMP_JOIN" ]; then
      cp "$TMP_JOIN" "$INSTALL_DIR/join-response.json"
      JOIN_NODE_ID="$(cat "$TMP_JOIN" | parse_json_field node_id || true)"
      [ -n "$JOIN_NODE_ID" ] && log "Assigned node_id: $JOIN_NODE_ID"
    else
      log "Join endpoint returned no data, continuing"
    fi
  else
    log "No join_url in bootstrap, skipping registration"
  fi

  cat > "$INSTALL_DIR/README.txt" <<EOF
AI Origins node enrollment completed.

Node name: $NODE_NAME
Core URL: ${CORE_URL:-not set}
Display URL: ${DISPLAY_URL:-not set}
WireGuard enabled: ${WG_ENABLED:-false}

Main files:
- $INSTALL_DIR/node.env
- $INSTALL_DIR/join-response.json (if returned)
- $LOG_FILE

Next step:
- WireGuard / agent / display can be layered in later
EOF

  echo "online" > "$STATE_DIR/status"
  date -u +"%Y-%m-%dT%H:%M:%SZ" > "$STATE_DIR/installed_at"

  log "Enrollment complete"
  log "Status file: $STATE_DIR/status"
  [ -n "$DISPLAY_URL" ] && log "Display URL: $DISPLAY_URL"

  echo
  echo "AI Origins node is enrolled."
  echo "Node: $NODE_NAME"
  [ -n "$DISPLAY_URL" ] && echo "Display: $DISPLAY_URL"
  echo "Done."
}

main "$@"
