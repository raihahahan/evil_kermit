#!/bin/bash

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Installing..."
    # Install git based on the package manager
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y git
    elif command -v yum &> /dev/null; then
        sudo yum install -y git
    elif command -v brew &> /dev/null; then
        brew install git
    else
        echo "Unsupported package manager. Please install git manually and run the script again."
        exit 1
    fi
fi

# Install prerequisites based on the package manager
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y libreadline-dev libconfig-dev libssl-dev lua5.2 liblua5.2-dev libevent-dev libjansson-dev libpython-dev
elif command -v yum &> /dev/null; then
    sudo yum install -y readline-devel libconfig-devel openssl-devel lua-devel lua-static libevent-devel jansson-devel python3
elif command -v brew &> /dev/null; then
    brew install readline libconfig openssl lua libevent jansson python
else
    echo "Unsupported package manager. Please install the prerequisites manually and run the script again."
    exit 1
fi

# Clone the Telegram CLI repository
git clone --recursive https://github.com/vysheng/tg.git
cd tg

# Build Telegram CLI
./configure
make

# Optionally move telegram-cli to a directory in your PATH
sudo mv ./bin/telegram-cli /usr/local/bin/

echo "Telegram CLI has been installed successfully. You can now run 'telegram-cli' to start it."
