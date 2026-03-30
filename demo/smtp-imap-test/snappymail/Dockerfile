FROM djmaze/snappymail:latest

COPY test.local.json /snappymail-config/test.local.json
COPY entrypoint-wrapper.sh /entrypoint-wrapper.sh

ENTRYPOINT ["/entrypoint-wrapper.sh"]
