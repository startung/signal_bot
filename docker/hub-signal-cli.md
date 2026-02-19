# signal-cli

[signal-cli](https://github.com/AsamK/signal-cli) packaged as a Docker image using the native Linux binary. Intended for use as a sidecar service alongside [Signaalbot](https://hub.docker.com/r/startung/signaalbot), but can also be used standalone.

This image uses the native binary (compiled with GraalVM) so no Java runtime is required.

## Usage with Signaalbot

The easiest way to use this image is via the Signaalbot Docker Compose setup:

```bash
curl -O https://raw.githubusercontent.com/startung/signaalbot/main/docker-compose.yml
```

See the [Signaalbot image](https://hub.docker.com/r/startung/signaalbot) for the full quick-start guide.

## Standalone usage

Register a new number:

```bash
docker run --rm -v signal-data:/root/.local/share/signal-cli startung/signal-cli \
  -a +YOUR_PHONE_NUMBER register
```

Verify:

```bash
docker run --rm -v signal-data:/root/.local/share/signal-cli startung/signal-cli \
  -a +YOUR_PHONE_NUMBER verify 123-456
```

Run as a JSON-RPC daemon:

```bash
docker run -d \
  -v signal-data:/root/.local/share/signal-cli \
  -p 7583:7583 \
  startung/signal-cli \
  -a +YOUR_PHONE_NUMBER daemon --tcp 0.0.0.0:7583
```

## Links

- [signal-cli source](https://github.com/AsamK/signal-cli)
- [Signaalbot source](https://github.com/startung/signaalbot)
- [Signaalbot image](https://hub.docker.com/r/startung/signaalbot)
