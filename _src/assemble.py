#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta as páginas de conteúdo de almofadadepapel.com.br a partir de fragmentos."""
import json, os, re, sys, html

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")
DEST = "/sessions/blissful-tender-darwin/mnt/papel"
BASE = "https://www.almofadadepapel.com.br"
TEL = "+55-11-96307-3163"
WA = "https://wa.me/5511963073163?text=Ol%C3%A1!%20Vi%20o%20site%20almofadadepapel.com.br%20e%20quero%20falar%20com%20um%20especialista."

HEADER = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{base}/paper_cushion_box.jpg">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Almofada de Papel">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{base}/paper_cushion_box.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/conteudo.css">
{jsonld}
</head>
<body>
<header class="site-header">
  <div class="wrap header-inner">
    <a href="/" class="logo-wrap" aria-label="Almofada de Papel — página inicial">
      <span class="logo-icon"><svg viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg></span>
      <span class="logo-txt"><span class="n">Almofada de Papel</span><span class="s">Consultoria T&eacute;cnica Independente</span></span>
    </a>
    <nav class="main-nav" aria-label="Navega&ccedil;&atilde;o principal">
      <a href="/guia/"{a_guia}>Guia</a>
      <a href="/comparativos/"{a_comp}>Comparativos</a>
      <a href="/segmentos/"{a_seg}>Segmentos</a>
      <a href="/alternativas/"{a_alt}>Alternativas</a>
      <a href="/glossario/"{a_glos}>Gloss&aacute;rio</a>
      <a href="/faq/"{a_faq}>FAQ</a>
      <a href="/#consultor" class="btn-header">Diagn&oacute;stico Gratuito</a>
    </nav>
  </div>
</header>
<nav class="breadcrumb" aria-label="Voc&ecirc; est&aacute; aqui">
  <div class="wrap"><ol>{breadcrumb}</ol></div>
</nav>
<div class="article-hero">
  <div class="{wrapclass}">
    <span class="tag">{tag}</span>
    <h1>{h1}</h1>
    <p class="lead">{lead}</p>
    <p class="article-meta">Atualizado em {updated_br} &middot; Por Especialista em Almofada de Papel &middot; almofadadepapel.com.br</p>
  </div>
</div>
<article class="content">
  <div class="{wrapclass}">
"""

CTA = """
<div class="cta-box">
  <h2>Quer saber se a almofada de papel faz sentido para a sua opera&ccedil;&atilde;o?</h2>
  <p>Diagn&oacute;stico t&eacute;cnico gratuito e sem compromisso: an&aacute;lise do seu produto, volume de pedidos e custo por embalagem.</p>
  <div class="btns">
    <a class="btn-cta" href="/#consultor">Solicitar Diagn&oacute;stico Gratuito</a>
    <a class="btn-wa" href="{wa}" target="_blank" rel="noopener">Conversar no WhatsApp</a>
  </div>
</div>
"""

FOOTER = """
  </div>
</article>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <span class="fn">Almofada <em>de Papel</em></span>
        <p>Consultoria independente especializada em almofada de papel kraft para embalagem sustent&aacute;vel. Atendimento em todo o Brasil. S&atilde;o Paulo, SP.</p>
        <p>(11) 96307-3163 &middot; contato@almofadadepapel.com.br</p>
      </div>
      <div>
        <h4>Conte&uacute;do</h4>
        <ul>
          <li><a href="/guia/">Guia completo</a></li>
          <li><a href="/glossario/">Gloss&aacute;rio t&eacute;cnico</a></li>
          <li><a href="/faq/">Perguntas frequentes</a></li>
          <li><a href="/#o-que-e">O que &eacute; almofada de papel</a></li>
        </ul>
      </div>
      <div>
        <h4>Comparativos</h4>
        <ul>
          <li><a href="/comparativos/almofada-de-papel-vs-plastico-bolha/">vs. Pl&aacute;stico bolha</a></li>
          <li><a href="/comparativos/almofada-de-papel-vs-almofada-de-ar/">vs. Almofada de ar</a></li>
          <li><a href="/comparativos/almofada-de-papel-vs-isopor-eps/">vs. Isopor / EPS</a></li>
          <li><a href="/comparativos/">Todos os comparativos</a></li>
        </ul>
      </div>
      <div>
        <h4>Segmentos</h4>
        <ul>
          <li><a href="/segmentos/e-commerce/">E-commerce</a></li>
          <li><a href="/segmentos/autopecas/">Autope&ccedil;as</a></li>
          <li><a href="/segmentos/eletronicos/">Eletr&ocirc;nicos</a></li>
          <li><a href="/segmentos/">Todos os segmentos</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 Almofada de Papel &middot; Especialista em Embalagem Sustent&aacute;vel &middot; S&atilde;o Paulo, Brasil</span>
      <span><a href="/">In&iacute;cio</a> &middot; <a href="/sitemap.xml">Sitemap</a></span>
    </div>
  </div>
