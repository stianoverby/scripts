#!/bin/bash
#
# Script: 
#    setup_bashrc.sh
#
# Description: 
#   This script creates a .bashrc2 file with custom aliases and environment variable configuration.
#    It checks if a kubeconfig file exists in the current directory and sets the KUBE_CONFIG environment variable accordingly.
#
# Preliminaries:
#   - Run 'chmod u+x filename' in your shell to give the user you are on execution priviliges. You of course will need a shell like bash.
#   - Before running the script, ensure that the kubeconfig file is present in the current directory.
#   - Please ensure that you have the necessary permissions to create and modify files in the relevant directories.
#
# Usage:
#   ./setup_bashrc.sh
#   

# Define the content of the .bashrc file
BASHRC_CONTENT='
# Aliases
alias ll="ls -al"
alias grep="grep --color=auto"
# Exports
'

# Check if .bashrc already exists
if [[ -e ~/.bashrc ]]; then
    echo "[INFO] .bashrc file already exists."
    exit 1
fi

echo "[INFO] Creating .bashrc file..."

# Check if kubeconfig file exists in the current directory
if [[ -e kubeconfigs/config ]]; then
    kubeconfig_path="$(pwd)/kubeconfigs/config"
    BASHRC_CONTENT+="
# Set KUBE_CONFIG environment variable
export KUBE_CONFIG=\"$kubeconfig_path\"
"
    echo "[INFO] KUBE_CONFIG environment variable set to: $kubeconfig_path"
else 
    echo "[INFO] kubeconfig file not found in the current directory."
fi

# Push content to .bashrc file
echo "$BASHRC_CONTENT" > ~/.bashrc
echo "[INFO] .bashrc file created."

# Source the .bashrc file to apply changes
source ~/.bashrc

echo "[INFO] Script completed."
