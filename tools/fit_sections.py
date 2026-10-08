"""Fit the solution pages: two-line titles, equal side-by-side boxes, even spacing.

Appends a marked CSS block to each page stylesheet (re-runnable, runs after balance_sections.py):
  - one title size on every solution page, with heading columns wide enough for two lines,
  - side headings stack (description under the title), CRM-style splits get a wider title column,
  - two-column layouts stretch so the left and right boxes end on the same line.
Titles, section order and interactions are untouched.

    python tools/fit_sections.py
"""
import os, re

import ast

# read the PAGES table from balance_sections.py without running it
_src = open(os.path.join(os.path.dirname(__file__), "balance_sections.py"), encoding="utf-8").read()
BALANCED = ast.literal_eval(re.search(r"^PAGES = (\{.*?^\})", _src, re.S | re.M).group(1))

ROOT = os.path.join(os.path.dirname(__file__), "..", "dist", "assets")
START, END = "/* fit:start */", "/* fit:end */"

# css file -> page prefix
PREFIX = {
    "accounting.css": "ac", "crm.css": "crm", "website.css": "wb", "email-marketing.css": "em",
    "hr.css": "hr", "inventory.css": "iv", "manufacturing.css": "mf", "pos.css": "ps",
    "project.css": "pj", "purchase.css": "pu", "sales.css": "sl",
}

# headings that sit in one column of a two-column layout: css file -> (grids evened to 50/50, grids kept as they are)
COLUMN_HEADS = {
    "accounting.css": ([".ac-ints", ".ac-quiz"], []),
    "crm.css": ([".crm-integ"], []),
    "website.css": ([".wb-scope"], []),
    "email-marketing.css": ([], [".em-scope", ".em-sec--dlv .em-head"]),
    "hr.css": ([".hr-plan"], []),
    "inventory.css": ([".iv-ready", ".iv-cfg"], []),
    "manufacturing.css": ([".mf-plan2"], []),
    "pos.css": ([".ps-scope"], []),
    "project.css": ([".pj-ready", ".pj-cfg", ".pj-quiz"], []),
    "purchase.css": ([".pu-ready", ".pu-cfg"], [".pu-int", ".pu-golive"]),
    "sales.css": ([".sl-impl", ".sl-faqs"], []),
}

# two-column layouts whose left and right boxes should end level: css file -> selectors of the grid
EQUAL = {
    "accounting.css": [".ac-mig", ".ac-test"],
    "website.css": [".wb-jr-g"],
    "email-marketing.css": [".em-aud", ".em-meas"],
    "hr.css": [".hr-l-grid", ".hr-p5", ".hr-wk"],
    "pos.css": [".ps-reg-w", ".ps-an"],
    "project.css": [".pj-plan-grid"],
    "purchase.css": [".pu-auto"],
}

# page-specific extras: css file -> raw css
WIDE_HEAD = "minmax(0,1.25fr) minmax(0,1fr)"  # longer titles get the bigger share of the row
EXTRA = {
    "accounting.css": "@media (min-width:1024px){.ac-ints{grid-template-columns:%s;}.ac-sec--chg>.container{grid-template-columns:minmax(0,1fr) minmax(0,1.25fr);}}" % WIDE_HEAD,
    "website.css": "@media (min-width:1024px){.wb-sec--anat>.container,.wb-scope{grid-template-columns:%s;}}" % WIDE_HEAD,
    "hr.css": ".hr-sec--str .hr-stack{max-width:none;}"
              # migration demo: the spreadsheet grows to the height of the issues panel, its rows share the extra space
              "@media (min-width:1001px){.hr-mig{align-items:stretch;}.hr-sheet{display:flex;flex-direction:column;}"
              ".hr-sheet>.ox-scroll{flex:1;display:flex;flex-direction:column;}.hr-sheet-t{flex:1;}.hr-sheet-t thead tr{height:1px;}"
              # app picker: the recommended-setup panel matches the question list, app tiles share the height
              ".hr-pick{align-items:stretch;}.hr-apps-w{display:flex;flex-direction:column;}"
              ".hr-apps{flex:1;grid-auto-rows:1fr;}.hr-app{justify-content:center;}}",
    "pos.css": "@media (min-width:1024px){.ps-sec--cfg .pl-2.is-w{grid-template-columns:minmax(0,1.55fr) minmax(0,1fr);}}",
    "inventory.css": "@media (min-width:1024px){.iv-cfg{grid-template-columns:%s;}}" % WIDE_HEAD,
    "email-marketing.css": "@media (min-width:1024px){.em-scope{grid-template-columns:%s;}}" % WIDE_HEAD
              # DNS rows: every value chip spans the full row instead of the width of its description
                           + ".em-dns-t{flex:1;}.em-dns{padding:10px 14px;}.em-dnss{gap:6px;}"
              # deliverability + segments: both columns end on the same line, the shorter side takes up the slack
                           + "@media (min-width:1001px){.em-dlv,.em-map{align-items:stretch;}"
                             ".em-dlv-l{grid-template-rows:1fr auto;}.em-dnss{grid-auto-rows:1fr;}.em-dnss li{display:flex;}.em-dnss li>.em-dns{flex:1;}"
                             ".em-uns{grid-template-rows:auto 1fr;}"
                             ".em-sgs{grid-auto-rows:1fr;}.em-sg{justify-content:center;padding:9px 14px;}"
                             ".em-wf{display:flex;flex-direction:column;}.em-wf-steps{flex:1;}.em-wf-steps li{justify-content:center;}}",
}

