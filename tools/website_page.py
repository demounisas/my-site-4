"""
Odoo Website page (odoo-ecommerce.html). Every screen is modelled on the real Odoo 20 Website app
(demo.odoo.com/odoo/website): the website builder with its Blocks / Customize / Theme panel and
snippets, the Optimize SEO dialog, Visitors, Live Chat, Website settings, Rewrite (301) redirects,
and the links from website forms and the shop to CRM, Sales, Inventory and Accounting.
Sample company: a Chennai fan maker selling to dealers, builders and homeowners under the
fictional brand "Kaveri Fans". Shared Odoo look: odoo-ui.css. Page styles: website.css.

hero(g) and build(g) get the build script's globals.
"""
import json

from crm_explorer import ic

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def head(eyebrow, title, sub="", cls=""):
    return ('<div class="wb-head%s"><p class="wb-eyebrow mono">%s</p><h2 class="wb-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="wb-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="wb-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


def data(sid, obj):
    """JSON for the page script, safe inside a <script> element."""
    return '<script type="application/json" id="%s">%s</script>' % (sid, json.dumps(obj).replace("</", "<\\/"))


def ox_head(a, b, right=""):
    return ('<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>%s</a><span>%s</span></span></div><span></span>%s</div>'
            % (a, b, right or "<span></span>"))


def browser(url, inner, cls=""):
    return ('<div class="wb-br %s"><div class="wb-br-bar"><i></i><i></i><i></i><span class="mono">%s</span></div><div class="wb-br-body">%s</div></div>' % (cls, url, inner))


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">Website</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["Edit pages without a developer", "Every form lands in your CRM", "Shop tied to live stock &amp; prices"])
    copy = ('<div class="wb-hero-copy">%s<p class="wb-eyebrow mono">ODOO WEBSITE IMPLEMENTATION</p>'
            '<h1 class="wb-h1">Business Website Development <span>Connected to Your Sales and Operations</span> with Odoo</h1>'
            '<p class="wb-lead">Unisas builds your website on Odoo, on the same system as your CRM, sales, stock and accounts. Enquiries become leads, '
            'quotes and orders on their own, product pages show real prices and stock, and your team updates the site themselves.</p>'
            '<ul class="wb-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Discuss your Odoo website %s</a>'
            '<a href="#explore" class="btn btn-ghost">Try the website builder</a></div></div>' % (crumb, points, g["ARROW"]))
    site = ('<div class="wb-hx-site"><div class="wb-hx-nav"><b>Kaveri<span>Fans</span></b><span>Shop</span><span>Dealers</span><span>Projects</span><span class="is-btn">Get a quote</span></div>'
            '<div class="wb-hx-hero"><div><small class="mono">BLDC &middot; 5-STAR RATED</small><strong>Ceiling fans built for Indian summers</strong><span class="wb-hx-cta">Shop fans</span></div><span class="wb-hx-fan" aria-hidden="true"><i></i><i></i><i></i></span></div>'
            '<div class="wb-hx-prods"><div><span></span><b>Aero 48</b><small>&#8377; 3,490 &middot; In stock</small></div><div><span></span><b>Breeze 36</b><small>&#8377; 2,790 &middot; 8 left</small></div><div><span></span><b>Turbo 40</b><small>&#8377; 2,450 &middot; In stock</small></div></div>'
            '<div class="wb-hx-form"><b>Dealer enquiry</b><span>Shree Distributors</span><span>ops@shreedist.in</span><em>Send</em></div></div>')
    pins = "".join('<i class="wb-hv-pin" style="--x:%d;--y:%d">%d</i>' % (x, y, n) for n, x, y in [(1, 66, 24), (2, 22, 62), (3, 95, 79)])
    phone = ('<div class="wb-hv-ph"><div class="wb-hv-ph-scr"><div class="wb-hv-mnav"><b>Kaveri<span>Fans</span></b><i aria-hidden="true"></i></div>'
             '<div class="wb-hv-mhero"><small class="mono">BLDC FANS</small><strong>Built for Indian summers</strong></div>'
             '<div class="wb-hv-mprod"><span></span><p><b>Aero 48</b><small>&#8377; 3,490 &middot; In stock</small></p></div>'
             '<div class="wb-hv-mprod"><span></span><p><b>Breeze 36</b><small>&#8377; 2,790 &middot; 8 left</small></p></div><p class="wb-hv-mbtn">Get a quote</p></div></div>')
    legend = "".join('<li><i class="wb-hv-pin">%d</i><span><b>%s</b>%s</span></li>' % (n, t, x) for n, t, x in
                     [(1, "Edited by your team", "Blocks, text and theme changed in the builder"), (2, "Live price &amp; stock", "Read from Sales and Inventory"),
                      (3, "Form to CRM lead", "Every enquiry assigned to a salesperson")])
    return ('<section class="wb-hero">' + copy + '<div class="wb-hero-vis wb-hv" aria-label="A company website built on Odoo, on a laptop and a phone, with what each part connects to">'
            '<div class="wb-hv-lap"><div class="wb-hv-lid"><div class="wb-hv-scr">' + site + pins + '</div></div><div class="wb-hv-base"></div></div>'
            + phone + '<ol class="wb-hv-leg">' + legend + '</ol></div></section>')

# ------------------------------------------------------------------ sections
def build(g):
    out = ""
    app_icon = g["TILE_ICONS"][8]

    # 1 ---- beyond the brand: hotspots on a page, brochure vs Odoo
    pins = [("Sign in", 96, 6, "Customer portal", "There is no login, so dealers phone in for order status and invoice copies.",
             "Dealers sign in to see their own prices, reorder, track deliveries and download invoices."),
            ("Get a quote", 25, 32, "Quote requests", "The button opens an email client. Half the requests never arrive, and none are tracked.",
             "A quote request becomes a CRM opportunity with the product, quantity and page it came from."),
            ("Products", 52, 54, "Live prices and stock", "Prices are typed into the page and go out of date. Stock is never shown.",
             "Product pages read prices and stock from Odoo, so what the site shows is what you can deliver."),
            ("Chat", 89, 84, "Live conversations", "No chat, or a plug-in whose conversations live outside your systems.",
             "Live Chat answered by sales, with the conversation saved on the contact and turned into a lead in one click."),
            ("Contact form", 36, 74, "Lead capture", "The form emails an inbox. Nobody owns the follow-up.",
             "Each form submission creates a lead, tagged with its source and campaign and assigned to a salesperson."),
            ("Visitors", 74, 70, "Who is looking", "You know how many people visited, not who or what they looked at.",
             "Odoo tracks known visitors and the pages they viewed, so sales can call the dealer who read the price list twice.")]
    pin_html = "".join('<button type="button" class="wb-pin%s" data-p1="%d" style="--x:%d;--y:%d" aria-label="%s" aria-pressed="%s">%d</button>'
                       % (" is-on" if i == 0 else "", i, x, y, n, "true" if i == 0 else "false", i + 1) for i, (n, x, y, *_r) in enumerate(pins))
    page = ('<div class="wb-mock"><div class="wb-m-nav"><b>Kaveri Fans</b><span></span><span></span><span></span><em>Sign in</em></div>'
            '<div class="wb-m-hero"><span class="wb-m-h"></span><span class="wb-m-l"></span><span class="wb-m-l is-s"></span><em>Get a quote</em></div>'
            '<div class="wb-m-row"><div class="wb-m-prods"><span></span><span></span><span></span></div></div>'
            '<div class="wb-m-row is-2"><div class="wb-m-form"><span></span><span></span><span></span><em></em></div><div class="wb-m-vis"><span></span><span></span></div></div>'
            '<span class="wb-m-chat"></span>%s</div>' % pin_html)
    out += sec(head("BEYOND THE BRAND", "What Should Your Business Website Do Beyond Presenting Your Brand?",
                    "A brochure website looks good and stops there. A business website takes enquiries, quotes, orders and questions, and hands each one to the right person. "
                    "Click a numbered spot and switch between the two.", "is-center")
               + '<div class="wb-bro" data-p1box><div class="wb-bro-l">%s<div class="wb-mode" role="group" aria-label="Website type"><button type="button" class="is-on" data-p1mode="bro" aria-pressed="true">Brochure website</button>'
                 '<button type="button" data-p1mode="odoo" aria-pressed="false">Odoo website</button></div></div>'
                 '<div class="wb-p1-card ox-solo" aria-live="polite"><p class="mono" data-p1k></p><h3 data-p1n></h3><p data-p1t></p><p class="wb-p1-score" data-p1s></p></div></div>'
                 % browser("yourcompany.in", page) + data("wb-pins", pins), "wb-sec--bro")

    # 2 ---- the website builder
    out += sec(head("A CONNECTED CHANNEL", "How Can Odoo Turn Your Website Into a Connected Business Channel?",
                    "This is the Odoo website builder. Click <b>Edit</b>, drop in blocks, restyle the theme and save. Then leave edit mode and use the site as a visitor: "
                    "add a fan to the cart or send the dealer form and see where it lands.", "is-center")
               + '<div class="ox wb-ox wb-ed" data-edbox><div class="wb-ed-bar" data-ed-bar></div><div class="wb-ed-main"><div class="wb-ed-canvas" data-ed-canvas></div><aside class="wb-ed-side" data-ed-side hidden></aside></div>'
                 '<div class="wb-ed-toast" data-ed-toast aria-live="polite"></div></div>'
                 '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview of the Odoo website builder. Edit, add blocks, change the theme, then try the form and cart.</p>'
               + data("wb-edicon", app_icon), "wb-sec--ed", "explore")

    # 3 ---- customer journey on the sitemap
    nodes = {"home": "Home", "prod": "Products", "pdp": "Aero 48 product page", "shop": "Shop", "cart": "Cart &amp; checkout", "dealer": "Dealer programme",
             "dform": "Dealer enquiry form", "portal": "My account (portal)", "proj": "Projects", "case": "Case study: 600-flat project", "quote": "Request a project quote",
             "blog": "Blog", "post": "Choosing a BLDC fan", "jobs": "Careers", "job": "Job: Service Technician"}
    tree = [["home"], ["prod", "pdp"], ["shop", "cart", "portal"], ["dealer", "dform"], ["proj", "case", "quote"], ["blog", "post"], ["jobs", "job"]]
    personas = [("dealer", "Dealer", "Wants margins, stock and a fast reorder", [("home", "Lands from a Google search for &lsquo;fan dealership Tamil Nadu&rsquo;", "Visitor tracked with source: Google"),
                    ("dealer", "Reads the dealer programme", "Page view logged on the visitor"), ("dform", "Sends the dealer enquiry form", "Lead in CRM, assigned to the Tamil Nadu sales team"),
                    ("portal", "Approved, signs in to the portal", "Sees dealer pricelist, orders and invoices"), ("cart", "Reorders 120 fans online", "Sales order at dealer prices, delivery created")]),
                ("home", "Homeowner", "Wants the right fan, delivered", [("post", "Finds the blog post on choosing a BLDC fan", "Visitor tracked; reads 2 posts"),
                    ("pdp", "Compares the Aero 48 page", "Live price and &lsquo;In stock&rsquo; from Inventory"), ("shop", "Adds 3 fans to the cart", "Abandoned-cart email if they leave"),
                    ("cart", "Pays by UPI at checkout", "Order confirmed, payment recorded, delivery created"), ("portal", "Tracks the delivery in My account", "Invoice downloadable, warranty registered")]),
                ("builder", "Builder", "Wants volume pricing for a project", [("proj", "Opens Projects from the menu", "Visitor tracked"), ("case", "Reads the 600-flat case study", "Page view logged"),
                    ("quote", "Requests a project quote for 1,800 fans", "Opportunity in CRM with quantity and site location"), ("dform", "Books a call with sales", "Meeting in the salesperson&rsquo;s calendar")]),
                ("job", "Job seeker", "Wants a role near home", [("home", "Arrives from a job portal", "Source tracked"), ("jobs", "Browses open roles", "Published from Recruitment"),
                    ("job", "Applies for Service Technician", "Applicant in Recruitment with CV attached")])]
    pb = "".join('<button type="button" class="wb-per%s" data-p3="%d" aria-pressed="%s"><b>%s</b><small>%s</small></button>' % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", n, x) for i, (k, n, x, s) in enumerate(personas))
    out += sec(head("YOUR CUSTOMER JOURNEY", "How Does Unisas Plan Your Website Around Your Customer Journey?",
                    "We start from who visits and what they need to do, then design the sitemap so each journey is short and every step is recorded in Odoo. "
                    "Choose a visitor and follow their path through the site.", "is-center")
               + '<div class="wb-jr" data-p3box><div class="wb-pers" role="group" aria-label="Visitor type">%s</div><div class="wb-jr-g"><div class="wb-map ox-solo" data-p3map></div>'
                 '<ol class="wb-steps ox-solo" data-p3steps aria-live="polite"></ol></div></div>' % pb
               + data("wb-nodes", nodes) + data("wb-tree", tree) + data("wb-pers", personas), "wb-sec--jr")

    # 4 ---- visibility, engagement, lead generation
    t4 = "".join('<button type="button" class="wb-tab%s" data-p4tab="%s" aria-pressed="%s">%s<small>%s</small></button>' % (" is-on" if k == "seo" else "", k, "true" if k == "seo" else "false", n, x)
                 for k, n, x in [("seo", "Visibility", "Optimize SEO"), ("chat", "Engagement", "Live Chat"), ("vis", "Lead generation", "Visitors")])
    visitors = [["IN-TN", "Shree Distributors", "Coimbatore", 9, "Dealer programme", "2 min ago", "known"], ["IN-KA", "Website Visitor #4821", "Bengaluru", 5, "Aero 48 product page", "6 min ago", ""],
                ["IN-TN", "Nair Builders", "Chennai", 7, "Case study: 600-flat project", "14 min ago", "known"], ["IN-KL", "Website Visitor #4817", "Kochi", 2, "Blog: Choosing a BLDC fan", "21 min ago", ""],
                ["IN-MH", "Orbit Interiors", "Pune", 4, "Request a project quote", "1 hour ago", "known"]]
    out += sec(head("VISIBILITY, ENGAGEMENT &amp; LEADS", "Which Odoo Website Features Can Improve Visibility, Engagement and Lead Generation?",
                    "Search tools to be found, chat to start conversations, and visitor tracking to know who is ready to buy. All three are built into Odoo and share the same contacts as your CRM.", "is-center")
               + '<div class="wb-feat" data-p4box><div class="wb-tabs" role="group" aria-label="Feature">%s</div><div class="wb-feat-b" data-p4b></div></div>' % t4
               + data("wb-visitors", visitors), "wb-sec--feat")

    # 5 ---- shaped around requirements: settings change the site
    sets = [("shop", "eCommerce", "Sell online with cart, checkout and payments", True), ("b2b", "Customer Account: B2B on invitation", "Dealers sign in for their own prices", True),
            ("lang", "Languages", "English, Tamil and Hindi", False), ("blog", "Blog", "Articles that bring search traffic", True), ("appt", "Appointments", "Visitors book a call or demo", False),
            ("events", "Events", "Dealer meets and product launches", False), ("jobs", "Jobs", "Careers page fed by Recruitment", False), ("chat", "Live Chat", "Chat window on every page", True),
            ("cookie", "Cookies Bar", "Consent banner for analytics cookies", True)]
    st5 = "".join('<li><label class="wb-set"><span class="wb-set-t"><b>%s</b><small>%s</small></span><input type="checkbox" data-p5="%s"%s><span class="wb-sw" aria-hidden="true"></span></label></li>'
                  % (n, x, k, " checked" if on else "") for k, n, x, on in sets)
    out += sec(head("SHAPED TO YOUR BUSINESS", "How Does Unisas Shape Odoo Website Around Your Business Requirements?",
                    "The same Odoo website can be a lead-generation site, a dealer portal or a full store. We switch on what your business needs and nothing else. "
                    "Turn features on and off and watch the site change.", "is-center")
               + '<div class="wb-shape" data-p5box><div class="ox wb-ox">%s<ul class="wb-sets">%s</ul></div><div class="wb-shape-r"><div data-p5site></div><p class="wb-shape-n" data-p5note aria-live="polite"></p></div></div>'
                 % (ox_head("Website", "Settings"), st5), "wb-sec--shape")

    # 6 ---- website to CRM, Sales and eCommerce
    flows = [("form", "Dealer enquiry form", [("web", "Website", "Form submitted", "Shree Distributors &middot; &lsquo;Interested in dealership for Coimbatore&rsquo;"),
                                                ("crm", "CRM", "Lead created", "Website: Dealer enquiry &middot; Source: Google / organic &middot; Team: Tamil Nadu"),
                                                ("crm", "CRM", "Assigned &amp; scheduled", "Rahul Menon &middot; Call tomorrow 11:00"),
                                                ("sale", "Sales", "Quotation sent", "S00241 &middot; 120 fans at dealer pricelist &middot; &#8377; 3,42,000.00")]),
             ("quote", "Request a quote on a product page", [("web", "Website", "Quote requested", "Aero 48 &times; 1,800 &middot; Nair Builders"),
                                                ("crm", "CRM", "Opportunity created", "Expected revenue &#8377; 52,92,000.00 &middot; Product: Aero 48"),
                                                ("sale", "Sales", "Quotation from the opportunity", "S00242 &middot; project pricelist &middot; signed online"),
                                                ("inv", "Inventory", "Delivery scheduled", "WH/OUT/00244 &middot; 3 batches of 600")]),
             ("order", "Online order", [("web", "Website", "Order placed", "3 &times; Breeze 36 &middot; paid by UPI &middot; &#8377; 8,370.00"),
                                        ("sale", "Sales", "Sales order confirmed", "S00243 &middot; eCommerce team"),
                                        ("inv", "Inventory", "Stock reserved, delivery created", "WH/OUT/00245 &middot; Breeze 36 stock 8 &rarr; 5"),
                                        ("acc", "Accounting", "Invoice &amp; payment", "INV/2026/00439 posted &middot; Razorpay payment reconciled")])]
    apps6 = [("web", "Website", "#2F6BD8"), ("crm", "CRM", "#8E4F83"), ("sale", "Sales", "#EE8A3C"), ("inv", "Inventory", "#1F8A78"), ("acc", "Accounting", "#B7791F")]
    fb = "".join('<button type="button" class="wb-flow%s" data-p6="%d" aria-pressed="%s">%s</button>' % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", n) for i, (k, n, s) in enumerate(flows))
    cols6 = "".join('<div class="wb-lane" data-p6lane="%s" style="--c:%s"><p class="wb-lane-h"><i></i>%s</p><div class="wb-lane-b"></div></div>' % (k, c, n) for k, n, c in apps6)
    out += sec(head("CRM, SALES &amp; ECOMMERCE", "How Can Odoo Connect Your Website With CRM, Sales and eCommerce?",
                    "There is no connector to maintain: the website writes straight into the same database as your sales team. Pick what a visitor does and follow it across the apps.", "is-center")
               + '<div class="wb-x" data-p6box><div class="wb-flows ox-solo" role="group" aria-label="Visitor action">%s<button type="button" class="ox-pbtn" data-p6run>Run again</button></div><div class="wb-lanes">%s</div></div>'
                 % (fb, cols6) + data("wb-flows", flows), "wb-sec--x")

    # 7 ---- configure, customize or integrate: a guessing game
    reqs = [("Dealer-only prices after login", "cfg", "Pricelists by customer, plus B2B sign-in. Standard Odoo."),
            ("Pay by UPI through Razorpay", "cfg", "Razorpay is a built-in payment provider in Odoo. You add your keys."),
            ("Choose fan colour and blade finish on the product page", "cfg", "Product variants with the configurator on the product page."),
            ("Register a warranty by serial number", "custom", "A small module: a website form that checks the serial number in Inventory and records the warranty."),
            ("Dealer locator that searches by pincode", "custom", "A custom snippet that reads dealer addresses and filters by distance."),
            ("Courier rates and labels from Shiprocket", "int", "A shipping connector calls the courier&rsquo;s API for rates, labels and tracking."),
            ("Show Google reviews on product pages", "int", "A scheduled job pulls reviews from the Google Business API.")]
    lab = {"cfg": "Configure", "custom": "Customize", "int": "Integrate"}
    rq = "".join('<li class="wb-q" data-p7="%d"><p>%s</p><span class="wb-q-b">%s</span><small class="wb-q-why"></small></li>'
                 % (i, r[0], "".join('<button type="button" data-p7a="%s">%s</button>' % (k, v) for k, v in lab.items())) for i, r in enumerate(reqs))
    out += sec(head("CONFIGURE, CUSTOMIZE OR INTEGRATE", "When Should Your Odoo Website Use Configuration, Customization or Integration?",
                    "Configure first, because it costs nothing at upgrade time. Customize only for something specific to your business that repeats often. Integrate when the data lives in another system. "
                    "Make your call for each requirement.", "is-center")
               + '<div class="wb-quiz" data-p7box><ol>%s</ol><div class="wb-quiz-s ox-solo"><p class="mono">YOUR SCORE</p><b data-p7score>0 / %d</b><p data-p7msg>Pick an answer for each requirement.</p>'
                 '<ul><li><i class="is-cfg"></i><b>Configure</b> settings, data, Studio</li><li><i class="is-custom"></i><b>Customize</b> code, kept small</li><li><i class="is-int"></i><b>Integrate</b> API or connector</li></ul></div></div>'
                 % (rq, len(reqs)) + data("wb-reqs", reqs), "wb-sec--quiz")

    # 8 ---- migration: redirects
    urls = [["/index.php", "auto", "/"], ["/products/aero-48-ceiling-fan/", "auto", "/shop/aero-48-ceiling-fan-1200mm"],
            ["/product-category/ceiling-fans/", "map", ["/shop/category/ceiling-fans", "/shop", "410 Gone"]],
            ["/2019/05/summer-cooling-tips/", "auto", "/blog/tips/summer-cooling-tips"], ["/dealer-registration/", "map", ["/dealers", "/contactus", "410 Gone"]],
            ["/offers/diwali-2021/", "map", ["410 Gone", "/shop", "/"]], ["/wp-content/uploads/catalogue-2025.pdf", "map", ["/web/content/catalogue-2026.pdf", "410 Gone"]],
            ["/contact-us/", "auto", "/contactus"]]
    inv = [("Pages", "48 &rarr; 31", "Merged thin pages"), ("Blog posts", "126", "With dates and authors"), ("Products", "640", "With images and specs"),
           ("Customers &amp; dealers", "2,310", "Into Contacts, portal invitations later"), ("Newsletter subscribers", "8,900", "With consent dates"), ("Redirects", "412", "Every old URL that had traffic")]
    out += sec(head("MIGRATION", "How Does Unisas Handle Existing Website Migration and Data Transition?",
                    "The risk in a website move is losing the search rankings your old URLs earned. We map every URL that had traffic to its new page with a 301 redirect before launch. "
                    "Map the remaining URLs and create the redirects.", "is-center")
               + '<div class="wb-mig" data-p8box><div class="ox wb-ox">%s<div class="ox-scroll"><table class="ox-table wb-url-t"><thead><tr><th>Old URL (WordPress)</th><th></th><th>New URL in Odoo</th><th>Status</th></tr></thead><tbody data-p8rows></tbody></table></div>'
                 '<div class="wb-rw" data-p8rw></div></div><ul class="wb-inv ox-solo"><li class="wb-inv-h"><b>What moves across</b><small>From a 6-year-old WordPress site</small></li>%s</ul></div>'
                 % (ox_head("Website", "Redirect map", '<span><button type="button" class="ox-pbtn" data-p8go disabled>Create Redirects</button></span>'),
                    "".join('<li><span>%s<small>%s</small></span><b>%s</b></li>' % (a, c, b) for a, b, c in inv)) + data("wb-urls", urls), "wb-sec--mig")

    # 9 ---- before go-live: checklist and audit rings
    checks = [("Domain &amp; SSL", "Domain pointed to Odoo and HTTPS certificate active", 1, "bp", 10),
              ("SEO", "Titles and descriptions on every page", 1, "seo", 14), ("SEO", "301 redirects from the old site tested", 1, "seo", 10),
              ("SEO", "Sitemap submitted to Google Search Console", 0, "seo", 8), ("Forms", "Every form tested into CRM and the right inbox", 1, "", 0),
              ("Payments", "Razorpay live keys set and a &#8377; 1 test order refunded", 1, "bp", 8), ("Legal", "Cookie bar, privacy policy and terms published", 1, "bp", 7),
              ("Speed", "Images compressed and lazy-loaded", 0, "perf", 20), ("Speed", "Unused snippets and fonts removed", 0, "perf", 12),
              ("Accessibility", "Alt text on images and colour contrast checked", 0, "a11y", 15), ("Accessibility", "Every page checked on a phone", 0, "a11y", 10),
              ("Analytics", "Analytics and conversion goals recording", 0, "", 0)]
    cl = "".join('<li><label class="wb-ck"><input type="checkbox" data-p9="%d"><span class="wb-ck-box" aria-hidden="true">%s</span><span><small>%s%s</small>%s</span></label></li>'
                 % (i, TICK, c, ' &middot; <em>Must have</em>' if crit else "", t) for i, (c, t, crit, k, v) in enumerate(checks))
    rings = [("perf", "Performance", 62), ("a11y", "Accessibility", 71), ("bp", "Best Practices", 75), ("seo", "SEO", 68)]
    rh = "".join('<li data-p9ring="%s" data-base="%d"><span class="wb-ring" style="--p:%d"><b>%d</b></span><small>%s</small></li>' % (k, v, v, v, n) for k, n, v in rings)
    out += sec(head("BEFORE GO-LIVE", "What Does an Odoo Website Implementation Need Before Going Live?",
                    "Twelve checks stand between a finished site and a safe launch. The must-haves protect your rankings, payments and enquiries; the rest make the site fast and easy to use. "
                    "Tick them off and watch the page audit scores rise.", "is-center")
               + '<div class="wb-go" data-p9box><ul class="wb-cks">%s</ul><div class="wb-go-r ox-solo"><p class="wb-go-h"><b>Page audit</b><small>kaverifans.in, mobile</small></p><ul class="wb-rings">%s</ul>'
                 '<div class="wb-pub"><span><b data-p9n>0 of 6</b> must-haves done</span><button type="button" class="ox-pbtn" data-p9pub disabled>Publish website</button></div><p class="wb-go-res" data-p9res aria-live="polite"></p></div></div>'
                 % (cl, rh) + data("wb-checks", checks), "wb-sec--go")

    # 10 ---- website and the rest of the business
    blocks = [("Header &middot; My account", "Portal", "#EE8A3C", "Customers and dealers see their orders, deliveries, invoices and tickets in one login.", "Sales &middot; Inventory &middot; Accounting &middot; Helpdesk"),
              ("Product page &middot; price &amp; stock", "Inventory &amp; Pricelists", "#1F8A78", "Price from the visitor&rsquo;s pricelist, stock from the website warehouse, lead time from the route.", "Inventory &middot; Sales"),
              ("Upcoming &middot; Dealer meet, Coimbatore", "Events", "#8E4F83", "Registrations, tickets and reminders, with attendees added to Contacts.", "Events &middot; Email Marketing"),
              ("Book a product demo", "Appointments", "#3E7CB1", "Slots from the salesperson&rsquo;s real calendar; bookings create a meeting and an opportunity.", "Calendar &middot; CRM"),
              ("Support &middot; raise a ticket", "Helpdesk", "#D23F3F", "Warranty and service requests become tickets with SLA timers and a technician assigned.", "Helpdesk &middot; Field Service"),
              ("Careers &middot; open roles", "Recruitment", "#5A7D9A", "Jobs published from Recruitment; applications land as applicants with CVs.", "Recruitment"),
              ("Newsletter sign-up", "Email Marketing", "#C98600", "Subscribers go to a mailing list with consent recorded, ready for the next campaign.", "Email Marketing &middot; Marketing Automation")]
    bl = "".join('<button type="button" class="wb-blk%s" data-p10="%d" style="--c:%s" aria-pressed="%s"><span>%s</span><em>%s</em></button>'
                 % (" is-on" if i == 0 else "", i, c, "true" if i == 0 else "false", b, a) for i, (b, a, c, x, apps) in enumerate(blocks))
    out += sec(head("THE REST OF YOUR BUSINESS", "How Can Unisas Connect Website Operations With the Rest of Your Business?",
                    "Beyond leads and orders, each part of the site can be the front door to another team: support, events, hiring, marketing. Pick a part of the page to see what sits behind it.", "is-center")
               + '<div class="wb-anat" data-p10box>%s<div class="wb-anat-c ox-solo" aria-live="polite"><p class="mono" data-p10k></p><h3 data-p10n></h3><p data-p10t></p><p class="wb-anat-apps"><small>Apps involved</small><b data-p10a></b></p></div></div>'
                 % browser("kaverifans.in", '<div class="wb-blks">%s</div>' % bl, "is-anat") + data("wb-blocks", blocks), "wb-sec--anat")

    # 11 ---- what your team manages after go-live
    roles = [("mkt", "Marketing", [("Publish a new landing page for the monsoon offer", "Website &rsaquo; Edit &rsaquo; + New &rsaquo; Page", 40), ("Write and schedule a blog post", "+ New &rsaquo; Blog Post", 30),
                                   ("Fix a page title and description", "Promote &rsaquo; Optimize SEO", 5), ("Send the newsletter to dealers", "Email Marketing &rsaquo; New Mailing", 20)]),
             ("sales", "Sales", [("Answer live chats and turn one into a lead", "Live Chat &rsaquo; Conversations", 10), ("Follow up visitors who read the price list", "Website &rsaquo; Reporting &rsaquo; Visitors", 15),
                                 ("Approve a new dealer&rsquo;s portal access", "Contacts &rsaquo; Action &rsaquo; Grant portal access", 2)]),
             ("store", "Store manager", [("Add a new fan model with photos and specs", "eCommerce &rsaquo; Products &rsaquo; New", 15), ("Run a 10% weekend discount", "eCommerce &rsaquo; Discount &amp; Loyalty", 5),
                                         ("Process today&rsquo;s online orders", "eCommerce &rsaquo; Orders &rsaquo; Unpaid / To deliver", 20), ("Change the home page banner", "Website &rsaquo; Edit", 10)]),
             ("hr", "HR", [("Publish a job opening", "Recruitment &rsaquo; Job Positions &rsaquo; Publish", 5), ("Update the careers page text", "Website &rsaquo; Edit", 10)]),
             ("sup", "Support", [("Answer website tickets within SLA", "Helpdesk &rsaquo; My Tickets", 30), ("Add an FAQ article to the help centre", "Knowledge &rsaquo; New Article", 15)])]
    rb = "".join('<button type="button" class="wb-role%s" data-p11="%d" aria-pressed="%s">%s</button>' % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", n) for i, (k, n, t) in enumerate(roles))
    out += sec(head("AFTER GO-LIVE", "What Can Your Team Manage Through Odoo After the Website Goes Live?",
                    "Day-to-day changes don&rsquo;t need a developer or a ticket to an agency. Here is a typical week for each team, with where they click in Odoo and how long it takes.", "is-center")
               + '<div class="wb-week" data-p11box><div class="wb-roles" role="group" aria-label="Team">%s</div><div class="ox wb-ox">%s<ul class="wb-tasks" data-p11list></ul><p class="wb-week-sum" data-p11sum></p></div></div>'
                 % (rb, ox_head("To Do", "This week")) + data("wb-roles", roles), "wb-sec--week")

    # 12 ---- from planning to support
    phases = [("Plan", "Week 1&ndash;2", ["Customer journeys and sitemap", "Feature list: configure, customize, integrate", "Content plan and owners", "URL inventory of the old site"], "Your goals, audiences and access to the current site and analytics."),
              ("Design", "Week 2&ndash;4", ["Wireframes for key pages", "Theme: colours, fonts, buttons", "Mobile layouts", "Design sign-off"], "Logo, brand guidelines and feedback on two design rounds."),
              ("Build", "Week 4&ndash;7", ["Pages built from Odoo blocks", "Forms wired to CRM", "Shop, pricelists and payments", "Custom snippets and connectors"], "Product data, prices and payment provider accounts."),
              ("Content &amp; migration", "Week 6&ndash;8", ["Pages, posts and products moved", "301 redirect map", "Images optimised", "SEO titles and descriptions"], "Approval of rewritten copy and any new photos."),
              ("Launch", "Week 8&ndash;9", ["Go-live checklist completed", "Domain, SSL and Search Console", "Team training by role", "Launch-day monitoring"], "A launch date and someone to approve go-live."),
              ("Grow", "Monthly", ["Analytics and lead report", "SEO and speed fixes", "New pages and campaigns", "Odoo upgrades tested"], "Priorities for the month.")]
    pbt = "".join('<li><button type="button" class="wb-ph%s" data-p12="%d" aria-pressed="%s"><span class="mono">%02d</span><b>%s</b><small>%s</small></button></li>'
                  % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", i + 1, n, w) for i, (n, w, d, y) in enumerate(phases))
    out += sec(head("WHAT WE DELIVER", "What Does Unisas Deliver From Website Planning to Ongoing Support?",
                    "Six phases, each ending with something you can see and sign off. Pick a phase to see what we hand over and what we need from you.", "is-center")
               + '<div class="wb-del" data-p12box><ol class="wb-phs">%s</ol><div class="wb-del-c ox-solo" aria-live="polite"><div><p class="wb-gi-h">Unisas delivers</p><ul class="wb-files" data-p12d></ul></div>'
                 '<div class="wb-del-y"><p class="wb-gi-h">We need from you</p><p data-p12y></p></div></div></div>' % pbt + data("wb-phases", phases), "wb-sec--del")

    # 13 ---- scope the implementation
    out += sec('<div class="wb-scope"><div>%s<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Scope my Odoo website %s</a></div></div>'
               '<div class="wb-sc ox-solo" data-p13box><p class="wb-sc-h"><b>Website scoping</b><small>A first recommendation. We confirm it after a short call.</small></p>'
               '<div class="wb-sc-in"><label class="is-wide"><span>What should the site mainly do?</span><select data-p13="type"><option value="0">Present the company and generate leads</option><option value="1">Leads plus a dealer / B2B portal</option>'
               '<option value="2">Sell online to consumers</option><option value="3">Several brands or countries</option></select></label>'
               '<label><span>Pages <b data-p13o="pages">25</b></span><input type="range" min="5" max="150" step="5" value="25" data-p13="pages"></label>'
               '<label><span>Products online <b data-p13o="prods">0</b></span><input type="range" min="0" max="3000" step="50" value="0" data-p13="prods"></label>'
               '<label><span>Languages <b data-p13o="langs">1</b></span><input type="range" min="1" max="4" value="1" data-p13="langs"></label>'
               '<label><span>Moving from</span><select data-p13="from"><option value="0">No website yet</option><option value="1" selected>WordPress</option><option value="2">Shopify / WooCommerce</option><option value="3">A custom site</option></select></label>'
               '<div class="wb-sc-chk is-wide"><label><input type="checkbox" data-p13x="1"> Courier or marketplace integration</label><label><input type="checkbox" data-p13x="1"> Custom features (configurator, locator)</label></div></div>'
               '<div class="wb-sc-out" data-p13out aria-live="polite"></div></div></div>'
               % (head("SCOPE YOUR PROJECT", "How Can We Scope the Right Odoo Website Implementation for Your Business?",
                       "Scope comes from what the site has to do, how much content and product data moves across, and what it connects to. "
                       "Answer a few questions for a first recommendation, then talk it through with us."), g["ARROW"]), "wb-sec--scope")

    return out + JS


CTA = ("Let's Plan a Website That Works for Your Business",
       "Tell us what your website needs to do: who visits, what they should be able to do, and which systems it should feed. We'll show you how it looks in Odoo and recommend the right scope.")


JS = r'''<script>
(function(){
  function J(id){var e=document.getElementById(id);return e?JSON.parse(e.textContent):null;}
  function press(group,el){group.forEach(function(b){var on=b===el;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});}
  function num(n,d){return n.toLocaleString('en-IN',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  /* --- 1 brochure vs Odoo --- */
  (function(){var bx=document.querySelector('[data-p1box]');if(!bx)return;var P=J('wb-pins'),pins=[].slice.call(bx.querySelectorAll('[data-p1]')),mb=[].slice.call(bx.querySelectorAll('[data-p1mode]')),cur=0,mode='bro';
    function draw(){var p=P[cur];bx.classList.toggle('is-odoo',mode==='odoo');bx.querySelector('[data-p1k]').textContent=(mode==='odoo'?'ODOO WEBSITE · ':'BROCHURE WEBSITE · ')+p[0].toUpperCase();
      bx.querySelector('[data-p1n]').innerHTML=p[3];bx.querySelector('[data-p1t]').innerHTML=mode==='odoo'?p[5]:p[4];
      bx.querySelector('[data-p1s]').innerHTML=mode==='odoo'?'<b>6 of 6</b> jobs done by the website, each recorded in Odoo.':'<b>0 of 6</b> jobs done. Every one still needs a phone call or an email.';}
    pins.forEach(function(b){b.addEventListener('click',function(){press(pins,b);cur=+b.getAttribute('data-p1');draw();});});
    mb.forEach(function(b){b.addEventListener('click',function(){press(mb,b);mode=b.getAttribute('data-p1mode');draw();});});draw();})();

  /* --- 2 website builder --- */
  (function(){var ed=document.querySelector('[data-edbox]');if(!ed)return;
    var bar=ed.querySelector('[data-ed-bar]'),cv=ed.querySelector('[data-ed-canvas]'),side=ed.querySelector('[data-ed-side]'),toast=ed.querySelector('[data-ed-toast]'),icon=J('wb-edicon');
    var SN={banner:'Banner',textimg:'Text - Image',features:'Features',numbers:'Numbers',products:'Products',form:'Form',quote:'Testimonial',cta:'Call to Action'};
    var CAT=[['Structure',['banner','textimg','features','numbers']],['Dynamic Content',['products','form']],['Inner Content',['quote','cta']]];
    var PAL=[['#2F6BD8','#F2B33D','#14213D'],['#1F8A78','#F28C38','#12302B'],['#8E4F83','#5DC1AA','#2A1A2E'],['#C2410C','#0EA5E9','#1C1917']];
    var FONTS=[['Sans','Inter, "Segoe UI", sans-serif'],['Serif','Georgia, "Times New Roman", serif'],['Rounded','"Trebuchet MS", "Segoe UI", sans-serif']];
    var uid=10,st={edit:false,mobile:false,tab:'blocks',sel:null,pal:0,font:0,btn:'round',cart:0,leads:0,dirty:false,
      page:[{id:1,t:'banner',bg:'primary',al:'left'},{id:2,t:'features',bg:'white',al:'center'},{id:3,t:'products',bg:'light',al:'left'},{id:4,t:'form',bg:'white',al:'left'}]};
    var saved=JSON.stringify(st.page),savedTheme=[0,0,'round'];
    var PRODS=[['Aero 48 Ceiling Fan','3,490','In stock',''],['Breeze 36 Ceiling Fan','2,790','Only 8 left','is-low'],['Turbo 40 Pedestal Fan','2,450','In stock','']];
    function block(b){var h='';
      if(b.t==='banner')h='<div class="wb-s-ban"><div><small>BLDC &middot; 5-STAR RATED</small><h4>Ceiling fans built for Indian summers</h4><p>Quiet, 65% less power, and a 2-year warranty on every fan.</p><span class="wb-s-btns"><a class="wb-s-btn" data-act="shop">Shop fans</a><a class="wb-s-btn is-o">Talk to sales</a></span></div><span class="wb-s-img is-fan"><i></i><i></i><i></i></span></div>';
      if(b.t==='textimg')h='<div class="wb-s-ti"><div><h4>Energy-efficient BLDC motors</h4><p>Our motors use 28 W at full speed, so a fan pays for itself in two summers. Made in our Coimbatore plant.</p></div><span class="wb-s-img"></span></div>';
      if(b.t==='features')h='<div class="wb-s-feat"><h4>Why Kaveri Fans</h4><div><span><i>&#9733;</i><b>5-star rated</b><small>BEE certified</small></span><span><i>&#10003;</i><b>2-year warranty</b><small>Registered online</small></span><span><i>&#9906;</i><b>Service in 38 cities</b><small>Technician in 48 h</small></span></div></div>';
      if(b.t==='numbers')h='<div class="wb-s-num"><span><b>1.2M</b><small>fans sold</small></span><span><b>38</b><small>service cities</small></span><span><b>4.6&#9733;</b><small>average rating</small></span></div>';
      if(b.t==='products')h='<div class="wb-s-prod"><h4>Best sellers</h4><div>'+PRODS.map(function(p,i){return '<span><i class="wb-s-pi" style="--h:'+(i*40+200)+'"></i><b>'+p[0]+'</b><em>&#8377; '+p[1]+'</em><small class="'+p[3]+'">'+p[2]+'</small><a class="wb-s-btn is-sm" data-act="cart">Add to cart</a></span>';}).join('')+'</div></div>';
      if(b.t==='form')h='<div class="wb-s-form"><div><h4>Become a dealer</h4><p>Tell us about your shop and we&rsquo;ll send the dealer price list.</p></div><form data-wbform><input value="Shree Distributors" aria-label="Company"><input value="ops@shreedist.in" aria-label="Email"><input value="Coimbatore" aria-label="City"><a class="wb-s-btn" data-act="submit">Send</a></form></div>';
      if(b.t==='quote')h='<div class="wb-s-q"><p>&ldquo;We switched our 600-flat project to Kaveri BLDC fans. Residents noticed the power bill first.&rdquo;</p><small>Anand Nair, Nair Builders</small></div>';
      if(b.t==='cta')h='<div class="wb-s-cta"><b>Building a project? Get volume pricing.</b><a class="wb-s-btn" data-act="submit">Request a quote</a></div>';
      return '<section class="wb-s bg-'+b.bg+' al-'+b.al+(st.edit&&st.sel===b.id?' is-sel':'')+'" data-blk="'+b.id+'">'+(st.edit&&st.sel===b.id?'<span class="wb-s-tag">'+SN[b.t]+'</span>':'')+h+'</section>';}
    function topbar(){if(st.edit)return '<div class="wb-eb is-edit"><span class="wb-eb-l"><b>Editing</b><small>Home</small></span><span class="wb-eb-r"><button type="button" class="ox-sbtn" data-ed="discard">Discard</button><button type="button" class="ox-pbtn" data-ed="save">Save</button></span></div>';
      return '<div class="wb-eb"><span class="wb-eb-l"><span class="ox-app">'+icon+'<b>Website</b></span><span class="ox-menu">Site</span><span class="ox-menu">eCommerce</span><span class="ox-menu">Reporting</span></span>'+
        '<span class="wb-eb-r"><button type="button" class="ox-sbtn" data-ed="new">+ New</button><button type="button" class="wb-dev'+(st.mobile?' is-on':'')+'" data-ed="mobile" aria-pressed="'+st.mobile+'" aria-label="Mobile preview">&#128241;</button>'+
        '<span class="wb-pubd"><i></i>Published</span><button type="button" class="ox-pbtn" data-ed="edit">Edit</button></span></div>';}
    function sidebar(){var tabs=[['blocks','Blocks'],['customize','Customize'],['theme','Theme']].map(function(t){return '<button type="button" data-edtab="'+t[0]+'" class="'+(st.tab===t[0]?'is-on':'')+'">'+t[1]+'</button>';}).join('');
      var b='';
      if(st.tab==='blocks')b=CAT.map(function(c){return '<p class="wb-sd-h">'+c[0]+'</p><div class="wb-snips">'+c[1].map(function(k){return '<button type="button" class="wb-snip" data-add="'+k+'"><span class="wb-snip-i is-'+k+'"></span>'+SN[k]+'</button>';}).join('')+'</div>';}).join('')+'<p class="wb-sd-n">Click a block to add it below the selected one.</p>';
      if(st.tab==='customize'){var s=st.page.filter(function(x){return x.id===st.sel;})[0];
        b=s?'<p class="wb-sd-t">'+SN[s.t]+'</p><p class="wb-sd-h">Background</p><div class="wb-sw-r">'+['white','light','primary','dark'].map(function(c){return '<button type="button" class="wb-swatch bg-'+c+(s.bg===c?' is-on':'')+'" data-bg="'+c+'" aria-label="'+c+'"></button>';}).join('')+'</div>'+
          '<p class="wb-sd-h">Alignment</p><div class="wb-seg">'+['left','center'].map(function(a){return '<button type="button" data-al="'+a+'" class="'+(s.al===a?'is-on':'')+'">'+a[0].toUpperCase()+a.slice(1)+'</button>';}).join('')+'</div>'+
          '<p class="wb-sd-h">Block</p><div class="wb-seg"><button type="button" data-mv="-1">&uarr; Up</button><button type="button" data-mv="1">&darr; Down</button><button type="button" data-dup>Duplicate</button><button type="button" data-del class="is-del">Delete</button></div>'
          :'<p class="wb-sd-n">Select a block on the page to customize it.</p>';}
      if(st.tab==='theme')b='<p class="wb-sd-h">Colors</p><div class="wb-pals">'+PAL.map(function(p,i){return '<button type="button" class="wb-pal'+(st.pal===i?' is-on':'')+'" data-pal="'+i+'" aria-label="Palette '+(i+1)+'">'+p.map(function(c){return '<i style="background:'+c+'"></i>';}).join('')+'</button>';}).join('')+'</div>'+
        '<p class="wb-sd-h">Font</p><div class="wb-seg">'+FONTS.map(function(f,i){return '<button type="button" data-font="'+i+'" class="'+(st.font===i?'is-on':'')+'" style="font-family:'+f[1].replace(/"/g,'&quot;')+'">'+f[0]+'</button>';}).join('')+'</div>'+
        '<p class="wb-sd-h">Buttons</p><div class="wb-seg"><button type="button" data-btn="round" class="'+(st.btn==='round'?'is-on':'')+'">Rounded</button><button type="button" data-btn="square" class="'+(st.btn==='square'?'is-on':'')+'">Square</button></div>';
      return '<div class="wb-sd-tabs">'+tabs+'</div><div class="wb-sd-b">'+b+'</div>';}
    function render(){var p=PAL[st.pal];bar.innerHTML=topbar();side.hidden=!st.edit;if(st.edit)side.innerHTML=sidebar();
      cv.className='wb-ed-canvas'+(st.mobile&&!st.edit?' is-mobile':'')+(st.edit?' is-edit':'')+' btn-'+st.btn;
      cv.style.setProperty('--s1',p[0]);cv.style.setProperty('--s2',p[1]);cv.style.setProperty('--s3',p[2]);cv.style.setProperty('--sf',FONTS[st.font][1]);
      cv.innerHTML='<div class="wb-site"><header class="wb-s-hd"><b>Kaveri<span>Fans</span></b><nav><span>Home</span><span>Shop</span><span>Dealers</span><span>Contact us</span></nav><span class="wb-s-cart">&#128722; <b>'+st.cart+'</b></span></header>'+
        st.page.map(block).join('')+'<footer class="wb-s-ft">&copy; Kaveri Fans &middot; Chennai &middot; Powered by Odoo</footer></div>';}
    function say(h){toast.innerHTML=h;toast.classList.remove('is-on');void toast.offsetWidth;toast.classList.add('is-on');}
    ed.addEventListener('click',function(e){var a=e.target.closest('[data-ed]');
      if(a){var k=a.getAttribute('data-ed');
        if(k==='edit'){st.edit=true;st.tab='blocks';st.sel=null;}
        if(k==='discard'){st.page=JSON.parse(saved);st.pal=savedTheme[0];st.font=savedTheme[1];st.btn=savedTheme[2];st.edit=false;st.sel=null;}
        if(k==='save'){saved=JSON.stringify(st.page);savedTheme=[st.pal,st.font,st.btn];st.edit=false;st.sel=null;say('<b>Saved.</b> The page is live; no developer, no deployment.');}
        if(k==='mobile')st.mobile=!st.mobile;
        if(k==='new')say('<b>+ New</b> creates a Page, Blog Post, Product, Event or Job Position from here.');
        render();return;}
      var t=e.target.closest('[data-edtab]');if(t){st.tab=t.getAttribute('data-edtab');render();return;}
      var ad=e.target.closest('[data-add]');if(ad){var nb={id:++uid,t:ad.getAttribute('data-add'),bg:'white',al:'left'},ix=st.page.map(function(x){return x.id;}).indexOf(st.sel);
        st.page.splice(ix<0?st.page.length:ix+1,0,nb);st.sel=nb.id;st.tab='customize';render();var el=cv.querySelector('[data-blk="'+nb.id+'"]');if(el)el.scrollIntoView({block:'nearest'});return;}
      var s=st.page.filter(function(x){return x.id===st.sel;})[0],i=st.page.indexOf(s);
      var bg=e.target.closest('[data-bg]');if(bg&&s){s.bg=bg.getAttribute('data-bg');render();return;}
      var al=e.target.closest('[data-al]');if(al&&s){s.al=al.getAttribute('data-al');render();return;}
      var mv=e.target.closest('[data-mv]');if(mv&&s){var j=i+(+mv.getAttribute('data-mv'));if(j>=0&&j<st.page.length){st.page.splice(i,1);st.page.splice(j,0,s);}render();return;}
      if(e.target.closest('[data-dup]')&&s){var c={id:++uid,t:s.t,bg:s.bg,al:s.al};st.page.splice(i+1,0,c);st.sel=c.id;render();return;}
      if(e.target.closest('[data-del]')&&s){st.page.splice(i,1);st.sel=null;render();return;}
      var pl=e.target.closest('[data-pal]');if(pl){st.pal=+pl.getAttribute('data-pal');render();return;}
      var fo=e.target.closest('[data-font]');if(fo){st.font=+fo.getAttribute('data-font');render();return;}
      var bt=e.target.closest('[data-btn]');if(bt){st.btn=bt.getAttribute('data-btn');render();return;}
      var blk=e.target.closest('[data-blk]');
      if(st.edit&&blk){e.preventDefault();st.sel=+blk.getAttribute('data-blk');st.tab='customize';render();return;}
      var act=e.target.closest('[data-act]');
      if(act&&!st.edit){var k2=act.getAttribute('data-act');
        if(k2==='cart'){st.cart++;render();say('<b>Added to cart.</b> Price from the public pricelist, stock checked in Inventory.');}
        if(k2==='submit'){st.leads++;say('<b>Lead created in CRM:</b> &lsquo;Website: '+(act.closest('.wb-s-cta')?'Project quote request':'Dealer enquiry')+'&rsquo; &middot; assigned to the Tamil Nadu team &middot; '+st.leads+' today');}
        if(k2==='shop')say('<b>Shop</b> lists products straight from eCommerce, with live stock.');}
    });
    render();})();

  /* --- 3 journey --- */
  (function(){var bx=document.querySelector('[data-p3box]');if(!bx)return;var N=J('wb-nodes'),T=J('wb-tree'),P=J('wb-pers'),bt=[].slice.call(bx.querySelectorAll('[data-p3]'));
    function draw(i){var path=P[i][3],idx={};path.forEach(function(s,j){if(idx[s[0]]===undefined)idx[s[0]]=j+1;});
      function nd(k,cls){return '<span class="wb-nd '+cls+(idx[k]?' is-on':'')+'">'+(idx[k]?'<em>'+idx[k]+'</em>':'')+N[k]+'</span>';}
      bx.querySelector('[data-p3map]').innerHTML='<div class="wb-map-root">'+nd('home','is-root')+'</div><div class="wb-map-cols">'+T.slice(1).map(function(col){return '<div>'+col.map(function(k,j){return nd(k,j?'is-kid':'is-top');}).join('')+'</div>';}).join('')+'</div>';
      bx.querySelector('[data-p3steps]').innerHTML='<li class="wb-st-h"><b>'+P[i][1]+'</b><small>'+P[i][2]+'</small></li>'+path.map(function(s,j){return '<li style="--i:'+j+'"><span class="wb-st-n">'+(j+1)+'</span><span><b>'+s[1]+'</b><small>'+s[2]+'</small></span></li>';}).join('');}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);draw(+b.getAttribute('data-p3'));});});draw(0);})();

  /* --- 4 SEO, chat, visitors --- */
  (function(){var bx=document.querySelector('[data-p4box]');if(!bx)return;var V=J('wb-visitors'),b=bx.querySelector('[data-p4b]'),tb=[].slice.call(bx.querySelectorAll('[data-p4tab]'));
    var st={tab:'seo',title:'Ceiling Fans | Kaveri Fans',desc:'Buy fans online.',kw:['bldc ceiling fan','energy saving fan','ceiling fan price'],chat:0,lead:false,vis:{}};
    var CHAT=[['v','Hi, do you have the Aero 48 in brown? Need 40 for a hotel in Ooty.'],['o','Yes, brown is in stock at our Coimbatore warehouse: 140 units. Shall I send the project price?'],['v','Yes please, and delivery time to Ooty?'],['o','3 to 4 days. I&rsquo;ll create your request so our project team sends a quote today.']];
    function used(k){var t=(st.title+' '+st.desc).toLowerCase(),r=[];if(st.title.toLowerCase().indexOf(k)>-1)r.push('Title');if(st.desc.toLowerCase().indexOf(k)>-1)r.push('Description');if(k==='bldc ceiling fan')r.push('H1');return r;}
    function seo(){var tl=st.title.length,dl=st.desc.length;
      return '<div class="wb-dlg ox-solo"><p class="wb-dlg-h"><b>Optimize SEO</b><small>Promote &rsaquo; Optimize SEO &middot; Home</small></p><div class="wb-seo"><div>'+
        '<label><span>Title <em class="'+(tl>60||tl<30?'is-bad':'is-ok')+'">'+tl+' / 60</em></span><input data-p4seo="title" value="'+esc(st.title)+'"></label>'+
        '<label><span>Description <em class="'+(dl>160||dl<70?'is-bad':'is-ok')+'">'+dl+' / 160</em></span><textarea rows="3" data-p4seo="desc">'+esc(st.desc)+'</textarea></label>'+
        '<p class="wb-sd-h">Keywords</p><table class="wb-kw"><thead><tr><th>Keyword</th><th>Used in page</th><th></th></tr></thead><tbody>'+st.kw.map(function(k,i){var u=used(k);return '<tr><td>'+esc(k)+'</td><td>'+(u.length?u.map(function(x){return '<span class="wb-used">'+x+'</span>';}).join(''):'<span class="wb-used is-no">Not used</span>')+'</td><td><button type="button" data-p4kwx="'+i+'" aria-label="Remove">&times;</button></td></tr>';}).join('')+
        '</tbody></table><div class="wb-kw-add"><input data-p4kw placeholder="Add a keyword"><button type="button" class="ox-sbtn" data-p4kwadd>Add</button></div></div>'+
        '<div><p class="wb-sd-h">Preview</p><div class="wb-gp"><small>kaverifans.in</small><b>'+esc(st.title.slice(0,62))+(tl>62?'&hellip;':'')+'</b><p>'+esc(st.desc.slice(0,158))+(dl>158?'&hellip;':'')+'</p></div>'+
        '<p class="wb-seo-tip">'+(tl>=30&&tl<=60&&dl>=70&&dl<=160?'<b>Good.</b> Title and description are the right length for Google.':'Aim for a <b>30&ndash;60</b> character title and a <b>70&ndash;160</b> character description. Try: &lsquo;BLDC Ceiling Fans that Cut Power Bills by 65% | Kaveri Fans&rsquo;.')+'</p></div></div></div>';}
    function chat(){var lines=CHAT.slice(0,st.chat+1);
      return '<div class="wb-chat-g"><div class="wb-chat ox-solo"><p class="wb-chat-h"><i></i><b>Kaveri Fans</b><small>Kavya is online</small></p><div class="wb-chat-b">'+lines.map(function(l){return '<p class="is-'+l[0]+'">'+l[1]+'</p>';}).join('')+'</div>'+
        '<div class="wb-chat-f">'+(st.chat<CHAT.length-1?'<button type="button" class="ox-pbtn" data-p4next>Next message</button>':(st.lead?'<span class="wb-ok">&#10003; Opportunity created</span>':'<button type="button" class="ox-pbtn" data-p4lead>/lead Create opportunity</button>'))+'</div></div>'+
        '<div class="wb-chat-side ox-solo"><p class="wb-sd-h">In Odoo</p><dl><div><dt>Visitor</dt><dd>Hotel Hilltop, Ooty</dd></div><div><dt>Pages viewed</dt><dd>Aero 48, Projects, Contact</dd></div><div><dt>Conversation</dt><dd>Saved on the contact</dd></div>'+
        '<div><dt>Opportunity</dt><dd>'+(st.lead?'<b>Aero 48 &times; 40 &middot; Ooty hotel</b><br><small>&#8377; 1,39,600.00 &middot; Project team</small>':'<span class="ox-muted">Not yet</span>')+'</dd></div></dl></div></div>';}
    function vis(){return '<div class="ox wb-ox">'+'<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Reporting</a><span>Visitors</span></span></div><span></span><span></span></div><div class="ox-scroll"><table class="ox-table wb-vis-t"><thead><tr><th>Visitor</th><th>Location</th><th class="ox-num">Page views</th><th>Last page</th><th>Last action</th><th></th></tr></thead><tbody>'+
      V.map(function(v,i){var s=st.vis[i];return '<tr><td><span class="wb-flag">'+v[0].split('-')[1]+'</span><b>'+v[1]+'</b>'+(v[6]?'<span class="wb-known">Known contact</span>':'')+'</td><td>'+v[2]+'</td><td class="ox-num">'+v[3]+'</td><td>'+v[4]+'</td><td class="ox-muted">'+v[5]+'</td><td class="ox-num">'+
        (s?'<span class="wb-ok">'+s+'</span>':(v[6]?'<button type="button" class="ox-sbtn" data-p4v="'+i+'" data-p4do="Lead created">Create Lead</button>':'<button type="button" class="ox-sbtn" data-p4v="'+i+'" data-p4do="Chat started">Chat</button>'))+'</td></tr>';}).join('')+
      '</tbody></table></div><p class="wb-vis-n">Known visitors are matched to contacts when they fill a form, sign in or click a newsletter link. Anonymous visitors can be greeted in Live Chat.</p></div>';}
    function draw(){b.innerHTML={seo:seo,chat:chat,vis:vis}[st.tab]();}
    tb.forEach(function(t){t.addEventListener('click',function(){press(tb,t);st.tab=t.getAttribute('data-p4tab');draw();});});
    b.addEventListener('input',function(e){var f=e.target.closest('[data-p4seo]');if(f){st[f.getAttribute('data-p4seo')]=f.value;var pos=f.selectionStart,k=f.getAttribute('data-p4seo');draw();var g=b.querySelector('[data-p4seo="'+k+'"]');g.focus();g.setSelectionRange(pos,pos);}});
    b.addEventListener('click',function(e){var x=e.target.closest('[data-p4kwx]');if(x){st.kw.splice(+x.getAttribute('data-p4kwx'),1);draw();return;}
      if(e.target.closest('[data-p4kwadd]')){var v=b.querySelector('[data-p4kw]').value.trim().toLowerCase();if(v&&st.kw.indexOf(v)<0)st.kw.push(v);draw();return;}
      if(e.target.closest('[data-p4next]')){st.chat++;draw();return;}if(e.target.closest('[data-p4lead]')){st.lead=true;draw();return;}
      var vv=e.target.closest('[data-p4v]');if(vv){st.vis[+vv.getAttribute('data-p4v')]=vv.getAttribute('data-p4do');draw();}});
    b.addEventListener('keydown',function(e){if(e.key==='Enter'&&e.target.matches('[data-p4kw]')){e.preventDefault();b.querySelector('[data-p4kwadd]').click();}});
    draw();})();

  /* --- 5 settings shape the site --- */
  (function(){var bx=document.querySelector('[data-p5box]');if(!bx)return;
    function draw(){var o={};bx.querySelectorAll('[data-p5]').forEach(function(i){o[i.getAttribute('data-p5')]=i.checked;});
      var menu=['Home','Products'];if(o.shop)menu.push('Shop');menu.push('Dealers');if(o.blog)menu.push('Blog');if(o.events)menu.push('Events');if(o.jobs)menu.push('Careers');menu.push('Contact us');
      var site='<div class="wb-mini"><div class="wb-mini-nav"><b>Kaveri<span>Fans</span></b><span class="wb-mini-m">'+menu.map(function(m){return '<span>'+m+'</span>';}).join('')+'</span><span class="wb-mini-r">'+
        (o.lang?'<span class="wb-lang">EN &#9662;</span>':'')+(o.b2b?'<span>Sign in</span>':'')+(o.shop?'<span>&#128722;</span>':'')+(o.appt?'<span class="is-btn">Book a demo</span>':'')+'</span></div>'+
        '<div class="wb-mini-hero"><b>Ceiling fans built for Indian summers</b>'+(o.shop?'<span class="is-btn">Shop fans</span>':'<span class="is-btn">Get a quote</span>')+'</div>'+
        '<div class="wb-mini-row">'+(o.shop?'<span class="wb-mini-card"><i></i>Aero 48<small>&#8377; 3,490'+(o.b2b?' &middot; dealer price after sign-in':'')+'</small></span><span class="wb-mini-card"><i></i>Breeze 36<small>&#8377; 2,790</small></span>':'<span class="wb-mini-card is-wide"><i></i>Product range<small>Enquire for prices</small></span>')+
        (o.events?'<span class="wb-mini-card is-ev"><i></i>Dealer meet<small>Nov 14 &middot; Coimbatore</small></span>':'')+(o.blog?'<span class="wb-mini-card is-blog"><i></i>Choosing a BLDC fan<small>Blog</small></span>':'')+'</div>'+
        (o.cookie?'<div class="wb-mini-cookie">We use cookies to improve your experience. <span>Accept</span></div>':'')+(o.chat?'<span class="wb-mini-chat">&#128172;</span>':'')+'</div>';
      bx.querySelector('[data-p5site]').innerHTML='<div class="wb-br"><div class="wb-br-bar"><i></i><i></i><i></i><span class="mono">kaverifans.in</span></div><div class="wb-br-body">'+site+'</div></div>';
      var n=Object.keys(o).filter(function(k){return o[k];}).length,type=o.shop?(o.b2b?'a store with a dealer portal':'an online store'):(o.b2b?'a lead-generation site with a dealer portal':'a lead-generation site');
      bx.querySelector('[data-p5note]').innerHTML='<b>'+n+' features on.</b> This is '+type+'. '+(o.lang?'Each page gets a translation, with its own URL per language. ':'')+'Every one of these is a setting, not custom code.';}
    bx.addEventListener('change',draw);draw();})();

  /* --- 6 website to apps --- */
  (function(){var bx=document.querySelector('[data-p6box]');if(!bx)return;var F=J('wb-flows'),fb=[].slice.call(bx.querySelectorAll('[data-p6]')),cur=0,timers=[];
    function run(){timers.forEach(clearTimeout);timers=[];bx.querySelectorAll('.wb-lane-b').forEach(function(l){l.innerHTML='';});bx.querySelectorAll('.wb-lane').forEach(function(l){l.classList.remove('is-hot');});
      var fast=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      F[cur][2].forEach(function(s,i){timers.push(setTimeout(function(){var lane=bx.querySelector('[data-p6lane="'+s[0]+'"]');lane.classList.add('is-hot');
        lane.querySelector('.wb-lane-b').insertAdjacentHTML('beforeend','<div class="wb-doc"><span class="wb-doc-n">'+(i+1)+'</span><b>'+s[2]+'</b><small>'+s[3]+'</small></div>');},fast?0:i*450));});}
    fb.forEach(function(b){b.addEventListener('click',function(){press(fb,b);cur=+b.getAttribute('data-p6');run();});});
    bx.querySelector('[data-p6run]').addEventListener('click',run);run();})();

  /* --- 7 quiz --- */
  (function(){var bx=document.querySelector('[data-p7box]');if(!bx)return;var R=J('wb-reqs'),ans={},L={cfg:'Configure',custom:'Customize',int:'Integrate'};
    bx.addEventListener('click',function(e){var b=e.target.closest('[data-p7a]');if(!b)return;var li=b.closest('[data-p7]'),i=+li.getAttribute('data-p7');if(ans[i]!==undefined)return;
      ans[i]=b.getAttribute('data-p7a');var ok=ans[i]===R[i][1];
      li.querySelectorAll('[data-p7a]').forEach(function(x){var k=x.getAttribute('data-p7a');x.disabled=true;x.classList.toggle('is-right',k===R[i][1]);x.classList.toggle('is-wrong',k===ans[i]&&!ok);});
      li.classList.add(ok?'is-ok':'is-no');li.querySelector('.wb-q-why').innerHTML=(ok?'&#10003; ':'Answer: <b>'+L[R[i][1]]+'</b>. ')+R[i][2];
      var n=Object.keys(ans).length,s=Object.keys(ans).filter(function(k){return ans[k]===R[k][1];}).length;bx.querySelector('[data-p7score]').textContent=s+' / '+R.length;
      bx.querySelector('[data-p7msg]').innerHTML=n<R.length?(R.length-n)+' left to answer.':(s>=6?'<b>Spot on.</b> You would scope this project the way we do.':'Three of seven are plain configuration, which surprises most people. That is money saved.');});})();

  /* --- 8 redirects --- */
  (function(){var bx=document.querySelector('[data-p8box]');if(!bx)return;var U=J('wb-urls'),pick={},go=bx.querySelector('[data-p8go]');
    function draw(){var left=0;bx.querySelector('[data-p8rows]').innerHTML=U.map(function(u,i){var to,stt;
        if(u[1]==='auto'){to='<span class="mono">'+u[2]+'</span>';stt='<span class="wb-b is-ok">Matched</span>';}
        else{var v=pick[i];if(!v)left++;to='<select data-p8="'+i+'" aria-label="New URL"><option value="">Choose&hellip;</option>'+u[2].map(function(o){return '<option'+(v===o?' selected':'')+'>'+o+'</option>';}).join('')+'</select>';
          stt=v?(v==='410 Gone'?'<span class="wb-b is-gone">410 Gone</span>':'<span class="wb-b is-ok">Mapped</span>'):'<span class="wb-b is-todo">To map</span>';}
        return '<tr><td class="mono">'+u[0]+'</td><td class="ox-muted">&rarr;</td><td>'+to+'</td><td>'+stt+'</td></tr>';}).join('');go.disabled=left>0;}
    bx.addEventListener('change',function(e){var s=e.target.closest('[data-p8]');if(s){pick[+s.getAttribute('data-p8')]=s.value;draw();bx.querySelector('[data-p8rw]').innerHTML='';}});
    go.addEventListener('click',function(){var rows=U.map(function(u,i){var to=u[1]==='auto'?u[2]:pick[i];return [u[0],to];}).filter(function(r){return r[0]!==r[1];});
      bx.querySelector('[data-p8rw]').innerHTML='<p class="wb-rw-h"><b>Website &rsaquo; Configuration &rsaquo; Rewrite</b><small>'+rows.length+' records created</small></p><table class="wb-rw-t"><thead><tr><th>Action</th><th>URL from</th><th>URL to</th></tr></thead><tbody>'+
        rows.map(function(r){return '<tr><td>'+(r[1]==='410 Gone'?'404 Not Found':'301 Moved permanently')+'</td><td class="mono">'+r[0]+'</td><td class="mono">'+(r[1]==='410 Gone'?'&mdash;':r[1])+'</td></tr>';}).join('')+'</tbody></table><p class="wb-rw-ok">Search engines follow the 301s to the new pages, so rankings carry over.</p>';});
    draw();})();

  /* --- 9 go-live --- */
  (function(){var bx=document.querySelector('[data-p9box]');if(!bx)return;var C=J('wb-checks'),pub=bx.querySelector('[data-p9pub]'),crit=C.filter(function(c){return c[2];}).length;
    function draw(){var add={perf:0,a11y:0,bp:0,seo:0},done=0;bx.querySelectorAll('[data-p9]').forEach(function(i){var c=C[+i.getAttribute('data-p9')];if(i.checked){if(c[3])add[c[3]]+=c[4];if(c[2])done++;}});
      bx.querySelectorAll('[data-p9ring]').forEach(function(r){var k=r.getAttribute('data-p9ring'),v=Math.min(100,+r.getAttribute('data-base')+add[k]),ring=r.querySelector('.wb-ring');ring.style.setProperty('--p',v);ring.querySelector('b').textContent=v;
        ring.className='wb-ring '+(v>=90?'is-good':(v>=50?'is-mid':'is-bad'));});
      bx.querySelector('[data-p9n]').textContent=done+' of '+crit;pub.disabled=done<crit;if(done<crit)bx.querySelector('[data-p9res]').innerHTML='';}
    bx.addEventListener('change',draw);pub.addEventListener('click',function(){bx.querySelector('[data-p9res]').innerHTML='<b>kaverifans.in is live.</b> Old URLs redirect, forms feed CRM and payments are on live keys.';});draw();})();

  /* --- 10 anatomy --- */
  (function(){var bx=document.querySelector('[data-p10box]');if(!bx)return;var B=J('wb-blocks'),bt=[].slice.call(bx.querySelectorAll('[data-p10]'));
    function draw(i){var b=B[i];bx.querySelector('[data-p10k]').innerHTML=b[0].toUpperCase();bx.querySelector('[data-p10k]').style.color=b[2];bx.querySelector('[data-p10n]').innerHTML=b[1];bx.querySelector('[data-p10t]').innerHTML=b[3];bx.querySelector('[data-p10a]').innerHTML=b[4];}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);draw(+b.getAttribute('data-p10'));});});draw(0);})();

  /* --- 11 team week --- */
  (function(){var bx=document.querySelector('[data-p11box]');if(!bx)return;var R=J('wb-roles'),bt=[].slice.call(bx.querySelectorAll('[data-p11]'));
    function draw(i){var t=R[i][2],m=t.reduce(function(a,x){return a+x[2];},0);
      bx.querySelector('[data-p11list]').innerHTML=t.map(function(x,j){return '<li style="--i:'+j+'"><label><input type="checkbox"><span class="wb-ck-box" aria-hidden="true">&#10003;</span><span><b>'+x[0]+'</b><small class="mono">'+x[1]+'</small></span></label><em>'+x[2]+' min</em></li>';}).join('');
      bx.querySelector('[data-p11sum]').innerHTML='<b>'+R[i][1]+':</b> about '+(m>=60?(Math.round(m/6)/10)+' hours':m+' minutes')+' a week, no developer needed.';}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);draw(+b.getAttribute('data-p11'));});});draw(0);})();

  /* --- 12 phases --- */
  (function(){var bx=document.querySelector('[data-p12box]');if(!bx)return;var P=J('wb-phases'),bt=[].slice.call(bx.querySelectorAll('[data-p12]'));
    function draw(i){bt.forEach(function(b,j){b.classList.toggle('is-done',j<i);});bx.querySelector('[data-p12d]').innerHTML=P[i][2].map(function(d,j){return '<li style="--i:'+j+'"><span class="wb-file" aria-hidden="true"></span>'+d+'</li>';}).join('');bx.querySelector('[data-p12y]').innerHTML=P[i][3];}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);draw(+b.getAttribute('data-p12'));});});draw(0);})();

  /* --- 13 scoping --- */
  (function(){var bx=document.querySelector('[data-p13box]');if(!bx)return;
    var PK=[['Business Website','Leads, content and SEO',['Website','CRM','Live Chat','Email Marketing']],['Website + Dealer Portal','Leads plus B2B ordering',['Website','CRM','Sales','Portal','Live Chat']],
            ['eCommerce Website','Sell online',['Website','eCommerce','Sales','Inventory','Accounting','Payments']],['Multi-site Website','Several brands or countries',['Website (multi-site)','eCommerce','Sales','Inventory','Accounting','Translations']]];
    function draw(){var v=function(k){return +bx.querySelector('[data-p13="'+k+'"]').value;},t=v('type'),pages=v('pages'),prods=v('prods'),langs=v('langs'),from=v('from'),x=0;
      bx.querySelectorAll('[data-p13x]:checked').forEach(function(){x++;});
      bx.querySelector('[data-p13o="pages"]').textContent=pages;bx.querySelector('[data-p13o="prods"]').textContent=num(prods);bx.querySelector('[data-p13o="langs"]').textContent=langs;
      if(prods>0&&t<2)t=t===1?1:2;
      var wk=4+Math.round(pages/30)+(t>=1?2:0)+(t>=2?2:0)+(t===3?3:0)+Math.round(prods/800)+(langs-1)*1+(from?1:0)+(from===2?1:0)+x*2,p=PK[t];
      var ask=['Your sitemap and the pages that bring enquiries today'];if(from)ask.push('Admin access to the current site and its analytics');if(prods)ask.push('Product data with prices, photos and stock');if(langs>1)ask.push('Who approves each translation');if(x)ask.push('API access for the services to connect');
      bx.querySelector('[data-p13out]').innerHTML='<div class="wb-pk"><p class="mono">RECOMMENDED</p><b>'+p[0]+'</b><small>'+p[1]+'</small><span class="wb-pk-wk">'+wk+'&ndash;'+(wk+2)+' weeks</span></div>'+
        '<div><p class="wb-gi-h">Apps</p><p class="wb-chips">'+p[2].map(function(a){return '<span>'+a+'</span>';}).join('')+'</p><p class="wb-gi-h">What we&rsquo;d ask you for</p><ul class="wb-ask">'+ask.map(function(a){return '<li>'+a+'</li>';}).join('')+'</ul></div>';}
    bx.addEventListener('input',draw);bx.addEventListener('change',draw);draw();})();
})();
</script>
'''
