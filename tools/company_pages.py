"""
Content for the company pages: dist/about.html and dist/contact.html.

Rendered by build_module_pages.py with the same section types as the module
and service pages. `nav` is the header link that gets highlighted.

CONTACT_DETAILS: fill in the real values and re-run the build; only the
filled-in ones are shown on the contact page, beside the form.
"""
from service_pages import row, sq

CONTACT_DETAILS = dict(
    email="",     # e.g. "hello@unisas.in"
    phone="",     # e.g. "+91 98765 43210"
    whatsapp="",  # digits with country code, e.g. "919876543210"
    address="",   # e.g. "Street, City, State PIN"
    hours="",     # e.g. "Mon–Sat, 9:30 am – 6:30 pm IST"
)

ICON_ABOUT = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="9" cy="8" r="3.2" stroke="currentColor" stroke-width="1.6"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="17" cy="9" r="2.4" stroke="currentColor" stroke-width="1.6"/><path d="M16.5 14.2c2.6.3 4.5 2.6 4.5 5.8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
ICON_CONTACT = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 5h16a1 1 0 011 1v10a1 1 0 01-1 1H9l-5 4V6a1 1 0 011-1z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M8 10h8M8 13h5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'


def contact_cards():
    d = CONTACT_DETAILS
    wa = "".join(c for c in d["whatsapp"] if c.isdigit())
    cards = [
        ("Email", d["email"], "mailto:" + d["email"]),
        ("Phone", d["phone"], "tel:" + d["phone"].replace(" ", "")),
        ("WhatsApp", "Chat with us", "https://wa.me/" + wa) if wa else ("WhatsApp", "", ""),
        ("Office", d["address"], ""),
        ("Working hours", d["hours"], ""),
    ]
    return [(label, ('<a href="%s">%s</a>' % (href, value)) if href else value) for label, value, href in cards if value]


COMPANY_MOCKS = {
    "about": '<div class="mock mk-team">'
        '<div class="mk-head"><div><span class="mono">YOUR PROJECT TEAM</span><strong>One team, start to finish</strong></div><em class="mk-pill ok">Single point of contact</em></div>'
        + row(sq("PM", "#1E3A5F"), "Project manager", "Phases, sign-offs &amp; timeline", "Every phase", "info")
        + row(sq("FC", "#5DC1AA"), "Functional consultant", "Maps your processes to Odoo", "Design &amp; training", "info")
        + row(sq("DV", "#8E4F83"), "Odoo developer", "Custom modules &amp; integrations", "Build", "info")
        + row(sq("QA", "#EE8A3C"), "QA tester", "Tests every scenario before go-live", "Testing", "info")
        + '<div class="mk-team-foot"><span>Workshop</span><i></i><span>Go-live</span><i></i><span>Long-term support</span></div>'
        '</div>',
}


