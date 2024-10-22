#!/bin/bash

# Function to check for Node.js version
check_node_version() {
  NODE_VERSION=$(node -v | cut -d'.' -f1 | sed 's/v//')
  if [ "$NODE_VERSION" -lt 20 ]; then
    echo "Error: Node.js version is less than 20. Please update Node.js to version 20 or higher."
    exit 1
  else
    echo "Node.js version is $NODE_VERSION"
  fi
}

# Function to install NestJS CLI globally
install_nest_cli() {
  if ! command -v nest &> /dev/null
  then
    echo "Nest CLI is not installed. Installing Nest CLI globally..."
    npm install -g @nestjs/cli
  else
    echo "Nest CLI is already installed."
  fi
}

# Function to check for .env.development file
check_env_file() {
  if [ ! -f ".env.development" ]; then
    echo "Error: .env.development file not found!"
    exit 1
  else
    echo ".env.development file found."
  fi
}

# Function to install npm dependencies and run development server
run_npm_commands() {
  echo "Installing npm dependencies..."
  npm install
  
  echo "Starting development server..."
  npm run start:dev
}

# Main script execution
check_node_version
install_nest_cli
check_env_file
run_npm_commands
