"""
Builds the 10 Odoo module pages, the 8 Odoo service pages (dist/odoo-*.html)
and the company pages (dist/about.html, dist/contact.html) from dist/index.html.

The header, footer, contact section, pop-up and scripts are copied from
index.html on every run, so after editing the homepage just re-run:

    python tools/build_module_pages.py

Module content lives in PAGES below, service content in service_pages.py,
About and Contact content in company_pages.py.
Each page picks its own hero style and its own sequence of section types so
no two pages share the same layout.
"""
import base64
import io
import os
import re

from company_pages import COMPANY, COMPANY_MOCKS, contact_cards
from service_pages import SERVICES, SERVICE_MOCKS
import crm_page
import sales_page
import inventory_page
import purchase_page
import project_page
import accounting_page
import manufacturing_page
import hr_page
import website_page
import email_marketing_page
import pos_page
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
ASSETS = os.path.join(DIST, "assets")
INDEX = os.path.join(DIST, "index.html")

src = io.open(INDEX, encoding="utf-8").read()


def between(start, end, s=src, include=True):
    i = s.index(start)
    j = s.index(end, i) + len(end)
    return s[i:j] if include else s[i + len(start):j - len(end)]


# ---------------------------------------------------------------- assets
os.makedirs(ASSETS, exist_ok=True)
EXT = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp", "image/svg+xml": "svg"}


def extract_data_uri(uri, name):
    m = re.match(r"data:([^;]+);base64,(.*)", uri, re.S)
    ext = EXT[m.group(1)]
    fname = "%s.%s" % (name, ext)
    with open(os.path.join(ASSETS, fname), "wb") as f:
        f.write(base64.b64decode(m.group(2)))
    return fname


css = between("<style>\n  :root{", "</style>", include=False)
css = "  :root{" + css
m = re.search(r'\.stats-band\{[^}]*?url\("(data:image[^"]+)"\)', css)
if m:
    css = css.replace(m.group(1), extract_data_uri(m.group(1), "stats-bg"))
with io.open(os.path.join(ASSETS, "site.css"), "w", encoding="utf-8", newline="") as f:
    f.write(css)

header = between('<header class="nav">', "</header>")
logo_uri = re.search(r'<img class="brand-logo" src="([^"]+)"', header).group(1)
# the homepage may embed the logo or point at assets/unisas-logo.png directly
logo_file = "assets/" + extract_data_uri(logo_uri, "unisas-logo") if logo_uri.startswith("data:") else logo_uri

final_cta = between('<section class="final-cta" id="get-demo">', "</section>")
footer = between('<footer class="site-footer">', "</footer>")
modal = between('<dialog class="consult-modal"', "</dialog>")
floats = between('<div class="float-actions">', "</div>\n\n")
# the site script is the last <script> on the homepage, ignoring the Wix-embed link fix that may follow it
_site_src = re.sub(r'<script>\s*/\* When embedded.*?</script>\s*', '', src, flags=re.S)
script = _site_src[_site_src.rindex("<script>"):_site_src.rindex("</script>") + len("</script>")]
fonts = between('<link rel="preconnect" href="https://fonts.googleapis.com">', 'display=swap" rel="stylesheet">')

# tile icons, in homepage order
TILE_ICONS = re.findall(r'<span class="app-ic">(<svg.*?</svg>)</span>', between('id="modules">', "</section>"))
# service icons, keyed by service (consulting, implementation, ...)
SERVICE_ICONS = dict(re.findall(r'id="svc-tab-(\w+)".*?<span class="icon-badge">(<svg.*?</svg>)</span>', src, re.S))


def rewrite_links(html):
    html = html.replace(logo_uri, logo_file)
    html = re.sub(r'href="#services" data-svc="(\w+)"', r'href="index.html?svc=\1#services" data-svc="\1"', html)
    html = html.replace('href="#"', 'href="index.html"', 1) if 'href="#">Home<' in html else html
    html = re.sub(r'href="#(?!get-demo")([\w-]+)"', r'href="index.html#\1"', html)
    return html


header = rewrite_links(header)
def menu_header(dd_id, slug):
    """Header with the given mega menu (Solutions or Services) and its link to this page highlighted."""
    btn = 'id="%s">\n        <button class="nav-dd-btn"' % dd_id
    assert btn in header, "mega menu %s not found in index.html header" % dd_id
    return (header.replace(btn, btn[:-1] + ' is-current"', 1)
            .replace('<a href="%s.html">' % slug, '<a href="%s.html" aria-current="page">' % slug, 1))


def module_header(slug):
    return menu_header("nav-dd-solutions", slug)


def service_header(slug):
    return menu_header("nav-dd", slug)


