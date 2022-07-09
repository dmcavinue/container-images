FROM openjdk:20-slim
RUN addgroup --system --gid 1001 jdk
RUN adduser --system --uid 1001 --group jdk
RUN chown -R jdk:jdk /opt
RUN mkdir /logs && chown -R jdk:jdk /logs