"""
Odoo Purchase page (odoo-purchase.html). Every section is modelled on a real
Odoo Purchase screen (demo.odoo.com/odoo/purchase): the RFQ dashboard and list,
the purchase order form with Alternatives, Purchase Settings, the receipt and
bill three-way match, bill digitisation, Merge Contacts and Purchase Analysis.
Shared Odoo look: dist/assets/odoo-ui.css. Page styles: dist/assets/purchase.css.

hero(g) and build(g) get the build script's globals.
"""
import json

from crm_explorer import ic, SEARCH, FUNNEL, V_KANBAN, V_LIST

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CROSS = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
TRUCK = ic('<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>', 18, 1.7)
BILL = ic('<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>', 18, 1.7)
MAIL = ic('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', 18, 1.7)
CHECK_C = ic('<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16 9.5"/>', 18, 1.8)
LIMIT = 500000

MENUS = ["Orders", "Products", "Reporting", "Configuration"]


def inr(n, dec=True):
    """Indian-format rupees: 12,00,000.00"""
    whole = int(round(n))
    digits = "%d" % whole
    rest, last3 = digits[:-3], digits[-3:]
    groups = []
    while len(rest) > 2:
        groups.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.insert(0, rest)
    out = ",".join(groups + [last3]) if groups else last3
    return "&#8377; " + out + (".00" if dec else "")


