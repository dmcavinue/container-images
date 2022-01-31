
FROM docker.io/hashicorp/terraform:1.1.4 as terraform

FROM summerwind/actions-runner:latest

# install dependencies
COPY --from=terraform /bin/terraform /usr/local/bin/terraform