</footer>
</body>
</html>
"""

MESES = {1:"janeiro",2:"fevereiro",3:"março",4:"abril",5:"maio",6:"junho",7:"julho",8:"agosto",9:"setembro",10:"outubro",11:"novembro",12:"dezembro"}

def strip_tags(s):
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()

def build_page(path):
    raw = open(path, encoding="utf-8").read()
    m = re.match(r"\s*<!--META\s*(\{.*?\})\s*META-->\s*", raw, re.S)
    if not m:
        raise SystemExit(f"META ausente em {path}")
    meta = json.loads(m.group(1))
    body = raw[m.end():]

    url_path = meta["path"]                      # ex.: comparativos/x/
    canonical = f"{BASE}/{url_path}"
    updated = meta.get("updated", "2026-07-17")
    y, mo, d = [int(x) for x in updated.split("-")]
    updated_br = f"{d} de {MESES[mo]} de {y}"

    # Breadcrumb visual + schema
    crumbs = [["Início", "/"]] + meta.get("crumbs", [])
    bc_html, bc_items = [], []
    for i, (name, href) in enumerate(crumbs):
        last = i == len(crumbs) - 1
        if last:
            bc_html.append(f'<li aria-current="page">{name}</li>')
        else:
            bc_html.append(f'<li><a href="{href}">{name}</a></li>')
        item = {"@type": "ListItem", "position": i + 1, "name": strip_tags(name)}
        item["item"] = canonical if last else (BASE + href)
        bc_items.append(item)

    schemas = [
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": bc_items},
        {"@context": "https://schema.org", "@type": meta.get("schema_type", "Article"),
         "headline": strip_tags(meta["h1"]),
         "description": meta["desc"],
         "inLanguage": "pt-BR",
         "datePublished": meta.get("published", "2026-07-17"),
         "dateModified": updated,
         "mainEntityOfPage": canonical,
         "image": f"{BASE}/paper_cushion_box.jpg",
         "author": {"@type": "Organization", "name": "Almofada de Papel — Consultoria Técnica", "url": BASE + "/"},
         "publisher": {"@type": "Organization", "name": "Almofada de Papel", "url": BASE + "/",
                        "logo": {"@type": "ImageObject", "url": f"{BASE}/logo.png"}}},
    ]

    # FAQPage automático a partir de <details> dentro de .faq-bloco
    faqs = []
    for blk in re.findall(r'<details>\s*<summary>(.*?)</summary>\s*<div class="faq-body">(.*?)</div>\s*</details>', body, re.S):
        faqs.append({"@type": "Question", "name": strip_tags(blk[0]),
                     "acceptedAnswer": {"@type": "Answer", "text": strip_tags(blk[1])}})
    if faqs:
        schemas.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faqs})

    jsonld = "\n".join('<script type="application/ld+json">' + json.dumps(s, ensure_ascii=False) + "</script>" for s in schemas)

    # nav ativo
    section = url_path.split("/")[0]
    act = lambda s: ' class="active"' if section == s else ""

    page = HEADER.format(
        title=meta["title"], desc=meta["desc"], canonical=canonical, base=BASE,
        jsonld=jsonld, breadcrumb="".join(bc_html), tag=meta.get("tag", "Guia técnico"),
        h1=meta["h1"], lead=meta["lead"], updated_br=updated_br,
        wrapclass=("wrap" if meta.get("wide") else "wrap-narrow"),
        a_guia=act("guia"), a_comp=act("comparativos"), a_seg=act("segmentos"),
        a_alt=act("alternativas"), a_glos=act("glossario"), a_faq=act("faq"),
    )
    page += body
    if meta.get("cta", True):
        page += CTA.format(wa=WA)
    page += FOOTER

    out = os.path.join(DEST, url_path.strip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(page)
    return url_path, len(faqs)

def main():
    built = []
    for root, _, files in os.walk(SRC):
        for f in sorted(files):
            if f.endswith(".html"):
                built.append(build_page(os.path.join(root, f)))
    for p, nf in sorted(built):
        print(f"OK  /{p}  (faqs: {nf})")
    print(f"\nTotal: {len(built)} páginas")

if __name__ == "__main__":
    main()
