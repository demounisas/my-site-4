"""
Content for the company pages: dist/about.html and dist/contact.html.

Rendered by build_module_pages.py with the same section types as the module
and service pages. `nav` is the header link that gets highlighted.

CONTACT_DETAILS: fill in the real values and re-run the build; only the
filled-in ones are shown on the contact page, beside the form.
"""

CONTACT_DETAILS = dict(
    company="Unisas ITBusiness Solutions Private Limited",
    email="avinash@unisasitbiz.com",
    phone="044-46042744",
    phone_href="+914446042744",
    whatsapp="",  # digits with country code, e.g. "919876543210"
    address="7/61, First Floor, Mookambika Complex,<br>New no.7, Old no.4, Sir Desika Road,<br>Mylapore, Chennai - 600004",
    hours="Monday to Saturday, 9:30 AM – 6:30 PM IST",
)

ICON_ABOUT = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="9" cy="8" r="3.2" stroke="currentColor" stroke-width="1.6"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="17" cy="9" r="2.4" stroke="currentColor" stroke-width="1.6"/><path d="M16.5 14.2c2.6.3 4.5 2.6 4.5 5.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
ICON_CONTACT = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5h16a1 1 0 011 1v10a1 1 0 01-1 1H9l-5 4V6a1 1 0 011-1z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M8 10h8M8 13h5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'


def contact_cards():
    d = CONTACT_DETAILS
    wa = "".join(c for c in d["whatsapp"] if c.isdigit())
    cards = [
        ("Address", d["address"], ""),
        ("Phone", d["phone"], "tel:" + d["phone_href"]),
        ("Email", d["email"], "mailto:" + d["email"]),
        ("WhatsApp", "Chat with us", "https://wa.me/" + wa) if wa else ("WhatsApp", "", ""),
        ("Business hours", d["hours"], ""),
    ]
    return [(label, ('<a href="%s">%s</a>' % (href, value)) if href else value) for label, value, href in cards if value]


COMPANY_MOCKS = {}


