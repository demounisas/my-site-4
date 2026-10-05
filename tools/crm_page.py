"""
Odoo CRM page: its own layouts (lead-journey hero, funnel, readiness check,
Kanban board, bento, rule cards, orbit, package card, Gantt timeline, report
mock, industry tabs, numbered reasons). It shares the brand (colours, type,
buttons, header, footer, contact form) with the homepage but none of its
section designs. Styles live under "Odoo CRM page" in dist/assets/modules.css.

hero(g) and build(g) get the build script's globals.
"""

import json

import crm_explorer as ox

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def icon(paths, size=20):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (size, size, paths))


IC = dict(
    inbox=icon('<path d="M3 13l3-8h12l3 8v6H3z"/><path d="M3 13h5l1 3h6l1-3h5"/>'),
    funnel=icon('<path d="M3 4h18l-7 8v7l-4 2v-9z"/>'),
    people=icon('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.5 3.4-5.5 6.5-5.5s5.7 2 6.5 5.5"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14.8c1.9.7 3.1 2.5 3.5 5.2"/>'),
    bell=icon('<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 21h4"/>'),
    doc=icon('<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>'),
    target=icon('<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>'),
    gear=icon('<circle cx="12" cy="12" r="3"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/>'),
    plug=icon('<path d="M9 3v5M15 3v5M6 8h12v3a6 6 0 0 1-12 0z"/><path d="M12 17v4"/>'),
    grad=icon('<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5"/>'),
    chat=icon('<path d="M4 5h16v11H9l-5 4z"/>'),
    mail=icon('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>'),
    phone=icon('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
    globe=icon('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 3 2.5 15 0 18M12 3c-2.5 3-2.5 15 0 18"/>'),
    cal=icon('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
    link=icon('<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>'),
    spark=icon('<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5L18 18M6 18l2.5-2.5M15.5 8.5L18 6"/>'),
    code=icon('<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 5l-3 14"/>'),
)


STAR = '<span class="ox-star%s"><svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.9 6.8 19.6l1-5.8L3.5 9.7l5.9-.8z"/></svg></span>'
STARS3 = (STAR % " is-on") * 3


def stars(n):
    return "".join(STAR % (" is-on" if i < n else "") for i in range(3))


def head(eyebrow, title, sub="", cls=""):
    return ('<div class="crm-head%s"><p class="crm-eyebrow mono">%s</p><h2 class="crm-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="crm-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="crm-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">CRM</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["Leads from web, email &amp; WhatsApp", "Stages that match your process", "Forecasts you can trust"])
    copy = ('<div class="crm-hero-copy">%s<p class="crm-eyebrow mono">ODOO CRM IMPLEMENTATION</p>'
            '<h1 class="crm-h1">CRM Implementation for <span>Smarter Sales</span>, Powered by Odoo</h1>'
            '<p class="crm-lead">We set up Odoo CRM around the way your team sells, so every lead lands in one pipeline, every follow-up is scheduled, '
            'and managers can forecast from real deals.</p><ul class="crm-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Discuss Odoo CRM %s</a>'
            '<a href="#setup" class="btn btn-ghost">How we set it up</a></div></div>' % (crumb, points, g["ARROW"]))
    journey = '''<div class="crm-journey" aria-hidden="true">
      <div class="crm-j-card crm-j-in"><div class="crm-j-top"><span class="crm-j-ic is-wa">%s</span><span><strong>New enquiry</strong><small>WhatsApp · 2 min ago</small></span></div>
        <p class="crm-j-bubble">Hi, we need one system for sales and stock across 3 branches. Can we talk this week?</p></div>
      <div class="crm-j-card crm-j-lead ox-solo"><p class="crm-j-label"><span class="crm-j-ic is-crm">%s</span>Lead created in <b>Qualified</b></p>
        <article class="ox-card is-static"><b class="ox-c-name">ERP for 3 branches</b><span class="ox-c-rev">&#8377; 12,00,000.00</span>
          <span class="ox-c-cust"><span class="ox-logo">S</span>Shree Distributors</span><span class="ox-tags"><span class="ox-tag ox-tag--green">Consulting</span></span>
          <span class="ox-c-foot"><span class="ox-stars">%s</span><span class="ox-act ox-act--orange">%s</span><span class="ox-team">Sales</span><span class="ox-av" style="--c:#4C9F70">M</span></span></article>
        <p class="crm-j-next">%s Call to confirm requirements · Today</p></div>
      <div class="crm-j-card crm-j-won ox-solo"><span class="ox-sbar is-mini"><span class="ox-sb is-done">Qualified</span><span class="ox-sb is-done">Proposition</span><span class="ox-sb is-cur">Won</span></span><span><strong>Quotation signed online</strong><small>Sales order created automatically</small></span><span class="ox-mini-ribbon">WON</span></div>
      <svg class="crm-j-path" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M30 18 C 70 22, 80 38, 62 50 S 30 76, 58 88" fill="none" stroke="currentColor" stroke-width="0.6" stroke-dasharray="2 2"/></svg>
    </div>''' % (icon('<path d="M4 20l1.3-4A8 8 0 1 1 8 18.7z"/>', 18), icon('<path d="M3 4h18l-7 8v7l-4 2v-9z"/>', 14), STARS3,
                 icon('<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>', 14),
                 icon('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>', 14))
    return '<section class="crm-hero">%s%s</section>' % (copy, journey)


# ------------------------------------------------------------------ sections
def inr(n):
    """Indian-format rupees (12,00,000.00); blank for zero, like an Odoo pivot cell."""
    if not n:
        return ""
    digits = "%d" % n
    rest, last3 = digits[:-3], digits[-3:]
    groups = []
    while len(rest) > 2:
        groups.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.insert(0, rest)
    return "&#8377; " + ",".join(groups + [last3]) + ".00"


def build(g):
    out = ""

    # 2 ---- what is Odoo CRM: interactive Odoo CRM explorer
    benefits = [(IC["inbox"], "One home for every enquiry", "Leads from your website, email, WhatsApp and calls land in one pipeline, tagged by source."),
                (IC["bell"], "No follow-up forgotten", "Every deal carries its next activity, coloured green, orange or red as it comes due."),
                (IC["target"], "Forecasts from real deals", "Expected revenue and probability come straight from the pipeline, not a spreadsheet.")]
    ben = "".join('<li><span class="crm-ic">%s</span><span><strong>%s</strong>%s</span></li>' % b for b in benefits)
    out += sec(head("WHAT IS ODOO CRM", "What Is Odoo CRM and How Can It Improve Your Sales Process?",
                    "Odoo CRM is the sales pipeline app inside Odoo ERP. It tracks every lead and opportunity from first enquiry to signed deal, "
                    "and shares its data with Sales, Invoicing and Email Marketing, so nothing is typed twice. Try it below: this is how your team's pipeline looks in Odoo.",
                    "is-center is-wide")
               + ox.frame(g["TILE_ICONS"][1]) + '<ul class="crm-benefits is-row">%s</ul>' % ben, "crm-sec--what")

    # 3 ---- readiness self-check
    signs = ["Leads come from several channels and some never get a reply",
             "Your pipeline lives in a spreadsheet only one person updates",
             "Nobody knows what will close this month without asking around",
             "Customer history leaves when a salesperson leaves",
             "Quotes are typed separately from the deal they belong to",
             "You're hiring salespeople and need clear lead rules"]
    chips = "".join('<button type="button" class="crm-q-chip" aria-pressed="false"><span class="crm-q-box">%s</span>%s</button>' % (TICK, s) for s in signs)
    out += sec('<div class="crm-quiz">%s<div class="crm-q-grid">%s</div>'
               '<div class="crm-q-result" aria-live="polite"><div class="crm-q-meter"><i style="--p:0"></i></div>'
               '<p class="crm-q-msg"><strong class="mono">0 / 6</strong><span>Tick the statements that sound like your team.</span></p>'
               '<a href="#get-demo" class="btn btn-primary btn-red crm-q-cta" data-svc-cta="implementation" hidden>Map my pipeline %s</a></div></div>'
               % (head("READINESS CHECK", "Is Your Sales Process Ready for a CRM?", "Tick what sounds familiar. Two or more and a CRM will pay for itself quickly. You don't need a perfect process first; we help you define it.", "is-center"),
                  chips, g["ARROW"]), "crm-sec--quiz")

    # 4 ---- designed around your process: Kanban board
    cols = [("CAPTURE", "01", "Every enquiry lands in one place", "Website forms, email aliases and WhatsApp create leads automatically, tagged by source.",
             ["Website & landing page forms", "Email-to-lead aliases", "Duplicate detection & merging"]),
            ("QUALIFY", "02", "The right lead reaches the right person", "Scoring and assignment rules route good leads by region, product or deal size.",
             ["Assignment by territory or product", "Lead scoring on your criteria", "Lost reasons you can report on"]),
            ("CLOSE", "03", "Deals keep moving until they're won", "Stages mirror your sales steps, and quotes are created straight from the deal.",
             ["Stages that match your process", "Quote directly from the deal", "Won deals flow into Sales & Invoicing"])]
    board = "".join('<div class="crm-col crm-col--%d"><p class="crm-col-head mono"><span>%s</span><b>%s</b></p><h3>%s</h3><p>%s</p>%s</div>'
                    % (i, tag, n, t, x, "".join('<div class="crm-kcard"><i></i>%s</div>' % p for p in pts)) for i, (tag, n, t, x, pts) in enumerate(cols))
    out += sec(head("OUR CRM DESIGN", "How We Design Odoo CRM Around Your Sales Process",
                    "We start from how your team actually sells, then shape Odoo's stages, rules and views around it.") + '<div class="crm-board">%s</div>' % board,
               "crm-sec--board", "setup")

    # 5 ---- what you can manage: bento
    mini = ('<div class="crm-bento-cards ox-solo" aria-hidden="true">'
            '<article class="ox-card is-static"><b class="ox-c-name">Quote for 40 POS terminals</b><span class="ox-c-rev">&#8377; 6,40,000.00</span>'
            '<span class="ox-c-cust"><span class="ox-logo">B</span>Bluebay Retail</span><span class="ox-tags"><span class="ox-tag ox-tag--red">Product</span></span>'
            '<span class="ox-c-foot"><span class="ox-stars">%s</span><span class="ox-act ox-act--green">%s</span><span class="ox-team">Sales</span><span class="ox-av" style="--c:#B5567E">A</span></span></article>'
            '<article class="ox-card is-static"><b class="ox-c-name">Clinic group onboarding</b><span class="ox-c-rev">&#8377; 5,25,000.00</span>'
            '<span class="ox-c-cust"><span class="ox-logo">S</span>Sunrise Clinics</span><span class="ox-tags"><span class="ox-tag ox-tag--green">Consulting</span></span>'
            '<span class="ox-c-foot"><span class="ox-stars">%s</span><span class="ox-act ox-act--red">%s</span><span class="ox-team">Sales</span><span class="ox-av" style="--c:#4C9F70">M</span></span></article></div>'
            % (stars(2), icon('<circle cx="9" cy="8" r="3"/><path d="M3 19c.6-3 3-5 6-5s5.4 2 6 5"/>', 14), stars(3),
               icon('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>', 14)))
    tiles = [("is-big", IC["funnel"], "Opportunities &amp; Pipeline", "Drag deals through stages on a Kanban board, with value, probability and expected close date on every card.", mini),
             ("", IC["inbox"], "Leads &amp; Enquiries", "Capture, de-duplicate and qualify enquiries before they reach the pipeline.", ""),
             ("is-dark", IC["bell"], "Activities &amp; Follow-ups", "Calls, meetings and to-dos on each deal, with reminders when they're due.", ""),
             ("", IC["people"], "Customers &amp; Contacts", "Companies, contacts and the full history of calls, emails and deals.", ""),
             ("", IC["doc"], "Quotations", "Turn an opportunity into a branded quote in one click.", ""),
             ("is-tint", IC["target"], "Sales Teams &amp; Targets", "Teams, territories and targets, with a dashboard for each manager.", "")]
    bento = "".join('<div class="crm-tile %s"><span class="crm-ic">%s</span><h3>%s</h3><p>%s</p>%s</div>' % t for t in tiles)
    out += sec(head("WHAT YOU CAN MANAGE", "What Can You Manage With Odoo CRM?", "One app covers the whole sales cycle, from first enquiry to the quote that wins the deal.")
               + '<div class="crm-bento">%s</div>' % bento, "crm-sec--bento")

    # 6 ---- automations: rule cards on navy
    rules = [("On creation", "A website form or email creates a lead", "Tag the source and assign the right salesperson by territory"),
             ("On save", "A lead matches your ideal-customer rules", "Set priority to high and move it up the salesperson's list"),
             ("Based on date field", "Last stage update is more than 7 days ago", "Schedule a follow-up call and notify the sales manager"),
             ("Stage is set to", "Stage is set to Proposition", "Create the quotation from your template, ready to send"),
             ("Stage is set to", "Stage is set to Won", "Confirm the sales order and hand over to delivery"),
             ("On archived", "A deal is marked lost", "Log the lost reason and add the contact to a nurture campaign")]
    cards = "".join('<li class="crm-rule"><span class="crm-rule-n mono">TRIGGER · %s</span><p><b class="mono">WHEN</b>%s</p><p><b class="mono">THEN</b>%s</p>'
                    '<span class="crm-toggle" aria-hidden="true"><i></i></span></li>' % (trg.upper(), w, t) for trg, w, t in rules)
    out += sec('<div class="crm-auto-wrap">%s<ul class="crm-rules">%s</ul></div>'
               % (head("AUTOMATION", "What CRM Processes Can Unisas Automate?",
                       "We automate the repetitive steps between your sales stages, so your team spends its time on conversations, not admin. These are the Odoo automation rules we set up most often."), cards),
               "crm-sec--auto")

    # 7 ---- integrations: orbit
    nodes = [(IC["globe"], "Website forms"), (IC["chat"], "WhatsApp"), (IC["mail"], "Email"), (IC["phone"], "Phone / VoIP"),
             (IC["cal"], "Google &amp; Outlook calendars"), (IC["link"], "LinkedIn &amp; ads"), (IC["spark"], "Marketing tools"), (IC["code"], "Custom APIs")]
    orbit = "".join('<li style="--k:%d"><span class="crm-o-node"><span class="crm-o-ic">%s</span><span class="crm-o-name">%s</span></span></li>' % (i, ic, n) for i, (ic, n) in enumerate(nodes))
    core = g["TILE_ICONS"][1]
    out += sec('<div class="crm-integ">%s<div class="crm-orbit" style="--n:%d"><div class="crm-o-core"><span class="crm-o-logo">%s</span><strong>Odoo CRM</strong><small class="mono">TWO-WAY SYNC</small></div><ul>%s</ul></div></div>'
               % (head("INTEGRATIONS", "How Can Odoo CRM Connect With Your Existing Business Systems?",
                       "Odoo CRM connects to the channels your leads already come from and the tools your team already uses, so enquiries, emails and calls are logged against the right deal automatically."
                       ' <a class="crm-inline-link" href="odoo-integration.html">See our integration service</a>'),
                  len(nodes), core, orbit), "crm-sec--integ")

    # 8 ---- what's included: one package card
    pk = [(IC["gear"], "Setup &amp; configuration", ["Pipeline stages &amp; sales teams", "Lead scoring &amp; assignment rules", "Activity types &amp; email templates", "Dashboards for each manager"]),
          (IC["plug"], "Data &amp; integrations", ["Import from Excel or your current CRM", "Website, email &amp; WhatsApp capture", "Calendar &amp; phone integration", "Link to Sales and Invoicing"]),
          (IC["grad"], "Training &amp; support", ["Role-based training for sales &amp; managers", "Short user guides for daily tasks", "Hypercare support after launch", "Improvements as you grow"])]
    colsh = "".join('<div class="crm-pk-col"><span class="crm-ic">%s</span><h3>%s</h3><ul>%s</ul></div>' % (ic, t, "".join("<li>%s%s</li>" % (TICK, p) for p in pts)) for ic, t, pts in pk)
    out += sec(head("WHAT'S INCLUDED", "What Does an Odoo CRM Implementation With Unisas Include?", "Everything needed to take your team from spreadsheets to a working pipeline, in one fixed-scope project.", "is-center")
               + '<div class="crm-package"><div class="crm-pk-head"><span class="mono">ODOO CRM IMPLEMENTATION PACKAGE</span><strong>Fixed scope · agreed up front</strong></div>'
                 '<div class="crm-pk-body">%s</div><div class="crm-pk-foot"><span>Need more than CRM? We extend the same project to Sales, Invoicing or Email Marketing.</span>'
                 '<a href="#get-demo" class="link-arrow" data-svc-cta="implementation">Get a scoped quote %s</a></div></div>' % (colsh, g["ARROW"]), "crm-sec--pkg")

    # 9 ---- process: six phases, and how the client's CRM pipeline takes shape in each
    phases = [("Discover", "Week 1", "Workshops with your sales team: how leads arrive, who follows them up, and what managers need to see.",
               "Sales process map", "2 workshops of 2 hours"),
              ("Design", "Week 2", "Pipeline stages, lead rules, automations and reports agreed on paper before anything is built.",
               "Design document with your stages", "1 review meeting"),
              ("Configure", "Weeks 3&ndash;4", "Sales teams, assignment rules, activity types, email templates and dashboards set up on a test database.",
               "Walkthrough of the test database", "1 hour a week"),
              ("Migrate &amp; connect", "Weeks 4&ndash;5", "Leads and customers imported from your spreadsheets or old CRM; website forms, email and WhatsApp connected.",
               "Data check: 2,340 leads and 860 customers", "Your current data exports"),
              ("Train", "Week 6", "Salespeople and managers learn on their own pipeline, with short guides for daily tasks.",
               "Every user logs a test deal", "Half a day per team"),
              ("Go live &amp; hypercare", "Weeks 6&ndash;8", "Switch-over to Odoo, daily check-ins in the first weeks, rules refined as the team settles in.",
               "Hypercare report after two weeks", "A go-live date")]
    steps = "".join('<li><button type="button" class="crm-pr-st%s" data-pr="%d" aria-pressed="%s"><span class="mono">%02d</span><b>%s</b><small>%s</small></button></li>'
                    % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", i + 1, n, w) for i, (n, w, d, so, you) in enumerate(phases))
    out += sec(head("OUR PROCESS", "What Does the Unisas Odoo CRM Implementation Process Look Like?",
                    "Six phases, each ending with something you sign off. Pick a phase to see what happens in it and how your Odoo CRM pipeline looks at that point. "
                    "A typical rollout takes six to eight weeks; integrations and data decide the rest.", "is-center")
               + '<div class="crm-pr" data-prbox><ol class="crm-pr-sts">%s</ol><div class="crm-pr-g"><div class="crm-pr-bd ox-solo" data-prboard aria-hidden="true"></div>'
                 '<div class="crm-pr-c" data-prcard aria-live="polite"></div></div></div>' % steps
               + '<script type="application/json" id="crm-phases">%s</script>' % json.dumps(phases), "crm-sec--proc")

    # 10 ---- results: report mock
    kpis = [("Pipeline value", "By stage, salesperson and expected close month", "M2 18 L10 14 L18 15 L26 9 L34 10 L42 4"),
            ("Win rate", "Conversion from lead to deal, by source", "M2 16 L10 15 L18 11 L26 12 L34 7 L42 6"),
            ("Sales cycle", "How long deals take to move through each stage", "M2 6 L10 8 L18 7 L26 11 L34 12 L42 15"),
            ("Activity", "Calls, meetings and follow-ups done per person", "M2 14 L10 9 L18 12 L26 6 L34 9 L42 5"),
            ("Lost reasons", "Why deals are lost, so you can fix the pattern", "M2 10 L10 12 L18 9 L26 11 L34 8 L42 9")]
    tiles = "".join('<div class="crm-kpi"><svg viewBox="0 0 44 20" aria-hidden="true"><path d="%s" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                    '<strong>%s</strong><span>%s</span></div>' % (p, t, x) for t, x, p in kpis)
    cols = ["This month", "Next month", "Later"]
    data = [("New", [0, 210000, 480000]), ("Qualified", [640000, 1200000, 0]), ("Proposition", [525000, 360000, 290000]), ("Won", [980000, 0, 0])]
    tot = [sum(r[1][i] for r in data) for i in range(3)]
    thead = '<tr><th></th>%s<th>Total</th></tr>' % "".join('<th>%s</th>' % c for c in cols)
    tbody = '<tr class="is-total"><th>&#9662; Total</th>%s<td>%s</td></tr>' % ("".join("<td>%s</td>" % inr(v) for v in tot), inr(sum(tot)))
    tbody += "".join('<tr><th>%s</th>%s<td>%s</td></tr>' % (n, "".join("<td>%s</td>" % inr(v) for v in vals), inr(sum(vals))) for n, vals in data)
    pivot = ('<div class="ox-solo ox-pv"><div class="ox-pv-bar"><span class="ox-crumb">Pipeline Analysis</span>'
             '<span class="ox-measure"><span class="is-on">Expected Revenue</span></span></div>'
             '<div class="ox-scroll"><table class="ox-pivot"><thead><tr><th></th><th colspan="4">&#9662; Expected Closing</th></tr>%s</thead><tbody>%s</tbody></table></div></div>'
             % (thead, tbody))
    out += sec('<div class="crm-results">%s<div class="crm-report" aria-label="Example Odoo CRM pipeline analysis">%s<div class="crm-kpis">%s</div></div></div>'
               % (head("RESULTS YOU CAN TRACK", "What Business Results Can You Track With Odoo CRM?",
                       "Because CRM shares data with Sales and Invoicing, every report reflects what was actually quoted, won and billed, and updates as deals move. "
                       "Slice any of these by salesperson, team, source or month."), pivot, tiles),
               "crm-sec--results")

    # 11 ---- businesses: industry tabs
    inds = [("manufacturing", "Manufacturing", "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=720&q=70&auto=format&fit=crop", "Engineer working on a production line",
             ["Dealer and distributor enquiries in one pipeline", "Project quotes built from your product catalogue", "Repeat-order reminders for key accounts"], ["CRM", "Sales", "MRP"]),
            ("retail", "Retail &amp; Distribution", "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=720&q=70&auto=format&fit=crop", "Retail clothing store interior",
             ["B2B accounts and dealer networks by territory", "Bulk-order opportunities with pricelists", "Visit and call plans for field sales"], ["CRM", "Sales", "Inventory"]),
            ("services", "Professional Services", "https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=720&q=70&auto=format&fit=crop", "Team working together on laptops",
             ["Enquiries turned into proposals", "Won deals become projects automatically", "Retainer renewals tracked before they lapse"], ["CRM", "Project", "Invoicing"]),
            ("trading", "Trading &amp; Import/Export", "https://images.unsplash.com/photo-1494412574643-ff11b0a5c1c3?w=720&q=70&auto=format&fit=crop", "Container port with cranes and shipping containers",
             ["Buyer enquiries across markets and currencies", "Sample and quote follow-ups scheduled", "Margins visible before the quote goes out"], ["CRM", "Sales", "Purchase"]),
            ("healthcare", "Healthcare &amp; Clinics", "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=720&q=70&auto=format&fit=crop", "Doctor using a smartphone",
             ["Patient and corporate enquiries in one place", "Follow-up calls scheduled automatically", "Campaigns for health checks and packages"], ["CRM", "Appointments", "Email"]),
            ("education", "Education &amp; Training", "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=720&q=70&auto=format&fit=crop", "Books, an apple and alphabet blocks on a desk",
             ["Admissions enquiries by course and campus", "Counselling calls and reminders", "Enrolment pipeline managers can forecast"], ["CRM", "Events", "eLearning"])]
    tabs = "".join('<button type="button" role="tab" class="crm-tab" id="crm-tab-%s" aria-controls="crm-panel-%s" aria-selected="%s"%s>%s</button>'
                   % (k, k, "true" if i == 0 else "false", "" if i == 0 else ' tabindex="-1"', n) for i, (k, n, *_r) in enumerate(inds))
    panels = "".join('<div class="crm-panel" role="tabpanel" id="crm-panel-%s" aria-labelledby="crm-tab-%s"%s><img src="%s" alt="%s" loading="lazy" width="720" height="440">'
                     '<div class="crm-panel-body"><p class="crm-eyebrow mono">HOW THEY USE ODOO CRM</p><h3>%s</h3><ul>%s</ul><div class="crm-mods">%s</div></div></div>'
                     % (k, k, "" if i == 0 else " hidden", img, alt, n, "".join("<li>%s%s</li>" % (TICK, p) for p in pts), "".join("<span>%s</span>" % m for m in mods))
                     for i, (k, n, img, alt, pts, mods) in enumerate(inds))
    out += sec(head("WHO IT'S FOR", "Which Businesses Can Use Odoo CRM?", "Any business that sells through conversations, quotes or follow-ups. Pick an industry to see how it's used.")
               + '<div class="crm-ind"><div class="crm-tabs" role="tablist" aria-label="Industries">%s</div><div class="crm-panels">%s</div></div>'
                 '<p class="crm-more">Don\'t see your industry? <a href="#get-demo">Tell us how your team sells</a> and we\'ll map it to Odoo CRM.</p>' % (tabs, panels),
               "crm-sec--ind")

    # 12 ---- why Unisas: icon cards
    why = [(IC["funnel"], "Built around your sales process", "We map how your team actually sells before configuring anything, so the CRM fits the way you work on day one."),
           (IC["grad"], "Certified Odoo specialists", "Functional consultants and developers who implement Odoo every day, including CRM, Sales and Invoicing together."),
           (IC["people"], "Support after go-live", "We stay on after launch to refine stages, rules and reports as your sales team grows.")]
    # each card opens with a small Odoo-style badge that shows what the card promises
    badges = ['<span class="ox-sbar is-mini"><span class="ox-sb is-done">New</span><span class="ox-sb is-done">Qualified</span><span class="ox-sb is-cur">Won</span></span>',
              '<span class="crm-why-apps">%s</span>' % "".join('<span><i style="--c:%s"></i>%s</span>' % a for a in
                                                               [("#5DC1AA", "CRM"), ("#E4402E", "Sales"), ("#8E4F83", "Invoicing")]),
              '<span class="crm-why-live"><i></i>Hypercare &middot; Active</span>']
    items = "".join('<li><span class="crm-why-top ox-solo" aria-hidden="true">%s</span><h3>%s</h3><p>%s</p></li>'
                    % (badges[i], t, x) for i, (ic, t, x) in enumerate(why))
    out += sec('<div class="crm-why-head">%s<p class="crm-sub">One team that understands both sales processes and Odoo, from the first workshop to long after go-live.</p></div><ol class="crm-why">%s</ol>'
               % (head("WHY UNISAS", "Why Businesses Choose Unisas for Odoo CRM"), items), "crm-sec--why")

    out += SCRIPT + ox.JS
    return out


SCRIPT = '''<script>
(function(){
  /* readiness check */
  var quiz=document.querySelector('.crm-quiz');
  if(quiz){
    var chips=quiz.querySelectorAll('.crm-q-chip'),bar=quiz.querySelector('.crm-q-meter i'),
        num=quiz.querySelector('.crm-q-msg strong'),txt=quiz.querySelector('.crm-q-msg span'),cta=quiz.querySelector('.crm-q-cta');
    var msgs=['Tick the statements that sound like your team.',
              'One sign so far. A simple CRM setup could already help.',
              'A CRM would already save your team time every week.',
              'You are ready for a CRM. Let\\u2019s map your pipeline.'];
    function update(){
      var n=quiz.querySelectorAll('.crm-q-chip[aria-pressed="true"]').length;
      bar.style.setProperty('--p',n/chips.length);
      num.textContent=n+' / '+chips.length;
      txt.textContent=msgs[n===0?0:n===1?1:n<4?2:3];
      cta.hidden=n<2;
    }
    chips.forEach(function(c){c.addEventListener('click',function(){c.setAttribute('aria-pressed',c.getAttribute('aria-pressed')==='true'?'false':'true');update();});});
  }
  /* industry tabs */
  var tabs=[].slice.call(document.querySelectorAll('.crm-tab'));
  function select(t,focus){
    tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;
      document.getElementById(x.getAttribute('aria-controls')).hidden=!on;});
    if(focus)t.focus();
  }
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){select(t);});
    t.addEventListener('keydown',function(e){
      var d={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1}[e.key];
      if(d){e.preventDefault();select(tabs[(i+d+tabs.length)%tabs.length],true);}
    });
  });
  /* rollout phases: the pipeline takes shape */
  var pr=document.querySelector('[data-prbox]');
  if(pr){
    var PH=JSON.parse(document.getElementById('crm-phases').textContent),pb=[].slice.call(pr.querySelectorAll('[data-pr]')),bd=pr.querySelector('[data-prboard]'),cd=pr.querySelector('[data-prcard]');
    var DRAFT=['Enquiry?','Talking','Quote sent','Won'],STG=['New','Qualified','Proposition','Won'],TOT=['&#8377; 6,90,000','&#8377; 18,40,000','&#8377; 8,85,000','&#8377; 9,80,000'];
    var CARDS=[[['Annual support contract','Kaveri Foods','2,10,000','Email','R','#3E7CB1','g'],['CRM for 2 showrooms','Nair Textiles','4,80,000','Website','A','#B5567E','o']],
               [['ERP for 3 branches','Shree Distributors','12,00,000','WhatsApp','M','#4C9F70','r'],['Quote for 40 POS terminals','Bluebay Retail','6,40,000','Website','A','#B5567E','g']],
               [['Clinic group onboarding','Sunrise Clinics','5,25,000','Referral','M','#4C9F70','o'],['Warehouse barcode setup','Arun Logistics','3,60,000','Email','R','#3E7CB1','g']],
               [['Dealer portal','Orbit Motors','9,80,000','Website','R','#3E7CB1','']]];
    var SRC={Website:'blue',Email:'purple',WhatsApp:'green',Referral:'yellow'};
    function board(L){
      var head='<div class="crm-pr-top"><b>'+(L<1?'Pipeline sketch':'Pipeline')+'</b>'+(L>=2?'<span class="ox-team">Sales &middot; Chennai</span>':'')+(L>=5?'<span class="crm-pr-live"><i></i>Live</span>':(L>=2?'<span class="crm-pr-test">Test database</span>':''))+'</div>';
      var cols=STG.map(function(s,i){var cs=L>=3?CARDS[i]:[];
        return '<div class="crm-pr-col'+(L<1?' is-draft':'')+'"><p><b>'+(L<1?DRAFT[i]:s)+'</b>'+(L>=5?'<small>'+TOT[i]+'</small>':(L>=3?'<small>'+cs.length+'</small>':''))+'</p>'+
          (cs.length?cs.map(function(c){return '<div class="crm-pr-card"><b>'+c[0]+'</b><span>&#8377; '+c[2]+'</span><span class="crm-pr-cust">'+c[1]+'</span><span class="crm-pr-foot"><span class="ox-tag ox-tag--'+SRC[c[3]]+'">'+c[3]+'</span>'+
            (L>=4?(c[6]?'<i class="crm-pr-act is-'+c[6]+'"></i>':'')+'<span class="ox-av is-sm" style="--c:'+c[5]+'">'+c[4]+'</span>':'')+'</span></div>';}).join(''):'<div class="crm-pr-empty">'+(L<1?'':'No records yet')+'</div>')+'</div>';}).join('');
      var foot=[];
      if(L>=2)foot.push('Assign by territory','Follow up after 7 days','Quote from template');
      if(L>=3)foot.push('2,340 leads imported','Website &middot; Email &middot; WhatsApp connected');
      if(L>=4)foot.push('8 users trained');
      if(L>=5)foot.push('Won this week &#8377; 9,80,000');
      return head+'<div class="crm-pr-cols">'+cols+'</div>'+(foot.length?'<p class="crm-pr-chips">'+foot.map(function(f){return '<span>'+f+'</span>';}).join('')+'</p>':'<p class="crm-pr-chips is-note">Stages drafted from your workshops. Nothing is built yet.</p>');}
    function draw(i){var p=PH[i];bd.innerHTML=board(i);
      cd.innerHTML='<p class="crm-eyebrow mono">PHASE '+(i+1)+' OF 6 &middot; '+p[1]+'</p><h3>'+p[0]+'</h3><p>'+p[2]+'</p><dl><div><dt>You sign off</dt><dd>'+p[3]+'</dd></div><div><dt>Your team&rsquo;s time</dt><dd>'+p[4]+'</dd></div></dl>'+
        '<div class="crm-pr-nav"><button type="button" class="btn btn-ghost" data-prgo="-1"'+(i?'':' disabled')+'>&larr; Previous</button><button type="button" class="btn btn-ghost" data-prgo="1"'+(i<5?'':' disabled')+'>Next phase &rarr;</button></div>';}
    var cur=0;function go(i){cur=i;pb.forEach(function(b,j){b.classList.toggle('is-on',j===i);b.classList.toggle('is-done',j<i);b.setAttribute('aria-pressed',j===i);});draw(i);}
    pb.forEach(function(b){b.addEventListener('click',function(){go(+b.getAttribute('data-pr'));});});
    cd.addEventListener('click',function(e){var b=e.target.closest('[data-prgo]');if(b)go(Math.max(0,Math.min(5,cur+(+b.getAttribute('data-prgo')))));});
    go(0);
  }
})();
</script>
'''

CTA = ("Let's Map Your Sales Process to Odoo CRM",
       "Tell us how your team sells today. We'll walk through your pipeline, show you how it looks in Odoo CRM, and recommend the right setup and integrations.")
