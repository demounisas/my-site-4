"""
Builds the 10 Odoo module pages (dist/odoo-*.html) from dist/index.html.

The header, footer, contact section, pop-up and scripts are copied from
index.html on every run, so after editing the homepage just re-run:

    python tools/build_module_pages.py

Page content lives in PAGES below. Each page picks its own hero style and
its own sequence of section types so no two pages share the same layout.
"""
import base64
import io
import os
import re

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
logo_uri = re.search(r'<img class="brand-logo" src="(data:image[^"]+)"', header).group(1)
logo_file = "assets/" + extract_data_uri(logo_uri, "unisas-logo")

final_cta = between('<section class="final-cta" id="get-demo">', "</section>")
footer = between('<footer class="site-footer">', "</footer>")
modal = between('<dialog class="consult-modal"', "</dialog>")
floats = between('<div class="float-actions">', "</div>\n\n")
script = src[src.rindex("<script>"):src.rindex("</script>") + len("</script>")]
fonts = between('<link rel="preconnect" href="https://fonts.googleapis.com">', 'display=swap" rel="stylesheet">')

# tile icons, in homepage order
TILE_ICONS = re.findall(r'<span class="app-ic">(<svg.*?</svg>)</span>', between('<section class="section" id="modules">', "</section>"))


def rewrite_links(html):
    html = html.replace(logo_uri, logo_file)
    html = re.sub(r'href="#services" data-svc="(\w+)"', r'href="index.html?svc=\1#services" data-svc="\1"', html)
    html = html.replace('href="#"', 'href="index.html"', 1) if 'href="#">Home<' in html else html
    html = re.sub(r'href="#(?!get-demo")([\w-]+)"', r'href="index.html#\1"', html)
    return html


header = rewrite_links(header).replace('<a href="index.html#modules">Solutions</a>', '<a href="index.html#modules" aria-current="page" style="color:var(--text);font-weight:600;">Solutions</a>')
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
    table = ('<div class="mp-table-wrap"><table class="mp-table"><thead><tr><th scope="col">Area</th><th scope="col">%s</th>'
             '<th scope="col">With Odoo %s</th></tr></thead><tbody>%s</tbody></table></div>' % (d["before"], d["module"], rows))
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


def related_block(page):
    chips = ""
    for slug in page["related"]:
        p = BY_SLUG[slug]
        chips += ('<a class="mp-rel" href="%s.html"><span class="mp-rel-ic">%s</span><span><strong>%s</strong><span>%s</span></span>%s</a>'
                  % (slug, TILE_ICONS[p["icon"]], p["name"], p["short"], ARROW))
    return section(head("Works hand in hand with", "CONNECTED MODULES", sub="Every Odoo app shares one database, so %s data flows straight into these modules." % page["name"]) +
                   '<div class="mp-rel-grid">%s</div>' % chips, alt=False, extra=' id="related"')


def faq_block(page, alt):
    items = ""
    for i, (q, a) in enumerate(page["faq"]):
        o = "true" if i == 0 else "false"
        items += ('<div class="faq-item" data-open="%s"><button class="faq-q" aria-expanded="%s">%s%s</button>'
                  '<div class="faq-a-wrap"><div class="faq-a-inner"><p class="faq-a">%s</p></div></div></div>' % (o, o, q, FAQ_ICON, a))
    return section(head("Questions about Odoo %s" % page["name"], "FAQ") + '<div class="faq-list">%s</div>' % items, alt)


def hero(page):
    h = page["hero"]
    icon = '<span class="mp-hero-ic">%s</span>' % TILE_ICONS[page["icon"]]
    crumb = '<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">%s</span></nav>' % page["name"]
    ctas = ('<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">%s %s</a>'
            '<a href="#%s" class="btn btn-ghost">%s</a></div>' % (h["cta"], ARROW, h["cta2_href"], h["cta2"]))
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
}

