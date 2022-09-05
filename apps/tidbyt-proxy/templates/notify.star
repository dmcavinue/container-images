{{ define "notify" }}
load("render.star", "render")

def main():
    return render.Root(
        child = render.Box(
            width = 64,
            height = 32,
            color = "{{ .BackgroundColor }}",
            child = render.Marquee(
                width=62,
                height=2,
                child=render.Text(content="{{ .Text }}", color="{{ .TextColor }}", align="center"),
                offset_start=5,
                offset_end=32,
            ),
        ),
    )
{{ end }}
