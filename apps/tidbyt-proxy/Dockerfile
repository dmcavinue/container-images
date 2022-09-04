FROM golang:1.17-alpine3.15
WORKDIR /build
COPY . .
RUN GOOS=linux CGO_ENABLED=0 go build -a -ldflags '-s -w -extldflags "-static"' -o app .

FROM alpine:3.15

ENV PIXLET_VERSION 0.18.2

RUN wget -q https://github.com/tidbyt/pixlet/releases/download/v${PIXLET_VERSION}/pixlet_${PIXLET_VERSION}_linux_amd64.tar.gz -O pixlet_${PIXLET_VERSION}_linux_amd64.tar.gz && \
  tar -xzf pixlet_${PIXLET_VERSION}_linux_amd64.tar.gz pixlet && \
  mv pixlet /usr/local/bin && \
  chmod +x /usr/local/bin/pixlet && \
  rm pixlet_${PIXLET_VERSION}_linux_amd64.tar.gz

RUN apk --no-cache add ca-certificates
WORKDIR /app
COPY --from=0 /build/app .
COPY --from=0 /build/templates templates/
CMD ["./app"]