# ---------------------------------------------------------------- page content
PAGES = [
    dict(slug="odoo-hr", icon=0, name="HR", short="Employees, attendance, payroll",
         meta="Odoo HR implementation for attendance, leave, payroll and appraisals. Unisas sets up Odoo Employees so your people data lives in one place.",
         hero=dict(style="split", eyebrow="ODOO HR / EMPLOYEES", title="One home for every employee record, from offer letter to payslip",
                   lead="We set up Odoo HR so attendance, leave, payroll and appraisals run from the same employee record — no more chasing spreadsheets at month end.",
                   points=["Biometric & mobile attendance", "Leave policies by location", "Payroll rules for your structure"],
                   cta="Discuss Odoo HR", cta2="See the employee lifecycle", cta2_href="lifecycle"),
         sections=[
             ("steps_h", dict(eyebrow="EMPLOYEE LIFECYCLE", title="Every stage of the employee journey, connected", extra=' id="lifecycle"', items=[
                 ("Recruit", "Job positions, applicants and interview stages in one pipeline."),
                 ("Onboard", "Checklists, documents and equipment handed over on day one."),
                 ("Attend", "Check-ins from biometric devices, kiosk or mobile."),
                 ("Leave", "Allocation rules, approvals and balances employees can see."),
                 ("Pay", "Salary structures, deductions and payslips in bulk."),
                 ("Grow", "Appraisals, goals and skills tracked over time.")])),
             ("features", dict(eyebrow="WHAT WE CONFIGURE", title="Set up around how your company actually works", alt=True, items=[
                 ("Departments & org chart", "Company, branch and department structure with managers, so approvals route to the right person."),
                 ("Attendance devices", "We connect biometric machines or enable mobile check-in with geolocation."),
                 ("Leave types & accruals", "Casual, sick, earned and comp-off leave with accrual and carry-forward rules."),
                 ("Payroll structures", "Salary rules for basic, allowances, PF, ESI and professional tax, validated with your accountant."),
                 ("Employee self-service", "Staff apply for leave, view payslips and update details without emailing HR."),
                 ("Appraisal cycles", "Review templates, reminders and manager feedback on a schedule you choose.")])),
             ("stats", dict(items=[("1", "employee record shared by every app"), ("0", "manual attendance re-entry"), ("Self-service", "for leave & payslips"), ("Payroll", "linked to accounting")])),
         ],
         related=["odoo-project", "odoo-accounting", "odoo-crm"],
         faq=[("Can Odoo connect to our biometric attendance machine?", "Yes. Most common biometric devices can push attendance into Odoo through a connector or scheduled import. We confirm your device model during scoping."),
              ("Does Odoo payroll handle Indian statutory deductions?", "Odoo payroll supports configurable salary rules, so PF, ESI and professional tax can be set up for your structure. We validate the rules with your accountant before go-live."),
              ("Can we start with attendance and leave only?", "Yes. Many clients start with Employees, Attendance and Time Off, then add Payroll and Appraisals in a later phase.")]),

    dict(slug="odoo-crm", icon=1, name="CRM", short="Leads & pipeline",
         meta="Odoo CRM implementation: lead capture, pipeline stages, follow-up activities and sales forecasting, configured for your sales team by Unisas.",
         hero=dict(style="center", eyebrow="ODOO CRM", title="See every lead, every stage and every next step in one pipeline",
                   lead="We configure Odoo CRM around your sales process, so leads from your website, WhatsApp and calls land in one place and nobody forgets a follow-up.",
                   points=["Lead capture from web & WhatsApp", "Pipeline stages that match your process", "Forecasts managers can trust"],
                   cta="Discuss Odoo CRM", cta2="How we set it up", cta2_href="setup"),
         sections=[
             ("stats", dict(items=[("Every", "lead source in one inbox"), ("Auto", "follow-up reminders"), ("Live", "pipeline forecast"), ("1-click", "quote from an opportunity")])),
             ("zigzag", dict(eyebrow="HOW WE SET IT UP", title="From first enquiry to signed deal", extra=' id="setup"', items=[
                 ("CAPTURE", "Never lose an enquiry", "We connect your website forms, email aliases and WhatsApp so every enquiry becomes a lead automatically, tagged by source.",
                  ["Website & landing page forms", "Email-to-lead aliases", "Duplicate detection & merging"]),
                 ("QUALIFY", "Focus on the leads that matter", "Lead scoring and assignment rules route good leads to the right salesperson by region, product or size.",
                  ["Assignment rules by territory", "Lead scoring on your criteria", "Lost reasons you can report on"]),
                 ("CLOSE", "Move deals forward, on time", "Scheduled activities, email templates and quotes created from the opportunity keep deals moving.",
                  ["Activity reminders & to-dos", "Quote directly from the deal", "Won deals flow into Sales"])])),
             ("checklist", dict(eyebrow="REPORTING", title="Numbers your sales review can rely on", alt=True, sub="Because CRM shares data with Sales and Accounting, reports show what was actually quoted, ordered and invoiced.", items=[
                 "Pipeline value by stage and salesperson", "Expected revenue and close-date forecast", "Conversion rate by lead source",
                 "Activity completion by team member", "Lost-deal reasons over time", "Custom dashboards per manager"])),
         ],
         related=["odoo-sales", "odoo-email-marketing", "odoo-ecommerce"],
         faq=[("Can Odoo CRM capture leads from WhatsApp?", "Yes. With a WhatsApp Business integration, incoming chats can create or update leads in Odoo. We set up the connector as part of the project."),
              ("Can we import our existing leads and customers?", "Yes. We clean and import contacts, companies and open opportunities from Excel or your current CRM before go-live."),
              ("Is Odoo CRM suitable for a small sales team?", "Yes. It works for teams of two as well as large sales organisations, and you only configure the stages and rules you need.")]),

    dict(slug="odoo-sales", icon=2, name="Sales", short="Quotes, orders, subscriptions",
         meta="Odoo Sales implementation: professional quotations, online signatures, sales orders, pricelists and subscriptions linked to inventory and invoicing.",
         hero=dict(style="split", eyebrow="ODOO SALES", title="Send quotes in minutes and turn them into orders without re-typing",
                   lead="We set up Odoo Sales with your products, pricelists and templates, so a quote becomes an order, a delivery and an invoice in a single flow.",
                   points=["Branded quote templates", "Online signature & payment", "Pricelists & discounts by customer"],
                   cta="Discuss Odoo Sales", cta2="See quote-to-cash", cta2_href="flow"),
         sections=[
             ("steps_v", dict(eyebrow="QUOTE TO CASH", title="One document, four steps, zero re-entry", extra=' id="flow"',
                              sub="Each step picks up the data from the one before it, so your team stops copying numbers between systems.", items=[
                 ("01", "Quote", "Pick products, apply the customer's pricelist and send a branded quotation by email or WhatsApp."),
                 ("02", "Confirm", "The customer signs or pays online; the quote becomes a sales order automatically."),
                 ("03", "Deliver", "Inventory reserves stock and creates the delivery order for your warehouse."),
                 ("04", "Invoice", "Invoice from the order with the right taxes, then track payment in Accounting.")])),
             ("bento", dict(eyebrow="FEATURES WE CONFIGURE", title="Built for how you sell", alt=True, wide=(0, 3), items=[
                 ("Pricelists that do the maths", "Customer-specific prices, quantity breaks, seasonal offers and multi-currency — applied automatically on every quote."),
                 ("Optional products", "Suggest add-ons and upsells right on the quotation."),
                 ("Subscriptions", "Recurring plans with automatic renewal invoices."),
                 ("Sales dashboards", "Revenue by product, salesperson, customer and region, updated live from confirmed orders — no end-of-month export.")])),
         ],
         related=["odoo-crm", "odoo-inventory", "odoo-accounting"],
         faq=[("Can customers accept a quote online?", "Yes. Quotations have a customer portal link where the customer can sign, and optionally pay, to confirm the order."),
              ("Can we have different prices for dealers and retail customers?", "Yes. Pricelists let you set prices and discounts per customer group, and Odoo applies them automatically."),
              ("Does Odoo Sales support recurring billing?", "Yes. With Subscriptions, recurring plans generate renewal orders and invoices on schedule.")]),

    dict(slug="odoo-inventory", icon=3, name="Inventory", short="Stock & warehouses",
         meta="Odoo Inventory implementation: multi-warehouse stock, barcode operations, reorder rules, lots and serial numbers, and accurate valuation.",
         hero=dict(style="dark", eyebrow="ODOO INVENTORY", title="Know exactly what you have, where it is, and when to reorder",
                   lead="We set up Odoo Inventory with your warehouses, locations and routes, so stock levels are accurate in real time and reorders happen before you run out.",
                   points=["Multi-warehouse & bin locations", "Barcode scanning on mobile", "Automatic reorder rules"],
                   cta="Discuss Odoo Inventory", cta2="Compare before & after", cta2_href="compare"),
         sections=[
             ("bento", dict(eyebrow="WHAT YOU GET", title="Stock control without the spreadsheets", wide=(0, 5), items=[
                 ("Real-time stock across every location", "Each receipt, transfer and delivery updates quantities instantly, per warehouse and per bin."),
                 ("Barcode operations", "Receive, pick and pack with a phone or scanner."),
                 ("Lots & serial numbers", "Full traceability from supplier to customer."),
                 ("Reorder rules", "Min/max rules create purchase or manufacturing orders."),
                 ("Routes", "Pick-pack-ship, drop-ship and cross-dock flows."),
                 ("Stock valuation", "FIFO or average cost, posted to Accounting automatically so your balance sheet matches the warehouse."),
                 ("Stock reports", "Ageing, movement history and forecasted stock.")])),
             ("compare", dict(eyebrow="BEFORE & AFTER", title="What changes when inventory moves to Odoo", alt=True, extra=' id="compare"', module="Inventory", before="Spreadsheets / Tally", items=[
                 ("Stock levels", "Updated at day end, often wrong", "Live after every movement"),
                 ("Reordering", "Someone notices a shortage", "Rules trigger POs automatically"),
                 ("Stock counts", "Paper sheets, manual entry", "Barcode cycle counts on mobile"),
                 ("Traceability", "Hard to find which batch went where", "Lot & serial tracking end to end"),
                 ("Valuation", "Calculated separately by accounts", "Posted automatically in real time")])),
         ],
         related=["odoo-purchase", "odoo-manufacturing", "odoo-ecommerce"],
         faq=[("Can we move our stock data from Tally into Odoo?", "Yes. We migrate item masters, opening stock by location and valuation, and reconcile the totals with you before go-live."),
              ("Do we need special barcode hardware?", "No. Odoo's barcode app works on Android phones and standard USB or Bluetooth scanners. Rugged handheld devices are optional."),
              ("Can Odoo manage several warehouses and branches?", "Yes. You can run multiple warehouses, each with its own locations and routes, and transfer stock between them.")]),

    dict(slug="odoo-purchase", icon=4, name="Purchase", short="Vendors & POs",
         meta="Odoo Purchase implementation: RFQs, vendor price comparison, approval workflows, receipts and three-way bill matching configured by Unisas.",
         hero=dict(style="reverse", eyebrow="ODOO PURCHASE", title="Buy at the right price, with approvals and bills that match",
                   lead="We configure Odoo Purchase so RFQs, approvals, goods receipts and vendor bills are linked — you always know what was ordered, received and billed.",
                   points=["RFQ comparison across vendors", "Approval limits by amount", "3-way match: PO, receipt, bill"],
                   cta="Discuss Odoo Purchase", cta2="See the purchase cycle", cta2_href="cycle"),
         sections=[
             ("checklist", dict(eyebrow="CONTROLS WE SET UP", title="Spend control without slowing buyers down", sub="Approval rules and vendor data are configured from your purchase policy, not a generic template.", items=[
                 "Approval levels by amount or category", "Vendor price lists & lead times", "Blanket orders & purchase agreements",
                 "Auto-created RFQs from reorder rules", "Receipts with quality checks", "Bills matched to PO and receipt"])),
             ("steps_h", dict(eyebrow="PURCHASE CYCLE", title="From request to paid bill", alt=True, extra=' id="cycle"', items=[
                 ("Request", "RFQ created by a buyer or a reorder rule."),
                 ("Compare", "Vendor quotes side by side on price and lead time."),
                 ("Receive", "Goods checked in against the PO, partial receipts included."),
                 ("Pay", "Vendor bill matched and scheduled for payment.")])),
             ("stats", dict(items=[("3-way", "PO · receipt · bill match"), ("Auto", "RFQs from stock levels"), ("Every", "vendor price in one list"), ("Clear", "approval trail")])),
         ],
         related=["odoo-inventory", "odoo-accounting", "odoo-manufacturing"],
         faq=[("Can Odoo enforce purchase approvals?", "Yes. POs above a limit you set need manager approval, and we can add more levels by amount or department."),
              ("Can vendors send quotes through a portal?", "Yes. Vendors can view RFQs and update prices through the Odoo portal, or you can record quotes received by email."),
              ("Does Odoo check bills against what was received?", "Yes. Bill control can be set to billed quantities or received quantities, so you only pay for what arrived.")]),

    dict(slug="odoo-project", icon=5, name="Project", short="Tasks, Gantt, timesheets",
         meta="Odoo Project implementation: tasks, Kanban and Gantt planning, timesheets and project profitability for service businesses, set up by Unisas.",
         hero=dict(style="split", eyebrow="ODOO PROJECT", title="Plan the work, track the hours, and see if the project makes money",
                   lead="We set up Odoo Project with your stages, templates and billing rules, so tasks, timesheets and invoices stay tied to the same project.",
                   points=["Kanban, list & Gantt views", "Timesheets from web or mobile", "Profitability per project"],
                   cta="Discuss Odoo Project", cta2="Explore features", cta2_href="features"),
         sections=[
             ("zigzag", dict(eyebrow="HOW TEAMS USE IT", title="Three views of the same project", alt=True, extra=' id="features"', items=[
                 ("PLAN", "Plan with Gantt and milestones", "Schedule tasks against people's availability and spot conflicts before they happen.",
                  ["Gantt with dependencies", "Milestones tied to billing", "Project templates for repeat work"]),
                 ("DO", "Run the day-to-day in Kanban", "Teams move tasks through your stages, comment, attach files and log time from one screen.",
                  ["Custom stages per project", "Task chatter & mentions", "Customer portal for sign-off"]),
                 ("MEASURE", "Know if it's profitable", "Timesheets, expenses and invoices roll up into a live profitability view per project.",
                  ["Planned vs actual hours", "Billable vs non-billable time", "Margin per project & customer"])])),
             ("features", dict(eyebrow="ALSO INCLUDED", title="Small details that save hours", cols=4, items=[
                 ("Recurring tasks", "Monthly filings or maintenance created automatically."),
                 ("Mobile timesheets", "Start/stop timers on the go."),
                 ("Customer portal", "Clients see progress without status emails."),
                 ("Billing options", "Fixed price, milestones or time & materials.")])),
         ],
         related=["odoo-hr", "odoo-sales", "odoo-accounting"],
         faq=[("Can we bill clients from timesheets?", "Yes. Projects can be billed on timesheets, milestones or fixed price, and Odoo drafts the invoice from the approved hours."),
              ("Can clients see their project status?", "Yes. The customer portal lets clients view tasks, progress and documents you choose to share."),
              ("Does Odoo Project have Gantt charts?", "Yes. Odoo Enterprise includes Gantt planning with dependencies and resource availability.")]),

    dict(slug="odoo-manufacturing", icon=6, name="Manufacturing", short="BoM, work orders, quality",
         meta="Odoo Manufacturing (MRP) implementation: bills of materials, work orders, work centres, quality checks and production planning by Unisas.",
         hero=dict(style="dark-center", eyebrow="ODOO MANUFACTURING (MRP)", title="Plan production, run the shop floor and control quality in one system",
                   lead="We set up Odoo MRP with your bills of materials, routings and work centres, so production orders pull the right materials and costs flow to accounting.",
                   points=["Multi-level BoMs & routings", "Shop-floor tablet view", "Quality checks at each step"],
                   cta="Discuss Odoo Manufacturing", cta2="See the production flow", cta2_href="mrp-flow"),
         sections=[
             ("steps_h", dict(eyebrow="PRODUCTION FLOW", title="From demand to finished goods", extra=' id="mrp-flow"', items=[
                 ("Demand", "Sales orders or reorder rules create manufacturing orders."),
                 ("Plan", "Materials reserved, work centres scheduled by capacity."),
                 ("Produce", "Operators follow instructions on the shop-floor tablet."),
                 ("Check", "Quality points pass or fail with photos and measurements."),
                 ("Cost", "Actual material and labour cost posted to accounting.")])),
             ("compare", dict(eyebrow="BEFORE & AFTER", title="What your production team gains", alt=True, module="MRP", before="Manual / Excel planning", items=[
                 ("Material planning", "Shortages found on the shop floor", "Components reserved before production starts"),
                 ("Work instructions", "Printed sheets, often outdated", "Latest instructions on a tablet"),
                 ("Quality", "Checks recorded on paper", "Quality points with pass/fail and alerts"),
                 ("Product cost", "Estimated once a year", "Actual cost per manufacturing order")])),
             ("features", dict(eyebrow="WHAT WE CONFIGURE", title="Set up for your shop floor", items=[
                 ("Bills of materials", "Multi-level BoMs, variants, by-products and kits."),
                 ("Work centres & routings", "Capacity, working hours and operation times."),
                 ("Subcontracting", "Send components out and receive finished goods back.")])),
         ],
         related=["odoo-inventory", "odoo-purchase", "odoo-accounting"],
         faq=[("Does Odoo MRP suit small manufacturers?", "Yes. You can start with simple BoMs and manufacturing orders, then add work centres, routings and quality control as you grow."),
              ("Can Odoo handle job work / subcontracting?", "Yes. Odoo supports subcontracting, where you send components to a vendor and receive the finished product back into stock."),
              ("Can operators use tablets on the shop floor?", "Yes. The shop-floor view is designed for tablets, showing work orders, instructions and quality checks step by step.")]),

    dict(slug="odoo-accounting", icon=7, name="Accounting", short="Invoicing & bank reconciliation",
         meta="Odoo Accounting implementation: invoicing, GST-ready taxes, bank reconciliation, payables, receivables and financial reports configured by Unisas.",
         hero=dict(style="split", eyebrow="ODOO ACCOUNTING", title="Invoices, bank and GST reports that reconcile themselves",
                   lead="We set up Odoo Accounting with your chart of accounts, taxes and bank feeds, so sales, purchases and payroll post automatically and month end takes days, not weeks.",
                   points=["GST-ready tax setup", "Bank statement matching", "Live P&L and balance sheet"],
                   cta="Discuss Odoo Accounting", cta2="What we set up", cta2_href="setup"),
         sections=[
             ("stats", dict(items=[("Auto", "bank reconciliation suggestions"), ("Live", "P&L & balance sheet"), ("GST", "tax setup & reports"), ("1", "ledger for every app")])),
             ("accordion", dict(eyebrow="WHAT WE SET UP", title="A finance setup your auditor will like", extra=' id="setup"',
                                sub="We work with your accountant or CA so the configuration matches how your books are kept today.", items=[
                 ("Chart of accounts & opening balances", "We map your existing ledgers, import opening balances from Tally or your current system, and reconcile them before go-live."),
                 ("Taxes & GST", "Tax rates, fiscal positions for inter-state and export sales, and the reports your filings need."),
                 ("Bank & payments", "Bank statement import or feeds, reconciliation models that auto-match common transactions, and payment follow-ups."),
                 ("Receivables & payables", "Customer invoices, vendor bills, payment terms, ageing reports and automated reminders."),
                 ("Reporting", "P&L, balance sheet, cash flow and custom management reports, filterable by branch or analytic account.")])),
             ("checklist", dict(eyebrow="DAY-TO-DAY", title="Less data entry for your finance team", alt=True, items=[
                 "Invoices generated from sales orders", "Vendor bills from POs or scanned PDFs", "Payroll entries posted automatically",
                 "Stock valuation posted in real time", "Analytic accounts by branch or project", "Multi-company & multi-currency"])),
         ],
         related=["odoo-sales", "odoo-purchase", "odoo-hr"],
         faq=[("Can we migrate from Tally to Odoo Accounting?", "Yes. We migrate ledgers, opening balances, open invoices and bills from Tally and reconcile totals with your accountant before cutover."),
              ("Is Odoo Accounting GST compliant?", "Odoo includes Indian localisation with GST taxes and reports. We configure it for your registrations and check it with your CA."),
              ("Can Odoo reconcile bank statements automatically?", "Odoo suggests matches between bank lines and invoices or bills, and reconciliation rules can auto-match recurring transactions.")]),

    dict(slug="odoo-ecommerce", icon=8, name="Website & eCommerce", short="Online store tied to stock",
         meta="Odoo Website and eCommerce implementation: an online store connected to inventory, payments, shipping and accounting, built by Unisas.",
         hero=dict(style="center", eyebrow="ODOO WEBSITE / ECOMMERCE", title="An online store that already knows your stock, prices and customers",
                   lead="We build your Odoo store on the same database as your ERP, so products, stock, orders, payments and invoices stay in sync without plugins or exports.",
                   points=["Live stock on product pages", "Razorpay, UPI & card payments", "Orders create deliveries & invoices"],
                   cta="Discuss Odoo eCommerce", cta2="See what's connected", cta2_href="hub"),
         sections=[
             ("hub", dict(eyebrow="ONE SYSTEM", title="Your store is plugged into everything", extra=' id="hub"', core="Your online store",
                          sub="No sync jobs or middleware — the website reads and writes the same data your team uses.", items=[
                 ("Inventory", "live stock"), ("Sales", "orders & pricelists"), ("Accounting", "invoices & payments"),
                 ("CRM", "customer history"), ("Shipping", "courier labels"), ("Email Marketing", "abandoned carts")])),
             ("features", dict(eyebrow="STORE FEATURES", title="Everything a growing store needs", alt=True, items=[
                 ("Drag-and-drop pages", "Edit your website and product pages without a developer."),
                 ("Payment gateways", "Razorpay, PayU, Stripe and other providers connected to Accounting."),
                 ("Courier integration", "Shipping rates and labels from your courier partners."),
                 ("B2B portal", "Customer-specific prices and reorders for dealers."),
                 ("Promotions", "Coupons, discount codes and loyalty programs."),
                 ("SEO basics", "Meta tags, clean URLs and a sitemap out of the box.")])),
             ("steps_v", dict(eyebrow="LAUNCH PLAN", title="From catalogue to first order", items=[
                 ("01", "Catalogue", "Products, variants, images and categories imported and cleaned."),
                 ("02", "Design", "Theme and pages built around your brand."),
                 ("03", "Connect", "Payments, courier and email set up and tested end to end."),
                 ("04", "Launch", "Go live with training for your team on orders and returns.")])),
         ],
         related=["odoo-inventory", "odoo-sales", "odoo-email-marketing"],
         faq=[("Can Odoo eCommerce accept UPI payments?", "Yes. Through payment providers such as Razorpay you can accept UPI, cards and net banking, with payments recorded in Accounting."),
              ("Do we need a separate website platform?", "No. Odoo Website hosts your pages and store on the same system as your ERP, so there's nothing to sync."),
              ("Can we sell to dealers and retail customers on one site?", "Yes. B2B customers can log in to see their own prices and reorder, while retail visitors see public prices.")]),

    dict(slug="odoo-email-marketing", icon=9, name="Email Marketing", short="Campaigns on CRM data",
         meta="Odoo Email Marketing and Marketing Automation implementation: segmented campaigns and automated journeys built on your CRM and sales data.",
         hero=dict(style="reverse", eyebrow="ODOO EMAIL MARKETING", title="Campaigns that use what you already know about your customers",
                   lead="We set up Odoo Email Marketing and Marketing Automation on top of your CRM and sales data, so every campaign reaches the right segment and results feed back into the pipeline.",
                   points=["Segments from CRM & sales data", "Drag-and-drop email builder", "Automated follow-up journeys"],
                   cta="Discuss Odoo Email Marketing", cta2="See an automated journey", cta2_href="journey"),
         sections=[
             ("flow", dict(eyebrow="MARKETING AUTOMATION", title="An automated journey, built once, running every day", extra=' id="journey"',
                           sub="Example: a new lead from your website gets nurtured until sales can take over.", items=[
                 ("trigger", "Lead created from website form"), ("wait", "Wait 1 day"), ("email", "Send product guide"),
                 ("if", "Opened the guide?"), ("email", "Send case study & offer"), ("action", "Assign to salesperson")])),
             ("stats", dict(items=[("Segments", "built from real purchase data"), ("A/B", "subject line testing"), ("Live", "open & click tracking"), ("Leads", "created from replies & clicks")])),
             ("zigzag", dict(eyebrow="WHAT WE SET UP", title="From list to revenue, measured", alt=True, items=[
                 ("AUDIENCE", "Clean lists and useful segments", "We import and de-duplicate your contacts, set up opt-in and unsubscribe handling, and build segments from CRM and order history.",
                  ["Import & de-duplicate contacts", "Consent & unsubscribe handling", "Segments by purchase behaviour"]),
                 ("CAMPAIGNS", "On-brand emails without a designer", "Reusable templates in your brand colours, so your team can send newsletters and offers in minutes.",
                  ["Branded templates", "A/B testing on subject lines", "Scheduled sends"]),
                 ("RESULTS", "Know which campaigns bring revenue", "Because emails, leads and orders share one database, you can see which campaigns led to real sales.",
                  ["Open, click & bounce rates", "Leads & quotes per campaign", "Revenue attributed to campaigns"])])),
         ],
         related=["odoo-crm", "odoo-ecommerce", "odoo-sales"],
         faq=[("Do we need a separate tool like Mailchimp?", "Usually not. Odoo Email Marketing covers newsletters, segments, A/B tests and tracking, with the advantage of using your CRM and sales data directly."),
              ("Can we automate follow-up emails?", "Yes. Marketing Automation lets you build journeys with triggers, waits, conditions and actions such as assigning a salesperson."),
              ("Will our emails land in the inbox?", "We configure your sending domain with SPF, DKIM and DMARC and advise on list hygiene to protect deliverability.")]),
]
BY_SLUG = {p["slug"]: p for p in PAGES}

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
<link rel="stylesheet" href="assets/modules.css">
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

for page in PAGES:
    out = ""
    for kind, data in page["sections"]:
        html = SECTIONS[kind](data, data.get("alt", False))
        if data.get("extra"):
            html = html.replace('<section class="', '<section%s class="' % data["extra"], 1)
        out += html
    out += related_block(page)
    out += faq_block(page, alt=True)
    html = TEMPLATE.format(
        title="Odoo %s Implementation | Unisas" % page["name"], meta=page["meta"], fonts=fonts,
        header=header, hero=hero(page), sections=out, final_cta=final_cta, footer=footer,
        modal=modal, floats=floats, script=script)
    with io.open(os.path.join(DIST, page["slug"] + ".html"), "w", encoding="utf-8", newline="") as f:
        f.write(html)
    print("wrote", page["slug"] + ".html", len(html) // 1024, "KB")