# pages whose hero title is long (70+ characters): a smaller H1 keeps it to two lines
LONG_H1 = ("accounting.css", "website.css", "hr.css", "inventory.css")

# hero grid (copy column first) per page
HERO = {"inventory.css": ".iv-hx-photo"}

TITLE = "clamp(1.6rem,2.3vw,2.1rem)"
SPLIT_TITLE = "clamp(1.4rem,1.9vw,1.7rem)"  # a heading beside a demo or form


def block(css_file):
    p = PREFIX[css_file]
    css = [
        # one title size everywhere, centred heads wide enough for two lines
        ".%(p)s-title{font-size:%(t)s;line-height:1.18;}"
        ".%(p)s-head{max-width:940px;}"
        ".%(p)s-h1{font-size:clamp(2rem,2.8vw,2.5rem);line-height:1.1;}"
        "body .final-cta-copy .section-title{max-width:24ch;font-size:%(t)s;}" % {"p": p, "t": TITLE}
    ]
    if css_file not in ("project.css", "purchase.css"):  # those two heroes are centred, single column
        css.append("@media (min-width:1024px){%s{grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);}}" % HERO.get(css_file, ".%s-hero" % p))
    if css_file in BALANCED:
        _, split, rev, side = BALANCED[css_file]
        if side:
            # side headings stack and centre: title, then the description under it (nothing floating on the right)
            heads = [".%s-sec--%s>.container>.%s-head" % (p, n, p) for n in side]
            css.append("@media (min-width:960px){%s{display:block;max-width:940px;margin-left:auto;margin-right:auto;text-align:center;}%s{margin:14px auto 0;max-width:none;justify-self:auto;}}"
                       % (",".join(heads), ",".join(h + ">.%s-sub" % p for h in heads)))
        both = split + rev
        if both:
            secs = [".%s-sec--%s>.container" % (p, n) for n in both]
            css.append("@media (min-width:1024px){%s{grid-template-columns:minmax(0,1fr) minmax(0,1fr);}%s{font-size:%s;}}"
                       % (",".join(secs), ",".join(s + ">.%s-head>.%s-title" % (p, p) for s in secs), SPLIT_TITLE))
    even, keep = COLUMN_HEADS.get(css_file, ([], []))
    if even or keep:
        css.append("@media (min-width:1024px){%s%s{font-size:%s;}}"
                   % ("%s{grid-template-columns:minmax(0,1fr) minmax(0,1fr);}" % ",".join(even) if even else "",
                      ",".join(g + " .%s-title" % p for g in even + keep), SPLIT_TITLE))
    eq = EQUAL.get(css_file)
    if eq:
        css.append("%s{align-items:stretch;}%s{align-self:stretch;}"
                   % (",".join(eq), ",".join(s + ">*" for s in eq)))
    if css_file in LONG_H1:
        css.append(".%s-h1{font-size:clamp(1.85rem,2.45vw,2.2rem);}" % p)
    css.append(EXTRA.get(css_file, ""))
    return START + "\n" + "\n".join(c for c in css if c) + "\n" + END


def main():
    for f in PREFIX:
        path = os.path.join(ROOT, f)
        s = open(path, encoding="utf-8").read()
        s = re.sub(r"\n?" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", "\n", s, flags=re.S).rstrip("\n")
        open(path, "w", encoding="utf-8", newline="\n").write(s + "\n" + block(f) + "\n")
        print("fit", f)


if __name__ == "__main__":
    main()
