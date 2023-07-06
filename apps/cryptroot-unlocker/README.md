Polls a provided ssh host/port and attempts a cryptroot unlock

example usage::
```bash
docker run --rm -it \
  -e SSH_HOST=192.168.0.1 \
  -e SSH_PORT=2222 \
  -e CRYPTKEY="xxxxxx" \
  -v <SSH_KEY>:/home/unlocker/.ssh/id_rsa \
  -v ~/.ssh/known_hosts:/home/unlocker/.ssh/known_hosts \
  -u 1000:1000 \
  dmcavinue/cryptroot-unlocker
```