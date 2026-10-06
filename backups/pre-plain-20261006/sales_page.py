"""
Odoo Sales page (odoo-sales.html). Every section is modelled on a real Odoo 20
screen (demo.odoo.com): quotation form, customer portal, Discuss, Settings,
chatter, Appointments. Section layouts are its own; none repeat the CRM page.
Shared Odoo look: dist/assets/odoo-ui.css. Page styles: dist/assets/sales.css.

hero(g) and build(g) get the build script's globals.
"""
import json

from crm_explorer import ic, SEARCH, FUNNEL, V_KANBAN, V_LIST, V_GRAPH

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CROSS = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
TRUCK = ic('<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>', 18, 1.7)
INVOICE = ic('<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>', 18, 1.7)
CARD = ic('<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M3 10h18"/>', 18, 1.7)
DOC = ic('<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>', 18, 1.7)
BOT = '<span class="ox-av is-bot">U</span>'


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
    out = ",".join(groups + [last3]) if rest or groups else last3
    return "&#8377; " + out + (".00" if dec else "")


def head(eyebrow, title, sub="", cls=""):
    return ('<div class="sl-head%s"><p class="sl-eyebrow mono">%s</p><h2 class="sl-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="sl-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="sl-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


def odoo_nav(app_icon, app, menus):
    return ('<div class="ox-nav"><span class="ox-app">%s<b>%s</b></span>%s<span class="ox-nav-r"><span class="ox-company">Your Company</span>'
            '<span class="ox-av" style="--c:#6B5B95">Y</span></span></div>' % (app_icon, app, "".join('<span class="ox-menu">%s</span>' % m for m in menus)))


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">Sales</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["Quotes in minutes", "Signed &amp; paid online", "Invoices from what you deliver"])
    copy = ('<div class="sl-hero-copy">%s<p class="sl-eyebrow mono">ODOO SALES IMPLEMENTATION</p>'
            '<h1 class="sl-h1">Salesforce Implementation Services <span>Customized with Odoo</span></h1>'
            '<p class="sl-lead">We implement Odoo Sales around the way your team quotes, sells and invoices, so a quotation becomes an order, a delivery '
            'and an invoice in one connected flow, with no re-typing between teams.</p><ul class="sl-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Discuss Odoo Sales %s</a>'
            '<a href="#explore" class="btn btn-ghost">Try the quote-to-cash demo</a></div></div>' % (crumb, points, g["ARROW"]))
    lines = [("Ergo task chair", "Mesh back, 4D armrests", 24, 8450), ("Height-adjustable desk", "Dual motor, 160 x 80 cm", 12, 32900),
             ("Installation &amp; setup", "On-site, 2 technicians", 1, 18000)]
    rows = "".join('<tr><td><b>%s</b><small>%s</small></td><td class="ox-num">%d.00</td><td class="ox-num">%s</td><td><span class="sl-tax">18%%</span></td>'
                   '<td class="ox-num">%s</td></tr>' % (n, d, q, inr(p), inr(q * p)) for n, d, q, p in lines)
    untaxed = sum(q * p for _n, _d, q, p in lines)
    # the customer's view: the printed quotation, accepted with an online signature
    sign = ('<svg class="sl-px-sig" viewBox="0 0 220 70" aria-hidden="true"><path d="M8 48c10-26 24-40 30-30s-14 36-4 36 18-30 26-30-6 26 4 26 14-22 22-22-4 20 6 20 12-18 20-26'
            ' M96 50c4-10 12-18 18-14s-6 16 2 16 14-14 22-16c6-2 2 12 10 12s16-14 26-18 M150 30c20-6 44-8 62-4" fill="none" stroke="#1F3A8A" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    doc = ('<div class="sl-hero-doc sl-px" aria-label="Example quotation accepted online"><div class="sl-px-back" aria-hidden="true"></div><article class="sl-px-paper">'
           '<header class="sl-px-top"><p class="sl-px-co">YOUR<b>COMPANY</b><small>12, Industrial Estate, Guindy, Chennai 600032 &middot; GSTIN 33AAACY0000A1Z5</small></p>'
           '<p class="sl-px-kind"><small>Quotation</small><b>S00482</b></p></header>'
           '<div class="sl-px-meta"><p><small>Customer</small><b>Bluebay Retail Pvt Ltd</b>4th Floor, Prestige Tower, Bengaluru 560001<br>GSTIN 29AABCB1234F1Z5</p>'
           '<dl><div><dt>Quotation Date</dt><dd>Oct 14, 2026</dd></div><div><dt>Expiration</dt><dd>Oct 31, 2026</dd></div><div><dt>Salesperson</dt><dd>Anita Rao</dd></div></dl></div>'
           '<table class="sl-px-t"><thead><tr><th>Description</th><th>Qty</th><th>Unit Price</th><th>Amount</th></tr></thead><tbody>%s</tbody></table>'
           '<div class="sl-px-tot"><span>Untaxed Amount</span><b>%s</b><span>GST 18%%</span><b>%s</b><span class="is-total">Total</span><b class="is-total">%s</b></div>'
           '<footer class="sl-px-foot"><div class="sl-px-sign"><small>Accepted on behalf of Bluebay Retail</small>%s<span><b>Rohan Shah</b> &middot; Oct 14, 2026, 11:42</span></div>'
           '<div class="sl-px-stamp"><b>PAID</b><small>UPI &middot; Ref 4417 2290</small></div></footer></article>'
           '<p class="sl-px-tag">%s Sales order confirmed &middot; delivery scheduled for Oct 17</p></div>'
           % ("".join('<tr><td><b>%s</b><small>%s</small></td><td>%d</td><td>%s</td><td>%s</td></tr>' % (n, d, q, inr(p), inr(q * p)) for n, d, q, p in lines),
              inr(untaxed), inr(untaxed * 0.18), inr(untaxed * 1.18), sign, TRUCK))
    return '<section class="sl-hero">%s%s</section>' % (copy, doc)


# ------------------------------------------------------------------ sections
def build(g):
    out = ""
    sales_icon = g["TILE_ICONS"][2]

    # 1 ---- ready? the messages your team sends today (Odoo Discuss look)
    msgs = [("Priya (Sales)", "#B5567E", "10:02", "Which price did we give Bluebay last time? I can't find the old quote."),
            ("Karthik (Warehouse)", "#3E7CB1", "10:15", "Who confirmed 40 chairs for Orbit Motors? We only have 26 in stock."),
            ("Divya (Accounts)", "#4C9F70", "10:31", "Invoice for Kaveri Foods: was the discount 10% or 12%? The order email says one thing, the quote another."),
            ("Rahul (Sales)", "#8E4F83", "10:48", "Customer wants the signed copy again. Does anyone have the final PDF?"),
            ("Anita (Manager)", "#C98600", "11:05", "Can someone send me this month's confirmed orders? Need it before the review.")]
    feed = "".join('<div class="sl-chat-msg"><span class="ox-av" style="--c:%s">%s</span><div><p><b>%s</b><small>%s</small></p><p>%s</p></div></div>'
                   % (c, n[0], n, t, x) for n, c, t, x in msgs)
    signs = ["Prices and discounts live in old emails and spreadsheets", "Orders are confirmed without checking stock",
             "Accounts re-types orders into invoices", "Nobody can find the latest signed quote", "Reports are built by hand every month"]
    out += sec('<div class="sl-ready"><div>%s<ul class="sl-signs">%s</ul><p class="sl-note">If two or more sound familiar, your sales process is ready for one connected system.</p></div>'
               '<div class="sl-chat ox-solo" aria-label="Example team chat showing common sales problems"><div class="sl-chat-head"><span class="sl-chat-hash">#</span><b>sales-team</b><small>5 new messages</small></div>%s'
               '<div class="sl-chat-input">Message #sales-team&hellip;</div></div></div>'
               % (head("READINESS CHECK", "Is Your Sales Process Ready for a More Connected System?",
                       "Most teams don't notice the cost of disconnected sales until it shows up in messages like these."),
                  "".join('<li>%s%s</li>' % (CROSS, s) for s in signs), feed), "sl-sec--ready")

    # 2 ---- how we implement: steps + Odoo Sales settings
    steps = [("Map your quote-to-cash", "We sit with sales, warehouse and accounts to map how you quote, approve, deliver and invoice today."),
             ("Switch on what you need", "We enable only the Odoo Sales features your process uses: pricelists, signatures, templates, delivery rules."),
             ("Connect the other teams", "Orders reserve stock in Inventory and invoices flow to Accounting, set to your invoicing policy."),
             ("Train and go live", "Your team practises on its own products and customers before the switch-over.")]
    st = "".join('<li><span class="sl-step-n mono">%02d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i + 1, t, x) for i, (t, x) in enumerate(steps))
    settings = [("Quotations &amp; Orders", [("Quotation Templates", "Reuse standard offers with products, terms and optional items", True),
                                              ("Online Signature", "Customers sign the quotation online to confirm", True),
                                              ("Online Payment", "Ask for a payment or deposit when they sign", True)]),
                ("Pricing", [("Discounts", "Grant discounts on sales order lines", True),
                             ("Pricelists", "Customer-specific prices, dealer tiers and seasonal offers", True)]),
                ("Shipping &amp; Invoicing", [("Delivery Methods", "Compute shipping costs and ship with your carriers", False),
                                              ("Invoice what is delivered", "Invoices follow delivered quantities, not ordered ones", True)])]
    blocks = ""
    for title, opts in settings:
        items = "".join('<label class="sl-set"><input type="checkbox"%s><span class="sl-chk" aria-hidden="true">%s</span><span><b>%s</b><small>%s</small></span></label>'
                        % (" checked" if on else "", TICK, n, d) for n, d, on in opts)
        blocks += '<div class="sl-set-group"><h4>%s</h4><div class="sl-set-grid">%s</div></div>' % (title, items)
    out += sec('<div class="sl-impl"><div>%s<ol class="sl-steps">%s</ol></div><div class="ox ox-settings">%s'
               '<div class="ox-cp"><div class="ox-cp-l"><span class="ox-new">Save</span><span class="ox-sbtn">Discard</span><span class="ox-crumb">Settings</span></div></div>'
               '<div class="sl-set-body">%s</div></div></div>'
               % (head("HOW WE IMPLEMENT", "How Can Unisas Implement Odoo Around Your Sales Process?",
                       "We don't hand you a blank system. We map your process first, then configure Odoo's own settings to match it."),
                  st, odoo_nav(sales_icon, "Sales", ["Orders", "Products", "Reporting", "Configuration"]), blocks), "sl-sec--impl")

    # 3 ---- what Odoo Sales does: interactive quote-to-cash explorer
    feats = [("Quotations", "Branded quotes from templates, with optional products and validity dates."),
             ("Online sign &amp; pay", "Customers accept and pay from a secure link, and the order confirms itself."),
             ("Pricelists &amp; discounts", "The right price for every customer, applied automatically."),
             ("Sales analysis", "Revenue by product, customer and salesperson, live from confirmed orders.")]
    out += sec(head("WHAT ODOO SALES DOES", "What Can Odoo Sales Do for Your Business?",
                    "Odoo Sales takes you from quotation to confirmed order to invoice in one place. Try it: open a quotation, change a quantity, send it, "
                    "preview what the customer sees, and confirm the order.", "is-center")
               + explorer(sales_icon)
               + '<ul class="sl-feats">%s</ul>' % "".join('<li><b>%s</b><span>%s</span></li>' % f for f in feats), "sl-sec--explore", "explore")

    # 4 ---- connected documents: SO -> delivery -> invoice -> payment
    docs = [("sales", "#EE8A3C", "Sales", "S00482", "Sales Order", ["Bluebay Retail Pvt Ltd", "3 products &middot; " + inr(605080)], ["Quotation", "Sent", "Sales Order"],
             "Confirmed when the customer signs. Stock is reserved straight away."),
            ("inv", "#5DC1AA", "Inventory", "WH/OUT/00031", "Delivery", ["Chennai warehouse", "37 units &middot; 3 lines"], ["Waiting", "Ready", "Done"],
             "Created automatically from the order, picked and shipped by the warehouse."),
            ("acc", "#8E4F83", "Accounting", "INV/2026/00042", "Customer Invoice", ["GST 18% &middot; e-Invoice ready", "Due in 30 days"], ["Draft", "Posted", "Paid"],
             "Raised from what was delivered, with the right taxes, then posted."),
            ("pay", "#1E9E4F", "Payments", "PAY/00117", "Payment", ["UPI &middot; Bank reconciled", inr(605080)], ["Draft", "In Payment", "Paid"],
             "Matched to the invoice when it lands in the bank. The order shows as fully paid.")]
    cards = ""
    for k, c, app, num, kind, facts, stages, txt in docs:
        sb = "".join('<span class="ox-sb" data-i="%d">%s</span>' % (i, s) for i, s in enumerate(stages))
        cards += ('<li class="sl-doc" style="--c:%s" data-doc="%s"><div class="sl-doc-card ox-solo"><p class="sl-doc-app"><i></i>%s</p><h3>%s</h3><small>%s</small>'
                  '<ul>%s</ul><span class="ox-sbar is-mini">%s</span><span class="sl-doc-stamp">Done</span></div><p class="sl-doc-txt">%s</p></li>'
                  % (c, k, app, num, kind, "".join("<li>%s</li>" % f for f in facts), sb, txt))
    out += sec(head("ONE CONNECTED FLOW", "How Does Odoo Connect Your Sales, Inventory and Accounting?",
                    "Every step creates the next document for you. Press play to follow one order from signature to payment.", "is-center")
               + '<div class="sl-chain"><button type="button" class="sl-play" data-chain-play>%s<span>Play the flow</span></button><ol class="sl-docs">%s</ol></div>'
               % (ic('<path d="M7 5l12 7-12 7z"/>', 16, 2), cards), "sl-sec--chain")

    # 5 ---- automation: chatter of one order
    events = [("08:12", "Quotation sent", "S00482 emailed to Rohan Shah from the <b>Dealer offer</b> template.", "mail"),
              ("Day 3", "Automatic reminder", "No reply yet, so a polite follow-up email went out by itself.", "bell"),
              ("Day 4", "Signed &amp; paid online", "Rohan signed and paid a 30% deposit via UPI. <span class='sl-track'>Status: Quotation &rarr; <b>Sales Order</b></span>", "sign"),
              ("Day 4", "Delivery created", "WH/OUT/00031 created and stock reserved in the Chennai warehouse.", "truck"),
              ("Day 6", "Invoice raised", "Delivered quantities invoiced as INV/2026/00042 and emailed with the e-Invoice IRN.", "inv"),
              ("Day 36", "Payment reminder", "Balance not received by the due date, so follow-up level 1 was sent.", "bell"),
              ("Day 38", "Paid &amp; reconciled", "Bank statement matched to the invoice. <span class='sl-track'>Invoice Status: <b>Paid</b></span>", "check")]
    eic = {"mail": ic('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', 15), "bell": ic('<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/>', 15),
           "sign": ic('<path d="M4 18c3-4 5-11 8-11 2 0 0 7 3 7 1.5 0 2.5-2 5-2"/><path d="M4 21h16"/>', 15), "truck": ic('<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>', 15),
           "inv": ic('<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/>', 15), "check": ic('<path d="M5 13l4 4L19 7"/>', 15)}
    log = "".join('<li class="sl-ev sl-ev--%s"><span class="sl-ev-ic">%s</span><div><p class="sl-ev-head"><b>Unisas Automation</b><small>%s</small></p><p class="sl-ev-title">%s</p><p>%s</p></div></li>'
                  % (k, eic[k], t, h, x) for t, h, x, k in events)
    out += sec('<div class="sl-auto">%s<div class="sl-chatter ox-solo"><div class="ox-ch-btns"><span class="ox-pbtn">Send message</span><span class="ox-sbtn">Log note</span><span class="ox-sbtn">Activity</span></div>'
               '<p class="ox-ch-sep">S00482 &middot; Bluebay Retail</p><ol class="sl-events">%s</ol></div></div>'
               % (head("AUTOMATION", "Which Sales Processes Can Unisas Automate Using Odoo?",
                       "This is the history of one order in Odoo. Nobody on your team had to do any of these steps by hand; Unisas sets up the rules that do them."), log),
               "sl-sec--auto")

    # 6 ---- customisation: branded quotation PDF with callouts
    pins = [("Your branding", "Logo, colours, fonts and layout on every quotation, order and invoice."),
            ("Custom fields", "Customer PO number, GSTIN, project code or any field your team needs."),
            ("Approval rules", "Discounts above your limit wait for a manager before the quote can be sent."),
            ("Product details", "Images, specs and optional add-ons so customers can upsell themselves."),
            ("Pay by UPI", "A payment QR and your bank details printed on the document.")]
    pin_list = "".join('<li data-pin="%d" tabindex="0"><span class="sl-pin">%d</span><div><b>%s</b><span>%s</span></div></li>' % (i + 1, i + 1, t, x) for i, (t, x) in enumerate(pins))
    pdf = ('<div class="sl-pdf" aria-hidden="true">'
           '<div class="sl-pdf-top"><span class="sl-pdf-logo">YOUR<b>LOGO</b></span><span class="sl-pdf-co">Your Company Pvt Ltd<br>GSTIN 33ABCDE1234F1Z5</span><span class="sl-pin" data-pin="1">1</span></div>'
           '<h4>Quotation # S00482</h4>'
           '<div class="sl-pdf-meta"><span><small>Quotation Date</small>01/10/2026</span><span><small>Customer PO</small>BB-PO-7781</span><span><small>Customer GSTIN</small>33AAACB4421K1ZQ</span><span class="sl-pin" data-pin="2">2</span></div>'
           '<div class="sl-pdf-warn"><b>Approval needed:</b> 15% discount is above your 10% limit.<span class="sl-pin" data-pin="3">3</span></div>'
           '<table><tr><th></th><th>Description</th><th>Qty</th><th>Amount</th></tr>'
           '<tr><td><i class="sl-pdf-img"></i></td><td>Ergo task chair<small>Mesh back, 4D armrests</small></td><td>24</td><td>' + inr(202800) + '</td></tr>'
           '<tr><td><i class="sl-pdf-img is-b"></i></td><td>Height-adjustable desk<small>Dual motor, 160 x 80 cm</small></td><td>12</td><td>' + inr(394800) + '</td></tr>'
           '<tr class="is-opt"><td></td><td>Optional: monitor arm<small>Add to order</small></td><td>12</td><td>' + inr(54000) + '</td></tr></table>'
           '<span class="sl-pin is-row" data-pin="4">4</span>'
           '<div class="sl-pdf-foot"><span class="sl-pdf-qr"></span><span><b>Scan to pay by UPI</b><br>HDFC Bank &middot; A/c 50200012345678</span><span class="sl-pin" data-pin="5">5</span></div></div>')
    out += sec('<div class="sl-custom">%s<div class="sl-custom-grid"><ol class="sl-pins">%s</ol>%s</div></div>'
               % (head("CUSTOMISATION", "How Can Unisas Customize Odoo Sales for Your Business?",
                       "We tailor documents, fields and rules with upgrade-safe changes, so Odoo works the way your customers and accountants expect. Hover a point to find it on the quotation.", "is-center"),
                  pin_list, pdf), "sl-sec--custom")

    # 7 ---- what's included: a quotation from Unisas (customer portal look)
    scope = [("Setup &amp; configuration", [("Sales process mapping workshop", "Quote, approval, delivery and invoicing flow agreed with your team"),
                                             ("Products, variants &amp; pricelists", "Your catalogue, units and customer-specific prices"),
                                             ("Quotation templates &amp; documents", "Branded quotation, order and invoice layouts"),
                                             ("Approval &amp; discount rules", "Limits per salesperson or team")]),
             ("Data &amp; integrations", [("Customer &amp; product import", "From Excel, Tally or your current system"),
                                           ("Inventory &amp; Accounting link", "Stock reservation and invoicing policy set up"),
                                           ("Online signature &amp; payment", "UPI / card gateway connected to the customer portal")]),
             ("Training &amp; support", [("Role-based training", "Sales, warehouse and accounts trained on their own data"),
                                          ("Go-live &amp; hypercare", "On-hand support through the first weeks")])]
    body = ""
    for title, items in scope:
        body += '<tr class="is-section"><td colspan="3">%s</td></tr>' % title
        body += "".join('<tr><td>%s<small>%s</small></td><td>1</td><td><span class="sl-incl">%sIncluded</span></td></tr>' % (n, d, TICK) for n, d in items)
    out += sec('<div class="sl-scope">%s<div class="sl-portal ox-solo"><aside class="sl-portal-side"><p class="sl-portal-big">Fixed price</p><small>Agreed after discovery</small>'
               '<a href="#get-demo" class="sl-portal-btn" data-svc-cta="implementation">Request your quotation</a><span class="sl-portal-btn is-ghost">Download</span>'
               '<div class="sl-portal-who"><span class="ox-av" style="--c:#714B67">U</span><span><b>Unisas</b><small>Your Odoo partner</small></span></div></aside>'
               '<div class="sl-portal-doc"><div class="sl-portal-head"><small>Quotation for <b>Your Company</b></small><h3>Odoo Sales Implementation</h3><small>Scope of a standard rollout</small></div>'
               '<table><thead><tr><th>Description</th><th>Qty</th><th></th></tr></thead><tbody>%s</tbody></table></div></div></div>'
               % (head("WHAT'S INCLUDED", "What Does an Odoo Sales Implementation with Unisas Include?",
                       "Here is our scope written the way you'll receive it: as an Odoo quotation you can review and sign online."), body), "sl-sec--scope")

    # 8 ---- business models: mini documents
    models = [("B2B &amp; wholesale", "Dealer tiers, volume breaks and credit limits on every order.", "Pricelist", "Dealer tier 2 &middot; &minus;12%", "S00517 &middot; 120 units"),
              ("B2C &amp; eCommerce", "Website orders flow in paid, ready to pick and invoice.", "Website order", "Paid via UPI", "S00521 &middot; online"),
              ("Subscriptions", "Recurring plans that renew and invoice themselves.", "Recurring", "Monthly &middot; next invoice Nov 1", "SUB/0042 &middot; active"),
              ("Rentals", "Rental periods, pickup and return tracked on the order.", "Rental period", "Oct 05 &rarr; Oct 12", "S00498 &middot; pickup today"),
              ("Projects &amp; services", "Milestone or timesheet billing for service work.", "Invoicing", "Milestones 30 / 40 / 30", "S00503 &middot; 2 of 3 billed"),
              ("Made to order", "Orders that trigger manufacturing or purchasing.", "Route", "Manufacture &middot; MO/00213", "S00509 &middot; in production")]
    cards = "".join('<li><div class="sl-mdoc ox-solo" aria-hidden="true"><span class="sl-mdoc-fold"></span><small>%s</small><b>%s</b><span>%s</span></div><h3>%s</h3><p>%s</p></li>'
                    % (k, v, ref, t, x) for t, x, k, v, ref in models)
    out += sec(head("BUSINESS MODELS", "Can Odoo Sales Support Different Business Models?",
                    "Yes. The same Sales app handles very different ways of selling, and many businesses run more than one at once.", "is-center")
               + '<ul class="sl-models">%s</ul>' % cards, "sl-sec--models")

    # 9 ---- benefits: before / after lanes
    before = [("Quote", "Built in Excel, emailed as PDF"), ("Approve", "Chased over WhatsApp"), ("Order", "Re-typed for the warehouse"), ("Invoice", "Re-typed again at month end")]
    after = [("Quote", "From a template in minutes"), ("Sign &amp; pay", "Customer accepts online"), ("Deliver", "Order already in the warehouse"), ("Invoice", "Raised from what was delivered")]
    lane = lambda steps, cls: '<ol class="sl-lane %s">%s</ol>' % (cls, "".join('<li><b>%s</b><span>%s</span></li>' % s for s in steps))
    bens = [("Faster quotes", "Templates and pricelists cut quoting from hours to minutes."), ("No double entry", "One order feeds delivery and invoicing."),
            ("Promises you can keep", "Salespeople see stock before they confirm."), ("Faster payment", "Online signature, payment links and reminders."),
            ("Fewer billing errors", "Invoices match what was actually delivered."), ("Live numbers", "Sales analysis without month-end spreadsheets.")]
    out += sec(head("BENEFITS", "What Business Benefits Can You Expect from Odoo Sales Implementation?",
                    "The biggest change is the number of times the same order is handled by hand.", "is-center")
               + '<div class="sl-lanes"><p class="sl-lane-label mono">TODAY</p>%s<p class="sl-lane-label mono is-after">WITH ODOO SALES</p>%s</div>' % (lane(before, "is-before"), lane(after, "is-after"))
               + '<ul class="sl-bens">%s</ul>' % "".join('<li>%s<div><b>%s</b><span>%s</span></div></li>' % (TICK, t, x) for t, x in bens), "sl-sec--bens")

    # 10 ---- why Unisas: comparison table
    rows = [("Starting point", "A generic demo database", "Your products, prices and customers from week one"),
            ("Customisation", "Heavy custom code to copy old habits", "Standard Odoo first; upgrade-safe changes only where needed"),
            ("Other teams", "Sales goes live alone", "Inventory and Accounting connected in the same project"),
            ("Training", "One generic session", "Role-based training for sales, warehouse and accounts"),
            ("After go-live", "Ticket queue", "Hypercare with the consultants who built it")]
    trs = "".join('<tr><th scope="row">%s</th><td>%s%s</td><td>%s%s</td></tr>' % (a, CROSS, b, TICK, c) for a, b, c in rows)
    out += sec(head("WHY UNISAS", "Why Choose Unisas for Odoo Sales Implementation?",
                    "What changes when an implementation partner starts from your sales process instead of the software.", "is-center")
               + '<div class="sl-compare-wrap"><table class="sl-compare"><thead><tr><th></th><th scope="col">A typical rollout</th><th scope="col"><span class="sl-us">Unisas</span></th></tr></thead><tbody>%s</tbody></table></div>' % trs,
               "sl-sec--why")

    # 11 ---- how we start: steps + Odoo Appointments booking
    start = [("Book a discovery call", "30 minutes with an Odoo consultant to understand how you sell today."),
             ("Fit-GAP workshop", "We map your quote-to-cash flow against standard Odoo Sales and list any gaps."),
             ("Fixed-scope proposal", "A clear scope, timeline and price, sent as an Odoo quotation you can sign online.")]
    sst = "".join('<li><span class="sl-step-n mono">%02d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i + 1, t, x) for i, (t, x) in enumerate(start))
    days = [("Mon", "05"), ("Tue", "06"), ("Wed", "07"), ("Thu", "08"), ("Fri", "09")]
    slots = ["10:00", "11:30", "14:00", "15:30", "17:00"]
    dbtn = "".join('<button type="button" class="sl-day%s" aria-pressed="%s"><small>%s</small><b>%s</b></button>' % (" is-on" if i == 1 else "", "true" if i == 1 else "false", d, n) for i, (d, n) in enumerate(days))
    sbtn = "".join('<button type="button" class="sl-slot" aria-pressed="false">%s</button>' % s for s in slots)
    out += sec('<div class="sl-start"><div>%s<ol class="sl-steps">%s</ol></div><div class="sl-book ox-solo"><div class="sl-book-head"><span class="ox-av" style="--c:#714B67">U</span>'
               '<span><b>Odoo Sales discovery call</b><small>30 min &middot; Google Meet &middot; Unisas consultant</small></span></div>'
               '<p class="sl-book-label">October 2026</p><div class="sl-days">%s</div><p class="sl-book-label">Available times (IST)</p><div class="sl-slots">%s</div>'
               '<a href="#get-demo" class="sl-book-btn is-off" data-svc-cta="implementation" aria-disabled="true">Pick a time</a></div></div>'
               % (head("GETTING STARTED", "How Do We Start Your Odoo Sales Implementation?", "Three simple steps, and the first one takes two minutes."), sst, dbtn, sbtn),
               "sl-sec--start")

    # 12 ---- FAQ
    faq = [("How long does an Odoo Sales implementation take?", "A focused Sales rollout typically takes 4 to 8 weeks. Connecting Inventory and Accounting, migrating data and custom documents add to that; we confirm the timeline in the fixed-scope proposal."),
           ("Can we keep our current quotation format?", "Yes. We rebuild your quotation, order and invoice layouts in Odoo with your branding, fields and terms."),
           ("Can customers sign and pay online?", "Yes. Customers get a secure link to review the quotation, sign it and pay a deposit or the full amount by UPI or card; the order confirms itself."),
           ("Does Odoo Sales handle GST and e-Invoicing?", "Yes. Indian GST taxes and the e-Invoice (IRN) integration are part of Odoo's Indian localisation, and we configure them with your accountant."),
           ("Can we import our existing customers, products and prices?", "Yes. We clean and import customers, products, variants and pricelists from Excel, Tally or your current system before go-live."),
           ("Can Odoo Sales work with our existing CRM or eCommerce site?", "Yes. Odoo CRM and Odoo eCommerce connect natively, and other systems can be integrated through APIs or connectors.")]
    items = "".join('<details class="sl-faq"%s><summary>%s<span class="sl-faq-ic" aria-hidden="true"></span></summary><p>%s</p></details>' % (" open" if i == 0 else "", q, a) for i, (q, a) in enumerate(faq))
    out += sec('<div class="sl-faqs">%s<div>%s</div></div>'
               % ('<div class="sl-faq-side">' + head("FAQ", "Frequently Asked Questions About Odoo Sales Implementation")
                  + '<div class="sl-faq-card"><b>Still have a question?</b><span>Talk to an Odoo consultant about your sales process.</span><a href="#get-demo" class="link-arrow" data-svc-cta="implementation">Ask us %s</a></div></div>' % g["ARROW"],
                  items), "sl-sec--faq")

    return out + JS


# ------------------------------------------------------------------ interactive explorer
ORDERS = [
    {"id": 1, "num": "S00482", "cust": "Bluebay Retail Pvt Ltd", "sp": "A", "date": "Oct 1", "state": "draft", "inv": "no",
     "lines": [["Ergo task chair", "Mesh back, 4D armrests", 24, 8450], ["Height-adjustable desk", "Dual motor, 160 x 80 cm", 12, 32900], ["Installation & setup", "On-site, 2 technicians", 1, 18000]]},
    {"id": 2, "num": "S00479", "cust": "Kaveri Foods", "sp": "R", "date": "Sep 30", "state": "sent", "inv": "no",
     "lines": [["Storage rack, 5 tier", "Powder-coated steel", 30, 6200], ["Delivery & assembly", "Coimbatore", 1, 9500]]},
    {"id": 3, "num": "S00476", "cust": "Orbit Motors", "sp": "M", "date": "Sep 28", "state": "sale", "inv": "to",
     "lines": [["Visitor chair", "Chrome frame", 40, 3900], ["Reception desk", "Walnut finish", 2, 46500]]},
    {"id": 4, "num": "S00471", "cust": "Sunrise Clinics", "sp": "A", "date": "Sep 26", "state": "sale", "inv": "done",
     "lines": [["Ergo task chair", "Mesh back, 4D armrests", 18, 8450]]},
    {"id": 5, "num": "S00468", "cust": "Indus Exports", "sp": "R", "date": "Sep 24", "state": "sent", "inv": "no",
     "lines": [["Conference table", "12 seater", 1, 128000], ["Conference chair", "Leather", 12, 11200]]},
    {"id": 6, "num": "S00463", "cust": "Arun Logistics", "sp": "M", "date": "Sep 22", "state": "sale", "inv": "to",
     "lines": [["Storage rack, 5 tier", "Powder-coated steel", 60, 6200]]},
]


def explorer(app_icon):
    views = [("list", "List", V_LIST), ("kanban", "Kanban", V_KANBAN), ("graph", "Graph", V_GRAPH)]
    switch = "".join('<button type="button" class="ox-vbtn%s" data-sx-view="%s" aria-label="%s view" title="%s" aria-pressed="%s">%s</button>'
                     % (" is-on" if k == "list" else "", k, n, n, "true" if k == "list" else "false", svg) for k, n, svg in views)
    return ('<div class="ox sl-ox" data-sx>' + odoo_nav(app_icon, "Sales", ["Orders", "Products", "Reporting", "Configuration"]) +
            '<div class="ox-cp"><div class="ox-cp-l"><button type="button" class="ox-new" data-sx-new>New</button><span class="ox-crumb" data-sx-crumb>Quotations</span></div>'
            '<label class="ox-search">%s<span class="ox-facet">%sMy Quotations</span><input type="search" placeholder="Search..." aria-label="Search quotations" data-sx-q></label>'
            '<div class="ox-views">%s</div></div><div class="ox-body" data-sx-body></div></div>'
            '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview with sample data. Open S00482, change a quantity, then Send, Preview and Confirm.</p>'
            % (SEARCH, FUNNEL, switch))


JS = '''<script>
(function(){
  /* --- quote-to-cash explorer --- */
  var root=document.querySelector('[data-sx]');
  if(root){
    var body=root.querySelector('[data-sx-body]'),crumb=root.querySelector('[data-sx-crumb]'),q=root.querySelector('[data-sx-q]');
    var D=%s, P={A:{n:'Anita Rao',c:'#B5567E'},R:{n:'Rahul Menon',c:'#3E7CB1'},M:{n:'Meera Iyer',c:'#4C9F70'}};
    var ST={draft:'Quotation',sent:'Quotation Sent',sale:'Sales Order'}, IV={no:'Nothing to Invoice',to:'To Invoice',done:'Fully Invoiced'};
    var st={view:'list',open:null,portal:false}, nextInv=43;
    D.forEach(function(o){o.log=[{w:'Unisas Bot',t:'Quotation created'}];});
    function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
    function inr(n){return '\\u20b9 '+n.toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2});}
    function untaxed(o){return o.lines.reduce(function(a,l){return a+l[2]*l[3];},0);}
    function total(o){return untaxed(o)*1.18;}
    function av(k){return '<span class="ox-av is-sm" style="--c:'+P[k].c+'">'+P[k].n[0]+'</span>';}
    function badge(s){return '<span class="sl-b sl-b--'+s+'">'+ST[s]+'</span>';}
    function ibadge(s){return '<span class="sl-b sl-b--i'+s+'">'+IV[s]+'</span>';}
    function rows(){var t=q.value.trim().toLowerCase();return D.filter(function(o){return !t||(o.num+' '+o.cust).toLowerCase().indexOf(t)>-1;});}
    function tiles(){
      var c=D.filter(function(o){return o.state!=='sale';}).length,d=D.filter(function(o){return o.state==='sale'&&!o.delivered;}).length,i=D.filter(function(o){return o.inv==='to';}).length;
      return '<div class="sl-tiles"><span class="sl-tile is-c"><b>'+c+'</b>To Confirm</span><span class="sl-tile is-d"><b>'+d+'</b>To Deliver</span><span class="sl-tile is-i"><b>'+i+'</b>To Invoice</span></div>';
    }
    function list(l){
      return tiles()+'<div class="ox-scroll"><table class="ox-table"><thead><tr><th class="ox-chk"><span class="ox-cb"></span></th><th>Number</th><th>Order Date</th><th>Customer</th><th>Salesperson</th><th class="ox-num">Total</th><th>Status</th><th>Invoice Status</th></tr></thead><tbody>'+
        l.map(function(o){return '<tr data-id="'+o.id+'" tabindex="0"><td class="ox-chk"><span class="ox-cb"></span></td><td><b>'+o.num+'</b></td><td>'+o.date+'</td><td>'+esc(o.cust)+'</td><td><span class="ox-sp">'+av(o.sp)+P[o.sp].n+'</span></td>'+
          '<td class="ox-num'+(o.inv==='to'?' sl-blue':'')+'"><b>'+inr(total(o))+'</b></td><td>'+badge(o.state)+'</td><td>'+ibadge(o.inv)+'</td></tr>';}).join('')+'</tbody></table></div>';
    }
    function kanban(l){
      return '<div class="sl-kgrid">'+l.map(function(o){return '<article class="sl-kcard" data-id="'+o.id+'" tabindex="0"><p><b>'+esc(o.cust)+'</b><b>'+inr(total(o))+'</b></p><p><span>'+o.num+' &middot; '+o.date+'</span>'+badge(o.state)+'</p><p class="sl-kfoot">'+ibadge(o.inv)+av(o.sp)+'</p></article>';}).join('')+'</div>';
    }
    function graph(l){
      var by={};l.filter(function(o){return o.state==='sale';}).forEach(function(o){by[o.cust]=(by[o.cust]||0)+untaxed(o);});
      var k=Object.keys(by),max=Math.max.apply(null,k.map(function(x){return by[x];}).concat([1]));
      return '<div class="ox-gtools"><span class="ox-measure"><span class="is-on">Untaxed Total</span></span><span class="sl-gnote">Confirmed sales orders by customer</span></div>'+
        (k.length?'<div class="sl-hbars">'+k.map(function(x){return '<div><span>'+esc(x)+'</span><i style="--w:'+(by[x]/max*100).toFixed(1)+'"></i><b>'+inr(by[x])+'</b></div>';}).join('')+'</div>':'<p class="ox-empty">Confirm an order to see it here.</p>');
    }
    function form(o){
      var i=['draft','sent','sale'].indexOf(o.state), edit=o.state!=='sale';
      var sb=['draft','sent','sale'].map(function(s,j){return '<span class="ox-sb'+(j===i?' is-cur':'')+'">'+ST[s]+'</span>';}).join('');
      var b=o.state==='draft'?'<button type="button" class="ox-pbtn" data-do="send">Send</button><button type="button" class="ox-sbtn" data-do="confirm">Confirm</button>':
            o.state==='sent'?'<button type="button" class="ox-pbtn" data-do="confirm">Confirm</button><button type="button" class="ox-sbtn" data-do="send">Send</button>':
            (o.inv==='to'?'<button type="button" class="ox-pbtn" data-do="invoice">Create Invoice</button>':'')+'<button type="button" class="ox-sbtn" data-do="send">Send</button>';
      b+='<button type="button" class="ox-sbtn" data-do="preview">Preview</button>';
      var smart=o.state==='sale'?'<span class="sl-smart">'+'<i><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h11v10H3zM14 9h4l3 3v4h-7z"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg></i><span>Delivery<b>1</b></span></span>'+(o.inv==='done'?'<span class="sl-smart"><i><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6"/></svg></i><span>Invoices<b>1</b></span></span>':''):'';
      var lines=o.lines.map(function(l,k){return '<tr><td><b>'+esc(l[0])+'</b><small>'+esc(l[1])+'</small></td><td class="ox-num">'+(edit?'<span class="sl-qty"><button type="button" data-q="-1" data-l="'+k+'" aria-label="Decrease">&minus;</button><b>'+l[2]+'</b><button type="button" data-q="1" data-l="'+k+'" aria-label="Increase">+</button></span>':l[2]+'.00')+'</td>'+
        '<td class="ox-num">'+inr(l[3])+'</td><td><span class="sl-tax">18%%</span></td><td class="ox-num">'+inr(l[2]*l[3])+'</td></tr>';}).join('');
      var log=o.log.slice().reverse().map(function(l){return '<div class="ox-msg"><span class="ox-av is-bot">U</span><div><p><b>'+l.w+'</b> <small>just now</small></p><p>'+l.t+'</p></div></div>';}).join('');
      return '<div class="ox-form"><div class="ox-f-main"><div class="ox-f-bar"><span class="ox-f-btns">'+b+'</span><span class="ox-sbar">'+sb+'</span></div>'+
        '<div class="ox-sheet">'+(smart?'<div class="sl-smarts">'+smart+'</div>':'')+'<h3>'+o.num+'</h3><dl class="ox-fields"><div><dt>Customer</dt><dd>'+esc(o.cust)+'</dd></div><div><dt>Expiration</dt><dd>Oct 31</dd></div>'+
        '<div><dt>Salesperson</dt><dd>'+av(o.sp)+P[o.sp].n+'</dd></div><div><dt>Payment Terms</dt><dd>30 Days</dd></div></dl>'+
        '<div class="ox-ftabs"><span class="is-on">Order Lines</span><span>Optional Products</span><span>Other Info</span></div>'+
        '<table class="sl-lines"><thead><tr><th>Product</th><th class="ox-num">Quantity</th><th class="ox-num">Unit Price</th><th>Taxes</th><th class="ox-num">Amount</th></tr></thead><tbody>'+lines+'</tbody></table>'+
        '<div class="sl-hd-tot"><span>Untaxed Amount:</span><b>'+inr(untaxed(o))+'</b><span>GST 18%%:</span><b>'+inr(untaxed(o)*0.18)+'</b><span class="is-total">Total:</span><b class="is-total">'+inr(total(o))+'</b></div></div></div>'+
        '<aside class="ox-chatter"><div class="ox-ch-btns"><span class="ox-pbtn">Send message</span><span class="ox-sbtn">Log note</span><span class="ox-sbtn">Activity</span></div><p class="ox-ch-sep">Today</p>'+log+'</aside></div>';
    }
    function portal(o){
      var signed=o.state==='sale';
      return '<div class="sl-portal is-live"><aside class="sl-portal-side"><p class="sl-portal-big">'+inr(total(o))+'</p><small>Tax Included</small>'+
        (signed?'<span class="sl-portal-ok">'+'&#10003; Signed &amp; paid</span>':'<button type="button" class="sl-portal-btn" data-do="sign">Sign &amp; Pay</button>')+
        '<span class="sl-portal-btn is-ghost">Download</span><div class="sl-portal-who">'+av(o.sp)+'<span><b>'+P[o.sp].n+'</b><small>Your Contact</small></span></div>'+
        '<button type="button" class="sl-back" data-do="back">&larr; Back to the order in Odoo</button></aside>'+
        '<div class="sl-portal-doc"><div class="sl-portal-head"><small>'+(signed?'Sales Order':'Quotation')+' for <b>'+esc(o.cust)+'</b></small><h3>'+o.num+'</h3><small>01/10/2026 &middot; Valid until 31/10/2026</small></div>'+
        '<table><thead><tr><th>Product</th><th>Qty</th><th>Amount</th></tr></thead><tbody>'+o.lines.map(function(l){return '<tr><td>'+esc(l[0])+'<small>'+esc(l[1])+'</small></td><td>'+l[2]+'</td><td>'+inr(l[2]*l[3])+'</td></tr>';}).join('')+
        '</tbody></table><p class="sl-portal-total"><span>Total</span><b>'+inr(total(o))+'</b></p></div></div>';
    }
    function render(){
      root.querySelectorAll('[data-sx-view]').forEach(function(b){var on=!st.open&&b.getAttribute('data-sx-view')===st.view;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
      if(st.open){var o=find(st.open);crumb.innerHTML='<a href="#" data-sx-back>Quotations</a><span>'+o.num+(st.portal?' (customer view)':'')+'</span>';body.innerHTML=st.portal?portal(o):form(o);return;}
      crumb.textContent=st.view==='graph'?'Sales Analysis':'Quotations';
      var l=rows();body.innerHTML=l.length?{list:list,kanban:kanban,graph:graph}[st.view](l):'<p class="ox-empty">No quotation matches \\u201c'+esc(q.value)+'\\u201d.</p>';
    }
    function find(id){return D.filter(function(x){return x.id===+id;})[0];}
    function confirm(o,how){o.state='sale';o.inv='to';o.log.push({w:'Unisas Bot',t:how+' <span class="sl-track">Status: '+ST.sent+' &rarr; <b>Sales Order</b></span>'});o.log.push({w:'Unisas Bot',t:'Delivery WH/OUT/000'+(30+o.id)+' created'});}
    root.addEventListener('click',function(e){
      var v=e.target.closest('[data-sx-view]');if(v){st.view=v.getAttribute('data-sx-view');st.open=null;st.portal=false;render();return;}
      if(e.target.closest('[data-sx-back]')){e.preventDefault();st.open=null;st.portal=false;render();return;}
      var o=st.open&&find(st.open);
      var qb=e.target.closest('[data-q]');if(qb&&o){var l=o.lines[+qb.getAttribute('data-l')];l[2]=Math.max(1,l[2]+(+qb.getAttribute('data-q')));render();return;}
      var d=e.target.closest('[data-do]');
      if(d&&o){var a=d.getAttribute('data-do');
        if(a==='send'){if(o.state==='draft')o.state='sent';o.log.push({w:P[o.sp].n,t:'Quotation sent to the customer by email'});}
        if(a==='confirm')confirm(o,'Order confirmed.');
        if(a==='preview')st.portal=true;
        if(a==='back')st.portal=false;
        if(a==='sign'){confirm(o,'Signed online by the customer and paid via UPI.');}
        if(a==='invoice'){o.inv='done';o.log.push({w:'Unisas Bot',t:'Invoice INV/2026/000'+(nextInv++)+' created and posted'});}
        render();return;}
      var r=e.target.closest('[data-id]');if(r){st.open=+r.getAttribute('data-id');st.portal=false;render();}
    });
    root.addEventListener('keydown',function(e){if(e.key==='Enter'){var r=e.target.closest&&e.target.closest('[data-id]');if(r){st.open=+r.getAttribute('data-id');render();}}});
    root.querySelector('[data-sx-new]').addEventListener('click',function(){st.open=1;st.portal=false;render();});
    q.addEventListener('input',function(){st.open=null;st.portal=false;render();});
    render();
  }
  /* --- document chain --- */
  var chain=document.querySelector('.sl-chain');
  if(chain){
    var docs=[].slice.call(chain.querySelectorAll('.sl-doc')),btn=chain.querySelector('[data-chain-play]'),timer=null;
    function set(step){docs.forEach(function(d,i){var bars=d.querySelectorAll('.ox-sb');var lvl=step>i?2:(step===i?1:0);
      bars.forEach(function(b,j){b.classList.toggle('is-cur',j===lvl);});d.classList.toggle('is-done',step>i);d.classList.toggle('is-now',step===i);});}
    set(-1);
    btn.addEventListener('click',function(){clearInterval(timer);var s=0;set(0);btn.disabled=true;
      timer=setInterval(function(){s++;set(s);if(s>docs.length){clearInterval(timer);btn.disabled=false;btn.querySelector('span').textContent='Play again';}},1100);});
  }
  /* --- customisation pins --- */
  var cust=document.querySelector('.sl-custom-grid');
  if(cust){cust.querySelectorAll('.sl-pins li').forEach(function(li){
    var n=li.getAttribute('data-pin');
    function on(x){cust.querySelectorAll('.sl-pdf [data-pin="'+n+'"]').forEach(function(p){p.classList.toggle('is-hot',x);});li.classList.toggle('is-hot',x);}
    li.addEventListener('mouseenter',function(){on(true);});li.addEventListener('mouseleave',function(){on(false);});
    li.addEventListener('focus',function(){on(true);});li.addEventListener('blur',function(){on(false);});
  });}
  /* --- booking widget --- */
  var book=document.querySelector('.sl-book');
  if(book){var go=book.querySelector('.sl-book-btn');
    function pick(sel,el){book.querySelectorAll(sel).forEach(function(x){var on=x===el;x.classList.toggle('is-on',on);x.setAttribute('aria-pressed',on);});}
    book.addEventListener('click',function(e){var d=e.target.closest('.sl-day');if(d)pick('.sl-day',d);
      var s=e.target.closest('.sl-slot');if(s){pick('.sl-slot',s);var day=book.querySelector('.sl-day.is-on');
        go.classList.remove('is-off');go.removeAttribute('aria-disabled');go.textContent='Confirm '+day.querySelector('small').textContent+' '+day.querySelector('b').textContent+' Oct, '+s.textContent;}
      if(e.target===go&&go.classList.contains('is-off'))e.preventDefault();});
  }
})();
</script>
''' % json.dumps(ORDERS)

CTA = ("Let's Connect Your Quote-to-Cash in Odoo",
       "Tell us how your team quotes, delivers and invoices today. We'll show you the same flow in Odoo Sales and recommend the right setup.")
