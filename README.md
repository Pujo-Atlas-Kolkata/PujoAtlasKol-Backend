
# Project Setup and Running Guide

This guide will walk you through the steps required to set up and run the project using Taskfile. Make sure you have all the prerequisites installed before proceeding.

## Prerequisites

Before you start, ensure that the following software is installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python](https://www.python.org/downloads/)
- [Node.js and npm](https://nodejs.org/)

You can check if these tools are installed by running the following commands:

```sh
docker --version
docker-compose --version
python --version
node --version
npm --version
```

## Setup

This project uses a `Tasksfile.yml` to automate the setup process. You need to install Task (task runner for Go) before proceeding:

- Installation instructions for Task can be found [here](https://taskfile.dev/#/installation).

Once Task is installed, you can proceed with the setup.

### Steps to Set Up

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Run the setup task:

   ```sh
   task setup
   ```

   This command will:

   - Check that all prerequisites are installed.
   - Ensure Docker is running.
   - Start the required services using Docker Compose.
   - Create a Python virtual environment.
   - Activate the virtual environment and install the necessary Python dependencies.
   - Run database migrations.
   - Set up the `node-cron` service.

3. Run the Application:
    ```sh
    python manage.py runserver
    ```
### Manual Setup (Optional)

If you want to perform each step manually, follow these commands:

1. **Check Prerequisites** (as described in the prerequisites section above).

2. **Start Docker Services**:

   ```sh
   docker-compose up -d
   ```

3. **Create a Virtual Environment**:

   ```sh
   python -m venv venv
   ```

4. **Activate the Virtual Environment**:

   - On Windows:

     ```sh
     venv\Scripts\activate
     ```

   - On Linux/macOS:

     ```sh
     source venv/bin/activate
     ```

5. **Install Python Dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

6. **Run Database Migrations**:

   ```sh
   python manage.py migrate
   ```

6. **Run Django Server**:

    ```sh
    python manage.py runserver
    ```

8. **Set Up `node-cron`**:

   ```sh
   cd node-cron
   npm install
   nohup node index.js &
   ```

   This will install the Node.js dependencies and start the cron job in the background.

## Running the Project

After completing the setup steps, the services should be up and running.

- To check if the backend is running properly, you can access it on the designated URL (e.g., `http://localhost:8000` for Django).
- To stop the Docker services:

  ```sh
  docker-compose down
  ```

## Troubleshooting

- **Docker Not Running**: Ensure Docker is running before starting the setup.
- **Virtual Environment Issues**: If you encounter issues activating the virtual environment, make sure you are using the correct command for your OS.
- **Port Conflicts**: If any port conflicts occur, make sure no other services are running on the required ports.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contributing

Feel free to submit issues and pull requests. Contributions are welcome!