def head(eyebrow, title, sub="", cls=""):
    return ('<div class="pu-head%s"><p class="pu-eyebrow mono">%s</p><h2 class="pu-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="pu-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="pu-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


def odoo_nav(app_icon, menus=MENUS):
    return ('<div class="ox-nav"><span class="ox-app">%s<b>Purchase</b></span>%s<span class="ox-nav-r"><span class="ox-company">Your Company</span>'
            '<span class="ox-av" style="--c:#3E7CB1">A</span></span></div>' % (app_icon, "".join('<span class="ox-menu">%s</span>' % m for m in menus)))


def steps(items):
    return '<ol class="pu-steps">%s</ol>' % "".join('<li><span class="pu-step-n mono">%02d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i + 1, t, x)
                                                     for i, (t, x) in enumerate(items))


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">Purchase</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["RFQs to vendors in minutes", "Approvals by amount", "Pay only for what arrived"])
    copy = ('<div class="pu-hero-copy">%s<p class="pu-eyebrow mono">ODOO PURCHASE IMPLEMENTATION</p>'
            '<h1 class="pu-h1">Purchase Order Software <span>for Smarter Procurement with Odoo</span></h1>'
            '<p class="pu-lead">Unisas sets up Odoo Purchase around how your team buys, so requests, vendor quotes, approvals, receipts and bills sit on one '
            'linked record. Nobody chases a PO over email, and you only pay for what reached your warehouse.</p><ul class="pu-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Discuss Odoo Purchase %s</a>'
            '<a href="#explore" class="btn btn-ghost">Try the purchase demo</a></div></div>' % (crumb, points, g["ARROW"]))
    # one purchase, five linked documents, left to right
    DOC = ic('<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>', 18, 1.7)
    OK = ic('<path d="M5 13l4 4L19 7"/>', 14, 2.4)
    steps_ = [(DOC, "Request for Quotation", "P00044", "Steel chair frame &times; 120", [("3 vendors asked", "")], "RFQ Sent", "rfq"),
              (CHECK_C, "Purchase Order", "P00045", "Kaveri Steel Works", [("Best of 3 offers", "ok"), (inr(214800, False), "")], "Purchase Order", "po"),
              (TRUCK, "Receipt", "WH/IN/00012", "Chennai Warehouse", [("120 / 120 Units", "ok")], "Done", "rec"),
              (BILL, "Vendor Bill", "BILL/2026/10/0007", "Matched to PO &amp; receipt", [("3-way match", "ok"), (inr(253464, False), "")], "Posted", "bill"),
              (ic('<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18M7 15h3"/>', 18, 1.7), "Payment", "PAY/2026/0221", "HDFC Bank &middot; NEFT",
               [("Reconciled", "ok")], "Paid", "paid")]
    cards = "".join('<li class="pu-hx-step is-%s"><span class="pu-hx-ic">%s</span><span class="pu-hx-n mono">%02d</span><small>%s</small><b>%s</b><span class="pu-hx-sub">%s</span>'
                    '<span class="pu-hx-facts">%s</span><span class="pu-hx-st">%s</span></li>'
                    % (k, icn, n + 1, kind, ref, sub, "".join('<i class="%s">%s%s</i>' % ("is-ok" if c else "", OK if c else "", t) for t, c in facts), st)
                    for n, (icn, kind, ref, sub, facts, st, k) in enumerate(steps_))
    vis = ('<div class="pu-hero-vis pu-hx-flow" aria-label="One purchase from request to payment"><ol class="pu-hx-steps">%s</ol>'
           '<p class="pu-hx-foot"><span>Every document links back to <b>P00045</b>.</span><span>Saved <b>%s</b> by comparing three vendors.</span>'
           '<span>Paid only for the <b>120 units</b> received.</span></p></div>' % (cards, inr(19200, False)))
    return '<section class="pu-hero pu-hx">%s%s</section>' % (copy, vis)


# ------------------------------------------------------------------ data
# RFQs / POs for the explorer. lines: [product, description, qty, unit price, uom]
ORDERS = [
    {"id": 1, "num": "P00044", "arr": "Oct 10", "vendor": "Sri Lakshmi Metals", "ref": "", "buyer": "A", "deadline": "Oct 03", "late": False, "state": "draft", "src": "Replenishment", "star": False,
     "lines": [["Steel chair frame", "Powder-coated, black", 120, 1850, "Units"], ["Gas lift cylinder", "Class 4, 100 mm", 120, 690, "Units"]],
     "alts": [{"num": "P00044", "v": "Sri Lakshmi Metals", "d": 7, "p": [1850, 690]}, {"num": "P00045", "v": "Kaveri Steel Works", "d": 14, "p": [1790, 680]},
              {"num": "P00046", "v": "Metro Fabricators", "d": 5, "p": [1950, 700]}]},
    {"id": 2, "num": "P00043", "arr": "Oct 06", "vendor": "Deccan Motors", "ref": "DM/Q/2231", "buyer": "A", "deadline": "Sep 29", "late": True, "state": "sent", "src": "CHN/MO/00215", "star": False,
     "lines": [["Desk frame motor", "Dual, 24 V", 40, 3200, "Units"]]},
    {"id": 3, "num": "P00042", "arr": "Oct 09", "vendor": "Ambika Plywood", "ref": "AP-7781", "buyer": "K", "deadline": "Oct 02", "late": False, "state": "approve", "src": "", "star": True,
     "lines": [["Plywood board 18 mm", "BWP grade, 8 x 4 ft", 300, 2150, "Units"]]},
    {"id": 4, "num": "P00041", "arr": "Oct 06", "vendor": "Kovai Chemicals", "ref": "KC/26/0912", "buyer": "K", "deadline": "Sep 26", "late": False, "state": "purchase", "src": "Replenishment", "star": False,
     "bill": "no", "lines": [["Seat foam adhesive", "Solvent-free", 40, 640, "L"]]},
    {"id": 5, "num": "P00040", "arr": "Oct 01", "vendor": "Shakti Fabrics", "ref": "SF/26-27/1182", "buyer": "A", "deadline": "Sep 22", "late": False, "state": "purchase", "src": "", "star": False,
     "bill": "to", "lines": [["Mesh fabric roll", "Breathable, grey", 600, 420, "m"]]},
    {"id": 6, "num": "P00039", "arr": "Sep 24", "vendor": "Pioneer Packaging", "ref": "PP-4410", "buyer": "K", "deadline": "Sep 19", "late": False, "state": "purchase", "src": "Replenishment", "star": False,
     "bill": "done", "lines": [["Corrugated carton, 5-ply", "60 x 60 x 90 cm", 2000, 38, "Units"]]},
]

VENDORS = [
    ["Sri Lakshmi Metals", "Coimbatore", "Steel frames", 96, 14, 2240000, "#3E7CB1"],
    ["Deccan Motors", "Pune", "Motors &amp; electricals", 91, 6, 768000, "#8E4F83"],
    ["Ambika Plywood", "Bengaluru", "Boards", 84, 9, 1935000, "#C98600"],
    ["Kovai Chemicals", "Coimbatore", "Adhesives", 88, 11, 281600, "#1F8A78"],
    ["Shakti Fabrics", "Tiruppur", "Upholstery", 79, 8, 1008000, "#B5567E"],
    ["Pioneer Packaging", "Chennai", "Packaging", 98, 22, 836000, "#264E86"],
]

# vendor, product, min qty, price, lead time (days), valid until
PRICELIST = [
    ["Sri Lakshmi Metals", "Steel chair frame", 100, 1850, 7, "Mar 31, 2027"],
    ["Sri Lakshmi Metals", "Steel chair frame", 500, 1760, 7, "Mar 31, 2027"],
    ["Kaveri Steel Works", "Steel chair frame", 100, 1790, 14, "Dec 31, 2026"],
    ["Deccan Motors", "Desk frame motor", 20, 3200, 10, "Mar 31, 2027"],
    ["Ambika Plywood", "Plywood board 18 mm", 50, 2150, 5, "Dec 31, 2026"],
    ["Kovai Chemicals", "Seat foam adhesive", 20, 640, 4, "Mar 31, 2027"],
    ["Shakti Fabrics", "Mesh fabric roll", 200, 420, 12, "Jan 31, 2027"],
    ["Pioneer Packaging", "Corrugated carton, 5-ply", 1000, 38, 3, "Mar 31, 2027"],
]


# ------------------------------------------------------------------ sections
def build(g):
    out = ""
    app_icon = g["TILE_ICONS"][4]

    # 1 ---- delays & manual work: the purchase inbox
    mails = [("Ravi (Production)", "#3E7CB1", "09:12", "RE: RE: FW: Steel frames urgent", "Line 2 stops on Thursday if the frames don't come. Has anyone sent the PO?", True),
             ("Sri Lakshmi Metals", "#6C757D", "09:40", "Revised quote v3 (final)", "Please find our revised rates attached. Kindly ignore v2 sent yesterday.", True),
             ("Anita (Purchase Head)", "#C98600", "10:05", "Approval pending: plywood order", "Which quote is this? I approved a different amount on WhatsApp.", False),
             ("Divya (Accounts)", "#4C9F70", "10:31", "Bill mismatch: Shakti Fabrics", "They billed 600 m, stores say 540 m arrived. Should I hold the payment?", False),
             ("Karthik (Stores)", "#8E4F83", "11:02", "Unknown delivery at gate", "40 L adhesive arrived. No PO number on the challan. Accept or return?", False)]
    inbox = "".join('<li class="%s"><span class="ox-av is-msg" style="--c:%s">%s</span><div><p><b>%s</b><small>%s</small></p><p class="pu-mail-s">%s</p><p class="pu-mail-x">%s</p></div></li>'
                    % ("is-unread" if u else "", c, n[0], n, t, s, x) for n, c, t, s, x, u in mails)
    signs = ["POs are raised over email, WhatsApp and phone calls", "Nobody can tell which vendor quote is the latest",
             "Approvals are given verbally and can't be traced", "Stores receive goods without a PO to check against",
             "Accounts pays bills without knowing what actually arrived"]
    out += sec('<div class="pu-ready"><div>%s<ul class="pu-signs">%s</ul><p class="pu-note">Each of these costs a little time. Together they slow production, '
               'bury your buyers in follow-ups and leave you paying for goods you never checked.</p></div>'
               '<div class="pu-inbox" aria-label="Example purchase team inbox"><div class="pu-inbox-bar"><b>Inbox</b><span class="pu-inbox-n">23 unread</span><span class="pu-inbox-q">purchase OR quote OR PO</span></div>'
               '<ul>%s</ul></div></div>'
               % (head("THE COST OF MANUAL PURCHASING", "Is Your Purchasing Process Creating Unnecessary Delays and Manual Work?",
                       "In most growing firms, purchasing runs on email and memory. It works until volume grows, then looks like this."),
                  "".join('<li>%s%s</li>' % (CROSS, s) for s in signs), inbox), "pu-sec--ready")

    # 2 ---- simplify: one document, every stage
    stages = [("rfq", "Request", "RFQ created", "The buyer, or a reordering rule, creates the RFQ. Vendor, price and lead time are filled in from the vendor pricelist.", "Prices copied from old quotes"),
              ("sent", "Send", "Emailed to vendor", "One click emails the RFQ from your template. The vendor's reply comes back into the RFQ's chatter.", "Separate emails in personal inboxes"),
              ("po", "Confirm", "Purchase order", "Once confirmed, the RFQ becomes a PO, and Inventory creates the expected receipt with its arrival date.", "Stores told by phone what to expect"),
              ("rec", "Receive", "Goods received", "Stores validate the receipt against the PO. Partial deliveries create a backorder on their own.", "Challans checked against memory"),
              ("bill", "Bill", "Bill matched", "The vendor bill is created from the PO and limited to the quantity actually received.", "Bills keyed in and checked by hand"),
              ("paid", "Pay", "Paid &amp; reconciled", "The payment is registered and matched to the bank statement. The PO shows as fully billed and paid.", "Payment status asked over email")]
    tabs = "".join('<button type="button" class="pu-stg%s" data-stg="%d" aria-pressed="%s"><span class="mono">%02d</span><b>%s</b><small>%s</small></button>'
                   % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", i + 1, s[1], s[2]) for i, s in enumerate(stages))
    out += sec(head("ONE CONNECTED WORKFLOW", "How Can Odoo Simplify Your Purchasing and Procurement Workflow?",
                    "In Odoo the whole purchase stays on one record, from the first request to the paid bill. Step through a single order to see what Odoo does at each stage.", "is-center")
               + '<div class="pu-flow" data-flow><div class="pu-stgs" role="group" aria-label="Purchase stages">%s</div>'
                 '<div class="pu-flow-main"><div class="pu-flow-doc ox-solo" data-flow-doc aria-live="polite"></div>'
                 '<div class="pu-flow-txt"><p data-flow-txt></p><p class="pu-flow-was"><span>Without Odoo</span><b data-flow-was></b></p></div></div></div>' % tabs
               + '<script type="application/json" id="pu-stages">%s</script>' % json.dumps([[s[0], s[3], s[4]] for s in stages]), "pu-sec--flow")

    # 3 ---- configure around your process: Purchase Settings
    impl = [("Map your purchase policy", "Who can buy what, up to which amount, from which vendors, and who signs off."),
            ("Set Odoo's own controls", "Approval limits, bill control and order locking set in standard Purchase Settings."),
            ("Load vendors &amp; prices", "Vendor pricelists, lead times and minimum quantities, so RFQs fill themselves."),
            ("Prove it with real orders", "Your buyers run real RFQs through the setup before go-live.")]

    def toggle(key, name, desc, on, extra=""):
        return ('<label class="pu-set"><input type="checkbox" data-set="%s"%s><span class="pu-chk" aria-hidden="true">%s</span><span><b>%s</b><small>%s</small>%s</span></label>'
                % (key, " checked" if on else "", TICK, name, desc, extra))
    amount = ('<span class="pu-set-amt">Minimum Amount <select data-set-amt aria-label="Minimum amount for approval">%s</select></span>'
              % "".join('<option value="%d"%s>%s</option>' % (v, " selected" if v == LIMIT else "", inr(v)) for v in (100000, 500000, 1000000)))
    bill_ctl = ('<span class="pu-set-radio"><label><input type="radio" name="pu-bc" value="ordered" data-set-bc> Ordered quantities</label>'
                '<label><input type="radio" name="pu-bc" value="received" data-set-bc checked> Received quantities</label></span>')
    blocks = [("Orders", toggle("approve", "Purchase Order Approval", "Request managers to approve orders above a minimum amount", True, amount)
               + toggle("lock", "Lock Confirmed Orders", "No longer edit orders once confirmed", True)
               + toggle("warn", "Warnings", "Get warnings in orders for products or vendors", False)
               + toggle("agree", "Purchase Agreements", "Manage your purchase agreements (call for tenders, blanket orders)", True)),
              ("Invoicing", '<div class="pu-set is-static"><span class="pu-chk is-blank" aria-hidden="true"></span><span><b>Bill Control</b><small>Quantities billed by vendors</small>%s</span></div>' % bill_ctl
               + toggle("match", "3-way matching", "Make sure you only pay bills for which you received the goods you ordered", True))]
    sets = "".join('<div class="pu-set-group"><h4>%s</h4><div class="pu-set-grid">%s</div></div>' % b for b in blocks)
    out += sec('<div class="pu-cfg"><div>%s%s</div><div><div class="ox pu-ox pu-settings" data-settings>%s'
               '<div class="ox-cp"><div class="ox-cp-l"><span class="ox-new">Save</span><span class="ox-sbtn">Discard</span><span class="ox-crumb">Settings</span></div></div>'
               '<div class="pu-set-body">%s</div></div>'
               '<div class="pu-effect ox-solo"><p class="pu-effect-h">What your team will see</p><ul data-set-out aria-live="polite"></ul></div></div></div>'
               % (head("CONFIGURED FOR YOUR POLICY", "How Does Unisas Configure Odoo Purchase Around Your Business Process?",
                       "We write your purchase policy into Odoo&rsquo;s settings. Change one on the right and see who it affects."),
                  steps(impl), odoo_nav(app_icon), sets), "pu-sec--cfg")

    # 4 ---- what can Odoo manage: the purchase explorer
    feats = [("Requests for quotation", "RFQs that fill vendor, price and lead time for you, and can be sent in one click."),
             ("Vendor alternatives", "Ask several vendors, compare them line by line and keep the best offer."),
             ("Vendors &amp; pricelists", "Prices by quantity break, lead times and validity dates for every vendor."),
             ("Purchase orders", "Confirmed orders with receipt and billing status always in view.")]
    menu = "".join('<button type="button" class="pu-menu%s" data-px-menu="%s" aria-pressed="%s">%s</button>' % (" is-on" if k == "rfq" else "", k, "true" if k == "rfq" else "false", n)
                   for k, n in [("rfq", "Requests for Quotation"), ("po", "Purchase Orders"), ("vendors", "Vendors"), ("prices", "Vendor Pricelists")])
    views = [("list", "List", V_LIST), ("kanban", "Kanban", V_KANBAN)]
    switch = "".join('<button type="button" class="ox-vbtn%s" data-px-view="%s" aria-label="%s view" title="%s" aria-pressed="%s">%s</button>'
                     % (" is-on" if k == "list" else "", k, n, n, "true" if k == "list" else "false", svg) for k, n, svg in views)
    out += sec(head("WHAT ODOO PURCHASE MANAGES", "What Can Odoo Manage Across Vendors, RFQs and Purchase Orders?",
                    "This is the Purchase app as your buyers will use it. Open <b>P00044</b> and compare the vendor alternatives, send an RFQ, or confirm "
                    "<b>P00042</b> to see the approval limit at work.", "is-center")
               + '<div class="ox pu-ox pu-px" data-px><div class="ox-nav"><span class="ox-app">%s<b>Purchase</b></span><span class="pu-menus" role="group" aria-label="Purchase menu">%s</span>'
                 '<span class="ox-nav-r"><span class="ox-company">Your Company</span><span class="ox-av" style="--c:#3E7CB1">A</span></span></div>'
                 '<div class="ox-cp"><div class="ox-cp-l"><button type="button" class="ox-new" data-px-new>New</button><span class="ox-crumb" data-px-crumb>Requests for Quotation</span></div>'
                 '<label class="ox-search">%s<span class="ox-facet" data-px-facet hidden></span><input type="search" placeholder="Search..." aria-label="Search purchases" data-px-q></label>'
                 '<div class="ox-views" data-px-views>%s</div></div><div class="ox-body pu-px-body" data-px-body></div></div>'
                 '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview with sample data. Click a dashboard number to filter, or open a row to work on it.</p>'
                 % (app_icon, menu, SEARCH, switch)
               + '<ul class="pu-feats">%s</ul>' % "".join('<li><b>%s</b><span>%s</span></li>' % f for f in feats), "pu-sec--explore", "explore")

    # 5 ---- automation: approval route + automation rules
    rules = [("Reordering rule: Steel chair frame", "Forecast below 30 units", "RFQ P00047 created at 02:00 for 80 units", True),
             ("Receipt reminder to vendor", "2 days before Expected Arrival", "Deccan Motors reminded about P00043, due Oct 06", True),
             ("Late receipt follow-up", "Expected Arrival passed", "Activity scheduled for Arjun on P00040", True),
             ("Blanket order call-off", "Weekly, Monday 08:00", "1,000 cartons released from BO/2026/0012", True),
             ("Update vendor price on confirm", "Purchase order confirmed", "Pricelist updated: Kovai Chemicals, &#8377; 640/L", False)]
    limits = [("Up to " + inr(100000, False), ["Buyer", "Sent to vendor"], "Small orders go straight out."),
              (inr(100000, False) + " to " + inr(LIMIT * 2, False), ["Buyer", "Purchase Manager", "Sent to vendor"], "One approval, from desk or phone."),
              ("Above " + inr(LIMIT * 2, False), ["Buyer", "Purchase Manager", "Finance Director", "Sent to vendor"], "Two approvals before the vendor sees it.")]
    lrows = "".join('<li><b>%s</b><ol class="pl-flow">%s</ol><p>%s</p></li>'
                    % (a, "".join('<li><span class="pl-chip%s">%s</span></li>' % (" is-ok" if k == len(r) - 1 else "", x) for k, x in enumerate(r)), n) for a, r, n in limits)
    out += sec(head("AUTOMATION", "How Can Unisas Automate Purchase Approvals, Reordering and Procurement Workflows?",
                    "Approvals follow your limits, reorders raise themselves and vendors get reminded without anyone sending an email. Here is a typical setup we agree with you.", "is-center")
               + '<div class="pu-auto"><div class="pl-card"><p class="pl-k">Approval route by order value</p><ul class="pl-steps pu-lim">%s</ul></div>'
                 '<div class="pl-card"><p class="pl-k">What runs on its own</p><ul class="pl-steps">%s</ul></div></div>'
                 % (lrows, "".join('<li><span class="pl-n">%d</span><b>%s</b><p><b>When:</b> %s. <span class="pl-muted">Example: %s</span></p></li>' % (k + 1, n, w, l) for k, (n, w, l, on) in enumerate(rules))),
               "pu-sec--auto")

    # 6 ---- connected: three-way match
    out += sec(head("CONNECTED APPS", "How Can Odoo Connect Purchasing With Inventory, Sales and Accounting?",
                    "A purchase order is linked to the sale that triggered it, the receipt that brings the goods in and the bill that pays for them. "
                    "Receive the goods and create the bill to see the three-way match.", "is-center")
               + '<div class="pu-match" data-tw><div class="ox pu-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Purchase Orders</a><span>P00038</span></span></div>'
                 '<span></span><span class="ox-sbar is-mini pu-tw-sb"><span class="ox-sb">RFQ</span><span class="ox-sb">RFQ Sent</span><span class="ox-sb is-cur">Purchase Order</span></span></div>'
                 '<div class="pu-tw-btns"><button type="button" class="ox-pbtn" data-tw-do="rec1">Receive 60 units</button><button type="button" class="ox-sbtn" data-tw-do="rec2" disabled>Receive remaining 40</button>'
                 '<button type="button" class="ox-sbtn" data-tw-do="bill">Create Bill</button><button type="button" class="ox-sbtn pu-tw-reset" data-tw-do="reset">Reset</button></div>'
                 '<div class="pu-tw-sheet"><div class="pu-smarts" data-tw-smart></div><p class="pu-doc-kind">Purchase Order</p><h3>P00038</h3>'
                 '<dl class="ox-fields"><div><dt>Vendor</dt><dd>Sri Lakshmi Metals</dd></div><div><dt>Source Document</dt><dd><span class="pu-link">S00482</span>&nbsp;Bluebay Retail</dd></div>'
                 '<div><dt>Receipt Status</dt><dd data-tw-rs></dd></div><div><dt>Billing Status</dt><dd data-tw-bs></dd></div></dl>'
                 '<div class="ox-ftabs"><span class="is-on">Products</span><span>Other Information</span></div>'
                 '<div class="ox-scroll"><table class="pu-lines"><thead><tr><th>Product</th><th class="ox-num">Quantity</th><th class="ox-num">Received</th><th class="ox-num">Billed</th><th class="ox-num">Unit Price</th><th class="ox-num">Amount</th></tr></thead>'
                 '<tbody data-tw-lines></tbody></table></div></div></div>'
                 '<ol class="pu-tw-apps" aria-live="polite">'
                 '<li data-tw-app="sales" style="--c:#EE8A3C"><b>Sales</b><span data-tw-txt>S00482 for 100 chairs triggered this PO (make to order). The salesperson sees the expected date.</span></li>'
                 '<li data-tw-app="inv" style="--c:#1F8A78"><b>Inventory</b><span data-tw-txt>Receipt WH/IN/00012 is waiting for 100 frames and 100 cylinders.</span></li>'
                 '<li data-tw-app="acc" style="--c:#8E4F83"><b>Accounting</b><span data-tw-txt>Nothing to bill yet. Bill control is set to received quantities.</span></li></ol></div>',
               "pu-sec--match")

    # 7 ---- integrations: bill digitisation + systems
    systems = [("Tally, Busy or Zoho Books", "Vendors, open bills and payment history"), ("GST portal", "GSTIN check, e-Invoice IRN and GSTR-2B reconciliation"),
               ("Vendor portal &amp; email", "Vendors confirm POs and send bills by email"), ("Banks", "Vendor payments and statement reconciliation"),
               ("Supplier APIs &amp; EDI", "Catalogues, prices and order confirmations"), ("Custom apps", "REST / XML-RPC for your own systems")]
    nodes = "".join('<li><b>%s</b><span>%s</span></li>' % s for s in systems)
    fields = [("Vendor", "Shakti Fabrics"), ("GSTIN", "33AAKFS4421M1Z8"), ("Bill Reference", "SF/26-27/1182"), ("Bill Date", "01/10/2026"),
              ("Purchase Order", "P00040"), ("Untaxed Amount", inr(252000)), ("GST 18%", inr(45360)), ("Total", inr(297360))]
    frows = "".join('<div data-ocr-f><dt>%s</dt><dd><span>%s</span></dd></div>' % f for f in fields)
    out += sec('<div class="pu-int"><div>%s<ul class="pu-sys">%s</ul></div><div class="pu-ocr" data-ocr>'
               '<div class="pu-mail ox-solo"><p class="pu-mail-h">%s<span><b>accounts@shaktifabrics.in</b><small>to bills@yourcompany.odoo.com</small></span></p>'
               '<p class="pu-mail-sub">Invoice SF/26-27/1182 for PO P00040</p><span class="pu-pdf">PDF<small>SF-1182.pdf</small></span>'
               '<button type="button" class="ox-pbtn" data-ocr-go>Process incoming email</button></div>'
               '<div class="ox pu-ox pu-ocr-form"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Vendor Bills</a><span data-ocr-name>Draft</span></span></div>'
               '<span></span><span class="pu-ocr-st" data-ocr-st>Waiting for email</span></div><dl class="pu-ocr-dl">%s</dl>'
               '<p class="pu-ocr-res" data-ocr-res role="status" aria-live="polite"></p></div></div></div>'
               % (head("INTEGRATIONS", "How Does Unisas Integrate Odoo Purchase With Your Existing Systems?",
                       "Odoo connects to your accounts, GST portal, banks and vendors. Here, an emailed bill becomes a draft matched to its PO."),
                  nodes, MAIL, frows), "pu-sec--int")

    # 8 ---- configure vs customize
    reqs = [("Approve POs above &#8377; 5 lakh", "cfg", "Purchase Settings: Purchase Order Approval with a minimum amount.", "Setting", "A day"),
            ("Pay only for what was received", "cfg", "Bill Control set to received quantities, with 3-way matching.", "Setting", "A day"),
            ("Vendor prices with quantity breaks", "cfg", "Vendor pricelists on each product, with minimum quantity and validity.", "Data load", "Part of migration"),
            ("Ask three vendors and pick the best", "cfg", "Purchase Agreements: call for tenders and RFQ alternatives.", "Setting", "A day"),
            ("PO print with our terms and GST details", "studio", "Your document layout, with fields added in Odoo Studio. Upgrade-safe.", "Studio", "2 to 3 days"),
            ("Two-level approval: manager, then finance above &#8377; 10 lakh", "custom", "A small approval rule module on top of standard approval.", "Module", "About a week"),
            ("Check the department budget before confirming", "custom", "Budget check linked to Accounting budgets, which blocks or warns on confirmation.", "Module", "1 to 2 weeks"),
            ("Vendor scorecard for quality and delivery", "custom", "On-time rate is standard. We add quality scores from receipts and a vendor report.", "Module", "About a week")]
    lab = {"cfg": "Configuration", "studio": "Studio", "custom": "Customization"}
    ritems = "".join('<li><button type="button" class="pu-req%s" data-req="%d" aria-pressed="%s"><span>%s</span><i class="pu-tag pu-tag--%s">%s</i></button></li>'
                     % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", r[0], r[1], lab[r[1]]) for i, r in enumerate(reqs))
    out += sec(head("CONFIGURE OR CUSTOMIZE", "When Should Odoo Purchase Be Configured and When Does It Need Customization?",
                    "Most purchase requirements are already in standard Odoo. We configure first, use Studio for light changes, and write code only when the business truly needs it.", "is-center")
               + '<div class="pu-cvc" data-cvc><ul class="pu-reqs">%s</ul><div class="pu-verdict ox-solo" aria-live="polite"><p class="pu-v-kind" data-v-kind></p><h3 data-v-req></h3><p data-v-how></p>'
                 '<dl><div><dt>Done with</dt><dd data-v-with></dd></div><div><dt>Typical effort</dt><dd data-v-eff></dd></div><div><dt>Survives upgrades</dt><dd>Yes</dd></div></dl>'
                 '<div class="pu-v-meter"><span style="--w:62"><b>62%%</b>Configuration</span><span style="--w:18"><b>18%%</b>Studio</span><span style="--w:20"><b>20%%</b>Custom</span></div>'
                 '<small class="pu-v-foot">Typical split of purchase requirements across our projects</small></div></div>' % ritems
               + '<script type="application/json" id="pu-reqs">%s</script>' % json.dumps([[r[0], lab[r[1]], r[1], r[2], r[3], r[4]] for r in reqs]), "pu-sec--cvc")

    # 9 ---- data migration: Merge Contacts + what moves
    dupes = [("Sri Lakshmi Metals", "slm.sales@gmail.com", "33ABCFS1234K1ZP", 41), ("SRI LAKSHMI METALS PVT LTD", "accounts@srilakshmimetals.in", "33ABCFS1234K1ZP", 128),
             ("Srilakshmi Metal", "", "33abcfs1234k1zp", 6)]
    drows = "".join('<tr><th>%s<br><small class="pl-muted">%s</small></th><td class="mono">%s</td><td class="is-c">%d</td></tr>' % (n, e or "No email", v, c)
                    for n, e, v, c in dupes)
    moved = [("Vendors", "412 &rarr; 386", "26 duplicates merged"), ("Vendor pricelists", "1,940 lines", "Quantity breaks and lead times"),
             ("Open purchase orders", "63", "With pending quantities"), ("Pending receipts", "27", "Matched to their POs"),
             ("Unpaid vendor bills", "118 &middot; " + inr(4862300, False), "Opening payables, tallied to the ledger"), ("Purchase history", "3 years", "For price trends and vendor reports")]
    mig = [("Extract", "Vendors, items, open POs and unpaid bills from Tally, Excel or your old ERP."),
           ("Clean &amp; de-duplicate", "Vendors merged on GSTIN, bank details verified, dead items archived."),
           ("Trial import", "A test load into a copy of your database, checked by your buyers."),
           ("Reconcile &amp; sign off", "Open POs and payables tallied to your books before cut-over.")]
    out += sec(head("DATA MIGRATION", "How Does Unisas Handle Supplier and Purchase Data Migration?",
                    "Duplicate vendors and old prices spoil RFQs from the first day. We clean and de-duplicate them before anything goes into Odoo, then reconcile what is still open.", "is-center")
               + '<div class="pu-mig">%s<div class="pl-card"><p class="pl-k">One vendor, three records</p><div class="pl-scroll"><table class="pl-table"><thead><tr><th>Name</th><th>GSTIN</th><th class="is-c">Documents</th></tr></thead><tbody>%s</tbody></table></div>'
                 '<p style="margin:12px 0 0"><span class="pl-chip is-ok">&#10003; Merged into SRI LAKSHMI METALS PVT LTD &middot; 175 documents, one GSTIN</span></p></div>'
                 '<div class="pl-card"><p class="pl-k">What moves across</p><ul class="pl-steps">%s</ul></div></div>'
                 % (steps(mig), drows, "".join('<li><span class="pl-n">%d</span><b>%s</b><em>%s</em><p>%s</p></li>' % (k + 1, a, b, c) for k, (a, b, c) in enumerate(moved))), "pu-sec--mig")

    # 10 ---- what's included: a purchase order from Unisas
    scope = [("Setup", [("Purchase policy &amp; approval workshop", "Who buys what, limits and sign-offs mapped"),
                        ("Purchase settings &amp; approvals", "Approval limits, order locking, bill control"),
                        ("Vendors, pricelists &amp; reordering", "Quantity breaks, lead times, min/max rules")]),
             ("Data &amp; integration", [("Supplier data migration", "Cleaned vendors, open POs and unpaid bills"),
                                         ("Inventory &amp; Accounting link", "Receipts, three-way match and payables")]),
             ("People &amp; go-live", [("UAT, training &amp; hypercare", "Buyers, approvers, stores and accounts, through the first month-end")])]
    body = ""
    for title, items in scope:
        body += '<tr class="is-section"><td colspan="4">%s</td></tr>' % title
        body += "".join('<tr><td><b>%s</b><small>%s</small></td><td class="ox-num">1.00</td><td><span class="pu-gst">Included</span></td><td><span class="pu-incl">%s</span></td></tr>' % (n, d, TICK)
                        for n, d in items)
    out += sec('<div class="pu-scope">%s<div class="ox pu-ox"><div class="ox-cp"><div class="ox-cp-l"><a href="#get-demo" class="ox-new pu-ox-link" data-svc-cta="implementation">Confirm Order</a>'
               '<span class="ox-sbtn">Print RFQ</span><span class="ox-crumb ox-crumb--stack"><a>Requests for Quotation</a><span>P-UNISAS/0001</span></span></div>'
               '<span></span><span class="ox-sbar is-mini pu-scope-sb"><span class="ox-sb">RFQ</span><span class="ox-sb is-cur">RFQ Sent</span><span class="ox-sb">Purchase Order</span></span></div>'
               '<div class="pu-scope-sheet"><p class="pu-doc-kind">Request for Quotation</p><h3>P-UNISAS/0001</h3><dl class="ox-fields"><div><dt>Vendor</dt><dd>Unisas</dd></div><div><dt>Order Deadline</dt><dd>After discovery</dd></div>'
               '<div><dt>Deliver To</dt><dd>Your Company: Purchasing</dd></div><div><dt>Pricing</dt><dd>Fixed price, agreed up front</dd></div></dl>'
               '<div class="ox-ftabs"><span class="is-on">Products</span><span>Other Information</span></div>'
               '<div class="ox-scroll"><table class="pu-scope-t"><thead><tr><th>Product</th><th class="ox-num">Quantity</th><th>Price</th><th></th></tr></thead><tbody>%s</tbody></table></div></div></div></div>'
               % (head("WHAT'S INCLUDED", "What Does an Odoo Purchase Implementation With Unisas Include?",
                       "Our standard scope, written as an Odoo RFQ. Press <b>Confirm Order</b> to ask for one priced for your business.", "is-center"), body), "pu-sec--scope")

    # 11 ---- testing, training, go-live
    uat = [("Buyers", [("RFQ to three vendors, choose the best alternative", True), ("Confirm a PO from a reordering rule", True), ("Update a vendor price and lead time", False)]),
           ("Approvers", [("Approve a PO above the limit from mobile", True), ("Reject and send back with a note", False)]),
           ("Stores", [("Receive a partial delivery and create a backorder", True), ("Return damaged goods to the vendor", False)]),
           ("Accounts", [("Bill from PO, blocked until goods received", False), ("Register payment and reconcile with the bank", False)])]
    ul = ""
    n = 0
    for role, items in uat:
        ul += '<li class="pu-uat-role">%s</li>' % role
        for t, on in items:
            ul += '<li><label class="pu-uat-i"><input type="checkbox" data-uat%s><span class="pu-chk" aria-hidden="true">%s</span><span>%s</span></label></li>' % (" checked" if on else "", TICK, t)
            n += 1
    golive = [("Test with your own data", "Every scenario is tested on your vendors, items and real orders from last month, not demo data."),
              ("Train by role", "Buyers, approvers, stores and accounts each learn only the screens they will use, with short guides in your terms."),
              ("Cut over cleanly", "Open POs, pending receipts and unpaid bills move across on a weekend, reconciled before Monday."),
              ("Stay with you", "Our consultants handle questions on the floor through the first month-end close.")]
    out += sec('<div class="pu-golive"><div>%s%s</div><div class="pu-uat ox-solo" data-uatbox><div class="pu-uat-h"><span><small>User acceptance testing</small><b>Go-live readiness</b></span>'
               '<span class="pu-uat-pct" data-uat-pct></span></div><div class="pu-uat-bar"><i data-uat-bar></i></div><ul>%s</ul>'
               '<p class="pu-uat-res" data-uat-res aria-live="polite"></p></div></div>'
               % (head("TESTING, TRAINING &amp; GO-LIVE", "How Does Unisas Prepare Your Team for Testing, Training and Go-Live?",
                       "Go-live is planned like a project, with a checklist each role signs off. Tick the remaining tests to see when the purchase team is ready."),
                  steps(golive), ul), "pu-sec--golive")

    # 12 ---- visibility: Purchase Analysis
    kpis = [("Spend this quarter", inr(7068600, False), "Across 6 vendors"), ("On-time delivery", "89%", "Vendor average, last 90 days"),
            ("Days to receive", "8", "From confirmation to receipt"), ("Price saved", inr(312400, False), "From RFQ alternatives")]
    out += sec(head("PROCUREMENT VISIBILITY", "How Can a Connected Odoo Purchase Process Improve Procurement Visibility?",
                    "When every PO, receipt and bill is in one place, the reports build themselves. This is Odoo's Purchase Analysis. Change the measure to compare vendors.", "is-center")
               + '<ul class="pu-kpis">%s</ul>' % "".join('<li><small>%s</small><b>%s</b><span>%s</span></li>' % k for k in kpis)
               + '<div class="ox pu-ox" data-pa>%s<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb">Purchase Analysis</span></div>'
                 '<span class="ox-search">%s<span class="ox-facet">%sOrder Date: Q3 2026</span><span class="ox-facet">%sVendor</span></span><span></span></div>'
                 '<div class="ox-gtools"><span class="ox-measure" role="group" aria-label="Measure">%s</span></div>'
                 '<div class="ox-chart pu-chart"><div class="ox-yaxis" data-pa-y></div><div class="ox-plot" data-pa-plot></div></div>'
                 '<p class="ox-legend"><i></i><span data-pa-leg>Untaxed Total</span></p></div>'
                 % (odoo_nav(app_icon, ["Orders", "Products", "Reporting", "Configuration"]), SEARCH, FUNNEL, FUNNEL,
                    "".join('<button type="button" class="%s" data-pa-m="%d" aria-pressed="%s">%s</button>' % ("is-on" if i == 0 else "", i, "true" if i == 0 else "false", m)
                            for i, m in enumerate(["Untaxed Total", "On-Time Rate", "Days to Receive", "Qty Ordered"]))), "pu-sec--pa")

    # 13 ---- are you ready? self-check
    qs = ["Do you raise more than 50 purchase orders a month?", "Do purchases need approval above a certain amount?",
          "Do you buy the same items from more than one vendor?", "Do stores receive goods against a PO number?",
          "Does accounts check bills against what was received?", "Do you need purchase reports without building spreadsheets?"]
    qitems = "".join('<li><span>%s</span><span class="pu-yn" role="group" aria-label="Answer"><button type="button" data-q="%d" data-a="1" aria-pressed="false">Yes</button>'
                     '<button type="button" data-q="%d" data-a="0" aria-pressed="false">No</button></span></li>' % (q, i, i) for i, q in enumerate(qs))
    out += sec('<div class="pu-quiz"><div>%s<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Book a procurement review %s</a></div></div>'
               '<div class="pu-q ox-solo" data-quiz><p class="pu-q-h"><b>Procurement readiness check</b><small>6 questions, 30 seconds</small></p><ol>%s</ol>'
               '<div class="pu-q-res" data-quiz-res aria-live="polite"><span class="pu-q-score" data-quiz-score>0 / 6</span><p data-quiz-txt>Answer the questions to see where you stand.</p></div></div></div>'
               % (head("READINESS CHECK", "Is Your Procurement Process Ready for Odoo Purchase?",
                       "Mostly yes? Your purchasing has outgrown email and spreadsheets. We&rsquo;ll show the same flow in Odoo."),
                  g["ARROW"], qitems), "pu-sec--quiz")

    return out + JS.replace("__ORDERS__", json.dumps(ORDERS)).replace("__VENDORS__", json.dumps(VENDORS)).replace("__PRICES__", json.dumps(PRICELIST)).replace("__LIMIT__", str(LIMIT))


JS = r'''<script>
(function(){
  function inr(n,d){return '₹ '+Number(n).toLocaleString('en-IN',{minimumFractionDigits:d===false?0:2,maximumFractionDigits:d===false?0:2});}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function press(group,el){group.forEach(function(b){var on=b===el;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});}
  var TRUCK='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h11v10H3zM14 9h4l3 3v4h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>';
  var BILL='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/></svg>';
  var CLOCK='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/></svg>';
  function smart(ic,label,val){return '<span class="pu-smart"><i>'+ic+'</i><span>'+label+'<b>'+val+'</b></span></span>';}
  var LIMIT=__LIMIT__;

  /* --- 2 one document, every stage --- */
  var fl=document.querySelector('[data-flow]');
  if(fl){var S=JSON.parse(document.getElementById('pu-stages').textContent),tabs=[].slice.call(fl.querySelectorAll('[data-stg]')),doc=fl.querySelector('[data-flow-doc]');
    var BTN=[['Send by Email','Print RFQ','Confirm Order'],['Confirm Order','Re-Send by Email','Print RFQ'],['Receive Products','Send PO by Email','Lock'],['Create Bill','Send PO by Email','Lock'],['Register Payment','Print','Reset to Draft'],['Print','Reverse']];
    var REC=['','','Not Received','Fully Received','Fully Received','Fully Received'],BS=['','','Nothing to Bill','Waiting Bills','Fully Billed','Fully Billed'];
    var LOG=['RFQ P00041 created from the reordering rule for Seat foam adhesive','RFQ emailed to Kovai Chemicals. <i>Reply: “Confirmed, dispatch Oct 06.”</i>','Purchase order confirmed. Receipt WH/IN/00012 created, expected Oct 06','WH/IN/00012 validated: 40 L received in CHN/Stock/D-05','Bill BILL/2026/10/0004 created for the 40 L received and posted','Payment PAY/2026/0221 reconciled with the HDFC statement. <b>Paid</b>'];
    function draw(i){var bill=i>=4,po=i>=2,cur=Math.min(i,2);
      var sb=['RFQ','RFQ Sent','Purchase Order'].map(function(s,j){return '<span class="ox-sb'+(j===cur?' is-cur':'')+'">'+s+'</span>';}).join('');
      var b=BTN[i].map(function(x,j){return '<span class="'+(j?'ox-sbtn':'ox-pbtn')+'">'+x+'</span>';}).join('');
      var sm=po?'<div class="pu-smarts">'+smart(TRUCK,'Receipt','1')+(bill?smart(BILL,'Vendor Bills','1'):'')+smart(CLOCK,'On-time Rate','88%')+'</div>':'';
      doc.innerHTML='<div class="pu-fd-bar"><span class="ox-f-btns">'+b+'</span><span class="ox-sbar is-mini">'+sb+'</span></div>'+
        '<div class="pu-fd-sheet">'+(i===5?'<span class="ox-ribbon">PAID</span>':'')+sm+'<p class="pu-doc-kind">'+(po?'Purchase Order':'Request for Quotation')+'</p><h3>P00041</h3>'+
        '<dl class="pu-fd-meta"><div><dt>Vendor</dt><dd>Kovai Chemicals</dd></div><div><dt>'+(po?'Confirmation Date':'Order Deadline')+'</dt><dd>'+(po?'Sep 26, 2026':'Sep 26, 2026')+'</dd></div>'+
        (po?'<div><dt>Receipt Status</dt><dd><span class="pu-st'+(i>=3?' is-ok':'')+'">'+REC[i]+'</span></dd></div><div><dt>Billing Status</dt><dd><span class="pu-st'+(i>=4?' is-ok':i===3?' is-to':'')+'">'+BS[i]+'</span></dd></div>':'<div><dt>Expected Arrival</dt><dd>Oct 06, 2026</dd></div><div><dt>Source Document</dt><dd>Replenishment</dd></div>')+'</dl>'+
        '<table class="pu-lines"><thead><tr><th>Product</th><th class="ox-num">Quantity</th>'+(po?'<th class="ox-num">Received</th><th class="ox-num">Billed</th>':'')+'<th class="ox-num">Unit Price</th><th class="ox-num">Amount</th></tr></thead>'+
        '<tbody><tr><td><b>Seat foam adhesive</b><small>Solvent-free</small></td><td class="ox-num">40.00 L</td>'+(po?'<td class="ox-num">'+(i>=3?'40.00':'0.00')+'</td><td class="ox-num">'+(i>=4?'40.00':'0.00')+'</td>':'')+'<td class="ox-num">'+inr(640)+'</td><td class="ox-num">'+inr(25600)+'</td></tr></tbody></table>'+
        '<div class="pu-fd-log"><span class="ox-av is-bot">U</span><p><b>'+(i===3?'Karthik (Stores)':i===1?'Arjun Nair':'Unisas Bot')+'</b> <small>just now</small><br>'+LOG[i]+'</p></div></div>';
      fl.querySelector('[data-flow-txt]').innerHTML=S[i][1];fl.querySelector('[data-flow-was]').innerHTML=S[i][2];
      tabs.forEach(function(t,j){t.classList.toggle('is-done',j<i);});}
    tabs.forEach(function(t){t.addEventListener('click',function(){press(tabs,t);draw(+t.getAttribute('data-stg'));});});draw(0);}

  /* --- 3 purchase settings --- */
  var stg=document.querySelector('[data-settings]');
  if(stg){var outl=document.querySelector('[data-set-out]');
    function on(k){var x=stg.querySelector('[data-set="'+k+'"]');return x&&x.checked;}
    function sdraw(){var amt=+stg.querySelector('[data-set-amt]').value,bc=stg.querySelector('[data-set-bc]:checked').value,l=[];
      stg.querySelector('[data-set-amt]').disabled=!on('approve');
      l.push(on('approve')?['ok','Buyers confirm orders up to '+inr(amt,false)+'. P00042 for '+inr(761100,false)+' waits as <b>To Approve</b> for the Purchase Manager.']:['warn','Any buyer can confirm any amount. P00042 for '+inr(761100,false)+' goes straight to the vendor.']);
      l.push(on('lock')?['ok','Confirmed POs are locked. Changing a price or quantity needs a manager to unlock it.']:['warn','Confirmed POs can still be edited after the vendor has accepted them.']);
      l.push(bc==='received'?['ok','Bills follow <b>received</b> quantities: 540 m arrived, so the bill is for 540 m, not the 600 m ordered.']:['warn','Bills follow <b>ordered</b> quantities: the full 600 m can be billed before anything arrives.']);
      if(on('match'))l.push(['ok','3-way matching blocks payment of a bill until the goods on it are received.']);
      if(on('agree'))l.push(['ok','Buyers can send one RFQ to several vendors and keep the best offer, or call off from blanket orders.']);
      if(on('warn'))l.push(['ok','Vendors on hold show a warning the moment a buyer selects them.']);
      if(on('uom'))l.push(['ok','Fabric is bought in rolls of 50 m and used in metres. Odoo converts it.']);
      if(on('drop'))l.push(['ok','Selected products ship straight from the vendor to your customer.']);
      outl.innerHTML=l.map(function(x){return '<li class="is-'+x[0]+'">'+x[1]+'</li>';}).join('');}
    stg.addEventListener('change',sdraw);sdraw();}

  /* --- 4 purchase explorer --- */
  var px=document.querySelector('[data-px]');
  if(px){var D=__ORDERS__,V=__VENDORS__,PL=__PRICES__,body=px.querySelector('[data-px-body]'),crumb=px.querySelector('[data-px-crumb]'),q=px.querySelector('[data-px-q]'),facet=px.querySelector('[data-px-facet]');
    var B={A:{n:'Arjun Nair',c:'#3E7CB1'},K:{n:'Kavya Menon',c:'#B5567E'}},ST={draft:'RFQ',sent:'RFQ Sent',approve:'To Approve',purchase:'Purchase Order'},BL={no:'Nothing to Bill',to:'Waiting Bills',done:'Fully Billed'};
    var MN={rfq:'Requests for Quotation',po:'Purchase Orders',vendors:'Vendors',prices:'Vendor Pricelists'};
    var st={menu:'rfq',view:'list',open:null,tab:'lines',f:null},nextP=47;
    D.forEach(function(o){o.log=[{w:'Unisas Bot',t:o.src==='Replenishment'?'Created by a reordering rule':'RFQ created'}];if(o.state==='approve')o.log.push({w:'Unisas Bot',t:'Approval requested from Anita Rao (Purchase Manager): order above '+inr(LIMIT,false)});});
    function untaxed(o){return o.lines.reduce(function(a,l){return a+l[2]*l[3];},0);}
    function total(o){return untaxed(o)*1.18;}
    function av(k){return '<span class="ox-av is-sm" style="--c:'+B[k].c+'">'+B[k].n[0]+'</span>';}
    function badge(s){return '<span class="pu-b pu-b--'+s+'">'+ST[s]+'</span>';}
    function bbadge(s){return '<span class="pu-b pu-b--i'+s+'">'+BL[s]+'</span>';}
    function late(o){return o.late&&(o.state==='draft'||o.state==='sent');}
    function find(id){return D.filter(function(x){return x.id===+id;})[0];}
    function rows(){var t=q.value.trim().toLowerCase();return D.filter(function(o){
      if(st.menu==='po'&&o.state!=='purchase')return false;
      if(st.f==='draft'&&o.state!=='draft')return false;if(st.f==='sent'&&o.state!=='sent')return false;if(st.f==='late'&&!late(o))return false;
      return !t||(o.num+' '+o.vendor).toLowerCase().indexOf(t)>-1;});}
    function dash(){var a=D.filter(function(o){return o.state==='draft';}),w=D.filter(function(o){return o.state==='sent';}),l=D.filter(late),my=function(x){return x.filter(function(o){return o.buyer==='A';}).length;};
      var tot=D.reduce(function(s,o){return s+total(o);},0),pur=D.filter(function(o){return o.state==='purchase';}).reduce(function(s,o){return s+total(o);},0);
      function c(k,n){return '<button type="button" class="pu-dc'+(st.f===k?' is-on':'')+'" data-px-f="'+k+'"><b>'+n+'</b></button>';}
      return '<div class="pu-dash"><div class="pu-dash-l"><span></span><small>To Send</small><small>Waiting</small><small>Late</small><span class="pu-dash-row">All RFQs</span>'+c('draft',a.length)+c('sent',w.length)+c('late',l.length)+
        '<span class="pu-dash-row">My RFQs</span><span class="pu-dc"><b>'+my(a)+'</b></span><span class="pu-dc"><b>'+my(w)+'</b></span><span class="pu-dc"><b>'+my(l)+'</b></span></div>'+
        '<div class="pu-dash-r"><span><small>Avg Order Value</small><b>'+inr(tot/D.length,false)+'</b></span><span><small>Purchased Last 7 Days</small><b>'+inr(pur,false)+'</b></span>'+
        '<span><small>Lead Time to Purchase</small><b>3 Days</b></span><span><small>RFQs Sent Last 7 Days</small><b>'+(w.length+3)+'</b></span></div></div>';}
    function list(l){var po=st.menu==='po';
      return (po?'':dash())+'<div class="ox-scroll"><table class="ox-table"><thead><tr><th class="ox-chk"><span class="ox-cb"></span></th><th></th><th>Reference</th><th>'+(po?'Confirmation Date':'Order Deadline')+'</th><th>Vendor</th><th>Buyer</th><th>Source Document</th><th class="ox-num">Total</th><th>'+(po?'Billing Status':'Status')+'</th></tr></thead><tbody>'+
        (l.length?l.map(function(o){return '<tr data-id="'+o.id+'" tabindex="0"><td class="ox-chk"><span class="ox-cb"></span></td><td><span class="pu-star'+(o.star?' is-on':'')+'">&#9733;</span></td><td><b>'+o.num+'</b></td>'+
          '<td class="'+(late(o)?'pu-late':'')+'">'+o.deadline+'</td><td>'+esc(o.vendor)+'</td><td><span class="ox-sp">'+av(o.buyer)+B[o.buyer].n+'</span></td><td class="ox-muted">'+(o.src||'')+'</td>'+
          '<td class="ox-num"><b>'+inr(total(o))+'</b></td><td>'+(po?bbadge(o.bill||'no'):badge(o.state))+'</td></tr>';}).join(''):'<tr><td colspan="9" class="ox-empty">No order matches.</td></tr>')+'</tbody></table></div>';}
    function kanban(l){var g=['draft','sent','approve','purchase'].filter(function(s){return st.menu!=='po'||s==='purchase';});
      return '<div class="pu-kb">'+g.map(function(s){var c=l.filter(function(o){return o.state===s;});
        return '<div class="pu-kcol"><p class="pu-kcol-h"><b>'+ST[s]+'</b><span>'+c.length+'</span></p>'+c.map(function(o){
          return '<article class="pu-kcard" data-id="'+o.id+'" tabindex="0"><p><b>'+esc(o.vendor)+'</b><b>'+inr(total(o),false)+'</b></p><p><span>'+o.num+' &middot; <span class="'+(late(o)?'pu-late':'')+'">'+o.deadline+'</span></span></p>'+
            '<p class="pu-kfoot"><span class="pu-star'+(o.star?' is-on':'')+'">&#9733;</span>'+badge(o.state)+av(o.buyer)+'</p></article>';}).join('')+'</div>';}).join('')+'</div>';}
    function vendors(){var t=q.value.trim().toLowerCase();
      return '<div class="pu-vgrid">'+V.filter(function(v){return !t||v[0].toLowerCase().indexOf(t)>-1;}).map(function(v){
        return '<article class="pu-vcard"><span class="pu-vlogo" style="--c:'+v[6]+'">'+v[0].split(' ').map(function(w){return w[0];}).join('').slice(0,2)+'</span><div><b>'+v[0]+'</b><small>'+v[1]+', India</small>'+
          '<span class="ox-tag ox-tag--sky">'+v[2]+'</span><p class="pu-vstat"><span>On-time rate</span><i style="--w:'+v[3]+'" class="'+(v[3]<85?'is-low':'')+'"></i><b>'+v[3]+'%</b></p>'+
          '<p class="pu-vfoot"><span>'+v[4]+' Purchases</span><span>'+inr(v[5],false)+'</span></p></div></article>';}).join('')+'</div>';}
    function prices(){var t=q.value.trim().toLowerCase();
      return '<div class="ox-scroll"><table class="ox-table"><thead><tr><th>Vendor</th><th>Product</th><th class="ox-num">Quantity</th><th class="ox-num">Price</th><th class="ox-num">Delivery Lead Time</th><th>End Date</th></tr></thead><tbody>'+
        PL.filter(function(p){return !t||(p[0]+' '+p[1]).toLowerCase().indexOf(t)>-1;}).map(function(p){return '<tr class="is-static"><td>'+p[0]+'</td><td>'+p[1]+'</td><td class="ox-num">'+p[2]+'</td><td class="ox-num"><b>'+inr(p[3])+'</b></td><td class="ox-num">'+p[4]+' days</td><td>'+p[5]+'</td></tr>';}).join('')+'</tbody></table></div>';}
    function form(o){var s=o.state,po=s==='purchase',edit=s==='draft'||s==='sent';
      var vis=['draft','sent'].concat(s==='approve'?['approve']:[]).concat(['purchase']);
      var sb=vis.map(function(x){return '<span class="ox-sb'+(x===s?' is-cur':'')+'">'+ST[x]+'</span>';}).join('');
      var b=s==='draft'?'<button type="button" class="ox-pbtn" data-do="send">Send by Email</button><button type="button" class="ox-sbtn" data-do="print">Print RFQ</button><button type="button" class="ox-sbtn" data-do="confirm">Confirm Order</button>':
            s==='sent'?'<button type="button" class="ox-pbtn" data-do="confirm">Confirm Order</button><button type="button" class="ox-sbtn" data-do="send">Re-Send by Email</button>':
            s==='approve'?'<button type="button" class="ox-pbtn" data-do="approve">Approve Order</button><button type="button" class="ox-sbtn" data-do="cancel">Cancel</button>':
            '<button type="button" class="ox-pbtn" data-do="sendpo">Send PO by Email</button><button type="button" class="ox-sbtn" data-do="print">Print</button>';
      var sm=po?'<div class="pu-smarts">'+smart(TRUCK,'Receipt','1')+smart(BILL,'Vendor Bills',o.bill==='done'?'1':'0')+smart(CLOCK,'On-time Rate','91%')+'</div>':'';
      var tabs='<div class="ox-ftabs pu-ftabs"><button type="button" class="'+(st.tab==='lines'?'is-on':'')+'" data-tab="lines">Products</button>'+(o.alts?'<button type="button" class="'+(st.tab==='alts'?'is-on':'')+'" data-tab="alts">Alternatives</button>':'')+'<button type="button" class="'+(st.tab==='other'?'is-on':'')+'" data-tab="other">Other Information</button></div>';
      var content;
      if(st.tab==='alts'&&o.alts){var mn=Math.min.apply(null,o.alts.map(function(a){return a.p.reduce(function(s,p,k){return s+p*o.lines[k][2];},0);})),fast=Math.min.apply(null,o.alts.map(function(a){return a.d;}));
        content='<p class="pu-alt-note">'+(o.alts.length>1?'Same request sent to '+o.alts.length+' vendors. Compare and keep the best offer; the others are cancelled.':'Alternative chosen. The other RFQs were cancelled.')+'</p><table class="pu-lines"><thead><tr><th>Reference</th><th>Vendor</th><th class="ox-num">Lead Time</th><th class="ox-num">Total</th><th></th></tr></thead><tbody>'+
          o.alts.map(function(a,k){var t=a.p.reduce(function(s,p,j){return s+p*o.lines[j][2];},0);
            return '<tr><td><b>'+a.num+'</b></td><td>'+a.v+(t===mn&&o.alts.length>1?' <span class="pu-tag pu-tag--cfg">Best price</span>':'')+(a.d===fast&&o.alts.length>1?' <span class="pu-tag pu-tag--studio">Fastest</span>':'')+'</td><td class="ox-num">'+a.d+' days</td><td class="ox-num"><b>'+inr(t*1.18)+'</b></td>'+
            '<td class="ox-num">'+(o.alts.length>1?'<button type="button" class="ox-sbtn" data-alt="'+k+'">Choose</button>':'<span class="pu-st is-ok">Kept</span>')+'</td></tr>';}).join('')+'</tbody></table>';}
      else if(st.tab==='other'){content='<dl class="ox-fields pu-other"><div><dt>Buyer</dt><dd>'+av(o.buyer)+B[o.buyer].n+'</dd></div><div><dt>Source Document</dt><dd>'+(o.src||'&mdash;')+'</dd></div><div><dt>Incoterm</dt><dd>FCA</dd></div><div><dt>Payment Terms</dt><dd>30 Days</dd></div><div><dt>Fiscal Position</dt><dd>Intra State (Tamil Nadu)</dd></div><div><dt>Deliver To</dt><dd>Chennai: Receipts</dd></div></dl>';}
      else{content='<table class="pu-lines"><thead><tr><th>Product</th><th class="ox-num">Quantity</th>'+(po?'<th class="ox-num">Received</th><th class="ox-num">Billed</th>':'')+'<th class="ox-num">Unit Price</th><th>Taxes</th><th class="ox-num">Amount</th></tr></thead><tbody>'+
        o.lines.map(function(l,k){var rec=po&&o.bill!=='no'?l[2]:0,bil=o.bill==='done'?l[2]:0;
          return '<tr><td><b>'+esc(l[0])+'</b><small>'+esc(l[1])+'</small></td><td class="ox-num">'+(edit?'<span class="pu-qty"><button type="button" data-q="-1" data-l="'+k+'" aria-label="Decrease">&minus;</button><b>'+l[2]+'</b><button type="button" data-q="1" data-l="'+k+'" aria-label="Increase">+</button></span>':l[2]+'.00')+' <small class="pu-uom">'+l[4]+'</small></td>'+
          (po?'<td class="ox-num">'+rec+'.00</td><td class="ox-num">'+bil+'.00</td>':'')+'<td class="ox-num">'+inr(l[3])+'</td><td><span class="pu-gst">GST 18%</span></td><td class="ox-num">'+inr(l[2]*l[3])+'</td></tr>';}).join('')+'</tbody></table>'+
        '<div class="pu-tot"><span>Untaxed Amount:</span><b>'+inr(untaxed(o))+'</b><span>GST 18%:</span><b>'+inr(untaxed(o)*0.18)+'</b><span class="is-total">Total:</span><b class="is-total">'+inr(total(o))+'</b></div>';}
      var log=o.log.slice().reverse().map(function(l){return '<div class="ox-msg"><span class="ox-av is-bot">U</span><div><p><b>'+l.w+'</b> <small>just now</small></p><p>'+l.t+'</p></div></div>';}).join('');
      return '<div class="ox-form pu-form"><div class="ox-f-main"><div class="ox-f-bar"><span class="ox-f-btns">'+b+'</span><span class="ox-sbar">'+sb+'</span></div>'+
        '<div class="ox-sheet">'+sm+'<p class="pu-doc-kind">'+(po?'Purchase Order':'Request for Quotation')+'</p><h3>'+o.num+'</h3><dl class="ox-fields"><div><dt>Vendor</dt><dd>'+esc(o.vendor)+'</dd></div><div><dt>'+(po?'Confirmation Date':'Order Deadline')+'</dt><dd class="'+(late(o)?'pu-late':'')+'">'+o.deadline+', 2026</dd></div>'+
        '<div><dt>Vendor Reference</dt><dd>'+(o.ref||'<span class="ox-muted">&mdash;</span>')+'</dd></div><div><dt>Expected Arrival</dt><dd>'+(o.arr||'Oct 15')+', 2026</dd></div></dl>'+tabs+content+'</div></div>'+
        '<aside class="ox-chatter"><div class="ox-ch-btns"><span class="ox-pbtn">Send message</span><span class="ox-sbtn">Log note</span><span class="ox-sbtn">Activity</span></div><p class="ox-ch-sep">Today</p>'+log+'</aside></div>';}
    function render(){var grid=st.menu==='rfq'||st.menu==='po';
      px.querySelector('[data-px-views]').style.visibility=grid&&!st.open?'visible':'hidden';
      px.querySelectorAll('[data-px-view]').forEach(function(b){var on=b.getAttribute('data-px-view')===st.view;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
      px.querySelectorAll('[data-px-menu]').forEach(function(b){var on=b.getAttribute('data-px-menu')===st.menu;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
      facet.hidden=!st.f||!!st.open;facet.textContent={draft:'To Send',sent:'Waiting',late:'Late'}[st.f]||'';
      if(st.open){var o=find(st.open);crumb.innerHTML='<a href="#" data-px-back>'+MN[st.menu]+'</a><span>'+o.num+'</span>';body.innerHTML=form(o);return;}
      crumb.textContent=MN[st.menu];
      body.innerHTML=st.menu==='vendors'?vendors():st.menu==='prices'?prices():(st.view==='kanban'?kanban(rows()):list(rows()));}
    function log(o,t,w){o.log.push({w:w||'Unisas Bot',t:t});}
    function confirm(o){if(total(o)>LIMIT){o.state='approve';log(o,'Order of '+inr(total(o),false)+' is above the '+inr(LIMIT,false)+' limit. <span class="pu-track">Status: <b>To Approve</b></span> Anita Rao notified.');}
      else{o.state='purchase';o.bill='no';log(o,'<span class="pu-track">Status: RFQ &rarr; <b>Purchase Order</b></span>');log(o,'Receipt WH/IN/000'+(12+o.id)+' created, expected in Chennai warehouse');}}
    px.addEventListener('click',function(e){
      var m=e.target.closest('[data-px-menu]');if(m){st.menu=m.getAttribute('data-px-menu');st.open=null;st.f=null;render();return;}
      var v=e.target.closest('[data-px-view]');if(v){st.view=v.getAttribute('data-px-view');st.open=null;render();return;}
      var f=e.target.closest('[data-px-f]');if(f){var k=f.getAttribute('data-px-f');st.f=st.f===k?null:k;st.view='list';render();return;}
      if(e.target.closest('[data-px-back]')){e.preventDefault();st.open=null;render();return;}
      var o=st.open&&find(st.open);
      var tb=e.target.closest('[data-tab]');if(tb&&o){st.tab=tb.getAttribute('data-tab');render();return;}
      var qb=e.target.closest('[data-q]');if(qb&&o){var l=o.lines[+qb.getAttribute('data-l')];l[2]=Math.max(1,l[2]+(+qb.getAttribute('data-q'))*10);render();return;}
      var al=e.target.closest('[data-alt]');if(al&&o){var a=o.alts[+al.getAttribute('data-alt')],others=o.alts.filter(function(x){return x!==a;}).map(function(x){return x.num;});
        o.vendor=a.v;o.num=a.num;a.p.forEach(function(p,k){o.lines[k][3]=p;});o.alts=[a];log(o,'Kept the offer from <b>'+a.v+'</b>. Alternatives '+others.join(', ')+' cancelled.');render();return;}
      var d=e.target.closest('[data-do]');
      if(d&&o){var x=d.getAttribute('data-do');
        if(x==='send'){if(o.state==='draft')o.state='sent';log(o,'RFQ emailed to '+esc(o.vendor)+' <span class="pu-track">Status: <b>RFQ Sent</b></span>',B[o.buyer].n);}
        if(x==='confirm')confirm(o);
        if(x==='approve'){o.state='purchase';o.bill='no';log(o,'Approved. <span class="pu-track">Status: To Approve &rarr; <b>Purchase Order</b></span>','Anita Rao');log(o,'Receipt WH/IN/000'+(12+o.id)+' created');}
        if(x==='cancel'){o.state='draft';log(o,'Sent back to the buyer for a better price','Anita Rao');}
        if(x==='sendpo')log(o,'Purchase order emailed to '+esc(o.vendor)+' with a receipt reminder 2 days before arrival',B[o.buyer].n);
        if(x==='print')log(o,'PDF downloaded',B[o.buyer].n);
        render();return;}
      var r=e.target.closest('[data-id]');if(r){st.open=+r.getAttribute('data-id');st.tab='lines';render();}});
    px.addEventListener('keydown',function(e){if(e.key==='Enter'){var r=e.target.closest&&e.target.closest('[data-id]');if(r){st.open=+r.getAttribute('data-id');st.tab='lines';render();}}});
    px.querySelector('[data-px-new]').addEventListener('click',function(){var o={id:100+nextP,num:'P000'+(nextP++),vendor:'Sri Lakshmi Metals',ref:'',buyer:'A',deadline:'Oct 08',late:false,state:'draft',src:'',star:false,
      lines:[['Steel chair frame','Powder-coated, black',100,1850,'Units']],log:[{w:'Arjun Nair',t:'RFQ created. Price and lead time filled from the vendor pricelist.'}]};D.unshift(o);st.menu='rfq';st.open=o.id;st.tab='lines';render();});
    q.addEventListener('input',function(){st.open=null;render();});
    render();}

  /* --- 6 three-way match --- */
  var tw=document.querySelector('[data-tw]');
  if(tw){var L=[['Steel chair frame',100,1850],['Gas lift cylinder',100,690]],t={rec:0,bill:0};
    var apps={sales:tw.querySelector('[data-tw-app="sales"]'),inv:tw.querySelector('[data-tw-app="inv"]'),acc:tw.querySelector('[data-tw-app="acc"]')};
    var R1=tw.querySelector('[data-tw-do="rec1"]'),R2=tw.querySelector('[data-tw-do="rec2"]'),BB=tw.querySelector('[data-tw-do="bill"]');
    function say(k,txt){apps[k].querySelector('[data-tw-txt]').innerHTML=txt;apps[k].classList.remove('is-hot');void apps[k].offsetWidth;apps[k].classList.add('is-hot');}
    function tdraw(){tw.querySelector('[data-tw-lines]').innerHTML=L.map(function(l){return '<tr><td><b>'+l[0]+'</b></td><td class="ox-num">'+l[1]+'.00</td><td class="ox-num'+(t.rec?' pu-in':'')+'">'+t.rec+'.00</td><td class="ox-num'+(t.bill?' pu-in':'')+'">'+t.bill+'.00</td><td class="ox-num">'+inr(l[2])+'</td><td class="ox-num">'+inr(l[1]*l[2])+'</td></tr>';}).join('');
      var rs=t.rec===0?['','Not Received']:t.rec<100?['is-to','Partially Received']:['is-ok','Fully Received'];
      var bs=t.bill===100?['is-ok','Fully Billed']:t.rec>t.bill?['is-to','Waiting Bills']:['','Nothing to Bill'];
      tw.querySelector('[data-tw-rs]').innerHTML='<span class="pu-st '+rs[0]+'">'+rs[1]+'</span>';tw.querySelector('[data-tw-bs]').innerHTML='<span class="pu-st '+bs[0]+'">'+bs[1]+'</span>';
      tw.querySelector('[data-tw-smart]').innerHTML=smart(TRUCK,'Receipts',t.rec?'2':'1')+smart(BILL,'Vendor Bills',t.bill?(t.split?'2':'1'):'0');
      R1.disabled=t.rec>0;R2.disabled=t.rec!==60;BB.disabled=t.bill>=t.rec;
      R1.className=t.rec>0?'ox-sbtn':'ox-pbtn';R2.className=t.rec===60&&t.bill===60?'ox-pbtn':'ox-sbtn';BB.className=t.rec>t.bill&&!(t.rec===60&&t.bill===60)?'ox-pbtn':'ox-sbtn';}
    tw.addEventListener('click',function(e){var b=e.target.closest('[data-tw-do]');if(!b||b.disabled)return;var k=b.getAttribute('data-tw-do');
      if(k==='rec1'){t.rec=60;say('inv','WH/IN/00012 validated: 60 + 60 received. Backorder <b>WH/IN/00013</b> created for the other 40.');say('sales','60 chairs can now be built. S00482 shows a partial availability date.');say('acc','Stock valued at '+inr(60*2540,false)+'. A bill can now be raised for 60 units.');}
      if(k==='rec2'){t.rec=100;say('inv','Backorder WH/IN/00013 validated. All 100 sets received.');say('sales','S00482 is ready to build and deliver in full.');say('acc',t.bill?'40 more units are ready to bill.':'100 units are ready to bill.');}
      if(k==='bill'){var n=t.rec-t.bill;if(t.bill)t.split=true;t.bill=t.rec;say('acc','Bill <b>BILL/2026/10/00'+(t.split?'08':'07')+'</b> for '+n+' units, '+inr(n*2540*1.18)+' incl. GST. It matches the PO and the receipt.');}
      if(k==='reset'){t={rec:0,bill:0};say('sales','S00482 for 100 chairs triggered this PO (make to order). The salesperson sees the expected date.');say('inv','Receipt WH/IN/00012 is waiting for 100 frames and 100 cylinders.');say('acc','Nothing to bill yet. Bill control is set to received quantities.');}
      tdraw();});
    tdraw();}

  /* --- 7 bill digitisation --- */
  var oc=document.querySelector('[data-ocr]');
  if(oc){var go=oc.querySelector('[data-ocr-go]'),fs=[].slice.call(oc.querySelectorAll('[data-ocr-f]')),res=oc.querySelector('[data-ocr-res]'),stt=oc.querySelector('[data-ocr-st]'),tm=[];
    go.addEventListener('click',function(){tm.forEach(clearTimeout);tm=[];fs.forEach(function(f){f.classList.remove('is-on');});res.className='pu-ocr-res';res.textContent='';go.disabled=true;
      stt.textContent='Digitizing…';stt.className='pu-ocr-st is-busy';oc.querySelector('[data-ocr-name]').textContent='Draft';
      fs.forEach(function(f,i){tm.push(setTimeout(function(){f.classList.add('is-on');},350+i*260));});
      tm.push(setTimeout(function(){stt.textContent='Draft';stt.className='pu-ocr-st';oc.querySelector('[data-ocr-name]').textContent='BILL/2026/10/0007';res.className='pu-ocr-res is-ok';
        res.innerHTML='Matched to <b>P00040</b>: 600 m ordered, 600 m received. GSTIN verified on the GST portal. Ready to post.';go.disabled=false;go.textContent='Run again';},350+fs.length*260+300));});}

  /* --- 8 configure vs customize --- */
  var cv=document.querySelector('[data-cvc]');
  if(cv){var RQ=JSON.parse(document.getElementById('pu-reqs').textContent),rb=[].slice.call(cv.querySelectorAll('[data-req]'));
    function vdraw(i){var r=RQ[i],k=cv.querySelector('[data-v-kind]');k.textContent=r[1];k.className='pu-v-kind pu-tag pu-tag--'+r[2];
      cv.querySelector('[data-v-req]').innerHTML=r[0];cv.querySelector('[data-v-how]').innerHTML=r[3];cv.querySelector('[data-v-with]').textContent=r[4];cv.querySelector('[data-v-eff]').textContent=r[5];}
    rb.forEach(function(b){b.addEventListener('click',function(){press(rb,b);vdraw(+b.getAttribute('data-req'));});});vdraw(0);}

  /* --- 11 go-live readiness --- */
  var ub=document.querySelector('[data-uatbox]');
  if(ub){var cb=[].slice.call(ub.querySelectorAll('[data-uat]'));
    function udraw(){var n=cb.filter(function(c){return c.checked;}).length,p=Math.round(n/cb.length*100);
      ub.querySelector('[data-uat-pct]').textContent=p+'%';ub.querySelector('[data-uat-bar]').style.width=p+'%';ub.classList.toggle('is-ready',p===100);
      ub.querySelector('[data-uat-res]').innerHTML=p===100?'<b>Ready for go-live.</b> Every role has signed off its scenarios.':(cb.length-n)+' scenario'+(cb.length-n===1?'':'s')+' left before the purchase team signs off.';}
    ub.addEventListener('change',udraw);udraw();}

  /* --- 12 purchase analysis --- */
  var pa=document.querySelector('[data-pa]');
  if(pa){var VN=['Sri Lakshmi','Ambika','Shakti','Pioneer','Deccan','Kovai'],M=[['Untaxed Total',[2240000,1935000,1008000,836000,768000,281600],function(v){return inr(v,false).replace('₹ ','₹');}],
      ['On-Time Rate',[96,84,79,98,91,88],function(v){return v+'%';}],['Days to Receive',[6.5,4.8,13.2,2.9,11.4,3.6],function(v){return v.toFixed(1);}],['Qty Ordered',[1210,900,2400,22000,240,520],function(v){return v.toLocaleString('en-IN');}]];
    var plot=pa.querySelector('[data-pa-plot]'),ya=pa.querySelector('[data-pa-y]'),mb2=[].slice.call(pa.querySelectorAll('[data-pa-m]'));
    function pdraw(i){var m=M[i],mx=i===1?100:Math.max.apply(null,m[1])*1.15;
      ya.innerHTML=[1,0.75,0.5,0.25,0].map(function(f){return '<span>'+m[2](i===1?Math.round(mx*f):i===2?mx*f:Math.round(mx*f))+'</span>';}).join('');
      plot.innerHTML=VN.map(function(n,k){return '<div class="ox-gcol"><div class="ox-gwrap"><span class="ox-gbar'+(i===1&&m[1][k]<85?' is-low':'')+'" style="--h:'+(m[1][k]/mx*100).toFixed(1)+'"><em>'+m[2](m[1][k])+'</em></span></div><small>'+n+'</small></div>';}).join('');
      pa.querySelector('[data-pa-leg]').textContent=m[0];}
    mb2.forEach(function(b){b.addEventListener('click',function(){press(mb2,b);pdraw(+b.getAttribute('data-pa-m'));});});pdraw(0);}

  /* --- 13 readiness quiz --- */
  var qz=document.querySelector('[data-quiz]');
  if(qz){var ans={};
    qz.addEventListener('click',function(e){var b=e.target.closest('[data-q]');if(!b)return;var k=b.getAttribute('data-q');ans[k]=+b.getAttribute('data-a');
      press([].slice.call(qz.querySelectorAll('[data-q="'+k+'"]')),b);
      var n=Object.keys(ans).length,y=Object.keys(ans).reduce(function(s,x){return s+ans[x];},0),txt;
      qz.querySelector('[data-quiz-score]').textContent=y+' / 6';
      txt=n<6?'Keep going: '+(6-n)+' question'+(6-n===1?'':'s')+' left.':y>=4?'<b>You are ready.</b> Your purchasing has outgrown email and spreadsheets. Odoo Purchase with approvals and three-way matching will pay back quickly.':
        y>=2?'<b>Nearly there.</b> Start with RFQs, vendor pricelists and receipts, then add approvals as volume grows.':'<b>Start simple.</b> Odoo Purchase can grow with you. A short call will show you what is worth setting up now.';
      qz.querySelector('[data-quiz-txt]').innerHTML=txt;qz.classList.toggle('is-done',n===6);});}
})();
</script>
'''

CTA = ("Let's Connect Your Procure-to-Pay in Odoo",
       "Tell us how you request, approve, receive and pay for purchases. We&rsquo;ll show the same flow in Odoo Purchase.")
