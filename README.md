## neo4j_docker

This repository provides a ready-to-use Docker Compose setup for deploying Neo4j, the popular open-source graph database, alongside supporting services such as Flask and Nginx. It is ideal for local development, prototyping, or as a starting point for more complex deployments.

---

## Features

- **Neo4j**: Runs the official Neo4j database in a Docker container.
- **Flask**: Optional backend service for custom APIs or business logic.
- **Nginx**: Optional reverse proxy for serving web content or API endpoints.
- **Docker Compose**: Simplifies multi-container orchestration and networking.

---

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)
- Minimum 4GB RAM recommended

---

## Getting Started

1. **Clone this repository**
   ```bash
   git clone https://github.com/voirinprof/neo4j_docker.git
   cd neo4j_docker
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Access Neo4j Browser**
   - Open your browser and go to: [http://localhost:7474](http://localhost:7474)
   - Default credentials :  
     - Username: `neo4j`  
     - Password: `neo4jpassword`

4. **Access Flask and Nginx (if configured)**
   - Flask: [http://localhost:5000](http://localhost:5000)
   - Nginx: [http://localhost:80](http://localhost:80)

---

## Usage

- **Stopping the environment**
  ```bash
  docker-compose down
  ```

- **Persisting Data**
  - Data is stored in Docker volumes by default. To persist data outside the container, adjust the `volumes` section in `docker-compose.yml` to map to a local directory.

- **Configuration**
  - Modify environment variables in `docker-compose.yml` to customize Neo4j settings (e.g., password, plugins, memory limits)[4][8].

---

## Project Structure

```
neo4j_docker/
│
├── docker-compose.yml   # Main Docker Compose file
├── flask/               # Flask application (optional)
├── nginx/               # Nginx configuration (optional)
├── web/                 # Static web content (optional)
└── README.md            # This file
```

---

## Customization

- **Neo4j Plugins**: To add plugins, mount a local directory to `/plugins` in the Neo4j service and place plugin JARs there[4].
- **Environment Variables**: Set Neo4j configuration options via environment variables in `docker-compose.yml` (e.g., `NEO4J_AUTH`, `NEO4J_dbms_memory_pagecache_size`).
- **Networking**: Adjust ports in `docker-compose.yml` as needed.

---

## Troubleshooting

- **Neo4j not starting**: Ensure no other service is using port 7474 or 7687.
- **Data not persisting**: Check your Docker volume or bind mount configuration.
- **Password issues**: The initial password is set via the `NEO4J_AUTH` environment variable. If you forget it, remove the data volume and restart to reset.

For more information, consult the [official Neo4j Docker documentation][4][8].

---

## License

This project is provided as-is for educational and development use.
