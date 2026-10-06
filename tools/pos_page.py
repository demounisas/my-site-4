"""
Odoo Point of Sale page (odoo-pos.html). Every screen is modelled on the real Odoo 20 Point of Sale app
(demo.odoo.com/odoo/point-of-sale): the register with categories, product grid, order lines, numpad and
Customer / Payment buttons, the payment and receipt screens, offline mode and order sync, POS settings,
products with taxes and pricelists, the Closing Register dialog, employee login, IoT hardware, the
restaurant floor plan and kitchen tickets, and Orders Analysis.
Sample company: a Chennai ethnic-wear chain with four stores, an online shop and a café in its flagship,
under the fictional brand "Nila Threads". Shared Odoo look: odoo-ui.css. Page styles: pos.css.

hero(g) and build(g) get the build script's globals.
"""
import json

import crm_explorer as ox

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
WIFI = ox.ic('<path d="M2.5 9a14 14 0 0 1 19 0M5.5 12.5a9.5 9.5 0 0 1 13 0M8.8 16a4.5 4.5 0 0 1 6.4 0"/><circle cx="12" cy="19.3" r="1" fill="currentColor"/>', 16, 2)


def head(eyebrow, title, sub="", cls=""):
    return ('<div class="ps-head%s"><p class="ps-eyebrow mono">%s</p><h2 class="ps-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="ps-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="ps-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


def data(sid, obj):
    """JSON for the page script, safe inside a <script> element."""
    return '<script type="application/json" id="%s">%s</script>' % (sid, json.dumps(obj).replace("</", "<\\/"))


def ox_head(a, b, right=""):
    return ('<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>%s</a><span>%s</span></span></div><span></span>%s</div>'
            % (a, b, right or "<span></span>"))


def btns(cls, attr, labels):
    """A row of toggle buttons, the first one pressed."""
    return "".join('<button type="button" class="%s%s" %s="%d" aria-pressed="%s">%s</button>'
                   % (cls, " is-on" if i == 0 else "", attr, i, "true" if i == 0 else "false", l) for i, l in enumerate(labels))


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">Point of Sale</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["Cash, card &amp; UPI", "Stock updated with every sale", "Keeps selling offline"])
    copy = ('<div class="ps-hero-copy">%s<p class="ps-eyebrow mono">ODOO POINT OF SALE IMPLEMENTATION</p>'
            '<h1 class="ps-h1">Point of Sale Software for <span>Smarter Store Management</span> with Odoo</h1>'
            '<p class="ps-lead">Unisas sets up Odoo Point of Sale for your shops, counters and restaurants. Every bill updates stock, customer history and accounting '
            'the moment it is paid, across every store, and the checkout keeps working when the internet doesn&rsquo;t.</p>'
            '<ul class="ps-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Plan your Odoo POS %s</a>'
            '<a href="#register" class="btn btn-ghost">Try the register</a></div></div>' % (crumb, points, g["ARROW"]))
    tiles = "".join('<span><i style="--h:%d"></i><b>%s</b><small>&#8377; %s</small></span>' % t for t in
                    [(220, "Cotton Kurta", "1,299"), (40, "Linen Kurta", "1,499"), (330, "Silk Saree", "12,500"), (20, "Silk Stole", "899"), (160, "Jhumkas", "449"), (280, "Tote Bag", "349")])
    reg = ('<div class="ps-hx-reg"><div class="ps-hx-top"><b>Nila<span>Threads</span></b><span class="is-on">Register</span><span>Orders</span><em>' + WIFI + ' Anitha</em></div>'
           '<div class="ps-hx-main"><div class="ps-hx-ord"><p><b>Cotton Kurta &ndash; Indigo</b><span>1.00 &times; &#8377; 1,299</span><em>&#8377; 1,299.00</em></p>'
           '<p><b>Silk Stole</b><span>1.00 &times; &#8377; 899</span><em>&#8377; 899.00</em></p><p><b>Oxidised Jhumkas</b><span>2.00 &times; &#8377; 449</span><em>&#8377; 898.00</em></p>'
           '<div class="ps-hx-tot"><span>Total</span><b>&#8377; 3,096.00</b></div><div class="ps-hx-pay"><span>Customer</span><span class="is-pay">Payment</span></div></div>'
           '<div class="ps-hx-grid">' + tiles + '</div></div></div>')
    paper = ('<div class="ps-hv-paper"><b>NILA THREADS</b><small>T. Nagar &middot; Chennai</small><p><span>Cotton Kurta</span><span>1,299.00</span></p>'
             '<p><span>Silk Stole</span><span>899.00</span></p><p><span>Jhumkas x2</span><span>898.00</span></p><p class="is-tot"><span>TOTAL</span><span>&#8377;3,096.00</span></p>'
             '<p><span>UPI</span><span>PAID</span></p><i class="ps-hv-bar" aria-hidden="true"></i></div>')
    term = ('<div class="ps-hv-term"><div class="ps-hv-tscr"><span class="ps-hx-qr"></span><b>&#8377; 3,096.00</b><small>' + TICK + 'UPI &middot; Paid</small></div>'
            '<div class="ps-hv-keys">' + "<i></i>" * 11 + '<i class="is-ok"></i></div></div>')
    return ('<section class="ps-hero">' + copy + '<div class="ps-hero-vis ps-hv" aria-label="The Odoo POS register on a counter tablet, with the receipt printing and the UPI payment confirmed on the terminal">'
            '<div class="ps-hv-dev"><div class="ps-hv-tab">' + reg + '</div><div class="ps-hv-stand"></div></div>'
            '<div class="ps-hv-prn">' + paper + '<div class="ps-hv-box"></div></div>' + term + '</div></section>')

# ------------------------------------------------------------------ sections
def build(g):
    out = ""
    app_icon = g["TILE_ICONS"][10]

    # 1 ---- gaps between checkout, inventory and accounting
    out += sec(head("THE GAPS", "Is Your Point of Sale Creating Gaps Between Checkout, Inventory and Accounting?",
                    "A standalone billing machine knows what was sold. Your stock sheet and your books find out later, if someone re-types it. "
                    "Ring up a few sales, close the day and count the gaps. Then try the same day on a connected POS.", "is-center")
               + '<div class="ps-gap" data-p1box><div class="ps-mode" role="group" aria-label="System"><button type="button" class="is-on" data-p1mode="old" aria-pressed="true">Standalone billing</button>'
                 '<button type="button" data-p1mode="odoo" aria-pressed="false">Connected POS</button></div>'
                 '<div class="ps-gap-g"><div class="ps-gp ox-solo"><p class="ps-gp-h"><i style="--c:#B8325A"></i>Checkout</p><div data-p1="pos"></div></div>'
                 '<div class="ps-gp ox-solo"><p class="ps-gp-h"><i style="--c:#1F8A78"></i>Inventory</p><div data-p1="inv"></div></div>'
                 '<div class="ps-gp ox-solo"><p class="ps-gp-h"><i style="--c:#B7791F"></i>Accounting</p><div data-p1="acc"></div></div></div>'
                 '<div class="ps-gap-f"><button type="button" class="ox-pbtn" data-p1sell>Ring up a sale</button><button type="button" class="ox-sbtn" data-p1close>Close the day</button>'
                 '<button type="button" class="ox-sbtn" data-p1reset>Start over</button><p class="ps-gap-msg" data-p1msg aria-live="polite"></p></div></div>', "ps-sec--gap")

    # 2 ---- the register
    cats = ["Kurtas", "Sarees", "Dupattas", "Accessories"]
    prods = [[1, "Cotton Kurta &ndash; Indigo", "Kurtas", 1299, 220, 2, 12], [2, "Linen Kurta &ndash; Mustard", "Kurtas", 1499, 42, 6, 12],
             [3, "Chanderi Kurta Set", "Kurtas", 2499, 300, 4, 12], [4, "Kanchipuram Silk Saree", "Sarees", 12500, 340, 1, 12],
             [5, "Block-print Cotton Saree", "Sarees", 2199, 18, 9, 12], [6, "Silk Stole", "Dupattas", 899, 20, 12, 5],
             [7, "Phulkari Dupatta", "Dupattas", 1199, 330, 5, 12], [8, "Oxidised Jhumkas", "Accessories", 449, 200, 20, 5],
             [9, "Jute Tote Bag", "Accessories", 349, 90, 30, 5], [10, "Gift Wrap", "Accessories", 50, 0, 99, 5]]
    out += sec(head("EVERY SALE, CONNECTED", "How Can Odoo Connect Every Sale With Your Store Operations?",
                    "This is the Odoo Point of Sale register for Nila Threads, T. Nagar. Add products, change a quantity on the numpad, pick a loyalty customer and take payment. "
                    "When you validate, see what the same sale changed in stock, loyalty and the session.", "is-center")
               + '<div class="ps-reg-w"><div class="ps-reg ox-solo" data-p2box><div class="ps-rt"><span class="ps-rt-logo">%s</span><button type="button" class="ps-rt-tab is-on" data-p2nav="register">Register</button>'
                 '<button type="button" class="ps-rt-tab" data-p2nav="orders">Orders <b data-p2n>0</b></button><label class="ps-rt-q">%s<input type="search" placeholder="Search products..." data-p2q aria-label="Search products"></label>'
                 '<span class="ps-rt-r"><span class="ps-wifi">%s</span><span class="ps-rt-emp"><span class="ox-av is-sm" style="--c:#B8325A">A</span>Anitha</span></span></div>'
                 '<div class="ps-rb" data-p2body></div></div><aside class="ps-fx ox-solo" aria-live="polite"><p class="ps-fx-h">What this sale changed</p><ul data-p2fx></ul></aside></div>'
                 '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview of the Odoo POS register with sample data. Click products, use the numpad, pay and validate.</p>'
                 % (app_icon, ox.SEARCH, WIFI) + data("ps-prods", prods) + data("ps-cats", cats), "ps-sec--reg", "register")

    # 3 ---- configured around how the store operates
    qs = [["Several cashiers share one counter", ["emp"]], ["Products have barcodes", ["bar"]], ["Customers sit at tables and order food", ["rest", "floor", "kitchen"]],
          ["Regulars pay at the end of the month", ["acct"]], ["Large items are delivered from the warehouse", ["ship"]], ["Members get special prices and points", ["price", "loyal"]],
          ["Staff can receive tips", ["tips"]], ["Some products are sold by weight", ["scale"]]]
    setts = {"emp": ["Log in with Employees", "Each cashier signs in with a PIN or badge; every order records who sold it"],
             "bar": ["Barcode Scanner", "Scan to add products, customers and coupons; default barcode nomenclature"],
             "rest": ["Is a Bar/Restaurant", "Orders are tied to tables and guests"], "floor": ["Floors &amp; Tables", "Your floor plan, tables coloured by status"],
             "kitchen": ["Preparation Display", "Orders sent to the kitchen screen or printer by category"],
             "acct": ["Customer Account payment", "Sales charged to the customer, invoiced and collected later"],
             "ship": ["Allow Ship Later", "The customer pays now; delivery is created from the warehouse"],
             "price": ["Flexible Pricelists", "Member, festive and wholesale prices chosen on the order"], "loyal": ["Loyalty, Gift Cards &amp; eWallet", "Points earned and spent in store and online"],
             "tips": ["Tips", "Tip added on the payment screen and tracked per employee"], "scale": ["Weighing Scale", "Products marked &lsquo;To Weigh With Scale&rsquo; read the weight from the IoT Box"]}
    presets = [["Boutique", [0, 1, 4, 5]], ["Supermarket", [0, 1, 5, 7]], ["Caf&eacute;", [0, 2, 6]], ["Wholesale counter", [1, 3, 4]]]
    out += sec(head("YOUR STORE, YOUR SETUP", "How Does Unisas Configure POS Around the Way Your Store Actually Operates?",
                    "We start from how your counter works: who checks out, what customers buy and how they pay. Each answer switches on a specific setting.", "is-center")
               + '<div class="pl-2 is-w"><div class="pl-card"><p class="pl-k">What we ask &rarr; what we switch on</p><div class="pl-scroll"><table class="pl-table"><tbody>%s</tbody></table></div></div>'
                 '<div class="pl-card"><p class="pl-k">Typical setups</p><ul class="pl-steps">%s</ul></div></div>'
                 % ("".join('<tr><th>%s</th><td><ul class="pl-chips">%s</ul><small class="pl-muted">%s</small></td></tr>'
                            % (q[0], "".join('<li class="pl-chip">%s</li>' % setts[k][0] for k in q[1]), "; ".join(setts[k][1] for k in q[1])) for q in qs),
                    "".join('<li><span class="pl-n">%d</span><b>%s</b><p>%s</p></li>' % (i + 1, pr[0], ", ".join(qs[j][0].lower() for j in pr[1]).capitalize() + ".") for i, pr in enumerate(presets))),
               "ps-sec--cfg")

    # 4 ---- offline
    out += sec(head("OFFLINE MODE", "Can Odoo Keep Your Checkout Running Even When the Internet Goes Down?",
                    "Yes. Once a session is open, the register keeps products, prices and customers in the browser. Orders taken offline are saved on the device and sent to Odoo when the connection returns. "
                    "Cut the internet, keep selling, then reconnect.", "is-center")
               + '<div class="ps-off" data-p4box><div class="ps-off-reg ox-solo"><div class="ps-off-top"><b>Register &middot; Counter 2</b><span class="ps-wifi" data-p4wifi>%s</span><span class="ps-off-q" data-p4q></span></div>'
                 '<div class="ps-off-b"><p class="ps-off-s" data-p4s></p><button type="button" class="ps-big" data-p4sell>Sell &amp; print receipt</button>'
                 '<label class="ps-net"><input type="checkbox" data-p4net checked><span class="ps-sw" aria-hidden="true"></span><span>Internet connection</span></label></div>'
                 '<ul class="ps-off-l" data-p4local></ul></div>'
                 '<div class="ox ps-ox">%s<div class="ox-scroll"><table class="ox-table ps-ord-t"><thead><tr><th>Order Ref</th><th>Time</th><th>Cashier</th><th class="ox-num">Total</th><th>Status</th></tr></thead><tbody data-p4srv></tbody></table></div>'
                 '<ul class="ps-off-n"><li><b>Works offline</b> Scanning, prices, discounts, cash payments, receipts</li><li><b>Needs the internet</b> Card terminals and live UPI confirmation; we set a fallback for each</li>'
                 '<li><b>Keep in mind</b> Don&rsquo;t reload the register tab while offline</li></ul></div></div>'
                 % (WIFI, ox_head("Point of Sale", "Orders")), "ps-sec--off")

    # 5 ---- products, pricing, taxes, rules
    lines = [["Linen Kurta &ndash; Mustard", 1499, 2, 12, 1], ["Silk Stole", 899, 1, 5, 0], ["Oxidised Jhumkas", 449, 1, 5, 0]]
    pls = [["Public Pricelist", 0, "List prices"], ["Nila Members", 10, "10% off for loyalty members"], ["Wholesale (10+ pcs)", 22, "Boutique resellers, min. 10 pieces"]]
    out += sec(head("PRODUCTS, PRICES &amp; RULES", "How Does Unisas Set Up Products, Pricing, Taxes and POS-Specific Rules?",
                    "Each product carries its POS category, barcode, variants and GST rate; pricelists, promotions and discount limits sit on top. "
                    "Here is how that looks for one product in a boutique.", "is-center")
               + '<div class="pl-2"><div class="pl-card"><p class="pl-k">What each product carries &middot; Linen Kurta, Mustard</p><div class="pl-scroll"><table class="pl-table"><tbody>'
                 '<tr><th>Sales price</th><td>&#8377; 1,499.00, tax included</td></tr><tr><th>GST</th><td><span class="pl-chip">GST 12%%</span></td></tr><tr><th>POS category</th><td>Kurtas</td></tr>'
                 '<tr><th>Barcode</th><td class="mono">8901234500217</td></tr><tr><th>Variants</th><td><ul class="pl-chips"><li class="pl-chip">S</li><li class="pl-chip">M</li><li class="pl-chip">L</li><li class="pl-chip">XL</li></ul></td></tr></tbody></table></div></div>'
                 '<div class="pl-card"><p class="pl-k">Rules that sit on top</p><ul class="pl-steps">%s'
                 '<li><span class="pl-n">%d</span><b>Festive promotion</b><em>Automatic</em><p>Buy 2 kurtas, get 10%% off them, applied on the order without the cashier doing anything.</p></li>'
                 '<li><span class="pl-n">%d</span><b>Discount limit</b><em>Up to 10%%</em><p>Cashiers can give up to 10%% on an order. Anything above needs the store manager&rsquo;s PIN.</p></li></ul></div></div>'
                 % ("".join('<li><span class="pl-n">%d</span><b>%s</b><em>%s</em><p>%s</p></li>' % (i + 1, x[0], "List price" if not x[1] else "%d%% off" % x[1], x[2]) for i, x in enumerate(pls)), len(pls) + 1, len(pls) + 2),
               "ps-sec--price")

    # 6 ---- inventory and accounting
    orders = [["Order 00042-001-0001", "10:12", "Cash", 3096], ["Order 00042-001-0002", "10:47", "UPI", 12500], ["Order 00042-001-0003", "11:30", "Card", 2499],
              ["Order 00042-001-0004", "12:05", "UPI", 2998], ["Order 00042-001-0005", "13:22", "Cash", 1748], ["Order 00042-001-0006", "15:40", "Card", 4398],
              ["Order 00042-001-0007", "17:15", "UPI", 1299], ["Order 00042-001-0008", "18:52", "Cash", 2647]]
    moves = [["Cotton Kurta &ndash; Indigo", 2, "2 &rarr; 0", True], ["Kanchipuram Silk Saree", 1, "1 &rarr; 0", True], ["Linen Kurta &ndash; Mustard", 2, "6 &rarr; 4", False],
             ["Chanderi Kurta Set", 2, "4 &rarr; 2", True], ["Silk Stole", 3, "12 &rarr; 9", False], ["Oxidised Jhumkas", 4, "20 &rarr; 16", False]]
    out += sec(head("INVENTORY &amp; ACCOUNTING", "How Can Odoo Connect POS Sales With Inventory and Accounting?",
                    "Stock leaves the store&rsquo;s location as each order is paid. When the register is closed, Odoo posts one journal entry for the session, split by payment method and GST rate, "
                    "and reordering rules raise purchase orders for what ran low. Close today&rsquo;s session and see all three.", "is-center")
               + '<div class="ps-cl" data-p6box><div class="ox ps-ox">%s<div class="ox-scroll"><table class="ox-table ps-ord-t"><thead><tr><th>Order Ref</th><th>Time</th><th>Payment</th><th class="ox-num">Total</th></tr></thead><tbody>%s</tbody>'
                 '<tfoot><tr><td colspan="3"><b>8 orders</b></td><td class="ox-num"><b data-p6tot></b></td></tr></tfoot></table></div></div>'
                 '<div class="ps-cl-r"><div class="ps-cl-tabs" role="group" aria-label="Result">%s</div><div class="ps-cl-b ox-solo" data-p6b aria-live="polite"></div></div></div>'
                 % (ox_head("POS/00042", "T. Nagar &middot; 10 Oct", '<span><button type="button" class="ox-pbtn" data-p6close>Close Register</button></span>'),
                    "".join('<tr><td>%s</td><td>%s</td><td>%s</td><td class="ox-num">&#8377; %s.00</td></tr>' % (o[0], o[1], o[2], "{:,}".format(o[3])) for o in orders),
                    btns("ps-tab", "data-p6t", ["Journal entry", "Stock moves", "Replenishment"]))
               + data("ps-orders", orders) + data("ps-moves", moves), "ps-sec--cl")

    # 7 ---- payments, cashiers, controls
    emps = [["Anitha S", "Cashier", "#B8325A", [1, 1, 0, 0, 0, 1]], ["Ravi Kumar", "Store Manager", "#3E7CB1", [1, 1, 1, 1, 1, 1]], ["Joel M", "Trainee", "#1F8A78", [1, 0, 0, 0, 0, 0]]]
    acts = ["Sell and take payment", "Discount up to 10%", "Discount above 10% or change a price", "Refund an order", "Open the cash drawer without a sale", "Close the register"]
    out += sec(head("PAYMENTS, CASHIERS &amp; CONTROLS", "How Should Your POS Handle Payments, Cashiers and Store-Level Controls?",
                    "Cashiers sign in with their own PIN, so every order, refund and discount is traceable to a person. Managers approve the risky actions, "
                    "and the register only closes once cash is counted.", "is-center")
               + '<div class="pl-2"><div class="pl-card"><p class="pl-k">Who can do what at the counter</p><div class="pl-scroll"><table class="pl-table"><thead><tr><th></th>%s</tr></thead><tbody>%s</tbody></table></div>'
                 '<p class="pl-muted" style="margin:10px 0 0;font-size:0.84rem">&times; means the action needs a manager&rsquo;s PIN.</p></div>'
                 '<div class="pl-card"><p class="pl-k">Closing the register &middot; 8 orders, &#8377; 31,185</p><div class="pl-scroll"><table class="pl-table"><thead><tr><th>Payment</th><th class="is-c">Expected</th><th class="is-c">Counted</th><th class="is-c">Difference</th></tr></thead><tbody>'
                 '<tr><th>Cash</th><td class="is-c">&#8377; 12,491</td><td class="is-c">&#8377; 12,291</td><td class="is-c"><span class="pl-chip is-bad">&minus; &#8377; 200</span></td></tr>'
                 '<tr><th>Card</th><td class="is-c">&#8377; 6,897</td><td class="is-c">&#8377; 6,897</td><td class="is-c"><span class="pl-chip is-ok">0</span></td></tr>'
                 '<tr><th>UPI</th><td class="is-c">&#8377; 16,797</td><td class="is-c">&#8377; 16,797</td><td class="is-c"><span class="pl-chip is-ok">0</span></td></tr></tbody></table></div>'
                 '<p class="pl-muted" style="margin:12px 0 0;font-size:0.88rem">Small differences are allowed with a note. Above &#8377; 200, only a manager can close, and the difference is posted to the books with the reason.</p></div></div>'
                 % ("".join('<th class="is-c">%s<br><small>%s</small></th>' % (e[0], e[1]) for e in emps),
                    "".join('<tr><th>%s</th>%s</tr>' % (a, "".join('<td class="is-c">%s</td>' % ('<span class="pl-chip is-ok">&#10003;</span>' if e[3][i] else '<span class="pl-chip is-bad">&times;</span>') for e in emps)) for i, a in enumerate(acts))),
               "ps-sec--ctl")

    # 8 ---- hardware and payment integrations
    devs = [["scan", "Barcode scanner", "USB or Bluetooth, works as a keyboard", ["Scan a product, a loyalty card and a coupon", "Nomenclature for price-embedded barcodes"], 14, 62],
            ["print", "Receipt printer", "Network ePOS printer, or USB through the IoT Box", ["GST receipt layout with logo and footer", "Reprint and email/WhatsApp receipt"], 36, 30],
            ["drawer", "Cash drawer", "Opened by the receipt printer", ["Opens only on cash payments", "Manager-only open without a sale"], 36, 70],
            ["display", "Customer display", "Second screen or tablet", ["Shows lines, total and the UPI QR", "Promotions while idle"], 60, 18],
            ["card", "Card terminal", "Integrated payment terminal (e.g. Razorpay or Paytm)", ["Amount sent from the register, no re-typing", "Approval and refunds recorded on the order"], 62, 62],
            ["scale", "Weighing scale", "Connected through the IoT Box", ["Weight read into the order line", "Tare and price per kg"], 86, 40],
            ["kitchen", "Kitchen printer", "Network printer by preparation category", ["Drinks to the bar, food to the kitchen", "Order changes printed as updates"], 86, 78]]
    pins = "".join('<button type="button" class="ps-dev%s" data-p8="%d" style="--x:%d;--y:%d" aria-pressed="%s"><span class="ps-dev-i is-%s" aria-hidden="true"></span><span>%s</span></button>'
                   % (" is-on" if i == 0 else "", i, d[4], d[5], "true" if i == 0 else "false", d[0], d[1]) for i, d in enumerate(devs))
    out += sec(head("HARDWARE &amp; PAYMENTS", "How Does Unisas Configure POS Hardware and Payment Integrations?",
                    "We confirm every device during scoping, connect it to the register, and test it at the counter before go-live: scanners, printers, drawers, displays, scales and card terminals. "
                    "Click a device on the counter, then run its test.", "is-center")
               + '<div class="ps-hw" data-p8box><div class="ps-counter" aria-label="Store counter"><div class="ps-desk" aria-hidden="true"></div>%s</div>'
                 '<div class="ps-hw-c ox-solo" aria-live="polite" data-p8card></div></div>' % pins + data("ps-devs", devs), "ps-sec--hw")

    # 9 ---- multi-store, loyalty, omnichannel
    scen = [["Out of stock here, ship from another store", [["T. Nagar register", "Chanderi Kurta Set, size M: 0 here", "Product info shows stock in every store"], ["Anna Nagar", "3 in stock, reserved for Meena", "Ship Later on the order"],
             ["Payment", "Paid in full by UPI at T. Nagar", "Delivery created from Anna Nagar"], ["Meena", "Delivered home in 2 days", "+250 points"]], 250],
            ["Bought online, returned in store", [["Website", "Phulkari Dupatta ordered online", "Shop and POS share products and customers"], ["Coimbatore register", "Refund from the original web order", "Return line linked to the order"],
             ["Inventory", "Item back into Coimbatore stock", "Sellable again the same day"], ["Meena", "Refund to eWallet", "Spendable in any store"]], 0],
            ["Points earned in store, spent online", [["T. Nagar register", "&#8377; 3,096 bill, member pricelist", "+310 points"], ["Loyalty", "1,550 points = &#8377; 155 reward", "Same programme for POS and website"],
             ["Website checkout", "Reward applied to an online order", "Points deducted"], ["Reporting", "Reward cost shown per channel", "Marketing sees what loyalty costs"]], 310]]
    stock = [["T. Nagar", 0], ["Anna Nagar", 3], ["Coimbatore", 1], ["Online warehouse", 7]]
    out += sec(head("STORES, LOYALTY &amp; OMNICHANNEL", "Can Odoo Support Multiple Stores, Customer Loyalty and Omnichannel Selling?",
                    "Every store, counter and the website share one product list, one customer list and one loyalty programme, so a customer is the same person everywhere. "
                    "Pick a situation and follow it.", "is-center")
               + '<div class="ps-omni" data-p9box><div class="ps-omni-l"><div class="ps-scn" role="group" aria-label="Situation">%s</div><ol class="ps-omni-s ox-solo" data-p9steps aria-live="polite"></ol></div>'
                 '<div class="ps-omni-r"><div class="ps-cust ox-solo"><span class="ox-av is-msg" style="--c:#8E4F83">M</span><span><b>Meena Krishnan</b><small>Member since 2023 &middot; 14 orders in 3 channels</small></span>'
                 '<div class="ps-pts"><b data-p9pts>1,240</b><small>loyalty points</small></div></div>'
                 '<div class="ps-stk ox-solo"><p><b>Chanderi Kurta Set &middot; M</b><small>On hand by store</small></p><ul>%s</ul></div></div></div>'
                 % (btns("ps-scb", "data-p9", [s[0] for s in scen]), "".join('<li><span>%s</span><i style="--p:%d"></i><b>%d</b></li>' % (n, q * 14, q) for n, q in stock))
               + data("ps-scen", scen), "ps-sec--omni")

    # 10 ---- retail, restaurants, others
    envs = [["retail", "Retail &amp; fashion"], ["rest", "Restaurant"], ["cafe", "Caf&eacute; &amp; quick service"], ["groc", "Grocery &amp; weighed goods"]]
    cfgs = {"retail": ["Product variants: size and colour picked on the register", "Exchanges and returns linked to the original receipt", "Barcode labels printed from Inventory", "Ship Later for alterations and home delivery"],
            "rest": ["Floor plan with tables, seats and status colours", "Orders sent to the kitchen by preparation category", "Split the bill by guest or item", "Tips and service charge"],
            "cafe": ["Combos: a drink and a snack at one price", "Self-order kiosk or QR menu at the table", "Order number on the customer display", "Fast cash with quick-amount buttons"],
            "groc": ["Scale reads weight into the line", "Price-embedded barcodes for packed items", "Lots and expiry dates on perishables", "Loyalty and weekly offers on fast movers"]}
    out += sec(head("YOUR SELLING ENVIRONMENT", "How Does Unisas Adapt POS Workflows for Retail, Restaurants or Other Selling Environments?",
                    "The same POS runs a boutique, a restaurant, a caf&eacute; counter or a grocery till; what changes is the workflow at the counter. Here is what we set up for each.", "is-center")
               + '<ul class="pl-grid" style="--cols:4">%s</ul>'
                 % "".join('<li><b>%s</b><ul class="pl-ticks ps-env-t">%s</ul></li>' % (n, "".join("<li>%s</li>" % c for c in cfgs[k])) for k, n in envs),
               "ps-sec--env")

    # 11 ---- insights
    rep = {"store": [["T. Nagar", 412000, 318], ["Anna Nagar", 296000, 241], ["Coimbatore", 188000, 167], ["Flagship caf&eacute;", 74000, 902]],
           "hour": [["10&ndash;12", 98000, 141], ["12&ndash;14", 132000, 236], ["14&ndash;16", 104000, 172], ["16&ndash;18", 186000, 288], ["18&ndash;20", 266000, 512], ["20&ndash;22", 184000, 279]],
           "cat": [["Sarees", 318000, 74], ["Kurtas", 342000, 266], ["Dupattas", 98000, 112], ["Accessories", 64000, 274], ["Caf&eacute;", 74000, 902]],
           "emp": [["Anitha S", 268000, 284], ["Ravi Kumar", 214000, 176], ["Priya D", 236000, 241], ["Joel M", 82000, 107], ["Caf&eacute; counter", 74000, 902]]}
    out += sec(head("SALES &amp; STORE INSIGHTS", "How Can Odoo Turn POS Transactions Into Useful Sales and Store Insights?",
                    "Every order carries the store, hour, cashier, products, payment method and customer, so Orders Analysis can slice the month any way you need. "
                    "Change the measure and the grouping.", "is-center")
               + '<div class="ps-an" data-p11box><div class="ox ps-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb">Orders Analysis</span></div><span></span><span></span></div>'
                 '<div class="ox-gtools"><span class="ox-measure">%s</span><span class="ps-gb"><small>Group by</small><select data-p11g><option value="store">Point of Sale</option><option value="hour">Hour</option>'
                 '<option value="cat">Product Category</option><option value="emp">Employee</option></select></span></div><div class="ps-bars" data-p11bars></div></div>'
                 '<div class="ps-an-r ox-solo" data-p11ins aria-live="polite"></div></div>'
                 % "".join('<button type="button" data-p11m="%s"%s>%s</button>' % (k, ' class="is-on"' if k == "rev" else "", n) for k, n in [("rev", "Total"), ("cnt", "Orders"), ("avg", "Average Order")])
               + data("ps-rep", rep), "ps-sec--an")

    # 12 ---- setup to go-live
    phases = [["Discover", "Week 1", ["Store visits and counter walkthrough", "Products, taxes and pricing reviewed", "Hardware list per counter", "Workflows: returns, exchanges, credit"], "Time at a busy counter, and your current billing data."],
              ["Products &amp; pricing", "Week 1&ndash;2", ["Products, variants and barcodes imported", "GST rates and HSN codes", "Pricelists, promotions, loyalty", "Opening stock per store"], "Product master and a stock count for each store."],
              ["Configure", "Week 2&ndash;3", ["POS per store and counter", "Employees, PINs and access", "Payment methods and journals", "Receipts, invoices and session rules"], "Bank and payment provider details."],
              ["Hardware &amp; payments", "Week 3", ["Printers, drawers, scanners, displays", "IoT Box and scales", "Card terminal and UPI QR", "Counter test with real bills"], "Devices on site and terminal credentials."],
              ["Train &amp; rehearse", "Week 4", ["Cashier and manager training", "Mock day with refunds and closing", "Offline drill", "Quick guides at each counter"], "Staff available for two short sessions."],
              ["Go-live &amp; support", "Week 4 onward", ["Opening day on site", "First closings checked with you", "Stock and accounts reconciled", "Monthly reviews and new stores"], "A go-live date and a store manager on hand."]]
    pbt = "".join('<li><button type="button" class="ps-ph%s" data-p12="%d" aria-pressed="%s"><span class="mono">%02d</span><b>%s</b><small>%s</small></button></li>'
                  % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", i + 1, n, w) for i, (n, w, d, y) in enumerate(phases))
    out += sec(head("SETUP TO GO-LIVE", "What Does Unisas Handle From POS Setup to Store Go-Live?",
                    "Six steps from your current billing system to a store running on Odoo, each ending with something you can test at the counter. Pick a step.", "is-center")
               + '<div class="ps-del" data-p12box><ol class="ps-phs">%s</ol><div class="ps-del-c ox-solo" aria-live="polite"><div><p class="ps-gi-h">Unisas delivers</p><ul class="ps-files" data-p12d></ul></div>'
                 '<div class="ps-del-y"><p class="ps-gi-h">We need from you</p><p data-p12y></p></div></div></div>' % pbt + data("ps-phases", phases), "ps-sec--del")

    # 13 ---- plan the implementation
    out += sec('<div class="ps-scope"><div>%s<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Plan my Odoo POS %s</a></div></div>'
               '<div class="ps-sc ox-solo" data-p13box><p class="ps-sc-h"><b>POS planner</b><small>A first recommendation. We confirm it after a short call.</small></p>'
               '<div class="ps-sc-in"><label class="is-wide"><span>What do you run?</span><select data-p13="type"><option value="0">Retail shops</option><option value="1">Restaurants or caf&eacute;s</option><option value="2">Supermarket / grocery</option><option value="3">Retail and food together</option></select></label>'
               '<label><span>Stores <b data-p13o="stores">2</b></span><input type="range" min="1" max="30" value="2" data-p13="stores"></label>'
               '<label><span>Counters per store <b data-p13o="counters">2</b></span><input type="range" min="1" max="10" value="2" data-p13="counters"></label>'
               '<label><span>Products <b data-p13o="prods">1,500</b></span><input type="range" min="100" max="30000" step="100" value="1500" data-p13="prods"></label>'
               '<label><span>Billing today</span><select data-p13="from"><option value="0">Manual / Excel</option><option value="1" selected>Standalone billing software</option><option value="2">Tally-based billing</option><option value="3">Another ERP</option></select></label>'
               '<div class="ps-sc-chk is-wide"><label><input type="checkbox" data-p13x="loyal" checked> Loyalty, gift cards or memberships</label><label><input type="checkbox" data-p13x="web"> Online store on the same stock</label>'
               '<label><input type="checkbox" data-p13x="card"> Integrated card terminal</label></div></div>'
               '<div class="ps-sc-out" data-p13out aria-live="polite"></div></div></div>'
               % (head("PLAN YOUR IMPLEMENTATION", "How Can We Plan an Odoo POS Implementation for Your Business?",
                       "The plan depends on how many stores and counters you have, what you sell, the hardware at each counter, and what your billing system holds today. "
                       "Answer a few questions for a first recommendation, then talk it through with us."), g["ARROW"]), "ps-sec--scope")

    return out + JS


CTA = ("Let's Plan a Checkout That Runs Your Whole Store",
       "Tell us about your stores, counters and how customers pay. We'll show you your products on the Odoo register and recommend the right setup, hardware and rollout plan.")

FAQ = [("Does Odoo POS work without internet?",
        "Yes. Once a session is open, the register keeps selling offline and saves orders on the device. They sync to Odoo when the connection returns. Card terminals and live UPI confirmation need a connection, so we set a fallback for each."),
       ("What hardware does Odoo POS support?",
        "Standard barcode scanners, receipt printers, cash drawers, customer displays and weighing scales, plus integrated card terminals in supported regions. Printers and scales usually connect through an Odoo IoT Box. We confirm your devices during scoping."),
       ("Can Odoo POS handle GST invoices and receipts?",
        "Yes. Products carry their GST rates and HSN codes, receipts show the tax breakdown, and a customer can ask for a GST invoice at the counter. Taxes are posted to the right accounts when the session closes."),
       ("Can we run several stores with different prices?",
        "Yes. Each store has its own POS and stock location, and pricelists can differ by store, customer group or season. Products, customers and loyalty stay shared."),
       ("Can Odoo POS be used in a restaurant?",
        "Yes. Restaurant mode adds floor plans, table orders, kitchen printing or a preparation display, bill splitting and tips."),
       ("How long does an Odoo POS implementation take?",
        "A single store with standard hardware is often live in three to four weeks. Multi-store rollouts, data migration from older billing systems and integrations add time; the planner above gives a first estimate.")]


JS = r'''<script>
(function(){
  function J(id){var e=document.getElementById(id);return e?JSON.parse(e.textContent):null;}
  function press(group,el){group.forEach(function(b){var on=b===el;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});}
  function num(n,d){return Number(n).toLocaleString('en-IN',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}
  function inr(n,d){return '&#8377; '+num(n,d===undefined?2:d);}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  var RED=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var TK='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var NO='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg>';

  /* --- 1 gaps --- */
  (function(){var bx=document.querySelector('[data-p1box]');if(!bx)return;var mb=[].slice.call(bx.querySelectorAll('[data-p1mode]'));
    var ITEMS=[['Cotton Kurta',1299],['Silk Stole',899],['Linen Kurta',1499],['Jhumkas',449],['Block-print Saree',2199],['Tote Bag',349]];
    var st={mode:'old',n:0,rev:0,closed:false,shelf:{},sys:{}};
    function reset(){st.n=0;st.rev=0;st.closed=false;st.sold=[];draw();}
    function draw(){var odoo=st.mode==='odoo',s=st.sold||[],pending=odoo?0:(st.closed?Math.max(0,s.length-Math.ceil(s.length*0.75)):s.length),
        unbooked=odoo?0:(st.closed?Math.round(st.rev*0.08):st.rev),cash=odoo?0:(st.closed&&s.length?340:0);
      bx.querySelector('[data-p1="pos"]').innerHTML='<b>'+st.n+'</b><small>bills printed</small><p>'+inr(st.rev,0)+' taken'+(s.length?'. Last: '+s[s.length-1]:'')+'</p>';
      bx.querySelector('[data-p1="inv"]').innerHTML=odoo?'<b class="is-ok">'+st.n+'</b><small>items deducted as sold</small><p>Shelf and system match, item by item.</p>'
        :'<b class="'+(pending?'is-bad':'')+'">'+pending+'</b><small>items still showing in stock</small><p>'+(st.closed?'Excel import at night missed a few lines.':'Stock sheet is updated at day end.')+'</p>';
      bx.querySelector('[data-p1="acc"]').innerHTML=odoo?'<b class="is-ok">'+(st.closed?inr(st.rev,0):'Posts at close')+'</b><small>'+(st.closed?'journal entry, by payment method':'one entry per session')+'</small><p>Cash, card and UPI already matched to orders.</p>'
        :'<b class="'+(unbooked?'is-bad':'')+'">'+inr(unbooked,0)+'</b><small>not yet in the books</small><p>'+(st.closed?'Re-typed in Tally; '+(cash?'cash short by &#8377; '+cash+', reason unknown.':''):'Accountant re-types the day&rsquo;s summary later.')+'</p>';
      var gaps=pending+(unbooked?1:0)+(cash?1:0);
      bx.querySelector('[data-p1msg]').innerHTML=!st.n?'Ring up a sale to start the day.':(odoo?'<b>0 gaps.</b> One sale, three apps updated together.':'<b>'+gaps+' gap'+(gaps===1?'':'s')+'</b> between checkout, stock and accounts'+(st.closed?' after closing.':' so far.'));
      bx.classList.toggle('is-odoo',odoo);}
    bx.querySelector('[data-p1sell]').addEventListener('click',function(){var it=ITEMS[st.n%ITEMS.length];st.n++;st.rev+=it[1];(st.sold=st.sold||[]).push(it[0]);draw();});
    bx.querySelector('[data-p1close]').addEventListener('click',function(){st.closed=true;draw();});
    bx.querySelector('[data-p1reset]').addEventListener('click',reset);
    mb.forEach(function(b){b.addEventListener('click',function(){press(mb,b);st.mode=b.getAttribute('data-p1mode');reset();});});reset();})();

  /* --- 2 the register --- */
  (function(){var bx=document.querySelector('[data-p2box]');if(!bx)return;var P=J('ps-prods'),C=J('ps-cats'),body=bx.querySelector('[data-p2body]'),fx=document.querySelector('[data-p2fx]'),q=bx.querySelector('[data-p2q]');
    var CUST=[['Meena Krishnan','98410 22314',1240,true],['Arun Prakash','99620 18820',310,true],['Shree Boutique','B2B &middot; GSTIN 33AAB...',0,false]];
    var st={scr:'reg',cat:null,lines:[],sel:null,mode:'qty',buf:'',cust:null,pays:[],pm:null,done:[],last:null};
    function p(id){return P.filter(function(x){return x[0]===id;})[0];}
    function total(){return st.lines.reduce(function(a,l){return a+l.q*l.pr*(1-l.d/100);},0);}
    function tax(){return st.lines.reduce(function(a,l){var t=l.q*l.pr*(1-l.d/100),r=p(l.id)[6];return a+t-t/(1+r/100);},0);}
    function paid(){return st.pays.reduce(function(a,x){return a+x.a;},0);}
    function lineHtml(l){var x=p(l.id),t=l.q*l.pr*(1-l.d/100);return '<li class="ps-ln'+(st.sel===l.id?' is-sel':'')+'" data-ln="'+l.id+'"><span class="ps-ln-n">'+x[1]+'</span><b>'+inr(t)+'</b><small>'+num(l.q,2)+' Units &times; '+inr(l.pr)+(l.d?' &middot; '+l.d+'% discount':'')+'</small></li>';}
    function grid(){var t=q.value.trim().toLowerCase();return P.filter(function(x){return (!st.cat||x[2]===st.cat)&&(!t||x[1].toLowerCase().indexOf(t)>-1);}).map(function(x){
      return '<button type="button" class="ps-pt" data-add="'+x[0]+'"><span class="ps-pt-img" style="--h:'+x[4]+'"></span><span class="ps-pt-n">'+x[1]+'</span><span class="ps-pt-p">'+inr(x[3])+'</span>'+(x[5]<=2?'<em>'+x[5]+' left</em>':'')+'</button>';}).join('')||'<p class="ps-empty">No product found.</p>';}
    function pad(){var K=['1','2','3','qty','4','5','6','disc','7','8','9','price','+/-','0','.','del'],L={qty:'Qty',disc:'%',price:'Price',del:'&#9003;'};
      return '<div class="ps-pad">'+K.map(function(k){return '<button type="button" class="'+(L[k]&&k!=='del'?'is-mode'+(st.mode===k?' is-on':''):'')+'" data-k="'+k+'">'+(L[k]||k)+'</button>';}).join('')+'</div>';}
    function reg(){var tot=total();
      return '<div class="ps-rg"><div class="ps-left"><ul class="ps-lines">'+(st.lines.length?st.lines.map(lineHtml).join(''):'<li class="ps-cart-e">Start adding products</li>')+'</ul>'+
        '<div class="ps-tot"><span>Total</span><b>'+inr(tot)+'</b><small>Taxes '+inr(tax())+'</small></div>'+
        '<div class="ps-act"><button type="button" class="ps-cbtn" data-do="cust">'+(st.cust!==null?'<b>'+CUST[st.cust][0]+'</b>':'Customer')+'</button><button type="button" class="ps-cbtn" data-do="note">Note</button>'+pad()+'<button type="button" class="ps-paybtn" data-do="pay"'+(st.lines.length?'':' disabled')+'>Payment</button></div></div>'+
        '<div class="ps-right"><div class="ps-cats"><button type="button" class="'+(st.cat?'':'is-on')+'" data-cat="">All</button>'+C.map(function(c){return '<button type="button" class="'+(st.cat===c?'is-on':'')+'" data-cat="'+c+'">'+c+'</button>';}).join('')+'</div><div class="ps-grid">'+grid()+'</div></div></div>';}
    function custScr(){return '<div class="ps-scr"><div class="ps-scr-h"><button type="button" class="ox-sbtn" data-do="back">&larr; Back</button><b>Customers</b><button type="button" class="ox-sbtn">Create</button></div>'+
      '<table class="ox-table ps-cust-t"><thead><tr><th>Name</th><th>Phone</th><th class="ox-num">Loyalty Points</th></tr></thead><tbody>'+CUST.map(function(c,i){return '<tr data-cust="'+i+'"><td><b>'+c[0]+'</b></td><td>'+c[1]+'</td><td class="ox-num">'+(c[3]?num(c[2]):'&mdash;')+'</td></tr>';}).join('')+'</tbody></table></div>';}
    function payScr(){var tot=total(),pd=paid(),rem=tot-pd,M=[['cash','Cash'],['card','Card (Razorpay)'],['upi','UPI QR']];
      return '<div class="ps-scr ps-pay"><div class="ps-scr-h"><button type="button" class="ox-sbtn" data-do="back">&larr; Back</button><b>Payment</b><span></span></div><div class="ps-pay-g"><div class="ps-pms">'+
        M.map(function(m){return '<button type="button" data-pm="'+m[0]+'">'+m[1]+'</button>';}).join('')+'</div><div class="ps-pay-m"><div class="ps-due"><small>'+(rem>0.005?'Remaining':'Change')+'</small><b>'+inr(Math.abs(rem))+'</b></div>'+
        '<ul class="ps-plines">'+st.pays.map(function(x,i){return '<li><span>'+x.n+'</span><b>'+inr(x.a)+'</b><button type="button" data-rmp="'+i+'" aria-label="Remove">&times;</button></li>';}).join('')+'</ul>'+
        (st.pays.some(function(x){return x.k==='cash';})?'<div class="ps-quick">'+[500,1000,2000].map(function(v){return '<button type="button" data-qa="'+v+'">+'+num(v)+'</button>';}).join('')+'</div>':'')+
        (st.pays.some(function(x){return x.k==='upi';})?'<p class="ps-qrline"><span class="ps-qr" aria-hidden="true"></span>QR shown on the customer display</p>':'')+
        '<div class="ps-pay-f"><span>'+(st.cust!==null?'Customer: <b>'+CUST[st.cust][0]+'</b>':'<button type="button" class="ps-link" data-do="cust">Add customer</button>')+'</span><button type="button" class="ps-val" data-do="validate"'+(rem>0.005||!st.pays.length?' disabled':'')+'>Validate</button></div></div></div></div>';}
    function rcpt(){var o=st.last;return '<div class="ps-scr ps-rc"><div class="ps-rc-ok">'+TK+'<b>Payment Successful</b><span>'+inr(o.tot)+(o.change>0.005?' &middot; change '+inr(o.change):'')+'</span><div class="ps-rc-b"><button type="button" class="ox-sbtn">Print Receipt</button><button type="button" class="ox-sbtn">Send by WhatsApp</button></div><button type="button" class="ps-val" data-do="new">New Order</button></div>'+
      '<div class="ps-paper"><p class="ps-paper-h"><b>Nila Threads</b><small>T. Nagar, Chennai &middot; GSTIN 33ABCDE1234F1Z5</small></p>'+o.lines.map(function(l){return '<p><span>'+l.n+'<small>'+num(l.q,2)+' &times; '+inr(l.pr)+(l.d?' &middot; -'+l.d+'%':'')+'</small></span><b>'+inr(l.t)+'</b></p>';}).join('')+
      '<p class="is-tot"><span>TOTAL</span><b>'+inr(o.tot)+'</b></p><p class="is-sm"><span>incl. GST</span><span>'+inr(o.tax)+'</span></p>'+o.pays.map(function(x){return '<p class="is-sm"><span>'+x.n+'</span><span>'+inr(x.a)+'</span></p>';}).join('')+
      '<p class="ps-paper-f">'+o.ref+' &middot; Served by Anitha'+(o.cust?'<br>'+o.cust+' &middot; +'+o.pts+' points':'')+'</p></div></div>';}
    function orders(){return '<div class="ps-scr"><div class="ps-scr-h"><b>Orders</b><span></span><span class="ps-muted">Session POS/00042</span></div>'+(st.done.length?'<table class="ox-table ps-cust-t"><thead><tr><th>Order</th><th>Customer</th><th>Payment</th><th class="ox-num">Total</th><th>Status</th></tr></thead><tbody>'+
      st.done.slice().reverse().map(function(o){return '<tr><td>'+o.ref+'</td><td>'+(o.cust||'&mdash;')+'</td><td>'+o.pays.map(function(x){return x.n;}).join(', ')+'</td><td class="ox-num">'+inr(o.tot)+'</td><td><span class="ps-paid">Paid</span></td></tr>';}).join('')+'</tbody></table>':'<p class="ps-empty">No paid orders yet in this session.</p>')+'</div>';}
    function render(){bx.querySelector('[data-p2n]').textContent=st.done.length;
      [].forEach.call(bx.querySelectorAll('[data-p2nav]'),function(b){b.classList.toggle('is-on',(b.getAttribute('data-p2nav')==='orders')===(st.scr==='orders'));});
      body.innerHTML={reg:reg,cust:custScr,pay:payScr,rcpt:rcpt,orders:orders}[st.scr]();}
    function effects(o){var fxl=[];o.lines.forEach(function(l){var x=p(l.id),before=x[5];x[5]=Math.max(0,x[5]-l.q);fxl.push(['Inventory','T. Nagar/Stock &rarr; Customers: '+l.n+' &times; '+num(l.q)+' (on hand '+before+' &rarr; '+x[5]+')'+(x[5]<=1?' &middot; reorder rule triggered':''),'#1F8A78']);});
      if(o.cust)fxl.push(['Loyalty','+'+o.pts+' points for '+o.cust,'#8E4F83']);
      fxl.push(['Session','POS/00042: order '+st.done.length+', '+inr(o.tot)+' by '+o.pays.map(function(x){return x.n;}).join(' + ')+(o.change>0.005?' (change '+inr(o.change)+' given)':''),'#B8325A']);
      fxl.push(['Accounting','Posted with the session at Closing Register: sales and GST '+inr(o.tax)+' by rate','#B7791F']);
      fx.innerHTML=fxl.map(function(f,i){return '<li style="--c:'+f[2]+';--i:'+i+'"><b>'+f[0]+'</b><span>'+f[1]+'</span></li>';}).join('');}
    function key(k){var l=st.lines.filter(function(x){return x.id===st.sel;})[0];
      if(k==='qty'||k==='disc'||k==='price'){st.mode=k;st.buf='';render();return;}if(!l)return;
      if(k==='del'){if(st.buf){st.buf=st.buf.slice(0,-1);}else if(st.mode==='qty'){st.lines=st.lines.filter(function(x){return x!==l;});st.sel=st.lines.length?st.lines[st.lines.length-1].id:null;render();return;}}
      else if(k==='+/-'){if(st.mode==='qty')l.q=-l.q;render();return;}else st.buf+=k;
      var v=parseFloat(st.buf||'0');if(st.mode==='qty'){if(st.buf)l.q=v;}if(st.mode==='disc')l.d=Math.min(100,v);if(st.mode==='price'&&st.buf)l.pr=v;render();}
    body.addEventListener('click',function(e){var a;
      if((a=e.target.closest('[data-add]'))){var id=+a.getAttribute('data-add'),x=p(id),l=st.lines.filter(function(y){return y.id===id;})[0];if(l)l.q+=1;else st.lines.push({id:id,q:1,pr:x[3],d:0});st.sel=id;st.mode='qty';st.buf='';render();return;}
      if((a=e.target.closest('[data-cat]'))){st.cat=a.getAttribute('data-cat')||null;render();return;}
      if((a=e.target.closest('[data-ln]'))){st.sel=+a.getAttribute('data-ln');st.buf='';render();return;}
      if((a=e.target.closest('[data-k]'))){key(a.getAttribute('data-k'));return;}
      if((a=e.target.closest('[data-cust]'))){st.cust=+a.getAttribute('data-cust');st.scr=st.back||'reg';render();return;}
      if((a=e.target.closest('[data-pm]'))){var k=a.getAttribute('data-pm'),rem=Math.max(0,total()-paid());st.pays.push({k:k,n:a.textContent,a:Math.round(rem*100)/100});render();return;}
      if((a=e.target.closest('[data-rmp]'))){st.pays.splice(+a.getAttribute('data-rmp'),1);render();return;}
      if((a=e.target.closest('[data-qa]'))){var c=st.pays.filter(function(x){return x.k==='cash';})[0];c.a+=+a.getAttribute('data-qa');render();return;}
      if(!(a=e.target.closest('[data-do]')))return;var d=a.getAttribute('data-do');
      if(d==='cust'){st.back=st.scr;st.scr='cust';}
      if(d==='back')st.scr=st.scr==='cust'?(st.back||'reg'):'reg';
      if(d==='note')return;
      if(d==='pay')st.scr='pay';
      if(d==='validate'){var tot=total(),c2=st.cust!==null?CUST[st.cust]:null,o={ref:'Order 00042-002-'+('000'+(st.done.length+1)).slice(-4),tot:tot,tax:tax(),change:paid()-tot,pays:st.pays.slice(),cust:c2?c2[0]:null,pts:c2&&c2[3]?Math.floor(tot/10):0,
          lines:st.lines.map(function(l){return {id:l.id,n:p(l.id)[1],q:l.q,pr:l.pr,d:l.d,t:l.q*l.pr*(1-l.d/100)};})};
        if(c2&&c2[3])c2[2]+=o.pts;st.done.push(o);st.last=o;effects(o);st.scr='rcpt';}
      if(d==='new'){st.lines=[];st.sel=null;st.pays=[];st.cust=null;st.scr='reg';}
      render();});
    bx.addEventListener('click',function(e){var n=e.target.closest('[data-p2nav]');if(n){st.scr=n.getAttribute('data-p2nav')==='orders'?'orders':'reg';render();}});
    q.addEventListener('input',function(){st.scr='reg';render();});
    fx.innerHTML='<li class="is-wait"><span>Validate a payment to see the stock, loyalty, session and accounting updates.</span></li>';render();})();

  /* --- 4 offline --- */
  (function(){var bx=document.querySelector('[data-p4box]');if(!bx)return;var net=bx.querySelector('[data-p4net]'),T=['Cotton Kurta','Silk Stole + Jhumkas','Block-print Saree','Tote Bag','Linen Kurta x2','Phulkari Dupatta'],AM=[1299,1348,2199,349,2998,1199];
    var st={n:0,local:[],srv:[['Order 00042-002-0001','10:12',3096,'Synced']],t:12};
    function draw(){var on=net.checked;bx.classList.toggle('is-off',!on);
      bx.querySelector('[data-p4q]').innerHTML=st.local.length?st.local.length+' to sync':'';
      bx.querySelector('[data-p4s]').innerHTML=on?'<b>Online.</b> Orders reach Odoo as they are paid.':'<b>Offline.</b> Keep selling: orders are saved on this device.';
      bx.querySelector('[data-p4local]').innerHTML=st.local.map(function(o){return '<li><span>'+o[0]+'</span><b>'+inr(o[2])+'</b><small>Saved on device</small></li>';}).join('');
      bx.querySelector('[data-p4srv]').innerHTML=st.srv.slice().reverse().map(function(o){return '<tr class="'+(o[3]==='new'?'is-new':'')+'"><td>'+o[0]+'</td><td>'+o[1]+'</td><td>Anitha</td><td class="ox-num">'+inr(o[2])+'</td><td><span class="ps-paid">Paid</span></td></tr>';}).join('');
      st.srv.forEach(function(o){if(o[3]==='new')o[3]='Synced';});}
    function sync(){if(!net.checked||!st.local.length)return;var o=st.local.shift();o[3]='new';st.srv.push(o);draw();setTimeout(sync,RED?0:500);}
    bx.querySelector('[data-p4sell]').addEventListener('click',function(){var i=st.n%T.length;st.n++;st.t+=7;var o=['Order 00042-002-'+('000'+(st.n+1)).slice(-4),'10:'+('0'+(st.t%60)).slice(-2),AM[i],''];
      if(net.checked){o[3]='new';st.srv.push(o);}else st.local.push(o);draw();});
    net.addEventListener('change',function(){draw();setTimeout(sync,RED?0:400);});draw();})();

  /* --- 6 session close --- */
  (function(){var bx=document.querySelector('[data-p6box]');if(!bx)return;var O=J('ps-orders'),MV=J('ps-moves'),b=bx.querySelector('[data-p6b]'),tabs=[].slice.call(bx.querySelectorAll('[data-p6t]')),closed=false,cur=0;
    var by={},tot=0;O.forEach(function(o){by[o[2]]=(by[o[2]]||0)+o[3];tot+=o[3];});bx.querySelector('[data-p6tot]').innerHTML=inr(tot);
    function draw(){if(!closed){b.innerHTML='<p class="ps-wait">The session is still open. Orders have already moved stock; press <b>Close Register</b> to post the accounting entry.</p>'+(cur===1?mv():'');return;}
      if(cur===0){var g12=Math.round(tot*0.83),g5=tot-g12,t12=g12-g12/1.12,t5=g5-g5/1.05,sales=tot-t12-t5;
        var R=[['Cash','1001 Cash T. Nagar',by.Cash,0],['Card','1012 Razorpay clearing',by.Card,0],['UPI','1013 UPI clearing',by.UPI,0],['Sales','4000 POS Sales',0,sales],['GST 12%','CGST + SGST output',0,t12],['GST 5%','CGST + SGST output',0,t5]];
        b.innerHTML='<p class="ps-je-h"><b>POSS/2026/10/0042</b><span class="ps-paid">Posted</span></p><table class="ox-table ps-je"><thead><tr><th>Account</th><th>Label</th><th class="ox-num">Debit</th><th class="ox-num">Credit</th></tr></thead><tbody>'+
          R.map(function(r,i){return '<tr style="--i:'+i+'"><td>'+r[1]+'</td><td>'+r[0]+'</td><td class="ox-num">'+(r[2]?inr(r[2]):'')+'</td><td class="ox-num">'+(r[3]?inr(r[3]):'')+'</td></tr>';}).join('')+
          '</tbody><tfoot><tr><td colspan="2"><b>Balanced</b></td><td class="ox-num"><b>'+inr(tot)+'</b></td><td class="ox-num"><b>'+inr(tot)+'</b></td></tr></tfoot></table><p class="ps-note">One entry for the whole session, split by payment method and GST rate. Card and UPI clearing accounts are matched to the bank later.</p>';}
      if(cur===1)b.innerHTML=mv();
      if(cur===2)b.innerHTML='<ul class="ps-rep">'+MV.filter(function(m){return m[3];}).map(function(m,i){return '<li style="--i:'+i+'"><b>'+m[0]+'</b><span>Below minimum (2). Reordering rule added to <b>P0008'+(7+i)+'</b>, draft RFQ to Kanchi Weavers.</span></li>';}).join('')+'</ul><p class="ps-note">Purchasing confirms the RFQs; when goods arrive they are received straight into T. Nagar stock.</p>';}
    function mv(){return '<table class="ox-table ps-je"><thead><tr><th>Product</th><th>From &rarr; To</th><th class="ox-num">Qty</th><th class="ox-num">On hand</th></tr></thead><tbody>'+MV.map(function(m,i){return '<tr style="--i:'+i+'"><td>'+m[0]+'</td><td>TNGR/Stock &rarr; Customers</td><td class="ox-num">'+m[1]+'</td><td class="ox-num">'+m[2]+'</td></tr>';}).join('')+'</tbody></table>';}
    tabs.forEach(function(t){t.addEventListener('click',function(){press(tabs,t);cur=+t.getAttribute('data-p6t');draw();});});
    bx.querySelector('[data-p6close]').addEventListener('click',function(e){closed=true;e.target.disabled=true;e.target.textContent='Closed';draw();});draw();})();

  /* --- 8 hardware --- */
  (function(){var bx=document.querySelector('[data-p8box]');if(!bx)return;var D=J('ps-devs'),pins=[].slice.call(bx.querySelectorAll('[data-p8]')),card=bx.querySelector('[data-p8card]'),cur=0,tested={};
    function draw(){var d=D[cur],t=tested[cur];card.innerHTML='<p class="ps-hw-h"><span class="ps-dev-i is-'+d[0]+'" aria-hidden="true"></span><span><b>'+d[1]+'</b><small>'+d[2]+'</small></span></p><ul class="ps-hw-l">'+
      d[3].map(function(x,i){return '<li class="'+(t?'is-ok':'')+'" style="--i:'+i+'">'+(t?TK:'<i></i>')+x+'</li>';}).join('')+'</ul>'+
      '<button type="button" class="ox-pbtn" data-p8test'+(t?' disabled':'')+'>'+(t?'Tested at the counter':'Run counter test')+'</button><p class="ps-hw-n">'+Object.keys(tested).length+' of '+D.length+' devices tested</p>';}
    pins.forEach(function(b){b.addEventListener('click',function(){press(pins,b);cur=+b.getAttribute('data-p8');draw();});});
    card.addEventListener('click',function(e){if(e.target.closest('[data-p8test]')){tested[cur]=1;pins[cur].classList.add('is-ok');draw();}});draw();})();

  /* --- 9 omnichannel --- */
  (function(){var bx=document.querySelector('[data-p9box]');if(!bx)return;var S=J('ps-scen'),bt=[].slice.call(bx.querySelectorAll('[data-p9]'));
    function draw(i){var s=S[i];bx.querySelector('[data-p9steps]').innerHTML=s[1].map(function(x,j){return '<li style="--i:'+j+'"><span class="ps-st-n">'+(j+1)+'</span><span><small>'+x[0]+'</small><b>'+x[1]+'</b><em>'+x[2]+'</em></span></li>';}).join('');
      bx.querySelector('[data-p9pts]').textContent=num(1240+s[2]);}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);draw(+b.getAttribute('data-p9'));});});draw(0);})();

  /* --- 11 insights --- */
  (function(){var bx=document.querySelector('[data-p11box]');if(!bx)return;var R=J('ps-rep'),g=bx.querySelector('[data-p11g]'),mb=[].slice.call(bx.querySelectorAll('[data-p11m]')),m='rev';
    var INS={store:'T. Nagar sells most, but the caf&eacute; has the most orders: a small average order worth bundling with a retail offer.',hour:'Half the day&rsquo;s revenue comes after 4 pm. Two cashiers from 4 to 8 pm cuts the queue.',
      cat:'Kurtas lead revenue with many small orders; sarees are fewer but bigger. Stock and staff training should follow that.',emp:'Anitha&rsquo;s average order is highest; her add-on selling is worth sharing with the team.'};
    function val(r){return m==='rev'?r[1]:(m==='cnt'?r[2]:r[1]/r[2]);}
    function draw(){var rows=R[g.value],mx=Math.max.apply(null,rows.map(val));
      bx.querySelector('[data-p11bars]').innerHTML=rows.map(function(r,i){var v=val(r);return '<div class="ps-bar" style="--i:'+i+'"><span>'+r[0]+'</span><i style="--p:'+(v/mx*100)+'"></i><b>'+(m==='cnt'?num(v):inr(v,0))+'</b></div>';}).join('');
      var tr=rows.reduce(function(a,r){return a+r[1];},0),tc=rows.reduce(function(a,r){return a+r[2];},0);
      bx.querySelector('[data-p11ins]').innerHTML='<p class="ps-gi-h">October so far</p><div class="ps-kp"><span><b>'+inr(tr,0)+'</b>Revenue</span><span><b>'+num(tc)+'</b>Orders</span><span><b>'+inr(tr/tc,0)+'</b>Average order</span></div><p class="ps-gi-h">What it tells you</p><p class="ps-ins">'+INS[g.value]+'</p>';}
    mb.forEach(function(b){b.addEventListener('click',function(){mb.forEach(function(x){x.classList.toggle('is-on',x===b);});m=b.getAttribute('data-p11m');draw();});});g.addEventListener('change',draw);draw();})();

  /* --- 12 phases --- */
  (function(){var bx=document.querySelector('[data-p12box]');if(!bx)return;var P=J('ps-phases'),bt=[].slice.call(bx.querySelectorAll('[data-p12]'));
    function draw(i){bx.querySelector('[data-p12d]').innerHTML=P[i][2].map(function(d,j){return '<li style="--i:'+j+'"><span class="ps-file" aria-hidden="true"></span>'+d+'</li>';}).join('');bx.querySelector('[data-p12y]').innerHTML=P[i][3];}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);draw(+b.getAttribute('data-p12'));});});draw(0);})();

  /* --- 13 planner --- */
  (function(){var bx=document.querySelector('[data-p13box]');if(!bx)return;
    function v(k){return +bx.querySelector('[data-p13="'+k+'"]').value;}function x(k){return bx.querySelector('[data-p13x="'+k+'"]').checked;}
    function draw(){var t=v('type'),s=v('stores'),c=v('counters'),p=v('prods'),f=v('from');
      bx.querySelector('[data-p13o="stores"]').textContent=s;bx.querySelector('[data-p13o="counters"]').textContent=c;bx.querySelector('[data-p13o="prods"]').textContent=num(p);
      var wk=3+(s>3?1:0)+(s>10?2:0)+(p>8000?1:0)+(f>=2?1:0)+(t===3?1:0)+(x('web')?1:0)+(x('card')?0.5:0)+(x('loyal')?0.5:0);
      var pk=s===1?['Single-store POS','One store, live in weeks']:(s<=5?['Multi-store POS','Pilot store first, then the rest']:['Store rollout programme','Pilot, then waves of stores']);
      var apps=['Point of Sale','Inventory','Invoicing'];if(t===1||t===3)apps.push('Restaurant');if(x('loyal'))apps.push('Loyalty');if(x('web'))apps.push('eCommerce');if(p>8000||f>=2)apps.push('Data migration');
      var ask=['Your counters and the hardware at each one'];if(f===1||f===2)ask.push('Exporting products, customers and stock from your billing system');if(x('card'))ask.push('Your card acquirer and terminal model');if(s>3)ask.push('Which store pilots first');if(t>=1)ask.push('Menu, kitchen stations and table layout');
      bx.querySelector('[data-p13out]').innerHTML='<div class="ps-pk"><p class="mono">RECOMMENDED</p><b>'+pk[0]+'</b><small>'+pk[1]+' &middot; '+num(s*c)+' counter'+(s*c>1?'s':'')+'</small><span class="ps-pk-wk">'+(Math.round(wk*2)/2)+'&ndash;'+(Math.round(wk*2)/2+2)+' weeks</span></div>'+
        '<div><p class="ps-gi-h">Apps</p><p class="ps-chips">'+apps.map(function(a){return '<span>'+a+'</span>';}).join('')+'</p><p class="ps-gi-h">We&rsquo;ll ask about</p><ul class="ps-ask">'+ask.map(function(a){return '<li>'+a+'</li>';}).join('')+'</ul></div>';}
    bx.addEventListener('input',draw);bx.addEventListener('change',draw);draw();})();
})();
</script>
'''
