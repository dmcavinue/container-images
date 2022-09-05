FROM golang:1.17-alpine3.15
WORKDIR /build
COPY . .
RUN GOOS=linux CGO_ENABLED=0 go build -a -ldflags '-s -w -extldflags "-static"' -o tidbyt .

FROM node:18.8.0

ENV PIXLET_VERSION 0.18.2

RUN wget -q https://github.com/tidbyt/pixlet/releases/download/v${PIXLET_VERSION}/pixlet_${PIXLET_VERSION}_linux_amd64.tar.gz -O pixlet_${PIXLET_VERSION}_linux_amd64.tar.gz && \
  tar -xzf pixlet_${PIXLET_VERSION}_linux_amd64.tar.gz pixlet && \
  mv pixlet /usr/local/bin && \
  chmod +x /usr/local/bin/pixlet && \
  rm pixlet_${PIXLET_VERSION}_linux_amd64.tar.gz

RUN apt-get update && apt-get install -y \
  ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=0 /build/tidbyt .
COPY --from=0 /build/templates templates/
CMD ["./tidbyt"]