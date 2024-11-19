# Network Monitor

This project is a network monitoring tool that listens to network traffic and monitors log files. It is built using Python and Docker.

## Project Structure

```
.gitignore
docker-compose.yml
Dockerfile
logs/
    data.log
README.md
requirements.txt
src/
    config/
        env.py
        logger.py
    log_monitor/
        monitor.py
    main.py
    network/
        listener.py
```

- `docker-compose.yml`: Docker Compose configuration file.
- `Dockerfile`: Dockerfile to build the Docker image.
- `logs/`: Directory to store log files.
- `requirements.txt`: Python dependencies.
- `src/`: Source code directory.
  - `config/`: Configuration files.
    - `env.py`: Environment variables configuration.
    - `logger.py`: Logging configuration.
  - `log_monitor/`: Log monitoring module.
    - `monitor.py`: Log monitoring script.
  - `main.py`: Main entry point of the application.
  - `network/`: Network listener module.
    - `listener.py`: Network listener script.

## Prerequisites

- Docker
- Docker Compose

## Build the Docker Image

To build the Docker image, run the following command:

```sh
docker build -t network_monitor:1.0.0 .
```

## Run the Docker Container

To run the Docker container, use Docker Compose:

```sh
docker-compose up -d
```

This will start the `network_monitor` container in detached mode.

## Environment Variables

The following environment variables are used in the project:

- `PORTS`: Ports to listen to (default: `5432`).
- `LOG_PATH`: Path to the log file (default: `/app/logs/data.log`).

These variables are set in the `docker-compose.yml` file.

## Logging

Logging is configured in the [`src/config/logger.py`](src/config/logger.py) file. The logger outputs logs to the console with the following format:

```
%(asctime)s | %(levelname)s | %(message)s
```

## Main Components

### Main Script

The main script is located in [`src/main.py`](src/main.py). It starts two processes:

- `network_listener`: Listens to network traffic.
- `monitor_logfile`: Monitors the log file.

### Network Listener

The network listener is implemented in [`src/network/listener.py`](src/network/listener.py). It listens to network traffic on the specified ports.

### Log Monitor

The log monitor is implemented in [`src/log_monitor/monitor.py`](src/log_monitor/monitor.py). It monitors the log file for changes.

## Development

To set up the development environment, follow these steps:

1. Clone the repository:

```sh
git clone https://github.com/idris-adigun/streaming-analysis/
```

2. Navigate to the project directory:

```sh
cd streaming-analysis
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```

4. Run the application:

```sh
python3 src/main.py
```
