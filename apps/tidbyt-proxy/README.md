

Copy `.env.example` and fill in your tidbyt api key and device id into the respective env vars.

`./templates/notify.star` is used to render a pixlet go template and push to the target device.

Example Home Assistant `rest_command` Service:

```yaml
rest_command:
  tidbyt-notify:
    url: http://tidbyt:8080/api/notify
    payload: '{"text": "{{ text }}", "textcolor": "{{ textcolor }}", "textsize": {{ textsize }}, "bgcolor": "{{ bgcolor }}"}'
    method: POST
```