def company_header(page):
    return header.replace('<a href="%s.html">%s</a>' % (page["slug"], page["nav"]),
                          '<a href="%s.html" aria-current="page" style="color:var(--text);font-weight:600;">%s</a>' % (page["slug"], page["nav"]), 1)


footer = rewrite_links(footer)

# ---------------------------------------------------------------- snippets
ARROW = '<svg width="15" height="11" viewBox="0 0 15 11" fill="none" aria-hidden="true"><path d="M9 1L14 5.5L9 10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M14 5.5H1" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
CHECK = '<svg width="18" height="18" viewBox="0 0 20 20" fill="none" aria-hidden="true"><circle cx="10" cy="10" r="9" fill="var(--success-tint)"/><path d="M6 10.2l2.6 2.6L14 7.6" stroke="var(--success)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
FAQ_ICON = '<svg class="faq-icon" width="28" height="28" viewBox="0 0 28 28" fill="none" aria-hidden="true"><circle class="faq-icon-ring" cx="14" cy="14" r="13" stroke="currentColor" stroke-width="1.5"/><path class="faq-icon-chev" d="M9.5 12l4.5 4.5 4.5-4.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def head(title, eyebrow, alt=False, center=True, sub=""):
    return ('<div class="section-head%s"><p class="eyebrow mono">%s</p><h2 class="section-title">%s</h2>%s</div>'
            % (" center" if center else "", eyebrow, title, '<p class="section-sub">%s</p>' % sub if sub else ""))


def section(body, alt=False, extra=""):
    return '<section class="section%s"%s><div class="container">%s</div></section>\n' % (" section-alt" if alt else "", extra, body)


# ---- section types
def s_features(d, alt):
    cols = d.get("cols", 3)
    cards = "".join('<div class="mp-card"><span class="mp-num mono">%02d</span><h3>%s</h3><p>%s</p></div>' % (i + 1, t, x)
                    for i, (t, x) in enumerate(d["items"]))
    return section(head(d["title"], d["eyebrow"], sub=d.get("sub", "")) + '<div class="mp-grid mp-cols-%d">%s</div>' % (cols, cards), alt)


