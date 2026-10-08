"""Balance the solution pages against the CRM page layout.

Appends a marked CSS block to each page stylesheet (re-runnable) that
  - puts compact sections in a CRM-style split: heading left, demo right (or reversed),
  - turns some centred headings into a side heading: title left, description right,
  - softens the large demo shadows so the interactions sit lighter on the page.
Titles, section order and interactions are untouched.

    python tools/balance_sections.py
"""
import os, re

ROOT = os.path.join(os.path.dirname(__file__), "..", "dist", "assets")
START, END = "/* balance:start */", "/* balance:end */"

PAGES = {
    # css file: (prefix, split sections, reversed splits, side-heading sections)
    "manufacturing.css": ("mf", ["cx"], [], ["chain", "cfg", "sort", "vis", "sup"]),
    "accounting.css": ("ac", [], ["chg"], ["explore", "je", "rec", "tree", "rep"]),
    "website.css": ("wb", ["anat"], ["week"], ["ed", "feat", "x", "mig"]),
    "email-marketing.css": ("em", [], ["ma"], ["aud", "proc", "quiz", "meas", "dlv"]),
    "pos.css": ("ps", ["off"], [], ["reg", "price", "ctl", "omni", "an"]),
    "hr.css": ("hr", [], ["raci"], ["str", "explore", "appr", "acc", "sk", "pick"]),
}

# demo tweaks that only apply while a section is split (the demo column is narrower)
SPLIT_FIX = {
    "mf": ".mf-sec--cx .mf-cx-grid{grid-template-columns:repeat(2,minmax(0,1fr));}.mf-sec--cx .mf-cx-app{min-height:120px;}",
    "ps": ".ps-sec--off .ps-off{grid-template-columns:minmax(0,1fr);}",
}


def block(p, split, rev, side):
    sec = lambda names: ",".join(".%s-sec--%s>.container" % (p, n) for n in names)
    css = []
    if side:
        s = sec(side)
        css.append(
            "@media (min-width:960px){"
            "%(h)s{max-width:none;margin-left:0;margin-right:0;text-align:left;display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr);column-gap:clamp(36px,5vw,80px);align-items:end;}"
            "%(e)s{grid-column:1;justify-self:start;}"
            "%(t)s{grid-column:1;margin-bottom:0;}"
            "%(s)s{grid-column:2;grid-row:1/span 2;margin:0;max-width:52ch;justify-self:end;}}"
            % {"h": ",".join(x + ">.%s-head" % p for x in s.split(",")),
               "e": ",".join(x + ">.%s-head>.%s-eyebrow" % (p, p) for x in s.split(",")),
               "t": ",".join(x + ">.%s-head>.%s-title" % (p, p) for x in s.split(",")),
               "s": ",".join(x + ">.%s-head>.%s-sub" % (p, p) for x in s.split(","))})
    for names, head_col, demo_col, cols in ((split, 1, 2, "minmax(0,5fr) minmax(0,7fr)"), (rev, 2, 1, "minmax(0,7fr) minmax(0,5fr)")):
        if not names:
            continue
        s = sec(names).split(",")
        css.append(
            "@media (min-width:1024px){"
            "%(c)s{display:grid;grid-template-columns:%(cols)s;column-gap:clamp(40px,5vw,76px);align-items:center;}"
            "%(k)s{grid-column:%(d)d;min-width:0;}"
            "%(h)s{grid-column:%(hc)d;grid-row:1;max-width:none;margin:0;text-align:left;}"
            "%(s)s{margin-left:0;margin-right:0;}}"
            % {"c": ",".join(s), "cols": cols, "d": demo_col, "hc": head_col,
               "k": ",".join(x + ">*" for x in s),
               "h": ",".join(x + ">.%s-head" % p for x in s),
               "s": ",".join(x + ">.%s-head>.%s-sub" % (p, p) for x in s)})
    if p in SPLIT_FIX:
        css.append("@media (min-width:1024px){%s}" % SPLIT_FIX[p])
    # lighter demo frames on this page (the shared .ox frame carries the heaviest shadow)
    css.append(".%s-sec .ox{box-shadow:0 14px 36px rgba(7,27,58,0.08);}" % p)
    return "\n".join([START] + css + [END])


def soften(css):
    # large navy shadows (blur >= 40px) -> one soft shadow, like the CRM page cards
    return re.sub(r"box-shadow:0 (\d+)px (\d+)px rgba\(7,27,58,0?\.\d+\)",
                  lambda m: "box-shadow:0 12px 32px rgba(7,27,58,0.07)" if int(m.group(2)) >= 40 else m.group(0), css)


for name, (p, split, rev, side) in PAGES.items():
    path = os.path.join(ROOT, name)
    css = open(path, encoding="utf-8").read()
    css = re.sub(r"\n?" + re.escape(START) + r".*?" + re.escape(END) + r"\n?", "\n", css, flags=re.S).rstrip("\n")
    css = soften(css) + "\n" + block(p, split, rev, side) + "\n"
    open(path, "w", encoding="utf-8", newline="").write(css)
    print("balanced", name)
