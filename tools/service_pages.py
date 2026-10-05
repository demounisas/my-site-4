"""
Content for the 8 Odoo service pages (dist/odoo-<service>.html).

Rendered by build_module_pages.py with the same section types as the module
pages. `svc` is the service key used by the homepage tabs and the lead form.
"""

ARROW_R = '<svg width="18" height="12" viewBox="0 0 18 12" fill="none" aria-hidden="true"><path d="M12 1l5 5-5 5M17 6H1" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def row(lead, title, sub, pill, kind="ok"):
    return ('<div class="mk-r">%s<div><strong>%s</strong><small>%s</small></div><em class="mk-pill %s">%s</em></div>'
            % (lead, title, sub, kind, pill))


def sq(text, color):
    return '<span class="mk-sq" style="--c:%s">%s</span>' % (color, text)


def num(n, state=""):
    return '<span class="mk-n mono%s">%s</span>' % (" " + state if state else "", n)


SERVICE_MOCKS = {
    "odoo-consulting": '<div class="mock mk-fit">'
        '<div class="mk-head"><div><span class="mono">FIT-GAP REPORT</span><strong>Distributor · 3 branches</strong></div><em class="mk-pill info">Draft v2</em></div>'
        + row(sq("AC", "#5DC1AA"), "GST invoicing &amp; e-way bills", "Accounting", "Standard")
        + row(sq("SA", "#5DC1AA"), "Dealer-wise pricelists", "Sales", "Standard")
        + row(sq("IN", "#F3B94C"), "Branch-to-branch transfers", "Inventory", "Configure", "wait")
        + row(sq("SC", "#E4402E"), "Scheme &amp; incentive calculation", "Sales", "Custom", "bad")
        + row(sq("TL", "#8E4F83"), "Monthly export for the CA", "Integration", "Connector", "info")
        + '<div class="mk-stack"><i style="--w:70%;--c:#5DC1AA"></i><i style="--w:20%;--c:#F3B94C"></i><i style="--w:10%;--c:#E4402E"></i></div>'
        '<div class="mk-legend mono"><span style="--c:#5DC1AA">70% standard</span><span style="--c:#F3B94C">20% configure</span><span style="--c:#E4402E">10% custom</span></div>'
        '</div>',

    "odoo-implementation": '<div class="mock mk-plan">'
        '<div class="mk-head"><div><span class="mono">GO-LIVE PLAN</span><strong>Week 7 of 10</strong></div><em class="mk-pill ok">On track</em></div>'
        '<div class="mk-progress"><i style="--w:68%"></i></div>'
        + row(num("01", "is-done"), "Discovery &amp; design", "Process maps signed off", "Done")
        + row(num("02", "is-done"), "Configuration", "Sales, Inventory, Accounting", "Done")
        + row(num("03", "is-done"), "Data import", "Masters &amp; opening balances", "Done")
        + row(num("04", "is-now"), "User acceptance testing", "42 of 58 scenarios passed", "In progress", "wait")
        + row(num("05"), "Training", "Role-based sessions", "Week 9", "info")
        + row(num("06"), "Go-live &amp; hypercare", "Cutover weekend", "Week 10", "info")
        + '</div>',

    "odoo-customization": '<div class="mock mk-code">'
        '<div class="mk-code-bar"><i></i><i></i><i></i><span class="mono">dealer_schemes/models/sale_order.py</span></div>'
        '<pre class="mono"><code><span class="k">class</span> <span class="c">SaleOrder</span>(models.Model):\n'
        '    _inherit = <span class="s">"sale.order"</span>\n\n'
        '    scheme_id = fields.Many2one(<span class="s">"dealer.scheme"</span>)\n'
        '    scheme_discount = fields.Monetary(\n'
        '        compute=<span class="s">"_compute_scheme_discount"</span>, store=<span class="k">True</span>)\n\n'
        '    <span class="d">@api.depends</span>(<span class="s">"order_line"</span>, <span class="s">"scheme_id"</span>)\n'
        '    <span class="k">def</span> <span class="c">_compute_scheme_discount</span>(self):\n'
        '        <span class="k">for</span> order <span class="k">in</span> self:\n'
        '            order.scheme_discount = order.scheme_id._apply(order)</code></pre>'
        '<div class="mk-code-foot"><em class="mk-pill ok">Tests passed</em><em class="mk-pill info">No core code changed</em></div>'
        '</div>',

    "odoo-integration": '<div class="mock mk-sync">'
        '<div class="mk-head"><div><span class="mono">CONNECTED SYSTEMS</span><strong>5 integrations live</strong></div><em class="mk-pill ok">All syncing</em></div>'
        + row(sq("RZ", "#4A90E2"), "Razorpay", "Payments → invoices marked paid", "2 min ago")
        + row(sq("WA", "#2E8B67"), "WhatsApp Business", "Order &amp; delivery updates to customers", "Active")
        + row(sq("SR", "#8E4F83"), "Courier API", "Shipping labels &amp; tracking numbers", "Active")
        + row(sq("AM", "#EE8A3C"), "Amazon Seller", "Orders in, stock levels out", "3 queued", "wait")
        + row(sq("TL", "#E4402E"), "Tally", "Daily journal export for the CA", "Tonight 23:00", "info")
        + '</div>',

    "odoo-data-migration": '<div class="mock mk-mig">'
        '<div class="mk-mig-path"><span>Tally ERP 9</span>' + ARROW_R + '<span class="is-to">Odoo</span></div>'
        '<p class="mono mk-title">VALIDATION · TEST MIGRATION #2</p>'
        + row("", "Customers &amp; vendors", '<span class="mono">1,248 of 1,248 records</span>', "Matched")
        + row("", "Products &amp; variants", '<span class="mono">3,412 of 3,412 records</span>', "Matched")
        + row("", "Opening stock value", '<span class="mono">₹ 42.6L = ₹ 42.6L</span>', "Reconciled")
        + row("", "Open invoices &amp; bills", '<span class="mono">386 of 386 documents</span>', "Matched")
        + row("", "Trial balance", '<span class="mono">Ledger totals by account</span>', "CA review", "wait")
        + '</div>',

    "odoo-support": '<div class="mock mk-desk">'
        '<div class="mk-head"><div><span class="mono">SUPPORT DESK</span><strong>September</strong></div><em class="mk-pill ok">Within plan hours</em></div>'
        '<div class="mk-hr-grid"><div><span class="mono">CLOSED</span><strong>14</strong></div><div><span class="mono">OPEN</span><strong>2</strong></div><div><span class="mono">HOURS USED</span><strong>11<small> / 16</small></strong></div></div>'
        + row(num("P1"), "GST report mismatch for September", "#1182 · Accounting", "In progress", "wait")
        + row(num("P3"), "Add approval step on purchase orders", "#1179 · Enhancement", "Scheduled", "info")
        + row(num("P2", "is-done"), "Stock report loading slowly", "#1175 · Performance", "Resolved")
        + row(num("—", "is-done"), "Weekly backup restore test", "Proactive check", "Passed")
        + '</div>',

    "odoo-training": '<div class="mock mk-train">'
        '<div class="mk-head"><div><span class="mono">GO-LIVE READINESS</span><strong>Training by team</strong></div><em class="mk-pill wait">Week 9</em></div>'
        '<div class="mk-bar"><span>Sales</span><i style="--w:100%;--c:#5DC1AA"></i><b class="mono">100%</b></div>'
        '<div class="mk-bar"><span>Warehouse</span><i style="--w:85%;--c:#5DC1AA"></i><b class="mono">85%</b></div>'
        '<div class="mk-bar"><span>Accounts</span><i style="--w:70%;--c:#F3B94C"></i><b class="mono">70%</b></div>'
        '<div class="mk-bar"><span>Managers</span><i style="--w:55%;--c:#EE8A3C"></i><b class="mono">55%</b></div>'
        + row(sq("TH", "#1E3A5F"), "Next: barcode receiving", "Warehouse · Thu 10:30 · on-site", "Booked", "info")
        + row(sq("▶", "#8E4F83"), "Recorded sessions", "12 videos in your library", "Available")
        + '</div>',

    "odoo-ai-automation": '<div class="mock mk-auto">'
        '<div class="mk-head"><div><span class="mono">AUTOMATION RUN</span><strong>Vendor bill intake</strong></div><em class="mk-pill ok">Done in 38 s</em></div>'
        '<ol class="mk-log">'
        '<li><span class="mono">10:02:14</span><div><strong>Bill PDF received by email</strong><small>Sri Lakshmi Metals · bill-0931.pdf</small></div></li>'
        '<li><span class="mono">10:02:21</span><div><strong>Details read from the PDF</strong><small>Vendor, GSTIN, date, ₹ 48,380 incl. GST</small></div></li>'
        '<li><span class="mono">10:02:24</span><div><strong>Matched to PO &amp; receipt</strong><small>P00217 · quantities agree</small></div></li>'
        '<li><span class="mono">10:02:31</span><div><strong>Draft bill created</strong><small>Posted to Accounting for approval</small></div></li>'
        '<li class="is-last"><span class="mono">10:02:52</span><div><strong>Approver notified on WhatsApp</strong><small>One tap to approve</small></div></li>'
        '</ol></div>',
}