COMPANY = [
    dict(slug="about", nav="About", name="About Unisas", short="Who we are and how we work", icon_svg=ICON_ABOUT,
         title="About Unisas | Odoo Implementation Partner",
         meta="About Unisas (ITBusiness Solutions Private Limited): certified Odoo consultants and developers who scope, build, launch and support Odoo for growing businesses.",
         hero=dict(style="split", eyebrow="ABOUT UNISAS", title="The Odoo team that stays after go-live",
                   lead="Unisas (ITBusiness Solutions Private Limited) is an Odoo implementation partner. Our certified consultants and developers understand business processes as well as code, and one team scopes, builds, launches and supports your system for the long term.",
                   points=["Certified Odoo consultants", "Standard first, custom when it pays", "You own your code"],
                   cta="Talk to our team", cta2="How we work", cta2_href="principles"),
         sections=[
             ("stats", dict(items=[("1 team", "from workshop to long-term support"), ("v16–v19", "Odoo versions we work with"),
                                   ("Both", "Community &amp; Enterprise"), ("Any host", "Odoo Online, Odoo.sh or on-premise")])),
             ("features", dict(eyebrow="WHAT WE BELIEVE", title="The principles behind every Odoo project", extra=' id="principles"', items=[
                 ("Standard first", "We use what Odoo already does well, and build custom only when configuration can't do the job."),
                 ("Upgrade-safe by design", "Custom work lives in separate modules, never in Odoo's core, so upgrades stay predictable."),
                 ("Clear phases and sign-offs", "Every phase ends with a deliverable you approve, so there are no surprises at go-live."),
                 ("Trained on your own system", "Your team learns on your configured database, not a generic demo."),
                 ("You own the result", "Documents, configuration and custom code are yours to keep, with any partner."),
                 ("In it for the long run", "We stay on after launch to support, improve and upgrade your Odoo.")])),
             ("steps_h", dict(eyebrow="OUR APPROACH", title="A proven, phased method", alt=True, items=[
                 ("Understand", "Workshops with the people who do the work."),
                 ("Plan", "Scope, modules, data and timelines agreed."),
                 ("Configure", "Standard Odoo set up to match the plan."),
                 ("Customize", "Custom modules where standard falls short."),
                 ("Integrate", "Payment, shipping and in-house systems connected."),
                 ("Support", "Go-live, training and continuous improvement.")])),
             ("zigzag", dict(eyebrow="WORK WITH US", title="Three ways to work with our team", sub="Pick the model that fits your project today and switch as your needs change.", items=[
                 ("FIXED-SCOPE PROJECT", "Scope and cost agreed up front", "After a discovery session we agree scope, deliverables and cost, then deliver in phases with clear sign-offs.",
                  ["Ideal for new implementations & migrations", "Milestone-based delivery & billing", "Training & hypercare included"]),
                 ("DEDICATED ODOO TEAM", "Odoo specialists as an extension of your team", "Developers, functional consultants, project managers and QA testers who work on your priorities, full-time or part-time.",
                  ["Monthly engagement, scale up or down", "Your timezone, your tools", "You own all the code"]),
                 ("SUPPORT RETAINER", "Pre-booked hours for a live system", "A block of monthly hours for fixes, small enhancements and regular care of an Odoo system that's already running.",
                  ["Priority response & bug fixes", "Small enhancements & new reports", "Upgrade & performance reviews"])])),
             ("checklist", dict(eyebrow="INDUSTRIES", title="Businesses we build Odoo for", alt=True, sub="We tailor each implementation to the workflows, compliance needs and reporting your industry demands.", items=[
                 "Manufacturing", "Retail &amp; distribution", "eCommerce", "Logistics &amp; wholesale", "Professional services",
                 "Trading &amp; import/export", "Healthcare &amp; clinics", "Education &amp; training"])),
         ],
         related_head=("What we do", "OUR SERVICES", "Every stage of your Odoo project, handled by the same team."),
         related=["odoo-consulting", "odoo-implementation", "odoo-support"],
         faq_title="Questions about working with Unisas",
         faq=[("Which Odoo versions and editions do you work with?", "We work with Odoo versions 16 to 19, on both Community and Enterprise, hosted on Odoo Online, Odoo.sh or your own servers."),
              ("Can you take over a project started by another partner?", "Yes. We start with a health check of your configuration and custom code, then take over support, fixes or the remaining rollout."),
              ("Do you only do large projects?", "No. We work with teams of around 15 people as well as multi-company operations, and phased rollouts let smaller businesses start with the modules they need first.")]),

    dict(slug="contact", nav="Contact", name="Contact", short="Talk to an Odoo consultant", icon_svg=ICON_CONTACT, form_first=True,
         title="Contact Unisas | Book a Free Odoo Consultation",
         meta="Contact Unisas to discuss your Odoo project. Book a free consultation with an Odoo consultant and get a reply within 1 business day.",
         # kept deliberately simple: a short heading, then the form (and contact details once filled in)
         hero=dict(style="simple", eyebrow="CONTACT US", title="Get in touch",
                   lead="Fill in the form and an Odoo consultant will reply within 1 business day."),
         sections=[]),
]