def s_steps_h(d, alt):
    steps = "".join('<li><span class="mp-step-dot mono">%d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, t, x) for i, (t, x) in enumerate(d["items"]))
    return section(head(d["title"], d["eyebrow"], sub=d.get("sub", "")) + '<ol class="mp-steps-h" style="--n:%d">%s</ol>' % (len(d["items"]), steps), alt)


def s_steps_v(d, alt):
    steps = "".join('<li><span class="mp-vdot mono">%s</span><div><h3>%s</h3><p>%s</p></div></li>' % (tag, t, x) for tag, t, x in d["items"])
    body = ('<div class="mp-split">%s<ol class="mp-steps-v">%s</ol></div>'
            % ('<div class="mp-sticky">' + head(d["title"], d["eyebrow"], center=False, sub=d.get("sub", "")) + "</div>", steps))
    return section(body, alt)


def s_zigzag(d, alt):
    rows = ""
    for i, (tag, t, x, points) in enumerate(d["items"]):
        pts = "".join("<li>%s%s</li>" % (CHECK, p) for p in points)
        rows += ('<div class="mp-zz%s"><div class="mp-zz-copy"><p class="mp-tag mono">%s</p><h3>%s</h3><p>%s</p></div>'
                 '<ul class="mp-zz-panel">%s</ul></div>' % (" is-rev" if i % 2 else "", tag, t, x, pts))
    return section(head(d["title"], d["eyebrow"], sub=d.get("sub", "")) + rows, alt)


def s_bento(d, alt):
    cells = "".join('<div class="mp-bento-cell%s"><h3>%s</h3><p>%s</p></div>' % (" is-wide" if i in d.get("wide", (0,)) else "", t, x)
                    for i, (t, x) in enumerate(d["items"]))
    return section(head(d["title"], d["eyebrow"], sub=d.get("sub", "")) + '<div class="mp-bento">%s</div>' % cells, alt)


def s_compare(d, alt):
    rows = "".join('<tr><th scope="row">%s</th><td class="is-bad">%s</td><td class="is-good">%s</td></tr>' % r for r in d["items"])
    after = d.get("after") or "With Odoo %s" % d["module"]
    table = ('<div class="mp-table-wrap"><table class="mp-table"><thead><tr><th scope="col">Area</th><th scope="col">%s</th>'
             '<th scope="col">%s</th></tr></thead><tbody>%s</tbody></table></div>' % (d["before"], after, rows))
    return section(head(d["title"], d["eyebrow"], sub=d.get("sub", "")) + table, alt)


def s_checklist(d, alt):
    items = "".join("<li>%s<span>%s</span></li>" % (CHECK, x) for x in d["items"])
    body = ('<div class="mp-check-wrap"><div>%s</div><ul class="mp-check">%s</ul></div>'
            % (head(d["title"], d["eyebrow"], center=False, sub=d.get("sub", "")), items))
    return section(body, alt)


def s_stats(d, alt):
    cells = "".join('<div><p class="mp-stat-big">%s</p><p class="mp-stat-label">%s</p></div>' % s for s in d["items"])
    return '<section class="mp-stats"><div class="container"><div class="mp-stats-row">%s</div></div></section>\n' % cells


def s_accordion(d, alt):
    items = "".join('<details class="mp-acc"%s><summary>%s</summary><p>%s</p></details>' % (" open" if i == 0 else "", t, x)
                    for i, (t, x) in enumerate(d["items"]))
    body = '<div class="mp-split">%s<div>%s</div></div>' % ('<div class="mp-sticky">' + head(d["title"], d["eyebrow"], center=False, sub=d.get("sub", "")) + "</div>", items)
    return section(body, alt)


def s_hub(d, alt):
    n = len(d["items"])
    nodes = "".join('<li style="--k:%d"><strong>%s</strong><span>%s</span></li>' % (i, t, x) for i, (t, x) in enumerate(d["items"]))
    body = head(d["title"], d["eyebrow"], sub=d.get("sub", "")) + (
        '<div class="mp-hub" style="--n:%d"><div class="mp-hub-core"><span class="mono">ODOO</span><strong>%s</strong></div><ul>%s</ul></div>' % (n, d["core"], nodes))
    return section(body, alt)


def s_flow(d, alt):
    nodes = "".join('<li class="mp-flow-%s"><span class="mono">%s</span><strong>%s</strong></li>' % (k, k.upper(), t) for k, t in d["items"])
    return section(head(d["title"], d["eyebrow"], sub=d.get("sub", "")) + '<ol class="mp-flow">%s</ol>' % nodes, alt)


SECTIONS = dict(features=s_features, steps_h=s_steps_h, steps_v=s_steps_v, zigzag=s_zigzag, bento=s_bento,
                compare=s_compare, checklist=s_checklist, stats=s_stats, accordion=s_accordion, hub=s_hub, flow=s_flow)


def is_service(page):
    return "svc" in page


def is_company(page):
    return "nav" in page


def page_icon(page):
    if is_company(page):
        return page["icon_svg"]
    return SERVICE_ICONS[page["svc"]] if is_service(page) else TILE_ICONS[page["icon"]]


def contact_form():
    """The homepage form section, trimmed for the contact page: no checklist or
    next-steps list, and the contact details (if filled in) beside the form."""
    f = re.sub(r'\s*<ul class="final-cta-list">.*?</ul>', "", final_cta, flags=re.S)
    f = re.sub(r'\s*<p class="svc-incl-label"[^>]*>What happens next</p>\s*<ol class="final-cta-steps">.*?</ol>', "", f, flags=re.S)
    f = re.sub(r'<h2 class="section-title">.*?</h2>', '<h2 class="section-title">Tell us about your project</h2>', f, count=1, flags=re.S)
    f = re.sub(r'<p class="section-sub">.*?</p>', '<p class="section-sub">A few lines on your current systems, the teams involved and your timeline help us prepare for the first call.</p>', f, count=1, flags=re.S)
    cards = contact_cards()
    if cards:
        items = "".join('<div><dt class="mono">%s</dt><dd>%s</dd></div>' % (label.upper(), value) for label, value in cards)
        # insert at the end of the copy column, just before the form card
        f, n = re.subn(r'(\n\s*</div>\s*<div class="lead-form-card">)', lambda m: '\n        <dl class="contact-list">%s</dl>%s' % (items, m.group(1)), f, count=1)
        assert n, "final-cta markup changed; update contact_form()"
    return f


def related_block(page):
    chips = ""
    for slug in page["related"]:
        p = BY_SLUG[slug]
        chips += ('<a class="mp-rel" href="%s.html"><span class="mp-rel-ic%s">%s</span><span><strong>%s</strong><span>%s</span></span>%s</a>'
                  % (slug, " is-line" if is_service(p) or is_company(p) else "", page_icon(p), p["name"], p["short"], ARROW))
    if page.get("related_head"):
        title, eyebrow, sub = page["related_head"]
        heading = head(title, eyebrow, sub=sub)
    elif is_service(page):
        heading = head("Related Odoo services", "MORE SERVICES", sub="One team covers every stage of your Odoo project, so each service picks up where the last one left off.")
    else:
        heading = head("Works hand in hand with", "CONNECTED MODULES", sub="Every Odoo app shares one database, so %s data flows straight into these modules." % page["name"])
    return section(heading + '<div class="mp-rel-grid">%s</div>' % chips, alt=False, extra=' id="related"')


def faq_block(page, alt):
    items = ""
    for i, (q, a) in enumerate(page["faq"]):
        o = "true" if i == 0 else "false"
        items += ('<div class="faq-item" data-open="%s"><button class="faq-q" aria-expanded="%s">%s%s</button>'
                  '<div class="faq-a-wrap"><div class="faq-a-inner"><p class="faq-a">%s</p></div></div></div>' % (o, o, q, FAQ_ICON, a))
    title = page.get("faq_title") or ("Questions about %s" % page["name"] if is_service(page) else "Questions about Odoo %s" % page["name"])
    return section(head(title, "FAQ") + '<div class="faq-list">%s</div>' % items, alt)


def hero(page):
    if page.get("hero_fn"):
        return page["hero_fn"](globals())
    h = page["hero"]
    if h["style"] == "simple":
        # heading only: no icon, points, buttons or visual
        crumb = '<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span aria-current="page">%s</span></nav>' % page["name"]
        return ('<section class="mp-hero mp-hero--simple"><div class="mp-hero-copy">%s<p class="eyebrow mono">%s</p><h1 class="mp-h1">%s</h1><p class="mp-lead">%s</p></div></section>'
                % (crumb, h["eyebrow"], h["title"], h["lead"]))
    service, company = is_service(page), is_company(page)
    icon = '<span class="mp-hero-ic%s">%s</span>' % (" is-line" if service or company else "", page_icon(page))
    if company:
        parent = ""
    elif service:
        parent = '<a href="index.html#services">Services</a><span>/</span>'
    else:
        parent = '<a href="index.html#modules">Solutions</a><span>/</span>'
    crumb = '<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>%s<span aria-current="page">%s</span></nav>' % (parent, page["name"])
    svc = page.get("svc", "unsure" if company else "implementation")
    # on a page that shows the form inline, the main CTA scrolls to it instead of opening the pop-up
    no_modal = " data-no-modal" if page.get("form_first") else ""
    ctas = ('<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="%s"%s>%s %s</a>'
            '<a href="#%s" class="btn btn-ghost">%s</a></div>' % (svc, no_modal, h["cta"], ARROW, h["cta2_href"], h["cta2"]))
    points = "".join("<li>%s%s</li>" % (CHECK, p) for p in h["points"])
    copy = ('<div class="mp-hero-copy">%s%s<p class="eyebrow mono">%s</p><h1 class="mp-h1">%s</h1><p class="mp-lead">%s</p>'
            '<ul class="mp-hero-points">%s</ul>%s</div>' % (crumb, icon, h["eyebrow"], h["title"], h["lead"], points, ctas))
    visual = '<div class="mp-hero-visual">%s</div>' % MOCKS[page["slug"]]
    return '<section class="mp-hero mp-hero--%s">%s%s</section>' % (h["style"], copy, visual)


# ---------------------------------------------------------------- hero mocks (one per page, all different)
def bar(label, pct, color="var(--navy-800)"):
    return '<div class="mk-bar"><span>%s</span><i style="--w:%d%%;--c:%s"></i><b class="mono">%d%%</b></div>' % (label, pct, color, pct)


MOCKS = {
    "odoo-hr": '''<div class="mock mk-hr">
      <div class="mk-hr-profile"><span class="mk-avatar">PR</span><div><strong>Priya Raman</strong><span>Operations Executive · Chennai</span></div><em class="mk-pill ok">Checked in 09:02</em></div>
      <div class="mk-hr-grid">
        <div><span class="mono">LEAVE BALANCE</span><strong>12<small> days</small></strong></div>
        <div><span class="mono">THIS MONTH</span><strong>21<small> / 22 days</small></strong></div>
        <div><span class="mono">NEXT REVIEW</span><strong>Oct 14</strong></div>
      </div>
      <div class="mk-hr-row"><span>Leave request · 3 days</span><em class="mk-pill wait">Awaiting manager</em></div>
      <div class="mk-hr-row"><span>September payslip</span><em class="mk-pill ok">Generated</em></div>
    </div>''',
    "odoo-crm": '''<div class="mock mk-kanban">
      <div class="mk-col"><p class="mono">NEW <b>4</b></p><div class="mk-k">Retail chain rollout<small>₹ 8.4L</small></div><div class="mk-k">Clinic group ERP<small>₹ 3.1L</small></div></div>
      <div class="mk-col"><p class="mono">QUALIFIED <b>3</b></p><div class="mk-k is-hot">Distributor · 3 branches<small>₹ 12L</small></div><div class="mk-k">D2C brand<small>₹ 5.6L</small></div></div>
      <div class="mk-col"><p class="mono">PROPOSAL <b>2</b></p><div class="mk-k">Auto parts maker<small>₹ 18L</small></div></div>
      <div class="mk-col is-won"><p class="mono">WON <b>5</b></p><div class="mk-k">Export house<small>₹ 9.2L</small></div></div>
    </div>''',
    "odoo-sales": '''<div class="mock mk-doc">
      <div class="mk-doc-head"><div><span class="mono">QUOTATION</span><strong>S00482</strong></div><em class="mk-pill ok">Signed online</em></div>
      <table><tr><td>Industrial fan · 24"</td><td class="mono">x 40</td><td class="mono">₹ 1,84,000</td></tr>
      <tr><td>Installation kit</td><td class="mono">x 40</td><td class="mono">₹ 22,000</td></tr>
      <tr><td>Annual service plan</td><td class="mono">x 1</td><td class="mono">₹ 18,000</td></tr></table>
      <div class="mk-doc-total"><span>Total incl. GST</span><strong class="mono">₹ 2,64,320</strong></div>
      <div class="mk-doc-flow"><span class="is-done">Quote</span><span class="is-done">Order</span><span class="is-now">Delivery</span><span>Invoice</span></div>
    </div>''',
    "odoo-inventory": '<div class="mock mk-stock"><p class="mono mk-title">STOCK BY WAREHOUSE</p>' + bar("Chennai DC", 82, "#5DC1AA") + bar("Bengaluru", 57, "#F3B94C") + bar("Coimbatore", 23, "#E4402E") + bar("Hyderabad", 68, "#8E4F83") +
        '<div class="mk-alert"><strong>Reorder rule triggered</strong><span>Coimbatore · SKU FAN-24 below minimum (40)</span></div></div>',
    "odoo-purchase": '''<div class="mock mk-po">
      <div class="mk-po-head"><span class="mono">PURCHASE ORDER · P00217</span><em class="mk-pill wait">Needs approval</em></div>
      <div class="mk-po-vendor"><strong>Sri Lakshmi Metals</strong><span>Best price of 3 RFQs · lead time 5 days</span></div>
      <div class="mk-po-cmp"><div class="is-best"><span>Vendor A</span><b class="mono">₹ 412/kg</b></div><div><span>Vendor B</span><b class="mono">₹ 436/kg</b></div><div><span>Vendor C</span><b class="mono">₹ 451/kg</b></div></div>
      <div class="mk-po-actions"><span class="mk-btn">Approve</span><span class="mk-btn ghost">Ask for changes</span></div>
    </div>''',
    "odoo-project": '''<div class="mock mk-gantt">
      <div class="mk-g-head mono"><span></span><span>W1</span><span>W2</span><span>W3</span><span>W4</span><span>W5</span></div>
      <div class="mk-g-row"><span>Discovery</span><i style="--s:0;--l:1.2;--c:#8E4F83"></i></div>
      <div class="mk-g-row"><span>Design</span><i style="--s:1;--l:1.5;--c:#5DC1AA"></i></div>
      <div class="mk-g-row"><span>Build</span><i style="--s:2;--l:2.2;--c:#F3B94C"></i></div>
      <div class="mk-g-row"><span>UAT</span><i style="--s:3.6;--l:1;--c:#EE8A3C"></i></div>
      <div class="mk-g-row"><span>Go-live</span><i class="is-ms" style="--s:4.7;--l:.3;--c:#E4402E"></i></div>
      <div class="mk-g-foot"><span>Logged this week <b class="mono">164 h</b></span><span>Budget used <b class="mono">58%</b></span></div>
    </div>''',
    "odoo-manufacturing": '''<div class="mock mk-bom">
      <p class="mono mk-title">BILL OF MATERIALS · CEILING FAN</p>
      <ul class="mk-tree"><li><strong>Ceiling fan assembly</strong><ul>
        <li>Motor unit<ul><li>Stator winding</li><li>Rotor housing</li></ul></li>
        <li>Blade set <small>x3</small></li><li>Canopy &amp; downrod</li></ul></li></ul>
      <div class="mk-wo"><span>WO/0931 · 250 units</span><div class="mk-wo-steps"><i class="is-done">Cutting</i><i class="is-done">Winding</i><i class="is-now">Assembly</i><i>QC</i></div></div>
    </div>''',
    "odoo-accounting": '''<div class="mock mk-ledger">
      <div class="mk-l-top"><div><span class="mono">RECEIVABLES</span><strong>₹ 18.4L</strong></div><div><span class="mono">PAYABLES</span><strong>₹ 9.7L</strong></div><div><span class="mono">GST PAYABLE</span><strong>₹ 2.1L</strong></div></div>
      <p class="mono mk-title">BANK RECONCILIATION</p>
      <div class="mk-l-row"><span>NEFT · Arun Traders</span><b class="mono">+ ₹ 64,200</b><em class="mk-pill ok">Matched INV/0419</em></div>
      <div class="mk-l-row"><span>UPI · Office supplies</span><b class="mono">− ₹ 3,480</b><em class="mk-pill ok">Matched BILL/0233</em></div>
      <div class="mk-l-row"><span>RTGS · Unknown ref</span><b class="mono">+ ₹ 1,20,000</b><em class="mk-pill wait">Review</em></div>
    </div>''',
    "odoo-ecommerce": '''<div class="mock mk-shop">
      <div class="mk-browser"><i></i><i></i><i></i><span class="mono">yourstore.com/shop</span></div>
      <div class="mk-shop-grid">
        <div><span class="mk-img" style="--c:#5DC1AA"></span><strong>Cotton kurta</strong><small class="mono">₹ 1,299 · 32 in stock</small></div>
        <div><span class="mk-img" style="--c:#F3B94C"></span><strong>Linen shirt</strong><small class="mono">₹ 1,799 · 8 in stock</small></div>
        <div><span class="mk-img" style="--c:#8E4F83"></span><strong>Silk stole</strong><small class="mono">₹ 899 · Low stock</small></div>
      </div>
      <div class="mk-shop-foot"><span>Order #1042 paid via UPI</span><em class="mk-pill ok">Invoice &amp; delivery created</em></div>
    </div>''',
    "odoo-email-marketing": '''<div class="mock mk-mail">
      <div class="mk-mail-head"><span class="mono">CAMPAIGN</span><strong>Diwali offer · repeat buyers</strong><small>Segment from CRM: purchased in last 6 months</small></div>
      <div class="mk-mail-body"><span class="mk-img" style="--c:#EE8A3C"></span><p><b></b><b></b><b class="short"></b></p><span class="mk-btn">Shop the offer</span></div>
      <div class="mk-mail-stats"><div><strong class="mono">4,812</strong><span>Sent</span></div><div><strong class="mono">41%</strong><span>Opened</span></div><div><strong class="mono">9.6%</strong><span>Clicked</span></div></div>
    </div>''',
    "odoo-pos": '''<div class="mock mk-pos">
      <div class="mk-pos-order">
        <div class="mk-pos-head"><span class="mono">ORDER 0412 · TILL 2</span><em class="mk-pill ok">Online</em></div>
        <div class="mk-pos-line"><span>Cotton kurta <small>x 2</small></span><b class="mono">₹ 2,598</b></div>
        <div class="mk-pos-line"><span>Silk stole</span><b class="mono">₹ 899</b></div>
        <div class="mk-pos-line"><span>Loyalty discount</span><b class="mono">− ₹ 175</b></div>
        <div class="mk-pos-total"><span>Total incl. GST</span><strong class="mono">₹ 3,322</strong></div>
      </div>
      <div class="mk-pos-pay">
        <p class="mono mk-title">PAYMENT</p>
        <span class="mk-pos-btn">Cash</span><span class="mk-pos-btn">Card</span><span class="mk-pos-btn is-on">UPI QR</span>
        <div class="mk-pos-note"><strong>Stock updated</strong><span>Chennai store · 2 kurtas left</span></div>
      </div>
    </div>''',
}
MOCKS.update(SERVICE_MOCKS)
MOCKS.update(COMPANY_MOCKS)

# ---------------------------------------------------------------- page content
PAGES = [
    dict(slug="odoo-hr", icon=0, name="HR", short="Employees, attendance, time off",
         title="HR Software for Small Businesses Configured to Fit Your Workflows with Odoo | Unisas",
         meta="Odoo HR implementation for small businesses by Unisas: employee records, onboarding, time off, attendance, approvals, access control, skills and appraisals, configured around your workflows.",
         hero=dict(style="split", eyebrow="ODOO HR", title="", lead="", points=[], cta="", cta2="", cta2_href=""),
         sections=[], build=hr_page.build, hero_fn=hr_page.hero, cta=hr_page.CTA, css=("odoo-ui.css", "hr.css"),
         faq=hr_page.FAQ, faq_title="Frequently Asked Questions About Odoo HR"),

    dict(slug="odoo-crm", icon=1, name="CRM", short="Leads & pipeline",
         title="Odoo CRM Implementation for Smarter Sales | Unisas",
         meta="Odoo CRM implementation by Unisas: lead capture, pipeline stages, sales automation, integrations and reporting, designed around your sales process.",
         hero=dict(style="split", eyebrow="ODOO CRM IMPLEMENTATION", title="CRM Implementation for Smarter Sales, Powered by Odoo",
                   lead="We set up Odoo CRM around how your team sells, so every lead lands in one pipeline and forecasts come from real deals.",
                   points=["Lead capture from web, email & WhatsApp", "Pipeline stages that match your process", "Forecasts managers can trust"],
                   cta="Discuss Odoo CRM", cta2="How we set it up", cta2_href="setup"),
         sections=[], build=crm_page.build, hero_fn=crm_page.hero, cta=crm_page.CTA, css=("odoo-ui.css", "crm.css")),

    dict(slug="odoo-sales", icon=2, name="Sales", short="Quotes, orders, subscriptions",
         title="Sales Implementation Services Customized with Odoo | Unisas",
         meta="Odoo Sales implementation by Unisas: quotations, online signature and payment, pricelists, and orders connected to inventory and accounting.",
         hero=dict(style="split", eyebrow="ODOO SALES", title="", lead="", points=[], cta="", cta2="", cta2_href=""),
         sections=[], build=sales_page.build, hero_fn=sales_page.hero, cta=sales_page.CTA, css=("odoo-ui.css", "sales.css")),

    dict(slug="odoo-inventory", icon=3, name="Inventory", short="Stock & warehouses",
         title="Inventory Implementation Services Tailored to Your Business with Odoo | Unisas",
         meta="Odoo Inventory implementation by Unisas: multi-warehouse stock, routes, reordering rules, barcode, lots and serial numbers, data migration and live valuation.",
         hero=dict(style="split", eyebrow="ODOO INVENTORY", title="", lead="", points=[], cta="", cta2="", cta2_href=""),
         sections=[], build=inventory_page.build, hero_fn=inventory_page.hero, cta=inventory_page.CTA, css=("odoo-ui.css", "inventory.css")),

    dict(slug="odoo-purchase", icon=4, name="Purchase", short="Vendors & POs",
         title="Purchase Order Software for Smarter Procurement with Odoo | Unisas",
         meta="Odoo Purchase implementation by Unisas: RFQs, vendor alternatives, approval limits, reordering, three-way matching with receipts and bills, and supplier data migration.",
         hero=dict(style="split", eyebrow="ODOO PURCHASE", title="", lead="", points=[], cta="", cta2="", cta2_href=""),
         sections=[], build=purchase_page.build, hero_fn=purchase_page.hero, cta=purchase_page.CTA, css=("odoo-ui.css", "purchase.css")),

    dict(slug="odoo-project", icon=5, name="Project", short="Tasks, Gantt, timesheets",
         title="Project Management Software for Teams That Deliver, Built on Odoo | Unisas",
         meta="Odoo Project implementation by Unisas: project management software with tasks, milestones, dependencies, Gantt planning, timesheets and billing, set up around your delivery process.",
         hero=dict(style="split", eyebrow="ODOO PROJECT", title="", lead="", points=[], cta="", cta2="", cta2_href=""),
         sections=[], build=project_page.build, hero_fn=project_page.hero, cta=project_page.CTA, css=("odoo-ui.css", "project.css")),

    dict(slug="odoo-manufacturing", icon=6, name="Manufacturing", short="BoM, work orders, quality",
         title="Manufacturing ERP Software for End-to-End Production Management with Odoo | Unisas",
         meta="Odoo Manufacturing ERP implementation by Unisas: bills of materials, work orders, work centres, production planning, quality, traceability and cost control, set up around your production model.",
         hero=dict(style="split", eyebrow="ODOO MANUFACTURING", title="", lead="", points=[], cta="", cta2="", cta2_href=""),
         sections=[], build=manufacturing_page.build, hero_fn=manufacturing_page.hero, cta=manufacturing_page.CTA, css=("odoo-ui.css", "manufacturing.css")),

    dict(slug="odoo-accounting", icon=7, name="Accounting", short="Invoicing & bank reconciliation",
         title="Best Accounting Software Implementation for Your Business with Odoo | Unisas",
         meta="Odoo Accounting implementation by Unisas: GST invoicing, vendor bills, bank reconciliation, Tally migration, financial reports and integrations, matched to your finance processes.",
         hero=dict(style="split", eyebrow="ODOO ACCOUNTING", title="", lead="", points=[], cta="", cta2="", cta2_href=""),
         sections=[], build=accounting_page.build, hero_fn=accounting_page.hero, cta=accounting_page.CTA, css=("odoo-ui.css", "accounting.css")),

    dict(slug="odoo-ecommerce", icon=8, name="Website & eCommerce", short="Website, shop &amp; portal",
         title="Business Website Development Connected to Your Sales and Operations with Odoo | Unisas",
         meta="Odoo website implementation by Unisas: a business website connected to CRM, sales, eCommerce and inventory, with SEO, lead capture, migration and support.",
         hero=dict(style="split", eyebrow="ODOO WEBSITE", title="", lead="", points=[], cta="", cta2="", cta2_href=""),
         sections=[], build=website_page.build, hero_fn=website_page.hero, cta=website_page.CTA, css=("odoo-ui.css", "website.css")),

    dict(slug="odoo-email-marketing", icon=9, name="Email Marketing", short="Campaigns on CRM data",
         title="Powerful Email Marketing Software with Odoo | Unisas",
         meta="Odoo Email Marketing implementation by Unisas: targeted audiences from CRM and sales data, campaign scheduling, Marketing Automation journeys, A/B testing, deliverability and revenue reporting.",
         hero=dict(style="split", eyebrow="ODOO EMAIL MARKETING", title="", lead="", points=[], cta="", cta2="", cta2_href=""),
         sections=[], build=email_marketing_page.build, hero_fn=email_marketing_page.hero, cta=email_marketing_page.CTA, css=("odoo-ui.css", "email-marketing.css"),
         faq=email_marketing_page.FAQ, faq_title="Frequently Asked Questions About Odoo Email Marketing"),

    dict(slug="odoo-pos", icon=10, name="Point of Sale", short="Retail & restaurant checkout",
         title="Point of Sale Software for Smarter Store Management with Odoo | Unisas",
         meta="Odoo Point of Sale implementation by Unisas: checkout connected to inventory and accounting, offline mode, pricing and GST, cashier controls, hardware and payments, multi-store loyalty and restaurant workflows.",
         hero=dict(style="split", eyebrow="ODOO POINT OF SALE", title="", lead="", points=[], cta="", cta2="", cta2_href=""),
         sections=[], build=pos_page.build, hero_fn=pos_page.hero, cta=pos_page.CTA, css=("odoo-ui.css", "pos.css"),
         faq=pos_page.FAQ, faq_title="Frequently Asked Questions About Odoo Point of Sale"),
]
ALL_PAGES = PAGES + SERVICES + COMPANY


def page_cta(page):
    """The homepage contact section, with this page's own heading and intro if it sets one."""
    if not page.get("cta"):
        return final_cta
    title, sub = page["cta"]
    f = re.sub(r'<h2 class="section-title">.*?</h2>', lambda m: '<h2 class="section-title">%s</h2>' % title, final_cta, count=1, flags=re.S)
    return re.sub(r'<p class="section-sub">.*?</p>', lambda m: '<p class="section-sub">%s</p>' % sub, f, count=1, flags=re.S)
BY_SLUG = {p["slug"]: p for p in ALL_PAGES}

# ---------------------------------------------------------------- page assembly
TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
{fonts}
<link rel="stylesheet" href="assets/site.css">
<link rel="stylesheet" href="assets/modules.css">{extra_css}
</head>
<body>
<div class="page mp-page">
  <div class="grid-field" aria-hidden="true"></div>
  {header}
  {hero}
</div>
<main>
{sections}
</main>
{final_cta}
{footer}
{modal}
{floats}
{script}
</body>
</html>
"""

SERVICE_LINK = re.compile(r'href="(odoo-(?:consulting|implementation|customization|integration|data-migration|support|training|ai-automation)\.html)"')

# optional: build only the pages named on the command line, e.g. `python tools/build_module_pages.py odoo-project`
ONLY = set(sys.argv[1:])

for page in ALL_PAGES:
    if ONLY and page["slug"] not in ONLY:
        continue
    # the contact page puts the form straight under the hero
    out = contact_form() if page.get("form_first") else ""
    for kind, data in page["sections"]:
        html = SECTIONS[kind](data, data.get("alt", False))
        if data.get("extra"):
            html = html.replace('<section class="', '<section%s class="' % data["extra"], 1)
        out += html
    if page.get("build"):
        out += page["build"](globals())
    if page.get("related"):
        out += related_block(page)
    if page.get("faq"):
        out += faq_block(page, alt=True)
    if is_company(page):
        page_header = company_header(page)
    elif is_service(page):
        page_header = service_header(page["slug"])
    else:
        page_header = module_header(page["slug"])
    html = TEMPLATE.format(
        title=page.get("title") or "Odoo %s Implementation | Unisas" % page["name"], meta=page["meta"], fonts=fonts,
        header=page_header, hero=hero(page), sections=out,
        final_cta="" if page.get("form_first") else page_cta(page), footer=footer,
        modal=modal, floats=floats,
        script=script + ('\n<script src="assets/odoo-motion.js" defer></script>' if "odoo-ui.css" in page.get("css", ()) else ""),
        extra_css="".join('\n<link rel="stylesheet" href="assets/%s">' % c for c in page.get("css", ())))
    # service pages are not linked yet: service links only set the URL hash
    html = SERVICE_LINK.sub(r'href="#/\1"', html)
    with io.open(os.path.join(DIST, page["slug"] + ".html"), "w", encoding="utf-8", newline="") as f:
        f.write(html)
    print("wrote", page["slug"] + ".html", len(html) // 1024, "KB")