SERVICES = [
    dict(slug="odoo-consulting", svc="consulting", name="Odoo Consulting", short="Fit-GAP, roadmap & budget",
         title="Odoo Consulting Services | Unisas",
         meta="Odoo consulting from Unisas: process audits, Fit-GAP analysis, edition and hosting advice, and a phased roadmap with a realistic budget before you commit.",
         hero=dict(style="split", eyebrow="ODOO CONSULTING", title="Know exactly what Odoo will do for you before anything is configured",
                   lead="We study how your teams work today, check it against standard Odoo, and hand you a phased plan with scope, budget and timeline you can take to your board.",
                   points=["Process audit & workshops", "Fit-GAP against standard Odoo", "Phased roadmap & estimate"],
                   cta="Discuss Odoo Consulting", cta2="See how it works", cta2_href="approach"),
         sections=[
             ("steps_h", dict(eyebrow="OUR APPROACH", title="From how you work today to a plan you can act on", extra=' id="approach"', items=[
                 ("Discover", "Workshops with each team to understand today's processes and pain points."),
                 ("Map", "Current processes documented, including the workarounds and spreadsheets."),
                 ("Fit-GAP", "Each requirement marked standard, configuration, custom or integration."),
                 ("Recommend", "Modules, edition and hosting chosen for your size and budget."),
                 ("Roadmap", "Phases, effort estimate and timeline agreed with you.")])),
             ("features", dict(eyebrow="WHAT WE ASSESS", title="The questions a good Odoo plan has to answer", alt=True, items=[
                 ("Processes", "Order-to-cash, procure-to-pay, production, HR and reporting, as they really run today."),
                 ("Modules", "Which Odoo apps you need now and which can wait for a later phase."),
                 ("Community vs Enterprise", "Which edition fits, based on the features you actually need and your user count."),
                 ("Hosting", "Odoo Online, Odoo.sh or on-premise, weighed against customisation and IT needs."),
                 ("Data", "What has to move from Tally, Excel or your current ERP, and how clean it is."),
                 ("Integrations", "Payment gateways, WhatsApp, couriers, marketplaces and in-house tools that must connect.")])),
             ("checklist", dict(eyebrow="WHAT YOU WALK AWAY WITH", title="Deliverables you keep, whoever implements", sub="The consulting output is yours. Use it with us or take it to any Odoo partner.", items=[
                 "Current-process maps for each team", "Fit-GAP report, requirement by requirement", "Module & edition recommendation",
                 "Hosting & licence advice", "Data migration & integration assessment", "Phased roadmap with effort estimate"])),
         ],
         related=["odoo-implementation", "odoo-customization", "odoo-data-migration"],
         faq=[("Why pay for consulting before implementation?", "A Fit-GAP study shows what standard Odoo already covers and what needs building, so you avoid surprise costs and scope changes mid-project."),
              ("How long does Odoo consulting take?", "For most small and mid-sized businesses the workshops and report take one to three weeks, depending on the number of teams and locations."),
              ("Do we have to implement with Unisas afterwards?", "No. The roadmap and Fit-GAP report are yours to keep and use with any partner, though most clients continue with us.")]),

    dict(slug="odoo-implementation", svc="implementation", name="Odoo Implementation", short="Setup, configuration & go-live",
         title="Odoo Implementation Services | Unisas",
         meta="End-to-end Odoo implementation by Unisas: configuration, data import, user roles, testing, training and go-live. Most SME projects go live in 6 to 12 weeks.",
         hero=dict(style="center", eyebrow="ODOO IMPLEMENTATION", title="Odoo set up the way your business actually runs",
                   lead="We handle the whole rollout: configuration, data import, user roles, testing, training and go-live. Your team starts on a system that already reflects how you work.",
                   points=["Certified Odoo consultants", "One team from scoping to support", "6–12 weeks for most SMEs"],
                   cta="Discuss Odoo Implementation", cta2="See the phases", cta2_href="phases"),
         sections=[
             ("stats", dict(items=[("6–12 wks", "typical go-live for SMEs"), ("1 team", "from scoping to support"), ("UAT", "signed off before go-live"), ("Hypercare", "support after launch")])),
             ("steps_v", dict(eyebrow="PROJECT PHASES", title="Six phases, one accountable team", extra=' id="phases"',
                              sub="Each phase ends with a sign-off, so you always know what has been delivered and what comes next.", items=[
                 ("01", "Discovery & design", "We confirm requirements, map processes and agree the solution design with each team lead."),
                 ("02", "Configuration", "Company, taxes, products, workflows, approvals and documents configured in a test database."),
                 ("03", "Data import", "Customers, vendors, products, opening stock and balances cleaned and imported."),
                 ("04", "Testing (UAT)", "Your team runs real scenarios end to end; we fix issues until every scenario passes."),
                 ("05", "Training", "Role-based sessions on your own configured database, not a generic demo."),
                 ("06", "Go-live & hypercare", "Planned cutover, then close support in the first weeks while the team settles in.")])),
             ("bento", dict(eyebrow="WHAT WE CONFIGURE", title="Everything needed to run the business on day one", alt=True, wide=(0, 3), items=[
                 ("Company & finance foundations", "Companies, branches, fiscal year, chart of accounts, GST taxes and currencies set up with your accountant."),
                 ("Modules & workflows", "Sales, purchase, inventory, manufacturing, HR and more, configured to your process."),
                 ("Roles & access", "User groups, record rules and approval limits per role."),
                 ("Documents & reports", "Quotations, invoices, delivery slips and management reports in your branding, plus dashboards each manager actually uses.")])),
         ],
         related=["odoo-consulting", "odoo-data-migration", "odoo-training"],
         faq=[("How long does an Odoo implementation take?", "Most small and mid-sized projects go live in 6 to 12 weeks. Larger rollouts with many modules, branches or custom development are usually split into phases."),
              ("Do you implement Odoo Community and Enterprise?", "Yes. We implement both editions and on Odoo Online, Odoo.sh or your own servers, and recommend the right fit during scoping."),
              ("What happens after go-live?", "We provide hypercare support in the first weeks after launch, then you can move to a monthly support plan or on-demand hours.")]),

    dict(slug="odoo-customization", svc="customization", name="Customization & Development", short="Custom modules & reports",
         title="Odoo Customization & Development Services | Unisas",
         meta="Odoo customization and development by Unisas: upgrade-safe custom modules, reports, automations, dashboards and website themes built to Odoo standards.",
         hero=dict(style="dark", eyebrow="ODOO CUSTOMIZATION & DEVELOPMENT", title="Custom modules that fit your workflow and survive upgrades",
                   lead="When standard Odoo doesn't cover a process, we extend it with clean modules built on Odoo's own framework, never by patching core code.",
                   points=["Custom modules & fields", "Reports & documents", "Upgrade-safe code"],
                   cta="Discuss Odoo Customization", cta2="What we build", cta2_href="build"),
         sections=[
             ("zigzag", dict(eyebrow="WHAT WE BUILD", title="Custom work, only where it pays off", extra=' id="build"',
                             sub="We check standard Odoo and Studio first, and write code only when configuration can't do the job.", items=[
                 ("MODULES", "Custom modules for processes Odoo doesn't cover", "New models, fields, screens and business rules packaged as a separate module, so your core Odoo stays untouched.",
                  ["New models, fields & views", "Business rules & validations", "Extensions to existing apps"]),
                 ("DOCUMENTS", "Reports and documents in your format", "Invoices, quotations, delivery challans and management reports designed to match your brand and compliance needs.",
                  ["QWeb PDF reports", "Branded document templates", "Excel exports & custom reports"]),
                 ("AUTOMATION", "Workflows, approvals and dashboards", "Multi-level approvals, scheduled jobs and KPI dashboards that turn Odoo into the system your managers check first.",
                  ["Approval workflows", "Scheduled actions", "Custom dashboards & KPIs"])])),
             ("compare", dict(eyebrow="HOW WE BUILD", title="Why upgrade-safe development matters", alt=True, before="Quick fixes & core edits", after="Unisas custom modules", items=[
                 ("Where the code lives", "Changes made inside Odoo's core files", "A separate module you can switch on or off"),
                 ("Upgrades", "Changes lost or broken at the next version", "Ported and tested with each upgrade"),
                 ("Quality", "No review, no tests", "Code review and automated tests"),
                 ("Ownership", "Only the original developer understands it", "Documented and handed over to you")])),
             ("checklist", dict(eyebrow="OUR STANDARDS", title="Code your next partner will thank you for", items=[
                 "Built to Odoo development guidelines", "Version-controlled in Git", "Code review before every release",
                 "Automated tests for business logic", "Tested on staging before production", "Technical documentation included"])),
         ],
         related=["odoo-integration", "odoo-consulting", "odoo-support"],
         faq=[("Will customizations break when we upgrade Odoo?", "Custom modules need porting to each new version, but because we never edit core code the work is predictable, and we include it in every upgrade plan."),
              ("Can Odoo Studio do this instead of code?", "Often, yes. For fields, simple screens and basic automations we use Studio first, and write code only when Studio can't deliver it cleanly."),
              ("Who owns the custom code?", "You do. Source code for modules built for you is handed over and can be maintained by your own team or any partner.")]),

    dict(slug="odoo-integration", svc="integration", name="Third-Party Integrations", short="Payments, WhatsApp, Tally, couriers",
         title="Odoo Integration Services | Unisas",
         meta="Odoo integration services by Unisas: connect Odoo to payment gateways, WhatsApp, Tally, courier APIs, marketplaces, banks and in-house software via APIs.",
         hero=dict(style="reverse", eyebrow="ODOO INTEGRATION", title="Connect Odoo to every system your business depends on",
                   lead="We link Odoo to payment gateways, WhatsApp, Tally, courier APIs, marketplaces, banks and your own software, so data moves both ways without anyone re-typing it.",
                   points=["Two-way sync", "Real-time or scheduled", "Error alerts & logs"],
                   cta="Discuss Odoo Integration", cta2="See what we connect", cta2_href="hub"),
         sections=[
             ("hub", dict(eyebrow="WHAT WE CONNECT", title="Odoo at the centre, everything else plugged in", extra=' id="hub"', core="Your Odoo database",
                          sub="Each connection writes into the same records your team already uses, so there is one version of the truth.", items=[
                 ("Payment gateways", "Razorpay, PayU, Stripe"), ("WhatsApp", "order & payment updates"), ("Tally", "exports for your CA"),
                 ("Couriers", "labels & tracking"), ("Marketplaces", "Amazon, Shopify, WooCommerce"), ("Banks & BI", "statements, Power BI")])),
             ("features", dict(eyebrow="HOW WE CONNECT", title="Integrations built to keep running", alt=True, items=[
                 ("Proven connectors", "Where a reliable connector exists, we use and configure it rather than reinventing it."),
                 ("Custom APIs", "REST and XML-RPC integrations for in-house or niche systems."),
                 ("Webhooks & real-time sync", "Events such as a payment or shipment update Odoo within seconds."),
                 ("Scheduled sync", "Batch jobs for systems that only exchange data daily or hourly."),
                 ("Error handling", "Failed syncs are logged, retried and flagged to the right person."),
                 ("Security", "API keys, limited-access users and encrypted connections.")])),
             ("steps_h", dict(eyebrow="OUR PROCESS", title="From two systems to one flow of data", items=[
                 ("Scope", "Which data moves, in which direction and how often."),
                 ("Map", "Fields matched between both systems, including edge cases."),
                 ("Build", "Connector configured or custom integration developed."),
                 ("Test", "Real transactions run end to end on staging."),
                 ("Monitor", "Logs and alerts set up after go-live.")])),
         ],
         related=["odoo-customization", "odoo-ai-automation", "odoo-data-migration"],
         faq=[("Can Odoo integrate with Tally?", "Yes. Many businesses keep Tally for their CA while running operations in Odoo. We set up scheduled exports or a connector so vouchers reach Tally without re-entry."),
              ("Which payment gateways work with Odoo?", "Odoo supports providers such as Razorpay, PayU and Stripe. Payments are recorded against invoices in Accounting automatically."),
              ("What if our software has no ready connector?", "If the system has an API, we build a custom integration using Odoo's REST or XML-RPC interfaces. If not, we can use scheduled file exchange.")]),

    dict(slug="odoo-data-migration", svc="migration", name="Data Migration", short="Tally, Excel & legacy ERP to Odoo",
         title="Odoo Data Migration & Upgrade Services | Unisas",
         meta="Odoo data migration by Unisas: move data from Tally, Excel, QuickBooks, SAP or another ERP into Odoo, or upgrade older Odoo versions, with full validation.",
         hero=dict(style="split", eyebrow="ODOO DATA MIGRATION", title="Move your data into Odoo safely, with every number checked",
                   lead="Whether you're leaving Tally, Excel, QuickBooks or another ERP, or upgrading an older Odoo database, we migrate, validate and reconcile your data before you switch over.",
                   points=["Test migration first", "Totals reconciled with you", "Minimal downtime at cutover"],
                   cta="Discuss Data Migration", cta2="See our method", cta2_href="method"),
         sections=[
             ("steps_v", dict(eyebrow="OUR METHOD", title="Test first, then cut over", extra=' id="method"',
                              sub="Your data is migrated at least once into a test database and checked by your team before the real switch.", items=[
                 ("01", "Extract", "Data exported from your current system, including history you want to keep."),
                 ("02", "Clean", "Duplicates merged, missing fields filled and inactive records archived."),
                 ("03", "Map", "Old fields and codes matched to Odoo's structure."),
                 ("04", "Test migration", "Data loaded into a test database so your team can check it."),
                 ("05", "Validate", "Record counts, stock values and ledger totals reconciled with you and your CA."),
                 ("06", "Cutover", "Final migration over a planned window, then go-live.")])),
             ("accordion", dict(eyebrow="WHERE WE MIGRATE FROM", title="Systems we move data out of", alt=True, items=[
                 ("Tally", "Ledgers, opening balances, stock items, parties and open vouchers, reconciled against your Tally trial balance."),
                 ("Excel & Google Sheets", "Customer, product and stock lists cleaned and structured so they import correctly."),
                 ("QuickBooks, Zoho & other accounting tools", "Contacts, items, open invoices and bills, and account balances."),
                 ("SAP & legacy ERPs", "Master data and open transactions extracted and mapped to Odoo's data model."),
                 ("Older Odoo versions", "Database upgrades to the latest version, with custom modules ported and tested."),
                 ("Community to Enterprise, or a hosting move", "Moves between editions and between Odoo Online, Odoo.sh and on-premise.")])),
             ("compare", dict(eyebrow="WHY IT MATTERS", title="Migration done properly vs. copy-paste", before="Manual re-entry", after="Unisas migration", items=[
                 ("Accuracy", "Typos and missing records", "Automated import, validated counts"),
                 ("Opening balances", "Don't match the old system", "Reconciled with your accountant"),
                 ("History", "Left behind in the old system", "Kept where it's useful"),
                 ("Downtime", "Days of double entry", "Short, planned cutover window")])),
         ],
         related=["odoo-implementation", "odoo-integration", "odoo-consulting"],
         faq=[("Can you migrate from Tally to Odoo?", "Yes. We migrate ledgers, parties, stock items, opening balances and open invoices from Tally, and reconcile the totals with your accountant before cutover."),
              ("How much historical data should we bring over?", "Usually masters, open transactions and opening balances, plus one or two years of history if you need it for reporting. We help you decide during scoping."),
              ("Will our business stop during migration?", "No. The test migrations run while you keep working in your old system. Only the final cutover needs a short, planned window, often over a weekend.")]),

    dict(slug="odoo-support", svc="support", name="Support & Maintenance", short="AMC & support plans after go-live",
         title="Odoo Support & Maintenance (AMC) | Unisas",
         meta="Odoo support and maintenance plans from Unisas: helpdesk, bug fixes, performance tuning, backups, security updates and upgrade planning after go-live.",
         hero=dict(style="dark-center", eyebrow="ODOO SUPPORT & MAINTENANCE", title="Keep Odoo fast, stable and improving after go-live",
                   lead="Once you're live, we stay on as your Odoo team: fixing issues, tuning performance, rolling out enhancements and planning upgrades so the system keeps up with the business.",
                   points=["Functional & technical helpdesk", "Monthly retainers or on-demand hours", "Proactive monitoring"],
                   cta="Discuss a Support Plan", cta2="What's covered", cta2_href="covered"),
         sections=[
             ("bento", dict(eyebrow="WHAT'S COVERED", title="One team that already knows your system", extra=' id="covered"', wide=(0, 4), items=[
                 ("Functional & technical helpdesk", "Users raise a ticket for anything from 'how do I…' questions to errors, and a consultant who knows your setup picks it up."),
                 ("Bug fixes", "Issues in configuration or custom modules diagnosed and fixed."),
                 ("Performance tuning", "Slow screens and reports investigated and sped up."),
                 ("Small enhancements", "New fields, reports and workflow tweaks as you grow."),
                 ("Upgrade planning", "We plan version upgrades, port custom modules and test them before you move, so upgrades are a project, not a surprise.")])),
             ("steps_h", dict(eyebrow="HOW A REQUEST IS HANDLED", title="From ticket to fix", alt=True, items=[
                 ("Raise", "By email, portal or WhatsApp, with screenshots."),
                 ("Triage", "Priority set by business impact."),
                 ("Fix", "Resolved on staging first where needed."),
                 ("Verify", "You confirm the fix works."),
                 ("Report", "Monthly summary of tickets and hours.")])),
             ("checklist", dict(eyebrow="PROACTIVE CARE", title="Problems caught before users notice", sub="Plans include regular checks, not just reactive fixes.", items=[
                 "Server & uptime monitoring", "Backups with restore tests", "Security & Odoo updates applied",
                 "Performance reviews", "Monthly usage & ticket report", "Upgrade roadmap reviews"])),
         ],
         related=["odoo-training", "odoo-customization", "odoo-implementation"],
         faq=[("Do you support Odoo systems implemented by another partner?", "Yes. We start with a short health check of your configuration and custom code, then take over support."),
              ("What support plans do you offer?", "Monthly retainers with a block of pre-booked hours, or on-demand hours for occasional help. Response times and priorities are agreed in your plan."),
              ("Are upgrades included in support?", "Upgrade planning is included. The upgrade itself is scoped separately because it depends on your version and custom modules.")]),

    dict(slug="odoo-training", svc="training", name="Training & Onboarding", short="Role-based training on your system",
         title="Odoo Training & Onboarding | Unisas",
         meta="Odoo training from Unisas: role-based sessions on your own configured database, admin training, user manuals, videos and train-the-trainer programmes.",
         hero=dict(style="reverse", eyebrow="ODOO TRAINING & ONBOARDING", title="Get every team confident in Odoo from day one",
                   lead="Role-based training delivered on your own configured database, not generic demos, so people learn the exact screens they'll use and adoption sticks after go-live.",
                   points=["Training on your own data", "Onsite, remote or recorded", "Manuals & videos you keep"],
                   cta="Discuss Odoo Training", cta2="See the programme", cta2_href="programme"),
         sections=[
             ("features", dict(eyebrow="WHO WE TRAIN", title="Different roles, different sessions", cols=4, items=[
                 ("End users", "The daily tasks for their role, step by step."),
                 ("Managers", "Approvals, dashboards and reports to run their team."),
                 ("Administrators", "Users, access rights, settings and basic troubleshooting."),
                 ("Internal trainers", "Train-the-trainer, so new hires learn in-house.")])),
             ("zigzag", dict(eyebrow="THE PROGRAMME", title="Training timed around your go-live", alt=True, extra=' id="programme"', items=[
                 ("BEFORE GO-LIVE", "Learn on a copy of your real system", "Hands-on sessions on your configured test database, using your own products, customers and workflows.",
                  ["Role-based sessions", "Practice scenarios per team", "Readiness check before cutover"]),
                 ("AT GO-LIVE", "Help on the floor when it counts", "Consultants available onsite or on call during the first days, so small questions don't become bottlenecks.",
                  ["Floor-walking support", "Quick-reference guides", "Daily check-ins with team leads"]),
                 ("AFTER GO-LIVE", "Keep skills growing", "Refresher and advanced sessions as teams settle in, plus onboarding for new hires.",
                  ["Refresher sessions", "Advanced features & reports", "New-joiner onboarding"])])),
             ("checklist", dict(eyebrow="MATERIALS YOU KEEP", title="Knowledge that stays in the company", items=[
                 "User manuals for your configuration", "Short screen-recorded videos", "Quick-reference cards per role",
                 "Admin & settings guide", "Session recordings", "FAQ from your own training sessions"])),
         ],
         related=["odoo-implementation", "odoo-support", "odoo-consulting"],
         faq=[("Is training included in an Odoo implementation?", "Yes. Role-based end-user training is part of every implementation. Extra sessions, advanced topics and train-the-trainer programmes can be added."),
              ("Can you train our team if someone else implemented Odoo?", "Yes. We review your configuration first so the training matches the system your team actually uses."),
              ("Do you offer training in regional languages?", "Tell us your team's preferred language when you enquire and we'll confirm what we can offer for your sessions.")]),

    dict(slug="odoo-ai-automation", svc="automation", name="AI & Automation", short="Automated workflows & AI capture",
         title="Odoo AI & Automation Services | Unisas",
         meta="Odoo AI and automation by Unisas: automated workflows, n8n and webhook automations, AI document capture, WhatsApp follow-ups and smart alerts.",
         hero=dict(style="center", eyebrow="ODOO AI & AUTOMATION", title="Put automation to work inside Odoo, and AI where it clearly saves time",
                   lead="We remove repetitive manual work by automating workflows across Odoo and the tools around it, and add AI for tasks like reading documents where it earns its place.",
                   points=["Automated actions & schedules", "AI document capture", "WhatsApp & email follow-ups"],
                   cta="Discuss AI & Automation", cta2="See an example", cta2_href="example"),
         sections=[
             ("flow", dict(eyebrow="EXAMPLE", title="A vendor bill that enters itself", extra=' id="example"',
                           sub="What used to take a clerk several minutes per bill runs automatically, with a person approving the result.", items=[
                 ("trigger", "Vendor emails a bill PDF"), ("action", "AI reads vendor, GSTIN and amounts"), ("if", "Matches a PO and receipt?"),
                 ("action", "Draft bill created in Accounting"), ("email", "Approver notified to review")])),
             ("features", dict(eyebrow="WHAT WE AUTOMATE", title="Repetitive work, handed to the system", alt=True, items=[
                 ("Automated actions", "Rules that update records, assign work or send messages when something changes."),
                 ("Scheduled jobs", "Daily reminders, overdue follow-ups and recurring documents created on time."),
                 ("n8n & webhooks", "Workflows that connect Odoo with the other apps your team uses."),
                 ("Document capture", "Bills and receipts read from PDFs and photos into draft entries."),
                 ("WhatsApp & email follow-ups", "Payment reminders, order updates and lead nurturing without manual messages."),
                 ("Smart alerts & reports", "Managers told about exceptions, like low margin or late deliveries, as they happen.")])),
             ("compare", dict(eyebrow="BEFORE & AFTER", title="Where the time goes back", before="Manual process", after="Automated with Unisas", items=[
                 ("Vendor bills", "Typed in from PDFs", "Captured automatically, approved by a person"),
                 ("Payment follow-ups", "Someone remembers to call", "Scheduled reminders on WhatsApp & email"),
                 ("New leads", "Assigned when someone checks the inbox", "Routed instantly to the right salesperson"),
                 ("Exceptions", "Found in month-end reports", "Alerted the day they happen")])),
         ],
         related=["odoo-integration", "odoo-customization", "odoo-support"],
         faq=[("Is AI necessary to automate Odoo?", "No. Most time savings come from ordinary automation rules and scheduled jobs. We use AI only for tasks like reading documents, where rules alone can't do the job."),
              ("What is n8n and why use it with Odoo?", "n8n is a workflow automation tool that connects Odoo to other apps through their APIs. It's useful for automations that span several systems."),
              ("Will automation replace human approval?", "Not unless you want it to. We usually keep a person approving key steps such as bills and payments, with the data entry done for them.")]),
]
