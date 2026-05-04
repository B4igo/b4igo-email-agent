FROM alpine:3.19

RUN apk add --no-cache curl jq

COPY bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh

CMD ["/bootstrap.sh"]
