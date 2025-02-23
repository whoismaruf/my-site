FROM ubuntu:latest
LABEL authors="maruf"

ENTRYPOINT ["top", "-b"]