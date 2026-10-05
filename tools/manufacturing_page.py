"""
Odoo Manufacturing page (odoo-manufacturing.html). Every screen is modelled on the real Odoo 20
Manufacturing app (demo.odoo.com/odoo/work-centers and the menus around it): the Work Centers
overview and form, Manufacturing Orders (Draft / Confirmed / In Progress / To Close / Done) with
their components and work orders, the BoM Overview, Planning by Work Center, the Replenishment
report, Quality checks, the Traceability report, Cost Analysis and OEE.
Sample company: a ceiling-fan maker in Chennai, so the same Aero 48 fan, its motor sub-assembly
and six work centres appear in every section. Shared Odoo look: odoo-ui.css. Page styles:
manufacturing.css.

hero(g) and build(g) get the build script's globals.
"""
import json

from crm_explorer import ic, SEARCH

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def inr(n, dec=True):
    whole = int(round(abs(n)))
    digits = "%d" % whole
    rest, last3 = digits[:-3], digits[-3:]
    groups = []
    while len(rest) > 2:
        groups.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.insert(0, rest)
    out = ",".join(groups + [last3]) if groups else last3
    return ("-" if n < 0 else "") + "&#8377; " + out + (".00" if dec else "")


def head(eyebrow, title, sub="", cls=""):
    return ('<div class="mf-head%s"><p class="mf-eyebrow mono">%s</p><h2 class="mf-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="mf-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="mf-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


def data(sid, obj):
    """JSON for the page script, safe inside a <script> element."""
    return '<script type="application/json" id="%s">%s</script>' % (sid, json.dumps(obj).replace("</", "<\\/"))


def nav(app_icon, menus=("Overview", "Operations", "Planning", "Products", "Reporting", "Configuration")):
    return ('<div class="ox-nav"><span class="ox-app">%s<b>Manufacturing</b></span>%s<span class="ox-nav-r"><span class="ox-company">Your Company</span>'
            '<span class="ox-av" style="--c:#0E7C86">D</span></span></div>' % (app_icon, "".join('<span class="ox-menu">%s</span>' % m for m in menus)))


# ------------------------------------------------------------------ shared sample data
# work centres: key, name, code, cost per hour, OEE %, OEE target, late WOs, load history (hours, last 4 weeks), alternatives
WC = [
    {"k": "PRS", "n": "Press Shop", "code": "PRS-01", "cost": 900, "oee": 78.4, "late": 0, "hist": [4.5, 6, 5.5, 7], "alt": "", "eff": 100, "cap": 2, "setup": 15, "clean": 10, "tag": "Fabrication"},
    {"k": "WND", "n": "Motor Winding", "code": "WND-01", "cost": 750, "oee": 71.2, "late": 1, "hist": [6, 8.5, 5, 3], "alt": "", "eff": 95, "cap": 4, "setup": 10, "clean": 5, "tag": "Motor"},
    {"k": "AS1", "n": "Assembly Line 1", "code": "ASM-01", "cost": 600, "oee": 84.6, "late": 0, "hist": [17, 21, 18.5, 22], "alt": "Assembly Line 2", "eff": 100, "cap": 6, "setup": 20, "clean": 10, "tag": "Assembly"},
    {"k": "AS2", "n": "Assembly Line 2", "code": "ASM-02", "cost": 600, "oee": 80.1, "late": 0, "hist": [3, 4.5, 2, 3.5], "alt": "Assembly Line 1", "eff": 90, "cap": 4, "setup": 20, "clean": 10, "tag": "Assembly"},
    {"k": "PNT", "n": "Paint Shop", "code": "PNT-01", "cost": 820, "oee": 69.8, "late": 2, "hist": [9, 12, 11, 13.5], "alt": "", "eff": 100, "cap": 1, "setup": 30, "clean": 25, "tag": "Finishing"},
    {"k": "TST", "n": "Testing &amp; QC", "code": "TST-01", "cost": 540, "oee": 91.3, "late": 0, "hist": [6, 7.5, 6.5, 8], "alt": "", "eff": 100, "cap": 3, "setup": 5, "clean": 5, "tag": "Quality"},
]
# routings: operation, work centre, minutes per unit
ROUTES = {
    "fan": [["Blade pressing", "PRS", 0.6], ["Final assembly", "AS1", 1.5], ["Powder coating", "PNT", 0.8], ["Run test &amp; pack", "TST", 0.5]],
    "motor": [["Stator winding", "WND", 1.2], ["Rotor fitting", "AS2", 0.7]],
    "ped": [["Final assembly", "AS2", 1.8], ["Run test &amp; pack", "TST", 0.5]],
}
PRODUCTS = {
    "aero": {"n": "Aero 48 Ceiling Fan 1200mm", "code": "FAN-A48", "r": "fan", "comp": [["Motor Assembly 48W", 1, "Units"], ["Blade Set 1200mm", 1, "Units"], ["Canopy &amp; Downrod Kit", 1, "Units"], ["Capacitor 2.5&micro;F", 1, "Units"], ["Packing Carton, 5-ply", 1, "Units"]]},
    "breeze": {"n": "Breeze 36 Ceiling Fan 900mm", "code": "FAN-B36", "r": "fan", "comp": [["Motor Assembly 36W", 1, "Units"], ["Blade Set 900mm", 1, "Units"], ["Canopy &amp; Downrod Kit", 1, "Units"], ["Capacitor 2.5&micro;F", 1, "Units"], ["Packing Carton, 5-ply", 1, "Units"]]},
    "motor": {"n": "Motor Assembly 48W", "code": "MTR-48", "r": "motor", "comp": [["Stator Lamination Stack", 1, "Units"], ["Copper Winding Wire 0.35mm", 0.42, "kg"], ["Rotor Housing", 1, "Units"], ["Ball Bearing 6202", 2, "Units"]]},
    "ped": {"n": "Turbo Pedestal Fan 400mm", "code": "FAN-T40", "r": "ped", "comp": [["Pedestal Motor 55W", 1, "Units"], ["Blade Set 400mm", 1, "Units"], ["Stand &amp; Base Kit", 1, "Units"], ["Packing Carton, 5-ply", 1, "Units"]]},
}
# manufacturing orders: st is draft / open / done; wo holds one state per routing step (wait, ready, progress, done)
MOS = [
    {"id": 1, "ref": "WH/MO/00042", "p": "aero", "qty": 250, "date": "Oct 19", "src": "S00231", "st": "open", "comp": "ok", "resp": "Meera Iyer", "wo": ["done", "progress", "wait", "wait"]},
    {"id": 2, "ref": "WH/MO/00043", "p": "motor", "qty": 250, "date": "Oct 16", "src": "WH/MO/00042", "st": "done", "comp": "ok", "resp": "Meera Iyer", "wo": ["done", "done"]},
    {"id": 3, "ref": "WH/MO/00044", "p": "breeze", "qty": 120, "date": "Oct 22", "src": "Reorder rule", "st": "open", "comp": "no", "resp": "Rahul Menon", "wo": ["wait", "wait", "wait", "wait"]},
    {"id": 4, "ref": "WH/MO/00045", "p": "ped", "qty": 80, "date": "Oct 21", "src": "S00236", "st": "open", "comp": "ok", "resp": "Rahul Menon", "wo": ["ready", "wait"]},
    {"id": 5, "ref": "WH/MO/00046", "p": "aero", "qty": 400, "date": "Oct 26", "src": "S00238", "st": "draft", "comp": "no", "resp": "Meera Iyer", "wo": ["wait", "wait", "wait", "wait"]},
]
# BoM overview for the Aero 48: code, name, qty per unit, uom, free to use, route, lead days, unit cost, sub-BoM key
BOM = {
    "comp": [["MTR-48", "Motor Assembly 48W", 1, "Units", 120, "Manufacture", 3, 0, "motor"],
             ["BLD-1200", "Blade Set 1200mm", 1, "Units", 520, "Buy", 7, 365, ""],
             ["CNP-KIT", "Canopy &amp; Downrod Kit", 1, "Units", 410, "Buy", 5, 142, ""],
             ["CAP-25", "Capacitor 2.5&micro;F", 1, "Units", 140, "Buy", 10, 38, ""],
             ["FST-PK", "Fastener Pack", 1, "Units", 2000, "Buy", 4, 12, ""],
             ["CTN-48", "Packing Carton, 5-ply", 1, "Units", 600, "Buy", 6, 46, ""]],
    "motor": [["STL-48", "Stator Lamination Stack", 1, "Units", 300, "Buy", 12, 310],
              ["CU-035", "Copper Winding Wire 0.35mm", 0.42, "kg", 160, "Buy", 8, 820],
              ["RTR-48", "Rotor Housing", 1, "Units", 260, "Buy", 9, 240],
              ["BRG-6202", "Ball Bearing 6202", 2, "Units", 900, "Buy", 5, 48]],
}
# planning by work centre: work centre, MO, operation, start day, length (days), state
PLAN = [["PRS", "WH/MO/00042", "Blade pressing", 0, 1, "done"], ["AS1", "WH/MO/00042", "Final assembly", 1, 2, "progress"], ["PNT", "WH/MO/00042", "Powder coating", 3, 1, "wait"],
        ["TST", "WH/MO/00042", "Run test &amp; pack", 4, 1, "wait"], ["AS2", "WH/MO/00045", "Final assembly", 2, 1, "ready"], ["TST", "WH/MO/00045", "Run test &amp; pack", 5, 1, "wait"],
        ["PRS", "WH/MO/00044", "Blade pressing", 3, 1, "wait"], ["AS1", "WH/MO/00044", "Final assembly", 4, 1, "wait"], ["PNT", "WH/MO/00044", "Powder coating", 5, 1, "wait"],
        ["WND", "WH/MO/00047", "Stator winding", 1, 3, "ready"], ["AS2", "WH/MO/00047", "Rotor fitting", 4, 2, "wait"], ["TST", "WH/MO/00044", "Run test &amp; pack", 7, 1, "wait"],
        ["PRS", "WH/MO/00046", "Blade pressing", 6, 2, "wait"], ["AS1", "WH/MO/00046", "Final assembly", 7, 3, "wait"]]


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">Manufacturing</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["Bills of materials &amp; routings", "Work orders on shop-floor tablets", "Actual cost on every order"])
    copy = ('<div class="mf-hero-copy">%s<p class="mf-eyebrow mono">ODOO MANUFACTURING IMPLEMENTATION</p>'
            '<h1 class="mf-h1">Manufacturing ERP Software for <span>End-to-End Production Management</span></h1>'
            '<p class="mf-lead">Unisas implements Odoo Manufacturing so sales orders, bills of materials, work orders, stock, quality checks and costs run '
            'in one connected system. Planners see real capacity, operators see the right instructions, and finance sees the actual cost of every order.</p>'
            '<ul class="mf-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Discuss Odoo Manufacturing %s</a>'
            '<a href="#explore" class="btn btn-ghost">Try the manufacturing demo</a></div></div>' % (crumb, points, g["ARROW"]))
    # one manufacturing order on the line, drawn as a blueprint sheet with a title block
    rows = [("PRS-01", "Press Shop", "Finished", "done", "250 / 250"), ("ASM-01", "Assembly Line 1", "In Progress", "run", "155 / 250"),
            ("PNT-01", "Paint Shop", "Ready", "ready", "0 / 250"), ("TST-01", "Testing &amp; QC", "Waiting", "wait", "0 / 250")]
    lis = "".join('<li class="is-%s"><span class="mf-hv-node">%s</span><b>%s</b><em>%s</em><small class="mono">%s</small></li>' % (k, code, n, st, q) for code, n, st, k, q in rows)
    tb = [("Components", "Available", "is-ok"), ("OEE today", "82.6%", ""), ("Cost so far", inr(318450, False), ""), ("Quality check", "12.2&deg; &#10003;", "is-ok")]
    return ('<section class="mf-hero">' + copy + '<div class="mf-hero-vis mf-hv" aria-label="A manufacturing order moving along four work centres, drawn as a production-line blueprint">'
            '<div class="mf-hv-sheet"><div class="mf-hv-hd"><span class="mf-hv-app">' + g["TILE_ICONS"][6] + '</span><span class="mf-hv-ttl"><small class="mono">WH/MO/00042 &middot; SHEET 1/1</small>'
            '<b>250 &times; Aero 48 Ceiling Fan</b></span><span class="mf-hv-ring" style="--p:62"><span><b>155</b><small>of 250</small></span></span></div>'
            '<ol class="mf-hv-line">' + lis + '<i class="mf-hv-item" style="--d:0s"></i><i class="mf-hv-item" style="--d:-2s"></i><i class="mf-hv-item" style="--d:-4s"></i></ol>'
            '<p class="mf-hv-dim mono">4 work centres &middot; 11.5 h cycle &middot; due 24 Oct</p>'
            '<div class="mf-hv-tb">' + "".join('<div><small class="mono">%s</small><b class="%s">%s</b></div>' % (a, c, b) for a, b, c in tb) + '</div></div></div></section>')

# ------------------------------------------------------------------ sections
def build(g):
    out = ""
    app_icon = g["TILE_ICONS"][6]

    # 1 ---- why manufacturing ERP is hard: a factory floor plan
    zones = [("sales", "Sales desk", "Delivery dates promised without seeing capacity",
              "Sales confirms 400 fans for the 26th. Nobody checked that the paint shop is already full that week, or that capacitors are short.",
              "Production capacity and component stock live in different places, so the promise is a guess.",
              "Sales order lines show the forecasted date from stock and open manufacturing orders, and Planning by Work Center shows the load before anyone commits."),
             ("plan", "Planning office", "Bills of materials kept in Excel, in several versions",
              "Engineering changed the capacitor last month. The shop floor is still building from the old sheet.",
              "Every product has variants, sub-assemblies and revisions, and they change while orders are running.",
              "One BoM per product and variant in Odoo, with sub-assemblies as their own BoMs. Changes go through engineering change orders when PLM is used."),
             ("store", "Stores", "Shortages found at the machine",
              "Assembly starts the order and stops two hours later: the canopy kits are in another warehouse.",
              "Component reservation only works if stock levels in the system are right, and they rarely are on day one.",
              "Manufacturing orders reserve components when confirmed and show Component Status. Reordering rules raise purchase or manufacturing orders before stock runs out."),
             ("floor", "Shop floor", "Progress lives on whiteboards",
              "The supervisor walks the line twice a day to find out what is done. Times are written on the job card at shift end.",
              "Operators need a screen that is faster than paper, or they will not use it.",
              "Shop Floor tablets at each work centre: operators start, pause and finish work orders, read the worksheet and record quantities, so times are captured as they happen."),
             ("qc", "Quality lab", "Checks on paper, recorded after the fact",
              "A batch of blades with the wrong pitch is found at final testing, after painting.",
              "Quality checks must sit in the right operation, with clear pass and fail rules, without slowing the line.",
              "Quality control points on each operation: measurements, pass/fail and photos, with alerts raised automatically when a check fails."),
             ("acct", "Accounts", "Product cost known only at year end",
              "The Aero 48 is priced on a cost sheet from 2023. Copper prices have moved twice since.",
              "Costing needs real consumption, real work-centre time and cost rates that someone maintains.",
              "Every manufacturing order records components consumed and work-centre time, so the Cost Analysis shows expected against actual cost per order.")]
    zb = "".join('<button type="button" class="mf-zone mf-zone--%s%s" data-zone="%d" aria-pressed="%s"><span class="mf-zone-n mono">%s</span><b>%s</b><span class="mf-zone-pin" aria-hidden="true">!</span></button>'
                 % (k, " is-on" if i == 0 else "", i, "true" if i == 0 else "false", "%02d" % (i + 1), n) for i, (k, n, *_r) in enumerate(zones))
    out += sec(head("WHY IT IS HARD", "What Makes Manufacturing ERP Difficult to Implement Across Production Operations?",
                    "A manufacturing ERP touches every department at once, and each one keeps its own version of the truth today. "
                    "Projects stall when BoMs, stock and shop-floor reporting are not fixed together. Pick an area of the factory to see where it usually breaks.", "is-center")
               + '<div class="mf-plan" data-zones><div class="mf-floor" role="group" aria-label="Factory areas">%s<span class="mf-floor-flow" aria-hidden="true"></span></div>'
                 '<div class="mf-zone-card ox-solo" aria-live="polite"><p class="mf-zc-k mono" data-z-area></p><h3 data-z-title></h3>'
                 '<p class="mf-zc-story" data-z-story></p><dl><div><dt>Why it is hard</dt><dd data-z-why></dd></div><div class="is-fix"><dt>How we handle it in Odoo</dt><dd data-z-fix></dd></div></dl></div></div>'
                 % zb + data("mf-zones", zones), "mf-sec--why")

    # 2 ---- connected workflow: the document chain from one sales order
    chain = [("Sales", "#EE8A3C", "S00231", "Sales order confirmed", "250 &times; Aero 48 Ceiling Fan for Shree Distributors, delivery Oct 30.", "Quotation signed online"),
             ("Manufacturing", "#0E7C86", "WH/MO/00042", "Manufacturing order created", "Replenish on Order (MTO) creates the order from BoM Aero 48, with 4 work orders.", "Manufacturing"),
             ("Manufacturing", "#0E7C86", "WH/MO/00043", "Sub-assembly order created", "The motor has its own BoM, so 250 Motor Assembly 48W are planned first.", "Manufacturing"),
             ("Inventory", "#1F8A78", "WH/PC/00118", "Components picked", "1,500 component units moved from stock to pre-production and reserved for the order.", "Transfers"),
             ("Shop floor", "#714B67", "4 work orders", "Work orders done", "Blade pressing, assembly, powder coating, test and pack. 31 h 40 min recorded on tablets.", "Work Orders"),
             ("Quality", "#B5567E", "QC/00391", "Final test passed", "248 passed, 2 failed for noise and were reworked on Assembly Line 2.", "Quality Checks"),
             ("Inventory", "#1F8A78", "WH/OUT/00231", "Delivered", "250 fans shipped with lot FAN-2610-0042; e-Way bill generated.", "Delivery"),
             ("Accounting", "#B7791F", "INV/2026/00431", "Invoiced and costed", "Invoice posted, and finished-goods value booked at the actual order cost.", "Invoices")]
    rail = "".join('<li style="--c:%s"><button type="button" data-ch="%d" aria-label="Step %d: %s"><span class="mf-ch-n mono">%d</span><small>%s</small></button></li>'
                   % (c, i, i + 1, t, i + 1, app) for i, (app, c, d, t, x, sb) in enumerate(chain))
    out += sec(head("CONNECTED WORKFLOW", "How Can Manufacturing ERP Software Connect Your Production Workflow?",
                    "One sales order sets off every document the factory needs, and each one links back to it. Step through an order and watch the smart buttons on the sales order fill up: "
                    "that is the whole trail, one click from the order.", "is-center")
               + '<div class="mf-chain" data-chain><ol class="mf-ch-rail">%s</ol><div class="mf-ch-body">'
                 '<div class="mf-ch-doc ox-solo" aria-live="polite"><p class="mf-ch-app mono" data-ch-app></p><h3 data-ch-title></h3><p class="mf-ch-ref mono" data-ch-ref></p><p data-ch-text></p>'
                 '<div class="mf-ch-btns"><button type="button" class="ox-sbtn" data-ch-prev>Back</button><button type="button" class="ox-pbtn" data-ch-next>Next step</button></div></div>'
                 '<div class="ox mf-ox mf-ch-so"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Sales Orders</a><span>S00231</span></span></div><span></span><span></span></div>'
                 '<div class="mf-ch-sheet"><div class="mf-smart" data-ch-smart></div><h4>S00231</h4><dl class="mf-ch-dl"><div><dt>Customer</dt><dd>Shree Distributors</dd></div><div><dt>Delivery</dt><dd>Oct 30</dd></div>'
                 '<div><dt>Product</dt><dd>[FAN-A48] Aero 48 Ceiling Fan</dd></div><div><dt>Quantity</dt><dd>250.00 Units</dd></div></dl><ol class="mf-ch-log" data-ch-log></ol></div></div></div></div>'
                 % rail + data("mf-chain", chain), "mf-sec--chain")

    # 3 ---- the explorer: MOs, BoM, work centres, planning
    menu = "".join('<button type="button" class="mf-menu%s" data-mx-menu="%s" aria-pressed="%s">%s</button>' % (" is-on" if k == "wc" else "", k, "true" if k == "wc" else "false", n)
                   for k, n in [("wc", "Work Centers"), ("mo", "Manufacturing Orders"), ("bom", "Bills of Materials"), ("plan", "Planning")])
    out += sec(head("BOMS, WORK ORDERS &amp; PLANNING", "How Can Odoo Manage Bills of Materials, Work Orders and Production Planning?",
                    "This is Odoo Manufacturing with a fan factory's data. Start on the <b>Work Centers</b> overview, open <b>WH/MO/00042</b> to finish its work orders, "
                    "change the quantity in the <b>BoM Overview</b>, then see the load in <b>Planning</b>.", "is-center")
               + '<div class="ox mf-ox mf-mx" data-mx><div class="ox-nav"><span class="ox-app">%s<b>Manufacturing</b></span><span class="mf-menus" role="group" aria-label="Manufacturing menu">%s</span>'
                 '<span class="ox-menu">Reporting</span><span class="ox-nav-r"><span class="ox-company">Your Company</span><span class="ox-av" style="--c:#0E7C86">D</span></span></div>'
                 '<div class="ox-cp"><div class="ox-cp-l"><button type="button" class="ox-new" data-mx-new>New</button><span class="ox-crumb ox-crumb--stack" data-mx-crumb></span></div>'
                 '<label class="ox-search">%s<input type="search" placeholder="Search..." aria-label="Search" data-mx-q></label><span></span></div>'
                 '<div class="ox-body mf-mx-body" data-mx-body></div></div>'
                 '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview with sample data. Open a work centre or an order, start and finish work orders, and watch the load change.</p>'
                 % (app_icon, menu, SEARCH)
               + data("mf-wc", WC) + data("mf-routes", ROUTES) + data("mf-products", PRODUCTS) + data("mf-mos", MOS) + data("mf-bom", BOM) + data("mf-plan", PLAN),
               "mf-sec--explore", "explore")

    # 4 ---- configure workflows: Odoo settings and the flow they produce
    toggles = [("wo", "Work Orders", "Process operations at specific work centers", True),
               ("qc", "Quality", "Add quality checks to your work orders", True),
               ("lot", "Lots &amp; Serial Numbers", "Track finished goods and components by lot", True),
               ("sub", "Subcontracting", "Send components to a job worker and receive the product back", False),
               ("byp", "By-Products", "Record scrap aluminium and offcuts that go back to stock", False),
               ("mps", "Master Production Schedule", "Plan production weeks ahead from a demand forecast", False)]
    tl = "".join('<li><label class="mf-set"><span class="mf-set-t"><b>%s</b><small>%s</small></span><input type="checkbox" data-set="%s"%s><span class="mf-sw" aria-hidden="true"></span></label></li>'
                 % (n, x, k, " checked" if on else "") for k, n, x, on in toggles)
    steps = [("1", "Manufacture (1 step)"), ("2", "Pick components and then manufacture (2 steps)"), ("3", "Pick components, manufacture and then store products (3 steps)")]
    rl = "".join('<label class="mf-radio"><input type="radio" name="mf-steps" value="%s"%s><span>%s</span></label>' % (k, " checked" if k == "2" else "", n) for k, n in steps)
    out += sec(head("CONFIGURED AROUND YOU", "How Does Unisas Configure Manufacturing Workflows Around Your Business?",
                    "We set Odoo's switches to match how your factory actually runs, not the other way round. Change the settings as we would in a workshop "
                    "and see the flow one manufacturing order will follow.", "is-center")
               + '<div class="mf-cfg" data-cfg><div class="ox mf-ox mf-cfg-set"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Settings</a><span>Manufacturing</span></span></div><span></span><span></span></div>'
                 '<div class="mf-cfg-body"><p class="mf-cfg-h">Operations</p><ul class="mf-sets">%s</ul><p class="mf-cfg-h">Warehouse &middot; Chennai Plant</p><div class="mf-radios" role="radiogroup" aria-label="Manufacture steps">%s</div></div></div>'
                 '<div class="mf-cfg-out ox-solo"><p class="mf-cfg-oh"><b>What one manufacturing order follows</b><small data-cfg-count></small></p><ol class="mf-route" data-cfg-route></ol><p class="mf-cfg-note" data-cfg-note></p></div></div>'
                 % (tl, rl), "mf-sec--cfg")

    # 5 ---- Manufacturing with Inventory, Purchase and Quality: one shortage, end to end
    apps = [("mrp", "Manufacturing", "#0E7C86"), ("inv", "Inventory", "#1F8A78"), ("pur", "Purchase", "#3E7CB1"), ("qc", "Quality", "#B5567E")]
    cols = "".join('<div class="mf-cx-app" data-cx-app="%s" style="--c:%s"><p class="mf-cx-h"><i></i>%s</p><div class="mf-cx-b" data-cx-b="%s"></div></div>' % (k, c, n, k) for k, n, c in apps)
    out += sec(head("CONNECTED APPS", "How Can Odoo Connect Manufacturing With Inventory, Purchase and Quality?",
                    "They share one database, so a shortage in one app becomes an action in the next. Confirm a large order and follow it through: "
                    "a capacitor shortage, a purchase, an incoming inspection and, finally, a manufacturing order that is ready to start.", "is-center")
               + '<div class="mf-cx" data-cx><div class="mf-cx-bar"><span class="mf-cx-step" data-cx-step></span><span class="mf-cx-acts" data-cx-acts></span><button type="button" class="ox-sbtn" data-cx-reset>Reset</button></div>'
                 '<div class="mf-cx-grid">%s</div><ol class="mf-cx-log" data-cx-log aria-live="polite"></ol></div>' % cols, "mf-sec--cx")

    # 6 ---- configure, customize or integrate: a sorting board
    reqs = [("Fan colours as product variants, one BoM for all", "cfg", "BoM lines apply to specific variants, so one BoM covers white, brown and ivory."),
            ("Send work to Assembly Line 2 when Line 1 is full", "cfg", "Alternative work centres on the operation; planning moves the work order automatically."),
            ("Operators see the drawing at each step", "cfg", "A PDF or Google Slide worksheet on the operation, shown on the Shop Floor tablet."),
            ("Approve BoM changes before they reach the floor", "cfg", "Engineering change orders in Odoo PLM, with approval stages and BoM versions."),
            ("Job card printed in our own format", "custom", "A custom QWeb report for the work order, with your layout and barcode."),
            ("Winding length calculated from motor rating", "custom", "A small module that computes wire quantity on the BoM line from the motor's attributes."),
            ("Machine counters post produced quantities", "int", "PLC or IoT Box connection that records quantities on the running work order."),
            ("Weighing scale on the packing line", "int", "IoT Box device read directly into the quality check or quantity field."),
            ("Customer schedules arrive by EDI", "int", "A scheduled connector that creates sales orders, which then trigger production.")]
    rq = "".join('<li><button type="button" class="mf-req" data-req="%d">%s</button></li>' % (i, r[0]) for i, r in enumerate(reqs))
    lanes = "".join('<div class="mf-lane mf-lane--%s"><p class="mf-lane-h"><b>%s</b><small>%s</small></p><ul data-lane="%s"></ul></div>' % (k, n, x, k)
                    for k, n, x in [("cfg", "Configure", "Standard Odoo settings and data. Upgrades with no extra work."),
                                    ("custom", "Customize", "Code or Studio, kept small, tested and documented."),
                                    ("int", "Integrate", "Connect a machine or another system through the API or IoT.")])
    out += sec(head("CONFIGURE, CUSTOMIZE OR INTEGRATE", "When Should Manufacturing ERP Be Configured, Customized or Integrated?",
                    "Most requirements are met by configuration. We customize only where it saves real time every week, and integrate where the data already lives in a machine or another system. "
                    "Pick a requirement to see where it lands and why.", "is-center")
               + '<div class="mf-sort" data-sort><div class="mf-pile"><p class="mf-pile-h"><b>Requirements from the workshop</b><span><button type="button" class="ox-sbtn" data-sort-all>Sort all</button><button type="button" class="ox-sbtn" data-sort-reset>Reset</button></span></p><ul data-pile>%s</ul></div>'
                 '<div class="mf-lanes">%s</div><p class="mf-sort-why" data-sort-why aria-live="polite">Choose a requirement on the left.</p></div>'
                 % (rq, lanes) + data("mf-reqs", reqs), "mf-sec--sort")

    # 7 ---- production models
    models = [("mts", "Make to Stock", "Fans, pumps, packaged goods", "Reordering rules keep finished goods between a minimum and maximum, and manufacturing orders are raised in batches.",
               {"Route": "Manufacture", "BoM type": "Manufacture this product", "Trigger": "Reordering rule (min 300, max 900)", "Tracking": "By lot"},
               ["Forecast or reorder rule", "Batch MO", "Finished stock", "Sales orders ship from stock"]),
              ("mto", "Make to Order", "Custom panels, furniture, machines", "Each confirmed sales order creates its own manufacturing order, linked both ways, so the customer's order and the build stay together.",
               {"Route": "Manufacture + Replenish on Order (MTO)", "BoM type": "Manufacture this product", "Trigger": "Sales order confirmation", "Tracking": "By serial number"},
               ["Sales order", "MO for that order", "Delivery to that customer", "Invoice"]),
              ("batch", "Batch &amp; process", "Food, chemicals, cosmetics", "Recipes as BoMs with by-products and scrap, lots with expiry dates, and quality checks on every batch.",
               {"Route": "Manufacture", "BoM type": "Manufacture this product (flexible consumption)", "Trigger": "MPS or reorder rule", "Tracking": "By lot, with expiry dates"},
               ["Weigh ingredients", "Batch MO", "Lab check", "Lot released with expiry"]),
              ("eto", "Engineer to order", "Special machines, projects", "Design and production run as a project: the BoM is built per order, and costs post to the project's analytic account.",
               {"Route": "Manufacture + MTO", "BoM type": "BoM per order, via PLM", "Trigger": "Project milestone", "Tracking": "By serial number"},
               ["Design in PLM", "Approved BoM", "MO per milestone", "Cost to project"]),
              ("sub", "Subcontracting (job work)", "Plating, heat treatment, winding", "Components are sent to the job worker, who returns finished parts. Stock at the vendor is tracked, and the bill is matched to what came back.",
               {"Route": "Buy + Resupply Subcontractor on Order", "BoM type": "Subcontracting", "Trigger": "Purchase order to the job worker", "Tracking": "By lot"},
               ["PO to job worker", "Components dispatched", "Finished parts received", "Bill matched"]),
              ("kit", "Kits &amp; assembly", "Spare kits, gift packs, combos", "Kits are sold and delivered as their components, with no manufacturing order at all. Light assembly uses a one-step order.",
               {"Route": "None (kit)", "BoM type": "Kit", "Trigger": "Sales order", "Tracking": "On components"},
               ["Sales order", "Components picked", "Delivered as one kit", "Invoice"])]
    mt = "".join('<button type="button" role="tab" class="mf-mtab%s" id="mf-mtab-%s" aria-selected="%s"%s data-model="%d">%s</button>'
                 % (" is-on" if i == 0 else "", k, "true" if i == 0 else "false", "" if i == 0 else ' tabindex="-1"', i, n) for i, (k, n, *_r) in enumerate(models))
    out += sec(head("PRODUCTION MODELS", "How Does Unisas Adapt Odoo for Different Production Models?",
                    "The same Odoo app runs a make-to-stock fan line and a make-to-order machine shop. What changes is the route, the BoM type, what triggers production and how you track it.")
               + '<div class="mf-models" data-models><div class="mf-mtabs" role="tablist" aria-label="Production models">%s</div>'
                 '<div class="mf-mpanel" role="tabpanel" aria-live="polite"><div class="mf-mp-copy"><p class="mf-mp-for mono" data-m-for></p><h3 data-m-name></h3><p data-m-text></p><ol class="mf-mp-flow" data-m-flow></ol></div>'
                 '<div class="ox mf-ox mf-mp-form"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Product</a><span>Setup in Odoo</span></span></div><span></span><span></span></div>'
                 '<dl class="mf-mp-dl" data-m-dl></dl><div class="mf-bomtype"><p>BoM Type</p><span data-bt="Manufacture this product">Manufacture this product</span><span data-bt="Kit">Kit</span><span data-bt="Subcontracting">Subcontracting</span></div></div></div></div>'
                 % mt + data("mf-models", models), "mf-sec--models")

    # 8 ---- data migration: Odoo's import screen
    cols8 = [("Parent Product", "Product", "FAN-A48"), ("Component Code", "BoM Lines / Component", "CAP-2.5UF"), ("Qty", "BoM Lines / Quantity", "1"),
             ("Unit", "BoM Lines / Product Unit of Measure", "Nos"), ("Operation", "Operations / Operation", "Final assembly"),
             ("Work Centre", "Operations / Work Center", "Assembly Line 1"), ("Std Time (min)", "Operations / Default Duration", "1.5"), ("Rev", "", "C")]
    mrows = "".join('<tr><td><b>%s</b><small>%s</small></td><td class="ox-muted">&rarr;</td><td>%s</td></tr>' % (c, ex, f or '<span class="mf-skip">To import, select a field&hellip;</span>') for c, f, ex in cols8)
    order = [("Units of measure", "Nos, kg, m, sets", "14"), ("Products &amp; components", "With internal reference and HSN", "1,860"), ("Work centres", "Costs per hour, capacity", "6"),
             ("Bills of materials", "Lines and operations", "212"), ("Opening stock", "By location, lot and serial", "3,940 lines"), ("Open orders &amp; WIP", "Started work recreated as MOs", "37")]
    out += sec(head("DATA MIGRATION", "How Does Unisas Handle Manufacturing Data Migration?",
                    "BoMs are where migrations fail: codes that don't match, units written three ways, work centres that changed names. We load in a fixed order and test every file before it goes in. "
                    "Try it with a BoM export from Excel.", "is-center")
               + '<div class="mf-mig"><div class="ox mf-ox" data-imp><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Bills of Materials</a><span>Import a File</span></span></div><span></span>'
                 '<span class="mf-imp-btns"><button type="button" class="ox-pbtn" data-imp-test>Test</button><button type="button" class="ox-sbtn" data-imp-go disabled>Import</button></span></div>'
                 '<div class="mf-imp-file"><span class="mf-xls">XLS</span><b>bom_aero_breeze_turbo.xlsx</b><small>62 rows &middot; Sheet1</small><button type="button" class="ox-sbtn" data-imp-fix hidden>Apply cleansing rules</button></div>'
                 '<div class="mf-imp-msg" data-imp-msg aria-live="polite"></div>'
                 '<div class="ox-scroll"><table class="ox-table mf-imp-t"><thead><tr><th>File Column</th><th></th><th>Odoo Field</th></tr></thead><tbody>%s</tbody></table></div></div>'
                 '<ol class="mf-load ox-solo"><li class="mf-load-h"><b>Load order</b><small>Each file depends on the one before it</small></li>%s</ol></div>'
                 % (mrows, "".join('<li><span class="mono">%02d</span><span><b>%s</b><small>%s</small></span><em>%s</em></li>' % (i + 1, a, b, c) for i, (a, b, c) in enumerate(order))),
               "mf-sec--mig")

    # 9 ---- visibility, traceability, cost
    trace = [[0, "WH/OUT/00231", "Aero 48 Ceiling Fan", "FAN-2610-0042", "Oct 30", "WH/Stock", "Customers", "250.00 Units"],
             [1, "WH/MO/00042", "Aero 48 Ceiling Fan", "FAN-2610-0042", "Oct 27", "Production", "WH/Stock", "250.00 Units"],
             [2, "WH/MO/00042", "Motor Assembly 48W", "MTR-2610-0187", "Oct 21", "WH/Stock", "Production", "250.00 Units"],
             [3, "WH/MO/00043", "Motor Assembly 48W", "MTR-2610-0187", "Oct 18", "Production", "WH/Stock", "250.00 Units"],
             [4, "WH/IN/00049", "Copper Winding Wire 0.35mm", "CW-118", "Oct 9", "Vendors", "WH/Stock", "105.00 kg"],
             [4, "WH/IN/00051", "Ball Bearing 6202", "BRG-2209", "Oct 10", "Vendors", "WH/Stock", "500.00 Units"],
             [2, "WH/IN/00055", "Capacitor 2.5&micro;F", "CAP-L2207", "Oct 14", "Vendors", "WH/Stock", "250.00 Units"],
             [2, "WH/IN/00050", "Blade Set 1200mm", "BLD-L0915", "Oct 10", "Vendors", "WH/Stock", "250.00 Units"]]
    cost = [["Components", "Motor Assembly 48W", 250, 1012.4, 1031.2], ["Components", "Blade Set 1200mm", 250, 365, 365], ["Components", "Canopy &amp; Downrod Kit", 250, 142, 142],
            ["Components", "Capacitor 2.5&micro;F", 250, 38, 38], ["Components", "Packing Carton, 5-ply", 250, 46, 46], ["Components", "Scrap: blades rejected", 0, 0, 3.65],
            ["Operations", "Blade pressing &middot; Press Shop", 150, 900, 900], ["Operations", "Final assembly &middot; Assembly Line 1", 375, 600, 600],
            ["Operations", "Powder coating &middot; Paint Shop", 200, 820, 820], ["Operations", "Run test &amp; pack &middot; Testing &amp; QC", 125, 540, 540]]
    real_min = [150 * 1.04, 375 * 1.11, 200 * 0.97, 125 * 1.02]
    oee = [[w["n"], w["code"], w["oee"], a, p, q, losses] for w, (a, p, q, losses) in zip(WC, [
        (86, 94, 97, [["Setup &amp; adjustments", 6.5], ["Material availability", 2.0], ["Equipment failure", 3.5]]),
        (82, 90, 96.5, [["Equipment failure", 9.5], ["Reduced speed", 5.0], ["Setup &amp; adjustments", 3.5]]),
        (92, 95, 96.8, [["Material availability", 4.5], ["Setup &amp; adjustments", 3.0]]),
        (90, 93, 95.7, [["Reduced speed", 4.0], ["Setup &amp; adjustments", 3.5]]),
        (78, 92, 97.2, [["Setup &amp; adjustments", 12.0], ["Cleaning between colours", 6.0], ["Equipment failure", 4.0]]),
        (97, 96, 98, [["Material availability", 1.5]])])]
    tabs9 = "".join('<button type="button" class="mf-vtab%s" data-vt="%s" aria-pressed="%s">%s</button>' % (" is-on" if i == 0 else "", k, "true" if i == 0 else "false", n)
                    for i, (k, n) in enumerate([("trace", "Traceability"), ("cost", "Cost Analysis"), ("oee", "Overall Equipment Effectiveness")]))
    out += sec(head("VISIBILITY &amp; COST CONTROL", "How Can Odoo Improve Production Visibility, Traceability and Cost Control?",
                    "Because every move, minute and component is recorded against the order, the reports below come straight from the shop floor, not from a spreadsheet at month end.", "is-center")
               + '<div class="ox mf-ox mf-vis" data-vis>%s<div class="mf-vtabs" role="group" aria-label="Reports">%s</div><div class="mf-vis-body" data-vis-body></div></div>'
                 % (nav(app_icon), tabs9) + data("mf-trace", trace) + data("mf-cost", {"rows": cost, "real": real_min}) + data("mf-oee", oee), "mf-sec--vis")

    # 10 ---- testing before go-live
    tests = [("Planner", "Sales order for 250 fans creates MO and motor sub-order", "pass", ""),
             ("Stores", "Pick components for WH/MO/00042 in two steps", "pass", ""),
             ("Operator", "Start, pause and finish work orders on the tablet", "pass", ""),
             ("Operator", "Record blade pitch on the quality check", "pass", ""),
             ("Stores", "Copper wire consumed in kg for 250 motors", "fail", "Consumed 105,000 kg: BoM line in g, product in kg. Fixed the unit of measure on the BoM line."),
             ("Quality", "Failed noise test sends fan to rework", "pass", ""),
             ("Planner", "Paint Shop overload moves orders to the next day", "fail", "Working hours had no lunch break, so capacity was overstated. Corrected the Paint Shop calendar."),
             ("Accounts", "Finished-goods value equals MO actual cost", "pass", "")]
    out += sec(head("TESTING", "How Does Unisas Test Manufacturing Workflows Before Go-Live?",
                    "We run your real products through test cycles in a copy of your database. Each person tests the steps they will do on day one, and every failure is fixed and re-run before sign-off.", "is-center")
               + '<div class="mf-test" data-test><div class="ox mf-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Go-live testing</a><span data-test-cycle>Test cycle 1</span></span></div><span></span>'
                 '<span class="mf-test-btns"><button type="button" class="ox-pbtn" data-test-run>Run test cycle</button></span></div>'
                 '<div class="ox-scroll"><table class="ox-table mf-test-t"><thead><tr><th>Role</th><th>Scenario</th><th>Result</th></tr></thead><tbody data-test-rows></tbody></table></div></div>'
                 '<div class="mf-sign ox-solo"><p class="mf-sign-h"><b>Sign-off</b><small data-test-sum>Not run yet</small></p><ul data-test-sign></ul><p class="mf-sign-res" data-test-res aria-live="polite"></p></div></div>'
                 + data("mf-tests", tests), "mf-sec--test")

    # 11 ---- what's included
    base = [("Discover &amp; design", ["Process workshops on the shop floor", "Production model, routes and steps agreed", "BoM and routing structure designed", "Fit-gap with effort for every gap"]),
            ("Configure", ["Manufacturing, Inventory and Purchase set up", "Work centres, calendars and cost rates", "Operations, worksheets and quality points", "Reordering rules and replenishment"]),
            ("Data &amp; integrations", ["Products, BoMs and routings loaded", "Opening stock by lot and location", "Open orders and work in progress", "Accounting, valuation and costing linked"]),
            ("Train &amp; go live", ["Role-based training on your products", "Shop-floor tablets set up at each station", "Test cycles and sign-off", "Hypercare on the floor after go-live"])]
    addons = [("qc", "Quality", "Control points, checks and alerts", 1), ("mnt", "Maintenance", "Preventive plans and breakdown requests per work centre", 1),
              ("plm", "PLM", "Engineering change orders and BoM versions", 2), ("iot", "IoT &amp; machines", "Scales, counters and PLC connections", 2),
              ("mps", "MPS", "Weekly production plan from forecast", 1), ("sub", "Subcontracting", "Job-work flows with resupply", 1)]
    bc = "".join('<div class="mf-pk-col"><span class="mf-pk-n mono">%02d</span><h3>%s</h3><ul>%s</ul></div>' % (i + 1, t, "".join("<li>%s%s</li>" % (TICK, p) for p in pts)) for i, (t, pts) in enumerate(base))
    ad = "".join('<li><label class="mf-add"><input type="checkbox" data-add="%d" value="%s"><span class="mf-add-b"><b>%s</b><small>%s</small></span><em>+%d wk</em></label></li>' % (w, k, n, x, w) for k, n, x, w in addons)
    out += sec(head("WHAT'S INCLUDED", "What Does a Manufacturing ERP Implementation With Unisas Include?",
                    "One fixed-scope project from the first shop-floor walk to the first weeks after go-live. Add the apps your plant needs and see how the plan changes.", "is-center")
               + '<div class="mf-pkg"><div class="mf-pk-head"><span class="mono">ODOO MANUFACTURING IMPLEMENTATION</span><strong data-pk-sum>Core scope &middot; 10 to 12 weeks</strong></div>'
                 '<div class="mf-pk-body">%s</div><div class="mf-pk-add"><p><b>Add to the scope</b><small>Each one is configured, loaded with your data and trained.</small></p><ul data-pk>%s</ul></div>'
                 '<div class="mf-pk-foot"><span data-pk-apps>Manufacturing &middot; Inventory &middot; Purchase &middot; Accounting</span>'
                 '<a href="#get-demo" class="link-arrow" data-svc-cta="implementation">Get a scoped quote %s</a></div></div>' % (bc, ad, g["ARROW"]), "mf-sec--pkg")

    # 12 ---- support after go-live
    tickets = [("new", "WO for Paint Shop stuck in Waiting", "Assembly Line 1", "Urgent", 2, "red",
                "The preceding work order was finished on paper, not on the tablet. We closed it with the right quantity, and added a supervisor check to the end-of-shift list."),
               ("new", "Add BoM for the new Aero 52 model", "Engineering", "Normal", 18, "green",
                "Copied the Aero 48 BoM as a new version, swapped the motor and blades, and set the new routing times from the pilot run."),
               ("prog", "Copper wire cost looks too high", "Accounts", "Normal", 9, "orange",
                "The last receipt was valued in grams. We corrected the vendor's unit of measure on the purchase line and revalued the stock."),
               ("prog", "Train the new night-shift supervisor", "Production", "Low", 30, "green",
                "A one-hour session on the shop floor, with the short guide for starting, blocking and closing work orders."),
               ("done", "Paint Shop OEE dropped to 58%", "Production", "Urgent", 0, "",
                "Colour changes were logged as equipment failures. We added a 'Colour change' loss reason so OEE now shows setup time correctly."),
               ("done", "Label printer on the packing line", "Stores", "Normal", 0, "",
                "Re-paired the printer with the IoT Box after a network change and printed a test lot label.")]
    stages = [("new", "New"), ("prog", "In Progress"), ("done", "Solved")]
    tk = ""
    for k, n in stages:
        cards = "".join('<button type="button" class="mf-tk" data-tk="%d"><b>%s</b><small>%s</small><span class="mf-tk-f"><span class="mf-pri mf-pri--%s">%s</span>%s</span></button>'
                        % (i, t[1], t[2], t[3].lower(), t[3], '<span class="mf-sla mf-sla--%s">SLA %dh</span>' % (t[5], t[4]) if t[5] else '<span class="mf-sla is-ok">Solved</span>')
                        for i, t in enumerate(tickets) if t[0] == k)
        tk += '<div class="mf-tk-col"><p class="mf-tk-h"><b>%s</b><small>%d</small></p>%s</div>' % (n, sum(1 for t in tickets if t[0] == k), cards)
    plans = [("First 4 weeks", "Hypercare", "A consultant on the floor or on call during every shift change, fixing issues the same day."),
             ("Every month", "Support desk", "Tickets with response times by priority, small changes and new BoMs included."),
             ("Every quarter", "Improvement review", "OEE, cost variance and late orders reviewed with you, and the next improvements planned.")]
    out += sec(head("AFTER GO-LIVE", "How Does Unisas Support Manufacturing Operations After Go-Live?",
                    "Production does not stop for software questions. Our support desk runs in Odoo Helpdesk with response times by priority. Open a ticket to see how it was solved.", "is-center")
               + '<div class="mf-sup"><div class="ox mf-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Helpdesk</a><span>Manufacturing Support</span></span></div><span></span><span></span></div>'
                 '<div class="mf-tk-board">%s</div><div class="mf-tk-det" data-tk-det aria-live="polite"><p class="ox-muted">Select a ticket to see the resolution.</p></div></div>'
                 '<ol class="mf-plans">%s</ol></div>' % (tk, "".join('<li><small class="mono">%s</small><b>%s</b><span>%s</span></li>' % p for p in plans))
               + data("mf-tickets", tickets), "mf-sec--sup")

    # 13 ---- plan your implementation
    out += sec('<div class="mf-plan2"><div>%s<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Plan my manufacturing ERP %s</a></div></div>'
               '<div class="mf-pl ox-solo" data-planner><p class="mf-pl-h"><b>Implementation planner</b><small>A first estimate. We confirm it after a shop-floor visit.</small></p>'
               '<div class="mf-pl-in"><label><span>Production model</span><select data-pl="model"><option value="0">Make to stock</option><option value="1">Make to order</option><option value="2">Batch &amp; process</option><option value="3">Engineer to order</option></select></label>'
               '<label><span>Products with a BoM <b data-pl-out="boms">200</b></span><input type="range" min="10" max="2000" step="10" value="200" data-pl="boms"></label>'
               '<label><span>Work centres <b data-pl-out="wcs">8</b></span><input type="range" min="1" max="40" value="8" data-pl="wcs"></label>'
               '<div class="mf-pl-seg"><span>Plants</span><span class="mf-seg" role="group" aria-label="Plants"><button type="button" data-plants="1" class="is-on" aria-pressed="true">1</button><button type="button" data-plants="2" aria-pressed="false">2</button><button type="button" data-plants="3" aria-pressed="false">3+</button></span></div>'
               '<div class="mf-pl-chk"><label><input type="checkbox" data-pl-x="2"> Machine or IoT integration</label><label><input type="checkbox" data-pl-x="1"> Quality &amp; maintenance</label><label><input type="checkbox" data-pl-x="2"> Migration from another ERP</label></div></div>'
               '<div class="mf-pl-out"><ol class="mf-pl-bars" data-pl-bars></ol><p class="mf-pl-tot" data-pl-tot aria-live="polite"></p></div></div></div>'
               % (head("PLAN YOUR PROJECT", "How Can You Plan Your Manufacturing ERP Implementation?",
                       "Start with one plant and the products that matter most, get the shop floor reporting reliably, then add planning, quality and maintenance. "
                       "Tell the planner about your factory for a first timeline, then talk it through with us."), g["ARROW"]), "mf-sec--plan")

    return out + JS


JS = r'''<script>
(function(){
  function J(id){var e=document.getElementById(id);return e?JSON.parse(e.textContent):null;}
  function inr(n,d){var s=Math.abs(n).toLocaleString('en-IN',{minimumFractionDigits:d===false?0:2,maximumFractionDigits:d===false?0:2});return (n<0?'-':'')+'₹ '+s;}
  function num(n,d){return n.toLocaleString('en-IN',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}
  function press(group,el){group.forEach(function(b){var on=b===el;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});}
  function hm(min){var h=Math.floor(min/60),m=Math.round(min%60);if(m===60){h++;m=0;}return (h<10?'0':'')+h+':'+(m<10?'0':'')+m;}

  /* --- 1 factory floor plan --- */
  var zb=document.querySelector('[data-zones]');
  if(zb){var Z=J('mf-zones'),zs=[].slice.call(zb.querySelectorAll('[data-zone]'));
    function zd(i){var z=Z[i];zb.querySelector('[data-z-area]').innerHTML=z[1];zb.querySelector('[data-z-title]').innerHTML=z[2];zb.querySelector('[data-z-story]').innerHTML='&ldquo;'+z[3]+'&rdquo;';
      zb.querySelector('[data-z-why]').innerHTML=z[4];zb.querySelector('[data-z-fix]').innerHTML=z[5];}
    zs.forEach(function(b){b.addEventListener('click',function(){press(zs,b);zd(+b.getAttribute('data-zone'));});});zd(0);}

  /* --- 2 document chain --- */
  var ch=document.querySelector('[data-chain]');
  if(ch){var C=J('mf-chain'),cur=0,rb=[].slice.call(ch.querySelectorAll('[data-ch]'));
    function cd(){var c=C[cur];
      rb.forEach(function(b,i){b.parentNode.classList.toggle('is-done',i<cur);b.parentNode.classList.toggle('is-cur',i===cur);b.setAttribute('aria-current',i===cur?'step':'false');});
      ch.querySelector('[data-ch-app]').innerHTML=c[0];ch.querySelector('[data-ch-app]').style.color=c[1];ch.querySelector('[data-ch-title]').innerHTML=c[3];
      ch.querySelector('[data-ch-ref]').innerHTML=c[2];ch.querySelector('[data-ch-text]').innerHTML=c[4];
      var cnt={};for(var i=1;i<=cur;i++){cnt[C[i][5]]=(cnt[C[i][5]]||0)+(C[i][5]==='Work Orders'?4:1);}
      ch.querySelector('[data-ch-smart]').innerHTML=Object.keys(cnt).map(function(k){return '<span class="mf-sb is-new"><b>'+cnt[k]+'</b>'+k+'</span>';}).join('')||'<span class="mf-sb is-empty">No linked documents yet</span>';
      ch.querySelector('[data-ch-log]').innerHTML=C.slice(0,cur+1).map(function(c,i){return '<li style="--c:'+c[1]+'"'+(i===cur?' class="is-new"':'')+'><b class="mono">'+c[2]+'</b><span>'+c[3]+'</span></li>';}).reverse().join('');
      ch.querySelector('[data-ch-prev]').disabled=cur===0;var nx=ch.querySelector('[data-ch-next]');nx.textContent=cur===C.length-1?'Start again':'Next step';}
    ch.querySelector('[data-ch-next]').addEventListener('click',function(){cur=cur===C.length-1?0:cur+1;cd();});
    ch.querySelector('[data-ch-prev]').addEventListener('click',function(){if(cur>0){cur--;cd();}});
    rb.forEach(function(b,i){b.addEventListener('click',function(){cur=i;cd();});});cd();}

  /* --- 3 manufacturing explorer --- */
  var mx=document.querySelector('[data-mx]');
  if(mx){var WC=J('mf-wc'),R=J('mf-routes'),P=J('mf-products'),M=J('mf-mos'),B=J('mf-bom'),PL=J('mf-plan');
    var body=mx.querySelector('[data-mx-body]'),crumb=mx.querySelector('[data-mx-crumb]'),q=mx.querySelector('[data-mx-q]'),menus=[].slice.call(mx.querySelectorAll('[data-mx-menu]'));
    var st={menu:'wc',mo:null,wc:null,tab:'wo',bq:250,fold:false};
    var WCK={};WC.forEach(function(w){WCK[w.k]=w;w.blocked=false;});
    var STL={draft:['Draft','dr'],confirmed:['Confirmed','cf'],progress:['In Progress','ip'],to_close:['To Close','tc'],done:['Done','dn']};
    var WOL={wait:['Waiting','wt'],ready:['Ready','rd'],progress:['In Progress','ip'],done:['Finished','dn']};
    M.forEach(function(m){m.log=[{w:'Unisas Bot',t:'Manufacturing order created from '+m.src}];});
    function mst(m){if(m.st!=='open')return m.st;if(m.wo.every(function(s){return s==='done';}))return 'to_close';if(m.wo.some(function(s){return s==='progress'||s==='done';}))return 'progress';return 'confirmed';}
    function ops(m){return R[P[m.p].r];}
    function nextOp(m){var r=ops(m);for(var i=0;i<m.wo.length;i++){if(m.wo[i]!=='done')return r[i][0]+' &middot; '+WCK[r[i][1]].n;}return '';}
    function badge(s){var x=STL[s];return '<span class="mf-b mf-b--'+x[1]+'">'+x[0]+'</span>';}
    function refresh(m){/* first unfinished work order becomes ready once components are reserved */
      if(m.st!=='open')return;var r=false;for(var i=0;i<m.wo.length;i++){if(m.wo[i]==='done')continue;if(m.wo[i]==='wait'&&m.comp==='ok'&&!r)m.wo[i]='ready';r=true;}}
    function setMenu(k){st.menu=k;st.mo=null;st.wc=null;menus.forEach(function(b){var on=b.getAttribute('data-mx-menu')===k;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});render();}
    function wcStats(w){var s={ready:0,wait:0,progress:0,load:0};
      M.forEach(function(m){if(m.st==='done')return;ops(m).forEach(function(o,i){if(o[1]!==w.k||m.wo[i]==='done')return;s[m.wo[i]]++;s.load+=m.qty*o[2]/60;});});return s;}
    function wcKanban(){var t=q.value.trim().toLowerCase();
      var L=WC.filter(function(w){return !t||(w.n+' '+w.code).toLowerCase().indexOf(t)>-1;});
      if(!L.length)return '<p class="ox-empty">No work center matches.</p>';
      return '<div class="mf-wck">'+L.map(function(w){var s=wcStats(w),act=s.ready+s.progress>0,mx=Math.max.apply(null,w.hist.concat([s.load,1]));
        var bars=w.hist.concat([s.load]).map(function(h,i){return '<i style="--h:'+(h/mx*100).toFixed(1)+'"'+(i===4?' class="is-now"':'')+' title="'+(i===4?'This week':'Week -'+(4-i))+': '+num(h,1)+' h"></i>';}).join('');
        return '<article class="mf-wcc'+(w.blocked?' is-blocked':'')+'" data-wc="'+w.k+'" tabindex="0"><header><span class="mf-wc-dot" title="'+(w.blocked?'Blocked':'Normal')+'"></span><b>'+w.n+'</b><small>'+w.code+'</small></header>'+
          '<div class="mf-wcc-b"><div><span class="'+(act?'ox-pbtn':'ox-sbtn')+'">'+(act?'Work Orders':'Plan Orders')+'</span><span class="mf-wcc-tag">'+w.tag+'</span></div>'+
          '<dl><div><dt>In Progress</dt><dd>'+s.progress+'</dd></div><div><dt>Ready</dt><dd>'+s.ready+'</dd></div><div><dt>Waiting</dt><dd>'+s.wait+'</dd></div>'+
          '<div class="'+(w.late?'is-late':'')+'"><dt>Late</dt><dd>'+w.late+'</dd></div><div><dt>Load</dt><dd>'+num(s.load,1)+' Hours</dd></div><div><dt>OEE</dt><dd class="'+(w.oee<75?'mf-red':(w.oee>=90?'mf-grn':''))+'">'+num(w.oee,1)+'%</dd></div></dl></div>'+
          '<div class="mf-wcc-g" aria-hidden="true">'+bars+'</div></article>';}).join('')+'</div>';}
    function wcForm(w){var s=wcStats(w);
      return '<div class="mf-form"><div class="ox-f-bar"><span class="ox-f-btns"><button type="button" class="'+(w.blocked?'ox-pbtn':'ox-sbtn')+'" data-do="block">'+(w.blocked?'Unblock':'Block')+'</button></span>'+
        '<span class="mf-smart"><span class="mf-sb"><b>'+num(w.oee,2)+'%</b>OEE</span><span class="mf-sb"><b>'+num(100-w.oee,1)+'%</b>Lost</span><span class="mf-sb"><b>'+num(s.load,1)+' h</b>Load</span><span class="mf-sb"><b>'+(w.eff)+'%</b>Performance</span></span></div>'+
        '<div class="ox-sheet">'+(w.blocked?'<span class="ox-ribbon is-lost">BLOCKED</span>':'')+'<p class="mf-f-k">Work Center</p><h3>'+w.n+'</h3>'+
        '<dl class="ox-fields"><div><dt>Tag</dt><dd><span class="ox-tag ox-tag--sky">'+w.tag+'</span></dd></div><div><dt>Code</dt><dd>'+w.code+'</dd></div>'+
        '<div><dt>Alternative Workcenters</dt><dd>'+(w.alt?'<span class="ox-tag ox-tag--purple">'+w.alt+'</span>':'<span class="ox-muted">None</span>')+'</dd></div><div><dt>Working Hours</dt><dd>Standard 48 hours/week</dd></div></dl>'+
        '<div class="ox-ftabs"><span class="is-on">General Information</span><span>Specific Capacities</span><span>Description</span></div>'+
        '<div class="mf-wc-gi"><div><p class="mf-gi-h">Production Information</p><dl class="mf-gi"><div><dt>Time Efficiency</dt><dd>'+w.eff+'.00 %</dd></div><div><dt>Capacity</dt><dd>'+w.cap+'.00</dd></div><div><dt>OEE Target</dt><dd>90.00 %</dd></div></dl></div>'+
        '<div><p class="mf-gi-h">Costing Information</p><dl class="mf-gi"><div><dt>Cost per hour</dt><dd>'+inr(w.cost)+'</dd></div></dl><p class="mf-gi-h">Time</p><dl class="mf-gi"><div><dt>Setup Time</dt><dd>'+w.setup+':00 minutes</dd></div><div><dt>Cleanup Time</dt><dd>'+w.clean+':00 minutes</dd></div></dl></div></div></div></div>';}
    function moList(){var t=q.value.trim().toLowerCase();
      var L=M.filter(function(m){return !t||(m.ref+' '+P[m.p].n+' '+m.src).toLowerCase().indexOf(t)>-1;});
      if(!L.length)return '<p class="ox-empty">No manufacturing order matches.</p>';
      return '<div class="ox-scroll"><table class="ox-table mf-mo-t"><thead><tr><th class="ox-chk"><span class="ox-cb"></span></th><th>Reference</th><th>Start</th><th>Product</th><th>Next Operation</th><th>Source</th><th>Component Status</th><th class="ox-num">Quantity</th><th>State</th></tr></thead><tbody>'+
        L.map(function(m){var s=mst(m);return '<tr data-mo="'+m.id+'" tabindex="0"><td class="ox-chk"><span class="ox-cb"></span></td><td><b>'+m.ref+'</b></td><td>'+m.date+'</td><td>'+P[m.p].n+'</td><td>'+nextOp(m)+'</td><td class="ox-muted">'+m.src+'</td>'+
          '<td>'+(s==='done'?'':(m.comp==='ok'?'<span class="mf-avail is-ok">Available</span>':'<span class="mf-avail">Not Available</span>'))+'</td><td class="ox-num">'+num(m.qty,2)+'</td><td>'+badge(s)+'</td></tr>';}).join('')+'</tbody></table></div>';}
    function moForm(m){var s=mst(m),r=ops(m),i,btn='';
      if(s==='draft')btn='<button type="button" class="ox-pbtn" data-do="confirm">Confirm</button>';
      else if(s!=='done'&&m.comp!=='ok')btn='<button type="button" class="ox-pbtn" data-do="avail">Check availability</button>';
      else if(s==='to_close')btn='<button type="button" class="ox-pbtn" data-do="produce">Produce All</button>';
      else if(s!=='done')btn='<button type="button" class="ox-sbtn" data-do="produce">Produce All</button>';
      if(s!=='done'&&s!=='draft')btn+='<span class="ox-sbtn is-off">Scrap</span>';
      var order=['draft','confirmed','progress','done'],ci=order.indexOf(s==='to_close'?'progress':s);
      var bar=order.map(function(k,j){return '<span class="ox-sb'+(j===ci?' is-cur':'')+(j<ci?' is-done':'')+'">'+STL[k][0]+'</span>';}).join('');
      var done=m.wo.filter(function(x){return x==='done';}).length,prod=s==='done'?m.qty:0;
      var comp='<table class="mf-lines"><thead><tr><th>Product</th><th>From</th><th class="ox-num">To Consume</th><th class="ox-num">Quantity</th><th>UoM</th><th></th></tr></thead><tbody>'+P[m.p].comp.map(function(c,j){var need=c[1]*m.qty,short=m.comp!=='ok'&&j===3;
          return '<tr><td>'+c[0]+'</td><td class="ox-muted">WH/Stock</td><td class="ox-num">'+num(need,2)+'</td><td class="ox-num">'+num(s==='done'?need:(s==='draft'?0:need*done/r.length),2)+'</td><td>'+c[2]+'</td><td>'+(s==='done'||s==='draft'?'':(short?'<span class="mf-avail">Not Available</span>':'<span class="mf-avail is-ok">Available</span>'))+'</td></tr>';}).join('')+'</tbody></table>';
      var wo='<table class="mf-lines"><thead><tr><th>Operation</th><th>Work Center</th><th class="ox-num">Expected Duration</th><th class="ox-num">Real Duration</th><th>Status</th><th></th></tr></thead><tbody>'+r.map(function(o,j){var x=m.wo[j],e=m.qty*o[2],act='';
          if(m.st==='open'&&x==='ready')act='<button type="button" class="ox-pbtn mf-wo-btn" data-wo="'+j+'" data-to="progress">Start</button>';
          if(m.st==='open'&&x==='progress')act='<button type="button" class="ox-pbtn mf-wo-btn is-done" data-wo="'+j+'" data-to="done">Done</button>';
          var real=x==='done'?hm(e*(0.94+((j*7+m.id*3)%13)/60)):(x==='progress'?'<span class="mf-run">'+hm(e*0.5)+'</span>':'00:00');
          var lbl=x==='wait'&&m.comp!=='ok'&&m.st==='open'?['Waiting for components','wt']:WOL[x];
          return '<tr class="is-'+x+'"><td>'+o[0]+'</td><td>'+WCK[o[1]].n+'</td><td class="ox-num">'+hm(e)+'</td><td class="ox-num">'+real+'</td><td><span class="mf-b mf-b--'+lbl[1]+'">'+lbl[0]+'</span></td><td class="ox-num">'+act+'</td></tr>';}).join('')+'</tbody></table>';
      var tabs='<div class="ox-ftabs mf-ftabs"><button type="button" data-tab="comp" class="'+(st.tab==='comp'?'is-on':'')+'">Components</button><button type="button" data-tab="wo" class="'+(st.tab==='wo'?'is-on':'')+'">Work Orders</button><button type="button" data-tab="misc" class="'+(st.tab==='misc'?'is-on':'')+'">Miscellaneous</button></div>';
      var misc='<dl class="ox-fields mf-misc"><div><dt>Operation Type</dt><dd>Chennai Plant: Manufacturing</dd></div><div><dt>Components Location</dt><dd>WH/Pre-Production</dd></div><div><dt>Finished Products Location</dt><dd>WH/Stock</dd></div><div><dt>Lot/Serial</dt><dd>FAN-2610-'+(m.id+41)+'</dd></div></dl>';
      var log=m.log.slice().reverse().map(function(l){return '<div class="ox-msg">'+(l.w==='Unisas Bot'?'<span class="ox-av is-bot">U</span>':'<span class="ox-av is-msg" style="--c:'+(l.w[0]==='M'?'#4C9F70':'#3E7CB1')+'">'+l.w[0]+'</span>')+'<div><p><b>'+l.w+'</b> <small>just now</small></p><p>'+l.t+'</p></div></div>';}).join('');
      return '<div class="ox-form mf-moform"><div class="ox-f-main"><div class="ox-f-bar"><span class="ox-f-btns">'+btn+'</span><span class="ox-sbar is-mini mf-sbar">'+bar+'</span></div>'+
        '<div class="ox-sheet">'+(s==='done'?'<span class="ox-ribbon">DONE</span>':'')+'<div class="mf-smart is-top"><button type="button" class="mf-sb" data-do="bom"><b>'+P[m.p].code+'</b>Structure &amp; Cost</button><span class="mf-sb"><b>'+done+'/'+r.length+'</b>Work Orders</span></div>'+
        '<p class="mf-f-k">Manufacturing Order</p><h3>'+m.ref+'</h3>'+
        '<dl class="ox-fields"><div><dt>Product</dt><dd>['+P[m.p].code+'] '+P[m.p].n+'</dd></div><div><dt>Scheduled Date</dt><dd>'+m.date+', 08:00</dd></div>'+
        '<div><dt>Quantity</dt><dd><b>'+num(prod,2)+'</b>&nbsp;/ '+num(m.qty,2)+' Units</dd></div><div><dt>Component Status</dt><dd>'+(s==='done'?'<span class="ox-muted">Consumed</span>':(m.comp==='ok'?'<span class="mf-avail is-ok">Available</span>':'<span class="mf-avail">Not Available</span>'))+'</dd></div>'+
        '<div><dt>Bill of Material</dt><dd>'+P[m.p].code+': '+P[m.p].n+'</dd></div><div><dt>Responsible</dt><dd>'+m.resp+'</dd></div></dl>'+tabs+(st.tab==='comp'?comp:(st.tab==='wo'?wo:misc))+'</div></div>'+
        '<aside class="ox-chatter"><div class="ox-ch-btns"><span class="ox-pbtn">Send message</span><span class="ox-sbtn">Log note</span></div><p class="ox-ch-sep">Today</p>'+log+'</aside></div>';}
    function bomView(){var qn=st.bq,rows='',ready=Infinity,tot=0,lead=0;
      function mcost(){var c=0;B.motor.forEach(function(x){c+=x[2]*x[7];});R.motor.forEach(function(o){c+=o[2]/60*WCK[o[1]].cost;});return c;}
      B.comp.forEach(function(c){var need=c[2]*qn,cst=(c[8]?mcost():c[7])*c[2],ok=c[4]>=need;ready=Math.min(ready,Math.floor(c[4]/c[2]));lead=Math.max(lead,c[6]);tot+=cst*qn;
        rows+='<tr class="'+(c[8]?'is-fold':'')+'"'+(c[8]?' data-fold tabindex="0"':'')+'><td class="mf-bo-1">'+(c[8]?'<span class="mf-caret">'+(st.fold?'&#9662;':'&#9656;')+'</span>':'')+'['+c[0]+'] '+c[1]+'</td><td class="ox-num">'+num(need,2)+' '+c[3]+'</td><td class="ox-num">'+num(c[4],2)+'</td>'+
          '<td>'+(ok?'<span class="mf-avail is-ok">Available</span>':'<span class="mf-avail">Not Available</span>')+'</td><td class="ox-num">'+c[6]+' days</td><td>'+c[5]+'</td><td class="ox-num">'+inr(cst*qn)+'</td></tr>';
        if(c[8]&&st.fold){B.motor.forEach(function(s){var n2=s[2]*need;rows+='<tr class="is-kid"><td class="mf-bo-2">['+s[0]+'] '+s[1]+'</td><td class="ox-num">'+num(n2,2)+' '+s[3]+'</td><td class="ox-num">'+num(s[4],2)+'</td><td>'+(s[4]>=n2?'<span class="mf-avail is-ok">Available</span>':'<span class="mf-avail">Not Available</span>')+'</td><td class="ox-num">'+s[6]+' days</td><td>Buy</td><td class="ox-num">'+inr(s[2]*s[7]*need)+'</td></tr>';});
          R.motor.forEach(function(o){var mins=o[2]*need;rows+='<tr class="is-kid is-op"><td class="mf-bo-2">'+o[0]+' &middot; '+WCK[o[1]].n+'</td><td class="ox-num">'+hm(mins)+'</td><td></td><td></td><td></td><td>Operation</td><td class="ox-num">'+inr(mins/60*WCK[o[1]].cost)+'</td></tr>';});}});
      rows+='<tr class="is-sec"><td colspan="7">Operations</td></tr>';
      R.fan.forEach(function(o){var mins=o[2]*qn,c=mins/60*WCK[o[1]].cost;tot+=c;rows+='<tr class="is-op"><td class="mf-bo-1">'+o[0]+' &middot; '+WCK[o[1]].n+'</td><td class="ox-num">'+hm(mins)+'</td><td></td><td></td><td></td><td>'+WCK[o[1]].code+'</td><td class="ox-num">'+inr(c)+'</td></tr>';});
      return '<div class="mf-bo"><div class="mf-bo-top"><div><p class="mf-f-k">BoM Overview</p><h3>[FAN-A48] Aero 48 Ceiling Fan 1200mm</h3></div>'+
        '<label class="mf-bo-q">Quantity <input type="number" min="1" max="5000" value="'+qn+'" data-bq aria-label="Quantity to produce"> Units</label></div>'+
        '<div class="mf-bo-sum"><span><small>Ready to produce</small><b class="'+(ready>=qn?'mf-grn':'mf-red')+'">'+num(ready)+' Units</b></span><span><small>Lead time</small><b>'+(lead+3)+' days</b></span><span><small>BoM cost</small><b>'+inr(tot)+'</b></span><span><small>Cost per unit</small><b>'+inr(tot/qn)+'</b></span></div>'+
        '<div class="ox-scroll"><table class="mf-lines mf-bo-t"><thead><tr><th>Product</th><th class="ox-num">Quantity</th><th class="ox-num">Free to Use</th><th>Availability</th><th class="ox-num">Lead Time</th><th>Route</th><th class="ox-num">BoM Cost</th></tr></thead><tbody>'+rows+
        '</tbody><tfoot><tr><td colspan="6">Total for '+num(qn)+' Units</td><td class="ox-num"><b>'+inr(tot)+'</b></td></tr></tfoot></table></div>'+
        (ready<qn?'<p class="mf-bo-note">Only '+num(ready)+' can be built today: <b>Capacitor 2.5&micro;F</b> limits the order. A reordering rule would raise a purchase for the rest.</p>':'')+'</div>';}
    function plan(){var days=['Mon 19','Tue 20','Wed 21','Thu 22','Fri 23','Mon 26','Tue 27','Wed 28','Thu 29','Fri 30'],n=days.length,today=2;
      return '<div class="ox-scroll"><div class="mf-pg" style="--n:'+n+'"><div class="mf-pg-row is-head"><span class="mf-pg-l">Work Center</span><span class="mf-pg-d">'+days.map(function(d,i){return '<span class="'+(i===today?'is-today':'')+'">'+d+'</span>';}).join('')+'</span></div>'+
        WC.map(function(w){var bars=PL.filter(function(p){return p[0]===w.k;}).map(function(p){return '<span class="mf-pg-bar is-'+p[5]+'" style="--s:'+p[3]+';--l:'+p[4]+'" title="'+p[1]+' - '+p[2]+'"><b>'+p[1].replace('WH/MO/','MO ')+'</b> '+p[2]+'</span>';}).join('');
          var load=PL.filter(function(p){return p[0]===w.k;}).reduce(function(a,p){return a+p[4];},0);
          return '<div class="mf-pg-row"><span class="mf-pg-l"><b>'+w.n+'</b><small>'+Math.round(load/n*100)+'% load</small></span><span class="mf-pg-t"><i class="mf-pg-today" style="--s:'+today+'"></i>'+bars+'</span></div>';}).join('')+'</div></div>'+
        '<p class="mf-pg-leg"><span><i class="is-done"></i>Finished</span><span><i class="is-progress"></i>In Progress</span><span><i class="is-ready"></i>Ready</span><span><i class="is-wait"></i>Waiting</span></p>';}
    function render(){var label;
      if(st.mo){var m=M.filter(function(x){return x.id===st.mo;})[0];crumb.innerHTML='<a href="#" data-back>Manufacturing Orders</a><span>'+m.ref+'</span>';body.innerHTML=moForm(m);return;}
      if(st.wc){var w=WCK[st.wc];crumb.innerHTML='<a href="#" data-back>Work Centers</a><span>'+w.n+'</span>';body.innerHTML=wcForm(w);return;}
      label={wc:'Work Centers',mo:'Manufacturing Orders',bom:'Bills of Materials',plan:'Planning by Work Center'}[st.menu];
      crumb.innerHTML=st.menu==='bom'?'<a>Bills of Materials</a><span>BoM Overview</span>':'<span>'+label+'</span>';
      body.innerHTML={wc:wcKanban,mo:moList,bom:bomView,plan:plan}[st.menu]();}
    function find(id){return M.filter(function(x){return x.id===id;})[0];}
    menus.forEach(function(b){b.addEventListener('click',function(){setMenu(b.getAttribute('data-mx-menu'));});});
    mx.querySelector('[data-mx-new]').addEventListener('click',function(){setMenu('mo');});
    q.addEventListener('input',function(){if(st.menu!=='wc'&&st.menu!=='mo')setMenu('mo');st.mo=null;st.wc=null;render();});
    mx.addEventListener('click',function(e){
      if(e.target.closest('[data-back]')){e.preventDefault();st.mo=null;st.wc=null;render();return;}
      var t=e.target.closest('[data-tab]');if(t){st.tab=t.getAttribute('data-tab');render();return;}
      var f=e.target.closest('[data-fold]');if(f){st.fold=!st.fold;render();return;}
      var m=st.mo&&find(st.mo),d=e.target.closest('[data-do]');
      if(d){var a=d.getAttribute('data-do');
        if(a==='block'&&st.wc){var w=WCK[st.wc];w.blocked=!w.blocked;render();return;}
        if(a==='bom'){setMenu('bom');return;}
        if(m){if(a==='confirm'){m.st='open';m.log.push({w:'Meera Iyer',t:'Order confirmed; components to reserve: '+P[m.p].comp.length});}
          if(a==='avail'){m.comp='ok';m.log.push({w:'Unisas Bot',t:'Components reserved after receipt WH/IN/00061'});}
          if(a==='produce'){m.wo=m.wo.map(function(){return 'done';});m.st='done';m.comp='ok';m.log.push({w:'Meera Iyer',t:'<b>'+num(m.qty)+'</b> units produced; stock and valuation updated'});}
          refresh(m);render();}return;}
      var wb=e.target.closest('[data-wo]');
      if(wb&&m){var j=+wb.getAttribute('data-wo'),to=wb.getAttribute('data-to'),o=ops(m)[j];
        if(to==='progress'&&WCK[o[1]].blocked){m.log.push({w:'Unisas Bot',t:WCK[o[1]].n+' is blocked; unblock it in Work Centers first'});render();return;}
        m.wo[j]=to;m.log.push({w:m.resp,t:o[0]+' '+(to==='done'?'<b>finished</b>':'started')+' on '+WCK[o[1]].n});
        if(to==='done'&&j+1<m.wo.length&&m.wo[j+1]==='wait')m.wo[j+1]='ready';render();return;}
      var r=e.target.closest('[data-mo]');if(r){st.mo=+r.getAttribute('data-mo');st.tab='wo';render();return;}
      var c=e.target.closest('[data-wc]');if(c){st.wc=c.getAttribute('data-wc');render();}
    });
    mx.addEventListener('keydown',function(e){if(e.key!=='Enter')return;var r=e.target.closest&&e.target.closest('[data-mo],[data-wc],[data-fold]');if(r){e.preventDefault();r.click();}});
    mx.addEventListener('change',function(e){if(e.target.matches('[data-bq]')){var v=Math.max(1,Math.min(5000,parseInt(e.target.value,10)||1));st.bq=v;render();var i=body.querySelector('[data-bq]');if(i)i.focus();}});
    render();}

  /* --- 4 settings --- */
  var cf=document.querySelector('[data-cfg]');
  if(cf){function cfd(){var on={};cf.querySelectorAll('[data-set]').forEach(function(i){on[i.getAttribute('data-set')]=i.checked;});
      var steps=cf.querySelector('input[name="mf-steps"]:checked').value,R2=[];
      if(on.mps)R2.push(['plan','Master Production Schedule','Weekly demand forecast creates the order']);
      else R2.push(['plan','Sales order or reordering rule','Triggers the manufacturing order']);
      if(on.sub)R2.push(['sub','Resupply Subcontractor','Components for plating sent to the job worker, then received back']);
      if(steps!=='1')R2.push(['pick','Pick Components','WH/PC: stock to WH/Pre-Production']);
      R2.push(['mo','Manufacturing Order','WH/MO: components consumed, finished goods produced'+(on.lot?', lot FAN-2610-0042':'')]);
      if(on.wo)R2.push(['wo','Work Orders','Blade pressing, Final assembly, Powder coating, Run test &amp; pack'+(on.qc?' &middot; quality checks at 2 steps':'')]);
      else if(on.qc)R2.push(['wo','Quality check','One check on the order before it is closed']);
      if(on.byp)R2.push(['byp','By-product','Aluminium offcuts, 0.08 kg per fan, back to stock']);
      if(steps==='3')R2.push(['store','Store Finished Product','WH/SFP: WH/Post-Production to stock']);
      R2.push(['stock','WH/Stock','Ready to deliver'+(on.lot?' by lot':'')]);
      cf.querySelector('[data-cfg-route]').innerHTML=R2.map(function(r,i){return '<li class="mf-r-'+r[0]+'" style="--i:'+i+'"><b>'+r[1]+'</b><small>'+r[2]+'</small></li>';}).join('');
      var docs=R2.filter(function(r){return /pick|mo|store|sub/.test(r[0]);}).length;
      cf.querySelector('[data-cfg-count]').textContent=docs+' document'+(docs>1?'s':'')+' per order';
      cf.querySelector('[data-cfg-note]').innerHTML=steps==='1'?'<b>1 step</b> suits a small plant where stores and production share the same floor.':(steps==='2'?'<b>2 steps</b> suits plants with a separate store: components are picked to the line before work starts.':'<b>3 steps</b> adds a check-in of finished goods, useful when a separate team inspects or packs them.');}
    cf.addEventListener('change',cfd);cfd();}

  /* --- 5 connected apps --- */
  var cx=document.querySelector('[data-cx]');
  if(cx){var step=0,fail=false;
    var B5=function(k){return cx.querySelector('[data-cx-b="'+k+'"]');};
    function row(a,b,c){return '<p class="mf-cx-r"><span>'+a+'</span><b class="'+(c||'')+'">'+b+'</b></p>';}
    var LOG=[];
    function cxd(){var acts='',title;
      cx.querySelectorAll('[data-cx-app]').forEach(function(a){a.classList.remove('is-hot','is-ok');});
      function hot(k,ok){cx.querySelector('[data-cx-app="'+k+'"]').classList.add(ok?'is-ok':'is-hot');}
      if(step===0){title='Step 1 of 4: a sales order for 400 fans arrives';acts='<button type="button" class="ox-pbtn" data-cx="1">Confirm S00238 &middot; 400 &times; Aero 48</button>';
        B5('mrp').innerHTML=row('Open orders','3')+row('Aero 48 free stock','85 Units');B5('inv').innerHTML=row('Capacitor 2.5&micro;F on hand','140 Units')+row('Reorder rule','Min 200 &middot; Max 600');
        B5('pur').innerHTML='<p class="mf-cx-idle">No open RFQ for capacitors.</p>';B5('qc').innerHTML='<p class="mf-cx-idle">Incoming inspection set on capacitors.</p>';}
      if(step>=1){B5('mrp').innerHTML='<p class="mf-cx-doc mono">WH/MO/00046</p>'+row('To produce','400 Units')+row('Component Status',step>=4&&!fail?'Available':'Not Available',step>=4&&!fail?'mf-grn':'mf-red');hot('mrp',step>=4&&!fail);}
      if(step>=1){B5('inv').innerHTML='<p class="mf-cx-doc mono">Replenishment</p>'+row('Capacitor 2.5&micro;F on hand',step>=4&&!fail?'1,000 Units':'140 Units')+row('Forecast',step>=4&&!fail?'600 Units':'-260 Units',step>=4&&!fail?'mf-grn':'mf-red')+row('To Order',step>=2?'0 Units':'860 Units');if(step===1)hot('inv');else if(step>=4&&!fail)hot('inv',1);}
      if(step===1){title='Step 2 of 4: Inventory finds a shortage';acts='<button type="button" class="ox-pbtn" data-cx="2">Order Once</button>';}
      if(step>=2){B5('pur').innerHTML='<p class="mf-cx-doc mono">P00093</p>'+row('Vendor','Sri Ram Electricals')+row('Capacitor 2.5&micro;F','860 &times; &#8377; 38.00')+row('Status',step>=3?'Purchase Order':'RFQ',step>=3?'mf-grn':'');hot('pur',step>=3);}
      if(step===2){title='Step 3 of 4: Purchase confirms the order';acts='<button type="button" class="ox-pbtn" data-cx="3">Confirm Order</button>';}
      if(step>=3){B5('qc').innerHTML='<p class="mf-cx-doc mono">WH/IN/00061 &middot; QC/00402</p>'+row('Check','Capacitance 2.5&micro;F &plusmn; 5%')+row('Sample','13 of 860')+row('Result',step>=4?(fail?'Fail: QA/0012':'Pass'):'To Do',step>=4?(fail?'mf-red':'mf-grn'):'');if(step>=4)hot('qc',!fail);else hot('qc');}
      if(step===3){title='Step 4 of 4: the goods arrive and Quality inspects them';acts='<button type="button" class="ox-pbtn" data-cx="pass">Pass</button><button type="button" class="ox-sbtn mf-fail" data-cx="fail">Fail</button>';}
      if(step>=4){title=fail?'Quality alert raised: the batch goes back to the vendor':'Done: the manufacturing order is ready to start';acts=fail?'<button type="button" class="ox-pbtn" data-cx="redo">Vendor replaces the batch</button>':'';}
      cx.querySelector('[data-cx-step]').innerHTML=title;cx.querySelector('[data-cx-acts]').innerHTML=acts;
      cx.querySelector('[data-cx-log]').innerHTML=LOG.map(function(l,i){return '<li style="--c:'+l[0]+'"'+(i===LOG.length-1?' class="is-new"':'')+'><b>'+l[1]+'</b>'+l[2]+'</li>';}).join('');}
    cx.addEventListener('click',function(e){var b=e.target.closest('[data-cx]');
      if(e.target.closest('[data-cx-reset]')){step=0;fail=false;LOG=[];cxd();return;}
      if(!b)return;var a=b.getAttribute('data-cx');
      if(a==='1'){step=1;LOG.push(['#EE8A3C','Sales','S00238 confirmed; Replenish on Order created WH/MO/00046']);LOG.push(['#1F8A78','Inventory','Capacitor 2.5µF forecast drops to -260']);}
      if(a==='2'){step=2;LOG.push(['#1F8A78','Inventory','Order Once: RFQ P00093 for 860 capacitors']);}
      if(a==='3'){step=3;LOG.push(['#3E7CB1','Purchase','P00093 confirmed; receipt WH/IN/00061 expected Oct 24']);}
      if(a==='pass'){step=4;fail=false;LOG.push(['#B5567E','Quality','Incoming inspection passed; receipt validated']);LOG.push(['#0E7C86','Manufacturing','WH/MO/00046 components reserved: ready to start']);}
      if(a==='fail'){step=4;fail=true;LOG.push(['#B5567E','Quality','Check failed; quality alert QA/0012 and return to vendor']);}
      if(a==='redo'){step=3;fail=false;LOG.push(['#3E7CB1','Purchase','Replacement batch received for P00093']);}
      cxd();});
    cxd();}

  /* --- 6 sort --- */
  var so=document.querySelector('[data-sort]');
  if(so){var RQ=J('mf-reqs'),why=so.querySelector('[data-sort-why]'),LN={cfg:'Configure',custom:'Customize',int:'Integrate'};
    function place(i,quiet){var b=so.querySelector('[data-req="'+i+'"]');if(!b||b.closest('[data-lane]'))return;
      var li=b.parentNode;so.querySelector('[data-lane="'+RQ[i][1]+'"]').appendChild(li);b.classList.add('is-placed');
      so.querySelectorAll('.mf-req.is-on').forEach(function(x){x.classList.remove('is-on');});b.classList.add('is-on');
      if(!quiet)why.innerHTML='<span class="mf-tagk mf-tagk--'+RQ[i][1]+'">'+LN[RQ[i][1]]+'</span> <b>'+RQ[i][0]+'</b>: '+RQ[i][2];}
    so.addEventListener('click',function(e){var b=e.target.closest('[data-req]');
      if(b){var i=+b.getAttribute('data-req');if(b.closest('[data-lane]')){so.querySelectorAll('.mf-req.is-on').forEach(function(x){x.classList.remove('is-on');});b.classList.add('is-on');why.innerHTML='<span class="mf-tagk mf-tagk--'+RQ[i][1]+'">'+LN[RQ[i][1]]+'</span> <b>'+RQ[i][0]+'</b>: '+RQ[i][2];}else place(i);return;}
      if(e.target.closest('[data-sort-all]')){RQ.forEach(function(r,i){place(i,true);});why.innerHTML='Seven of nine land in <b>Configure</b> or <b>Integrate</b> with no custom code. That is typical for our manufacturing projects.';return;}
      if(e.target.closest('[data-sort-reset]')){var pile=so.querySelector('[data-pile]');RQ.forEach(function(r,i){var b=so.querySelector('[data-req="'+i+'"]');b.classList.remove('is-placed','is-on');pile.appendChild(b.parentNode);});why.textContent='Choose a requirement on the left.';}
    });}

  /* --- 7 production models --- */
  var md=document.querySelector('[data-models]');
  if(md){var MD=J('mf-models'),mt=[].slice.call(md.querySelectorAll('[data-model]'));
    function mdd(i){var m=MD[i];mt.forEach(function(t,j){var on=j===i;t.classList.toggle('is-on',on);t.setAttribute('aria-selected',on);t.tabIndex=on?0:-1;});
      md.querySelector('[data-m-for]').innerHTML='TYPICAL FOR: '+m[2].toUpperCase();md.querySelector('[data-m-name]').innerHTML=m[1];md.querySelector('[data-m-text]').innerHTML=m[3];
      md.querySelector('[data-m-flow]').innerHTML=m[5].map(function(s){return '<li>'+s+'</li>';}).join('');
      md.querySelector('[data-m-dl]').innerHTML=Object.keys(m[4]).map(function(k){return '<div><dt>'+k+'</dt><dd>'+m[4][k]+'</dd></div>';}).join('');
      md.querySelectorAll('[data-bt]').forEach(function(b){b.classList.toggle('is-on',m[4]['BoM type'].indexOf(b.getAttribute('data-bt'))===0||(b.getAttribute('data-bt')==='Manufacture this product'&&/^BoM per/.test(m[4]['BoM type'])));});}
    mt.forEach(function(t,i){t.addEventListener('click',function(){mdd(i);});t.addEventListener('keydown',function(e){var d={ArrowRight:1,ArrowDown:1,ArrowLeft:-1,ArrowUp:-1}[e.key];if(d){e.preventDefault();var k=(i+d+mt.length)%mt.length;mdd(k);mt[k].focus();}});});mdd(0);}

  /* --- 8 import --- */
  var im=document.querySelector('[data-imp]');
  if(im){var msg=im.querySelector('[data-imp-msg]'),go=im.querySelector('[data-imp-go]'),fix=im.querySelector('[data-imp-fix]'),fixed=false;
    function show(){msg.className='mf-imp-msg';msg.innerHTML='<p>Click <b>Test</b> to check the file before anything is imported.</p>';}
    im.querySelector('[data-imp-test]').addEventListener('click',function(){
      if(!fixed){msg.className='mf-imp-msg is-err';msg.innerHTML='<p><b>The file has 3 errors.</b> Nothing was imported.</p><ul><li>Row 14: No matching record found for name ‘CAP-2.5UF’ in field ‘Component’</li><li>Row 22: Value ‘Nos’ not found in selection field ‘Product Unit of Measure’</li><li>Row 31: No matching record found for name ‘Paint Booth’ in field ‘Work Center’</li></ul>';fix.hidden=false;go.disabled=true;}
      else{msg.className='mf-imp-msg is-ok';msg.innerHTML='<p><b>Everything seems valid.</b> 62 rows ready: 3 BoMs, 47 lines, 12 operations.</p>';go.disabled=false;go.className='ox-pbtn';}});
    fix.addEventListener('click',function(){fixed=true;fix.hidden=true;msg.className='mf-imp-msg';msg.innerHTML='<p>Cleansing rules applied: <b>CAP-2.5UF &rarr; CAP-25</b>, <b>Nos &rarr; Units</b>, <b>Paint Booth &rarr; Paint Shop</b>. Test again.</p>';
      im.querySelectorAll('.mf-imp-t tbody tr').forEach(function(tr,i){if(i===1||i===3||i===5)tr.classList.add('is-fixed');});});
    go.addEventListener('click',function(){msg.className='mf-imp-msg is-ok';msg.innerHTML='<p><b>62 records successfully imported.</b> BoMs for Aero 48, Breeze 36 and Turbo 40 are live in Bills of Materials.</p>';go.disabled=true;go.className='ox-sbtn';});
    show();}

  /* --- 9 reports --- */
  var vs=document.querySelector('[data-vis]');
  if(vs){var TR=J('mf-trace'),CO=J('mf-cost'),OE=J('mf-oee'),vb=vs.querySelector('[data-vis-body]'),vt=[].slice.call(vs.querySelectorAll('[data-vt]')),closed={},per=false,oi=4;
    function trace(){var hide=-1,rows='';
      TR.forEach(function(r,i){if(hide>-1&&r[0]>hide)return;hide=-1;var kids=TR[i+1]&&TR[i+1][0]>r[0];if(kids&&closed[i])hide=r[0];
        rows+='<tr class="'+(r[3]==='CW-118'?'is-hit':'')+'"'+(kids?' data-tr="'+i+'" tabindex="0"':'')+'><td style="padding-left:'+(14+r[0]*18)+'px">'+(kids?'<span class="mf-caret">'+(closed[i]?'&#9656;':'&#9662;')+'</span>':'<span class="mf-caret"></span>')+'<b>'+r[1]+'</b></td><td>'+r[2]+'</td><td><span class="mf-lot">'+r[3]+'</span></td><td>'+r[4]+'</td><td class="ox-muted">'+r[5]+'</td><td class="ox-muted">'+r[6]+'</td><td class="ox-num">'+r[7]+'</td></tr>';});
      return '<div class="mf-vis-bar"><span class="ox-crumb">Traceability Report</span><span class="ox-facet">Lot/Serial: FAN-2610-0042</span></div><div class="ox-scroll"><table class="ox-table mf-tr-t"><thead><tr><th>Reference</th><th>Product</th><th>Lot/Serial</th><th>Date</th><th>From</th><th>To</th><th class="ox-num">Quantity</th></tr></thead><tbody>'+rows+'</tbody></table></div>'+
        '<p class="mf-recall"><b>Supplier recall on copper lot CW-118?</b> Run the report downstream from the lot: 250 motors, 250 fans in lot FAN-2610-0042, one customer to contact. Minutes, not days.</p>';}
    function cost(){var C=CO.rows,body='',ex=0,re=0,q=250,sec='';
      C.forEach(function(r,i){var e,a;if(r[0]==='Components'){e=r[2]*r[3];a=r[2]?r[2]*r[4]:q*r[4];}else{var k=i-6;e=r[2]/60*r[3];a=CO.real[k]/60*r[4];}
        ex+=e;re+=a;if(r[0]!==sec){sec=r[0];body+='<tr class="is-sec"><td colspan="5">'+sec+'</td></tr>';}
        var dv=per?1/q:1,v=a-e;
        body+='<tr><td>'+r[1]+'</td><td class="ox-num">'+(r[0]==='Operations'?hm(r[2])+' &rarr; '+hm(CO.real[i-6]):(r[2]?num(r[2],2):''))+'</td><td class="ox-num">'+inr(e*dv)+'</td><td class="ox-num">'+inr(a*dv)+'</td><td class="ox-num '+(v>0.5?'mf-red':(v<-0.5?'mf-grn':'ox-muted'))+'">'+(Math.abs(v)<0.5?'&ndash;':(v>0?'+':'')+inr(v*dv))+'</td></tr>';});
      var dv=per?1/q:1;
      return '<div class="mf-vis-bar"><span class="ox-crumb">Cost Analysis &middot; WH/MO/00042</span><span class="mf-seg" role="group" aria-label="Show"><button type="button" data-per="0" class="'+(per?'':'is-on')+'" aria-pressed="'+!per+'">Total</button><button type="button" data-per="1" class="'+(per?'is-on':'')+'" aria-pressed="'+per+'">Per unit</button></span></div>'+
        '<div class="ox-scroll"><table class="ox-table mf-co-t"><thead><tr><th>Cost</th><th class="ox-num">Quantity / Time</th><th class="ox-num">Expected</th><th class="ox-num">Real</th><th class="ox-num">Variance</th></tr></thead><tbody>'+body+'</tbody>'+
        '<tfoot><tr><td><b>Total cost'+(per?' per unit':'')+'</b></td><td></td><td class="ox-num"><b>'+inr(ex*dv)+'</b></td><td class="ox-num"><b>'+inr(re*dv)+'</b></td><td class="ox-num mf-red"><b>+'+inr((re-ex)*dv)+'</b></td></tr></tfoot></table></div>'+
        '<p class="mf-recall"><b>Where the '+inr(re-ex,false)+' went:</b> final assembly ran 11% over its standard time and the motor sub-order used more copper than its BoM. Both show up the day the order closes.</p>';}
    function oee(){var o=OE[oi];
      return '<div class="mf-vis-bar"><span class="ox-crumb">Overall Equipment Effectiveness &middot; Last 30 days</span><span class="ox-facet">Target 90%</span></div><div class="mf-oee"><ul class="mf-oee-l">'+
        OE.map(function(w,i){return '<li><button type="button" data-oee="'+i+'" class="'+(i===oi?'is-on':'')+'" aria-pressed="'+(i===oi)+'"><span>'+w[0]+'</span><span class="mf-oee-bar"><i style="--w:'+w[2]+'" class="'+(w[2]<75?'is-low':(w[2]>=90?'is-hi':''))+'"></i><em></em></span><b>'+num(w[2],1)+'%</b></button></li>';}).join('')+'</ul>'+
        '<div class="mf-oee-d"><p class="mf-f-k">'+o[1]+'</p><h4>'+o[0]+'</h4><div class="mf-apq"><span><small>Availability</small><b>'+o[3]+'%</b></span><i>&times;</i><span><small>Performance</small><b>'+o[4]+'%</b></span><i>&times;</i><span><small>Quality</small><b>'+o[5]+'%</b></span><i>=</i><span class="is-oee"><small>OEE</small><b>'+num(o[2],1)+'%</b></span></div>'+
        '<p class="mf-gi-h">Losses (hours)</p><ul class="mf-loss">'+o[6].map(function(l){return '<li><span>'+l[0]+'</span><i style="--w:'+(l[1]/12*100)+'"></i><b>'+num(l[1],1)+'</b></li>';}).join('')+'</ul></div></div>';}
    function vd(){var k=vs.querySelector('[data-vt].is-on').getAttribute('data-vt');vb.innerHTML={trace:trace,cost:cost,oee:oee}[k]();}
    vt.forEach(function(b){b.addEventListener('click',function(){press(vt,b);vd();});});
    vs.addEventListener('click',function(e){var t=e.target.closest('[data-tr]');if(t){var i=+t.getAttribute('data-tr');closed[i]=!closed[i];vd();return;}
      var p=e.target.closest('[data-per]');if(p){per=p.getAttribute('data-per')==='1';vd();return;}
      var o=e.target.closest('[data-oee]');if(o){oi=+o.getAttribute('data-oee');vd();}});
    vs.addEventListener('keydown',function(e){if(e.key==='Enter'){var t=e.target.closest&&e.target.closest('[data-tr]');if(t){e.preventDefault();t.click();}}});
    vd();}

  /* --- 10 test cycles --- */
  var ts=document.querySelector('[data-test]');
  if(ts){var T=J('mf-tests'),cyc=1,res=T.map(function(){return '';}),busy=false,runBtn=ts.querySelector('[data-test-run]');
    var roles=T.map(function(t){return t[0];}).filter(function(r,i,a){return a.indexOf(r)===i;});
    function td(){ts.querySelector('[data-test-rows]').innerHTML=T.map(function(t,i){var r=res[i],l=r==='pass'?'<span class="mf-b mf-b--dn">Passed</span>':(r==='fail'?'<span class="mf-b mf-b--fl">Failed</span>':(r==='run'?'<span class="mf-b mf-b--ip">Running&hellip;</span>':'<span class="mf-b mf-b--dr">Not run</span>'));
        return '<tr class="is-'+(r||'idle')+'"><td>'+t[0]+'</td><td>'+t[1]+(r==='fail'||(cyc===2&&t[3]&&r==='pass')?'<small class="mf-t-note">'+(r==='fail'?'Issue: ':'Fixed: ')+t[3]+'</small>':'')+'</td><td>'+l+'</td></tr>';}).join('');
      var p=res.filter(function(r){return r==='pass';}).length,f=res.filter(function(r){return r==='fail';}).length;
      ts.querySelector('[data-test-cycle]').textContent='Test cycle '+cyc;
      ts.querySelector('[data-test-sum]').textContent=p+f?p+' passed, '+f+' failed':'Not run yet';
      ts.querySelector('[data-test-sign]').innerHTML=roles.map(function(r){var mine=T.map(function(t,i){return t[0]===r?res[i]:null;}).filter(function(x){return x!==null;});
        var ok=mine.every(function(x){return x==='pass';});return '<li class="'+(ok?'is-ok':'')+'"><span class="mf-sign-ic">'+(ok?'&#10003;':'')+'</span>'+r+'</li>';}).join('');
      var all=p===T.length;ts.querySelector('.mf-sign').classList.toggle('is-ready',all);
      ts.querySelector('[data-test-res]').innerHTML=all?'<b>Ready for go-live.</b> Every role has signed off its scenarios.':(f?'Two issues found. Fix them and run cycle 2.':'Run the cycle to test with real data.');}
    runBtn.addEventListener('click',function(){if(busy)return;if(res.every(function(r){return r==='pass';})){cyc=1;res=T.map(function(){return '';});td();runBtn.textContent='Run test cycle';return;}
      busy=true;runBtn.disabled=true;var second=res.some(function(r){return r==='fail';});if(second)cyc=2;res=T.map(function(){return '';});
      var i=0;(function next(){if(i>0)res[i-1]=second?'pass':T[i-1][2];if(i>=T.length){busy=false;runBtn.disabled=false;runBtn.textContent=res.every(function(r){return r==='pass';})?'Start over':'Fix issues and run cycle 2';td();return;}
        res[i]='run';td();i++;setTimeout(next,260);})();});
    td();}

  /* --- 11 package --- */
  var pk=document.querySelector('[data-pk]');
  if(pk){var box=pk.closest('.mf-pkg');pk.addEventListener('change',function(){var w=0,n=[];pk.querySelectorAll('input:checked').forEach(function(i){w+=+i.getAttribute('data-add');n.push(i.closest('label').querySelector('b').innerHTML);});
      box.querySelector('[data-pk-sum]').innerHTML=(n.length?'Core + '+n.length+' app'+(n.length>1?'s':''):'Core scope')+' &middot; '+(10+Math.ceil(w*0.8))+' to '+(12+w)+' weeks';
      box.querySelector('[data-pk-apps]').innerHTML=['Manufacturing','Inventory','Purchase','Accounting'].concat(n).join(' &middot; ');});}

  /* --- 12 helpdesk --- */
  var tkb=document.querySelector('[data-tk-det]');
  if(tkb){var TK=J('mf-tickets'),tks=[].slice.call(document.querySelectorAll('[data-tk]'));
    tks.forEach(function(b){b.addEventListener('click',function(){tks.forEach(function(x){x.classList.toggle('is-on',x===b);});var t=TK[+b.getAttribute('data-tk')];
      tkb.innerHTML='<p class="mf-f-k">'+t[2]+' &middot; '+t[3]+' priority</p><h4>'+t[1]+'</h4><p>'+t[6]+'</p>';});});}

  /* --- 13 planner --- */
  var pn=document.querySelector('[data-planner]');
  if(pn){var plants=1;
    function pd(){var model=+pn.querySelector('[data-pl="model"]').value,boms=+pn.querySelector('[data-pl="boms"]').value,wcs=+pn.querySelector('[data-pl="wcs"]').value,x=0;
      pn.querySelectorAll('[data-pl-x]:checked').forEach(function(c){x+=+c.getAttribute('data-pl-x');});
      pn.querySelector('[data-pl-out="boms"]').textContent=num(boms);pn.querySelector('[data-pl-out="wcs"]').textContent=wcs;
      var ph=[['Discover &amp; design',2+(model===3?1:0)+(plants>1?1:0)],['Configure',2+Math.round(wcs/12)+(model>=2?1:0)],['Data migration',1+Math.round(boms/600)],
              ['Integrations',x?Math.ceil(x/1.5):0],['Test cycles',2+(plants>2?1:0)],['Go live &amp; hypercare',2+(plants-1)]].filter(function(p){return p[1]>0;});
      var start=0,total=0;ph.forEach(function(p,i){p.s=start;start+=Math.max(1,p[1]-(i>1&&i<ph.length-1?1:0));});total=ph.reduce(function(a,p){return Math.max(a,p.s+p[1]);},0);
      pn.querySelector('[data-pl-bars]').innerHTML=ph.map(function(p){return '<li><span>'+p[0]+'</span><span class="mf-pl-tr"><i style="--s:'+(p.s/total*100)+';--l:'+(p[1]/total*100)+'"></i></span><b>'+p[1]+' wk</b></li>';}).join('');
      pn.querySelector('[data-pl-tot]').innerHTML='About <b>'+total+' weeks</b> to go live'+(plants>1?' with the first plant, then 4 to 6 weeks for each further plant':'')+'.';}
    pn.addEventListener('input',pd);pn.addEventListener('change',pd);
    pn.querySelectorAll('[data-plants]').forEach(function(b,i,all){b.addEventListener('click',function(){plants=+b.getAttribute('data-plants');press([].slice.call(all),b);pd();});});pd();}
})();
</script>
'''

CTA = ("Let's Map Your Production Process to Odoo",
       "Tell us how your factory runs today: your products, work centres and the systems you use. We'll walk your production flow in Odoo Manufacturing "
       "and recommend the right setup, scope and timeline.")
