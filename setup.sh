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
#   ./setup.sh
#   - Follow the prompts to confirm or skip each installation step.
#   -After the script finishes, check the installed software and perform any additional configuration if required.


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
echo "Checking Xcode command-line tools..."
if ! command -v git &>/dev/null; then
    echo "Xcode command-line tools not found."
    echo "Installing Xcode comman-line tools..."
    xcode-select --install 2>/dev/null
    echo "Xcode command-line tools installed."
else
    echo "Xcode command-line tools are already installed."
fi
echo ""

# Install Homebrew
echo "Checking Homebrew..."
if ! command -v brew &>/dev/null; then
    echo "Homebrew not found"
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew is already installed."
fi
echo ""

# Install Python 3
echo "Checking Python 3..."
if ! command -v python3 &>/dev/null; then
    echo "Python 3 not found."
    echo "Installing Python 3..."
    brew install python
    echo "Python 3 installed."
else
    echo "Python 3 is already installed."
fi

# Install Git
echo "Checking Git..."
xcode-select --install 2>/dev/null
if ! command -v git &>/dev/null; then
    echo "Git not found."
    echo "Installing Git..."
    brew install git
else
    echo "Git is already installed."
fi
echo ""

# Fetch git repos
if confirm "Do you want to clone all repos belonging to the ISA-team?"; then
    echo "Cloning all repos..."
    python3 clone.py
    echo "All repos cloned."
else
    echo "Skipping cloning of repos"
fi
echo ""

# Install NAIS
# TODO: Check Naisdevice
echo "Not able to check if Naisdevice already exist..."
if confirm "Do you want to install Naisdevice?"; then
    echo "Installing Naisdevice..."
    brew tap nais/tap
    brew install Naisdevice
    echo "Naisdevice installed."
else
    echo "Skipping Naisdevice installation."
fi
echo ""

# Install Kubernetes
echo "Checking Kubernetes..."
if ! command -v kubectl &>/dev/null; then
    echo "Kubernetes not found."
    if confirm "Do you want to install Kubernetes?"; then
        echo "Installing Kubernetes..."
        brew install kubectl
        echo "Kubernetes installed."
    else
        echo "Skipping Kubernetes installation."
        echo ""
        exit 0
    fi
else
    echo "Kubernetes is already installed."
fi
echo ""

# Add .bashrc file 
echo "Checking .bashrc..."
source setup_bashrc.sh
