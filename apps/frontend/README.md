## Running with Docker

You can run this project in a production-ready container using Docker and Docker Compose. The provided `Dockerfile` builds and optimizes the Next.js app, and the `docker-compose.yml` makes it easy to start the service.

### Requirements
- Docker (latest)
- Docker Compose (v2 or later)
- Node.js version used in the image: `22.13.1-slim` (handled by the Dockerfile)

### Environment Variables
- The app supports environment variables via `.env.local` or `.env.example`. Uncomment the `env_file` line in `docker-compose.yml` if you want to use a custom environment file.

### Build and Run

From the project root, build and start the app:

```bash
# Build and start the app
docker compose up --build
```

The app will be available at [http://localhost:3000](http://localhost:3000).

### Ports
- `3000` (Next.js default) is exposed and mapped to your local machine.

### Notes
- No external services (like databases) are required by default.
- The container runs as a non-root user for improved security.
- Healthchecks are configured for the `/health` endpoint (adjust if needed).

For custom configuration, review the `Dockerfile` and `docker-compose.yml` for additional options.
