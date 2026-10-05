"""
Odoo Email Marketing page (odoo-email-marketing.html). Every screen is modelled on the real Odoo 20
Email Marketing and Marketing Automation apps (demo.odoo.com/odoo/email-marketing): the Mailings app in Kanban,
List, Calendar and Graph views, the mailing form
with its Draft / In Queue / Sending / Sent status bar, Send, Schedule and Test buttons, the Recipients
domain editor, mail templates, the A/B Tests tab, mailing statistics and smart buttons (Leads,
Quotations, Revenues), Link Tracker, Settings, the Marketing Automation workflow with Opened /
Not opened / Clicked triggers, and the public "manage your subscriptions" page.
Sample company: a Madurai spice and ready-mix maker selling online, to retailers and to distributors,
under the fictional brand "Amudha Spices". Shared Odoo look: odoo-ui.css. Page styles: email-marketing.css.

hero(g) and build(g) get the build script's globals.
"""
import json

import crm_explorer as ox

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


V_CAL = ox.ic('<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 10h16M9 3v4M15 3v4"/>', 16, 1.9)


def head(eyebrow, title, sub="", cls=""):
    return ('<div class="em-head%s"><p class="em-eyebrow mono">%s</p><h2 class="em-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="em-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="em-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


def data(sid, obj):
    """JSON for the page script, safe inside a <script> element."""
    return '<script type="application/json" id="%s">%s</script>' % (sid, json.dumps(obj).replace("</", "<\\/"))


def ox_head(a, b, right=""):
    return ('<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>%s</a><span>%s</span></span></div><span></span>%s</div>'
            % (a, b, right or "<span></span>"))


def pressed(cls, attr, items, label):
    """A row of toggle buttons, the first one pressed."""
    return "".join('<button type="button" class="%s%s" %s="%d" aria-pressed="%s">%s</button>'
                   % (cls, " is-on" if i == 0 else "", attr, i, "true" if i == 0 else "false", label(x)) for i, x in enumerate(items))


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">Email Marketing</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["Audiences from CRM &amp; sales data", "Scheduled, tested campaigns", "Opens, clicks &amp; revenue in one report"])
    copy = ('<div class="em-hero-copy">%s<p class="em-eyebrow mono">ODOO EMAIL MARKETING IMPLEMENTATION</p>'
            '<h1 class="em-h1">Powerful <span>Email Marketing Software</span> with Odoo</h1>'
            '<p class="em-lead">Unisas sets up Odoo Email Marketing on the same database as your contacts, CRM and sales. Every campaign goes to a segment you can trust, '
            'lands in the inbox at the right hour, and reports the leads, quotations and orders it brought in.</p>'
            '<ul class="em-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Plan your email marketing %s</a>'
            '<a href="#compose" class="btn btn-ghost">Build a mailing</a></div></div>' % (crumb, points, g["ARROW"]))
    mail = ('<div class="em-hx-mail"><div class="em-hx-top"><span class="em-hx-from"><i>A</i><span><b>Amudha Spices</b><small>to Sri Murugan Stores</small></span></span><small>Tue 07:30</small></div>'
            '<p class="em-hx-subj">Diwali gift boxes: 15% off bulk orders till 25 Oct</p>'
            '<div class="em-hx-body"><div class="em-hx-ban"><small class="mono">DIWALI 2026 &middot; FOR RETAILERS</small><strong>Gift boxes your customers will ask for</strong><span>Order for my store</span></div></div></div>')
    steps = [("Sent", "1,712", 100, "#F2B33D"), ("Opened", "910", 86, "#E58A2E"), ("Clicked", "325", 72, "#C9622A"), ("Leads", "46", 58, "#A2473A"), ("Quotations", "31", 46, "#714B67")]
    fun = ('<div class="em-hv-fun"><p class="mono"><span>DIWALI TRADE OFFER</span><span>RESULTS</span></p><ol>'
           + "".join('<li style="--w:%d;--c:%s;--i:%d"><span>%s</span><b>%s</b></li>' % (w, c, i, n, v) for i, (n, v, w, c) in enumerate(steps))
           + '</ol><p class="em-hv-rev"><span>Revenue from this one email</span><b>&#8377; 18,40,000</b></p></div>')
    plane = ('<svg class="em-hv-plane" viewBox="0 0 260 160" aria-hidden="true"><path d="M6 150 C 70 146, 92 52, 160 66 S 228 52, 232 22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="4 7" opacity=".55"/>'
             '<path d="M224 12 L256 2 L242 32 L236 20 Z M236 20 L256 2" fill="currentColor" stroke="currentColor" stroke-width="1" stroke-linejoin="round"/></svg>')
    return ('<section class="em-hero">' + copy + '<div class="em-hero-vis em-hv" aria-label="A retailer email from Odoo Email Marketing and its results: sent, opened, clicked, leads, quotations and revenue">'
            + plane + mail + fun + '</div></section>')

# ------------------------------------------------------------------ sections
def build(g):
    out = ""
    app_icon = g["TILE_ICONS"][9]

    # 1 ---- right customers, right time
    types = {"ret": ["Retailers", "#B5541B"], "dist": ["Distributors", "#714B67"], "home": ["Home cooks", "#1F8A78"],
             "rep": ["Repeat buyers", "#2F6BD8"], "lap": ["Lapsed 90+ days", "#8A8F98"], "new": ["New subscribers", "#C98600"]}
    order = "home rep ret home new lap home rep dist home ret lap new home rep home ret lap home rep new home lap ret home rep dist home new lap " \
            "rep home ret home lap rep new home ret lap home rep home new dist ret home lap rep home new home ret lap rep home".split()
    camps = [["Diwali trade offer", "Gift boxes at trade price", ["ret", "dist"], "Tue 07:30", "before shops open"],
             ["New: Chettinad Sambar Mix", "Product launch with a recipe", ["home", "rep", "new"], "Thu 19:00", "when dinner is planned"],
             ["We miss you: 10% back", "Win-back offer", ["lap"], "Sat 10:00", "weekend shopping hour"]]
    leg = "".join('<li><i style="background:%s"></i>%s</li>' % (c, n) for n, c in types.values())
    out += sec(head("RIGHT PEOPLE, RIGHT TIME", "Are Your Email Campaigns Reaching the Right Customers at the Right Time?",
                    "One newsletter to the whole list is easy to send and expensive in unsubscribes. Pick a campaign, then compare sending it to everyone at one time "
                    "with sending it to the right segment at the hour they read email.", "is-center")
               + '<div class="em-aim" data-e1box><div class="em-aim-l"><div class="em-camps" role="group" aria-label="Campaign">%s</div>'
                 '<div class="em-aim-card ox-solo"><div class="em-mode" role="group" aria-label="Sending method"><button type="button" class="is-on" data-e1mode="all" aria-pressed="true">Everyone, one time</button>'
                 '<button type="button" data-e1mode="seg" aria-pressed="false">Odoo segment, best time</button></div>'
                 '<div class="em-dots" data-e1dots aria-hidden="true"></div><ul class="em-leg">%s</ul><p class="em-when" data-e1when></p></div></div>'
                 '<div class="em-aim-r ox-solo" aria-live="polite"><p class="mono">ONE SEND, 12,300 CONTACTS</p><ul class="em-kpis" data-e1kpis></ul><p class="em-aim-msg" data-e1msg></p></div></div>'
                 % (pressed("em-camp", "data-e1", camps, lambda c: "<b>%s</b><small>%s</small>" % (c[0], c[1])), leg)
               + data("em-types", types) + data("em-order", order) + data("em-camps", camps), "em-sec--aim")

    # 2 ---- recipients domain editor
    models = {
        "contact": {"label": "Contact", "base": 12400, "cols": ["Name", "Tags", "State", "Orders", "Last order"],
                    "rows": [["Sri Murugan Stores", "Retailer", "Tamil Nadu", 14, 12], ["Lakshmi Ramesh", "Home cook", "Tamil Nadu", 3, 140],
                             ["Annapoorna Supermarket", "Retailer", "Kerala", 22, 8], ["Deepa Krishnan", "Home cook", "Karnataka", 0, -1],
                             ["Velan Traders", "Distributor", "Tamil Nadu", 31, 20], ["Kavitha Sundar", "Home cook", "Tamil Nadu", 6, 35],
                             ["Fresh Basket Mart", "Retailer", "Tamil Nadu", 9, 120], ["Rahul Menon", "Home cook", "Kerala", 1, 200],
                             ["Meena Provisions", "Retailer", "Tamil Nadu", 0, -1], ["Arjun Iyer", "Home cook", "Tamil Nadu", 2, 95]],
                    "rules": [["Tags", "contains", "Retailer", 0.14, 1, "eq", "Retailer"], ["State", "is in", "Tamil Nadu", 0.58, 2, "eq", "Tamil Nadu"],
                              ["Sale Order Count", "is greater than", "0", 0.46, 3, "gt", 0], ["Last Order Date", "is before", "90 days ago", 0.22, 4, "gt", 90]]},
        "lead": {"label": "Lead/Opportunity", "base": 1960, "cols": ["Opportunity", "Stage", "Tags", "Salesperson"],
                 "rows": [["Diwali stock: 60 boxes", "Qualified", "Bulk order", "Priya Raman"], ["New stockist, Trichy", "New", "Stockist", "Karthik S"],
                          ["Hotel chain spice supply", "Proposition", "Bulk order", "Priya Raman"], ["Corporate Diwali gifting", "New", "Bulk order", "Karthik S"],
                          ["Supermarket shelf space", "Qualified", "Stockist", "Priya Raman"], ["Export enquiry, Singapore", "New", "Export", "Anitha M"]],
                 "rules": [["Stage", "is in", "New, Qualified", 0.55, 1, "in", ["New", "Qualified"]], ["Tags", "contains", "Bulk order", 0.3, 2, "eq", "Bulk order"],
                           ["Salesperson", "is in", "Priya Raman", 0.4, 3, "eq", "Priya Raman"]]},
    }
    lists = [["Newsletter", 8912, True], ["Recipe Club", 4380, False], ["Retailer offers", 1736, False], ["Distributors", 212, False]]
    out += sec(head("TARGETED AUDIENCES", "How Can Odoo Organize Contacts Into Targeted Email Audiences?",
                    "In Odoo the audience is part of the mailing. Choose mailing lists, or point the mailing at contacts, leads or customers and filter them by anything Odoo knows: "
                    "tags, location, orders, stage or salesperson. Turn rules on and off and watch the recipient count.", "is-center")
               + '<div class="em-aud" data-e2box><div class="ox em-ox">%s<div class="em-rcp"><div class="em-fld"><span class="em-lbl">Recipients</span><div class="em-seg" role="group" aria-label="Recipients">'
                 '<button type="button" class="is-on" data-e2m="list" aria-pressed="true">Mailing List</button><button type="button" data-e2m="contact" aria-pressed="false">Contact</button>'
                 '<button type="button" data-e2m="lead" aria-pressed="false">Lead/Opportunity</button></div></div><div data-e2body></div></div></div>'
                 '<div class="em-aud-r ox-solo" aria-live="polite"><p class="em-cnt"><b data-e2n>0</b><span>records</span></p><p class="em-cnt-s" data-e2s></p>'
                 '<ul class="em-clean"><li>%s Blocklisted addresses removed</li><li>%s Opted-out list members skipped</li><li>%s Duplicate emails sent once</li></ul></div></div>'
                 % (ox_head("Mailings", "Diwali trade offer"), TICK, TICK, TICK)
               + data("em-models", models) + data("em-lists", lists), "em-sec--aud")

    # 3 ---- segments to workflows
    segs = [["New subscribers", "~380 a month", "Signed up on the website or at an expo stall", "Marketing Automation",
             "Contact &middot; on list <b>Newsletter</b> &middot; created in the last 24 hours",
             [["Day 0", "Welcome + recipe e-book"], ["Day 1", "10% first-order code, if opened"], ["Day 4", "Reminder, if code not used"]],
             "First orders within 14 days", "Moved to Recipe Club after the first order"],
            ["Home cooks &amp; repeat buyers", "2,460 contacts", "Bought online at least twice", "Email Marketing mailings",
             "Contact &middot; tag <b>Home cook</b> &middot; Sale Order Count &gt; 1",
             [["Monthly", "Recipe newsletter"], ["Launches", "New product mailer"], ["Festivals", "Festive offer, Thu 19:00"]],
             "Repeat-order rate, revenue per email", "Website orders tagged with the campaign"],
            ["Lapsed customers", "1,230 contacts", "No order in 90 days", "Marketing Automation",
             "Contact &middot; Last Order Date before 90 days ago &middot; not blocklisted",
             [["Day 0", "&lsquo;We miss you&rsquo; with best sellers"], ["Day 3", "10% back code, if no order"], ["Day 30", "Moved to a quiet list, if never opened"]],
             "Win-back orders, list health", "Reactivated customers reported in Sales"],
            ["Retailers", "1,736 contacts", "Shops that stock Amudha products", "Mailings + automation",
             "Contact &middot; tag <b>Retailer</b> &middot; on list <b>Retailer offers</b>",
             [["Tue 07:30", "Monthly trade offer"], ["On click", "&lsquo;Bulk order&rsquo; creates a CRM lead"], ["24 h", "Salesperson calls the shop"]],
             "Leads, quotations and trade revenue", "Lead to the territory salesperson"],
            ["Distributors", "212 contacts", "Area distributors with credit terms", "Plain-text mailings",
             "Contact &middot; tag <b>Distributor</b> &middot; Salesperson is set",
             [["Quarterly", "Price list from the area manager"], ["On reply", "Reply lands in the manager&rsquo;s inbox"], ["Logged", "Conversation saved on the contact"]],
             "Replies and price-list downloads", "Account manager follows up"],
            ["Expo &amp; event leads", "~640 per event", "Scanned at trade fairs and food expos", "Marketing Automation",
             "Lead &middot; source <b>Expo</b> &middot; Event is the current fair",
             [["2 hours", "Thank-you and catalogue"], ["Day 2", "Stockist offer"], ["On click", "&lsquo;Become a stockist&rsquo; assigns sales"]],
             "Stockist enquiries per event", "Opportunity in the Stockist pipeline"]]
    sb = "".join('<button type="button" class="em-sg%s" data-e3="%d" aria-pressed="%s"><b>%s</b><small>%s</small></button>'
                 % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", s[0], s[1]) for i, s in enumerate(segs))
    out += sec(head("SEGMENTS TO WORKFLOWS", "How Does Unisas Map Your Customer Segments to the Right Campaign Workflows?",
                    "Not every segment needs the same treatment. Some get a monthly mailing, some a timed journey, some a plain email from their salesperson. "
                    "We map each segment to its audience in Odoo, its sequence, the number that proves it works and who takes over. Pick a segment.", "is-center")
               + '<div class="em-map" data-e3box><div class="em-sgs" role="group" aria-label="Customer segment">%s</div><div class="em-wf ox-solo" aria-live="polite" data-e3card></div></div>' % sb
               + data("em-segs", segs), "em-sec--map")

    # 4 ---- the Email Marketing app: mailings in Kanban, List, Calendar and Graph, each opening the mailing form
    mailings = [
        dict(id=1, sub="Diwali trade offer: 15% off gift boxes", prev="Order by 25 Oct for delivery before Dhanteras", list="Retailer offers", n=1736, st="done", when="07 Oct", day=7, resp="P", tpl="promo",
             s=[98.6, 52.4, 4.1, 18.7, 1.4], lead=46, quo=31, rev=1840000),
        dict(id=2, sub="October recipe newsletter", prev="Chettinad chicken, lemon rasam and more", list="Newsletter", n=8912, st="done", when="03 Oct", day=3, resp="K", tpl="news",
             s=[97.9, 38.2, 0.6, 9.4, 2.1], lead=0, quo=0, rev=196400),
        dict(id=3, sub="Weekend offer: Rasam Powder 2 + 1", prev="This weekend only, on our website", list="Recipe Club", n=4380, st="sending", when="Today", day=10, resp="K", tpl="promo", prog=64),
        dict(id=4, sub="Madurai Food Expo: your trade pass", prev="Stall B12, free tasting, 14 to 16 Nov", list="Distributors", n=212, st="queue", when="15 Oct, 10:00", day=15, resp="P", tpl="event"),
        dict(id=5, sub="Dhanteras sweets with our ready mixes", prev="Five recipes for the festive week", list="Newsletter", n=8912, st="queue", when="27 Oct, 19:00", day=27, resp="K", tpl="news"),
        dict(id=6, sub="Pongal pre-order for retailers", prev="", list="Retailer offers", n=1736, st="draft", when="", day=0, resp="P", tpl=None),
        dict(id=7, sub="Welcome to the Recipe Club", prev="Your free e-book of 30 recipes", list="Recipe Club", n=4380, st="draft", when="", day=0, resp="K", tpl="welcome"),
        dict(id=8, sub="We miss you: 10% back", prev="Your favourites, 10% off this week", list="Lapsed 90 days", n=1230, st="done", when="19 Sep", day=0, resp="P", tpl="promo",
             s=[96.4, 29.5, 1.2, 7.1, 3.6], lead=0, quo=0, rev=74300)]
    views = [("kanban", "Kanban", ox.V_KANBAN), ("list", "List", ox.V_LIST), ("calendar", "Calendar", V_CAL), ("graph", "Graph", ox.V_GRAPH)]
    switch = "".join('<button type="button" class="ox-vbtn%s" data-e4view="%s" aria-label="%s view" title="%s" aria-pressed="%s">%s</button>'
                     % (" is-on" if k == "kanban" else "", k, n, n, "true" if k == "kanban" else "false", svg) for k, n, svg in views)
    out += sec(head("CREATE &amp; SCHEDULE", "What Can Odoo Email Marketing Do for Campaign Creation and Scheduling?",
                    "This is the Odoo Email Marketing app with Amudha Spices&rsquo; mailings. Switch between Kanban, List, Calendar and Graph, open a mailing to see its results, "
                    "or press <b>New</b>: pick a template, send yourself a test, then schedule it or send it now.", "is-center")
               + '<div class="ox em-ox em-app" data-e4box><div class="ox-nav"><span class="ox-app">%s<b>Email Marketing</b></span><span class="ox-menu">Mailings</span><span class="ox-menu">Mailing Lists</span>'
                 '<span class="ox-menu">Reporting</span><span class="ox-menu">Configuration</span><span class="ox-nav-r"><span class="ox-company">Amudha Spices</span><span class="ox-av" style="--c:#B5541B">P</span></span></div>'
                 '<div class="ox-cp"><div class="ox-cp-l"><button type="button" class="ox-new" data-e4new>New</button><span class="ox-crumb" data-e4crumb>Mailings</span></div>'
                 '<label class="ox-search">%s<input type="search" placeholder="Search..." aria-label="Search mailings" data-e4q></label><div class="ox-views">%s</div></div>'
                 '<div class="ox-body em-app-b" data-e4body></div><div data-e4dlg></div><div class="em-toast" data-e4toast aria-live="polite"></div></div>'
                 '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview with sample data. Open a mailing, switch views, or create, test and schedule a new one.</p>'
                 % (app_icon, ox.SEARCH, switch) + data("em-mailings", mailings), "em-sec--mf", "compose")

    # 5 ---- configured around your process
    steps = [["Plan", "Marketing manager", "Agrees the quarter&rsquo;s campaigns and dates.",
              [["Settings &rsaquo; Mailing Campaigns", "Campaigns group mailings, SMS and social posts with one budget and report"],
               ["Campaigns &rsaquo; stages", "New &rarr; Schedule &rarr; Design &rarr; Sent, so the calendar shows what is ready"],
               ["Campaign tags", "Festive, Launch, Trade, Win-back"]]],
             ["Audience", "Marketing executive", "Picks who gets it.",
              [["Mailing Lists", "One list per audience, with opt-in source recorded"], ["Saved filters", "Favourites such as &lsquo;Lapsed 90 days&rsquo; and &lsquo;Retailers, Tamil Nadu&rsquo;"],
               ["Access rights", "Sales can add contacts to lists, only marketing can send"]]],
             ["Design", "Designer", "Builds the email.",
              [["Brand template", "Saved as a favourite mailing, with your colours, fonts and footer"], ["Building blocks", "Product grid, coupon, recipe card and event blocks"],
               ["Placeholders", "Customer name and salesperson filled in per recipient"]]],
             ["Approve", "Sales head", "Checks prices and offers.",
              [["Responsible", "Each mailing has an owner"], ["Activities", "&lsquo;Review mailing&rsquo; assigned to the approver, with a due date"],
               ["Chatter", "Comments and approvals kept on the mailing"]]],
             ["Test", "Marketing executive", "Checks it on phone and desktop.",
              [["Test recipients", "A saved list of team inboxes on Gmail, Outlook and mobile"], ["Preview text", "Set for every mailing"],
               ["Links", "Every link tracked and tagged with the campaign"]]],
             ["Send", "Marketing executive", "Schedules for the right hour.",
              [["Scheduled date", "Retailers 07:30, home cooks 19:00"], ["Outgoing mail server", "Dedicated server for bulk mail, separate from invoices"],
               ["Sending limits", "Batches sized to your email plan"]]],
             ["Report", "Marketing manager", "Reviews results each Monday.",
              [["24H Stat Mailing Reports", "Results emailed to the owner a day after sending"], ["Reporting &rsaquo; Mailings", "Pivot by campaign, list and month"],
               ["CRM &amp; Sales", "Pipeline and revenue grouped by UTM campaign"]]]]
    st = "".join('<li><button type="button" class="em-st%s" data-e5="%d" aria-pressed="%s"><span class="mono">%02d</span><b>%s</b><small>%s</small></button></li>'
                 % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", i + 1, s[0], s[1]) for i, s in enumerate(steps))
    out += sec(head("YOUR MARKETING PROCESS", "How Does Unisas Configure Email Campaigns Around Your Marketing Process?",
                    "Your team already has a way of planning, approving and reporting campaigns. We set up Odoo so each step has an owner, a place in the system and a record of what was done. "
                    "Click a step to see what we configure.", "is-center")
               + '<div class="em-proc" data-e5box><ol class="em-sts">%s</ol><div class="ox em-ox">%s<div class="em-cfg" data-e5card aria-live="polite"></div></div></div>'
                 % (st, ox_head("Email Marketing", "Configuration")) + data("em-steps", steps), "em-sec--proc")

    # 6 ---- CRM and customer activity
    flows = [["A retailer clicks &lsquo;Order for my store&rsquo;", [["em", "Email Marketing", "Opened and clicked", "Diwali trade offer &middot; Sri Murugan Stores &middot; 07:42"],
                                                                      ["web", "Website", "Lands on the trade page", "Tracked with UTM: Diwali 2026 / Email / Retailer offers"],
                                                                      ["crm", "CRM", "Lead created", "&lsquo;Diwali stock: 40 boxes&rsquo; &middot; Team Madurai &middot; Priya Raman"],
                                                                      ["sale", "Sales", "Quotation sent", "S00418 &middot; 40 gift boxes &middot; &#8377; 64,800.00"],
                                                                      ["ct", "Contact", "History on the contact", "Mailing opened, link clicked, lead and quote in the chatter"]],
              [1, 1, 64800]],
             ["A customer replies to the newsletter", [["em", "Email Marketing", "Reply received", "&lsquo;Do you ship to Singapore?&rsquo; &middot; October recipe newsletter"],
                                                       ["crm", "CRM", "Lead from the reply", "Reply-to alias sales@ creates &lsquo;Export enquiry, Singapore&rsquo;"],
                                                       ["ct", "Contact", "Conversation saved", "The email thread sits on Deepa Krishnan&rsquo;s contact"],
                                                       ["sale", "Sales", "Quotation in SGD", "S00420 &middot; export pricelist &middot; SGD 420.00"]],
              [1, 1, 26300]],
             ["A lapsed buyer comes back", [["em", "Email Marketing", "Win-back email clicked", "We miss you: 10% back &middot; Rahul Menon"],
                                            ["web", "Website", "Order with code COMEBACK10", "3 items &middot; paid by UPI"],
                                            ["sale", "Sales", "Sales order confirmed", "S00422 &middot; &#8377; 1,240.00 &middot; coupon applied"],
                                            ["ct", "Contact", "Back in the active segment", "Last Order Date updated, leaves the lapsed filter"],
                                            ["em", "Email Marketing", "Revenue on the mailing", "Revenues smart button: + &#8377; 1,240.00"]],
              [0, 0, 1240]]]
    apps6 = [["em", "Email Marketing", "#B5541B"], ["web", "Website", "#2F6BD8"], ["crm", "CRM", "#8E4F83"], ["sale", "Sales", "#EE8A3C"], ["ct", "Contacts", "#1F8A78"]]
    fb = "".join('<button type="button" class="em-flow%s" data-e6="%d" aria-pressed="%s">%s</button>' % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", f[0]) for i, f in enumerate(flows))
    lanes = "".join('<div class="em-lane" data-e6lane="%s" style="--c:%s"><p class="em-lane-h"><i></i>%s</p><div class="em-lane-b"></div></div>' % (k, c, n) for k, n, c in apps6)
    out += sec(head("CRM &amp; CUSTOMER ACTIVITY", "How Can Odoo Connect Email Campaigns With CRM and Customer Activity?",
                    "Mailings, contacts, leads and orders share one database, so a click or a reply turns into work for sales, and every order can be traced back to the email that started it. "
                    "Pick what a recipient does and follow it across the apps.", "is-center")
               + '<div class="em-x" data-e6box><div class="em-flows ox-solo" role="group" aria-label="Recipient action">%s<button type="button" class="ox-pbtn" data-e6run>Run again</button></div>'
                 '<div class="em-lanes">%s</div><div class="em-sbtns ox-solo" aria-live="polite"><span class="em-sbtns-h">On the mailing</span><span class="em-sbtn"><b data-e6k="0">0</b>Leads</span>'
                 '<span class="em-sbtn"><b data-e6k="1">0</b>Quotations</span><span class="em-sbtn"><b data-e6k="2">&#8377; 0</b>Revenues</span></div></div>'
                 % (fb, lanes) + data("em-flows", flows), "em-sec--x")

    # 7 ---- mailing or automation
    reqs = [["Announce the new Chettinad Sambar Mix to everyone on the newsletter", "mail", "A one-off message to a list at a chosen time is a mailing."],
            ["Welcome each new subscriber, then send a first-order code the next day", "auto", "It runs for each person from the day they join, so it is a journey."],
            ["Send the Diwali price list to all retailers on Tuesday morning", "mail", "Same message, same moment, one audience: a scheduled mailing."],
            ["Resend the welcome email with a new subject to people who didn&rsquo;t open it", "auto", "&lsquo;Mail: Not opened&rsquo; is a Marketing Automation trigger."],
            ["Ask buyers for a review 10 days after delivery", "auto", "Timed from each customer&rsquo;s own delivery date, so it needs a workflow."],
            ["The monthly recipe newsletter", "mail", "A regular mailing, often duplicated from last month&rsquo;s."],
            ["Tell the salesperson when a retailer clicks the bulk-order link", "auto", "&lsquo;Mail: Clicked&rsquo; can trigger a server action that creates a lead or an activity."]]
    lab = {"mail": "Mailing", "auto": "Marketing Automation"}
    rq = "".join('<li class="em-q" data-e7="%d"><p>%s</p><span class="em-q-b">%s</span><small class="em-q-why"></small></li>'
                 % (i, r[0], "".join('<button type="button" data-e7a="%s">%s</button>' % (k, v) for k, v in lab.items())) for i, r in enumerate(reqs))
    out += sec(head("MAILINGS OR AUTOMATION", "When Should Email Marketing Be Combined With Odoo Marketing Automation?",
                    "Use a mailing when the same message goes to a list at one moment. Add Marketing Automation when timing depends on each person: when they joined, opened, clicked or ordered. "
                    "Make your call for each campaign.", "is-center")
               + '<div class="em-quiz" data-e7box><ol>%s</ol><div class="em-quiz-s ox-solo"><p class="mono">YOUR SCORE</p><b data-e7score>0 / %d</b><p data-e7msg>Pick an answer for each campaign.</p>'
                 '<ul><li><i class="is-mail"></i><b>Mailing</b> one message, one send time, one audience</li><li><i class="is-auto"></i><b>Marketing Automation</b> per-person timing and triggers</li></ul></div></div>'
                 % (rq, len(reqs)) + data("em-reqs", reqs), "em-sec--quiz")

    # 8 ---- marketing automation workflow
    acts = [["a", "", "Beginning of workflow", "Email", "Welcome + recipe e-book", 0, "Immediately", 982, 18],
            ["b", "a", "Mail: Opened", "Email", "Your 10% first-order code", 1, "1 Days after", 498, 0],
            ["c", "b", "Mail: Clicked", "Server Action", "Add to list &lsquo;First-order intent&rsquo;", 1, "Immediately after", 197, 0],
            ["d", "b", "Mail: Not clicked", "Email", "Your code expires in 48 hours", 4, "3 Days after", 301, 0],
            ["e", "a", "Mail: Not opened", "Email", "Resend with a new subject line", 3, "2 Days after", 484, 0]]
    out += sec(head("AUTOMATED JOURNEYS", "How Does Unisas Build and Configure Automated Customer Journeys?",
                    "This is an Odoo Marketing Automation campaign for new subscribers. Each activity waits for a trigger on the one above it: opened, not opened, clicked. "
                    "Press <b>Start</b>, then move through the first week and watch 1,000 subscribers flow through it.", "is-center")
               + '<div class="ox em-ox em-ma" data-e8box><div class="ox-nav"><span class="ox-app">%s<b>Marketing Automation</b></span><span class="ox-menu">Campaigns</span><span class="ox-menu">Reporting</span><span class="ox-menu">Configuration</span></div>'
                 '<div class="em-ma-bar"><span class="ox-crumb ox-crumb--stack"><a>Campaigns</a><span>Welcome &amp; first order</span></span><span class="em-ma-btns" data-e8btns></span>'
                 '<span class="ox-sbar"><span class="ox-sb" data-e8s="draft">New</span><span class="ox-sb" data-e8s="run">Running</span><span class="ox-sb" data-e8s="stop">Stopped</span></span></div>'
                 '<div class="em-ma-sheet"><dl class="em-ma-f"><div><dt>Target</dt><dd>Contact</dd></div><div><dt>Unicity based on</dt><dd>Email</dd></div>'
                 '<div class="is-wide"><dt>Filter</dt><dd><span class="em-dom">Mailing List is <b>Newsletter</b></span><span class="em-dom">Created on is in the <b>last 24 hours</b></span><span class="em-dom">Blacklist is <b>not set</b></span></dd></div></dl>'
                 '<div class="em-ma-sum" data-e8sum></div><div class="em-ma-tree" data-e8tree></div></div></div>' % app_icon
               + data("em-acts", acts), "em-sec--ma")

    # 9 ---- measure
    mails = [["Diwali trade offer: 15% off gift boxes", "Retailer offers", "07 Oct", 1736, 98.6, 52.4, 4.1, 18.7, 1.4, 46, 31, 1840000],
             ["October recipe newsletter", "Newsletter", "03 Oct", 8912, 97.9, 38.2, 0.6, 9.4, 2.1, 0, 0, 196400],
             ["New: Chettinad Sambar Mix", "Recipe Club", "24 Sep", 6380, 98.1, 41.7, 0.9, 12.8, 1.9, 3, 0, 284900],
             ["We miss you: 10% back", "Lapsed 90 days", "19 Sep", 1230, 96.4, 29.5, 1.2, 7.1, 3.6, 0, 0, 74300]]
    rows = "".join('<tr data-e9="%d"%s><td><b>%s</b></td><td>%s</td><td>%s</td><td class="ox-num">%s</td><td class="ox-num">%.1f%%</td><td class="ox-num">%.1f%%</td></tr>'
                   % (i, ' class="is-on"' if i == 0 else "", m[0], m[1], m[2], "{:,}".format(m[3]), m[5], m[7]) for i, m in enumerate(mails))
    out += sec(head("OPENS, CLICKS, LEADS &amp; REVENUE", "How Can Odoo Help Measure Opens, Clicks, Leads and Campaign Revenue?",
                    "Every sent mailing carries its own statistics, and because CRM and Sales sit in the same database it also shows the leads, quotations and revenue it produced. "
                    "Click a mailing to open its results.", "is-center")
               + '<div class="em-meas" data-e9box><div class="ox em-ox">%s<div class="ox-scroll"><table class="ox-table em-ml"><thead><tr><th>Subject</th><th>Recipients</th><th>Sent on</th>'
                 '<th class="ox-num">Sent</th><th class="ox-num">Opened</th><th class="ox-num">Clicked</th></tr></thead><tbody>%s</tbody></table></div></div>'
                 '<div class="em-st-card ox-solo" data-e9card aria-live="polite"></div></div>' % (ox_head("Email Marketing", "Mailings"), rows)
               + data("em-mails", mails), "em-sec--meas")

    # 10 ---- A/B testing and tracking
    links = [["amudhaspices.in/shop/festive-gift-box", "Diwali 2026", "Email", "Diwali trade offer", 214],
             ["amudhaspices.in/trade/bulk-order", "Diwali 2026", "Email", "Diwali trade offer", 141],
             ["amudhaspices.in/recipes/chettinad-sambar", "Sambar Mix launch", "Email", "New: Chettinad Sambar Mix", 388],
             ["wa.me/919800000000", "Diwali 2026", "Email", "Diwali trade offer", 37]]
    lt = "".join('<tr><td>%s</td><td>%s</td><td>%s</td><td class="ox-num">%d</td></tr>' % (l[0], l[1], l[3], l[4]) for l in links)
    ab = {"n": 1736, "a": "Diwali gift boxes: 15% off for your store", "b": "Your Diwali shelf, sorted: gift boxes at trade price",
          "res": {"open": [44.1, 51.8, "%"], "click": [12.3, 11.6, "%"], "lead": [9, 13, ""], "rev": [310000, 422000, "inr"]}}
    out += sec(head("TRACKING, TESTING &amp; REPORTING", "How Does Unisas Configure Tracking, Testing and Campaign Reporting?",
                    "We switch on A/B testing for subject lines and offers, tag every link with the campaign, and set the reports your team reads each week. "
                    "Set up the test below, run it and see which version Odoo sends to everyone else.", "is-center")
               + '<div class="em-ab" data-e10box><div class="ox em-ox">%s<div class="em-ab-b"><label class="em-abl"><input type="checkbox" data-e10on checked><span class="em-cbx" aria-hidden="true">%s</span><b>Allow A/B Testing</b></label>'
                 '<div class="em-ab-in" data-e10in><label class="em-abr"><span>Test on <b data-e10pv>20</b>%% of the recipients</span><input type="range" min="10" max="50" step="5" value="20" data-e10p></label>'
                 '<label class="em-abr"><span>Winner Selection</span><select data-e10w><option value="open">Highest Open Rate</option><option value="click">Highest Click Rate</option>'
                 '<option value="lead">Leads</option><option value="rev">Revenues</option><option value="manual">Manual</option></select></label>'
                 '<div class="em-vers"><div><small>Version A &middot; Subject</small><b>%s</b></div><div><small>Version B &middot; Subject</small><b>%s</b></div></div>'
                 '<p class="em-ab-note" data-e10note></p><button type="button" class="ox-pbtn" data-e10run>Send test versions</button><div class="em-ab-res" data-e10res aria-live="polite"></div></div></div></div>'
                 '<div class="em-ab-r"><div class="ox em-ox">%s<div class="ox-scroll"><table class="ox-table em-lt"><thead><tr><th>Target URL</th><th>Campaign</th><th>Source</th><th class="ox-num">Clicks</th></tr></thead><tbody>%s</tbody></table></div></div>'
                 '<ul class="em-rep ox-solo"><li><b>24H stat report</b><span>Emailed to the mailing&rsquo;s owner one day after sending</span></li><li><b>Mailing analysis</b><span>Pivot by campaign, list and month: sent, opened, clicked, bounced</span></li>'
                 '<li><b>Pipeline by campaign</b><span>CRM grouped by UTM campaign and source</span></li><li><b>Revenue by campaign</b><span>Sales analysis filtered by campaign</span></li></ul></div></div>'
                 % (ox_head("Diwali trade offer", "A/B Tests"), TICK, ab["a"], ab["b"], ox_head("Email Marketing", "Link Tracker"), lt)
               + data("em-ab", ab), "em-sec--ab", "ab-test")

    # 11 ---- deliverability and unsubscriptions
    recs = [["SPF", "TXT", "@", "v=spf1 include:_spf.odoo.com ~all", 12, "Tells inboxes Odoo may send for amudhaspices.in"],
            ["DKIM", "CNAME", "odoo._domainkey", "odoo._domainkey.odoo.com", 14, "Signs every email so it cannot be forged"],
            ["DMARC", "TXT", "_dmarc", "v=DMARC1; p=quarantine; rua=mailto:dmarc@amudhaspices.in", 8, "Tells inboxes what to do with failures, and reports them"],
            ["From address", "", "", "offers@amudhaspices.in, not a Gmail address", 6, "Sender on your own authenticated domain"],
            ["Bounce handling", "", "", "Hard bounces blocklisted automatically", 7, "Keeps dead addresses from hurting your reputation"],
            ["List hygiene", "", "", "Contacts with no opens in 12 months moved to a quiet list", 7, "Fewer sends to people who never read"]]
    rc = "".join('<li><label class="em-dns"><input type="checkbox" data-e11="%d"><span class="em-sw" aria-hidden="true"></span><span class="em-dns-t"><b>%s%s</b><code>%s</code><small>%s</small></span></label></li>'
                 % (i, r[0], ' <em class="mono">%s %s</em>' % (r[1], r[2]) if r[1] else "", r[3], r[5]) for i, r in enumerate(recs))
    subs = [["Newsletter", True], ["Recipe Club", True], ["Retailer offers", False]]
    reasons = ["I never subscribed to this list", "I receive too many emails from this list", "The content of these emails is not relevant to me", "Other"]
    out += sec(head("DELIVERABILITY &amp; UNSUBSCRIPTIONS", "How Should Your Odoo Email Marketing Setup Handle Deliverability and Unsubscriptions?",
                    "A campaign only works if it reaches the inbox, and people who want fewer emails can say so in one click. "
                    "Configure the sending domain on the left; unsubscribe as a recipient on the right and see what Odoo records.", "is-center")
               + '<div class="em-dlv"><div class="em-dlv-l" data-e11box><ul class="em-dnss">%s</ul><div class="em-gauge ox-solo"><span class="em-ring" data-e11ring style="--p:43"><b data-e11v>43%%</b></span>'
                 '<span><b>Expected inbox placement</b><small data-e11msg></small></span></div></div>'
                 '<div class="em-uns" data-e11ubox><div class="em-uns-m ox-solo" data-e11u></div><div class="em-uns-o ox-solo" data-e11rec aria-live="polite"></div></div></div>'
                 % rc + data("em-recs", recs) + data("em-subs", subs) + data("em-reasons", reasons), "em-sec--dlv")

    # 12 ---- setup to launch
    phases = [["Discover", "Week 1", ["Audiences and segments mapped", "Campaign calendar for the quarter", "Current tool and lists reviewed", "KPIs agreed per segment"], "Access to your current email tool, last year&rsquo;s campaigns and the people who run them."],
              ["Contacts &amp; lists", "Week 1&ndash;2", ["Contacts imported and de-duplicated", "Consent and source recorded", "Mailing lists and saved filters", "Blocklist imported from the old tool"], "Contact exports and the unsubscribe list from your current tool."],
              ["Domain &amp; sending", "Week 2", ["SPF, DKIM and DMARC records", "From and reply-to addresses", "Outgoing mail server and limits", "Test sends to Gmail, Outlook and Yahoo"], "Access to your DNS, or 20 minutes with whoever manages it."],
              ["Templates", "Week 2&ndash;3", ["Brand template in your colours", "Newsletter, offer, launch and plain-text layouts", "Footer with address and unsubscribe", "Mobile checks"], "Logo, brand colours and two past emails you liked."],
              ["Campaigns &amp; journeys", "Week 3&ndash;4", ["First mailings built and scheduled", "Welcome and win-back journeys", "A/B tests and link tracking", "CRM lead rules on clicks and replies"], "Approval of copy and offers."],
              ["Launch &amp; report", "Week 4 onward", ["First campaign sent with us on hand", "Team trained by role", "24H reports and monthly dashboard", "Monthly review and improvements"], "A launch date and an owner for each campaign."]]
    pbt = "".join('<li><button type="button" class="em-ph%s" data-e12="%d" aria-pressed="%s"><span class="mono">%02d</span><b>%s</b><small>%s</small></button></li>'
                  % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", i + 1, n, w) for i, (n, w, d, y) in enumerate(phases))
    out += sec(head("SETUP TO LAUNCH", "What Does Unisas Handle From Email Marketing Setup to Campaign Launch?",
                    "Six steps from your current list to your first measured campaign. Each ends with something you can see and approve. Pick a step to see what we hand over and what we need from you.", "is-center")
               + '<div class="em-del" data-e12box><ol class="em-phs">%s</ol><div class="em-del-c ox-solo" aria-live="polite"><div><p class="em-gi-h">Unisas delivers</p><ul class="em-files" data-e12d></ul></div>'
                 '<div class="em-del-y"><p class="em-gi-h">We need from you</p><p data-e12y></p></div></div></div>' % pbt + data("em-phases", phases), "em-sec--del")

    # 13 ---- plan the implementation
    out += sec('<div class="em-scope"><div>%s<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Plan my email marketing %s</a></div></div>'
               '<div class="em-sc ox-solo" data-e13box><p class="em-sc-h"><b>Email marketing planner</b><small>A first recommendation. We confirm it after a short call.</small></p>'
               '<div class="em-sc-in"><label><span>Contacts <b data-e13o="contacts">10,000</b></span><input type="range" min="1000" max="100000" step="1000" value="10000" data-e13="contacts"></label>'
               '<label><span>Mailings a month <b data-e13o="mails">4</b></span><input type="range" min="1" max="20" value="4" data-e13="mails"></label>'
               '<label><span>Moving from</span><select data-e13="from"><option value="0">Nothing yet / Excel</option><option value="1" selected>Mailchimp</option><option value="2">Zoho Campaigns / Brevo</option><option value="3">Another CRM&rsquo;s email tool</option></select></label>'
               '<label><span>Odoo today</span><select data-e13="odoo"><option value="0">Not on Odoo yet</option><option value="1" selected>Using CRM / Sales</option><option value="2">Using eCommerce too</option></select></label>'
               '<div class="em-sc-chk is-wide"><label><input type="checkbox" data-e13x="auto" checked> Automated journeys (welcome, win-back)</label><label><input type="checkbox" data-e13x="ab"> A/B testing and revenue reporting</label>'
               '<label><input type="checkbox" data-e13x="sms"> SMS or WhatsApp alongside email</label></div></div>'
               '<div class="em-sc-out" data-e13out aria-live="polite"></div></div></div>'
               % (head("PLAN YOUR IMPLEMENTATION", "How Can We Plan an Odoo Email Marketing Implementation for Your Business?",
                       "The plan depends on how many contacts move across, how often you send, and whether you need automated journeys and revenue reporting. "
                       "Answer a few questions for a first recommendation, then talk it through with us."), g["ARROW"]), "em-sec--scope")

    return out + JS


CTA = ("Let's Plan Email Campaigns That Bring In Orders",
       "Tell us who you email today, how often, and what you want them to do. We'll show you your campaigns in Odoo Email Marketing and recommend the right setup, from lists and domain to automated journeys.")

FAQ = [("Do we still need Mailchimp or another email tool with Odoo?",
        "Usually not. Odoo Email Marketing covers mailing lists, templates, scheduling, A/B tests and tracking, and it reads your CRM and sales data directly. Most clients move their lists across and cancel the separate tool."),
       ("Can we import our existing contacts and unsubscribe list?",
        "Yes. We import contacts with their consent source, de-duplicate them, and import your unsubscribe and bounce lists into the Odoo blocklist so nobody who opted out is emailed again."),
       ("What is the difference between Email Marketing and Marketing Automation?",
        "Email Marketing sends a mailing to a list at a chosen time. Marketing Automation runs journeys for each contact, with steps triggered by when they joined, opened, clicked or ordered. Many businesses use both."),
       ("Will our emails land in the inbox?",
        "We set up SPF, DKIM and DMARC on your domain, send from your own address, handle bounces automatically and keep lists clean. Those four things decide inbox placement more than anything else."),
       ("Can we see revenue from each campaign?",
        "Yes. With CRM and Sales in Odoo, each mailing shows the leads, quotations and revenue that came from it, and links are tagged with the campaign for website orders."),
       ("Is there a limit on how many emails we can send?",
        "Odoo Online includes a daily allowance and you can buy more mail credits; on Odoo.sh or your own server you can use a dedicated mail service. We size it to your list during scoping.")]


JS = r'''<script>
(function(){
  function J(id){var e=document.getElementById(id);return e?JSON.parse(e.textContent):null;}
  function press(group,el){group.forEach(function(b){var on=b===el;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});}
  function num(n,d){return Number(n).toLocaleString('en-IN',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}
  function inr(n){return '&#8377; '+num(n);}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  var TK='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  /* --- 1 right people, right time --- */
  (function(){var bx=document.querySelector('[data-e1box]');if(!bx)return;var T=J('em-types'),O=J('em-order'),C=J('em-camps'),PER=205,
    cb=[].slice.call(bx.querySelectorAll('[data-e1]')),mb=[].slice.call(bx.querySelectorAll('[data-e1mode]')),cur=0,mode='all';
    function draw(){var c=C[cur],seg=mode==='seg',rel=0,irr=0;
      bx.querySelector('[data-e1dots]').innerHTML=O.map(function(t){var r=c[2].indexOf(t)>-1,got=seg?r:true;if(got){if(r)rel++;else irr++;}
        return '<i class="'+(got?(r?'is-rel':'is-irr'):'is-off')+'" style="--c:'+T[t][1]+'" title="'+T[t][0]+'"></i>';}).join('');
      var rec=(rel+irr)*PER,op=rel*PER*(seg?0.46:0.40)+irr*PER*0.08,un=irr*PER*0.012+rel*PER*0.001,ord=rel*PER*(seg?0.034:0.024);
      bx.querySelector('[data-e1when]').innerHTML=seg?'<b>'+c[3]+'</b> &middot; '+c[4]:'<b>Mon 09:00</b> &middot; the whole list at once';
      bx.querySelector('[data-e1kpis]').innerHTML=[['Recipients',num(rec)],['Open rate',(op/rec*100).toFixed(1)+'%'],['Unsubscribes',num(Math.round(un))],['Orders',num(Math.round(ord))]]
        .map(function(k){return '<li><small>'+k[0]+'</small><b>'+k[1]+'</b></li>';}).join('');
      bx.querySelector('[data-e1msg]').innerHTML=seg?'<b>Only the people it was written for</b> get it, at the hour they read email. Fewer sends, more orders, almost no unsubscribes.'
        :'<b>'+num(irr*PER)+' people</b> got an email that wasn&rsquo;t meant for them. They are the ones who unsubscribe or mark it as spam.';}
    cb.forEach(function(b){b.addEventListener('click',function(){press(cb,b);cur=+b.getAttribute('data-e1');draw();});});
    mb.forEach(function(b){b.addEventListener('click',function(){press(mb,b);mode=b.getAttribute('data-e1mode');draw();});});draw();})();

  /* --- 2 recipients --- */
  (function(){var bx=document.querySelector('[data-e2box]');if(!bx)return;var M=J('em-models'),L=J('em-lists'),body=bx.querySelector('[data-e2body]'),mb=[].slice.call(bx.querySelectorAll('[data-e2m]')),
    st={m:'list',on:{contact:[true,true,false,false],lead:[true,false,false]},lists:L.map(function(l){return l[2];})};
    function test(r,ru){var v=r[ru[4]];if(ru[5]==='eq')return v===ru[6];if(ru[5]==='gt')return v>ru[6];if(ru[5]==='in')return ru[6].indexOf(v)>-1;return true;}
    function draw(){var n,s;
      if(st.m==='list'){var k=0,cnt=0;L.forEach(function(l,i){if(st.lists[i]){k++;cnt+=l[1];}});n=Math.round(cnt*(k>1?0.94:1)*0.98);
        body.innerHTML='<div class="em-fld"><span class="em-lbl">Select Mailing List</span><div class="em-lists">'+L.map(function(l,i){return '<label class="em-li'+(st.lists[i]?' is-on':'')+'"><input type="checkbox" data-e2l="'+i+'"'+(st.lists[i]?' checked':'')+'><b>'+l[0]+'</b><small>'+num(l[1])+' contacts</small></label>';}).join('')+'</div></div>';
        s=k?'Subscribed members of '+k+' list'+(k>1?'s':'')+', not opted out or blocklisted.':'Select at least one mailing list.';}
      else{var m=M[st.m],on=st.on[st.m],f=1;m.rules.forEach(function(r,i){if(on[i])f*=r[3];});n=Math.round(m.base*f*0.97);
        var rows=m.rows.filter(function(r){return m.rules.every(function(ru,i){return !on[i]||test(r,ru);});});
        body.innerHTML='<div class="em-dom-ed"><p class="em-match">Match <b>all</b> of the following rules:</p>'+m.rules.map(function(r,i){return '<label class="em-rule'+(on[i]?' is-on':'')+'"><input type="checkbox" data-e2r="'+i+'"'+(on[i]?' checked':'')+'><span class="em-sw" aria-hidden="true"></span><span class="em-r-f">'+r[0]+'</span><span class="em-r-o">'+r[1]+'</span><span class="em-r-v">'+r[2]+'</span></label>';}).join('')+
          '<p class="em-r-hint">Odoo filters on any field: tags, country, orders, invoices, events attended, website visits.</p></div>'+
          '<div class="ox-scroll"><table class="ox-table em-pv"><thead><tr>'+m.cols.map(function(c){return '<th>'+c+'</th>';}).join('')+'</tr></thead><tbody>'+
          (rows.length?rows.slice(0,5).map(function(r){return '<tr>'+r.map(function(v,j){return '<td>'+(st.m==='contact'&&j===4?(v<0?'<span class="ox-muted">Never</span>':v+' days ago'):v)+'</td>';}).join('')+'</tr>';}).join(''):'<tr><td colspan="5" class="ox-muted">No sample records match. The count on the right is for the full database.</td></tr>')+'</tbody></table></div>';
        s=m.label+' records matching '+on.filter(Boolean).length+' rule'+(on.filter(Boolean).length===1?'':'s')+', blocklisted addresses removed.';}
      bx.querySelector('[data-e2n]').textContent=num(n);bx.querySelector('[data-e2s]').textContent=s;}
    bx.addEventListener('change',function(e){var l=e.target.closest('[data-e2l]');if(l){st.lists[+l.getAttribute('data-e2l')]=l.checked;draw();return;}
      var r=e.target.closest('[data-e2r]');if(r){st.on[st.m][+r.getAttribute('data-e2r')]=r.checked;draw();}});
    mb.forEach(function(b){b.addEventListener('click',function(){press(mb,b);st.m=b.getAttribute('data-e2m');draw();});});draw();})();

  /* --- 3 segments --- */
  (function(){var bx=document.querySelector('[data-e3box]');if(!bx)return;var S=J('em-segs'),bt=[].slice.call(bx.querySelectorAll('[data-e3]')),card=bx.querySelector('[data-e3card]');
    function draw(i){var s=S[i];card.innerHTML='<div class="em-wf-h"><span><b>'+s[0]+'</b><small>'+s[2]+'</small></span><span class="em-wf-type'+(/Automation|automation/.test(s[3])?' is-auto':'')+'">'+s[3]+'</span></div>'+
      '<p class="em-wf-dom"><small>Audience in Odoo</small>'+s[4]+'</p><ol class="em-wf-steps">'+s[5].map(function(x,j){return '<li style="--i:'+j+'"><small class="mono">'+x[0]+'</small><b>'+x[1]+'</b></li>';}).join('')+'</ol>'+
      '<div class="em-wf-f"><p><small>Measured by</small>'+s[6]+'</p><p><small>Hand-off</small>'+s[7]+'</p></div>';}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);draw(+b.getAttribute('data-e3'));});});draw(0);})();

  /* --- 4 Email Marketing app --- */
  (function(){var bx=document.querySelector('[data-e4box]');if(!bx)return;
    var body=bx.querySelector('[data-e4body]'),crumb=bx.querySelector('[data-e4crumb]'),q=bx.querySelector('[data-e4q]'),dlgBox=bx.querySelector('[data-e4dlg]'),toast=bx.querySelector('[data-e4toast]'),timer;
    var M=J('em-mailings'),PPL={P:['Priya Raman','#B5541B'],K:['Kavya Nair','#3E7CB1']},uid=100;
    var COLS=[['draft','Draft'],['queue','In Queue'],['sending','Sending'],['done','Sent']],LBL={draft:'Draft',queue:'In Queue',sending:'Sending',done:'Sent'};
    var TPL=[['plain','Plain Text'],['welcome','Welcome Message'],['news','Newsletter'],['promo','Promotion Program'],['event','Event Promo']];
    var st={view:'kanban',open:null,tab:'body',dlg:null,measure:1};
    function say(h){toast.innerHTML=h;toast.classList.remove('is-on');void toast.offsetWidth;toast.classList.add('is-on');}
    function av(k,c){return '<span class="ox-av '+(c||'')+'" style="--c:'+PPL[k][1]+'" title="'+PPL[k][0]+'">'+PPL[k][0][0]+'</span>';}
    function find(id){return M.filter(function(m){return m.id===+id;})[0];}
    function rows(){var t=q.value.trim().toLowerCase();return M.filter(function(m){return !t||(m.sub+' '+m.list).toLowerCase().indexOf(t)>-1;});}
    function name(m){return m.sub?esc(m.sub):'<span class="ox-muted">(no subject)</span>';}
    function when(m){return m.st==='done'?'Sent on '+m.when:(m.st==='queue'?'Scheduled for '+m.when:(m.st==='sending'?'Sending now':'Not scheduled'));}
    /* views */
    function card(m){return '<article class="ox-card em-mc" tabindex="0" data-id="'+m.id+'"><b class="ox-c-name">'+name(m)+'</b><span class="em-mc-l">'+m.list+' &middot; '+num(m.n)+' recipients</span>'+
      (m.st==='done'?'<span class="em-mc-s"><span><b>'+num(Math.round(m.n*m.s[0]/100))+'</b>Sent</span><span><b>'+Math.round(m.s[1])+'%</b>Opened</span><span><b>'+Math.round(m.s[3])+'%</b>Clicked</span></span>':'')+
      (m.st==='sending'?'<span class="em-mc-p"><i style="--p:'+m.prog+'"></i><small>'+m.prog+'% sent</small></span>':'')+
      '<span class="ox-c-foot"><span class="em-mc-d">'+when(m)+'</span>'+av(m.resp)+'</span></article>';}
    function kanban(l){return '<div class="ox-kanban em-kb">'+COLS.map(function(c){var x=l.filter(function(m){return m.st===c[0];});
      return '<section class="ox-col"><header><b>'+c[1]+'</b><span class="em-kb-n">'+x.length+'</span></header><div class="ox-cards">'+x.map(card).join('')+'</div></section>';}).join('')+'</div>';}
    function list(l){return '<div class="ox-scroll"><table class="ox-table em-lv"><thead><tr><th class="ox-chk"><span class="ox-cb"></span></th><th>Subject</th><th>Recipients</th><th>Responsible</th><th>Date</th><th class="ox-num">Sent</th><th class="ox-num">Opened</th><th class="ox-num">Clicked</th><th>Status</th></tr></thead><tbody>'+
      l.map(function(m){var d=m.st==='done';return '<tr data-id="'+m.id+'" tabindex="0"><td class="ox-chk"><span class="ox-cb"></span></td><td><b>'+name(m)+'</b></td><td>'+m.list+'</td><td><span class="ox-sp">'+av(m.resp,'is-sm')+PPL[m.resp][0]+'</span></td><td>'+(m.when||'<span class="ox-muted">&mdash;</span>')+'</td>'+
        '<td class="ox-num">'+(d?num(Math.round(m.n*m.s[0]/100)):'')+'</td><td class="ox-num">'+(d?m.s[1].toFixed(1)+'%':'')+'</td><td class="ox-num">'+(d?m.s[3].toFixed(1)+'%':'')+'</td><td><span class="em-stp is-'+m.st+'">'+LBL[m.st]+'</span></td></tr>';}).join('')+'</tbody></table></div>';}
    function calendar(l){var h='<div class="em-cal-h"><b>October 2026</b><span class="ox-measure"><span class="is-on">Month</span></span></div><div class="ox-scroll"><div class="em-cal"><div class="em-cal-r is-h">'+['Mon','Tue','Wed','Thu','Fri','Sat','Sun'].map(function(d){return '<span>'+d+'</span>';}).join('')+'</div>';
      for(var w=0;w<5;w++){h+='<div class="em-cal-r">';for(var k=0;k<7;k++){var d=w*7+k-2;/* 1 Oct 2026 is a Thursday */
        var ev=d>=1&&d<=31?l.filter(function(m){return m.day===d;}):[];
        h+='<div class="em-cal-c'+(d<1||d>31?' is-out':'')+(d===10?' is-today':'')+'"><small>'+(d<1?30+d:(d>31?d-31:d))+'</small>'+ev.map(function(m){return '<button type="button" class="em-cal-e is-'+m.st+'" data-id="'+m.id+'">'+(m.when.indexOf(',')>-1?'<b>'+m.when.split(', ')[1]+'</b> ':'')+name(m)+'</button>';}).join('')+'</div>';}h+='</div>';}
      return h+'</div></div><p class="em-cal-n">Drafts without a date stay off the calendar; sent and scheduled mailings appear on their day.</p>';}
    function graph(l){var MS=[[1,'Opened'],[3,'Clicked'],[2,'Replied']],k=st.measure,d=l.filter(function(m){return m.st==='done';});
      var v=d.map(function(m){return m.s[k];}),mx=Math.max.apply(null,v.concat([1])),top=Math.ceil(mx/10)*10||10;
      return '<div class="ox-gtools"><span class="ox-measure">'+MS.map(function(x){return '<button type="button" data-e4m="'+x[0]+'" class="'+(k===x[0]?'is-on':'')+'">'+x[1]+' (%)</button>';}).join('')+'</span></div>'+
        '<div class="ox-chart"><div class="ox-yaxis">'+[4,3,2,1,0].map(function(i){return '<span>'+(top*i/4)+'%</span>';}).join('')+'</div><div class="ox-plot">'+
        d.map(function(m){return '<div class="ox-gcol"><span class="ox-gwrap"><span class="ox-gbar" style="--h:'+(m.s[k]/top*100).toFixed(1)+'" title="'+esc(m.sub)+'"><em>'+m.s[k]+'%</em></span></span><small>'+esc(m.sub.split(':')[0])+'</small></div>';}).join('')+
        '</div></div><p class="ox-legend"><i></i>'+MS.filter(function(x){return x[0]===k;})[0][1]+' rate by mailing</p>';}
    /* the mailing form */
    function mail(m){var s=name(m),t=m.tpl;
      if(t==='plain')return '<div class="em-e is-plain"><p>Dear Sri Murugan Stores,</p><p>'+s+'.</p><p>Our festive gift boxes are back, at trade price with 15% off on orders of 20 boxes or more. Reply to this email or call me to book your stock.</p><p>Regards,<br>'+PPL[m.resp][0]+'<br>Amudha Spices</p></div>';
      var hd='<div class="em-e-hd"><b>Amudha<span>Spices</span></b><small>View in browser</small></div>',ft='<p class="em-e-ft">Amudha Spices, Madurai 625001 &middot; <u>Unsubscribe</u> &middot; <u>Manage preferences</u></p>';
      if(t==='welcome')return '<div class="em-e">'+hd+'<div class="em-e-ban is-g"><small>WELCOME</small><h4>'+s+'</h4><p>Thank you for joining. Here&rsquo;s our free e-book of 30 South Indian recipes.</p><a>Download the e-book</a></div>'+ft+'</div>';
      if(t==='news')return '<div class="em-e">'+hd+'<div class="em-e-ban"><small>FROM OUR KITCHEN</small><h4>'+s+'</h4></div><div class="em-e-2"><span><i style="--h:18"></i><b>Chettinad chicken</b><small>Read the recipe</small></span><span><i style="--h:42"></i><b>Quick lemon rasam</b><small>Read the recipe</small></span></div>'+ft+'</div>';
      if(t==='promo')return '<div class="em-e">'+hd+'<div class="em-e-ban is-o"><small>LIMITED OFFER</small><h4>'+s+'</h4><a>Shop the offer</a></div><div class="em-e-3"><span><i style="--h:18"></i><b>Sambar Masala</b><small>&#8377; 85</small></span><span><i style="--h:4"></i><b>Rasam Powder</b><small>&#8377; 70</small></span><span><i style="--h:38"></i><b>Festive Gift Box</b><small>&#8377; 1,620</small></span></div><div class="em-e-cp"><small>Use code</small><b>TRADE15</b></div>'+ft+'</div>';
      if(t==='event')return '<div class="em-e">'+hd+'<div class="em-e-ban is-p"><small>MADURAI FOOD EXPO &middot; 14&ndash;16 NOV</small><h4>'+s+'</h4><p>Stall B12 &middot; Tamukkam Grounds &middot; free tasting</p><a>Register for a trade pass</a></div>'+ft+'</div>';
      return '';}
    function form(m){var ro=m.st!=='draft',btn='',tb='';
      if(m.st==='draft')btn='<button type="button" class="ox-pbtn" data-e4="send">Send</button><button type="button" class="ox-sbtn" data-e4="schedule">Schedule</button><button type="button" class="ox-sbtn" data-e4="test">Test</button>';
      if(m.st==='queue')btn='<button type="button" class="ox-pbtn" data-e4="send">Send Now</button><button type="button" class="ox-sbtn" data-e4="cancel">Cancel</button>';
      if(m.st==='done')btn='<button type="button" class="ox-sbtn" data-e4="dup">Duplicate</button>';
      var R=m.st==='done'?[[m.s[0]+'%','Received'],[m.s[1]+'%','Opened'],[m.s[2]+'%','Replied'],[m.s[3]+'%','Clicked'],[m.s[4]+'%','Bounced'],[m.lead,'Leads'],[m.quo,'Quotations'],[inr(m.rev),'Revenues']]:[];
      if(st.tab==='ab')tb='<p class="em-tab-n">Turn on <b>Allow A/B Testing</b> to send two versions to a sample and the winner to everyone else. <a href="#ab-test">See it below</a>.</p>';
      else if(st.tab==='set')tb='<dl class="em-set"><div><dt>Email From</dt><dd>Amudha Spices &lt;offers@amudhaspices.in&gt;</dd></div><div><dt>Reply To</dt><dd>sales@amudhaspices.in (creates a lead)</dd></div><div><dt>Responsible</dt><dd>'+av(m.resp,'is-sm')+' '+PPL[m.resp][0]+'</dd></div><div><dt>Mail Server</dt><dd>Bulk mail server</dd></div><div><dt>Campaign</dt><dd>Festive 2026</dd></div><div><dt>Medium / Source</dt><dd>Email / '+(m.sub?esc(m.sub.split(':')[0]):'New mailing')+'</dd></div></dl>';
      else if(!m.tpl)tb='<p class="em-tab-n">Choose a template to start, or design from scratch.</p><div class="em-tpls">'+TPL.map(function(t){return '<button type="button" class="em-tpl" data-e4t="'+t[0]+'"><span class="em-tpl-i is-'+t[0]+'"><i></i><i></i><i></i></span>'+t[1]+'</button>';}).join('')+'</div>';
      else tb='<div class="em-ebox">'+mail(m)+'</div>'+(m.st==='draft'?'<button type="button" class="em-chg" data-e4="tpl">Change template</button>':'');
      return '<div class="em-mf-bar"><span class="em-mf-btns">'+btn+'</span><span class="ox-sbar">'+COLS.map(function(c){return '<span class="ox-sb'+(m.st===c[0]?' is-cur':'')+'">'+c[1]+'</span>';}).join('')+'</span></div>'+
        (m.st==='queue'?'<p class="em-banner">This mailing is scheduled for <b>'+m.when+'</b>.</p>':'')+(m.st==='sending'?'<p class="em-banner is-s">Sending to '+num(Math.round(m.n*0.986))+' recipients&hellip; <b>'+m.prog+'%</b><i style="--p:'+m.prog+'"></i></p>':'')+
        '<div class="em-mf-sheet">'+(R.length?'<div class="em-smart">'+R.map(function(r,i){return '<span style="--i:'+i+'"><b>'+r[0]+'</b>'+r[1]+'</span>';}).join('')+'</div>':'')+
        '<div class="em-mf-f"><label><span>Subject</span><input data-e4s value="'+esc(m.sub)+'" placeholder="e.g. Our new Sambar Mix is here"'+(ro?' readonly':'')+'></label><label><span>Preview Text</span><input data-e4p value="'+esc(m.prev)+'" placeholder="Catchy preview sentence"'+(ro?' readonly':'')+'></label>'+
        '<div class="em-mf-r"><span>Recipients</span><span><b>Mailing List</b> <span class="em-pill">'+m.list+'</span> <small class="ox-muted">'+num(m.n)+' records</small></span></div></div>'+
        '<div class="ox-ftabs em-ftabs">'+[['body','Mail Body'],['ab','A/B Tests'],['set','Settings']].map(function(t){return '<button type="button" class="'+(st.tab===t[0]?'is-on':'')+'" data-e4tab="'+t[0]+'">'+t[1]+'</button>';}).join('')+'</div><div class="em-mf-body">'+tb+'</div></div>';}
    function dialog(){if(st.dlg==='test')return '<div class="em-dlg" role="dialog" aria-label="Test Mailing"><div><p class="em-dlg-h"><b>Test Mailing</b><button type="button" data-e4="close" aria-label="Close">&times;</button></p><label><span>Recipients</span><input value="priya@amudhaspices.in, design@amudhaspices.in" aria-label="Test recipients"></label><p class="em-dlg-f"><button type="button" class="ox-pbtn" data-e4="dotest">Send Sample Mail</button><button type="button" class="ox-sbtn" data-e4="close">Discard</button></p></div></div>';
      if(st.dlg==='schedule')return '<div class="em-dlg" role="dialog" aria-label="When do you want to send your mailing?"><div><p class="em-dlg-h"><b>When do you want to send your mailing?</b><button type="button" data-e4="close" aria-label="Close">&times;</button></p><div class="em-whens">'+['13 Oct, 07:30','15 Oct, 19:00','17 Oct, 10:00'].map(function(w,i){return '<label><input type="radio" name="em-when" value="'+w+'"'+(i?'':' checked')+'>'+['Tue','Thu','Sat'][i]+' '+w+'</label>';}).join('')+'</div><p class="em-dlg-f"><button type="button" class="ox-pbtn" data-e4="doschedule">Schedule</button><button type="button" class="ox-sbtn" data-e4="close">Discard</button></p></div></div>';
      return '';}
    function render(){bx.querySelectorAll('[data-e4view]').forEach(function(b){var on=!st.open&&b.getAttribute('data-e4view')===st.view;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
      dlgBox.innerHTML=dialog();
      if(st.open){var m=find(st.open);crumb.innerHTML='<a href="#" data-e4back>Mailings</a><span>'+(m.sub?esc(m.sub):'New')+'</span>';body.innerHTML=form(m);return;}
      crumb.textContent=st.view==='graph'?'Mailing Analysis':'Mailings';var l=rows();
      body.innerHTML=l.length?{kanban:kanban,list:list,calendar:calendar,graph:graph}[st.view](l):'<p class="ox-empty">No mailing matches &ldquo;'+esc(q.value)+'&rdquo;.</p>';}
    function open(id){st.open=+id;st.tab='body';st.dlg=null;render();body.scrollTop=0;}
    bx.addEventListener('input',function(e){var m=st.open&&find(st.open);if(!m)return;
      if(e.target.matches('[data-e4s]')){m.sub=e.target.value;var h=body.querySelector('.em-e-ban h4, .em-e.is-plain p:nth-child(2)');if(h)h.textContent=m.tpl==='plain'?m.sub+'.':m.sub;var c=crumb.querySelector('span');if(c)c.textContent=m.sub||'New';}
      if(e.target.matches('[data-e4p]'))m.prev=e.target.value;});
    q.addEventListener('input',function(){st.open=null;render();});
    bx.addEventListener('keydown',function(e){if(e.key==='Enter'&&!st.open){var r=e.target.closest&&e.target.closest('[data-id]');if(r){e.preventDefault();open(r.getAttribute('data-id'));}}});
    bx.addEventListener('click',function(e){
      var v=e.target.closest('[data-e4view]');if(v){st.view=v.getAttribute('data-e4view');st.open=null;render();return;}
      if(e.target.closest('[data-e4back]')){e.preventDefault();st.open=null;render();return;}
      if(e.target.closest('[data-e4new]')){var nm={id:++uid,sub:'',prev:'',list:'Newsletter',n:8912,st:'draft',when:'',day:0,resp:'P',tpl:null};M.unshift(nm);open(nm.id);return;}
      var ms=e.target.closest('[data-e4m]');if(ms){st.measure=+ms.getAttribute('data-e4m');render();return;}
      var m=st.open&&find(st.open);
      if(!m){var r=e.target.closest('[data-id]');if(r)open(r.getAttribute('data-id'));return;}
      var t=e.target.closest('[data-e4t]');if(t){m.tpl=t.getAttribute('data-e4t');render();return;}
      var tb=e.target.closest('[data-e4tab]');if(tb){st.tab=tb.getAttribute('data-e4tab');render();return;}
      var a=e.target.closest('[data-e4]');if(!a)return;var k=a.getAttribute('data-e4');
      if((k==='send'||k==='schedule'||k==='test')&&m.st==='draft'&&(!m.tpl||!m.sub)){st.tab='body';render();say(!m.sub?'Write a subject first.':'Choose a template first: the mailing has no body yet.');return;}
      if(k==='tpl')m.tpl=null;
      if(k==='test'||k==='schedule')st.dlg=k;
      if(k==='close')st.dlg=null;
      if(k==='dotest'){st.dlg=null;say('<b>Sample sent</b> to priya@ and design@. Check it on your phone before sending.');}
      if(k==='doschedule'){var rd=dlgBox.querySelector('input[name="em-when"]:checked');m.when=rd?rd.value:'';m.day=parseInt(m.when,10)||0;st.dlg=null;m.st='queue';say('<b>Scheduled.</b> Odoo sends it automatically on '+m.when+'. It now shows in the calendar.');}
      if(k==='cancel'){m.st='draft';m.when='';m.day=0;}
      if(k==='dup'){var c={id:++uid,sub:'Copy of '+m.sub,prev:m.prev,list:m.list,n:m.n,st:'draft',when:'',day:0,resp:m.resp,tpl:m.tpl};M.unshift(c);open(c.id);say('<b>Duplicated.</b> Edit the copy and schedule it.');return;}
      if(k==='send'){st.dlg=null;m.st='sending';m.prog=0;m.when='Today';m.day=10;var id=m.id;clearInterval(timer);timer=setInterval(function(){var x=find(id);x.prog=Math.min(100,x.prog+(window.matchMedia('(prefers-reduced-motion: reduce)').matches?100:9));
        if(x.prog>=100){clearInterval(timer);x.st='done';x.when='10 Oct';x.s=[98.2,47.6,2.3,14.1,1.8];x.lead=12;x.quo=7;x.rev=412000;say('<b>Sent.</b> Statistics update on the mailing as people open, click and order.');}
        if(st.open===id||!st.open)render();},160);}
      render();});
    render();})();

  /* --- 5 process --- */
  (function(){var bx=document.querySelector('[data-e5box]');if(!bx)return;var S=J('em-steps'),bt=[].slice.call(bx.querySelectorAll('[data-e5]')),card=bx.querySelector('[data-e5card]');
    function draw(i){var s=S[i];card.innerHTML='<div class="em-cfg-h"><span class="ox-av" style="--c:#B5541B">'+s[1][0]+'</span><span><b>'+s[0]+' &middot; '+s[1]+'</b><small>'+s[2]+'</small></span></div>'+
      '<ul class="em-cfg-l">'+s[3].map(function(x,j){return '<li style="--i:'+j+'"><span class="em-sw is-on" aria-hidden="true"></span><span><b>'+x[0]+'</b><small>'+x[1]+'</small></span></li>';}).join('')+'</ul>';}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);draw(+b.getAttribute('data-e5'));});});draw(0);})();

  /* --- 6 CRM flow --- */
  (function(){var bx=document.querySelector('[data-e6box]');if(!bx)return;var F=J('em-flows'),bt=[].slice.call(bx.querySelectorAll('[data-e6]')),cur=0,tm=[];
    function run(){tm.forEach(clearTimeout);tm=[];var f=F[cur],red=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      [].forEach.call(bx.querySelectorAll('[data-e6lane]'),function(l){l.classList.remove('is-on');l.querySelector('.em-lane-b').innerHTML='';});
      [].forEach.call(bx.querySelectorAll('[data-e6k]'),function(k){k.innerHTML=k.getAttribute('data-e6k')==='2'?'&#8377; 0':'0';});
      f[1].forEach(function(s,i){tm.push(setTimeout(function(){var l=bx.querySelector('[data-e6lane="'+s[0]+'"]');l.classList.add('is-on');
        l.querySelector('.em-lane-b').insertAdjacentHTML('beforeend','<div class="em-ev"><span class="em-ev-n">'+(i+1)+'</span><b>'+s[2]+'</b><small>'+s[3]+'</small></div>');
        if(i===f[1].length-1){var k=bx.querySelectorAll('[data-e6k]');k[0].textContent=f[2][0];k[1].textContent=f[2][1];k[2].innerHTML=inr(f[2][2]);}},red?0:i*650));});}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);cur=+b.getAttribute('data-e6');run();});});
    bx.querySelector('[data-e6run]').addEventListener('click',run);
    var io='IntersectionObserver' in window?new IntersectionObserver(function(en){if(en[0].isIntersecting){run();io.disconnect();}},{threshold:0.3}):null;if(io)io.observe(bx);else run();})();

  /* --- 7 quiz --- */
  (function(){var bx=document.querySelector('[data-e7box]');if(!bx)return;var R=J('em-reqs'),ans={};
    bx.addEventListener('click',function(e){var b=e.target.closest('[data-e7a]');if(!b)return;var li=b.closest('[data-e7]'),i=+li.getAttribute('data-e7');if(ans[i]!==undefined)return;
      var a=b.getAttribute('data-e7a'),ok=a===R[i][1];ans[i]=ok;li.classList.add(ok?'is-ok':'is-no');
      [].forEach.call(li.querySelectorAll('[data-e7a]'),function(x){x.disabled=true;if(x.getAttribute('data-e7a')===R[i][1])x.classList.add('is-right');});b.classList.add('is-picked');
      li.querySelector('.em-q-why').innerHTML=(ok?'<b>Right.</b> ':'<b>'+(R[i][1]==='mail'?'Mailing':'Marketing Automation')+'.</b> ')+R[i][2];
      var n=Object.keys(ans).length,s=Object.keys(ans).filter(function(k){return ans[k];}).length;bx.querySelector('[data-e7score]').textContent=s+' / '+R.length;
      bx.querySelector('[data-e7msg]').innerHTML=n<R.length?(R.length-n)+' to go.':(s>=6?'You know when to automate. Let&rsquo;s plan your journeys.':'The rule: same message and moment for everyone is a mailing; timing per person is automation.');});})();

  /* --- 8 marketing automation --- */
  (function(){var bx=document.querySelector('[data-e8box]');if(!bx)return;var A=J('em-acts'),st={s:'draft',day:0};
    function card(a){var done=st.s!=='draft'&&st.day>=a[5],sch=st.s!=='draft'&&!done,kids=A.filter(function(x){return x[1]===a[0];});
      return '<div class="em-act'+(done?' is-done':'')+'"><div class="em-act-c"><span class="em-act-i is-'+(a[3]==='Email'?'mail':'srv')+'" aria-hidden="true"></span><span class="em-act-t"><b>'+a[4]+'</b><small>'+a[3]+' &middot; '+a[6]+' '+(a[1]?'<em>'+a[2]+'</em>':a[2])+'</small></span>'+
        '<span class="em-act-n">'+(done?'<span class="is-ok">'+num(a[7])+'<small>Success</small></span><span class="is-rej">'+num(a[8])+'<small>Rejected</small></span>':(sch?'<span class="is-sch">Scheduled<small>day '+a[5]+'</small></span>':'<span class="ox-muted">&mdash;</span>'))+'</span></div>'+
        (kids.length?'<div class="em-act-k">'+kids.map(card).join('')+'</div>':'')+'</div>';}
    function draw(){bx.querySelector('[data-e8btns]').innerHTML=st.s==='draft'?'<button type="button" class="ox-pbtn" data-e8="start">Start</button>':(st.s==='run'?'<button type="button" class="ox-pbtn" data-e8="day"'+(st.day>=7?' disabled':'')+'>Next day &rarr;</button><button type="button" class="ox-sbtn" data-e8="stop">Stop</button>':'<button type="button" class="ox-sbtn" data-e8="reset">Reset</button>');
      [].forEach.call(bx.querySelectorAll('[data-e8s]'),function(x){x.classList.toggle('is-cur',x.getAttribute('data-e8s')===st.s);});
      var p=st.s==='draft'?0:1000,mails=A.filter(function(a){return a[3]==='Email'&&st.s!=='draft'&&st.day>=a[5];}).reduce(function(t,a){return t+a[7];},0);
      bx.querySelector('[data-e8sum]').innerHTML='<span><b>'+num(st.day>=7?0:p)+'</b>Running</span><span><b>'+num(st.day>=7?p:0)+'</b>Completed</span><span><b>'+num(mails)+'</b>Emails sent</span><span class="em-day">'+(st.s==='draft'?'Not started':'Day '+st.day+' of 7')+'<i style="--p:'+(st.day/7*100)+'"></i></span>';
      bx.querySelector('[data-e8tree]').innerHTML=A.filter(function(a){return !a[1];}).map(card).join('')+'<p class="em-add">Add child activity: <span>Opened</span><span>Not opened</span><span>Replied</span><span>Clicked</span><span>Not clicked</span><span>Bounced</span></p>';}
    bx.addEventListener('click',function(e){var b=e.target.closest('[data-e8]');if(!b)return;var k=b.getAttribute('data-e8');
      if(k==='start'){st.s='run';st.day=0;}if(k==='day')st.day=Math.min(7,st.day+1);if(k==='stop')st.s='stop';if(k==='reset'){st.s='draft';st.day=0;}draw();});draw();})();

  /* --- 9 measure --- */
  (function(){var bx=document.querySelector('[data-e9box]');if(!bx)return;var M=J('em-mails'),rows=[].slice.call(bx.querySelectorAll('[data-e9]')),card=bx.querySelector('[data-e9card]');
    function draw(i){var m=M[i],sent=m[3],rcv=Math.round(sent*m[4]/100),op=Math.round(sent*m[5]/100),cl=Math.round(sent*m[7]/100);
      var F=[['Sent',sent],['Received',rcv],['Opened',op],['Clicked',cl]];
      card.innerHTML='<p class="em-st-h"><b>'+m[0]+'</b><small>'+m[1]+' &middot; sent '+m[2]+'</small></p><div class="em-smart is-card">'+[[m[4]+'%','Received'],[m[5]+'%','Opened'],[m[6]+'%','Replied'],[m[7]+'%','Clicked'],[m[8]+'%','Bounced']].map(function(r,j){return '<span style="--i:'+j+'"><b>'+r[0]+'</b>'+r[1]+'</span>';}).join('')+'</div>'+
        '<ul class="em-fun">'+F.map(function(f){return '<li><span>'+f[0]+'</span><i style="--p:'+(f[1]/sent*100)+'"></i><b>'+num(f[1])+'</b></li>';}).join('')+'</ul>'+
        '<div class="em-money"><span><b>'+m[9]+'</b>Leads</span><span><b>'+m[10]+'</b>Quotations</span><span><b>'+inr(m[11])+'</b>Revenues</span><span><b>'+inr(Math.round(m[11]/sent))+'</b>per email sent</span></div>';}
    rows.forEach(function(r){r.addEventListener('click',function(){rows.forEach(function(x){x.classList.toggle('is-on',x===r);});draw(+r.getAttribute('data-e9'));});});draw(0);})();

  /* --- 10 A/B --- */
  (function(){var bx=document.querySelector('[data-e10box]');if(!bx)return;var D=J('em-ab'),on=bx.querySelector('[data-e10on]'),pin=bx.querySelector('[data-e10p]'),w=bx.querySelector('[data-e10w]'),res=bx.querySelector('[data-e10res]');
    var LB={open:'Open rate',click:'Click rate',lead:'Leads',rev:'Revenues'};
    function fmt(v,u){return u==='%'?v.toFixed(1)+'%':(u==='inr'?inr(v):v);}
    function note(){var p=+pin.value,t=Math.round(D.n*p/100);bx.querySelector('[data-e10pv]').textContent=p;
      bx.querySelector('[data-e10note]').innerHTML='Each version goes to <b>'+num(Math.round(t/2))+'</b> retailers. The winner goes to the other <b>'+num(D.n-t)+'</b> on <b>Tue 13 Oct, 07:30</b>.';
      bx.querySelector('[data-e10in]').classList.toggle('is-off',!on.checked);res.innerHTML='';}
    function pick(win){var t=Math.round(D.n*(+pin.value)/100);res.insertAdjacentHTML('beforeend','<p class="em-win">'+TK+' Version <b>'+win+'</b> wins. Final mailing sent to the remaining <b>'+num(D.n-t)+'</b> recipients.</p>');}
    function run(){var k=w.value,show=k==='manual'?['open','click','lead','rev']:[k];
      res.innerHTML=show.map(function(m){var r=D.res[m],mx=Math.max(r[0],r[1]);return '<div class="em-abm"><small>'+LB[m]+'</small>'+['A','B'].map(function(v,i){return '<p class="'+(k!=='manual'&&r[i]===mx?'is-win':'')+'"><span>'+v+'</span><i style="--p:'+(r[i]/mx*100)+'"></i><b>'+fmt(r[i],r[2])+'</b></p>';}).join('')+'</div>';}).join('');
      if(k==='manual')res.insertAdjacentHTML('beforeend','<p class="em-pickw">Pick the winner: <button type="button" class="ox-sbtn" data-e10pick="A">Send version A</button><button type="button" class="ox-sbtn" data-e10pick="B">Send version B</button></p>');
      else{var r=D.res[k];pick(r[0]>r[1]?'A':'B');}}
    on.addEventListener('change',note);pin.addEventListener('input',note);w.addEventListener('change',function(){res.innerHTML='';});
    bx.querySelector('[data-e10run]').addEventListener('click',function(){if(on.checked)run();});
    res.addEventListener('click',function(e){var b=e.target.closest('[data-e10pick]');if(!b)return;var p=res.querySelector('.em-pickw');if(p)p.remove();pick(b.getAttribute('data-e10pick'));});note();})();

  /* --- 11 deliverability & unsubscribe --- */
  (function(){var bx=document.querySelector('[data-e11box]');if(!bx)return;var R=J('em-recs'),ring=bx.querySelector('[data-e11ring]');
    function draw(){var v=43,n=0;[].forEach.call(bx.querySelectorAll('[data-e11]'),function(c){if(c.checked){v+=R[+c.getAttribute('data-e11')][4];n++;}});
      ring.style.setProperty('--p',v);bx.querySelector('[data-e11v]').textContent=v+'%';
      bx.querySelector('[data-e11msg]').textContent=n===R.length?'All six in place. This is where we leave every client.':(n<3?'Without SPF, DKIM and DMARC, Gmail and Outlook treat bulk mail as suspect.':(R.length-n)+' left. Each one moves more mail out of spam.');}
    bx.addEventListener('change',draw);draw();})();
  (function(){var bx=document.querySelector('[data-e11ubox]');if(!bx)return;var S=J('em-subs'),RS=J('em-reasons'),u=bx.querySelector('[data-e11u]'),rec=bx.querySelector('[data-e11rec]'),
    st={page:false,subs:S.map(function(s){return s[1];}),reason:null,block:false,saved:false};
    function draw(){
      if(!st.page)u.innerHTML='<p class="em-u-h"><b>October recipe newsletter</b><small>From Amudha Spices &middot; to lakshmi.r@gmail.com</small></p><div class="em-u-mail"><span></span><span></span><span class="is-s"></span></div><p class="em-u-ft">Amudha Spices, Madurai &middot; <button type="button" data-e11go>Unsubscribe</button> &middot; Manage preferences</p>';
      else{var off=S.some(function(s,i){return s[1]&&!st.subs[i];})||st.block;
        u.innerHTML='<div class="em-u-url mono">amudhaspices.in/mailing/my</div><p class="em-u-h"><b>Manage your mailing subscriptions</b><small>lakshmi.r@gmail.com</small></p>'+
        '<ul class="em-u-subs">'+S.map(function(s,i){return '<li><label><input type="checkbox" data-e11s="'+i+'"'+(st.subs[i]?' checked':'')+(st.block?' disabled':'')+'><span class="em-sw" aria-hidden="true"></span>'+s[0]+'</label></li>';}).join('')+'</ul>'+
        '<label class="em-u-bl"><input type="checkbox" data-e11b'+(st.block?' checked':'')+'> Exclude me from all mailings (blocklist)</label>'+
        (off?'<p class="em-u-q">Please let us know why you updated your subscription.</p><div class="em-u-rs">'+RS.map(function(r,i){return '<label><input type="radio" name="em-rs" data-e11r="'+i+'"'+(st.reason===i?' checked':'')+'>'+r+'</label>';}).join('')+'</div>':'')+
        '<p class="em-u-f"><button type="button" class="ox-pbtn" data-e11save'+(off?'':' disabled')+'>Update my subscriptions</button><button type="button" class="ox-sbtn" data-e11back>Back to the email</button></p>';}
      var ch=S.map(function(s,i){return [s[0],st.saved&&s[1]&&!st.subs[i]];});
      rec.innerHTML='<p class="em-u-h"><b>In Odoo</b><small>Mailing List Contacts &middot; lakshmi.r@gmail.com</small></p><table class="ox-table em-u-t"><thead><tr><th>Mailing List</th><th>Opt Out</th><th>Reason</th></tr></thead><tbody>'+
        ch.map(function(c,i){return '<tr><td>'+c[0]+'</td><td>'+(c[1]||(st.saved&&st.block)?'<span class="em-oo">'+TK+'</span>':(S[i][1]?'<span class="ox-muted">No</span>':'<span class="ox-muted">Not a member</span>'))+'</td><td>'+((c[1]||(st.saved&&st.block&&S[i][1]))&&st.reason!==null?RS[st.reason]:'')+'</td></tr>';}).join('')+'</tbody></table>'+
        '<p class="em-u-bk'+(st.saved&&st.block?' is-on':'')+'">'+(st.saved&&st.block?TK+' Added to the <b>Blacklist</b>. No mailing can reach this address again.':'Blacklist: not listed')+'</p>'+
        (st.saved?'<p class="em-u-log">Logged on the contact: <b>unsubscribed '+(st.block?'from all mailings':'from '+ch.filter(function(c){return c[1];}).map(function(c){return c[0];}).join(', '))+'</b>.</p>':'<p class="em-u-log ox-muted">Unsubscribe as Lakshmi to see what Odoo records.</p>');}
    bx.addEventListener('click',function(e){if(e.target.closest('[data-e11go]')){st.page=true;draw();return;}if(e.target.closest('[data-e11back]')){st={page:false,subs:S.map(function(s){return s[1];}),reason:null,block:false,saved:false};draw();return;}
      if(e.target.closest('[data-e11save]')){st.saved=true;draw();}});
    bx.addEventListener('change',function(e){var s=e.target.closest('[data-e11s]');if(s){st.subs[+s.getAttribute('data-e11s')]=s.checked;st.saved=false;}
      if(e.target.matches('[data-e11b]')){st.block=e.target.checked;st.saved=false;}var r=e.target.closest('[data-e11r]');if(r)st.reason=+r.getAttribute('data-e11r');draw();});draw();})();

  /* --- 12 phases --- */
  (function(){var bx=document.querySelector('[data-e12box]');if(!bx)return;var P=J('em-phases'),bt=[].slice.call(bx.querySelectorAll('[data-e12]'));
    function draw(i){bx.querySelector('[data-e12d]').innerHTML=P[i][2].map(function(d,j){return '<li style="--i:'+j+'"><span class="em-file" aria-hidden="true"></span>'+d+'</li>';}).join('');bx.querySelector('[data-e12y]').innerHTML=P[i][3];}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);draw(+b.getAttribute('data-e12'));});});draw(0);})();

  /* --- 13 planner --- */
  (function(){var bx=document.querySelector('[data-e13box]');if(!bx)return;
    function v(k){return bx.querySelector('[data-e13="'+k+'"]');}function x(k){return bx.querySelector('[data-e13x="'+k+'"]').checked;}
    function draw(){var c=+v('contacts').value,m=+v('mails').value,f=+v('from').value,o=+v('odoo').value,au=x('auto'),ab=x('ab'),sm=x('sms');
      bx.querySelector('[data-e13o="contacts"]').textContent=num(c);bx.querySelector('[data-e13o="mails"]').textContent=m;
      var wk=2+(c>30000?1:0)+(f>0?1:0)+(o===0?2:0)+(au?1:0)+(ab?0.5:0)+(sm?0.5:0);
      var pk=o===0?['Odoo CRM + Email Marketing','Contacts, CRM and campaigns set up together']:(au?['Email Marketing + Automation','Mailings plus automated journeys']:['Email Marketing essentials','Lists, templates, domain and reporting']);
      var apps=['Email Marketing','Contacts'];if(au)apps.push('Marketing Automation');if(o>0||ab)apps.push('CRM');if(o===2||ab)apps.push('Sales');if(o===2)apps.push('eCommerce');if(sm)apps.push('SMS Marketing');
      var ask=['Where your contacts and unsubscribes live today'];if(c>30000)ask.push('Daily sending volume and a dedicated mail server');if(f===1)ask.push('Mailchimp audiences, tags and groups to map to lists');if(au)ask.push('Which journeys matter most: welcome, win-back, post-purchase');if(sm)ask.push('SMS or WhatsApp provider and templates');
      bx.querySelector('[data-e13out]').innerHTML='<div class="em-pk"><p class="mono">RECOMMENDED</p><b>'+pk[0]+'</b><small>'+pk[1]+'</small><span class="em-pk-wk">'+(Math.round(wk*2)/2)+'&ndash;'+(Math.round(wk*2)/2+1)+' weeks</span></div>'+
        '<div><p class="em-gi-h">Apps</p><p class="em-chips">'+apps.map(function(a){return '<span>'+a+'</span>';}).join('')+'</p><p class="em-gi-h">We&rsquo;ll ask about</p><ul class="em-ask">'+ask.map(function(a){return '<li>'+a+'</li>';}).join('')+'</ul></div>';}
    bx.addEventListener('input',draw);bx.addEventListener('change',draw);draw();})();
})();
</script>
'''
