FROM openjdk:20-slim

RUN groupadd --gid 1000 jdk \
    && useradd --uid 1000 --gid jdk --create-home jdk

RUN chown -R jdk:jdk /opt
RUN mkdir /logs && chown -R jdk:jdk /logs