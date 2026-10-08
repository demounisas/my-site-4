"""
Odoo Inventory page (odoo-inventory.html). Every section is modelled on a real
Odoo Inventory screen (demo.odoo.com/odoo/inventory): Overview cards, Moves
History, Stock report, Warehouse routes, Replenishment, the Barcode app,
Traceability, Forecasted report, Import and Stock Valuation.
Shared Odoo look: dist/assets/odoo-ui.css. Page styles: dist/assets/inventory.css.

hero(g) and build(g) get the build script's globals.
"""
import json

from crm_explorer import ic, SEARCH, FUNNEL

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CROSS = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
SCAN = ic('<path d="M4 7V5a1 1 0 0 1 1-1h2M17 4h2a1 1 0 0 1 1 1v2M20 17v2a1 1 0 0 1-1 1h-2M7 20H5a1 1 0 0 1-1-1v-2"/><path d="M8 8v8M11 8v8M14 8v8M17 8v8"/>', 18, 1.8)
ARROW_R = ic('<path d="M5 12h14M13 6l6 6-6 6"/>', 14, 2)


def inr(n, dec=False):
    """Indian-format rupees: 12,00,000"""
    whole = int(round(n))
    neg = whole < 0
    digits = "%d" % abs(whole)
    rest, last3 = digits[:-3], digits[-3:]
    groups = []
    while len(rest) > 2:
        groups.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.insert(0, rest)
    out = ",".join(groups + [last3]) if groups else last3
    return ("&minus;" if neg else "") + "&#8377; " + out + (".00" if dec else "")


