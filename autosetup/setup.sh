#!/bin/bash
#
# Script: setup.sh
# Description: 
#   This script automates the installation of Xcode command-line tools, Homebrew, Python 3, Git, and other usefull things.
#   It also provides options to clone specific Git repositories, install Naisdevice, and install Kubernetes.
#   User confirmation is requested for each installation step.
#
# Preliminaries:
#   - Run 'chmod u+x filename' in your shell to give the user you are on execution priviliges. You of course will need a shell like bash.
#   - For Git cloning, a Python script named "clone.py" is called to perform the cloning operation.
#   - Please ensure that you have the necessary permissions to create and modify files in the relevant directories.
#
# Usage: 
#   sudo ./setup.sh
#   - Follow the prompts to confirm or skip each installation step.
#   - After the script finishes, check the installed software and perform any additional configuration if required.


# Get confirmation from user that the installation is wanted
confirm() {
    read -r -p "$1 [Y/n] " response
    case "$response" in
        [yY][eE][sS]|[yY]|"")
            true
            ;;
        [nN][oO]|[nN])
            false
            ;;
        *)
            false
            ;;
    esac
}

# Install Xcode command-line tools
if confirm "Do you want to install Xcode command-line tools?"; then
    echo "[INFO] Installing Xcode comman-line tools..."
    xcode-select --install 2>/dev/null
    echo "[INFO] Xcode command-line tools installed."
else
    echo "[INFO] NOT installing Xcode command-line tools."
fi

# Install Homebrew
if confirm "Do you want to install Homebrew?"; then
    echo "[INFO] Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    echo "[INFO] Homebrew installed"
    echo "[INFO] Updating Homebrew..."
    brew update
    echo "[INFO] Updated Homebrew."
else
    echo "[INFO] NOT installing Homebrew."
fi

# Install Python 3
if confirm "Do you want to install Python 3?"; then
    echo "[INFO] Installing Python 3..."
    brew install python
    echo "[INFO] Python 3 installed."
else
    echo "[INFO] Skipping Python 3 installation."
fi

# Install Java 11
if confirm "Do you want to install Java 11?"; then
    echo "[INFO] Installing Java 11..."
    brew install java11
    echo "[INFO] Java 11 installed."
    echo "[INFO] Initializing symbol link."
    sudo ln -sfn /usr/local/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
    echo "[INFO] Symbol link initialized."

else
    echo "[INFO] Skipping Java 11 installation."
fi

# Install Git
if confirm "Do you want to install git?"; then
    echo "[INFO] Installing Git..."
    brew install git
    echo "[INFO] Git installed..."
else
    echo "[INFO] Skipping git installation."
fi

# Fetch git repos
if confirm "Do you want to clone all repos belonging to the ISA-team?"; then
    echo "[INFO] Cloning all repos..."
    python3 clone.py
    echo "[INFO] All repos cloned."
else
    echo "[INFO] Skipping cloning of repos"
fi

# Install NAIS
# TODO: Check Naisdevice
echo "[WARN] Not able to check if Naisdevice already exist..."
if confirm "Do you want to install Naisdevice?"; then
    echo "[INFO] Installing Naisdevice..."
    brew tap nais/tap
    brew install Naisdevice
    echo "[INFO] Naisdevice installed."
else
    echo "[INFO] Skipping Naisdevice installation."
fi

# Install Kubernetes
echo "[INFO] Checking Kubernetes..."
if confirm "Do you want to install Kubernetes?"; then
    echo "[INFO] Installing Kubernetes..."
    brew install kubectl
    echo "[INFO] Kubernetes installed."
else
    echo "[INFO] Skipping Kubernetes installation."
fi

# Add .bashrc file 
echo "[INFO] Checking .bashrc..."
./setup_bashrc.sh
