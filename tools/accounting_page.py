"""
Odoo Accounting page (odoo-accounting.html). Every screen is modelled on the real Odoo 20
Accounting app (demo.odoo.com/odoo/accounting): the journal dashboard, customer invoices and
vendor bills (Draft / Posted, Not Paid / In Payment / Partially Paid / Paid), Register Payment,
journal items, bank reconciliation with reconciliation models, the Profit and Loss, Balance
Sheet, Aged Receivable and Tax Report layouts, lock dates and fiscal localization.
Sample company: Chennai (Tamil Nadu), so intra-state sales carry 18% GST (9% CGST + 9% SGST)
and inter-state sales 18% IGST. Shared Odoo look: odoo-ui.css. Page styles: accounting.css.

hero(g) and build(g) get the build script's globals.
"""
import json

from crm_explorer import ic, SEARCH, V_KANBAN, V_LIST

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CROSS = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
BANK = ic('<path d="M3 10l9-6 9 6M5 10v8M9.5 10v8M14.5 10v8M19 10v8M3 20h18"/>', 18, 1.7)
MENUS = ["Dashboard", "Customers", "Vendors", "Accounting", "Review", "Reporting", "Configuration"]


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
    return ('<div class="ac-head%s"><p class="ac-eyebrow mono">%s</p><h2 class="ac-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="ac-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="ac-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


def odoo_nav(app_icon, menus=MENUS):
    return ('<div class="ox-nav"><span class="ox-app">%s<b>Accounting</b></span>%s<span class="ox-nav-r"><span class="ox-company">Your Company</span>'
            '<span class="ox-av" style="--c:#C98600">D</span></span></div>' % (app_icon, "".join('<span class="ox-menu">%s</span>' % m for m in menus)))


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">Accounting</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["GST-ready invoicing &amp; bills", "Bank reconciliation in minutes", "Reports that are always current"])
    copy = ('<div class="ac-hero-copy">%s<p class="ac-eyebrow mono">ODOO ACCOUNTING IMPLEMENTATION</p>'
            '<h1 class="ac-h1">Best Accounting Software Implementation <span>for Your Business with Odoo</span></h1>'
            '<p class="ac-lead">Unisas sets up Odoo Accounting so invoices, bills, payments, GST and bank reconciliation run in one system, current every day.</p>'
            '<ul class="ac-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Discuss Odoo Accounting %s</a>'
            '<a href="#explore" class="btn btn-ghost">Try the accounting demo</a></div></div>' % (crumb, points, g["ARROW"]))
    # bank statement lines on the left, the Odoo entries they reconcile with on the right
    left = [("Oct 12", "NEFT-BLUEBAY RETAIL PVT LTD", 726408), ("Oct 12", "UPI/KAVERI FOODS/412233", 118000), ("Oct 13", "NEFT-KAVERI STEEL WORKS", -253464),
            ("Oct 13", "CHRG/SMS ALERT Q3", -118), ("Oct 14", "RTGS-SHREE DISTRIBUTORS", 300000)]
    right = [("BILL/2026/10/0007", "Kaveri Steel Works", "Paid", "ok"), ("INV/2026/00412", "Bluebay Retail", "Paid", "ok"),
             ("INV/2026/00398", "Shree Distributors", "Partially Paid", "part"), ("INV/2026/00407", "Kaveri Foods", "Paid", "ok"), ("Bank Fees", "Reconciliation model", "Rule", "rule")]
    pairs = [(0, 1), (1, 3), (2, 0), (3, 4), (4, 2)]
    lrows = "".join('<li><small>%s</small><b>%s</b><em class="%s">%s</em></li>' % (d, l, "is-out" if a < 0 else "", inr(a)) for d, l, a in left)
    rrows = "".join('<li class="is-%s"><b>%s</b><small>%s</small><span>%s</span></li>' % (k, n, p, s) for n, p, s, k in right)
    H = 64
    paths = "".join('<path class="%s" style="--i:%d" d="M0 %d C 40 %d, 60 %d, 100 %d"/>' % ("is-rule" if b == 4 else "", i, a * H + H // 2, a * H + H // 2, b * H + H // 2, b * H + H // 2)
                    for i, (a, b) in enumerate(pairs))
    vis = ('<div class="ac-hero-vis ac-hx" aria-label="Bank statement lines matched to invoices and bills"><div class="ac-hx-top"><span class="ac-hx-app">%s<b>Bank Reconciliation</b></span>'
           '<span class="ac-hx-acct">%s HDFC Current A/c &middot; 0042</span></div>'
           '<div class="ac-hx-cols"><p class="ac-hx-h"><span>Bank statement</span><span></span><span>Odoo</span></p>'
           '<ul class="ac-hx-l">%s</ul><svg class="ac-hx-svg" viewBox="0 0 100 %d" preserveAspectRatio="none" aria-hidden="true">%s</svg><ul class="ac-hx-r">%s</ul></div>'
           '<div class="ac-hx-foot"><span><b>38</b> of 41 lines matched automatically today</span><i><b style="width:93%%"></b></i></div></div>'
           % (g["TILE_ICONS"][7], BANK, lrows, H * 5, paths, rrows))
    return '<section class="ac-hero">%s%s</section>' % (copy, vis)


# ------------------------------------------------------------------ data
# invoices / bills: [id, kind, number, partner, place, date, due, lines[[name, qty, price]], tax, state, pay, paid, late]
MOVES = [
    {"id": 1, "k": "out", "n": "", "p": "Orbit Motors Pvt Ltd", "pl": "Pune, Maharashtra", "d": "Oct 14", "due": "Nov 13", "lines": [["Dealer portal implementation", 1, 980000]], "tax": "igst", "st": "draft", "pay": "not_paid", "paid": 0},
    {"id": 2, "k": "out", "n": "INV/2026/00412", "p": "Bluebay Retail Pvt Ltd", "pl": "Bengaluru, Karnataka", "d": "Oct 14", "due": "Nov 13",
     "lines": [["Ergo task chair", 24, 8450], ["Height-adjustable desk", 12, 32900], ["Installation &amp; setup", 1, 18000]], "tax": "igst", "st": "posted", "pay": "paid", "paid": 726408},
    {"id": 3, "k": "out", "n": "INV/2026/00411", "p": "Sunrise Clinics", "pl": "Hyderabad, Telangana", "d": "Oct 13", "due": "Oct 30", "lines": [["Clinic group onboarding", 1, 525000]], "tax": "igst", "st": "posted", "pay": "not_paid", "paid": 0},
    {"id": 4, "k": "out", "n": "INV/2026/00407", "p": "Kaveri Foods", "pl": "Coimbatore, Tamil Nadu", "d": "Oct 9", "due": "Oct 24", "lines": [["Annual support contract", 1, 100000]], "tax": "gst", "st": "posted", "pay": "in_payment", "paid": 118000},
    {"id": 5, "k": "out", "n": "INV/2026/00398", "p": "Shree Distributors", "pl": "Chennai, Tamil Nadu", "d": "Oct 1", "due": "Oct 31", "lines": [["ERP for 3 branches: milestone 1", 1, 500000]], "tax": "gst", "st": "posted", "pay": "partial", "paid": 300000},
    {"id": 6, "k": "out", "n": "INV/2026/00385", "p": "Nair Textiles", "pl": "Kochi, Kerala", "d": "Aug 29", "due": "Sep 28", "lines": [["CRM rollout for 2 showrooms", 1, 480000]], "tax": "igst", "st": "posted", "pay": "not_paid", "paid": 0, "late": True},
    {"id": 11, "k": "in", "n": "", "p": "Shakti Fabrics", "pl": "Tiruppur, Tamil Nadu", "d": "Oct 14", "due": "Nov 13", "lines": [["Mesh fabric roll", 600, 420]], "tax": "gst", "st": "draft", "pay": "not_paid", "paid": 0, "src": "Digitized from email"},
    {"id": 12, "k": "in", "n": "BILL/2026/10/0007", "p": "Kaveri Steel Works", "pl": "Salem, Tamil Nadu", "d": "Oct 10", "due": "Oct 25", "lines": [["Steel chair frame", 120, 1790]], "tax": "gst", "st": "posted", "pay": "paid", "paid": 253464},
    {"id": 13, "k": "in", "n": "BILL/2026/10/0006", "p": "Pioneer Packaging", "pl": "Chennai, Tamil Nadu", "d": "Oct 6", "due": "Oct 20", "lines": [["Corrugated carton, 5-ply", 2000, 38]], "tax": "gst", "st": "posted", "pay": "not_paid", "paid": 0},
    {"id": 14, "k": "in", "n": "BILL/2026/10/0005", "p": "Sri Lakshmi Metals", "pl": "Coimbatore, Tamil Nadu", "d": "Sep 24", "due": "Oct 9", "lines": [["Steel chair frame", 120, 1850]], "tax": "gst", "st": "posted", "pay": "not_paid", "paid": 0, "late": True},
]


# ------------------------------------------------------------------ sections
def build(g):
    out = ""
    app_icon = g["TILE_ICONS"][7]

    # 1 ---- what the best accounting software should manage
    areas = [("inv", "Customer invoicing", "Customers &rsaquo; Invoices", "GST invoices with HSN codes, e-Invoice IRN and payment links, created from sales orders or deliveries.", "Typing invoices in Tally after the sale"),
             ("bill", "Vendor bills", "Vendors &rsaquo; Bills", "Bills digitized from email, matched to purchase orders and receipts before they are paid.", "Bills checked by hand against challans"),
             ("bank", "Bank &amp; cash", "Accounting &rsaquo; Closing &rsaquo; Reconcile", "Statement lines imported daily and matched to invoices and bills automatically.", "Ticking bank statements in Excel"),
             ("tax", "GST &amp; TDS", "Reporting &rsaquo; Tax Report", "CGST, SGST and IGST computed on every line, with GSTR-1 and 3B figures ready to file.", "Rebuilding GST figures every month"),
             ("ar", "Receivables &amp; follow-up", "Reporting &rsaquo; Aged Receivable", "Overdue invoices by age, with reminder emails sent on a schedule.", "Calling customers from a list"),
             ("asset", "Assets &amp; depreciation", "Accounting &rsaquo; Assets", "Asset register with depreciation posted every month.", "Year-end depreciation worksheet"),
             ("budget", "Budgets &amp; cost centres", "Configuration &rsaquo; Financial Budgets", "Budgets per branch or project, compared with actuals through analytic accounts.", "Branch P&amp;Ls built from exports"),
             ("close", "Closing &amp; reports", "Reporting &rsaquo; Statement Reports", "Profit and Loss, Balance Sheet and Cash Flow, live at any date, with lock dates once filed.", "Waiting for month end to see numbers")]
    out += sec(head("WHAT IT SHOULD MANAGE", "What Should the Best Accounting Software Actually Help Your Business Manage?",
                    "More than bookkeeping. Good accounting software runs the daily finance work and keeps the books current as it happens. "
                    "These are the eight areas we set up, and what each one replaces.", "is-center")
               + '<ul class="pl-grid is-plain" style="--cols:4">%s</ul>'
                 % "".join('<li><span class="pl-n">%02d</span><b>%s</b><p>%s</p><p class="pl-foot"><span class="pl-chip is-bad">Replaces</span> %s</p></li>' % (i + 1, a[1], a[3], a[4]) for i, a in enumerate(areas)),
               "ac-sec--areas")

    # 2 ---- core operations in one system: dashboard, invoices, bills
    menu = "".join('<button type="button" class="ac-menu%s" data-ax-menu="%s" aria-pressed="%s">%s</button>' % (" is-on" if k == "dash" else "", k, "true" if k == "dash" else "false", n)
                   for k, n in [("dash", "Dashboard"), ("out", "Customers"), ("in", "Vendors")])
    out += sec(head("ONE SYSTEM FOR CORE ACCOUNTING", "How Can Odoo Bring Your Core Accounting Operations Into One System?",
                    "This is the Odoo Accounting dashboard as your finance team will use it. Open <b>Customer Invoices</b>, confirm the draft invoice for "
                    "Orbit Motors, then register a payment against it.", "is-center")
               + '<div class="ox ac-ox ac-ax" data-ax><div class="ox-nav"><span class="ox-app">%s<b>Accounting</b></span><span class="ac-menus" role="group" aria-label="Accounting menu">%s</span>'
                 '<span class="ox-menu">Accounting</span><span class="ox-menu">Reporting</span><span class="ox-nav-r"><span class="ox-company">Your Company</span><span class="ox-av" style="--c:#C98600">D</span></span></div>'
                 '<div class="ox-cp"><div class="ox-cp-l"><button type="button" class="ox-new" data-ax-new>New</button><span class="ox-crumb ox-crumb--stack" data-ax-crumb>Accounting Dashboard</span></div>'
                 '<label class="ox-search">%s<span class="ox-facet" data-ax-facet hidden></span><input type="search" placeholder="Search..." aria-label="Search invoices and bills" data-ax-q></label><span></span></div>'
                 '<div class="ox-body ac-ax-body" data-ax-body></div></div>'
                 '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview with sample data. Click a journal, open an invoice, confirm it and register a payment.</p>'
                 % (app_icon, menu, SEARCH), "ac-sec--explore", "explore")

    # 3 ---- match Odoo to your finance processes: fit-gap
    fit = [("Invoicing", ["Invoice after delivery", "Invoice on order (advance)", "Milestone billing"],
            ["Invoicing policy: <b>Delivered quantities</b> on the product", "<b>Down payments</b> from the sales order, deducted on the final invoice", "<b>Milestones</b> on the order line, invoiced as each is reached"]),
           ("Credit control", ["No credit limits", "Credit limit per dealer", "Block orders when overdue"],
            ["Standard: invoices and reminders only", "<b>Sales Credit Limit</b> in settings, with a limit on each customer", "Credit limit warning plus a small rule that blocks confirmation"]),
           ("Bill approval", ["Accounts posts all bills", "Manager approves above a limit", "Bills must match the PO"],
            ["Bills posted by the <b>Billing</b> role", "<b>Purchase Order Approval</b> before the order, so bills follow approved POs", "<b>Bill Control: received quantities</b> with 3-way matching"]),
           ("Payments", ["Cheques and NEFT by hand", "Weekly payment run", "Collections via UPI links"],
            ["<b>Register Payment</b> on each bill, printed cheques if needed", "<b>Batch Payments</b> exported as a bank upload file", "<b>Online Payments</b> on invoices with Razorpay or UPI"]),
           ("Month end", ["Close in Tally after 10th", "Close by the 5th", "Branch-wise close"],
            ["Lock date set after each GST return", "<b>Closing</b> checklist with accruals and <b>Lock Dates</b>", "<b>Analytic plans</b> per branch with a lock date for the company"])]
    kind = ["std", "cfg", "cfg"]
    rows = ""
    for i, (area, opts, maps) in enumerate(fit):
        sel = "".join('<option value="%d">%s</option>' % (j, o) for j, o in enumerate(opts))
        rows += ('<tr><th>%s</th><td><select data-fit="%d" aria-label="Your practice for %s">%s</select></td><td data-fit-odoo="%d">%s</td><td data-fit-k="%d"></td></tr>'
                 % (area, i, area, sel, i, maps[0], i))
    out += sec(head("MATCHED TO YOUR PROCESS", "How Does Unisas Match Odoo Accounting to Your Existing Finance Processes?",
                    "We don't change how your finance team works to suit the software. We map each practice to the Odoo feature that does it. "
                    "Choose how you work today and see what we would set up.", "is-center")
               + '<div class="ac-fit ox-solo" data-fitbox><div class="ox-scroll"><table class="ac-fit-t"><thead><tr><th>Process</th><th>How you work today</th><th>What we set up in Odoo</th><th>Fit</th></tr></thead>'
                 '<tbody>%s</tbody></table></div><p class="ac-fit-sum" data-fit-sum aria-live="polite"></p></div>'
                 '<script type="application/json" id="ac-fit">%s</script>' % (rows, json.dumps([[m for m in f[2]] for f in fit])), "ac-sec--fit")

    # 4 ---- connected: the journal entries each app posts
    ops = [("sale", "Sales", "#EE8A3C", "Invoice the customer", "INV/2026/00412 posted for Bluebay Retail",
            [["121000 Accounts Receivable", 726408, 0], ["400000 Product Sales", 0, 615600], ["Output IGST 18%", 0, 110808]]),
           ("dlv", "Inventory", "#1F8A78", "Deliver the goods", "WH/OUT/00231 validated: 24 chairs, 12 desks",
            [["500000 Cost of Goods Sold", 410000, 0], ["110100 Inventory Valuation", 0, 410000]]),
           ("rec", "Inventory", "#1F8A78", "Receive from a vendor", "WH/IN/00012 validated: 120 steel frames",
            [["110100 Inventory Valuation", 214800, 0], ["Bills to receive", 0, 214800]]),
           ("bill", "Purchase", "#3E7CB1", "Post the vendor bill", "BILL/2026/10/0007 from Kaveri Steel Works",
            [["Bills to receive", 214800, 0], ["Input CGST 9%", 19332, 0], ["Input SGST 9%", 19332, 0], ["211000 Accounts Payable", 0, 253464]]),
           ("pay", "Accounting", "#8E4F83", "Pay and reconcile", "NEFT to Kaveri Steel Works matched on the HDFC statement",
            [["211000 Accounts Payable", 253464, 0], ["101401 Bank", 0, 253464]])]
    obtn = "".join('<li><button type="button" class="ac-op" data-op="%d" style="--c:%s"><span class="ac-op-app">%s</span><b>%s</b><small>%s</small><span class="ac-op-st">Post</span></button></li>'
                   % (i, c, app, t, d) for i, (k, app, c, t, d, l) in enumerate(ops))
    out += sec(head("CONNECTED APPS", "Can Odoo Connect Accounting With Sales, Purchase and Inventory?",
                    "Yes, and nobody re-types anything. Every sale, delivery, receipt and bill posts its own journal entry the moment it happens. "
                    "Post each step and watch the general ledger build itself, balanced at every step.", "is-center")
               + '<div class="ac-je" data-je><ol class="ac-ops">%s</ol><div class="ac-je-r"><div class="ox ac-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Journal Entries</a><span data-je-name>Nothing posted yet</span></span></div>'
                 '<span></span><button type="button" class="ox-sbtn ac-je-reset" data-je-reset>Reset</button></div><div class="ox-scroll"><table class="ac-jt" data-je-entry></table></div></div>'
                 '<div class="ac-gl ox-solo"><p class="ac-gl-h"><b>General Ledger</b><small data-je-check></small></p><div class="ox-scroll"><table class="ac-jt is-gl" data-je-gl></table></div></div></div></div>'
                 '<script type="application/json" id="ac-ops">%s</script>' % (obtn, json.dumps([[o[3], o[4], o[5], o[1]] for o in ops])), "ac-sec--je")

    # 5 ---- configure before go-live
    cfg = [("Fiscal localization", "Settings &rsaquo; Fiscal Localization", "<b>India - Accounting</b> package: Indian chart of accounts, GST tax groups and the GSTR reports. Company GSTIN and state set, so the right tax applies:  CGST + SGST and when IGST."),
           ("Chart of accounts", "Configuration &rsaquo; Chart of Accounts", "Your Tally ledgers mapped to the new accounts and account types, so the Balance Sheet and P&amp;L group correctly from day one."),
           ("Taxes", "Configuration &rsaquo; Taxes", "GST 5, 12, 18 and 28%, IGST, reverse charge, and TDS sections such as 194C and 194J, with fiscal positions for exports and SEZ."),
           ("Journals &amp; banks", "Configuration &rsaquo; Journals", "One bank journal per account (HDFC, ICICI), cash journals per branch, and the outstanding receipts and payments accounts."),
           ("Payment terms &amp; reminders", "Configuration &rsaquo; Payment Terms", "30 Days, 50% advance, end-of-month terms, plus <b>Invoice Reminders</b> at 7, 15 and 30 days overdue."),
           ("Fiscal year &amp; lock dates", "Accounting &rsaquo; Closing &rsaquo; Lock Dates", "April to March fiscal year. Lock dates set after each filed return so nobody posts into a closed period."),
           ("Opening balances", "Accounting &rsaquo; Journal Entries", "Trial balance at cut-over, plus every open invoice and bill, so ageing and follow-ups are right from day one."),
           ("Documents &amp; e-Invoicing", "Settings &rsaquo; Indian Electronic Invoicing", "Invoice layout with HSN and bank details, e-Invoice IRN and e-Way bill credentials on the GST portal."),
           ("Users &amp; access", "Settings &rsaquo; Users", "<b>Billing</b> for the billing team, <b>Accountant</b> for finance, <b>Auditor</b> read-only access for your CA.")]
    out += sec(head("BEFORE GO-LIVE", "What Does Your Business Need to Configure Before Going Live?",
                    "Nine things decide whether your books are right from the first day. We set each one with your accountant.", "is-center")
               + '<ol class="pl-grid is-line" style="--cols:3">%s</ol>'
                 % "".join('<li><span class="pl-n">%02d</span><b>%s</b><p>%s</p></li>' % (i + 1, t, x) for i, (t, p, x) in enumerate(cfg)), "ac-sec--cfg")

    # 6 ---- less manual work: bank reconciliation
    out += sec(head("LESS MANUAL WORK", "How Can Odoo Reduce Manual Invoicing, Payments and Reconciliation Work?",
                    "Invoices are created from orders, payments come in through payment links, and bank lines match themselves. "
                    "This is Odoo's bank reconciliation. Select a statement line and validate the match Odoo proposes, or reconcile them all at once.", "is-center")
               + '<div class="ac-rec" data-rec><div class="ox ac-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Bank</a><span>HDFC Current A/c &middot; 0042</span></span></div>'
                 '<span></span><button type="button" class="ox-pbtn" data-rec-all>Reconcile all</button></div>'
                 '<div class="ac-rec-grid"><ul class="ac-rec-lines" data-rec-lines></ul><div class="ac-rec-panel" data-rec-panel aria-live="polite"></div></div></div>'
                 '<ul class="ac-auto">'
                 '<li><b>Invoices from orders</b><span>Delivered quantities become a draft invoice; nothing is typed twice.</span></li>'
                 '<li><b>Payment links</b><span>Customers pay by UPI or card from the invoice email; Odoo registers the payment.</span></li>'
                 '<li><b>Bills from email</b><span>Vendor PDFs sent to bills@ are digitized into draft bills.</span></li>'
                 '<li><b>Reminders</b><span>Overdue invoices get polite reminders at 7, 15 and 30 days.</span></li></ul></div>', "ac-sec--rec", "reconcile")

    # 7 ---- when to customize: decision tree
    examples = [("Show HSN code and our bank details on invoices", ["y"], "studio", "Odoo Studio / report layout", "A day"),
                ("Depreciation posted every month", ["n", "y"], "cfg", "Assets with a depreciation model", "Part of setup"),
                ("Budget against actual for each branch", ["n", "y"], "cfg", "Financial Budgets with analytic plans", "Part of setup"),
                ("Two-level approval for bills above &#8377; 5 lakh", ["n", "n", "y"], "custom", "Small approval module on vendor bills", "About a week"),
                ("Sales commission on collected invoices", ["n", "n", "y"], "custom", "Commission rule on reconciled payments", "1 to 2 weeks"),
                ("A one-off reclassification for last year", ["n", "n", "n"], "manual", "Journal entry by your accountant", "An hour")]
    ex = "".join('<li><button type="button" class="ac-ex%s" data-ex="%d" aria-pressed="%s">%s</button></li>' % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", e[0]) for i, e in enumerate(examples))
    qs = [("q1", "Is it about how a document looks, or a field you need to record?"), ("q2", "Does standard Odoo already have a setting or feature for it?"), ("q3", "Does it happen often enough that doing it by hand costs real time?")]
    tree = "".join('<div class="ac-tq" data-tq="%d"><span class="ac-tq-n mono">%d</span><p>%s</p><span class="ac-tq-a"><i data-a="y">Yes</i><i data-a="n">No</i></span></div>' % (i, i + 1, q) for i, (k, q) in enumerate(qs))
    out += sec(head("CONFIGURE OR CUSTOMIZE", "When Should Odoo Accounting Be Customized for Your Business?",
                    "Only when configuration and Studio can't do the job and the task repeats often enough to pay for the code. Pick a requirement to see how we decide.", "is-center")
               + '<div class="ac-tree" data-tree><ul class="ac-exs">%s</ul><div class="ac-tree-r ox-solo"><div class="ac-tqs">%s</div>'
                 '<div class="ac-verdict" aria-live="polite"><span class="ac-v-kind" data-v-kind></span><b data-v-how></b><small data-v-eff></small></div></div></div>'
                 '<script type="application/json" id="ac-ex">%s</script>' % (ex, tree, json.dumps(examples)), "ac-sec--tree")

    # 8 ---- migration from Tally
    groups = [("Sundry Debtors", "Receivable", "121000 Accounts Receivable"), ("Sundry Creditors", "Payable", "211000 Accounts Payable"),
              ("Bank Accounts", "Bank and Cash", "101401 HDFC Current A/c"), ("Duties &amp; Taxes", "Current Liabilities", "Output CGST / SGST / IGST"),
              ("Sales Accounts", "Income", "400000 Product Sales"), ("Purchase Accounts", "Cost of Revenue", "500000 Cost of Goods Sold"),
              ("Indirect Expenses", "Expenses", "600000 Expenses"), ("Fixed Assets", "Fixed Assets", "151000 Fixed Assets"),
              ("Capital Account", "Equity", "301000 Capital"), ("Suspense A/c", "To be mapped", "&mdash;")]
    grows = "".join('<tr class="%s"><td>%s</td><td class="ox-muted">&rarr;</td><td><span class="ac-type">%s</span></td><td>%s</td></tr>'
                    % ("is-gap" if t == "To be mapped" else "", a, t, o) for a, t, o in groups)
    moved = [("Ledgers &rarr; accounts", "412 &rarr; 186", "Duplicates and dead ledgers merged"), ("Customers &amp; vendors", "1,240", "With GSTIN and state"),
             ("Open invoices", "318 &middot; " + inr(18640200, False), "So ageing is right on day one"), ("Open bills", "164 &middot; " + inr(7215400, False), "With due dates"),
             ("Opening trial balance", "31 Mar 2026", "Tallied to the audited books"), ("History", "2 years", "Monthly balances for comparison reports")]
    out += sec(head("DATA MIGRATION", "How Does Unisas Migrate Your Existing Accounting Data to Odoo?",
                    "Most of our clients come from Tally. We map every ledger group to an Odoo account, bring across what is still open, and prove the opening trial balance before cut-over.", "is-center")
               + '<div class="ac-mig"><div class="ox ac-ox" data-tb><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Migration</a><span>Tally ledger groups &rarr; Odoo accounts</span></span></div></div>'
                 '<div class="ox-scroll"><table class="ox-table ac-map"><thead><tr><th>Tally group</th><th></th><th>Odoo account type</th><th>Odoo account</th></tr></thead><tbody data-tb-map>%s</tbody></table></div>'
                 '<div class="ac-tb"><p class="ac-tb-h"><b>Opening trial balance check</b><small>As of 31 Mar 2026</small></p>'
                 '<dl class="ac-tb-dl"><div><dt>Tally total debit</dt><dd>%s</dd></div><div><dt>Odoo total debit</dt><dd data-tb-odoo>%s</dd></div><div><dt>Difference</dt><dd data-tb-diff class="ac-red">%s</dd></div></dl>'
                 '<div class="ac-tb-btns"><button type="button" class="ox-pbtn" data-tb-fix>Map Suspense A/c and re-check</button></div><p class="ac-tb-res" data-tb-res aria-live="polite">One ledger is still unmapped, so the books don&rsquo;t tie yet.</p></div></div>'
                 '<ul class="ac-moved ox-solo"><li class="ac-moved-h"><b>What moves to Odoo</b><small>Sample from a 3-branch distributor</small></li>%s</ul></div>'
                 % (grows, inr(48216540), inr(48204060), inr(12480), "".join('<li><span>%s<small>%s</small></span><b>%s</b></li>' % (a, c, b) for a, b, c in moved)), "ac-sec--mig")

    # 9 ---- financial reports
    rtabs = "".join('<button type="button" class="ac-rtab%s" data-rep="%s" aria-pressed="%s">%s</button>' % (" is-on" if i == 0 else "", k, "true" if i == 0 else "false", n)
                    for i, (k, n) in enumerate([("pl", "Profit and Loss"), ("bs", "Balance Sheet"), ("ar", "Aged Receivable"), ("tax", "Tax Report"), ("ex", "Executive Summary")]))
    out += sec(head("REPORTS &amp; INSIGHTS", "What Financial Reports and Business Insights Can Odoo Provide?",
                    "Every report is live, at any date, and drills down to the entry behind each number. Switch reports, compare with last month, and unfold a line.", "is-center")
               + '<div class="ox ac-ox ac-rep" data-rep-box>%s<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb" data-rep-title>Profit and Loss</span></div><span></span>'
                 '<label class="ac-cmp"><input type="checkbox" data-rep-cmp checked> Compare: Previous Period</label></div>'
                 '<div class="ac-rtabs" role="group" aria-label="Reports">%s</div><div class="ac-rep-filters"><span class="ox-sbtn">&#128197; Sep 2026</span><span class="ox-sbtn">Journals: All</span><span class="ox-sbtn">Analytic: All branches</span><span class="ox-sbtn">PDF</span><span class="ox-sbtn">XLSX</span></div>'
                 '<div class="ox-scroll"><table class="ac-rt" data-rep-t></table></div></div>' % (odoo_nav(app_icon), rtabs), "ac-sec--rep")

    # 10 ---- integrations
    ints = [("Banks", "HDFC, ICICI, Axis", "Daily", "In", [["06:10", "Statement imported: 41 lines, closing balance &#8377; 49,85,880.00"], ["06:10", "38 lines matched automatically"], ["06:11", "3 lines left for review"]]),
            ("GST e-Invoice", "IRP via GSP", "On posting", "Out", [["11:42", "INV/2026/00412: IRN generated, QR code added to the PDF"], ["11:43", "Acknowledgement 1324 1000 9877 stored on the invoice"], ["15:02", "INV/2026/00398: e-Invoice cancelled within 24 hours"]]),
            ("e-Way Bill", "NIC portal", "On delivery", "Out", [["12:05", "EWB 4211 0098 7765 generated for WH/OUT/00231, valid till Oct 16"], ["12:05", "Vehicle TN 09 BX 4412 added"]]),
            ("GSTR filing data", "GSTR-1 / 3B / 2B", "Monthly", "Both", [["Oct 9", "GSTR-2B downloaded: 164 vendor invoices"], ["Oct 9", "Matched 158, 6 missing in vendor filings"], ["Oct 11", "GSTR-1 JSON exported for September"]]),
            ("Payment gateway", "Razorpay, UPI", "Real time", "In", [["10:21", "&#8377; 1,18,000.00 received from Kaveri Foods for INV/2026/00407"], ["10:21", "Payment registered, invoice In Payment"]]),
            ("Payroll", "Odoo Payroll or your provider", "Monthly", "In", [["Sep 30", "Salary journal posted: 64 employees, &#8377; 38,42,000.00"], ["Sep 30", "PF, ESI and TDS liabilities booked"]]),
            ("BI &amp; Excel", "Spreadsheet, Power BI", "Live", "Out", [["Live", "Branch P&amp;L pivot refreshed from the ledger"], ["Live", "Receivables dashboard shared with directors"]]),
            ("Tally (during transition)", "Parallel run", "Daily", "Out", [["Oct 1", "Day book exported for the parallel run"], ["Oct 1", "Trial balance compared: no differences"]])]
    ibtn = "".join('<li><button type="button" class="ac-int%s" data-int="%d" aria-pressed="%s"><b>%s</b><small>%s</small></button></li>'
                   % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", n, w) for i, (n, w, f, d, l) in enumerate(ints))
    out += sec('%s<div class="ac-ints"><ul class="ac-int-list">%s</ul><div class="ac-int-log ox-solo" aria-live="polite"><p class="ac-int-h"><b data-int-name></b>'
               '<span><small>Direction</small><em data-int-dir></em></span><span><small>Runs</small><em data-int-freq></em></span></p><ol data-int-log></ol></div></div>'
               '<script type="application/json" id="ac-int">%s</script>'
               % (head("INTEGRATIONS", "How Does Unisas Integrate Odoo Accounting With Your Other Business Systems?",
                       "Banks, the GST portal, payment gateways and payroll feed Odoo directly, so finance stops re-entering what another system already knows. Pick a connection to see its activity log."),
                  ibtn, json.dumps(ints)), "ac-sec--int")

    # 11 ---- testing before go-live: parallel run
    tb = [("Sundry Debtors / Accounts Receivable", 18640200, 18640200), ("Sundry Creditors / Accounts Payable", -7215400, -7215400), ("HDFC Current A/c / Bank", 4985880, 4985880),
          ("Output GST", -1284310, -1271830), ("Sales Accounts / Product Sales", -41260000, -41260000), ("Indirect Expenses / Expenses", 6420500, 6420500)]
    trows = "".join('<tr><th>%s</th><td class="is-c">%s</td><td class="is-c">%s</td><td class="is-c">%s</td></tr>'
                    % (n, inr(t), inr(o), '<span class="pl-chip is-bad">%s</span>' % inr(t - o) if t != o else '<span class="pl-chip is-ok">&#10003; 0.00</span>') for n, t, o in tb)
    uat = [("Billing", [("Invoice from a delivered sales order", True), ("Send an e-Invoice and check the IRN", False)]),
           ("Accounts", [("Post a vendor bill from email", True), ("Reconcile a full day of bank lines", False), ("File GSTR-3B figures from the Tax Report", False)]),
           ("Management", [("Read the P&amp;L by branch", False)])]
    ul = ""
    for role, items in uat:
        ul += '<li class="ac-uat-role">%s</li>' % role
        ul += "".join('<li><label class="ac-uat-i"><input type="checkbox" data-uat%s><span class="ac-chk" aria-hidden="true">%s</span><span>%s</span></label></li>' % (" checked" if on else "", TICK, t) for t, on in items)
    out += sec(head("TESTING &amp; GO-LIVE", "How Do We Test and Prepare Your Accounting System Before Go-Live?",
                    "For one month Odoo runs beside your old system. Every difference is explained and fixed before you switch, and each role signs off its own scenarios.", "is-center")
               + '<div class="ac-test"><div class="pl-card"><p class="pl-k">Parallel run &middot; trial balance, September 2026</p><div class="pl-scroll"><table class="pl-table"><thead><tr><th>Account</th><th class="is-c">Old system</th><th class="is-c">New system</th><th class="is-c">Difference</th></tr></thead>'
                 '<tbody>%s</tbody></table></div><p class="pl-muted" style="margin:12px 0 0;font-size:0.88rem"><b style="color:var(--text)">Explained and fixed:</b> a GST credit note was posted in Tally on Sep 30 and in the new books on Oct 1. Corrected and locked before sign-off.</p></div>'
                 '<div class="ac-uat ox-solo" data-uatbox><div class="ac-uat-h"><span><small>User acceptance testing</small><b>Go-live readiness</b></span><span class="ac-uat-pct" data-uat-pct></span></div>'
                 '<div class="ac-uat-bar"><i data-uat-bar></i></div><ul>%s</ul><p class="ac-uat-res" data-uat-res aria-live="polite"></p></div></div>' % (trows, ul), "ac-sec--test")

    # 12 ---- what changes
    kpis = [("Month-end close", 12, 4, "days"), ("Invoice sent after delivery", 6, 0, "days"), ("Days sales outstanding", 58, 41, "days"),
            ("Bank reconciliation", 16, 1, "hours a month"), ("GST return preparation", 24, 3, "hours a month"), ("Manual journal entries", 900, 120, "a month")]
    krows = "".join('<li data-b="%d" data-a="%d"><span class="ac-k-n">%s</span><span class="ac-k-bar"><i></i></span><b class="ac-k-v">%d</b><small>%s</small></li>' % (b, a, n, b, u) for n, b, a, u in kpis)
    out += sec(head("WHAT CHANGES", "What Can a Properly Implemented Accounting System Change for Your Business?",
                    "Typical results from our accounting projects, measured three months after go-live. Switch between before and after.", "is-center")
               + '<div class="ac-chg ox-solo" data-chg><div class="ac-chg-sw" role="group" aria-label="Compare"><button type="button" class="is-on" data-chg-m="b" aria-pressed="true">Before Odoo</button>'
                 '<button type="button" data-chg-m="a" aria-pressed="false">After Odoo</button></div><ul class="ac-kl">%s</ul>'
                 '<p class="ac-chg-note" data-chg-note aria-live="polite"></p></div>' % krows, "ac-sec--chg")

    # 13 ---- readiness: maturity check
    mat = [("Invoicing", ["Typed by hand", "From a separate tool", "From orders, automatically"]),
           ("Bank reconciliation", ["In Excel at month end", "Weekly in Tally", "Daily, mostly automatic"]),
           ("GST returns", ["Rebuilt every month", "Exported, then fixed", "Straight from the books"]),
           ("Reports", ["Built at month end", "From exports when asked", "Live, at any date"]),
           ("Payments &amp; collections", ["Chased by phone", "Reminders sent by hand", "Links and automatic reminders"])]
    mrows = "".join('<li><span>%s</span><span class="ac-seg" role="group" aria-label="%s">%s</span></li>'
                    % (a, a, "".join('<button type="button" data-m="%d" data-v="%d" aria-pressed="false">%s</button>' % (i, j, o) for j, o in enumerate(opts))) for i, (a, opts) in enumerate(mat))
    out += sec('<div class="ac-quiz"><div>%s<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Book a finance process review %s</a></div></div>'
               '<div class="ac-q ox-solo" data-mat><p class="ac-q-h"><b>Finance maturity check</b><small>Choose where you are today in each area</small></p><ol>%s</ol>'
               '<div class="ac-q-res"><span class="ac-q-dial" data-mat-dial style="--p:0"><b data-mat-score>0</b></span><p data-mat-txt>Answer all five to see your score.</p></div></div></div>'
               % (head("READINESS CHECK", "Is Your Business Ready to Move to a Better Accounting System?",
                       "Mostly on the left? Your finance team is doing the system&rsquo;s work. We&rsquo;ll show your month in Odoo."),
                  g["ARROW"], mrows), "ac-sec--quiz")

    return out + JS.replace("__MOVES__", json.dumps(MOVES))


JS = r'''<script>
(function(){
  function inr(n,d){var s=Math.abs(n).toLocaleString('en-IN',{minimumFractionDigits:d===false?0:2,maximumFractionDigits:d===false?0:2});return (n<0?'-':'')+'₹ '+s;}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function press(group,el){group.forEach(function(b){var on=b===el;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});}
  function J(id){return JSON.parse(document.getElementById(id).textContent);}

  /* --- 2 accounting explorer --- */
  var ax=document.querySelector('[data-ax]');
  if(ax){var M=__MOVES__,body=ax.querySelector('[data-ax-body]'),crumb=ax.querySelector('[data-ax-crumb]'),q=ax.querySelector('[data-ax-q]'),facet=ax.querySelector('[data-ax-facet]');
    var st={menu:'dash',open:null,tab:'lines',pay:false,f:null},seq={out:413,in:8};
    var PS={not_paid:['Not Paid','np'],in_payment:['In Payment','ip'],paid:['Paid','pd'],partial:['Partially Paid','pp']};
    M.forEach(function(m){m.log=[{w:'Unisas Bot',t:m.src?m.src+': vendor, date and amounts read from the PDF':(m.st==='draft'?'Draft created':'Invoice created')}];});
    function unt(m){return m.lines.reduce(function(s,l){return s+l[1]*l[2];},0);}
    function tax(m){return Math.round(unt(m)*0.18);}
    function tot(m){return unt(m)+tax(m);}
    function due(m){return tot(m)-m.paid;}
    function find(id){return M.filter(function(x){return x.id===+id;})[0];}
    function name(m){return m.n||(m.k==='out'?'Draft Invoice':'Draft Bill');}
    function badge(m){if(m.st==='draft')return '<span class="ac-b ac-b--dr">Draft</span>';var p=PS[m.pay];return '<span class="ac-b ac-b--'+p[1]+'">'+p[0]+'</span>';}
    function card(k,title,code,btn,rows,graph){return '<article class="ac-jc" data-jc="'+k+'"><p class="ac-jc-h"><b>'+title+'</b><small>'+code+'</small></p><div class="ac-jc-b"><div>'+btn+'</div><dl>'+rows+'</dl></div>'+graph+'</article>';}
    function bars(v,late){var mx=Math.max.apply(null,v.concat([1]));return '<div class="ac-jc-g">'+v.map(function(x,i){return '<span><i class="'+(i===0&&late?'is-late':'')+'" style="height:'+Math.max(4,x/mx*100)+'%"></i><small>'+['Due','This Week','Next Week','Later'][i]+'</small></span>';}).join('')+'</div>';}
    function dash(){var O=M.filter(function(m){return m.k==='out';}),I=M.filter(function(m){return m.k==='in';});
      function sum(l){return l.reduce(function(s,m){return s+due(m);},0);}
      var ou=O.filter(function(m){return m.st==='posted'&&m.pay!=='paid'&&m.pay!=='in_payment';}),ol=ou.filter(function(m){return m.late;}),od=O.filter(function(m){return m.st==='draft';});
      var iu=I.filter(function(m){return m.st==='posted'&&m.pay!=='paid'&&m.pay!=='in_payment';}),il=iu.filter(function(m){return m.late;}),idr=I.filter(function(m){return m.st==='draft';});
      function r(lbl,n,amt,f,cls){return '<div class="'+(cls||'')+'"><dt><button type="button" data-jf="'+f+'">'+n+' '+lbl+'</button></dt><dd>'+inr(amt,false)+'</dd></div>';}
      return '<div class="ac-dash">'+
        card('out','Customer Invoices','INV','<button type="button" class="ox-pbtn" data-ax-go="out">New Invoice</button><span class="ox-sbtn">Upload</span>',
          r('To Validate',od.length,od.reduce(function(s,m){return s+tot(m);},0),'out:draft')+r('Unpaid',ou.length,sum(ou),'out:unpaid')+r('Late',ol.length,sum(ol),'out:late','is-late'),bars([sum(ol),0,619500,Math.max(0,sum(ou)-sum(ol)-619500)],1))+
        card('in','Vendor Bills','BILL','<button type="button" class="ox-pbtn" data-ax-go="in">New Bill</button><span class="ox-sbtn">Upload</span>',
          r('To Validate',idr.length,idr.reduce(function(s,m){return s+tot(m);},0),'in:draft')+r('To Pay',iu.length,sum(iu),'in:unpaid')+r('Late',il.length,sum(il),'in:late','is-late'),bars([sum(il),89680,0,0],1))+
        card('bank','Bank','HDFC &middot; 0042','<a class="ox-pbtn ac-ln" href="#reconcile">Reconcile 3 Items</a>','<div><dt>Balance in GL</dt><dd>'+inr(4862300,false)+'</dd></div><div><dt>Last Statement</dt><dd>'+inr(4985880,false)+'</dd></div>',
          '<svg class="ac-jc-line" viewBox="0 0 200 50" preserveAspectRatio="none" aria-hidden="true"><path d="M0 38 L25 34 L50 36 L75 26 L100 28 L125 18 L150 22 L175 12 L200 14" fill="none" stroke="#017E84" stroke-width="2"/><path d="M0 38 L25 34 L50 36 L75 26 L100 28 L125 18 L150 22 L175 12 L200 14 V50 H0z" fill="rgba(1,126,132,0.1)"/></svg>')+
        card('cash','Cash','CSH1 &middot; Chennai','<span class="ox-sbtn">New Transaction</span>','<div><dt>Balance</dt><dd>'+inr(42650,false)+'</dd></div>','')+
        card('misc','Miscellaneous Operations','MISC','<span class="ox-sbtn">New Entry</span>','<div><dt>2 To Post</dt><dd>Accruals for September</dd></div>','')+
        card('tax','Tax Returns','GSTR-3B &middot; Sep','<span class="ox-sbtn">Tax Report</span>','<div class="is-late"><dt>Due Oct 20</dt><dd>'+inr(132450,false)+' payable</dd></div>','')+'</div>';}
    function rows(){var t=q.value.trim().toLowerCase();return M.filter(function(m){
      if(m.k!==st.menu)return false;if(st.f==='draft'&&m.st!=='draft')return false;if(st.f==='unpaid'&&!(m.st==='posted'&&(m.pay==='not_paid'||m.pay==='partial')))return false;if(st.f==='late'&&!m.late)return false;
      return !t||(name(m)+' '+m.p).toLowerCase().indexOf(t)>-1;});}
    function list(){var l=rows(),out=st.menu==='out';var tt=l.reduce(function(s,m){return s+tot(m);},0),dd=l.reduce(function(s,m){return s+(m.st==='posted'?due(m):0);},0);
      return '<div class="ox-scroll"><table class="ox-table"><thead><tr><th class="ox-chk"><span class="ox-cb"></span></th><th>Number</th><th>'+(out?'Customer':'Vendor')+'</th><th>'+(out?'Invoice':'Bill')+' Date</th><th>Due Date</th><th class="ox-num">Tax Excluded</th><th class="ox-num">Total</th><th class="ox-num">Amount Due</th><th>Status</th></tr></thead><tbody>'+
        (l.length?l.map(function(m){return '<tr data-id="'+m.id+'" tabindex="0"><td class="ox-chk"><span class="ox-cb"></span></td><td><b>'+name(m)+'</b></td><td>'+m.p+'</td><td>'+m.d+'</td><td class="'+(m.late&&m.pay!=='paid'?'ac-red':'')+'">'+m.due+'</td><td class="ox-num">'+inr(unt(m))+'</td><td class="ox-num">'+inr(tot(m))+'</td><td class="ox-num">'+(m.st==='posted'?inr(due(m)):'')+'</td><td>'+badge(m)+'</td></tr>';}).join(''):'<tr><td colspan="9" class="ox-empty">No record matches.</td></tr>')+
        '</tbody><tfoot><tr><td></td><td colspan="4"></td><td></td><td class="ox-num"><b>'+inr(tt)+'</b></td><td class="ox-num"><b>'+inr(dd)+'</b></td><td></td></tr></tfoot></table></div>';}
    function taxRows(m){var u=unt(m);return m.tax==='igst'?[['Output IGST 18%',Math.round(u*0.18)]]:[[(m.k==='out'?'Output':'Input')+' CGST 9%',Math.round(u*0.09)],[(m.k==='out'?'Output':'Input')+' SGST 9%',Math.round(u*0.09)]];}
    function jitems(m){var out=m.k==='out',l=[];
      if(out){l.push(['121000 Accounts Receivable',m.p,tot(m),0]);m.lines.forEach(function(x){l.push(['400000 Product Sales',x[0],0,x[1]*x[2]]);});taxRows(m).forEach(function(t){l.push([t[0],'',0,t[1]]);});}
      else{m.lines.forEach(function(x){l.push(['500000 Cost of Goods Sold',x[0],x[1]*x[2],0]);});taxRows(m).forEach(function(t){l.push([t[0].replace('Output','Input'),'',t[1],0]);});l.push(['211000 Accounts Payable',m.p,0,tot(m)]);}
      return '<table class="ac-lines"><thead><tr><th>Account</th><th>Label</th><th class="ox-num">Debit</th><th class="ox-num">Credit</th></tr></thead><tbody>'+
        l.map(function(x){return '<tr><td>'+x[0]+'</td><td class="ox-muted">'+x[1]+'</td><td class="ox-num">'+(x[2]?inr(x[2]):'')+'</td><td class="ox-num">'+(x[3]?inr(x[3]):'')+'</td></tr>';}).join('')+
        '</tbody><tfoot><tr><td colspan="2"></td><td class="ox-num"><b>'+inr(tot(m))+'</b></td><td class="ox-num"><b>'+inr(tot(m))+'</b></td></tr></tfoot></table>';}
    function form(m){var out=m.k==='out',dr=m.st==='draft';
      var sb=['Draft','Posted'].map(function(s){return '<span class="ox-sb'+((s==='Draft')===dr?' is-cur':'')+'">'+s+'</span>';}).join('');
      var b=dr?'<button type="button" class="ox-pbtn" data-do="confirm">Confirm</button><span class="ox-sbtn">Preview</span><span class="ox-sbtn">Cancel</span>':
        (m.pay==='paid'||m.pay==='in_payment'?'<button type="button" class="ox-sbtn" data-do="send">'+(out?'Send':'Print')+'</button><span class="ox-sbtn">Preview</span><span class="ox-sbtn">Reset to Draft</span>':
        '<button type="button" class="ox-pbtn" data-do="paywin">Register Payment</button><button type="button" class="ox-sbtn" data-do="send">'+(out?'Send':'Print')+'</button><span class="ox-sbtn">Preview</span><span class="ox-sbtn">Reset to Draft</span>');
      var rib=m.pay==='paid'?'<span class="ox-ribbon">PAID</span>':m.pay==='in_payment'?'<span class="ox-ribbon ac-rib-ip">IN PAYMENT</span>':m.pay==='partial'?'<span class="ox-ribbon ac-rib-pp">PARTIAL</span>':'';
      var tabs='<div class="ox-ftabs ac-ftabs"><button type="button" class="'+(st.tab==='lines'?'is-on':'')+'" data-tab="lines">'+(out?'Invoice':'Bill')+' Lines</button><button type="button" class="'+(st.tab==='ji'?'is-on':'')+'" data-tab="ji">Journal Items</button><button type="button" class="'+(st.tab==='oth'?'is-on':'')+'" data-tab="oth">Other Info</button></div>';
      var content;
      if(st.tab==='ji')content=jitems(m);
      else if(st.tab==='oth')content='<dl class="ox-fields ac-oth"><div><dt>Place of Supply</dt><dd>'+m.pl+'</dd></div><div><dt>Fiscal Position</dt><dd>'+(m.tax==='igst'?'Inter State':'Intra State')+'</dd></div><div><dt>Journal</dt><dd>'+(out?'Customer Invoices (INV)':'Vendor Bills (BILL)')+'</dd></div><div><dt>Payment Reference</dt><dd>'+(m.n||'Assigned on confirm')+'</dd></div></dl>';
      else content='<table class="ac-lines"><thead><tr><th>Product</th><th class="ox-num">Quantity</th><th class="ox-num">Price</th><th>Taxes</th><th class="ox-num">Amount</th></tr></thead><tbody>'+
        m.lines.map(function(x){return '<tr><td><b>'+x[0]+'</b></td><td class="ox-num">'+x[1]+'.00</td><td class="ox-num">'+inr(x[2])+'</td><td><span class="ac-tax">18% '+(m.tax==='igst'?'IGST':'GST')+'</span></td><td class="ox-num">'+inr(x[1]*x[2])+'</td></tr>';}).join('')+'</tbody></table>'+
        '<div class="ac-tot"><span>Untaxed Amount:</span><b>'+inr(unt(m))+'</b>'+taxRows(m).map(function(t){return '<span>'+t[0].replace(/^(Output|Input) /,'')+':</span><b>'+inr(t[1])+'</b>';}).join('')+
        '<span class="is-total">Total:</span><b class="is-total">'+inr(tot(m))+'</b>'+(m.paid?'<span class="ac-paid-l">Paid on Oct 14:</span><b class="ac-paid-l">'+inr(m.paid)+'</b><span class="is-total">Amount Due:</span><b class="is-total">'+inr(due(m))+'</b>':'')+'</div>';
      var pay=st.pay?'<div class="ac-paywin"><p class="ac-pw-h"><b>Register Payment</b><button type="button" data-do="paycancel" aria-label="Close">&times;</button></p><dl class="ox-fields"><div><dt>Journal</dt><dd>Bank (HDFC)</dd></div><div><dt>Amount</dt><dd><b>'+inr(due(m))+'</b></dd></div>'+
        '<div><dt>Payment Method</dt><dd>'+(out?'Manual (NEFT / UPI)':'NEFT')+'</dd></div><div><dt>Payment Date</dt><dd>Oct 14, 2026</dd></div><div><dt>Memo</dt><dd>'+m.n+'</dd></div></dl>'+
        '<p class="ac-pw-btns"><button type="button" class="ox-pbtn" data-do="pay">Create Payment</button><button type="button" class="ox-sbtn" data-do="paycancel">Discard</button></p></div>':'';
      var log=m.log.slice().reverse().map(function(l){return '<div class="ox-msg"><span class="ox-av is-bot">U</span><div><p><b>'+l.w+'</b> <small>just now</small></p><p>'+l.t+'</p></div></div>';}).join('');
      return '<div class="ox-form ac-form"><div class="ox-f-main"><div class="ox-f-bar"><span class="ox-f-btns">'+b+'</span><span class="ox-sbar">'+sb+'</span></div>'+pay+
        '<div class="ox-sheet">'+rib+'<p class="ac-doc-kind">'+(out?'Customer Invoice':'Vendor Bill')+'</p><h3>'+name(m)+'</h3><dl class="ox-fields"><div><dt>'+(out?'Customer':'Vendor')+'</dt><dd><span><b>'+m.p+'</b><br><small class="ox-muted">'+m.pl+'</small></span></dd></div>'+
        '<div><dt>'+(out?'Invoice':'Bill')+' Date</dt><dd>'+m.d+', 2026</dd></div><div><dt>GST Treatment</dt><dd>Registered Business - Regular</dd></div><div><dt>Due Date</dt><dd class="'+(m.late&&m.pay!=='paid'?'ac-red':'')+'">'+m.due+', 2026</dd></div></dl>'+tabs+content+'</div></div>'+
        '<aside class="ox-chatter"><div class="ox-ch-btns"><span class="ox-pbtn">Send message</span><span class="ox-sbtn">Log note</span><span class="ox-sbtn">Activity</span></div><p class="ox-ch-sep">Today</p>'+log+'</aside></div>';}
    function render(){ax.querySelectorAll('[data-ax-menu]').forEach(function(b){var on=b.getAttribute('data-ax-menu')===st.menu;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
      facet.hidden=!st.f||!!st.open||st.menu==='dash';facet.textContent={draft:'To Validate',unpaid:st.menu==='out'?'Unpaid':'To Pay',late:'Late'}[st.f]||'';
      var MN={out:'Invoices',in:'Bills'};
      if(st.open){var m=find(st.open);crumb.innerHTML='<a href="#" data-ax-back>'+MN[m.k]+'</a><span>'+name(m)+'</span>';body.innerHTML=form(m);return;}
      if(st.menu==='dash'){crumb.innerHTML='<span>Accounting Dashboard</span>';body.innerHTML=dash();return;}
      crumb.innerHTML='<span>'+MN[st.menu]+'</span>';body.innerHTML=list();}
    function log(m,t,w){m.log.push({w:w||'Divya (Accounts)',t:t});}
    ax.addEventListener('click',function(e){
      var mn=e.target.closest('[data-ax-menu]');if(mn){st.menu=mn.getAttribute('data-ax-menu');st.open=null;st.f=null;render();return;}
      var jf=e.target.closest('[data-jf]');if(jf){var p=jf.getAttribute('data-jf').split(':');st.menu=p[0];st.f=p[1];st.open=null;render();return;}
      var go=e.target.closest('[data-ax-go]');if(go){st.menu=go.getAttribute('data-ax-go');st.f=null;newDoc();return;}
      var jc=e.target.closest('[data-jc="out"],[data-jc="in"]');if(jc&&!e.target.closest('button,a,.ox-sbtn')){st.menu=jc.getAttribute('data-jc');st.f=null;render();return;}
      if(e.target.closest('[data-ax-back]')){e.preventDefault();st.open=null;st.pay=false;render();return;}
      var m=st.open&&find(st.open);
      var tb=e.target.closest('[data-tab]');if(tb&&m){st.tab=tb.getAttribute('data-tab');render();return;}
      var d=e.target.closest('[data-do]');
      if(d&&m){var x=d.getAttribute('data-do');
        if(x==='confirm'){m.st='posted';m.n=m.k==='out'?'INV/2026/00'+(seq.out++):'BILL/2026/10/000'+(seq.in++);log(m,'Status: Draft &rarr; <b>Posted</b>. Number '+m.n+' assigned.');if(m.k==='out')log(m,'e-Invoice: IRN generated and QR code added','GST Portal');}
        if(x==='paywin')st.pay=true;
        if(x==='paycancel')st.pay=false;
        if(x==='pay'){var a=due(m);m.paid+=a;m.pay='in_payment';st.pay=false;log(m,'Payment of <b>'+inr(a)+'</b> registered on Bank (HDFC). Status: <b>In Payment</b> until the bank statement line is reconciled.');}
        if(x==='send')log(m,(m.k==='out'?'Invoice emailed to '+m.p+' with a UPI payment link':'Printed'));
        render();return;}
      var r=e.target.closest('[data-id]');if(r){st.open=+r.getAttribute('data-id');st.tab='lines';st.pay=false;render();}});
    ax.addEventListener('keydown',function(e){if(e.key==='Enter'){var r=e.target.closest&&e.target.closest('[data-id]');if(r){st.open=+r.getAttribute('data-id');st.tab='lines';render();}}});
    function newDoc(){var out=st.menu!=='in';var m={id:100+seq.out+seq.in,k:out?'out':'in',n:'',p:out?'Orbit Motors Pvt Ltd':'Pioneer Packaging',pl:out?'Pune, Maharashtra':'Chennai, Tamil Nadu',d:'Oct 14',due:'Nov 13',
      lines:[[out?'Implementation services':'Corrugated carton, 5-ply',out?1:1000,out?150000:38]],tax:out?'igst':'gst',st:'draft',pay:'not_paid',paid:0,log:[{w:'Divya (Accounts)',t:'Draft created'}]};M.unshift(m);st.menu=m.k;st.open=m.id;st.tab='lines';render();}
    ax.querySelector('[data-ax-new]').addEventListener('click',function(){if(st.menu==='dash')st.menu='out';newDoc();});
    q.addEventListener('input',function(){st.open=null;if(st.menu==='dash')st.menu='out';render();});
    render();}

  /* --- 3 fit-gap --- */
  var fb=document.querySelector('[data-fitbox]');
  if(fb){var F=J('ac-fit');
    var KIND=[[0,1,1],[0,1,2],[0,1,1],[0,1,1],[1,1,1]];
    function fdraw(){var c={std:0,cfg:0,cus:0};
      fb.querySelectorAll('[data-fit]').forEach(function(s){var i=+s.getAttribute('data-fit'),v=+s.value,k=KIND[i][v],lab=[['std','Standard'],['cfg','Configuration'],['cus','Small customization']][k];
        fb.querySelector('[data-fit-odoo="'+i+'"]').innerHTML=F[i][v];fb.querySelector('[data-fit-k="'+i+'"]').innerHTML='<span class="ac-fitb ac-fitb--'+lab[0]+'">'+lab[1]+'</span>';c[lab[0]]++;});
      fb.querySelector('[data-fit-sum]').innerHTML='<b>'+(c.std+c.cfg)+' of 5</b> processes run on standard Odoo'+(c.cus?', <b>'+c.cus+'</b> needs a small customization.':', with no custom code.');}
    fb.addEventListener('change',fdraw);fdraw();}

  /* --- 4 journal entries --- */
  var je=document.querySelector('[data-je]');
  if(je){var O=J('ac-ops'),posted=[],ob=[].slice.call(je.querySelectorAll('[data-op]'));
    function jdraw(last){var e=last!=null?O[last]:null;
      je.querySelector('[data-je-name]').innerHTML=e?e[1]:'Nothing posted yet';
      je.querySelector('[data-je-entry]').innerHTML=e?'<thead><tr><th>Account</th><th class="ox-num">Debit</th><th class="ox-num">Credit</th></tr></thead><tbody>'+e[2].map(function(l){return '<tr class="is-new"><td>'+l[0]+'</td><td class="ox-num">'+(l[1]?inr(l[1]):'')+'</td><td class="ox-num">'+(l[2]?inr(l[2]):'')+'</td></tr>';}).join('')+'</tbody>':'<tbody><tr><td class="ox-empty">&larr; Press <b>Post</b> on any step to see the journal entry it creates.</td></tr></tbody>';
      var G={},order=[];posted.forEach(function(i){O[i][2].forEach(function(l){if(!G[l[0]]){G[l[0]]=0;order.push(l[0]);}G[l[0]]+=l[1]-l[2];});});
      var td=0,tc=0;var rows=order.map(function(a){var v=G[a];if(v>0)td+=v;else tc-=v;return '<tr><td>'+a+'</td><td class="ox-num">'+(v>0?inr(v):'')+'</td><td class="ox-num">'+(v<0?inr(-v):'')+'</td></tr>';}).join('');
      je.querySelector('[data-je-gl]').innerHTML='<thead><tr><th>Account</th><th class="ox-num">Debit</th><th class="ox-num">Credit</th></tr></thead><tbody>'+(rows||'<tr><td colspan="3" class="ox-muted">No lines yet.</td></tr>')+'</tbody><tfoot><tr><td><b>Total</b></td><td class="ox-num"><b>'+inr(td)+'</b></td><td class="ox-num"><b>'+inr(tc)+'</b></td></tr></tfoot>';
      je.querySelector('[data-je-check]').innerHTML=posted.length?'<span class="ac-ok">'+TICKS+' Balanced: debits equal credits</span>':'';
      ob.forEach(function(b,i){var p=posted.indexOf(i)>-1;b.classList.toggle('is-posted',p);b.querySelector('.ac-op-st').textContent=p?'Posted':'Post';});}
    var TICKS='&#10003;';
    je.addEventListener('click',function(e){var b=e.target.closest('[data-op]');if(b){var i=+b.getAttribute('data-op');if(posted.indexOf(i)<0)posted.push(i);jdraw(i);return;}
      if(e.target.closest('[data-je-reset]')){posted=[];jdraw(null);}});jdraw(null);}

  /* --- 6 bank reconciliation --- */
  var rc=document.querySelector('[data-rec]');
  if(rc){var L0=[{d:'Oct 14',l:'RTGS-SHREE DISTRIBUTORS',a:300000,p:'Shree Distributors',m:'INV/2026/00398',due:590000,k:'part'},
      {d:'Oct 14',l:'UPI/SUNRISE CLINICS/88120',a:619500,p:'Sunrise Clinics',m:'INV/2026/00411',due:619500,k:'full'},
      {d:'Oct 13',l:'NEFT-PIONEER PACKAGING',a:-89680,p:'Pioneer Packaging',m:'BILL/2026/10/0006',due:89680,k:'full'},
      {d:'Oct 13',l:'CHRG/SMS ALERT Q3',a:-118,p:'',m:'Bank Fees',due:118,k:'model'},
      {d:'Oct 12',l:'INT.COLL/SAVINGS SWEEP',a:2140,p:'',m:'',due:0,k:'none'}],L,sel;
    function rreset(){L=L0.map(function(x){var y={};for(var k in x)y[k]=x[k];return y;});sel=0;}
    function rdraw(){var n=L.filter(function(x){return x.ok;}).length;
      rc.querySelector('[data-rec-lines]').innerHTML=L.map(function(x,i){return '<li class="'+(i===sel?'is-sel ':'')+(x.ok?'is-ok':'')+'"><button type="button" data-rl="'+i+'"><small>'+x.d+'</small><b>'+x.l+'</b><span>'+(x.p||'&nbsp;')+'</span><em class="'+(x.a<0?'is-out':'')+'">'+inr(x.a)+'</em>'+(x.ok?'<i class="ac-rl-ok">&#10003;</i>':'')+'</button></li>';}).join('')+
        '<li class="ac-rl-sum">'+n+' of '+L.length+' reconciled</li>';
      var x=L[sel],p=rc.querySelector('[data-rec-panel]');
      if(x.ok){p.innerHTML='<p class="ac-rp-ok"><b>Reconciled</b>'+x.note+'</p>';return;}
      var sug=x.k==='none'?'<p class="ac-rp-none">No match found. Choose a rule:</p><p class="ac-rp-models"><button type="button" class="ox-sbtn" data-rm="Other Income">Interest received</button><button type="button" class="ox-sbtn" data-rm="Internal Transfers">Internal Transfers</button><button type="button" class="ox-sbtn" data-rm="Owner\'s Current Account">Owner\'s Current Account</button></p>':
        '<table class="ac-lines"><thead><tr><th>Account</th><th>Partner</th><th>Label</th><th class="ox-num">Amount</th></tr></thead><tbody>'+
        '<tr class="is-bank"><td>101402 Bank Suspense Account</td><td>'+(x.p||'')+'</td><td>'+x.l+'</td><td class="ox-num">'+inr(x.a)+'</td></tr>'+
        (x.k==='model'?'<tr><td>620000 Bank Fees</td><td></td><td>Bank Fees (reconciliation model)</td><td class="ox-num">'+inr(-x.a)+'</td></tr>':
         '<tr><td>'+(x.a>0?'121000 Accounts Receivable':'211000 Accounts Payable')+'</td><td>'+x.p+'</td><td><b>'+x.m+'</b></td><td class="ox-num">'+inr(-x.a)+'</td></tr>')+'</tbody></table>'+
        (x.k==='part'?'<p class="ac-rp-note">Partial payment: <b>'+inr(x.due-x.a)+'</b> stays open on '+x.m+'.</p>':'')+
        '<p class="ac-rp-btns"><button type="button" class="ox-pbtn" data-rv>Validate</button><span class="ox-sbtn">Reset</span><span class="ox-sbtn">To Check</span></p>';
      p.innerHTML='<p class="ac-rp-h"><b>'+x.l+'</b><span>'+x.d+' &middot; '+inr(x.a)+'</span></p><p class="ac-rp-tabs"><span class="is-on">'+(x.k==='none'?'Reconcile with a model':'Match Existing Entries')+'</span><span>Manual Operations</span></p>'+sug;}
    function rv(x,acc){x.ok=true;x.note=acc?' with <b>'+acc+'</b>.':(x.k==='model'?' with the <b>Bank Fees</b> model.':' against <b>'+x.m+'</b>'+(x.k==='part'?', now Partially Paid.':', now Paid.'));}
    rc.addEventListener('click',function(e){var b=e.target.closest('[data-rl]');if(b){sel=+b.getAttribute('data-rl');rdraw();return;}
      if(e.target.closest('[data-rv]')){rv(L[sel]);var nx=L.findIndex(function(x){return !x.ok;});if(nx>-1)sel=nx;rdraw();return;}
      var rm=e.target.closest('[data-rm]');if(rm){rv(L[sel],rm.getAttribute('data-rm'));var n2=L.findIndex(function(x){return !x.ok;});if(n2>-1)sel=n2;rdraw();return;}
      if(e.target.closest('[data-rec-all]')){var all=L.every(function(x){return x.ok;});if(all){rreset();}else{L.forEach(function(x){if(!x.ok&&x.k!=='none')rv(x);});var n3=L.findIndex(function(x){return !x.ok;});sel=n3>-1?n3:0;}
        rc.querySelector('[data-rec-all]').textContent=L.every(function(x){return x.ok;})?'Start over':'Reconcile all';rdraw();}});
    rreset();rdraw();}

  /* --- 7 decision tree --- */
  var tr=document.querySelector('[data-tree]');
  if(tr){var E=J('ac-ex'),eb=[].slice.call(tr.querySelectorAll('[data-ex]')),LAB={studio:'Studio',cfg:'Configuration',custom:'Customization',manual:'Do it by hand'};
    function tdraw(i){var e=E[i];tr.querySelectorAll('[data-tq]').forEach(function(q,k){var a=e[1][k];q.classList.toggle('is-on',a!==undefined);q.classList.toggle('is-off',a===undefined);
        q.querySelectorAll('[data-a]').forEach(function(x){x.classList.toggle('is-pick',x.getAttribute('data-a')===a);});});
      var k=tr.querySelector('[data-v-kind]');k.textContent=LAB[e[2]];k.className='ac-v-kind ac-fitb ac-fitb--'+e[2];tr.querySelector('[data-v-how]').innerHTML=e[3];tr.querySelector('[data-v-eff]').textContent='Typical effort: '+e[4];}
    eb.forEach(function(b){b.addEventListener('click',function(){press(eb,b);tdraw(+b.getAttribute('data-ex'));});});tdraw(0);}

  /* --- 8 trial balance check --- */
  var tb=document.querySelector('[data-tb]');
  if(tb){var fix=tb.querySelector('[data-tb-fix]');
    fix.addEventListener('click',function(){var g=tb.querySelector('tr.is-gap');var done=!!fix.getAttribute('data-done');
      if(!done){if(g){g.classList.remove('is-gap');g.classList.add('is-fixed');g.children[2].innerHTML='<span class="ac-type">Current Assets</span>';g.children[3].innerHTML='141000 Prepaid Expenses (advance to contractor)';}
        tb.querySelector('[data-tb-odoo]').innerHTML=inr(48216540);var d=tb.querySelector('[data-tb-diff]');d.innerHTML=inr(0);d.className='ac-grn';
        tb.querySelector('[data-tb-res]').innerHTML='<b>Books tie.</b> The &#8377; 12,480 in Suspense was an advance to a contractor. Ready for cut-over.';tb.querySelector('[data-tb-res]').className='ac-tb-res is-ok';fix.textContent='Show the original difference';fix.setAttribute('data-done','1');}
      else{var f=tb.querySelector('tr.is-fixed');if(f){f.classList.remove('is-fixed');f.classList.add('is-gap');f.children[2].innerHTML='<span class="ac-type">To be mapped</span>';f.children[3].innerHTML='&mdash;';}
        tb.querySelector('[data-tb-odoo]').innerHTML=inr(48204060);var d2=tb.querySelector('[data-tb-diff]');d2.innerHTML=inr(12480);d2.className='ac-red';
        tb.querySelector('[data-tb-res]').innerHTML='One ledger is still unmapped, so the books don&rsquo;t tie yet.';tb.querySelector('[data-tb-res]').className='ac-tb-res';fix.textContent='Map Suspense A/c and re-check';fix.removeAttribute('data-done');}});}

  /* --- 9 reports --- */
  var rp=document.querySelector('[data-rep-box]');
  if(rp){var cmp=rp.querySelector('[data-rep-cmp]'),rb=[].slice.call(rp.querySelectorAll('[data-rep]')),cur='pl',open={};
    var R={pl:{t:'Profit and Loss',c:['Sep 2026','Aug 2026'],r:[[0,'Revenue',[4126000,3812000],[['400000 Product Sales',[3986000,3702000]],['450000 Other Income',[140000,110000]]]],[0,'Costs of Revenue',[-2265000,-2128000],[['500000 Cost of Goods Sold',[-2265000,-2128000]]]],
          [1,'Gross Profit',[1861000,1684000]],[0,'Operating Expenses',[-1242000,-1196000],[['630000 Salary Expenses',[-842000,-820000]],['612000 Rent',[-180000,-180000]],['620000 Bank Fees',[-4200,-3900]],['600000 Expenses',[-215800,-192100]]]],
          [1,'Operating Income (or Loss)',[619000,488000]],[0,'Other Income',[21400,18200]],[0,'Other Expenses',[-38600,-41000]],[2,'Net Profit',[601800,465200]]]},
      bs:{t:'Balance Sheet',c:['Sep 30, 2026','Aug 31, 2026'],r:[[3,'ASSETS'],[0,'Bank and Cash Accounts',[5028530,4410200],[['101401 HDFC Current A/c',[4862300,4280000]],['101506 Cash',[42650,38900]],['101402 Bank Suspense Account',[123580,91300]]]],
          [0,'Receivables',[18640200,17920400]],[0,'Current Assets',[9480000,9122000]],[0,'Fixed Assets',[12650000,12890000]],[1,'Total ASSETS',[45798730,44342600]],
          [3,'LIABILITIES'],[0,'Payables',[7215400,6984000]],[0,'Current Liabilities (GST, TDS, salaries)',[3912000,3770000]],[1,'Total LIABILITIES',[11127400,10754000]],
          [3,'EQUITY'],[0,'Capital',[20000000,20000000]],[0,'Current Year Unallocated Earnings',[3618200,3016400]],[0,'Previous Years Earnings',[11053130,10572200]],[1,'Total EQUITY',[34671330,33588600]],[2,'LIABILITIES + EQUITY',[45798730,44342600]]]},
      ar:{t:'Aged Receivable',c:['At Date','1-30','31-60','61-90','91-120','Older','Total'],aged:1,r:[['Nair Textiles',[0,566400,0,0,0,0]],['Shree Distributors',[290000,0,0,0,0,0]],['Sunrise Clinics',[619500,0,0,0,0,0]],
          ['Orbit Motors Pvt Ltd',[0,0,412000,0,0,0]],['Indus Exports',[0,0,0,184000,0,96000]]]},
      tax:{t:'Tax Report',c:['Sep 2026','Aug 2026'],r:[[3,'OUTPUT TAX (GSTR-1)'],[0,'Output CGST 9%',[214200,198400]],[0,'Output SGST 9%',[214200,198400]],[0,'Output IGST 18%',[328500,301100]],[1,'Total output tax',[756900,697900]],
          [3,'INPUT TAX CREDIT (GSTR-2B)'],[0,'Input CGST 9%',[-189600,-176300]],[0,'Input SGST 9%',[-189600,-176300]],[0,'Input IGST 18%',[-245250,-221800]],[1,'Total input credit',[-624450,-574400]],[2,'Net GST payable (GSTR-3B)',[132450,123500]]]},
      ex:{t:'Executive Summary',c:['Sep 2026','Aug 2026'],r:[[3,'CASH'],[0,'Cash received',[3940000,3612000]],[0,'Cash spent',[-3322000,-3190000]],[1,'Cash surplus',[618000,422000]],[3,'PROFITABILITY'],[0,'Gross profit margin',['45.1%','44.2%']],[0,'Net profit margin',['14.6%','12.2%']],
          [3,'PERFORMANCE'],[0,'Average debtors days',['41','46']],[0,'Average creditors days',['38','37']],[0,'Return on investments',['1.7%','1.4%']]]}};
    function v(x){return typeof x==='string'?x:inr(x,false);}
    function pct(a,b){if(typeof a==='string'||!b)return '';var p=(a-b)/Math.abs(b)*100;return '<span class="'+(p>=0?'ac-grn':'ac-red')+'">'+(p>=0?'+':'')+p.toFixed(1)+'%</span>';}
    function rdraw(){var d=R[cur],c=cmp.checked;rp.querySelector('[data-rep-title]').textContent=d.t;cmp.parentNode.style.visibility=d.aged?'hidden':'visible';var h,b='';
      if(d.aged){h='<thead><tr><th></th>'+d.c.map(function(x){return '<th class="ox-num">'+x+'</th>';}).join('')+'</tr></thead>';var T=[0,0,0,0,0,0];
        d.r.forEach(function(r){var s=r[1].reduce(function(a,x){return a+x;},0);r[1].forEach(function(x,i){T[i]+=x;});b+='<tr><td>'+r[0]+'</td>'+r[1].map(function(x){return '<td class="ox-num">'+(x?inr(x,false):'')+'</td>';}).join('')+'<td class="ox-num"><b>'+inr(s,false)+'</b></td></tr>';});
        b+='<tr class="is-l2"><td>Total Aged Receivable</td>'+T.map(function(x){return '<td class="ox-num">'+inr(x,false)+'</td>';}).join('')+'<td class="ox-num">'+inr(T.reduce(function(a,x){return a+x;},0),false)+'</td></tr>';}
      else{h='<thead><tr><th></th><th class="ox-num">'+d.c[0]+'</th>'+(c?'<th class="ox-num">'+d.c[1]+'</th><th class="ox-num">%</th>':'')+'</tr></thead>';
        d.r.forEach(function(r,i){if(r[0]===3){b+='<tr class="is-sec"><td colspan="'+(c?4:2)+'">'+r[1]+'</td></tr>';return;}var kids=r[3],key=cur+i;
          b+='<tr class="is-l'+r[0]+(kids?' is-fold':'')+'"'+(kids?' data-fold="'+key+'" tabindex="0"':'')+'><td>'+(kids?'<span class="ac-caret">'+(open[key]?'&#9662;':'&#9656;')+'</span>':'')+r[1]+'</td><td class="ox-num">'+v(r[2][0])+'</td>'+(c?'<td class="ox-num">'+v(r[2][1])+'</td><td class="ox-num">'+pct(r[2][0],r[2][1])+'</td>':'')+'</tr>';
          if(kids&&open[key])kids.forEach(function(k){b+='<tr class="is-kid"><td>'+k[0]+'</td><td class="ox-num">'+v(k[1][0])+'</td>'+(c?'<td class="ox-num">'+v(k[1][1])+'</td><td class="ox-num">'+pct(k[1][0],k[1][1])+'</td>':'')+'</tr>';});});}
      rp.querySelector('[data-rep-t]').innerHTML=h+'<tbody>'+b+'</tbody>';}
    rb.forEach(function(x){x.addEventListener('click',function(){press(rb,x);cur=x.getAttribute('data-rep');rdraw();});});
    cmp.addEventListener('change',rdraw);
    rp.addEventListener('click',function(e){var f=e.target.closest('[data-fold]');if(f){var k=f.getAttribute('data-fold');open[k]=!open[k];rdraw();}});
    rp.addEventListener('keydown',function(e){if(e.key==='Enter'){var f=e.target.closest('[data-fold]');if(f){var k=f.getAttribute('data-fold');open[k]=!open[k];rdraw();}}});
    open.pl0=true;rdraw();}

  /* --- 10 integrations --- */
  var il=document.querySelector('.ac-int-log');
  if(il){var I=J('ac-int'),ib=[].slice.call(document.querySelectorAll('[data-int]'));
    function idraw(i){var x=I[i];il.querySelector('[data-int-name]').innerHTML=x[0];il.querySelector('[data-int-dir]').textContent={In:'Into Odoo',Out:'Out of Odoo',Both:'Both ways'}[x[3]];il.querySelector('[data-int-freq]').textContent=x[2];
      il.querySelector('[data-int-log]').innerHTML=x[4].map(function(l,k){return '<li style="--k:'+k+'"><small class="mono">'+l[0]+'</small><span>'+l[1]+'</span></li>';}).join('');}
    ib.forEach(function(b){b.addEventListener('click',function(){press(ib,b);idraw(+b.getAttribute('data-int'));});});idraw(0);}

  /* --- 11 parallel run + UAT --- */
  var ub=document.querySelector('[data-uatbox]');
  if(ub){var cbx=[].slice.call(ub.querySelectorAll('[data-uat]'));
    function udraw(){var n=cbx.filter(function(c){return c.checked;}).length,p=Math.round(n/cbx.length*100);
      ub.querySelector('[data-uat-pct]').textContent=p+'%';ub.querySelector('[data-uat-bar]').style.width=p+'%';ub.classList.toggle('is-ready',p===100);
      ub.querySelector('[data-uat-res]').innerHTML=p===100?'<b>Ready for go-live.</b> Every role has signed off.':(cbx.length-n)+' scenario'+(cbx.length-n===1?'':'s')+' left before go-live.';}
    ub.addEventListener('change',udraw);udraw();}

  /* --- 12 before / after --- */
  var cg=document.querySelector('[data-chg]');
  if(cg){var cbs=[].slice.call(cg.querySelectorAll('[data-chg-m]'));
    function gdraw(m){cg.classList.toggle('is-after',m==='a');cg.querySelectorAll('.ac-kl li').forEach(function(li){var b=+li.getAttribute('data-b'),a=+li.getAttribute('data-a'),val=m==='a'?a:b;
        li.querySelector('.ac-k-bar i').style.width=(val/b*100)+'%';li.querySelector('.ac-k-v').textContent=val;});
      cg.querySelector('[data-chg-note]').innerHTML=m==='a'?'Month end in <b>4 days</b> instead of 12, and invoices go out the day goods leave.':'Typical starting point: Tally, Excel and a lot of re-typing.';}
    cbs.forEach(function(b){b.addEventListener('click',function(){press(cbs,b);gdraw(b.getAttribute('data-chg-m'));});});gdraw('b');}

  /* --- 13 maturity --- */
  var mt=document.querySelector('[data-mat]');
  if(mt){var ans={};
    mt.addEventListener('click',function(e){var b=e.target.closest('[data-m]');if(!b)return;var k=b.getAttribute('data-m');ans[k]=+b.getAttribute('data-v');
      press([].slice.call(mt.querySelectorAll('[data-m="'+k+'"]')),b);
      var n=Object.keys(ans).length,s=Object.keys(ans).reduce(function(a,x){return a+ans[x];},0),score=Math.round(s/10*100);
      mt.querySelector('[data-mat-score]').textContent=n?score:0;mt.querySelector('[data-mat-dial]').style.setProperty('--p',n?score:0);
      mt.querySelector('[data-mat-txt]').innerHTML=n<5?'Keep going: '+(5-n)+' area'+(5-n===1?'':'s')+' left.':score<40?'<b>Ready for a better system.</b> Your team is doing by hand what Odoo does automatically. The move will pay back within the first year.':
        score<75?'<b>Partly there.</b> The basics work, but re-entry and month-end catch-up still cost days. Odoo closes those gaps.':'<b>Well run already.</b> Odoo will mainly save time on reconciliation and give you live reports.';});}
})();
</script>
'''

CTA = ("Let's Build Your Accounting System in Odoo",
       "Tell us how you invoice, pay, reconcile and close today. We&rsquo;ll show the same month in Odoo Accounting.")
