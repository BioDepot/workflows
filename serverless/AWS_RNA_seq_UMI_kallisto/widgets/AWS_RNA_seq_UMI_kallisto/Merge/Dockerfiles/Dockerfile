FROM ubuntu:20.04
RUN apt-get update && apt-get install -y nano bash libboost-filesystem-dev
COPY w384/ /384/
COPY w96/ /96/
ADD start.sh /usr/local/bin/start.sh
ENV NWELLS 96
ENTRYPOINT ["start.sh"]