def head(eyebrow, title, sub="", cls=""):
    return ('<div class="iv-head%s"><p class="iv-eyebrow mono">%s</p><h2 class="iv-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="iv-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="iv-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


def odoo_nav(app_icon, app, menus):
    return ('<div class="ox-nav"><span class="ox-app">%s<b>%s</b></span>%s<span class="ox-nav-r"><span class="ox-company">Your Company</span>'
            '<span class="ox-av" style="--c:#6B5B95">Y</span></span></div>' % (app_icon, app, "".join('<span class="ox-menu">%s</span>' % m for m in menus)))


MENUS = ["Overview", "Operations", "Products", "Reporting", "Configuration"]
MENUS_S = ["Operations", "Products", "Reporting"]


def steps(items):
    return '<ol class="iv-steps">%s</ol>' % "".join('<li><span class="iv-step-n mono">%02d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i + 1, t, x)
                                                     for i, (t, x) in enumerate(items))


def op_card(name, wh, todo, links, bars, late_bar=None):
    """An Odoo Inventory Overview card for one operation type."""
    lk = "".join('<li%s><span>%s</span><b>%d</b></li>' % (' class="is-late"' if n == "Late" else "", n, v) for n, v in links)
    labels = ["Before", "Yesterday", "Today", "Tomorrow", "After"]
    mx = max(bars) or 1
    gb = "".join('<span%s><i style="--h:%d"></i><small>%s</small></span>' % (' class="is-late"' if i == late_bar else "", round(v / mx * 100), labels[i])
                 for i, v in enumerate(bars))
    return ('<div class="iv-op"><p class="iv-op-h"><b>%s</b><small>%s</small></p><div class="iv-op-b"><span class="iv-op-btn">%d To Process</span><ul>%s</ul></div>'
            '<div class="iv-op-g">%s</div></div>' % (name, wh, todo, lk, gb))


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">Inventory</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["Live stock in every warehouse", "Barcode, lots &amp; serials", "Reorders that raise themselves"])
    copy = ('<div class="iv-hero-copy">%s<p class="iv-eyebrow mono">ODOO INVENTORY IMPLEMENTATION</p>'
            '<h1 class="iv-h1">Inventory Implementation Services <span>Tailored to Your Business with Odoo</span></h1>'
            '<p class="iv-lead">We set up Odoo Inventory around your warehouses, so stock updates as it moves and reorders go out on time.</p><ul class="iv-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Discuss Odoo Inventory %s</a>'
            '<a href="#explore" class="btn btn-ghost">Explore live stock</a></div></div>' % (crumb, points, g["ARROW"]))
    # a receipt being scanned on the shop floor with the Odoo Barcode app
    bars = "".join('<i style="width:%dpx"></i>' % w for w in (2, 1, 3, 1, 2, 2, 1, 3, 1, 1, 2, 3, 1, 2, 1, 1, 3, 2, 1, 2, 2, 1, 3, 1))
    lines = [("Steel chair frame", "LOT-2610-A", 60, 60, "done"), ("Gas lift cylinder", "Class 4, 100 mm", 24, 60, "cur"), ("Seat foam pad", "45 x 45 cm", 0, 60, "")]
    rows = "".join('<li class="is-%s"><span><b>%s</b><small>%s</small></span><em>%d <i>/ %d</i></em><span class="iv-hx-qbar"><i style="width:%d%%"></i></span></li>'
                   % (st or "todo", n, d, q, t, q * 100 // t) for n, d, q, t, st in lines)
    dash = ('<div class="iv-hero-vis iv-hx-phone" aria-label="Odoo Barcode app scanning a receipt"><div class="iv-hx-screen">'
            '<p class="iv-hx-sb"><span>11:42</span><span>5G &#9646;&#9646;&#9646;</span></p>'
            '<p class="iv-hx-bar"><span>&larr;</span><b>CHN/IN/00009</b><small>Receipt</small></p>'
            '<div class="iv-hx-cam"><span class="iv-hx-code">%s</span><i class="iv-hx-laser"></i><span class="iv-hx-cnr"></span></div>'
            '<p class="iv-hx-scan">%s<span><b>Gas lift cylinder</b><small>8 901234 567893 &middot; +1</small></span></p>'
            '<p class="iv-hx-loc"><small>From</small>Sri Lakshmi Metals<small>To</small><b>WH/Stock/Shelf A-02</b></p>'
            '<ul class="iv-hx-lines">%s</ul><span class="iv-hx-val">Validate</span></div></div>' % (bars, SCAN, rows))
    return ('<section class="iv-hero iv-hx"><div class="iv-hx-photo">%s%s</div></section>' % (copy, dash))


# ------------------------------------------------------------------ data
WH = {"CHN": "Chennai", "BLR": "Bengaluru", "CBE": "Coimbatore"}
# ref, name, unit, cost, min, tracking, {wh: [on hand, reserved, incoming, outgoing, [(location, qty)]]}
PRODUCTS = [
    ["FURN-0101", "Ergo task chair", "Units", 5900, 30, "", {
        "CHN": [40, 24, 60, 24, [["Shelf A-02", 28], ["Shelf A-03", 12]]], "BLR": [18, 6, 0, 6, [["Stock", 18]]], "CBE": [6, 0, 20, 0, [["Stock", 6]]]}],
    ["FURN-0204", "Height-adjustable desk", "Units", 23400, 10, "", {
        "CHN": [9, 9, 12, 12, [["Shelf C-01", 9]]], "BLR": [4, 2, 0, 2, [["Stock", 4]]], "CBE": [0, 0, 0, 0, []]}],
    ["FURN-0310", "Storage rack, 5 tier", "Units", 4100, 20, "", {
        "CHN": [64, 20, 0, 20, [["Bulk B-04", 64]]], "BLR": [12, 0, 0, 0, [["Stock", 12]]], "CBE": [3, 0, 20, 0, [["Stock", 3]]]}],
    ["FURN-0122", "Visitor chair", "Units", 2650, 25, "", {
        "CHN": [52, 40, 0, 40, [["Shelf B-01", 52]]], "BLR": [10, 0, 0, 0, [["Stock", 10]]], "CBE": [14, 0, 0, 0, [["Stock", 14]]]}],
    ["COMP-2210", "Desk frame motor", "Units", 3200, 20, "Serial", {
        "CHN": [31, 12, 40, 12, [["Components D-02", 31]]], "BLR": [0, 0, 0, 0, []], "CBE": [0, 0, 0, 0, []]}],
    ["COMP-0450", "Seat foam adhesive", "L", 640, 15, "Lot", {
        "CHN": [22, 6, 0, 6, [["Components D-05 &middot; LOT-2026-0912", 14], ["Components D-05 &middot; LOT-2026-0807", 8]]], "BLR": [0, 0, 0, 0, []], "CBE": [0, 0, 0, 0, []]}],
]

# date, reference, product, from, to, qty, app, origin
MOVES = [
    ["Oct 01, 09:12", "CHN/IN/00009", "Ergo task chair", "Partners/Vendors", "CHN/Stock/Shelf A-02", 60, "purchase", "P00031 &middot; Sri Lakshmi Metals"],
    ["Oct 01, 10:40", "CHN/OUT/00031", "Ergo task chair", "CHN/Stock/Shelf A-02", "Partners/Customers", 24, "sales", "S00482 &middot; Bluebay Retail"],
    ["Oct 01, 11:05", "CHN/MO/00213", "Desk frame motor", "CHN/Stock/Components D-02", "Virtual/Production", 12, "mrp", "Component consumed"],
    ["Oct 01, 11:52", "CHN/MO/00213", "Height-adjustable desk", "Virtual/Production", "CHN/Stock/Shelf C-01", 12, "mrp", "Finished product"],
    ["Oct 01, 12:30", "CHN/INT/00004", "Storage rack, 5 tier", "CHN/Stock/Bulk B-04", "Transit/Coimbatore", 20, "internal", "Replenish Coimbatore"],
    ["Oct 01, 14:15", "Physical Inventory", "Visitor chair", "Virtual/Inventory adjustment", "CHN/Stock/Shelf B-01", 2, "adjust", "Cycle count, Shelf B-01"],
    ["Oct 01, 15:02", "BLR/OUT/00118", "Ergo task chair", "BLR/Stock", "Partners/Customers", 6, "sales", "S00491 &middot; Website order"],
    ["Oct 01, 16:20", "CHN/OUT/00032", "Visitor chair", "CHN/Stock/Shelf B-01", "Partners/Customers", 40, "sales", "S00476 &middot; Orbit Motors"],
    ["Oct 01, 17:45", "CHN/IN/00010", "Seat foam adhesive", "Partners/Vendors", "CHN/Stock/Components D-05", 14, "purchase", "P00033 &middot; Kovai Chemicals"],
]

# product, location, on hand, forecast, route, vendor, min, max
REPLEN = [
    ["Ergo task chair", "CBE/Stock", 6, 26, "Buy", "Sri Lakshmi Metals", 30, 80],
    ["Height-adjustable desk", "CHN/Stock", 9, 9, "Manufacture", "CHN/MO", 10, 30],
    ["Desk frame motor", "CHN/Stock", 31, 19, "Buy", "Deccan Motors", 20, 60],
    ["Seat foam adhesive", "CHN/Stock", 22, 16, "Buy", "Kovai Chemicals", 15, 40],
    ["Storage rack, 5 tier", "BLR/Stock", 12, 12, "Resupply from CHN", "CHN/INT", 20, 50],
]


# ------------------------------------------------------------------ sections
def build(g):
    out = ""
    inv_icon = g["TILE_ICONS"][3]

    # 1 ---- can your system keep up? the spreadsheet everyone edits
    signs = ["Stock figures differ between the warehouse, sales and accounts", "Shortages are found when the order is already promised",
             "Each branch keeps its own sheet, updated at day end", "Nobody can say which batch went to which customer",
             "Stock value is worked out once a month, by hand"]
    rows = [("FURN-0101", "Ergo task chair", "40", "18", "6", "29 Sep"), ("FURN-0204", "Height-adj. desk", "9", "4", "#REF!", "12 Sep"),
            ("FURN-0310", "Storage rack", "64", "12", "3", "29 Sep"), ("FURN-0122", "Visitor chair", "52", "?", "14", "18 Sep"),
            ("COMP-2210", "Desk motor", "31", "", "", "02 Sep")]
    grid = "".join('<tr><th>%d</th>%s</tr>' % (i + 2, "".join('<td%s>%s</td>' % (' class="is-err"' if v in ("#REF!", "?") else "", v) for v in r))
                   for i, r in enumerate(rows))
    sheet = ('<div class="iv-xl" aria-label="Example stock spreadsheet with conflicting numbers">'
             '<div class="iv-xl-bar"><i></i><i></i><i></i><b>stock_master_FINAL_v7 (2).xlsx</b><small>Edited by 4 people</small></div>'
             '<div class="iv-xl-fx"><span>C2</span><span>fx</span><span>=40-Dispatch!C14</span></div>'
             '<div class="iv-xl-scroll"><table><thead><tr><th></th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th></tr>'
             '<tr class="is-h"><th>1</th><td>Item code</td><td>Item</td><td>Chennai</td><td>Bengaluru</td><td>Coimbatore</td><td>Updated</td></tr></thead><tbody>%s</tbody></table></div>'
             '<div class="iv-xl-tabs"><span class="is-on">Chennai</span><span>BLR_new</span><span>Copy of CBE</span><span>Dispatch</span></div>'
             '<p class="iv-note-pin is-1"><b>Karthik (Warehouse)</b>Counted 37 on Friday, not 40. Who changed it?</p>'
             '<p class="iv-note-pin is-2"><b>Divya (Accounts)</b>Is this the sheet with September&rsquo;s value?</p></div>' % grid)
    out += sec('<div class="iv-ready"><div>%s<ul class="iv-signs">%s</ul><p class="iv-note">If two or more of these sound familiar, your stock has outgrown spreadsheets '
               'and standalone billing software.</p></div>%s</div>'
               % (head("READINESS CHECK", "Can Your Inventory System Keep Up With Your Growing Operations?",
                       "More SKUs, more locations and more channels all put pressure on the same weak point: one shared file that is never quite current."),
                  "".join('<li>%s%s</li>' % (CROSS, s) for s in signs), sheet), "iv-sec--ready")

    # 2 ---- one move, every app: Moves History with app filter
    apps = [("all", "All moves", "#495057"), ("purchase", "Purchase", "#E06F5F"), ("sales", "Sales", "#EE8A3C"), ("mrp", "Manufacturing", "#8E4F83"),
            ("internal", "Internal transfer", "#1F8A78"), ("adjust", "Stock count", "#3E7CB1")]
    chips = "".join('<button type="button" class="iv-app%s" data-mv="%s" style="--c:%s" aria-pressed="%s"><i></i>%s<b>%d</b></button>'
                    % (" is-on" if k == "all" else "", k, c, "true" if k == "all" else "false", n,
                       len(MOVES) if k == "all" else len([m for m in MOVES if m[6] == k])) for k, n, c in apps)
    mrows = "".join('<tr data-app="%s"><td>%s</td><td><b>%s</b><small>%s</small></td><td>%s</td><td class="ox-muted">%s</td><td>%s</td>'
                    '<td class="ox-num"><b class="%s">%d.00</b></td><td><span class="iv-done">Done</span></td></tr>'
                    % (a, d, r, o, p, f, t, "iv-in" if t.startswith(("CHN/Stock", "BLR/Stock", "CBE/Stock")) else "iv-out", q)
                    for d, r, p, f, t, q, a, o in MOVES)
    effects = [("Sales", "Free-to-use stock shown on every order line, deliveries created on confirmation"),
               ("Purchase", "Receipts expected from each PO, bills checked against what arrived"),
               ("Manufacturing", "Components reserved and consumed, finished goods put away"),
               ("Accounting", "Every move posts its stock value, no month-end re-entry")]
    out += sec(head("ONE DATABASE", "How Can Odoo Connect Inventory, Warehouses and Business Operations?",
                    "In Odoo, every app moves stock through the same ledger. Filter one day of real movements by the app that created them.", "is-center")
               + '<div class="iv-moves"><div class="iv-apps" role="group" aria-label="Filter moves by app">%s</div>'
                 '<div class="ox iv-ox">%s<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb">Moves History</span></div>'
                 '<span class="ox-search">%s<span class="ox-facet">%sDone</span><span class="ox-facet" data-mv-facet hidden></span></span><span></span></div>'
                 '<div class="ox-scroll iv-moves-scroll"><table class="ox-table"><thead><tr><th>Date</th><th>Reference</th><th>Product</th><th>From</th><th>To</th>'
                 '<th class="ox-num">Quantity</th><th>Status</th></tr></thead><tbody>%s</tbody></table></div></div></div>'
                 % (chips, odoo_nav(inv_icon, "Inventory", MENUS), SEARCH, FUNNEL, mrows)
               + '<ul class="iv-effects">%s</ul>' % "".join('<li><b>%s</b><span>%s</span></li>' % e for e in effects), "iv-sec--moves")

    # 3 ---- what can it manage: live stock explorer
    feats = [("Warehouses &amp; bins", "Every warehouse, zone, rack and shelf as its own location."),
             ("Free vs reserved", "See what is promised and what is still free to sell."),
             ("Incoming &amp; outgoing", "Forecasts built from confirmed POs, SOs and MOs."),
             ("Units &amp; packages", "Buy in boxes, store in units, sell by the pack.")]
    out += sec(head("WHAT ODOO INVENTORY MANAGES", "What Can Odoo Inventory Manage Across Your Warehouses?",
                    "One stock report for every warehouse. Switch warehouse, search a product, and open a row to see exactly which shelf holds it.", "is-center")
               + '<div class="ox iv-ox" data-st>%s<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb">Stock</span></div>'
                 '<label class="ox-search">%s<span class="ox-facet">%s<span data-st-facet>All Warehouses</span></span><input type="search" placeholder="Search product..." aria-label="Search products" data-st-q></label>'
                 '<div class="iv-whs" role="group" aria-label="Warehouse">%s</div></div><div class="ox-body iv-st-body" data-st-body></div></div>'
                 '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview with sample data. Pick a warehouse, then open a product to see its locations.</p>'
                 % (odoo_nav(inv_icon, "Inventory", MENUS), SEARCH, FUNNEL,
                    "".join('<button type="button" class="iv-wh%s" data-wh="%s" aria-pressed="%s">%s</button>' % (" is-on" if k == "ALL" else "", k, "true" if k == "ALL" else "false", n)
                            for k, n in [("ALL", "All")] + [(k, k) for k in WH]))
               + '<ul class="iv-feats">%s</ul>' % "".join('<li><b>%s</b><span>%s</span></li>' % f for f in feats), "iv-sec--explore", "explore")

    # 4 ---- configure around your workflows: warehouse routes
    impl = [("Walk your warehouse", "We follow goods from the dock to the shelf to the truck, and note every hand-off."),
            ("Mirror your layout", "Warehouses, zones and bins in Odoo match the labels on your racks."),
            ("Choose the steps", "One-step or multi-step receipts and deliveries, only where they add control."),
            ("Test with real orders", "Your team runs real receipts and dispatches before go-live.")]
    def radios(name, opts, on):
        return "".join('<label class="iv-radio"><input type="radio" name="%s" value="%d"%s><span></span>%s</label>' % (name, i + 1, " checked" if i + 1 == on else "", o)
                       for i, o in enumerate(opts))
    out += sec('<div class="iv-cfg"><div>%s%s</div><div class="ox iv-ox iv-wh-form" data-route>%s'
               '<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Warehouses</a><span>Chennai Warehouse</span></span></div></div>'
               '<div class="iv-wf"><div class="iv-wf-sheet"><h3>Chennai Warehouse <small>CHN</small></h3>'
               '<div class="ox-ftabs"><span>General Information</span><span class="is-on">Warehouse Configuration</span><span>Technical Information</span></div>'
               '<div class="iv-wf-grid"><fieldset><legend>Incoming Shipments</legend>%s</fieldset><fieldset><legend>Outgoing Shipments</legend>%s</fieldset></div>'
               '<p class="iv-route-label">Route for one pallet through Chennai Warehouse</p><ol class="iv-route" data-route-flow aria-live="polite"></ol></div></div></div></div>'
               % (head("CONFIGURED FOR YOUR FLOOR", "How Does Unisas Configure Odoo Inventory Around Your Existing Workflows?",
                       "We don't change how your warehouse works to suit the software. We set Odoo's own warehouse options to match it. Try the settings on the right."),
                  steps(impl), odoo_nav(inv_icon, "Inventory", MENUS_S),
                  radios("iv-in", ["Receive and Store (1 step)", "Receive then Store (2 steps)", "Receive, Quality Control, then Store (3 steps)"], 2),
                  radios("iv-out", ["Deliver (1 step)", "Pick then Deliver (2 steps)", "Pick, Pack, then Deliver (3 steps)"], 1)), "iv-sec--cfg")

    # 5 ---- automate replenishment: Replenishment screen
    rules = [("Reordering rules", "Min and max per product and warehouse, so orders go out on time."),
             ("Make to order", "A confirmed sale can raise its own PO or manufacturing order."),
             ("Resupply between warehouses", "Branches top up from your main warehouse automatically."),
             ("Putaway rules", "Received goods are sent straight to the right shelf.")]
    out += sec('<div class="iv-rep">%s<div><div class="ox iv-ox" data-rp>%s<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb">Replenishment</span></div>'
               '<span class="ox-search">%s<span class="ox-facet">%sTrigger: Manual</span><span class="ox-facet">%sTo Reorder</span></span><span></span></div>'
               '<div class="ox-scroll"><table class="ox-table iv-rp-table"><thead><tr><th>Product</th><th>Location</th><th class="ox-num">On Hand</th><th class="ox-num">Forecast</th>'
               '<th>Route</th><th class="ox-num">Min</th><th class="ox-num">Max</th><th class="ox-num">To Order</th><th></th></tr></thead><tbody data-rp-body></tbody></table></div>'
               '<div class="iv-toast" data-rp-toast role="status" aria-live="polite"></div></div>'
               '<p class="ox-hint"><span class="ox-hint-dot"></span>Click <b>Order Once</b> to raise the order, or <b>Automate</b> to let Odoo do it from now on.</p></div></div>'
               % ('<div class="iv-rep-copy">' + head("REPLENISHMENT", "How Can Odoo Automate Replenishment and Stock Movement?",
                                                     "Odoo compares forecasted stock against your rules every day and tells you, or simply orders, what is about to run out.")
                  + '<ul class="iv-rules">%s</ul></div>' % "".join('<li>%s<div><b>%s</b><span>%s</span></div></li>' % (TICK, t, x) for t, x in rules),
                  odoo_nav(inv_icon, "Inventory", MENUS), SEARCH, FUNNEL, FUNNEL), "iv-sec--rep")

    # 6 ---- barcode, lots & serials: Barcode app + traceability
    trace = [("in", "CHN/IN/00009", "Received from Sri Lakshmi Metals", "Sep 24 &middot; 3 units"),
             ("mrp", "CHN/MO/00213", "Built into Height-adjustable desk", "Sep 29 &middot; 1 unit"),
             ("out", "CHN/OUT/00031", "Delivered to Bluebay Retail Pvt Ltd", "Oct 01 &middot; 1 unit"),
             ("ret", "Warranty", "Covered until Oct 2028", "Linked to the customer invoice")]
    cfgs = [("GS1 or your own barcodes", "Products, locations, lots and packages all scannable."),
            ("Lots with expiry dates", "FEFO picking so the oldest batch leaves first."),
            ("Serial numbers", "One record per unit, from vendor to customer to warranty."),
            ("Labels that print", "Product, lot and location labels for your Zebra or office printer.")]
    out += sec(head("BARCODE &amp; TRACEABILITY", "How Can Unisas Configure Barcode, Lot and Serial Number Tracking?",
                    "We decide with you what gets a barcode, which products need lots or serial numbers, and what labels you print. Then any unit can be traced from vendor to customer.", "is-center")
               + '<div class="pl-2"><ul class="pl-grid" style="--cols:2">%s</ul><div class="pl-card"><p class="pl-k">One serial number, end to end &middot; SN-MTR-000481</p><ol class="pl-steps">%s</ol></div></div>'
                 % ("".join('<li><span class="pl-n">%02d</span><b>%s</b><p>%s</p></li>' % (i + 1, t, x) for i, (t, x) in enumerate(cfgs)),
                    "".join('<li><span class="pl-n">%d</span><b>%s</b><em>%s</em><p>%s</p></li>' % (i + 1, w, d, r) for i, (k, r, w, d) in enumerate(trace))), "iv-sec--bc")

    # 7 ---- connected with sales, purchase, manufacturing: Forecasted report
    lines = [("purchase", "P00034", "Sri Lakshmi Metals", "Oct 06", 60, "Incoming"), ("sales", "S00482", "Bluebay Retail", "Oct 03", -24, "Reserved"),
             ("mrp", "CHN/MO/00215", "Component for Executive chair kit", "Oct 08", -10, "Waiting"), ("sales", "S00497", "Kaveri Foods", "Oct 10", -18, "Waiting"),
             ("purchase", "P00036", "Sri Lakshmi Metals (draft)", "Oct 14", 40, "RFQ"), ("sales", "S00503", "Indus Exports", "Oct 15", -30, "Waiting")]
    bal, pts = 40, [40]
    for l in lines:
        bal += l[4]
        pts.append(bal)
    lrows = "".join('<tr data-app="%s"><td><span class="iv-dot" style="--c:%s"></span><b>%s</b><small>%s</small></td><td>%s</td><td class="ox-num"><b class="%s">%+d</b></td><td><span class="iv-pill">%s</span></td></tr>'
                    % (a, {"purchase": "#E06F5F", "sales": "#EE8A3C", "mrp": "#8E4F83"}[a], r, w, d, "iv-in" if q > 0 else "iv-out", q, s) for a, r, w, d, q, s in lines)
    # stepped forecast line
    W, H, mx = 520, 150, max(pts) + 10
    xs = [round(i * W / (len(pts) - 1)) for i in range(len(pts))]
    ys = [round(H - p / mx * H) for p in pts]
    path = "M0 %d" % ys[0] + "".join(" H%d V%d" % (xs[i], ys[i]) for i in range(1, len(pts))) + " H%d" % W
    minline = round(H - 30 / mx * H)
    chart = ('<svg class="iv-fc-chart" viewBox="0 0 %d %d" preserveAspectRatio="none" aria-hidden="true"><path d="%s V%d H0 Z" class="iv-fc-area"/><path d="%s" class="iv-fc-line"/>'
             '<line x1="0" x2="%d" y1="%d" y2="%d" class="iv-fc-min"/></svg>' % (W, H, path, H, path, W, minline, minline))
    tabs = "".join('<button type="button" class="iv-fc-tab%s" data-fc="%s" aria-pressed="%s">%s</button>' % (" is-on" if k == "all" else "", k, "true" if k == "all" else "false", n)
                   for k, n in [("all", "All"), ("sales", "Sales"), ("purchase", "Purchase"), ("mrp", "Manufacturing")])
    links = [("sales", "Sales", "Salespeople see free stock and the expected date on the order line, and confirming reserves it."),
             ("purchase", "Purchase", "Every PO becomes an expected receipt, and you pay only for what was received."),
             ("mrp", "Manufacturing", "Components are reserved when an MO is confirmed and finished goods arrive in stock.")]
    out += sec(head("CONNECTED APPS", "How Does Unisas Connect Odoo Inventory With Sales, Purchase and Manufacturing?",
                    "This is Odoo's Forecasted Report for one product. Every confirmed order from every app is already in it, so the future stock line is always current.", "is-center")
               + '<div class="iv-fc"><ul class="iv-fc-links">%s</ul><div class="ox iv-ox" data-fcr><div class="iv-fc-top"><div><small>Forecasted Report</small><h3>[FURN-0101] Ergo task chair</h3></div>'
                 '<dl><div><dt>On Hand</dt><dd>40</dd></div><div><dt>Forecasted</dt><dd>%d</dd></div><div><dt>Min</dt><dd>30</dd></div></dl></div>'
                 '<div class="iv-fc-graph">%s<span class="iv-fc-minl">Reorder point 30</span></div><div class="iv-fc-tabs" role="group" aria-label="Filter by app">%s</div>'
                 '<div class="ox-scroll"><table class="ox-table iv-fc-table"><thead><tr><th>Document</th><th>Date</th><th class="ox-num">Quantity</th><th>Status</th></tr></thead><tbody>%s</tbody></table></div></div></div>'
                 % ("".join('<li data-fc-link="%s"><b>%s</b><span>%s</span></li>' % l for l in links), pts[-1], chart, tabs, lrows), "iv-sec--fc")

    # 8 ---- integrations
    systems = [("Marketplaces &amp; store", "Shopify, Amazon, Flipkart", "Orders in, stock levels out", "in-out"),
               ("Couriers", "Shiprocket, Delhivery, Blue Dart", "Rates, labels and AWB tracking", "out"),
               ("Accounting history", "Tally, Busy, Zoho Books", "Masters and opening balances", "in"),
               ("GST e-Way bill", "NIC portal", "e-Way bill on dispatch", "out"),
               ("Devices", "Scanners, Zebra printers, scales", "Scans in, labels out", "in-out"),
               ("3PL &amp; custom apps", "REST / XML-RPC API", "Receipts and dispatch confirmations", "in-out")]
    arrows = {"in": "&larr;", "out": "&rarr;", "in-out": "&harr;"}
    nodes = "".join('<li><span class="iv-sys-dir">%s</span><b>%s</b><small>%s</small><span>%s</span></li>' % (arrows[d], t, s, x) for t, s, x, d in systems)
    log = [("10:42:08", "Amazon", "Order 402-8812 imported as S00511, 2 units reserved in BLR/Stock"),
           ("10:42:11", "Shopify", "Stock for FURN-0101 updated to 18 (Bengaluru)"),
           ("10:55:30", "Shiprocket", "AWB 1442 9876 5510 created for BLR/OUT/00119"),
           ("11:02:47", "e-Way bill", "EWB 3410 2287 6612 generated for CHN/OUT/00032"),
           ("11:15:02", "Zebra ZD421", "12 lot labels printed for CHN/IN/00010")]
    out += sec('%s<div class="iv-int"><ul class="iv-sys">%s</ul><div class="iv-log ox-solo"><p class="iv-log-h"><b>Integration log</b><span class="iv-live">Live</span></p>'
               '<ol>%s</ol><p class="iv-log-f">Failed syncs retry automatically and alert your team in Odoo.</p></div></div>'
               % (head("INTEGRATIONS", "How Can Unisas Integrate Odoo Inventory With Your Existing Systems?",
                       "Your stock rarely lives in one system. We connect Odoo to the channels, carriers and devices around it, so one stock figure feeds them all."),
                  nodes, "".join('<li><span class="mono">%s</span><b>%s</b><p>%s</p></li>' % l for l in log)), "iv-sec--int")

    # 9 ---- data migration: Odoo import screen + reconciliation
    mig = [("Extract", "Item masters, godowns, batches and closing stock from Tally, Excel or your old ERP."),
           ("Clean", "Duplicates merged, units standardised, dead SKUs archived with your sign-off."),
           ("Test import", "A trial load into a copy of your database, with every warning fixed."),
           ("Reconcile", "Quantity and value matched warehouse by warehouse before cutover.")]
    maps = [("Item Code", "Internal Reference"), ("Item Name", "Name"), ("UOM", "Unit of Measure"), ("Godown", "Location"),
            ("Batch No", "Lot/Serial Number"), ("Closing Qty", "Counted Quantity"), ("Rate", "Cost")]
    mrows2 = "".join('<tr><th>%s</th><td class="is-c">&rarr;</td><td>%s</td></tr>' % (a, b) for a, b in maps)
    rec = [("Chennai", 1842, 4823600), ("Bengaluru", 412, 1094500), ("Coimbatore", 233, 386200)]
    rrows = "".join('<tr><th>%s</th><td class="is-c">%s</td><td class="is-c">%s</td></tr>'
                    % (w, "{:,}".format(q), inr(v)) for w, q, v in rec)
    out += sec(head("DATA MIGRATION", "How Does Unisas Handle Inventory Data Migration and Validation?",
                    "Bad opening stock spoils a good implementation. We test every import and reconcile every warehouse before you go live.", "is-center")
               + '<div class="iv-mig">%s<div class="pl-card"><p class="pl-k">Column mapping &middot; tally_closing_stock_30Sep.xlsx</p><div class="pl-scroll"><table class="pl-table"><thead><tr><th>Your file</th><th></th><th>Becomes</th></tr></thead><tbody>%s</tbody></table></div></div>'
                 '<div class="pl-card"><p class="pl-k">Opening stock reconciliation</p><p class="pl-muted" style="margin:-6px 0 10px;font-size:0.86rem">Tally closing 30 Sep vs new opening 01 Oct</p><div class="pl-scroll"><table class="pl-table"><thead><tr><th>Warehouse</th><th class="is-c">Units</th><th class="is-c">Value</th></tr></thead><tbody>%s</tbody>'
                 '<tfoot><tr><th>Total</th><td class="is-c"><b>2,487</b></td><td class="is-c"><b>%s</b></td></tr></tfoot></table></div><p style="margin:12px 0 0"><span class="pl-chip is-ok">&#10003; All warehouses matched &middot; signed off</span></p></div></div>'
                 % (steps(mig), mrows2, rrows, inr(sum(v for _w, _q, v in rec))),
               "iv-sec--mig")

    # 10 ---- visibility & valuation: costing method switch
    kpis = [("Stock value", inr(6304300), "All warehouses, live"), ("Days of cover", "38", "Ergo task chair, at current sales"),
            ("Ageing &gt; 90 days", inr(412800), "17 products to clear"), ("Count accuracy", "98.6%", "Last 30 cycle counts")]
    out += sec(head("VISIBILITY &amp; VALUATION", "How Can Odoo Improve Inventory Visibility and Valuation?",
                    "Every movement carries its cost, so stock value is live, not a month-end estimate. Switch the costing method to see how Odoo values the same movements.", "is-center")
               + '<ul class="iv-kpis">%s</ul>' % "".join('<li><small>%s</small><b>%s</b><span>%s</span></li>' % k for k in kpis)
               + '<div class="ox iv-ox" data-val><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Valuation</a><span>[FURN-0101] Ergo task chair</span></span></div>'
                 '<span></span><div class="iv-cost" role="group" aria-label="Costing method"><span>Costing Method</span><button type="button" class="is-on" data-cost="fifo" aria-pressed="true">FIFO</button>'
                 '<button type="button" data-cost="avco" aria-pressed="false">Average Cost (AVCO)</button></div></div>'
                 '<div class="ox-scroll"><table class="ox-table iv-val-table"><thead><tr><th>Date</th><th>Reference</th><th class="ox-num">Quantity</th><th class="ox-num">Unit Value</th>'
                 '<th class="ox-num">Total Value</th><th class="ox-num">Remaining Qty</th></tr></thead><tbody data-val-body></tbody></table></div>'
                 '<div class="iv-val-sum" data-val-sum></div></div>', "iv-sec--val")

    # 11 ---- what's included: an Odoo receipt from Unisas
    scope = [("Discovery &amp; design", [("Warehouse walk-through &amp; process map", "Receipt, storage, picking and dispatch flows agreed"),
                                         ("Warehouse, location &amp; route design", "Bins, zones and 1/2/3-step operations")]),
             ("Configuration", [("Products, variants &amp; units", "Categories, packaging and units of measure"),
                                ("Reordering &amp; putaway rules", "Min/max, MTO and resupply between warehouses"),
                                ("Lots, serials &amp; expiry", "Tracking rules and FEFO removal strategy"),
                                ("Valuation &amp; accounting link", "FIFO or AVCO with automated stock entries")]),
             ("Data, devices &amp; people", [("Opening stock migration", "Tested import and warehouse-wise reconciliation"),
                                              ("Barcode &amp; label printing", "Scanners, mobile app and label templates"),
                                              ("Role-based training", "Storekeepers, buyers and accounts on their own data"),
                                              ("Go-live &amp; first cycle count", "Hypercare support through the first weeks")])]
    body = ""
    for title, items in scope:
        body += '<tr class="is-section"><td colspan="4">%s</td></tr>' % title
        body += "".join('<tr><td><b>%s</b><small>%s</small></td><td class="ox-num">1.00</td><td class="ox-num">1.00</td><td><span class="iv-picked">%s</span></td></tr>' % (n, d, TICK)
                        for n, d in items)
    out += sec('<div class="iv-scope">%s<div class="ox iv-ox"><div class="ox-cp"><div class="ox-cp-l"><a href="#get-demo" class="ox-new iv-ox-link" data-svc-cta="implementation">Validate</a>'
               '<span class="ox-sbtn">Print</span><span class="ox-crumb ox-crumb--stack"><a>Receipts</a><span>UNISAS/IMPL/00001</span></span></div>'
               '<span></span><span class="ox-sbar is-mini iv-scope-sb"><span class="ox-sb">Draft</span><span class="ox-sb is-cur">Ready</span><span class="ox-sb">Done</span></span></div>'
               '<div class="iv-scope-sheet"><h3>UNISAS/IMPL/00001</h3><dl class="ox-fields"><div><dt>Receive From</dt><dd>Unisas</dd></div><div><dt>Scheduled Date</dt><dd>After discovery</dd></div>'
               '<div><dt>Destination</dt><dd>Your Company / Stock</dd></div><div><dt>Source Document</dt><dd>Fixed-scope proposal</dd></div></dl>'
               '<div class="ox-ftabs"><span class="is-on">Operations</span><span>Additional Info</span></div>'
               '<table class="iv-scope-t"><thead><tr><th>Product</th><th class="ox-num">Demand</th><th class="ox-num">Quantity</th><th>Picked</th></tr></thead><tbody>%s</tbody></table></div></div></div>'
               % (head("WHAT'S INCLUDED", "What Does an Odoo Inventory Implementation With Unisas Include?",
                       "Our standard scope, written as the Odoo receipt you'll get from us. Press Validate to request it for your warehouses.", "is-center"), body), "iv-sec--scope")

    # 12 ---- businesses: product labels
    biz = [("Distribution &amp; wholesale", "Several warehouses, bulk storage and fast pick-pack-ship.", "CHN / Bulk B-04", "PALLET &middot; 40 units", "8 901234 567012"),
           ("Manufacturing", "Components reserved for production and finished goods put away.", "COMP-2210", "SN-MTR-000481", "8 901234 221007"),
           ("Retail &amp; eCommerce", "One stock figure for stores, website and marketplaces.", "Cotton kurta &middot; M &middot; Blue", "VARIANT &middot; 3 stores", "8 901234 880145"),
           ("Pharma &amp; food", "Lots with expiry dates and first-expiry-first-out picking.", "LOT-2026-0912", "EXP 03/2027 &middot; FEFO", "8 901234 450092"),
           ("Electronics &amp; equipment", "Serial numbers tied to warranty and service history.", "Laptop 14&Prime; i5", "SN 5CG2481KQ7", "8 901234 330218"),
           ("Spare parts &amp; trading", "Thousands of SKUs, bin locations and reorder points.", "Bearing 6204-2RS", "BIN R12-S3 &middot; MIN 200", "8 901234 620421")]
    cards = "".join('<li><div class="iv-label" aria-hidden="true"><small>%s</small><b>%s</b><i class="iv-bars"></i><span class="mono">%s</span></div><h3>%s</h3><p>%s</p></li>'
                    % (a, b, c, t, x) for t, x, a, b, c in biz)
    out += sec(head("WHO IT'S FOR", "Which Businesses Can Use Odoo for Inventory and Warehouse Management?",
                    "Any business that holds stock. What changes from one industry to the next is how stock is tracked, so here is the label each one would print.", "is-center")
               + '<ul class="iv-biz">%s</ul>' % cards, "iv-sec--biz")

    # 13 ---- plan
    phases = [("Discovery &amp; warehouse walk-through", 0, 2, "#5DC1AA"), ("Locations, routes &amp; rules", 2, 3, "#1F8A78"),
              ("Data migration &amp; barcode setup", 4, 3, "#F3B94C"), ("Testing &amp; training", 6, 2, "#8E4F83"), ("Go-live &amp; first cycle count", 8, 2, "#E06F5F")]
    weeks = "".join('<span>W%d</span>' % (i + 1) for i in range(10))
    prow = "".join('<div class="iv-pl-row"><span>%s</span><div><i style="--s:%d;--l:%d;--c:%s"></i></div></div>' % (n, s, l, c) for n, s, l, c in phases)
    first = [("A 30-minute call", "How you receive, store and ship today, and where it hurts."),
             ("A warehouse visit", "On site or by video, to see your racks, labels and paperwork."),
             ("A fixed-scope plan", "Phases, timeline and price, agreed before any work starts.")]
    out += sec('<div class="iv-plan"><div>%s<ol class="iv-first">%s</ol><div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Plan my Odoo Inventory rollout %s</a></div></div>'
               '<div class="iv-pl ox-solo"><p class="iv-pl-h"><b>Typical rollout</b><small>8 to 10 weeks, single company, up to 3 warehouses</small></p>'
               '<div class="iv-pl-weeks"><span></span><div>%s</div></div>%s</div></div>'
               % (head("NEXT STEPS", "How Can We Plan Your Odoo Inventory Implementation?",
                       "Every plan starts with your warehouse, not a template. Here is how a typical rollout runs."),
                  "".join('<li><b>%s</b><span>%s</span></li>' % f for f in first), g["ARROW"], weeks, prow), "iv-sec--plan")

    return out + JS.replace("__PRODUCTS__", json.dumps(PRODUCTS)).replace("__WH__", json.dumps(WH)).replace("__REPLEN__", json.dumps(REPLEN))


JS = r'''<script>
(function(){
  function inr(n){var s=Math.round(Math.abs(n)).toLocaleString('en-IN');return (n<0?'−':'')+'₹ '+s;}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function press(group,el){group.forEach(function(b){var on=b===el;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});}

  /* --- moves history filter --- */
  var mv=document.querySelector('.iv-moves');
  if(mv){var btns=[].slice.call(mv.querySelectorAll('[data-mv]')),facet=mv.querySelector('[data-mv-facet]');
    btns.forEach(function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-mv');press(btns,b);
      mv.querySelectorAll('tbody tr').forEach(function(r){r.hidden=k!=='all'&&r.getAttribute('data-app')!==k;});
      facet.hidden=k==='all';facet.textContent=b.textContent.replace(/\d+$/,'');});});}

  /* --- stock explorer --- */
  var st=document.querySelector('[data-st]');
  if(st){var P=__PRODUCTS__,WH=__WH__,body=st.querySelector('[data-st-body]'),q=st.querySelector('[data-st-q]'),fac=st.querySelector('[data-st-facet]');
    var whb=[].slice.call(st.querySelectorAll('[data-wh]')),cur='ALL',open={};
    function agg(p){var keys=cur==='ALL'?Object.keys(WH):[cur],a=[0,0,0,0],locs=[];
      keys.forEach(function(k){var d=p[6][k];for(var i=0;i<4;i++)a[i]+=d[i];d[4].forEach(function(l){locs.push([k+'/Stock'+(l[0]==='Stock'?'':'/'+l[0]),l[1]]);});});return {a:a,locs:locs};}
    function render(){var t=q.value.trim().toLowerCase(),tv=0,html='';
      P.forEach(function(p){if(t&&(p[0]+' '+p[1]).toLowerCase().indexOf(t)<0)return;
        var g=agg(p),a=g.a,fc=a[0]+a[2]-a[3],low=fc<p[4];tv+=a[0]*p[3];
        html+='<tr data-p="'+p[0]+'" tabindex="0" aria-expanded="'+(!!open[p[0]])+'"><td><span class="iv-caret">'+(open[p[0]]?'▾':'▸')+'</span><b>['+p[0]+'] '+esc(p[1])+'</b>'+(p[5]?'<span class="iv-trk">'+p[5]+'</span>':'')+'</td>'+
          '<td class="ox-num"><b>'+a[0]+'</b></td><td class="ox-num">'+(a[0]-a[1])+'</td><td class="ox-num iv-in">'+(a[2]?'+'+a[2]:'0')+'</td><td class="ox-num iv-out">'+(a[3]?'−'+a[3]:'0')+'</td>'+
          '<td class="ox-num"><b'+(low?' class="iv-low" title="Below reorder point '+p[4]+'"':'')+'>'+fc+'</b></td><td class="ox-muted">'+p[2]+'</td><td class="ox-num">'+inr(a[0]*p[3])+'</td></tr>';
        if(open[p[0]])html+='<tr class="iv-sub-row"><td colspan="8">'+(g.locs.length?'<ul>'+g.locs.map(function(l){return '<li><span>'+l[0]+'</span><b>'+l[1]+' '+p[2]+'</b></li>';}).join('')+'</ul>':'<p>No stock in this warehouse.</p>')+'</td></tr>';});
      body.innerHTML=html?'<div class="ox-scroll"><table class="ox-table iv-st-table"><thead><tr><th>Product</th><th class="ox-num">On Hand</th><th class="ox-num">Free to Use</th><th class="ox-num">Incoming</th><th class="ox-num">Outgoing</th><th class="ox-num">Forecasted</th><th>Unit</th><th class="ox-num">Value</th></tr></thead><tbody>'+html+
        '</tbody><tfoot><tr><td colspan="7"><b>Total value</b></td><td class="ox-num"><b>'+inr(tv)+'</b></td></tr></tfoot></table></div>':'<p class="ox-empty">No product matches “'+esc(q.value)+'”.</p>';}
    whb.forEach(function(b){b.addEventListener('click',function(){cur=b.getAttribute('data-wh');press(whb,b);fac.textContent=cur==='ALL'?'All Warehouses':WH[cur]+' Warehouse';render();});});
    function toggle(r){var k=r.getAttribute('data-p');open[k]=!open[k];render();var n=body.querySelector('[data-p="'+k+'"]');if(n)n.focus();}
    body.addEventListener('click',function(e){var r=e.target.closest('[data-p]');if(r)toggle(r);});
    body.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){var r=e.target.closest('[data-p]');if(r){e.preventDefault();toggle(r);}}});
    q.addEventListener('input',render);open['FURN-0101']=true;render();}

  /* --- warehouse route --- */
  var rt=document.querySelector('[data-route]');
  if(rt){var flow=rt.querySelector('[data-route-flow]');
    function draw(){var i=+rt.querySelector('[name="iv-in"]:checked').value,o=+rt.querySelector('[name="iv-out"]:checked').value;
      var s=[['ext','Partners/Vendors','']];
      s.push(i===1?['op','CHN/Stock','Receipt']:['op','CHN/Input','Receipt']);
      if(i===3)s.push(['op','CHN/Quality Control','Quality check']);
      if(i>1)s.push(['op','CHN/Stock','Storage']);
      if(o===3){s.push(['op','CHN/Packing Zone','Pick']);s.push(['op','CHN/Output','Pack']);}
      if(o===2)s.push(['op','CHN/Output','Pick']);
      s.push(['ext','Partners/Customers','Delivery']);
      flow.innerHTML=s.map(function(x){return '<li class="is-'+x[0]+'">'+(x[2]?'<small>'+x[2]+'</small>':'')+'<b>'+x[1]+'</b></li>';}).join('');
      flow.setAttribute('aria-label',(s.length-1)+' moves per pallet');}
    rt.addEventListener('change',draw);draw();}

  /* --- replenishment --- */
  var rp=document.querySelector('[data-rp]');
  if(rp){var R=__REPLEN__,rb=rp.querySelector('[data-rp-body]'),toast=rp.querySelector('[data-rp-toast]'),po=35,mo=214,it=5,tt;
    R.forEach(function(r){r.auto=false;r.done=false;});
    function rrender(){var l=R.filter(function(r){return !r.done;});
      rb.innerHTML=l.length?l.map(function(r,i){var need=Math.max(0,r[7]-r[3]);return '<tr><td><b>'+esc(r[0])+'</b></td><td class="ox-muted">'+r[1]+'</td><td class="ox-num">'+r[2]+'</td><td class="ox-num"><b class="'+(r[3]<r[6]?'iv-low':'')+'">'+r[3]+'</b></td>'+
        '<td><span class="iv-route-pill is-'+(r[4]==='Buy'?'buy':r[4]==='Manufacture'?'mfg':'int')+'">'+r[4]+'</span></td><td class="ox-num">'+r[6]+'</td><td class="ox-num">'+r[7]+'</td><td class="ox-num"><b>'+need+'</b></td>'+
        '<td class="iv-rp-act">'+(r.auto?'<span class="iv-auto">'+'Automated</span>':'<button type="button" class="ox-pbtn" data-rp-do="once" data-i="'+R.indexOf(r)+'">Order Once</button><button type="button" class="ox-sbtn" data-rp-do="auto" data-i="'+R.indexOf(r)+'">Automate</button>')+'</td></tr>';}).join('')
        :'<tr><td colspan="9" class="ox-empty">Nothing to reorder. Odoo will check again tonight.</td></tr>';}
    function say(m){toast.innerHTML=m;toast.classList.add('is-on');clearTimeout(tt);tt=setTimeout(function(){toast.classList.remove('is-on');},3600);}
    rb.addEventListener('click',function(e){var b=e.target.closest('[data-rp-do]');if(!b)return;var r=R[+b.getAttribute('data-i')],need=Math.max(0,r[7]-r[3]),doc;
      doc=r[4]==='Buy'?'Purchase order <b>P000'+(po++)+'</b> sent to '+r[5]:r[4]==='Manufacture'?'Manufacturing order <b>CHN/MO/00'+(mo++)+'</b> created':'Transfer <b>CHN/INT/0000'+(it++)+'</b> to '+r[1].split('/')[0];
      if(b.getAttribute('data-rp-do')==='once'){r.done=true;say(doc+' for '+need+' units.');}
      else{r.auto=true;say('Rule automated: Odoo will reorder <b>'+esc(r[0])+'</b> on its own whenever forecast drops below '+r[6]+'.');}
      rrender();});
    rrender();}

  /* --- forecast filter --- */
  var fc=document.querySelector('[data-fcr]');
  if(fc){var tabs=[].slice.call(fc.querySelectorAll('[data-fc]')),links=[].slice.call(document.querySelectorAll('[data-fc-link]'));
    function pick(k){tabs.forEach(function(b){var on=b.getAttribute('data-fc')===k;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
      fc.querySelectorAll('tbody tr').forEach(function(r){r.classList.toggle('is-dim',k!=='all'&&r.getAttribute('data-app')!==k);});
      links.forEach(function(l){l.classList.toggle('is-on',l.getAttribute('data-fc-link')===k);});}
    tabs.forEach(function(b){b.addEventListener('click',function(){pick(b.getAttribute('data-fc'));});});
    links.forEach(function(l){l.addEventListener('mouseenter',function(){pick(l.getAttribute('data-fc-link'));});l.addEventListener('mouseleave',function(){pick('all');});});}

  /* --- valuation FIFO vs AVCO --- */
  var vl=document.querySelector('[data-val]');
  if(vl){var M=[['Sep 03','CHN/IN/00004',40,5900],['Sep 10','CHN/OUT/00022',-24],['Sep 18','CHN/IN/00007',60,6300],['Sep 26','CHN/OUT/00027',-30]],
      vb=vl.querySelector('[data-val-body]'),sum=vl.querySelector('[data-val-sum]'),cb=[].slice.call(vl.querySelectorAll('[data-cost]'));
    function calc(m){var layers=[],rows=[],cogs=0,qty=0,val=0;
      M.forEach(function(x){if(x[2]>0){layers.push({q:x[2],c:x[3],ref:x[1]});qty+=x[2];val+=x[2]*x[3];rows.push([x[0],x[1],x[2],x[3],x[2]*x[3]]);}
        else{var out=-x[2],cost=0;if(m==='fifo'){while(out>0){var l=layers[0],t=Math.min(out,l.q);cost+=t*l.c;l.q-=t;out-=t;if(!l.q)layers.shift();}}
          else{cost=out*val/qty;}
          qty+=x[2];val-=cost;cogs+=cost;rows.push([x[0],x[1],x[2],cost/-x[2],-cost]);}
        rows[rows.length-1].push(m==='fifo'?layers.map(function(l){return l.q;}).reduce(function(a,b){return a+b;},0):qty);});
      return {rows:rows,cogs:cogs,qty:qty,val:val};}
    function vdraw(m){var r=calc(m);
      vb.innerHTML=r.rows.map(function(x){return '<tr><td>'+x[0]+'</td><td><b>'+x[1]+'</b></td><td class="ox-num '+(x[2]>0?'iv-in':'iv-out')+'">'+(x[2]>0?'+':'−')+Math.abs(x[2])+'</td><td class="ox-num">'+inr(x[3])+'</td><td class="ox-num">'+inr(x[4])+'</td><td class="ox-num">'+x[5]+'</td></tr>';}).join('');
      sum.innerHTML='<span><small>Cost of goods sold</small><b>'+inr(r.cogs)+'</b></span><span><small>Remaining value ('+r.qty+' units)</small><b>'+inr(r.val)+'</b></span><span><small>Unit value now</small><b>'+inr(r.val/r.qty)+'</b></span><span class="iv-val-je"><small>Posted to Accounting</small><b>Stock Valuation / Cost of Goods Sold</b></span>';}
    cb.forEach(function(b){b.addEventListener('click',function(){press(cb,b);vdraw(b.getAttribute('data-cost'));});});vdraw('fifo');}
})();
</script>
'''

CTA = ("Let's Get Your Stock Under Control in Odoo",
       "Tell us your warehouses, SKUs and channels. We&rsquo;ll show the same flow in Odoo Inventory and recommend a setup.")
