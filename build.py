# Builds the public privacy and support pages from the Markdown sources in the
# app repository. Run: python3 build.py
import html, pathlib, re

SRC = pathlib.Path("/Users/valentinosteiskal/Proyectos/valtri/docs/tienda")
OUT = pathlib.Path(__file__).parent

def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    text = re.sub(r"([\w.+-]+@[\w-]+(?:\.[\w-]+)+)", r'<a href="mailto:\1">\1</a>', text)
    return text

def render(md):
    out, para, items = [], [], []
    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>"); para.clear()
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>"); items.clear()
    for line in md.splitlines():
        if line.strip() == "---":
            flush(); out.append('<hr id="english">'); continue
        if line.startswith("# "):
            flush(); out.append(f"<h1>{inline(line[2:])}</h1>"); continue
        if line.startswith("## "):
            flush(); out.append(f"<h2>{inline(line[3:])}</h2>"); continue
        if re.fullmatch(r"\*\*[^*]+\*\*", line.strip()):
            flush(); out.append(f"<h3>{inline(line.strip()[2:-2])}</h3>"); continue
        if line.startswith("- "):
            if para: flush()
            items.append(line[2:]); continue
        if not line.strip():
            flush(); continue
        if items: flush()
        para.append(line.strip())
    flush()
    return "\n".join(out)

PAGE = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="{root}favicon.png">
<link rel="apple-touch-icon" href="{root}apple-touch-icon.png">
<style>
:root {{ --bg:#f0f0f0; --surface:#fff; --text:#242528; --muted:#5c5e63; --line:#e6e6e4; --accent:#2c6e72; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#242528; --surface:#2e2f33; --text:#f5f5f3; --muted:#abadb2; --line:#393a3f; --accent:#86c3c3; }} }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font:17px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
main {{ max-width:720px; margin:0 auto; padding:32px 16px 64px; }}
header {{ display:flex; flex-wrap:wrap; align-items:center; gap:8px 12px; margin-bottom:24px; }}
header img {{ width:40px; height:40px; border-radius:10px; }}
header a {{ color:var(--text); text-decoration:none; font-weight:600; font-size:19px; }}
nav {{ margin-left:auto; display:flex; flex-wrap:wrap; gap:4px 16px; font-size:15px; }}
nav a {{ color:var(--accent); text-decoration:none; }}
h1 {{ font-size:30px; line-height:1.2; margin:24px 0 8px; }}
h2 {{ font-size:20px; margin:32px 0 8px; }}
h3 {{ font-size:17px; margin:24px 0 4px; }}
h3 + p {{ margin-top:0; }}
p, li {{ color:var(--text); }}
ul {{ padding-left:20px; }}
li {{ margin:6px 0; }}
a {{ color:var(--accent); }}
code {{ background:var(--surface); border:1px solid var(--line); border-radius:6px; padding:1px 6px; font-size:15px; }}
hr {{ border:0; border-top:1px solid var(--line); margin:48px 0 0; }}
.card {{ background:var(--surface); border-radius:16px; padding:8px 24px 24px; }}
footer {{ color:var(--muted); font-size:14px; margin-top:32px; }}
</style>
</head>
<body>
<main>
<header>
<img src="{root}favicon.png" alt="" width="40" height="40">
<a href="{root}">Tranco</a>
<nav><a href="{root}privacidad/">Privacidad</a><a href="{root}soporte/">Soporte</a><a href="#english">English</a></nav>
</header>
<div class="card">
{body}
</div>
<footer>© 2026 Valentino · <a href="mailto:tinosteiskal@gmail.com">tinosteiskal@gmail.com</a></footer>
</main>
</body>
</html>
"""

def write(path, title, description, body, root):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(PAGE.format(title=title, description=description, body=body, root=root), encoding="utf-8")

write(OUT / "privacidad/index.html", "Privacidad de Tranco",
      "Política de privacidad de la app Tranco. Privacy policy for the Tranco app.",
      render((SRC / "politica-de-privacidad.md").read_text()), "../")
write(OUT / "soporte/index.html", "Soporte de Tranco",
      "Ayuda y contacto de la app Tranco. Help and contact for the Tranco app.",
      render((SRC / "soporte.md").read_text()), "../")
write(OUT / "index.html", "Tranco",
      "Tranco, diario de entrenamiento de triatlón para iPhone.",
      """<h1>Tranco</h1>
<p>Diario de entrenamiento de triatlón para iPhone.</p>
<ul><li><a href="privacidad/">Política de privacidad</a></li><li><a href="soporte/">Soporte</a></li></ul>
<hr id="english">
<p>Triathlon training journal for iPhone.</p>
<ul><li><a href="privacidad/#english">Privacy policy</a></li><li><a href="soporte/#english">Support</a></li></ul>""", "")
print("ok")
