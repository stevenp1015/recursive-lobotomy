#!/bin/bash
# LINK_XITTER.SH - Broadcast Linker for RecursiveLobotomy
# This script will set up the official X-CLI credentials for the agent.

CONFIG_DIR="$HOME/.config/x-cli"
ENV_FILE="$CONFIG_DIR/.env"

mkdir -p "$CONFIG_DIR"

echo "--- XITTER BROADCAST LINKER ---"
echo "You need 5 secrets from https://developer.x.com/en/portal/dashboard"
echo ""

read -p "Enter X_API_KEY: " API_KEY
read -p "Enter X_API_SECRET: " API_SECRET
read -p "Enter X_BEARER_TOKEN: " BEARER
read -p "Enter X_ACCESS_TOKEN: " ACCESS
read -p "Enter X_ACCESS_TOKEN_SECRET: " ACCESS_SECRET

cat > "$ENV_FILE" <<EOF
X_API_KEY=$API_KEY
X_API_SECRET=$API_SECRET
X_BEARER_TOKEN=$BEARER
X_ACCESS_TOKEN=$ACCESS
X_ACCESS_TOKEN_SECRET=$ACCESS_SECRET
EOF

chmod 600 "$ENV_FILE"

echo ""
echo "Broadcast Linker Successful. Permissions restricted to 600."
echo "Testing connection..."
x-cli me mentions --max 1
