# Function to check for Node.js version
function Check-NodeVersion {
    $nodeVersion = (node -v) -replace 'v', ''
    $majorVersion = $nodeVersion.Split('.')[0]
    
    if ($majorVersion -lt 20) {
        Write-Host "Error: Node.js version is less than 20. Please update Node.js to version 20 or higher." -ForegroundColor Red
        exit 1
    } else {
        Write-Host "Node.js version is $majorVersion"
    }
}

# Function to install NestJS CLI globally
function Install-NestCli {
    if (-not (Get-Command nest -ErrorAction SilentlyContinue)) {
        Write-Host "Nest CLI is not installed. Installing Nest CLI globally..."
        npm install -g @nestjs/cli
    } else {
        Write-Host "Nest CLI is already installed."
    }
}

# Function to check for .env.development file
function Check-EnvFile {
    if (-not (Test-Path ".env.development")) {
        Write-Host "Error: .env.development file not found!" -ForegroundColor Red
        exit 1
    } else {
        Write-Host ".env.development file found."
    }
}

# Function to install npm dependencies and run development server
function Run-NpmCommands {
    Write-Host "Installing npm dependencies..."
    npm install
    
    Write-Host "Starting development server..."
    npm run start:dev
}

# Main script execution
Check-NodeVersion
Install-NestCli
Check-EnvFile
Run-NpmCommands