COMPANY = [
    dict(slug="about", nav="About", name="About Unisas", short="Who we are and how we work", icon_svg=ICON_ABOUT,
         title="About Unisas | ERP Consulting, Implementation &amp; Integration",
         meta="Unisas ITBusiness Solutions Private Limited delivers ERP-integrated SaaS applications on cloud or on-premise, with consulting, implementation, integration and ongoing support backed by 75+ years of combined experience.",
         hero=dict(style="center", plain=True, eyebrow="ABOUT UNISAS", title="Technology that fits your business, not the other way around.",
                   lead="Unisas ITBusiness Solutions Private Limited is a software services company built on a simple belief: technology should serve business goals, not complicate them.",
                   points=["75+ years of combined ERP experience", "Cloud or on-premise", "Greenfield &amp; brownfield projects"],
                   cta="Talk to Our Team", cta2="What we do", cta2_href="what-we-do"),
         sections=[
             ("stats", dict(items=[("75+ years", "combined ERP industry experience"), ("1 platform", "to run your entire business"),
                                   ("Flexible", "cloud or on-premise deployment"), ("Every size", "of business, new or existing ERP")])),
             ("story", dict(eyebrow="WHO WE ARE", title="Who We Are", lead="Technology should serve business goals, not complicate them.", items=[
                 "Unisas ITBusiness Solutions Private Limited is a software services company built on that simple belief. We're a young company, but our team brings over <strong>75 years of combined industry experience</strong> in ERP implementation, integration and consulting.",
                 "We work with businesses of every size to turn complex processes into clear, connected systems that deliver measurable results."])),
             ("bento", dict(eyebrow="WHAT WE DO", title="What We Do", alt=True, extra=' id="what-we-do"', wide=(0, 3), items=[
                 ("One platform, on the cloud or on-premise", "Unisas delivers a complete suite of ERP-integrated SaaS applications, available on the cloud or on-premise, designed to run your entire business from a single platform."),
                 ("Greenfield", "Implementing your first ERP system? We set it up around how your business actually works."),
                 ("Brownfield", "Modernising an existing ERP? We build on the systems and data you already have."),
                 ("Your transformation can start immediately", "No matter how complex your business or technology landscape, we meet you where you are and get moving from day one.")])),
             ("steps_h", dict(eyebrow="FULL LIFECYCLE", title="Our services cover the full lifecycle", items=[
                 ("Consulting", "Understanding your processes before recommending a solution."),
                 ("Implementation", "Deploying ERP systems tailored to how you actually operate."),
                 ("Integration", "Connecting your existing tools into one reliable source of truth."),
                 ("Ongoing support", "Helping your system scale as your business grows.")])),
             ("checklist", dict(eyebrow="WHY ERP MATTERS", title="Why ERP Matters", alt=True,
                                sub="In a fast-moving market, keeping up isn't enough. Efficiency, accuracy and adaptability decide who stays ahead. A well-implemented ERP system gives you:", items=[
                 "<strong>One integrated system</strong>Every part of your value chain connected, with no duplicated effort.",
                 "<strong>Reliable data</strong>Centralised information that reduces errors and supports confident decisions.",
                 "<strong>Real-time visibility</strong>Live insight into performance so you can respond faster.",
                 "<strong>Better collaboration</strong>Every department working from the same information.",
                 "<strong>Lower costs</strong>Fewer manual tasks and leaner processes over time.",
                 "<strong>Room to grow</strong>A system that scales and adapts as your business expands.",
                 "<strong>Built-in compliance</strong>Automated processes and audit trails that support regulatory requirements.",
                 "<strong>Happier customers</strong>Faster response times and smoother order fulfilment.",
                 "<strong>A fit for your business</strong>Configurable to your specific workflows.",
                 "<strong>Stronger security</strong>Centralised data with controlled access."])),
             ("mission", dict(eyebrow="PURPOSE", title="Our Mission &amp; Vision", items=[
                 ("Our Mission", "To achieve customer delight through innovative, cost-effective and value-added consulting, implementation and integration of software services, and to maximise value, growth and satisfaction for our clients while upholding the highest standards of business ethics."),
                 ("Our Vision", "To be a leader in innovative software services, bridging the gap between technology and business needs with agile, customised solutions that accelerate our clients' growth in a rapidly evolving digital landscape.")])),
             ("features", dict(eyebrow="WHAT GUIDES US", title="Our Values", cols=4, alt=True, items=[
                 ("Integrity", "We do what we say, and we say it honestly."),
                 ("Innovation", "We look for better ways, not just familiar ones."),
                 ("Accountability", "We own our outcomes and our clients' results."),
                 ("Sustainability", "We build solutions and relationships that last.")])),
         ],
         cta=("Let's Build What's Next", "Whether you're starting fresh or upgrading what you have, Unisas is your partner in turning business goals into working systems.")),

    dict(slug="contact", nav="Contact", name="Contact", short="Talk to our team", icon_svg=ICON_CONTACT, form_first=True,
         title="Contact Unisas | Talk to Our ERP Team",
         meta="Contact Unisas ITBusiness Solutions in Mylapore, Chennai. Call 044-46042744 or send us your requirement and our team will respond within one business day.",
         hero=dict(style="simple", eyebrow="CONTACT US", title="Let's talk about your business, not just your software.",
                   lead="Whether you're planning your first ERP rollout, upgrading an existing system, or just exploring what's possible, our team is ready to help. Tell us where you are today, and we'll show you a practical path forward."),
         # the form section: contact details and next steps on the left, the form on the right
         contact=dict(
             eyebrow="GET IN TOUCH", title="Get in Touch",
             form_title="Send Us a Message",
             form_intro="Fill in the form below and a member of our team will respond within one business day.",
             button="Request a Consultation",
             industries=["Manufacturing", "FMCG", "Healthcare", "BFSI", "Logistics", "Education", "Other"],
             sizes=["1–50", "51–200", "201–1000", "1000+"],
             interests=[("implementation", "New ERP Implementation"), ("upgrade", "Upgrading an Existing System"),
                        ("integration", "System Integration"), ("consulting", "Consulting"), ("other", "Other")],
             steps=[("We review your requirement.", "Our team studies what you've shared before reaching out."),
                    ("Discovery call.", "A short conversation to understand your processes, challenges and goals."),
                    ("Tailored proposal.", "A clear recommendation with scope, timeline and cost, with no generic packages.")]),
         sections=[
             ("industries", dict(eyebrow="INDUSTRIES", title="Industries We Serve",
                                 note="Don't see your industry? <a href='#get-demo' data-no-modal>Get in touch anyway.</a> Our ERP solutions adapt to the way your business works.", items=[
                 ("Manufacturing", "Bills of materials, work orders, quality checks, and shop-floor planning in Odoo MRP.", ["MRP", "Quality", "PLM"]),
                 ("Retail &amp; Distribution", "Point of sale, multi-warehouse stock, purchasing, and replenishment in one flow.", ["POS", "Inventory", "Purchase"]),
                 ("eCommerce", "Online stores and marketplaces synced with inventory, orders, and accounting.", ["Website", "eCommerce", "Sales"]),
                 ("Logistics &amp; Wholesale", "Warehouse routes, barcode operations, and delivery tracking at scale.", ["Inventory", "Barcode", "Fleet"]),
                 ("Professional Services", "Projects, timesheets, and invoicing connected for accurate, on-time billing.", ["Project", "Timesheets", "Invoicing"]),
                 ("Trading &amp; Import/Export", "Multi-currency, landed costs, and supplier management across borders.", ["Accounting", "Purchase", "Inventory"]),
                 ("Healthcare &amp; Clinics", "Appointments, patient records, pharmacy stock, and billing on one platform.", ["Appointments", "Inventory", "Accounting"]),
                 ("Education &amp; Training", "Admissions, fee collection, courses, and staff management in one system.", ["eLearning", "Events", "Accounting"]),
                 ("Construction &amp; Real Estate", "Project costing, subcontractors, site materials, and property rentals.", ["Project", "Purchase", "Rental"]),
                 ("Food &amp; Beverage", "Recipes, batch production, lot and expiry tracking, and restaurant POS.", ["MRP", "Inventory", "POS"]),
                 ("Hospitality &amp; Events", "Bookings, event ticketing, front-desk POS, and staff scheduling.", ["Events", "POS", "Planning"]),
                 ("Automotive &amp; Field Service", "Service jobs, spare parts, technician scheduling, and vehicle fleets.", ["Field Service", "Inventory", "Fleet"])])),
             ("talk", dict(alt=True, title="Prefer to Talk Now?",
                           sub="Call us or send us an email. We're happy to answer questions before you commit to anything.")),
         ]),
]
