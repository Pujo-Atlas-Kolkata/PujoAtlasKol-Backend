
# PujoAtlasKol-Backend
<p>
<img src="public/file-type-node.svg" height="50px" width="50px" alt="Node Icon"/>
</p>
<p>
<img src="public/file-type-typescript-official.svg" height="50px" width="50px" alt="TS Icon"/>
</p>
<p>
<img src="https://nestjs.com/img/logo-small.svg" width="50px" height="50px" alt="Nest Logo" />
</p>
          
Welcome to Pujo Atlas - your ultimate guide for Pandal Hopping during Durga Puja in Kolkata! This open-source project aims to provide a comprehensive and user-friendly webapp that lists all the Durga Pujas happening around Kolkata and offers a host of features to make your pandal hopping experience seamless and enjoyable.

## Prerequisites
- **Node.js** version 20 or higher is required.

## Setup Instructions

_Some commands will assume you have the Github CLI installed, if you haven't, consider [installing it](https://github.com/cli/cli#installation), but you can always use the Web UI if you prefer that instead._

1. **Fork the repository**
   Do make sure that the branch node-implementation comes with your [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)

```bash
gh repo fork Pujo-Atlas-Kolkata/PujoAtlasKol-Backend
```

2. **Clone the Git Repository**:
   ```bash
   git clone https://github.com/Pujo-Atlas-Kolkata/PujoAtlasKol-Backend.git
   cd PujoAtlasKol-Backend
   ```

3. **Checkout to the `node-implementation` branch**:
   ```bash
   git checkout node-implementation
   ```

4. **Setup `.env.development` File**:
   Create a `.env.development` file in the root of your project and add the following environment variables:

   ```env
   DJANGO_DB_NAME=PujoAtlasDb
   DJANGO_DB_USER=PujoAtlasDb_owner
   DJANGO_DB_PASSWORD=I1*******0aC # contact in discord for actual password
   DJANGO_DB_HOST=ep-tight-frost-a1w3l3i2.ap-southeast-1.aws.neon.tech
   DJANGO_DB_PORT=5432
   DJANGO_DB_SYNC_MODE=dev
   SSL_MODE=true
   ```

5. **Run Setup Script**:
   Depending on your operating system, run the appropriate setup script to install dependencies and start the development server.

   ### For Unix/Linux/macOS Users:
   - Make the `setup.sh` script executable:
     ```bash
     chmod +x setup.sh
     ```
   - Run the setup script:
     ```bash
     ./setup.sh
     ```

   ### For Windows Users:
   - Run the PowerShell script:
     ```powershell
     ./setup.ps1
     ```

## What This Setup Will Do:
- The setup script will check for the Node.js version (must be 20 or higher).
- It will install the NestJS CLI globally if it isn't already installed.
- It checks for the existence of the `.env.development` file and ensures the necessary environment variables are set.
- It installs the required dependencies (`npm install`) and starts the NestJS development server (`npm run start:dev`).

## Notes
- Ensure you have the correct permissions to run scripts on your machine.
- If you encounter any issues during the setup process, verify that Node.js version 20 or higher is installed and that your `.env.development` file contains the correct values.



### Key Elements of the README:
1. **Prerequisites**: Clearly state the required Node.js version.
2. **Setup Instructions**: Include all steps for cloning, checking out to the correct branch, and setting up environment variables.
3. **Platform-Specific Setup**: Instructions for Unix-based systems and Windows, including the necessary commands for making the script executable and running it.
4. **What the Script Does**: Describes the process that will be automated by the script.
5. **Best Practice**: Ensure the user sets up the `.env.development` correctly and provides instructions in an easily readable format.

This `README.md` should provide all necessary information for users to successfully set up and run the development server on any supported operating system.
