{{ define "notify" }}

load("render.star", "render")
load("encoding/base64.star", "base64")

ICON = {
  "bitcoin": base64.decode("""
iVBORw0KGgoAAAANSUhEUgAAABEAAAARCAYAAAA7bUf6AAAAlklEQVQ4T2NkwAH+H2T/jy7FaP+
TEZtyDEG4Zi0TTPXXzoDF0A1DMQRsADbN6MZdO4NiENwQbAbERh1lWLzMmgFGo5iFZBDYEFwuwG
sISCPUIKyGgDRjAyBXYXMNIz5XgDQga8TpLboYgux8DO/AwoUuLiEqTLBFMcmxQ7V0gssgklIsL
AYozjsoBoE45OZi5DRBSnkCAMLhlPBiQGHlAAAAAElFTkSuQmCC
""")
}

def main():
    return render.Root(
        child = render.Box(
            color = "{{ .BackgroundColor }}",
            child = render.Row(
                expanded = True,
                main_align = "space_evenly",
                cross_align = "center",
                children = [
                    {{if .Icon }}
                    render.Box(
                        width = 12,
                        height = 12,
                        child = render.Image(
                            src = ICON["{{ .Icon }}"],
                            width=11,
                            height=11
                        )
                    ),
                    render.Marquee(
                        width=50,
                        height=2,
                        child=render.Text(content="{{ .Text }}", color="{{ .TextColor }}"),
                        offset_start=5,
                        offset_end=38,
                        align="center"
                    )
                    {{else}}
                    render.Marquee( 
                        width=62,
                        height=2,
                        child=render.Text(content="{{ .Text }}", color="{{ .TextColor }}"),
                        offset_start=5,
                        offset_end=32,
                        align="center"
                    )
                    {{ end }}
                ],
            ),
        ),
    )
{{ end }}