FROM excalidraw/excalidraw:latest as build

FROM nginxinc/nginx-unprivileged:1.25.3-alpine

COPY --from=build /usr/share/nginx/html /usr/share/nginx/html
