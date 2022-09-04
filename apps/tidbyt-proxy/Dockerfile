FROM golang:1.17-alpine3.15
WORKDIR /build
COPY . .
RUN GOOS=linux CGO_ENABLED=0 go build -a -ldflags '-s -w -extldflags "-static"' -o app .

FROM alpine:3.15
RUN apk --no-cache add ca-certificates
WORKDIR /app
COPY --from=0 /build/app .
CMD ["./app"]