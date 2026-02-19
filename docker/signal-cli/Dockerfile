FROM eclipse-temurin:21-jre-jammy

ARG SIGNAL_CLI_VERSION=0.13.12

RUN apt-get update && apt-get install -y --no-install-recommends wget \
    && wget -q "https://github.com/AsamK/signal-cli/releases/download/v${SIGNAL_CLI_VERSION}/signal-cli-${SIGNAL_CLI_VERSION}-Linux.tar.gz" \
    && tar xf "signal-cli-${SIGNAL_CLI_VERSION}-Linux.tar.gz" -C /opt/ \
    && ln -s "/opt/signal-cli-${SIGNAL_CLI_VERSION}/bin/signal-cli" /usr/local/bin/signal-cli \
    && rm "signal-cli-${SIGNAL_CLI_VERSION}-Linux.tar.gz" \
    && apt-get remove -y wget && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["signal-cli"]
