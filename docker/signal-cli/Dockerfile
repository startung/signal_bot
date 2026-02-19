FROM debian:bookworm-slim

ARG SIGNAL_CLI_VERSION=0.13.24

RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates wget \
    && wget -q "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_CLI_VERSION}/signal-cli-${SIGNAL_CLI_VERSION}-Linux-native.tar.gz" \
    && tar xf "signal-cli-${SIGNAL_CLI_VERSION}-Linux-native.tar.gz" -C /usr/local/bin/ \
    && rm "signal-cli-${SIGNAL_CLI_VERSION}-Linux-native.tar.gz" \
    && apt-get remove -y wget && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["signal-cli"]
