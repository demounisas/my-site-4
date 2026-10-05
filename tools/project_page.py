"""
Odoo Project page (odoo-project.html). Every screen is modelled on the real Odoo 20
Project app (demo.odoo.com/odoo/project): the Projects kanban with status bubbles,
task stages (New, In Progress, Done, Cancelled), task states (In Progress, Changes
Requested, Approved, Done, Cancelled, Waiting), milestones, Blocked By dependencies,
the task form with Timesheets and Sub-tasks, project settings, the Gantt view and the
project profitability panel. Sample data is Indian; structure and wording follow Odoo.
Shared Odoo look: dist/assets/odoo-ui.css. Page styles: dist/assets/project.css.

hero(g) and build(g) get the build script's globals.
"""
import json

from crm_explorer import ic, SEARCH, V_KANBAN, V_LIST

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CROSS = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>'
CLOCK = ic('<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>', 18, 1.7)
FLAG = ic('<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>', 18, 1.7)
V_GANTT = ic('<path d="M4 6h9M8 12h10M6 18h7"/>', 16, 2.2)
MENUS = ["Projects", "Tasks", "Reporting", "Configuration"]


def inr(n, dec=False):
    """Indian-format rupees: 12,00,000"""
    whole = int(round(n))
    neg, digits = whole < 0, "%d" % abs(whole)
    rest, last3 = digits[:-3], digits[-3:]
    groups = []
    while len(rest) > 2:
        groups.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.insert(0, rest)
    out = ",".join(groups + [last3]) if groups else last3
    return ("-" if neg else "") + "&#8377; " + out + (".00" if dec else "")


def head(eyebrow, title, sub="", cls=""):
    return ('<div class="pj-head%s"><p class="pj-eyebrow mono">%s</p><h2 class="pj-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="pj-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="pj-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


def odoo_nav(app_icon, menus=MENUS):
    return ('<div class="ox-nav"><span class="ox-app">%s<b>Project</b></span>%s<span class="ox-nav-r"><span class="ox-company">Your Company</span>'
            '<span class="ox-av" style="--c:#4C9F70">M</span></span></div>' % (app_icon, "".join('<span class="ox-menu">%s</span>' % m for m in menus)))


def steps(items):
    return '<ol class="pj-steps">%s</ol>' % "".join('<li><span class="pj-step-n mono">%02d</span><div><h3>%s</h3><p>%s</p></div></li>' % (i + 1, t, x)
                                                     for i, (t, x) in enumerate(items))


# Odoo 20 project status bubbles (project.project.last_update_status)
STATUS = {"on_track": ("On Track", "#10AE51"), "at_risk": ("At Risk", "#F5A41A"), "off_track": ("Off Track", "#F04F4F"),
          "on_hold": ("On Hold", "#3E88D8"), "done": ("Complete", "#2B7A4B"), "to_define": ("Set Status", "#C3C9CF")}


def bubble(k):
    n, c = STATUS[k]
    return '<span class="pj-bub" style="--c:%s"><i></i>%s</span>' % (c, n)


# ------------------------------------------------------------------ data
# Today in every widget: Wed 14 Oct 2026 (day 9 counted from Mon 5 Oct).
PEOPLE = {"M": ["Meera Iyer", "Project Manager", "#4C9F70"], "A": ["Anita Rao", "Interior Designer", "#B5567E"],
          "R": ["Rahul Menon", "Site Engineer", "#3E7CB1"], "K": ["Karthik Raj", "Procurement", "#C98600"],
          "V": ["Vijay Kumar", "Electrician", "#6B5B95"]}

PROJECTS = [
    {"id": 1, "name": "Office Fit-out: Chennai HQ", "cust": "Shree Distributors", "pm": "M", "d": "Oct 5 &#10142; Nov 6", "st": "on_track", "fav": True, "tag": ["Fit-out", "green"], "ms": "Second Phase", "color": "#1F9E80"},
    {"id": 2, "name": "ERP Rollout", "cust": "Bluebay Retail", "pm": "R", "d": "Sep 14 &#10142; Dec 18", "st": "at_risk", "fav": True, "tag": ["Implementation", "sky"], "ms": "Data Migration", "color": "#3E7CB1"},
    {"id": 3, "name": "Website Redesign", "cust": "Sunrise Clinics", "pm": "A", "d": "Aug 24 &#10142; Oct 19", "st": "off_track", "fav": False, "tag": ["Design", "purple"], "ms": "Launch", "color": "#B5567E"},
    {"id": 4, "name": "Annual Maintenance", "cust": "Kaveri Foods", "pm": "K", "d": "Apr 1 &#10142; Mar 31", "st": "on_hold", "fav": False, "tag": ["Retainer", "yellow"], "ms": "", "color": "#C98600", "label": "Tickets"},
    {"id": 5, "name": "Research &amp; Development", "cust": "", "pm": "M", "d": "", "st": "done", "fav": False, "tag": ["Internal", "blue"], "ms": "", "color": ""},
    {"id": 6, "name": "Internal", "cust": "", "pm": "M", "d": "", "st": "to_define", "fav": False, "tag": None, "ms": "", "color": ""},
]

# tasks: p project, s stage, st state (ip cr ap dn cx wt), u assignees, dl deadline (day offset from Oct 5), al/sp hours,
# ms milestone, sub [closed, total], blk blocked by task id, tags [[name, colour]]
TASKS = [
    {"id": 11, "p": 1, "n": "Layout planning: cabins & meeting rooms", "s": "New", "st": "ip", "pri": 0, "u": ["A"], "tags": [["Design", "purple"]], "dl": 16, "al": 24, "sp": 0, "ms": "Second Phase"},
    {"id": 12, "p": 1, "n": "Furniture vendor coordination", "s": "New", "st": "ip", "pri": 0, "u": ["K"], "tags": [["External", "sky"], ["Interior", "green"]], "dl": None, "al": 12, "sp": 0, "ms": "Second Phase", "sub": [0, 3]},
    {"id": 13, "p": 1, "n": "Wrong paint colour in cabin 3!!", "s": "New", "st": "ip", "pri": 1, "u": ["R"], "tags": [["Bug", "red"]], "dl": 11, "al": 4, "sp": 0, "ms": ""},
    {"id": 14, "p": 1, "n": "Electrical & data cabling", "s": "In Progress", "st": "ap", "pri": 1, "u": ["R"], "tags": [["Site Work", "yellow"]], "dl": 14, "al": 64, "sp": 42.5, "ms": "Second Phase"},
    {"id": 15, "p": 1, "n": "Energy certificate", "s": "In Progress", "st": "ip", "pri": 1, "u": ["M"], "tags": [], "dl": 7, "al": 15, "sp": 22, "ms": "Second Phase", "act": "overdue"},
    {"id": 16, "p": 1, "n": "Black chairs for managers", "s": "In Progress", "st": "cr", "pri": 0, "u": ["K"], "tags": [["Interior", "green"]], "dl": 12, "al": 6, "sp": 5.25, "ms": "Second Phase"},
    {"id": 17, "p": 1, "n": "False ceiling & painting", "s": "In Progress", "st": "wt", "pri": 0, "u": ["R"], "tags": [["Site Work", "yellow"]], "dl": 21, "al": 56, "sp": 0, "ms": "Second Phase", "blk": 14},
    {"id": 18, "p": 1, "n": "Customer review", "s": "In Progress", "st": "ip", "pri": 0, "u": ["M", "A"], "tags": [], "dl": 18, "al": 8, "sp": 2, "ms": "Final Phase", "sub": [0, 1]},
    {"id": 19, "p": 1, "n": "Site survey & measurements", "s": "Done", "st": "dn", "pri": 0, "u": ["A"], "tags": [["Design", "purple"]], "dl": 2, "al": 16, "sp": 18, "ms": "First Phase"},
    {"id": 20, "p": 1, "n": "Layout approval from client", "s": "Done", "st": "dn", "pri": 0, "u": ["A"], "tags": [], "dl": 6, "al": 8, "sp": 6.5, "ms": "First Phase"},
    {"id": 21, "p": 1, "n": "Lunch room: kitchen", "s": "Done", "st": "dn", "pri": 0, "u": ["K"], "tags": [["Interior", "green"]], "dl": 8, "al": 32, "sp": 38, "ms": "First Phase"},
    {"id": 22, "p": 1, "n": "Reception signage", "s": "Cancelled", "st": "cx", "pri": 0, "u": ["A"], "tags": [], "dl": None, "al": 0, "sp": 0, "ms": ""},
    {"id": 31, "p": 2, "n": "Fit-gap workshop with store managers", "s": "Done", "st": "dn", "pri": 0, "u": ["R"], "tags": [], "dl": 1, "al": 12, "sp": 11, "ms": "Design"},
    {"id": 32, "p": 2, "n": "Import 4,200 products from Tally", "s": "In Progress", "st": "cr", "pri": 1, "u": ["R"], "tags": [["Data", "sky"]], "dl": 8, "al": 20, "sp": 26, "ms": "Data Migration", "act": "overdue"},
    {"id": 33, "p": 2, "n": "POS terminals for 40 stores", "s": "New", "st": "wt", "pri": 0, "u": ["K"], "tags": [], "dl": 24, "al": 30, "sp": 0, "ms": "Go-live", "blk": 32},
    {"id": 41, "p": 3, "n": "Doctor profile pages", "s": "In Progress", "st": "ip", "pri": 1, "u": ["A"], "tags": [["Design", "purple"]], "dl": 4, "al": 18, "sp": 24, "ms": "Launch", "act": "overdue"},
    {"id": 42, "p": 3, "n": "Appointment booking form", "s": "New", "st": "ip", "pri": 0, "u": ["A"], "tags": [], "dl": 12, "al": 10, "sp": 0, "ms": "Launch"},
    {"id": 51, "p": 4, "n": "Cold-room sensor not syncing", "s": "New", "st": "ip", "pri": 1, "u": ["K"], "tags": [["Bug", "red"]], "dl": 10, "al": 3, "sp": 1, "ms": ""},
    {"id": 52, "p": 4, "n": "Monthly preventive maintenance", "s": "In Progress", "st": "ap", "pri": 0, "u": ["K"], "tags": [["Recurring", "yellow"]], "dl": 26, "al": 6, "sp": 2, "ms": ""},
    {"id": 61, "p": 5, "n": "Evaluate acoustic panels", "s": "Done", "st": "dn", "pri": 0, "u": ["M"], "tags": [], "dl": None, "al": 8, "sp": 8, "ms": ""},
    {"id": 71, "p": 6, "n": "Internal training", "s": "New", "st": "ip", "pri": 0, "u": ["M"], "tags": [], "dl": None, "al": 0, "sp": 4, "ms": ""},
]

TIMESHEETS = {14: [["Oct 13", "R", "Conduit runs, floor 2", 6], ["Oct 12", "R", "Cabling cabins 1-6", 8], ["Oct 10", "V", "Switchboard prep", 4.5],
                   ["Oct 9", "R", "Floor 1 cabling", 7.5], ["Oct 8", "R", "Data points layout", 8], ["Oct 7", "R", "Site walk with contractor", 8.5]],
              15: [["Oct 12", "M", "Load calculation for TNEB", 4], ["Oct 9", "M", "Document collection", 6], ["Oct 8", "M", "Site inspection with consultant", 8],
                   ["Oct 6", "M", "Call with consultant", 4]]}


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">Project</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["Tasks, milestones &amp; dependencies", "Timesheets that become invoices", "Live status on every project"])
    copy = ('<div class="pj-hero-copy">%s<p class="pj-eyebrow mono">ODOO PROJECT IMPLEMENTATION</p>'
            '<h1 class="pj-h1">Project Management Software <span>That Plans, Tracks and Bills Your Work</span></h1>'
            '<p class="pj-lead">Unisas sets up Odoo Project around how your team delivers, so every project, task, deadline and billable hour sits in one '
            'system that is connected to your sales and accounts. Managers see what is late before the client does.</p><ul class="pj-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Discuss Odoo Project %s</a>'
            '<a href="#explore" class="btn btn-ghost">Try the project demo</a></div></div>' % (crumb, points, g["ARROW"]))
    # portfolio timeline: Oct 1 to Dec 31 (92 days), today Oct 14 (day 13)
    DAYS, NOW = 92, 13
    rows = [(PROJECTS[0], [("Design", 4, 8, "done"), ("Site work", 12, 22, "doing"), ("Handover", 34, 3, "todo")], [(11, "First Phase reached", True), (36, "Handover &middot; Nov 6", False)]),
            (PROJECTS[1], [("Configure", 0, 19, "done"), ("Data migration", 19, 27, "late"), ("Training", 46, 26, "todo")], [(78, "Go-live &middot; Dec 18", False)]),
            (PROJECTS[2], [("Content", 0, 12, "done"), ("Build", 10, 16, "late")], [(18, "Launch &middot; Oct 19", False)]),
            (PROJECTS[3], [], [(d, "Monthly maintenance visit", d < NOW) for d in (6, 37, 67)])]
    body = ""
    for pr, bars, ms in rows:
        track = "".join('<span class="pj-hx-bar is-%s" style="--s:%s;--l:%s"><em>%s</em></span>' % (st, s0, ln, lab) for lab, s0, ln, st in bars)
        track += "".join('<i class="pj-hx-ms%s%s" style="--s:%s" title="%s"></i>' % (" is-ok" if ok else "", " is-dot" if not bars else "", d, t) for d, t, ok in ms)
        body += ('<div class="pj-hx-row"><div class="pj-hx-lab"><b>%s</b><small>%s</small>%s</div><div class="pj-hx-track">%s</div></div>'
                 % (pr["name"], pr["cust"], bubble(pr["st"]), track))
    months = '<span style="--d:31">October</span><span style="--d:30">November</span><span style="--d:31">December</span>'
    vis = ('<div class="pj-hero-vis pj-hx" style="--n:%d" aria-label="Example project portfolio timeline"><div class="pj-hx-head"><div class="pj-hx-lab"><span class="pj-hx-app">%s<b>Project</b></span></div>'
           '<div class="pj-hx-months">%s</div></div><div class="pj-hx-body"><i class="pj-hx-now" style="--s:%d"><b>Today</b></i>%s</div>'
           '<p class="pj-hx-leg"><span class="is-done">Done</span><span class="is-doing">In progress</span><span class="is-late">Running late</span><span class="is-todo">Planned</span><span class="is-ms">Milestone</span></p></div>'
           % (DAYS, g["TILE_ICONS"][5], months, NOW, body))
    return '<section class="pj-hero mp-hero--dark-center">%s%s</section>' % (copy, vis)


# ------------------------------------------------------------------ sections
def build(g):
    out = ""
    app_icon = g["TILE_ICONS"][5]

    # 1 ---- the problem: the spreadsheet tracker
    signs = ["Plans live in a spreadsheet that is out of date by Tuesday", "Nobody knows which task is holding up the next one",
             "Status meetings exist only to find out where things stand", "Hours are logged on paper, or not at all",
             "Invoices go out late because nobody knows what can be billed"]
    rows = [("Electrical cabling", "Rahul", "WIP??", "12-Oct", "ask Rahul", "is-bad"), ("False ceiling", "contractor", "Not started", "", "waiting on cabling?", ""),
            ("Black chairs", "Karthik", "Done", "09-Oct", "client wants changes", "is-bad"), ("Energy certificate", "Meera", "In progress", "07-Oct", "", "is-late"),
            ("Layout approval", "Anita", "DONE", "06-Oct", "pls confirm with client", ""), ("Hours - Oct", "everyone", "", "", "see WhatsApp", "is-bad")]
    sheet = "".join('<tr class="%s"><td>%d</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (c, i + 2, a, b, s, d, n) for i, (a, b, s, d, n, c) in enumerate(rows))
    out += sec('<div class="pj-ready"><div>%s<ul class="pj-signs">%s</ul><p class="pj-note">Each gap is small. Together they mean slipped deadlines, unbilled hours '
               'and clients who hear about a delay last.</p></div>'
               '<div class="pj-xl" aria-label="Example project tracker spreadsheet"><div class="pj-xl-bar"><span class="pj-xl-ic">X</span><b>Project_Tracker_FINAL_v7 (2).xlsx</b><span class="pj-xl-warn">Read-only: Meera is editing</span></div>'
               '<div class="pj-xl-fx"><span>F4</span><i>fx</i><span>=IF(D4="","ask Rahul",D4)</span></div><div class="ox-scroll"><table class="pj-xl-t"><thead><tr><th></th><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th></tr>'
               '<tr class="pj-xl-h"><td>1</td><td>Task</td><td>Owner</td><td>Status</td><td>Due</td><td>Notes</td></tr></thead><tbody>%s</tbody></table></div>'
               '<div class="pj-xl-tabs"><span class="is-on">Oct plan</span><span>Oct plan (old)</span><span>Hours</span><span>Sheet3</span></div></div></div>'
               % (head("THE COST OF MANAGING PROJECTS BY HAND", "Is Your Project Delivery Process Difficult to Plan, Track or Bill?",
                       "Most teams run projects on spreadsheets, chat groups and memory. It works for two projects. At ten, it looks like this."),
                  "".join('<li>%s%s</li>' % (CROSS, s) for s in signs), sheet), "pj-sec--ready")

    # 2 ---- one workflow: the project explorer
    menu = "".join('<button type="button" class="pj-menu%s" data-pe-menu="%s" aria-pressed="%s">%s</button>' % (" is-on" if k == "projects" else "", k, "true" if k == "projects" else "false", n)
                   for k, n in [("projects", "Projects"), ("mine", "My Tasks")])
    views = [("kanban", "Kanban", V_KANBAN), ("list", "List", V_LIST)]
    switch = "".join('<button type="button" class="ox-vbtn%s" data-pe-view="%s" aria-label="%s view" title="%s" aria-pressed="%s">%s</button>'
                     % (" is-on" if k == "kanban" else "", k, n, n, "true" if k == "kanban" else "false", svg) for k, n, svg in views)
    feats = [("Projects", "Every client job or internal initiative, with its manager, dates, status and favourites."),
             ("Tasks &amp; stages", "Stages you define, with tasks dragged from New to Done as work moves."),
             ("Task states", "In Progress, Changes Requested, Approved or Waiting, so the board shows what needs attention."),
             ("Time on every task", "Allocated against spent hours, logged straight into the task's Timesheets tab.")]
    out += sec(head("ONE WORKFLOW", "How Can Odoo Bring Projects, Tasks and Teams Into One Workflow?",
                    "This is the Odoo Project app as your team will use it. Open <b>Office Fit-out: Chennai HQ</b>, drag a task to another stage, "
                    "change its state, or open it and log time.", "is-center")
               + '<div class="ox pj-ox pj-pe" data-pe><div class="ox-nav"><span class="ox-app">%s<b>Project</b></span><span class="pj-menus" role="group" aria-label="Project menu">%s</span>'
                 '<span class="ox-menu">Reporting</span><span class="ox-nav-r"><span class="ox-company">Your Company</span><span class="ox-av" style="--c:#4C9F70">M</span></span></div>'
                 '<div class="ox-cp"><div class="ox-cp-l"><button type="button" class="ox-new" data-pe-new>New</button><span class="ox-crumb ox-crumb--stack" data-pe-crumb>Projects</span></div>'
                 '<label class="ox-search">%s<input type="search" placeholder="Search..." aria-label="Search projects and tasks" data-pe-q></label>'
                 '<div class="ox-views" data-pe-views>%s</div></div><div class="ox-body pj-pe-body" data-pe-body></div></div>'
                 '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview with sample data. Open a project, drag tasks between stages, or click a task&rsquo;s state icon.</p>'
                 % (app_icon, menu, SEARCH, switch)
               + '<ul class="pj-feats">%s</ul>' % "".join('<li><b>%s</b><span>%s</span></li>' % f for f in feats), "pj-sec--explore", "explore")

    # 3 ---- configure around your delivery process: project settings
    impl = [("Map how you deliver", "Phases, hand-offs, approvals and who bills what, taken from how your team works today."),
            ("Turn it into Odoo settings", "Stages, milestones, dependencies, visibility and billing set per project or template."),
            ("Build project templates", "Repeat work starts from a template with its stages, tasks and milestones already in place."),
            ("Prove it on a live project", "Your managers run a current project through the setup before go-live.")]

    def toggle(key, name, desc, on):
        return ('<label class="pj-set"><input type="checkbox" data-set="%s"%s><span class="pj-chk" aria-hidden="true">%s</span><span><b>%s</b><small>%s</small></span></label>'
                % (key, " checked" if on else "", TICK, name, desc))
    vis = ('<div class="pj-set is-static"><span class="pj-chk is-blank" aria-hidden="true"></span><span><b>Visibility</b><small>Who can see this project and its tasks</small>'
           '<span class="pj-radio">%s</span></span></div>' % "".join('<label><input type="radio" name="pj-vis" value="%s" data-set-vis%s> %s</label>' % (v, " checked" if v == "portal" else "", n)
                                                                     for v, n in [("private", "Invited internal users (private)"), ("internal", "All internal users"),
                                                                                  ("portal", "Invited portal users and all internal users (public)")]))
    blocks = [("Tasks Management", toggle("ms", "Milestones", "Track major progress points that must be reached", True)
               + toggle("dep", "Task Dependencies", "Determine the order in which to perform tasks", True)
               + toggle("rec", "Recurring Tasks", "Auto-generate tasks for regular activities", False)
               + toggle("rate", "Customer Ratings", "Get customer feedback on the work done", False)),
              ("Time Management", toggle("ts", "Timesheets", "Log time on tasks", True)
               + toggle("bill", "Billable", "Invoice your time and material to customers", True)),
              ("Visibility", vis)]
    sets = "".join('<div class="pj-set-group"><h4>%s</h4><div class="pj-set-grid">%s</div></div>' % b for b in blocks)
    out += sec('<div class="pj-cfg"><div>%s%s</div><div><div class="ox pj-ox pj-settings" data-settings>%s'
               '<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Projects</a><span>Office Fit-out: Chennai HQ</span></span></div></div>'
               '<div class="pj-set-tabs"><span>Description</span><span class="is-on">Settings</span></div><div class="pj-set-body">%s</div></div>'
               '<div class="pj-effect ox-solo"><p class="pj-effect-h">What your team and client will see</p><ul data-set-out aria-live="polite"></ul></div></div></div>'
               % (head("CONFIGURED AROUND YOUR DELIVERY", "How Does Unisas Configure Odoo Project Around Your Delivery Process?",
                       "We start from how your projects really run, then set Odoo's own project settings to match. Change a setting on the right to see what it does."),
                  steps(impl), odoo_nav(app_icon), sets), "pj-sec--cfg")

    # 4 ---- milestones and dependencies
    out += sec(head("TASKS, MILESTONES &amp; DEPENDENCIES", "What Can You Manage With Odoo Projects, Tasks, Milestones and Dependencies?",
                    "Tasks wait for the work they depend on, and milestones are reached when their tasks are done. Mark the next task as done and watch the chain move.", "is-center")
               + '<div class="pj-dep" data-dep><div class="ox pj-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Office Fit-out: Chennai HQ</a><span>Tasks by dependency</span></span></div>'
                 '<span></span><button type="button" class="ox-sbtn pj-dep-reset" data-dep-reset>Reset</button></div><ol class="pj-chain" data-dep-chain aria-live="polite"></ol></div>'
                 '<div class="pj-dep-side"><div class="ox pj-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb">Milestones</span></div></div>'
                 '<div class="ox-scroll"><table class="ox-table pj-ms-t"><thead><tr><th>Name</th><th>Deadline</th><th class="ox-num">Tasks</th><th>Reached</th></tr></thead><tbody data-dep-ms></tbody></table></div></div>'
                 '<ul class="pj-mini">'
                 '<li><b>Sub-tasks</b><span>Split a task into smaller ones with their own assignee and deadline. <i>Furniture vendor coordination &middot; 0/3</i></span></li>'
                 '<li><b>Recurring tasks</b><span>Monthly maintenance or GST filings are created on schedule. <i>Repeat every 1 month</i></span></li>'
                 '<li><b>Activities</b><span>Calls and to-dos on a task, with reminders when they fall due.</span></li></ul></div></div>', "pj-sec--dep")

    # 5 ---- timesheets, sales and accounting
    out += sec(head("CONNECTED TO SALES &amp; ACCOUNTING", "How Does Unisas Connect Project Management With Timesheets, Sales and Accounting?",
                    "A confirmed sales order creates the project. Hours logged on tasks become billable, the invoice is drafted from them, and the project's profitability updates as you go. "
                    "Log some work and invoice it.", "is-center")
               + '<div class="pj-bill" data-bill><div class="ox pj-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Sales Orders</a><span>S00482</span></span></div>'
                 '<span></span><span class="ox-sbar is-mini pj-bill-sb"><span class="ox-sb">Quotation</span><span class="ox-sb">Quotation Sent</span><span class="ox-sb is-cur">Sales Order</span></span></div>'
                 '<div class="pj-bill-btns"><button type="button" class="ox-pbtn" data-bill-do="log">Log 8 hours on a task</button><button type="button" class="ox-sbtn" data-bill-do="inv">Create Invoice</button>'
                 '<button type="button" class="ox-sbtn pj-bill-reset" data-bill-do="reset">Reset</button></div>'
                 '<div class="pj-bill-sheet"><div class="pj-smarts" data-bill-smart></div><p class="pj-doc-kind">Sales Order</p><h3>S00482</h3>'
                 '<dl class="ox-fields"><div><dt>Customer</dt><dd>Shree Distributors</dd></div><div><dt>Project</dt><dd><span class="pj-link">Office Fit-out: Chennai HQ</span></dd></div>'
                 '<div><dt>Invoice Status</dt><dd data-bill-is></dd></div><div><dt>Payment Terms</dt><dd>15 Days</dd></div></dl>'
                 '<div class="ox-ftabs"><span class="is-on">Order Lines</span><span>Other Info</span></div>'
                 '<div class="ox-scroll"><table class="pj-lines"><thead><tr><th>Product</th><th class="ox-num">Quantity</th><th class="ox-num">Delivered</th><th class="ox-num">Invoiced</th><th class="ox-num">Unit Price</th><th class="ox-num">Amount</th></tr></thead>'
                 '<tbody data-bill-lines></tbody></table></div></div></div>'
                 '<div class="pj-prof ox-solo"><p class="pj-prof-h"><b>Profitability</b><small>Office Fit-out: Chennai HQ</small></p><div class="ox-scroll"><table class="pj-prof-t" data-bill-prof></table></div>'
                 '<ol class="pj-bill-apps" aria-live="polite">'
                 '<li data-bill-app="sales" style="--c:#EE8A3C"><b>Sales</b><span data-bill-txt></span></li>'
                 '<li data-bill-app="ts" style="--c:#1F9E80"><b>Timesheets</b><span data-bill-txt></span></li>'
                 '<li data-bill-app="acc" style="--c:#8E4F83"><b>Accounting</b><span data-bill-txt></span></li></ol></div></div>', "pj-sec--bill")

    # 6 ---- planning: Gantt + project update
    out += sec(head("PLANNING &amp; PROGRESS", "Can Odoo Help You Plan Resources, Deadlines and Project Progress?",
                    "The Gantt view plans tasks against people and dates. When a task slips, the tasks that depend on it move with it, and the project's status tells you whether the deadline is still safe. "
                    "Try delaying the cabling, then add an electrician.", "is-center")
               + '<div class="pj-plan" data-plan><div class="pj-plan-ctl"><button type="button" class="ox-sbtn" data-plan-do="delay" aria-pressed="false">Delay cabling by 4 days</button>'
                 '<button type="button" class="ox-sbtn" data-plan-do="crew" aria-pressed="false">Add a second electrician</button><button type="button" class="ox-sbtn" data-plan-do="reset">Reset</button></div>'
                 '<div class="pj-plan-grid"><div class="ox pj-ox ox-gt pj-gt" style="--n:35">%s'
                 '<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Office Fit-out: Chennai HQ</a><span>Tasks</span></span></div><span></span>'
                 '<div class="ox-views"><span class="ox-vbtn">%s</span><span class="ox-vbtn">%s</span><span class="ox-vbtn is-on">%s</span></div></div>'
                 '<div class="ox-scroll"><div class="ox-gt-grid pj-gt-grid" data-plan-gantt></div></div></div>'
                 '<aside class="pj-upd ox-solo" aria-live="polite"><p class="pj-upd-h"><small>Project Update</small><b>Weekly review &middot; Oct 14</b></p>'
                 '<p class="pj-upd-st" data-plan-st></p><div class="pj-upd-prog"><span>Progress</span><i><b data-plan-bar></b></i><em data-plan-pct></em></div>'
                 '<dl class="pj-upd-dl"><div><dt>Handover</dt><dd data-plan-end></dd></div><div><dt>Deadline</dt><dd>Nov 6</dd></div><div><dt>Rahul\'s load</dt><dd data-plan-load></dd></div></dl>'
                 '<p class="pj-upd-txt" data-plan-txt></p></aside></div></div>'
               % (odoo_nav(app_icon), V_KANBAN, V_LIST, V_GANTT), "pj-sec--plan")

    # 7 ---- data, roles, customization
    roles = [("pm", "Project Manager", "Project: Administrator", "All projects, the Gantt plan and profitability",
              ["Create projects from templates", "Set stages, milestones and deadlines", "Post project updates", "See margins per project"], ["Validate invoices (Accounts does)"]),
             ("tm", "Team Member", "Project: User", "My Tasks, sorted by deadline",
              ["Move their tasks between stages", "Log time from web or mobile", "Comment and @mention colleagues"], ["See other teams' private projects", "See rates or margins"]),
             ("cl", "Client", "Portal user, project shared with Edit", "The client portal: their project only",
              ["See task progress and documents", "Approve work or request changes", "Comment on a task by email or portal"], ["See internal notes or hours cost", "See other clients"]),
             ("ac", "Accounts", "Invoicing: Billing", "Sales orders ready to invoice",
              ["Invoice timesheets and milestones", "Check delivered against invoiced hours"], ["Edit tasks or plans"])]
    rtabs = "".join('<button type="button" class="pj-role%s" data-role="%d" aria-pressed="%s"><b>%s</b><small>%s</small></button>'
                    % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", r[1], r[2]) for i, r in enumerate(roles))
    reqs = [("Stages and milestones per project type", "cfg"), ("Clients approve work in the portal", "cfg"), ("Project templates for repeat jobs", "cfg"),
            ("Extra fields: site address, PO number, region", "studio"), ("Your own task report and client status PDF", "studio"),
            ("Stage gate: no handover until the checklist is complete", "custom"), ("Sync tasks with a client's Jira", "custom")]
    lab = {"cfg": "Configuration", "studio": "Studio", "custom": "Customization"}
    out += sec(head("DATA, ROLES &amp; CUSTOMIZATION", "How Does Unisas Handle Project Data, Roles and Workflow Customization?",
                    "Each person sees what their role needs and nothing more. We configure first, use Odoo Studio for light changes, and write code only when the process truly needs it.", "is-center")
               + '<div class="pj-roles" data-roles><div class="pj-role-tabs" role="group" aria-label="Roles">%s</div><div class="pj-role-card ox-solo" aria-live="polite" data-role-card></div>'
                 '<div class="pj-reqs ox-solo"><p class="pj-effect-h">Typical requests and how we meet them</p><ul>%s</ul></div></div>'
                 '<script type="application/json" id="pj-roles">%s</script>'
               % (rtabs, "".join('<li><span>%s</span><i class="pj-tag pj-tag--%s">%s</i></li>' % (t, k, lab[k]) for t, k in reqs), json.dumps(roles)), "pj-sec--roles")

    # 8 ---- connected apps
    apps = [("Timesheets", "#1F9E80", "Hours logged on tasks from web, mobile or a running timer, approved by managers.", "Rahul logs 3:30 on cabling; it shows on the task, the SO and the margin."),
            ("Planning", "#E4402E", "Shifts and roles planned across projects, so nobody is booked twice.", "Vijay is planned Oct 12-16 on Chennai HQ, 8 hours a day."),
            ("Sales", "#EE8A3C", "A confirmed order creates the project and its tasks from a template.", "S00482 confirmed: project and 11 tasks created."),
            ("Accounting", "#8E4F83", "Invoices from timesheets or milestones, and real costs per project.", "INV/2026/0412 drafted for 40 hours at &#8377; 2,500."),
            ("Purchase", "#264E86", "Materials bought for a project are costed to it.", "PO for 24 chairs charged to Chennai HQ."),
            ("Expenses", "#C98600", "Travel and site expenses re-invoiced to the client at cost.", "Site visit taxi, &#8377; 640, added to the next invoice."),
            ("Helpdesk", "#5AA7E8", "Support tickets after handover, with time billed on the AMC.", "Ticket #212: AC not cooling, under the retainer."),
            ("Field Service", "#B5567E", "On-site jobs with worksheets, signatures and route planning.", "Installation report signed on the technician's phone."),
            ("Documents", "#3E7CB1", "Drawings, approvals and site photos filed per project.", "Layout_v3.pdf shared with the client to sign."),
            ("Spreadsheet", "#10AE51", "Live dashboards built on project data, no exports.", "Utilisation by person for October."),
            ("Sign", "#714B67", "Scope and handover documents signed electronically.", "Handover certificate signed by Shree Distributors."),
            ("Discuss", "#017E84", "Chat and mentions on every task, in one place with email.", "@Karthik: chairs arrive Thursday?")]
    abtn = "".join('<button type="button" class="pj-app%s" data-app="%d" aria-pressed="%s" style="--c:%s"><i>%s</i>%s</button>'
                   % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", c, n[0], n) for i, (n, c, x, e) in enumerate(apps))
    out += sec('<div class="pj-apps-wrap"><div>%s<div class="pj-apps" role="group" aria-label="Odoo apps">%s</div></div>'
               '<div class="pj-app-card ox-solo" aria-live="polite" data-app-card><span class="pj-app-core">%s<b>Project</b></span><span class="pj-app-link"></span>'
               '<span class="pj-app-to" data-app-to></span><p data-app-what></p><p class="pj-app-ex" data-app-ex></p></div></div>'
               '<script type="application/json" id="pj-apps">%s</script>'
               % (head("CONNECTED APPS", "Which Odoo Applications Can Be Connected to Your Project Workflow?",
                       "Odoo Project shares one database with the rest of Odoo, so there is nothing to sync. Pick an app to see what it adds to a project."),
                  abtn, app_icon, json.dumps(apps)), "pj-sec--apps")

    # 9 ---- migration, testing, training
    sources = {"Excel": [["Task", "Title"], ["Project", "Project"], ["Owner", "Assignees"], ["Status", "Stage"], ["Due", "Deadline"], ["Est. hrs", "Allocated Time"], ["Notes", "Description"]],
               "Asana": [["Name", "Title"], ["Projects", "Project"], ["Assignee", "Assignees"], ["Section/Column", "Stage"], ["Due Date", "Deadline"], ["Parent task", "Parent Task"], ["Tags", "Tags"]],
               "Trello": [["Card Name", "Title"], ["Board Name", "Project"], ["Members", "Assignees"], ["List Name", "Stage"], ["Due Date", "Deadline"], ["Labels", "Tags"], ["Card Description", "Description"]],
               "MS Project": [["Task Name", "Title"], ["Resource Names", "Assignees"], ["Start", "Planned Date"], ["Finish", "Deadline"], ["Work", "Allocated Time"], ["Predecessors", "Blocked By"], ["Milestone", "Milestone"]],
               "Jira": [["Summary", "Title"], ["Project name", "Project"], ["Assignee", "Assignees"], ["Status", "Stage"], ["Due date", "Deadline"], ["Original Estimate", "Allocated Time"], ["Issue links", "Blocked By"]]}
    src_btn = "".join('<button type="button" class="pj-src%s" data-src="%s" aria-pressed="%s">%s</button>' % (" is-on" if i == 0 else "", k, "true" if i == 0 else "false", k)
                      for i, k in enumerate(sources))
    uat = [("Project managers", [("Create a project from the fit-out template", True), ("Reschedule the Gantt after a delay", True), ("Post a weekly project update", False)]),
           ("Team", [("Log time from the mobile app", True), ("Move a task and request changes", False)]),
           ("Client", [("Approve a task in the portal", False)]),
           ("Accounts", [("Invoice timesheets from S00482", False)])]
    ul = ""
    for role, items in uat:
        ul += '<li class="pj-uat-role">%s</li>' % role
        ul += "".join('<li><label class="pj-uat-i"><input type="checkbox" data-uat%s><span class="pj-chk" aria-hidden="true">%s</span><span>%s</span></label></li>' % (" checked" if on else "", TICK, t)
                      for t, on in items)
    mig = [("Extract", "Open projects, tasks, hours and contacts from Excel, Asana, Trello, MS Project or Jira."),
           ("Map &amp; clean", "Statuses mapped to stages, owners to users, closed work archived."),
           ("Trial import", "A test load your managers check against the old tool."),
           ("Train by role", "Managers, team, accounts and clients each learn only their screens.")]
    out += sec(head("MIGRATION, TESTING &amp; TRAINING", "How Does Unisas Manage Data Migration, Testing and User Training?",
                    "Your live projects come across with their tasks, owners, dates and logged hours. Each role then tests its own scenarios before go-live. Pick where your projects live today.", "is-center")
               + '<div class="pj-mig">%s<div class="ox pj-ox pj-imp" data-imp><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Tasks</a><span>Import a File</span></span></div></div>'
                 '<div class="pj-imp-body"><div class="pj-srcs" role="group" aria-label="Source">%s</div><p class="pj-imp-file" data-imp-file></p>'
                 '<div class="ox-scroll"><table class="ox-table pj-imp-t"><thead><tr><th>File Column</th><th></th><th>Odoo Field</th></tr></thead><tbody data-imp-rows></tbody></table></div>'
                 '<div class="pj-imp-btns"><button type="button" class="ox-sbtn" data-imp-do="test">Test</button><button type="button" class="ox-pbtn" data-imp-do="go">Import</button></div>'
                 '<p class="pj-imp-res" data-imp-res role="status" aria-live="polite"></p></div></div>'
                 '<div class="pj-uat ox-solo" data-uatbox><div class="pj-uat-h"><span><small>User acceptance testing</small><b>Go-live readiness</b></span><span class="pj-uat-pct" data-uat-pct></span></div>'
                 '<div class="pj-uat-bar"><i data-uat-bar></i></div><ul>%s</ul><p class="pj-uat-res" data-uat-res aria-live="polite"></p></div></div>'
                 '<script type="application/json" id="pj-src">%s</script>' % (steps(mig), src_btn, ul, json.dumps(sources)), "pj-sec--mig")

    # 10 ---- what's included: the implementation as an Odoo project
    scope = [("First Phase: Discover &amp; design", ["Workshops on how you deliver and bill", "Stages, milestones and project templates designed", "Roles, visibility and portal access agreed"]),
             ("Second Phase: Configure &amp; connect", ["Odoo Project, Timesheets and Planning configured", "Sales order to project and invoicing set up", "Open projects, tasks and hours migrated"]),
             ("Final Phase: Test, train &amp; go live", ["User testing with each role", "Training for managers, team, accounts and clients", "Go-live and hypercare through the first billing cycle"])]
    body = ""
    for title, items in scope:
        body += '<li class="pj-sc-ms"><span class="pj-sc-flag">%s</span><b>%s</b><span class="pj-sc-n">%d tasks</span></li>' % (FLAG, title, len(items))
        body += "".join('<li class="pj-sc-t"><span class="pj-incl">%s</span><span>%s</span><span class="pj-st-ic is-ap" title="Included"></span></li>' % (TICK, t) for t in items)
    out += sec('<div class="pj-scope">%s<div class="ox pj-ox"><div class="ox-cp"><div class="ox-cp-l"><a href="#get-demo" class="ox-new pj-ox-link" data-svc-cta="implementation">Get a scoped quote</a>'
               '<span class="ox-crumb ox-crumb--stack"><a>Projects</a><span>Odoo Project Implementation</span></span></div><span></span>%s</div>'
               '<div class="pj-scope-sheet"><dl class="ox-fields"><div><dt>Customer</dt><dd>Your Company</dd></div><div><dt>Project Manager</dt><dd>Unisas consultant</dd></div>'
               '<div><dt>Pricing</dt><dd>Fixed scope, agreed up front</dd></div><div><dt>Typical length</dt><dd>4 to 8 weeks</dd></div></dl>'
               '<div class="ox-ftabs"><span class="is-on">Milestones &amp; tasks</span><span>Settings</span></div><ul class="pj-sc-list">%s</ul></div></div></div>'
               % (head("WHAT'S INCLUDED", "What Does an Odoo Project Implementation With Unisas Include?",
                       "Our standard scope, written the way we run it: as an Odoo project with three milestones.", "is-center"), bubble("on_track"), body), "pj-sec--scope")

    # 11 ---- business processes
    procs = [("agency", "Client projects &amp; agencies", ["Brief", "Design", "Client Review", "Revisions", "Delivered"], "Fixed price by milestone",
              ["Clients approve work in the portal", "Change requests tracked as tasks", "Retainer hours billed monthly"], ["Project", "Timesheets", "Sales", "Sign"]),
             ("fitout", "Construction &amp; fit-out", ["Survey", "Design Sign-off", "Procurement", "Site Work", "Snag List", "Handover"], "Milestone payments (advance, stage, retention)",
              ["Material POs costed to the job", "Site photos and drawings per task", "Dependencies between trades"], ["Project", "Purchase", "Documents", "Field Service"]),
             ("it", "IT &amp; software services", ["Backlog", "Sprint", "In Review", "QA", "Released"], "Time &amp; materials from timesheets",
              ["Sprints as milestones", "Bugs and requests from Helpdesk", "Hours per developer per client"], ["Project", "Timesheets", "Helpdesk", "Knowledge"]),
             ("consult", "Consulting, audit &amp; compliance", ["Engagement Letter", "Fieldwork", "Review", "Report", "Closed"], "Fixed fee or monthly retainer",
              ["Recurring tasks for GST and ROC filings", "Partner review before release", "Budget against actual hours"], ["Project", "Timesheets", "Documents", "Sign"]),
             ("eng", "Engineering &amp; installation", ["Design", "Fabrication", "Dispatch", "Installation", "Commissioning"], "Milestones linked to delivery",
              ["Manufacturing orders linked to the project", "Installation with on-site worksheets", "AMC after commissioning"], ["Project", "Manufacturing", "Inventory", "Field Service"]),
             ("internal", "Internal &amp; marketing projects", ["To Do", "Doing", "Blocked", "Done"], "Not billed; cost tracked",
              ["Campaign and event plans with deadlines", "Department budgets against hours", "Shared knowledge base"], ["Project", "Marketing", "Knowledge", "Spreadsheet"])]
    tabs = "".join('<button type="button" role="tab" class="pj-tab" id="pj-tab-%s" aria-controls="pj-panel-%s" aria-selected="%s"%s>%s</button>'
                   % (k, k, "true" if i == 0 else "false", "" if i == 0 else ' tabindex="-1"', n) for i, (k, n, *_r) in enumerate(procs))
    panels = "".join('<div class="pj-panel" role="tabpanel" id="pj-panel-%s" aria-labelledby="pj-tab-%s"%s><div class="pj-pstages ox-solo">%s</div>'
                     '<div class="pj-panel-body"><div><p class="pj-eyebrow mono">HOW IT RUNS IN ODOO</p><h3>%s</h3><ul>%s</ul></div>'
                     '<div class="pj-panel-meta"><p><small>Billing</small><b>%s</b></p><p><small>Apps</small><span class="pj-mods">%s</span></p></div></div></div>'
                     % (k, k, "" if i == 0 else " hidden", "".join('<span><b>%s</b><i></i></span>' % s for s in st), n,
                        "".join("<li>%s%s</li>" % (TICK, p) for p in pts), bill, "".join("<span>%s</span>" % m for m in mods))
                     for i, (k, n, st, bill, pts, mods) in enumerate(procs))
    out += sec(head("PROCESSES IT SUPPORTS", "What Business Processes Can Odoo Project Support?",
                    "Any work that has steps, people and deadlines. Each process gets its own stages and billing. Pick one to see the stages we usually set up.")
               + '<div class="pj-ind"><div class="pj-tabs" role="tablist" aria-label="Business processes">%s</div><div class="pj-panels">%s</div></div>'
                 '<p class="pj-more">Run something else? <a href="#get-demo">Tell us how your projects move</a> and we&rsquo;ll map it to Odoo.</p>' % (tabs, panels),
               "pj-sec--ind")

    # 12 ---- discovery to go-live
    phases = [("Discover", "Week 1", ["Workshops with managers, team leads and accounts", "Current projects, tools and billing reviewed", "Pain points ranked by cost"], "Process map and scope", "Signed scope and plan"),
              ("Design", "Week 2", ["Stages, milestones and templates per project type", "Roles, visibility and portal access", "Billing rules: fixed, milestone or timesheets"], "Solution design document", "Design sign-off"),
              ("Configure", "Weeks 3-4", ["Project, Timesheets and Planning set up on a test copy", "Sales order to project to invoice flow", "Reports and dashboards"], "Working test database", "Demo on your own projects"),
              ("Migrate", "Weeks 4-5", ["Open projects, tasks and hours imported", "Customers and contacts de-duplicated", "Trial load checked by managers"], "Migrated test data", "Data sign-off"),
              ("Test &amp; Train", "Weeks 5-6", ["User testing by every role", "Role-based training with short guides", "Fixes and final adjustments"], "UAT checklist complete", "Go-live approval"),
              ("Go live &amp; Hypercare", "Weeks 6-8", ["Switch-over on a weekend", "Consultants on call for the first weeks", "First invoices from timesheets checked together"], "Live system", "Handover")]
    pbar = "".join('<button type="button" class="ox-sb%s" data-ph="%d" aria-pressed="%s">%s</button>' % (" is-cur" if i == 0 else "", i, "true" if i == 0 else "false", p[0]) for i, p in enumerate(phases))
    out += sec(head("FROM DISCOVERY TO GO-LIVE", "How Does an Odoo Project Implementation Move From Discovery to Go-Live?",
                    "Six phases, each ending with something you sign off. We run it in Odoo Project too, so you can follow progress in the portal. Step through the phases.", "is-center")
               + '<div class="pj-phase" data-phase><div class="pj-ph-bar"><span class="ox-sbar pj-ph-sbar" role="group" aria-label="Phases">%s</span></div>'
                 '<div class="pj-ph-card" aria-live="polite"><div class="pj-ph-l"><p class="pj-ph-when mono" data-ph-when></p><h3 data-ph-name></h3><ul data-ph-do></ul></div>'
                 '<div class="pj-ph-r"><p><small>Deliverable</small><b data-ph-del></b></p><p><small>You sign off</small><b data-ph-sign></b></p>'
                 '<div class="pj-ph-prog"><span>Overall progress</span><i><b data-ph-bar></b></i></div></div></div></div>'
                 '<script type="application/json" id="pj-phases">%s</script>' % (pbar, json.dumps(phases)), "pj-sec--phase")

    # 13 ---- readiness quiz
    qs = ["Do you run more than five projects at the same time?", "Do tasks often wait on someone else's work?",
          "Do you bill clients for time or by milestone?", "Do managers spend hours each week chasing status?",
          "Do you need to know which projects make money?", "Do clients ask for updates by phone or WhatsApp?"]
    qitems = "".join('<li><span>%s</span><span class="pj-yn" role="group" aria-label="Answer"><button type="button" data-q="%d" data-a="1" aria-pressed="false">Yes</button>'
                     '<button type="button" data-q="%d" data-a="0" aria-pressed="false">No</button></span></li>' % (q, i, i) for i, q in enumerate(qs))
    out += sec('<div class="pj-quiz"><div>%s<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Book a project workflow review %s</a></div></div>'
               '<div class="pj-q ox-solo" data-quiz><p class="pj-q-h"><b>Project readiness check</b><small>6 questions, 30 seconds</small></p><ol>%s</ol>'
               '<div class="pj-q-res" data-quiz-res aria-live="polite"><span class="pj-q-score" data-quiz-score>0 / 6</span><p data-quiz-txt>Answer the questions to see where you stand.</p></div></div></div>'
               % (head("READINESS CHECK", "Is Your Business Ready to Build a Project Workflow With Odoo?",
                       "If most of these sound familiar, your projects have outgrown spreadsheets and chat groups. We'll review one of your live projects and show it to you in Odoo."),
                  g["ARROW"], qitems), "pj-sec--quiz")

    data = {"P": PROJECTS, "T": TASKS, "U": PEOPLE, "TS": {str(k): v for k, v in TIMESHEETS.items()}, "S": {k: list(v) for k, v in STATUS.items()}}
    return out + JS.replace("__DATA__", json.dumps(data))


JS = r'''<script>
(function(){
  var DATA=__DATA__, U=DATA.U, TODAY=9;
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function inr(n,d){var s=Math.abs(n).toLocaleString('en-IN',{minimumFractionDigits:d?2:0,maximumFractionDigits:d?2:0});return (n<0?'-':'')+'₹ '+s;}
  function press(group,el){group.forEach(function(b){var on=b===el;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});}
  function day(d){if(d===null||d===undefined)return '';return d<27?'Oct '+(5+d):'Nov '+(d-26);}
  function hm(h){var m=Math.round(Math.abs(h)*60);return (h<0?'-':'')+Math.floor(m/60)+':'+('0'+m%60).slice(-2);}
  function av(k,cls){var p=U[k];return '<span class="ox-av '+(cls||'is-sm')+'" style="--c:'+p[2]+'" title="'+p[0]+'">'+p[0][0]+'</span>';}
  function bub(k){var s=DATA.S[k];var c={on_track:'#10AE51',at_risk:'#F5A41A',off_track:'#F04F4F',on_hold:'#3E88D8',done:'#2B7A4B',to_define:'#C3C9CF'}[k];return '<span class="pj-bub" style="--c:'+c+'"><i></i>'+s[0]+'</span>';}
  /* Odoo 20 task states */
  var ST={ip:['In Progress','<circle cx="12" cy="12" r="8"/>'],cr:['Changes Requested','<circle cx="12" cy="12" r="8"/><path d="M12 7.5v5.5M12 16v.5"/>'],
          ap:['Approved','<path d="M7 11v9H4v-9zM7 11l4-7c1.5 0 2.5 1 2.2 2.6L12.6 10H18a2 2 0 0 1 2 2.3l-1.2 6A2 2 0 0 1 16.8 20H7"/>'],
          dn:['Done','<circle cx="12" cy="12" r="8"/><path d="M8 12.5l2.7 2.7L16 9.8"/>'],cx:['Cancelled','<circle cx="12" cy="12" r="8"/><path d="M9 9l6 6M15 9l-6 6"/>'],
          wt:['Waiting','<path d="M7 4h10M7 20h10M8 4c0 5 8 5 8 8s-8 3-8 8M16 4c0 5-8 5-8 8"/>']};
  function stIcon(s,btn,id){var h='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ST[s][1]+'</svg>';
    return btn?'<button type="button" class="pj-st-ic is-'+s+'" data-st-menu="'+id+'" title="'+ST[s][0]+'" aria-label="State: '+ST[s][0]+'">'+h+'</button>':'<span class="pj-st-ic is-'+s+'" title="'+ST[s][0]+'">'+h+'</span>';}
  var STAR='<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.9 6.8 19.6l1-5.8L3.5 9.7l5.9-.8z"/></svg>';
  var FLAG='<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 21V4M5 4h11l-2 4 2 4H5"/></svg>';
  var CAL='<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>';
  var SUB='<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 4v12a3 3 0 0 0 3 3h9M6 9h12"/></svg>';
  var CLK='<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 8v4.5l3 2"/></svg>';

  /* --- 2 project explorer --- */
  var pe=document.querySelector('[data-pe]');
  if(pe){var P=DATA.P,T=DATA.T,TS=DATA.TS,body=pe.querySelector('[data-pe-body]'),crumb=pe.querySelector('[data-pe-crumb]'),q=pe.querySelector('[data-pe-q]');
    var STAGES=['New','In Progress','Done','Cancelled'],st={menu:'projects',proj:null,task:null,view:'kanban',tab:'desc',menuOpen:null},nid=100;
    T.forEach(function(t){t.log=[{w:'Unisas Bot',t:'Task created'}];if(t.blk)t.log.push({w:'Unisas Bot',t:'Blocked by <b>'+esc(find(t.blk).n)+'</b>'});});
    function find(id){return T.filter(function(x){return x.id===+id;})[0];}
    function proj(id){return P.filter(function(x){return x.id===+id;})[0];}
    function closed(t){return t.st==='dn'||t.st==='cx';}
    function match(s){var v=q.value.trim().toLowerCase();return !v||s.toLowerCase().indexOf(v)>-1;}
    function tasksOf(){return T.filter(function(t){return (st.menu==='mine'?t.u.indexOf('M')>-1:t.p===st.proj)&&match(t.n);});}
    function pcard(p){var n=T.filter(function(t){return t.p===p.id&&!closed(t);}).length;
      return '<article class="pj-pcard is-live" tabindex="0" data-proj="'+p.id+'" style="--pc:'+(p.color||'transparent')+'"><p class="pj-pc-top"><button type="button" class="pj-fav'+(p.fav?' is-on':'')+'" data-fav="'+p.id+'" aria-label="Favourite">&#9733;</button><b>'+p.name+'</b></p>'+
        (p.cust?'<small>'+p.cust+'</small>':'')+(p.d?'<span class="pj-pc-date">'+CAL+p.d+'</span>':'')+(p.tag?'<span class="ox-tags"><span class="ox-tag ox-tag--'+p.tag[1]+'">'+p.tag[0]+'</span></span>':'')+
        '<p class="pj-pc-foot"><span class="pj-pc-n">'+n+' '+(p.label||'Tasks')+'</span>'+(p.ms?'<span class="pj-pc-ms">'+FLAG+p.ms+'</span>':'')+bub(p.st)+av(p.pm)+'</p></article>';}
    function projects(){var l=P.filter(function(p){return match(p.name+' '+p.cust);});
      if(st.view==='list')return '<div class="ox-scroll"><table class="ox-table"><thead><tr><th></th><th>Name</th><th>Customer</th><th>Project Manager</th><th>Dates</th><th>Milestone</th><th>Status</th></tr></thead><tbody>'+
        l.map(function(p){return '<tr data-proj="'+p.id+'" tabindex="0"><td><span class="pj-fav'+(p.fav?' is-on':'')+'">&#9733;</span></td><td><b>'+p.name+'</b></td><td>'+(p.cust||'')+'</td><td><span class="ox-sp">'+av(p.pm)+U[p.pm][0]+'</span></td><td>'+(p.d||'')+'</td><td>'+(p.ms||'')+'</td><td>'+bub(p.st)+'</td></tr>';}).join('')+'</tbody></table></div>';
      return '<div class="pj-pgrid is-big">'+l.map(pcard).join('')+'</div>';}
    function rem(t){if(!t.al)return '';var r=t.al-t.sp;return '<span class="pj-rem'+(r<0?' is-over':'')+'" title="Remaining hours">'+hm(r)+'</span>';}
    function tcard(t){var late=t.dl!==null&&t.dl!==undefined&&t.dl<TODAY&&!closed(t);
      return '<article class="ox-card pj-tcard'+(closed(t)?' is-closed':'')+'" draggable="true" tabindex="0" data-task="'+t.id+'"><b class="ox-c-name">'+esc(t.n)+'</b>'+
        (st.menu==='mine'?'<small class="pj-tc-p">'+proj(t.p).name+'</small>':(proj(t.p).cust?'<small class="pj-tc-p">'+proj(t.p).cust+'</small>':''))+
        (t.tags.length?'<span class="ox-tags">'+t.tags.map(function(g){return '<span class="ox-tag ox-tag--'+g[1]+'">'+g[0]+'</span>';}).join('')+'</span>':'')+
        (t.ms?'<span class="pj-tc-ms">'+FLAG+t.ms+'</span>':'')+
        ((t.dl!==null&&t.dl!==undefined)||t.sub?'<span class="pj-tc-meta">'+(t.dl!==null&&t.dl!==undefined?'<span class="'+(late?'pj-late':'')+'">'+CAL+day(t.dl)+'</span>':'')+(t.sub?'<span class="pj-tc-sub">'+SUB+t.sub[0]+'/'+t.sub[1]+'</span>':'')+'</span>':'')+
        '<span class="ox-c-foot"><span class="ox-star'+(t.pri?' is-on':'')+'">'+STAR+'</span>'+(t.act?'<span class="ox-act ox-act--red" title="Overdue activity">'+CLK+'</span>':'')+rem(t)+
        '<span class="pj-tc-r">'+stIcon(t.st,1,t.id)+t.u.map(function(k){return av(k);}).join('')+'</span></span></article>';}
    function kanban(l){var cols=STAGES.slice(0,3),cx=l.filter(function(t){return t.s==='Cancelled';}).length;
      var C={ip:'pj-p-grey',cr:'pj-p-orange',ap:'pj-p-green',dn:'pj-p-green',cx:'pj-p-red',wt:'pj-p-blue'};
      return '<div class="ox-kanban pj-kanban">'+cols.map(function(s){var c=l.filter(function(t){return t.s===s;}),k={};
        c.forEach(function(t){k[C[t.st]]=(k[C[t.st]]||0)+1;});
        var bar=c.length?Object.keys(k).map(function(x){return '<i class="'+x+'" style="flex:'+k[x]+'"></i>';}).join(''):'<i class="pj-p-grey" style="flex:1"></i>';
        return '<section class="ox-col" data-stage="'+s+'"><header><b>'+s+'</b><span class="ox-plus" aria-hidden="true">+</span></header><div class="ox-prog"><span class="ox-bar">'+bar+'</span><b>'+c.length+'</b></div>'+
          '<div class="ox-cards">'+c.map(tcard).join('')+'</div></section>';}).join('')+
        '<section class="pj-fold" data-stage="Cancelled"><b>Cancelled</b><span>('+cx+')</span></section></div>';}
    function tlist(l){return '<div class="ox-scroll"><table class="ox-table"><thead><tr><th></th><th>Title</th><th>Milestone</th><th>Assignees</th><th>Deadline</th><th class="ox-num">Allocated</th><th class="ox-num">Time Spent</th><th>Stage</th><th></th></tr></thead><tbody>'+
      l.map(function(t){var late=t.dl!==null&&t.dl!==undefined&&t.dl<TODAY&&!closed(t);return '<tr data-task="'+t.id+'" tabindex="0"><td><span class="ox-star'+(t.pri?' is-on':'')+'">'+STAR+'</span></td><td><b>'+esc(t.n)+'</b></td><td>'+(t.ms||'')+'</td><td>'+t.u.map(function(k){return av(k);}).join(' ')+'</td>'+
        '<td class="'+(late?'pj-late':'')+'">'+day(t.dl)+'</td><td class="ox-num">'+hm(t.al)+'</td><td class="ox-num'+(t.sp>t.al&&t.al?' pj-late':'')+'">'+hm(t.sp)+'</td><td><span class="ox-stage-pill">'+t.s+'</span></td><td>'+stIcon(t.st)+'</td></tr>';}).join('')+'</tbody></table></div>';}
    function form(t){var p=proj(t.p),i=STAGES.indexOf(t.s);
      var sb=STAGES.slice(0,3).map(function(s,j){return '<button type="button" class="ox-sb'+(s===t.s?' is-cur':'')+'" data-stage-set="'+s+'">'+s+'</button>';}).join('');
      var tabs=[['desc','Description'],['ts','Timesheets'],['sub','Sub-tasks'],['blk','Blocked By']].map(function(x){return '<button type="button" class="'+(st.tab===x[0]?'is-on':'')+'" data-tab="'+x[0]+'">'+x[1]+'</button>';}).join('');
      var lines=TS[t.id]||(TS[t.id]=[]),content;
      if(st.tab==='ts'){content='<table class="pj-lines"><thead><tr><th>Date</th><th>Employee</th><th>Description</th><th class="ox-num">Time Spent</th></tr></thead><tbody>'+
          lines.map(function(l){return '<tr><td>'+l[0]+'</td><td><span class="ox-sp">'+av(l[1])+U[l[1]][0]+'</span></td><td>'+esc(l[2])+'</td><td class="ox-num">'+hm(l[3])+'</td></tr>';}).join('')+
          '<tr><td colspan="4"><button type="button" class="pj-addline" data-do="log">Add a line</button></td></tr></tbody></table>'+
          '<div class="pj-ts-tot"><span>Time Spent:</span><b>'+hm(t.sp)+'</b><span>Remaining Time:</span><b class="'+(t.al-t.sp<0?'pj-late':'')+'">'+hm(t.al-t.sp)+'</b></div>';}
      else if(st.tab==='sub'){var n=t.sub?t.sub[1]:0;content=n?'<table class="pj-lines"><tbody>'+['Confirm order and delivery date','Prepare site for delivery','Log delivery and report issues'].slice(0,n).map(function(x,k){return '<tr><td>'+stIcon(k<t.sub[0]?'dn':'ip')+'</td><td>'+x+'</td><td>'+av(t.u[0])+'</td></tr>';}).join('')+'</tbody></table>':'<p class="ox-muted pj-empty">No sub-tasks. <span class="pj-link">Add a line</span></p>';}
      else if(st.tab==='blk'){var b=t.blk&&find(t.blk);content=b?'<table class="pj-lines"><thead><tr><th>Title</th><th>Assignees</th><th>Stage</th><th></th></tr></thead><tbody><tr><td><b>'+esc(b.n)+'</b></td><td>'+b.u.map(function(k){return av(k);}).join('')+'</td><td>'+b.s+'</td><td>'+stIcon(b.st)+'</td></tr></tbody></table><p class="pj-note-s">This task stays <b>Waiting</b> until the task above is done.</p>':'<p class="ox-muted pj-empty">Not blocked by any task.</p>';}
      else content='<p class="ox-desc">'+(t.id===14?'Run conduits and Cat6 cabling for cabins 1-12 and the meeting rooms. Switchboard by Vijay. Photos of every floor box before the ceiling closes.':'Notes, checklists and files for this task, shared with the team.')+'</p>';
      var log=t.log.slice().reverse().map(function(l){return '<div class="ox-msg"><span class="ox-av is-bot">U</span><div><p><b>'+l.w+'</b> <small>just now</small></p><p>'+l.t+'</p></div></div>';}).join('');
      return '<div class="ox-form pj-form"><div class="ox-f-main"><div class="ox-f-bar"><span class="ox-f-btns"><span class="ox-sbtn">Share</span></span><span class="ox-sbar">'+sb+'</span></div>'+
        '<div class="ox-sheet"><div class="pj-f-title"><span class="ox-star'+(t.pri?' is-on':'')+'">'+STAR+'</span><h3>'+esc(t.n)+'</h3>'+stIcon(t.st,1,t.id)+'</div>'+
        '<dl class="ox-fields"><div><dt>Project</dt><dd>'+p.name+'</dd></div><div><dt>Customer</dt><dd>'+(p.cust||'')+'</dd></div>'+
        '<div><dt>Milestone</dt><dd>'+(t.ms||'')+'</dd></div><div><dt>Allocated Time</dt><dd>'+hm(t.al)+' <small class="ox-muted">('+(t.al?Math.round(t.sp/t.al*100):0)+'%)</small></dd></div>'+
        '<div><dt>Assignees</dt><dd>'+t.u.map(function(k){return '<span class="ox-sp">'+av(k)+U[k][0]+'</span>';}).join(' ')+'</dd></div><div><dt>Deadline</dt><dd class="'+(t.dl!==null&&t.dl!==undefined&&t.dl<TODAY&&!closed(t)?'pj-late':'')+'">'+(day(t.dl)?day(t.dl)+', 2026':'')+'</dd></div>'+
        '<div><dt>Tags</dt><dd>'+t.tags.map(function(g){return '<span class="ox-tag ox-tag--'+g[1]+'">'+g[0]+'</span>';}).join('')+'</dd></div></dl>'+
        '<div class="ox-ftabs pj-ftabs">'+tabs+'</div>'+content+'</div></div>'+
        '<aside class="ox-chatter"><div class="ox-ch-btns"><span class="ox-pbtn">Send message</span><span class="ox-sbtn">Log note</span><span class="ox-sbtn">Activity</span></div><p class="ox-ch-sep">Today</p>'+log+'</aside></div>';}
    function stMenu(t){return '<div class="pj-stmenu" role="menu">'+['ip','cr','ap','cx','dn'].map(function(s){return '<button type="button" role="menuitem" data-st-set="'+s+'" data-id="'+t.id+'"'+(t.st===s?' class="is-on"':'')+'>'+stIcon(s)+ST[s][0]+'</button>';}).join('')+'</div>';}
    function render(){var views=pe.querySelector('[data-pe-views]');views.style.visibility=st.task?'hidden':'visible';
      pe.querySelectorAll('[data-pe-view]').forEach(function(b){var on=b.getAttribute('data-pe-view')===st.view;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
      pe.querySelectorAll('[data-pe-menu]').forEach(function(b){var on=b.getAttribute('data-pe-menu')===st.menu;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
      var parent=st.menu==='mine'?'My Tasks':(st.proj?proj(st.proj).name:'Projects');
      if(st.task){var t=find(st.task);crumb.innerHTML='<a href="#" data-pe-back>'+parent+'</a><span>'+esc(t.n)+'</span>';body.innerHTML=form(t);return;}
      if(st.menu==='projects'&&!st.proj){crumb.innerHTML='<span>Projects</span>';body.innerHTML=projects();return;}
      crumb.innerHTML=st.menu==='mine'?'<span>My Tasks</span>':'<a href="#" data-pe-home>Projects</a><span>'+parent+'</span>';
      var l=tasksOf();body.innerHTML=st.view==='list'?tlist(l):kanban(l);
      if(st.menuOpen){var b=body.querySelector('[data-st-menu="'+st.menuOpen+'"]');if(b){b.insertAdjacentHTML('afterend',stMenu(find(st.menuOpen)));b.parentNode.classList.add('has-menu');}}}
    function log(t,txt,w){t.log.push({w:w||U[t.u[0]||'M'][0],t:txt});}
    function setState(t,s){if(t.st===s)return;t.st=s;log(t,'State: <b>'+ST[s][0]+'</b>');
      if(s==='dn'){T.forEach(function(x){if(x.blk===t.id&&x.st==='wt'){x.st='ip';log(x,'<b>'+esc(t.n)+'</b> is done. This task is no longer blocked.','Unisas Bot');}});}
      if(s==='cx'){t.s='Cancelled';}}
    pe.addEventListener('click',function(e){
      var m=e.target.closest('[data-pe-menu]');if(m){st.menu=m.getAttribute('data-pe-menu');st.proj=null;st.task=null;st.menuOpen=null;render();return;}
      var v=e.target.closest('[data-pe-view]');if(v){st.view=v.getAttribute('data-pe-view');st.menuOpen=null;render();return;}
      if(e.target.closest('[data-pe-back]')){e.preventDefault();st.task=null;render();return;}
      if(e.target.closest('[data-pe-home]')){e.preventDefault();st.proj=null;render();return;}
      var fv=e.target.closest('[data-fav]');if(fv){var pp=proj(fv.getAttribute('data-fav'));pp.fav=!pp.fav;render();return;}
      var ss=e.target.closest('[data-st-set]');if(ss){setState(find(ss.getAttribute('data-id')),ss.getAttribute('data-st-set'));st.menuOpen=null;render();return;}
      var sm=e.target.closest('[data-st-menu]');if(sm){var id=+sm.getAttribute('data-st-menu'),tk=find(id);
        if(tk.st==='wt'){st.menuOpen=null;render();var b=body.querySelector('[data-st-menu="'+id+'"]');if(b){b.insertAdjacentHTML('afterend','<div class="pj-stmenu is-note">Waiting on <b>'+esc(find(tk.blk).n)+'</b></div>');b.parentNode.classList.add('has-menu');}return;}
        st.menuOpen=st.menuOpen===id?null:id;render();return;}
      if(st.menuOpen){st.menuOpen=null;render();}
      var t=st.task&&find(st.task);
      var tb=e.target.closest('[data-tab]');if(tb&&t){st.tab=tb.getAttribute('data-tab');render();return;}
      var sg=e.target.closest('[data-stage-set]');if(sg&&t){var s=sg.getAttribute('data-stage-set');if(s!==t.s){log(t,'Stage: '+t.s+' &rarr; <b>'+s+'</b>');t.s=s;}render();return;}
      var d=e.target.closest('[data-do="log"]');if(d&&t){var k=t.u[0]||'M';(TS[t.id]=TS[t.id]||[]).unshift(['Oct 14',k,'Site work',2]);t.sp+=2;log(t,'2:00 logged by '+U[k][0]);render();return;}
      var pr=e.target.closest('[data-proj]');if(pr){st.proj=+pr.getAttribute('data-proj');st.view='kanban';render();return;}
      var r=e.target.closest('[data-task]');if(r){st.task=+r.getAttribute('data-task');st.tab=st.task===14?'ts':'desc';render();}});
    pe.addEventListener('keydown',function(e){if(e.key!=='Enter')return;var pr=e.target.closest&&e.target.closest('[data-proj]');if(pr&&!e.target.closest('button')){st.proj=+pr.getAttribute('data-proj');render();return;}
      var r=e.target.closest&&e.target.closest('[data-task]');if(r&&!e.target.closest('button')){st.task=+r.getAttribute('data-task');st.tab='desc';render();}});
    pe.querySelector('[data-pe-new]').addEventListener('click',function(){if(st.menu==='projects'&&!st.proj){st.proj=1;}
      var t={id:nid++,p:st.proj||1,n:'New task',s:'New',st:'ip',pri:0,u:['M'],tags:[],dl:null,al:0,sp:0,ms:'',log:[{w:'Meera Iyer',t:'Task created'}]};T.unshift(t);st.task=t.id;st.tab='desc';render();});
    q.addEventListener('input',function(){st.task=null;render();});
    var drag=null;
    body.addEventListener('dragstart',function(e){var c=e.target.closest&&e.target.closest('[data-task]');if(!c)return;drag=c.getAttribute('data-task');c.classList.add('is-drag');try{e.dataTransfer.setData('text/plain',drag);}catch(x){}});
    body.addEventListener('dragend',function(){drag=null;body.querySelectorAll('.is-drag,.is-over').forEach(function(x){x.classList.remove('is-drag','is-over');});});
    body.addEventListener('dragover',function(e){var c=e.target.closest('[data-stage]');if(c&&drag){e.preventDefault();body.querySelectorAll('.is-over').forEach(function(x){if(x!==c)x.classList.remove('is-over');});c.classList.add('is-over');}});
    body.addEventListener('drop',function(e){var c=e.target.closest('[data-stage]');if(c&&drag){e.preventDefault();var t=find(drag),s=c.getAttribute('data-stage');
      if(s!==t.s){log(t,'Stage: '+t.s+' &rarr; <b>'+s+'</b>');t.s=s;if(s==='Cancelled')t.st='cx';else if(t.st==='cx')t.st='ip';}drag=null;render();}});
    render();}

  /* --- 3 project settings --- */
  var stg=document.querySelector('[data-settings]');
  if(stg){var outl=document.querySelector('[data-set-out]');
    function on(k){var x=stg.querySelector('[data-set="'+k+'"]');return x&&x.checked;}
    function sdraw(){var v=stg.querySelector('[data-set-vis]:checked').value,l=[];
      l.push(on('ms')?['ok','Tasks are grouped under <b>First, Second and Final Phase</b>. A milestone can trigger its invoice when reached.']:['warn','No milestones: progress is judged task by task, and milestone billing is not available.']);
      l.push(on('dep')?['ok','<b>False ceiling</b> waits until <b>Electrical cabling</b> is done, and moves with it on the Gantt.']:['warn','Tasks can start in any order. Nothing stops painting before the cabling is finished.']);
      if(on('rec'))l.push(['ok','<b>Weekly site safety check</b> is created every Monday without anyone remembering it.']);
      if(on('rate'))l.push(['ok','When a task reaches Done, Shree Distributors gets a one-click rating email.']);
      l.push(on('ts')?['ok','The team logs hours on each task, against <b>Allocated Time</b>.']:['warn','No hours on tasks, so effort and margin are unknown.']);
      if(on('bill'))l.push(on('ts')?['ok','Logged hours flow to sales order <b>S00482</b>, ready to invoice.']:['warn','Billable, but without timesheets only fixed-price or milestone billing works.']);
      l.push(v==='private'?['ok','Only the people invited can open this project.']:v==='internal'?['ok','Everyone in the company can see the project; the client cannot.']:['ok','The client logs in to the <b>portal</b> and follows their tasks, without internal notes or costs.']);
      outl.innerHTML=l.map(function(x){return '<li class="is-'+x[0]+'">'+x[1]+'</li>';}).join('');}
    stg.addEventListener('change',sdraw);sdraw();}

  /* --- 4 dependencies & milestones --- */
  var dp=document.querySelector('[data-dep]');
  if(dp){var C0=[['Site survey & measurements','A','First Phase','dn'],['Layout approval from client','A','First Phase','ip'],['Electrical & data cabling','R','Second Phase','wt'],
          ['False ceiling & painting','R','Second Phase','wt'],['Furniture installation','K','Final Phase','wt'],['Snag list & handover','M','Final Phase','wt']];
    var MS=[['First Phase','Oct 12'],['Second Phase','Oct 26'],['Final Phase','Nov 6']],C,note='';
    function reset(){C=C0.map(function(x){return x.slice();});note='';}
    function ddraw(){var cur=C.findIndex(function(x){return x[3]==='ip';});
      dp.querySelector('[data-dep-chain]').innerHTML=C.map(function(x,i){var p=U[x[1]];
        return '<li class="is-'+x[3]+'">'+stIcon(x[3])+'<div><b>'+x[0]+'</b><small>'+p[0]+' &middot; '+x[2]+(i?' &middot; Blocked by: '+C[i-1][0]:'')+'</small></div>'+
          (i===cur?'<button type="button" class="ox-pbtn" data-dep-done="'+i+'">Mark as Done</button>':'<span class="pj-chain-st">'+ST[x[3]][0]+'</span>')+'</li>';}).join('')+(note?'<li class="pj-chain-note">'+note+'</li>':'');
      dp.querySelector('[data-dep-ms]').innerHTML=MS.map(function(m){var ts=C.filter(function(x){return x[2]===m[0];}),d=ts.filter(function(x){return x[3]==='dn';}).length,ok=d===ts.length;
        return '<tr class="is-static'+(ok?' is-ok':'')+'"><td><b>'+m[0]+'</b></td><td>'+m[1]+'</td><td class="ox-num">'+d+'/'+ts.length+'</td><td><span class="ox-cb'+(ok?' is-on':'')+'"></span>'+(ok?' <small class="pj-ok">Reached</small>':'')+'</td></tr>';}).join('');}
    dp.addEventListener('click',function(e){var b=e.target.closest('[data-dep-done]');
      if(b){var i=+b.getAttribute('data-dep-done');C[i][3]='dn';note='<b>'+C[i][0]+'</b> is done.';
        if(C[i+1]){C[i+1][3]='ip';note+=' <b>'+C[i+1][0]+'</b> is no longer blocked and '+U[C[i+1][1]][0]+' is notified.';}
        var m=C[i][2];if(C.filter(function(x){return x[2]===m;}).every(function(x){return x[3]==='dn';}))note+=' Milestone <b>'+m+'</b> reached.';
        if(C.every(function(x){return x[3]==='dn';}))note='All tasks done. The project is ready for handover.';ddraw();}
      if(e.target.closest('[data-dep-reset]')){reset();ddraw();}});
    reset();ddraw();}

  /* --- 5 timesheets to invoice --- */
  var bl=document.querySelector('[data-bill]');
  if(bl){var RATE=2500,COST=1100,PO=185000,ORD=120,b;
    function breset(){b={del:64,inv:40,n:0};}
    function say(k,t){var li=bl.querySelector('[data-bill-app="'+k+'"]');li.querySelector('[data-bill-txt]').innerHTML=t;li.classList.remove('is-hot');void li.offsetWidth;li.classList.add('is-hot');}
    function bdraw(){bl.querySelector('[data-bill-lines]').innerHTML='<tr><td><b>Fit-out design &amp; supervision</b><small>Service, invoiced on timesheets</small></td><td class="ox-num">'+ORD+'.00 Hours</td>'+
        '<td class="ox-num pj-in">'+b.del.toFixed(2)+'</td><td class="ox-num">'+b.inv.toFixed(2)+'</td><td class="ox-num">'+inr(RATE,1)+'</td><td class="ox-num">'+inr(ORD*RATE,1)+'</td></tr>'+
        '<tr><td><b>Modular workstations</b><small>Delivered and invoiced</small></td><td class="ox-num">24.00 Units</td><td class="ox-num">24.00</td><td class="ox-num">24.00</td><td class="ox-num">'+inr(14500,1)+'</td><td class="ox-num">'+inr(348000,1)+'</td></tr>';
      var toinv=b.del>b.inv;bl.querySelector('[data-bill-is]').innerHTML='<span class="pj-st '+(toinv?'is-to':'is-ok')+'">'+(toinv?'To Invoice':'Fully Invoiced')+'</span>';
      bl.querySelector('[data-bill-smart]').innerHTML='<span class="pj-smart"><span>Project<b>1</b></span></span><span class="pj-smart"><span>Tasks<b>11</b></span></span><span class="pj-smart"><span>Recorded<b>'+b.del+' Hours</b></span></span><span class="pj-smart"><span>Invoices<b>'+(1+b.n)+'</b></span></span>';
      var ri=b.inv*RATE+348000,rt=(b.del-b.inv)*RATE,ct=b.del*COST+PO,exp=ri+rt;
      function row(n,e,a,c,cls){return '<tr class="'+(cls||'')+'"><td>'+n+'</td><td class="ox-num">'+e+'</td><td class="ox-num">'+a+'</td><td class="ox-num">'+c+'</td></tr>';}
      bl.querySelector('[data-bill-prof]').innerHTML='<thead><tr><th>Revenues</th><th class="ox-num">Expected</th><th class="ox-num">To Invoice</th><th class="ox-num">Invoiced</th></tr></thead><tbody>'+
        row('Timesheets (billed on timesheets)',inr((b.del)*RATE),inr(rt),inr(b.inv*RATE))+row('Materials',inr(348000),inr(0),inr(348000))+
        row('<b>Total</b>','<b>'+inr(exp)+'</b>','<b>'+inr(rt)+'</b>','<b>'+inr(ri)+'</b>','is-tot')+
        '</tbody><thead><tr><th>Costs</th><th class="ox-num">Expected</th><th class="ox-num">To Bill</th><th class="ox-num">Billed</th></tr></thead><tbody>'+
        row('Timesheets',inr(-b.del*COST),inr(0),inr(-b.del*COST))+row('Purchase Orders',inr(-PO),inr(0),inr(-PO))+
        row('<b>Total</b>','<b>'+inr(-ct)+'</b>',inr(0),'<b>'+inr(-ct)+'</b>','is-tot')+
        '</tbody><tfoot><tr><td><b>Margin</b></td><td class="ox-num"><b class="pj-in">'+inr(exp-ct)+'</b></td><td colspan="2" class="ox-num"><b>'+Math.round((exp-ct)/exp*100)+'%</b></td></tr></tfoot>';
      var L=bl.querySelector('[data-bill-do="log"]'),I=bl.querySelector('[data-bill-do="inv"]');L.disabled=b.del>=ORD;I.disabled=!toinv;I.className=toinv?'ox-pbtn':'ox-sbtn';L.className=toinv?'ox-sbtn':'ox-pbtn';}
    bl.addEventListener('click',function(e){var x=e.target.closest('[data-bill-do]');if(!x||x.disabled)return;var k=x.getAttribute('data-bill-do');
      if(k==='log'){b.del=Math.min(ORD,b.del+8);say('ts','Rahul Menon logged <b>8:00</b> on <i>Electrical &amp; data cabling</i>. The task shows '+b.del+' of 120 hours used.');say('sales','Delivered quantity on S00482 is now <b>'+b.del+' hours</b>.');say('acc',(b.del-b.inv)+' hours ('+inr((b.del-b.inv)*RATE)+') are ready to invoice.');}
      if(k==='inv'){var h=b.del-b.inv;b.inv=b.del;b.n++;say('acc','Invoice <b>INV/2026/04'+(12+b.n)+'</b> for '+h+' hours, '+inr(h*RATE*1.18)+' incl. GST, drafted with the timesheet lines attached.');say('ts','The invoiced timesheets are locked, so nobody edits billed hours.');say('sales','S00482: '+b.inv+' of 120 hours invoiced.');}
      if(k==='reset'){breset();say('sales','S00482 created the project and its tasks from the fit-out template.');say('ts','64 hours logged so far by the team, against 120 sold.');say('acc','40 hours invoiced. 24 hours are waiting to be billed.');}
      bdraw();});
    breset();say('sales','S00482 created the project and its tasks from the fit-out template.');say('ts','64 hours logged so far by the team, against 120 sold.');say('acc','40 hours invoiced. 24 hours are waiting to be billed.');bdraw();}

  /* --- 6 Gantt planning --- */
  var pl=document.querySelector('[data-plan]');
  if(pl){var N=35,DL=32,ps={delay:false,crew:false};
    function plan(){var t4s=7+(ps.delay?4:0),t4l=ps.crew?5:8,t5s=t4s+t4l,t6s=t5s+7,t7s=t6s+6;
      return [['A','Site survey',0,3,'done',''],['A','Layout approval',3,4,'done','Site survey'],['K','Furniture order',7,4,'done','Layout approval'],
        ['R','Electrical &amp; data cabling',t4s,t4l,'doing','Layout approval'],['R','False ceiling &amp; painting',t5s,7,'todo','Electrical &amp; data cabling'],
        ['K','Furniture installation',t6s,6,'todo','False ceiling &amp; painting'],['M','Snag list &amp; handover',t7s,3,'todo','Furniture installation']].concat(ps.crew?[['V','Electrical &amp; data cabling',t4s,t4l,'doing','Layout approval']]:[]);}
    function gdraw(){var L=plan(),end=0;L.forEach(function(t){end=Math.max(end,t[2]+t[3]);});
      var days='';for(var d=0;d<N;d++){var we=d%7===5||d%7===6;days+='<span class="'+(we?'is-we':'')+(d===TODAY?' is-today':'')+'">'+('0'+(d<27?5+d:d-26)).slice(-2)+'</span>';}
      var cols='';for(d=0;d<N;d++)if(d%7===5||d%7===6)cols+='<i class="ox-gt-we" style="--d:'+d+'"></i>';cols+='<i class="ox-gt-today" style="--d:'+TODAY+'"></i><i class="pj-gt-dl" style="--d:'+DL+'" title="Deadline Nov 6"></i>';
      var rows='';['A','K','M','R','V'].forEach(function(k){var ts=L.filter(function(t){return t[0]===k;});if(!ts.length)return;var p=U[k],h=ts.reduce(function(s,t){return s+t[3]*8;},0);
        var over=k==='R'&&ps.delay&&!ps.crew;
        rows+='<div class="ox-gt-row is-group"><div class="ox-gt-label"><span class="ox-gt-caret">&#9662;</span><span class="ox-av" style="--c:'+p[2]+'">'+p[0][0]+'</span><span class="ox-gt-who"><b>'+p[0]+'</b><small>'+p[1]+'</small></span><span class="ox-gt-h">'+h+'h</span></div><div class="ox-gt-track"></div></div>';
        ts.forEach(function(t){var late=t[2]+t[3]>DL;rows+='<div class="ox-gt-row"><div class="ox-gt-label is-task"><span>'+t[1]+'</span></div><div class="ox-gt-track">'+
          '<button type="button" class="ox-gt-bar is-'+t[4]+(late?' pj-late-bar':'')+'" style="--s:'+t[2]+';--l:'+t[3]+'"><span class="pj-gt-t">'+t[1]+'</span><span class="ox-gt-pop'+(t[2]+t[3]>N-12?' is-end':'')+(k==='R'||k==='V'?' is-up':'')+'" role="tooltip"><b>'+t[1]+'</b><span>'+day(t[2])+' &rarr; '+day(t[2]+t[3]-1)+'</span><span>Assignee: '+p[0]+'</span>'+(t[5]?'<span>Blocked by: '+t[5]+'</span>':'')+(late?'<small>Ends after the project deadline (Nov 6).</small>':'')+'</span></button></div></div>';});});
      pl.querySelector('[data-plan-gantt]').innerHTML='<div class="ox-gt-head"><div class="ox-gt-label is-head">Planning</div><div class="ox-gt-track"><div class="ox-gt-months"><span style="--d:27">October 2026</span><span style="--d:8">November 2026</span></div><div class="ox-gt-days">'+days+'</div></div></div>'+
        '<div class="ox-gt-body"><div class="ox-gt-cols" aria-hidden="true">'+cols+'</div>'+rows+'</div>';
      var risk=end>DL,pct=ps.delay&&!ps.crew?38:45;
      pl.querySelector('[data-plan-st]').innerHTML=bub(risk?'at_risk':'on_track');pl.querySelector('[data-plan-bar]').style.width=pct+'%';pl.querySelector('[data-plan-pct]').textContent=pct+'%';
      pl.querySelector('[data-plan-end]').innerHTML='<span class="'+(risk?'pj-late':'pj-in')+'">'+day(end-1)+'</span>';
      pl.querySelector('[data-plan-load]').innerHTML=ps.delay&&!ps.crew?'<span class="pj-late">Booked into Nov</span>':'Within plan';
      pl.querySelector('[data-plan-txt]').innerHTML=!ps.delay?'Cabling ends Oct 19, ceiling and furniture follow, and handover lands on '+day(end-1)+', two days before the deadline.':
        ps.crew?'Vijay joins the cabling from '+day(11)+'. It now takes five days, so handover is back to <b>'+day(end-1)+'</b>, inside the deadline.':
        'Switchgear arrives four days late. Ceiling, furniture and handover all move with it, and handover now falls on <b>'+day(end-1)+'</b>, after the Nov 6 deadline.';
      pl.querySelectorAll('[data-plan-do]').forEach(function(b){var k=b.getAttribute('data-plan-do');if(k!=='reset'){b.setAttribute('aria-pressed',ps[k]);b.classList.toggle('is-on',ps[k]);}});
      pl.querySelector('[data-plan-do="crew"]').disabled=!ps.delay;}
    pl.addEventListener('click',function(e){var b=e.target.closest('[data-plan-do]');if(!b||b.disabled)return;var k=b.getAttribute('data-plan-do');
      if(k==='reset'){ps={delay:false,crew:false};}else{ps[k]=!ps[k];if(k==='delay'&&!ps.delay)ps.crew=false;}gdraw();});
    gdraw();}

  /* --- 7 roles --- */
  var rl=document.querySelector('[data-roles]');
  if(rl){var R=JSON.parse(document.getElementById('pj-roles').textContent),rb=[].slice.call(rl.querySelectorAll('[data-role]')),card=rl.querySelector('[data-role-card]');
    function rdraw(i){var r=R[i];card.innerHTML='<p class="pj-role-h"><b>'+r[1]+'</b><span class="pj-tag pj-tag--cfg">'+r[2]+'</span></p><p class="pj-role-land"><small>Lands on</small>'+r[3]+'</p>'+
      '<div class="pj-role-cols"><div><small>Can</small><ul>'+r[4].map(function(x){return '<li class="is-y">'+x+'</li>';}).join('')+'</ul></div><div><small>Cannot</small><ul>'+r[5].map(function(x){return '<li class="is-n">'+x+'</li>';}).join('')+'</ul></div></div>';}
    rb.forEach(function(b){b.addEventListener('click',function(){press(rb,b);rdraw(+b.getAttribute('data-role'));});});rdraw(0);}

  /* --- 8 apps --- */
  var ap=document.querySelector('[data-app-card]');
  if(ap){var A=JSON.parse(document.getElementById('pj-apps').textContent),ab=[].slice.call(document.querySelectorAll('[data-app]'));
    function adraw(i){var a=A[i];ap.style.setProperty('--c',a[1]);ap.querySelector('[data-app-to]').innerHTML='<i>'+a[0][0]+'</i><b>'+a[0]+'</b>';ap.querySelector('[data-app-what]').innerHTML=a[2];
      ap.querySelector('[data-app-ex]').innerHTML='<small>For example</small>'+a[3];ap.classList.remove('is-hot');void ap.offsetWidth;ap.classList.add('is-hot');}
    ab.forEach(function(b){b.addEventListener('click',function(){press(ab,b);adraw(+b.getAttribute('data-app'));});});adraw(0);}

  /* --- 9 import + UAT --- */
  var im=document.querySelector('[data-imp]');
  if(im){var SRC=JSON.parse(document.getElementById('pj-src').textContent),sb=[].slice.call(im.querySelectorAll('[data-src]')),cur='Excel',res=im.querySelector('[data-imp-res]');
    var FILE={'Excel':'Project_Tracker_FINAL_v7.xlsx','Asana':'asana_export_office_fitout.csv','Trello':'trello_board_export.json → csv','MS Project':'ChennaiHQ_plan.mpp → xml','Jira':'jira_issues_FIT.csv'};
    function idraw(){im.querySelector('[data-imp-file]').innerHTML='<b>'+FILE[cur]+'</b> &middot; 312 rows';
      im.querySelector('[data-imp-rows]').innerHTML=SRC[cur].map(function(r){return '<tr class="is-static"><td>'+r[0]+'</td><td class="ox-muted">&rarr;</td><td><span class="pj-sel">'+r[1]+'</span></td></tr>';}).join('');res.className='pj-imp-res';res.textContent='';}
    sb.forEach(function(b){b.addEventListener('click',function(){press(sb,b);cur=b.getAttribute('data-src');idraw();});});
    im.addEventListener('click',function(e){var b=e.target.closest('[data-imp-do]');if(!b)return;
      if(b.getAttribute('data-imp-do')==='test'){res.className='pj-imp-res is-info';res.innerHTML='Everything seems valid. 312 tasks, 6 stages and 14 users matched.';}
      else{res.className='pj-imp-res is-ok';res.innerHTML='312 records successfully imported into <b>'+(cur==='Excel'?'4 projects':'Office Fit-out: Chennai HQ')+'</b>, with stages, assignees and deadlines.';}});
    idraw();}
  var ub=document.querySelector('[data-uatbox]');
  if(ub){var cb=[].slice.call(ub.querySelectorAll('[data-uat]'));
    function udraw(){var n=cb.filter(function(c){return c.checked;}).length,p=Math.round(n/cb.length*100);
      ub.querySelector('[data-uat-pct]').textContent=p+'%';ub.querySelector('[data-uat-bar]').style.width=p+'%';ub.classList.toggle('is-ready',p===100);
      ub.querySelector('[data-uat-res]').innerHTML=p===100?'<b>Ready for go-live.</b> Every role has signed off its scenarios.':(cb.length-n)+' scenario'+(cb.length-n===1?'':'s')+' left before go-live.';}
    ub.addEventListener('change',udraw);udraw();}

  /* --- 11 process tabs --- */
  var tabs=[].slice.call(document.querySelectorAll('.pj-tab'));
  function sel(t,f){tabs.forEach(function(x){var o=x===t;x.setAttribute('aria-selected',o);x.tabIndex=o?0:-1;document.getElementById(x.getAttribute('aria-controls')).hidden=!o;});if(f)t.focus();}
  tabs.forEach(function(t,i){t.addEventListener('click',function(){sel(t);});t.addEventListener('keydown',function(e){var d={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1}[e.key];if(d){e.preventDefault();sel(tabs[(i+d+tabs.length)%tabs.length],true);}});});

  /* --- 12 phases --- */
  var ph=document.querySelector('[data-phase]');
  if(ph){var PH=JSON.parse(document.getElementById('pj-phases').textContent),pb=[].slice.call(ph.querySelectorAll('[data-ph]'));
    function phdraw(i){var p=PH[i];pb.forEach(function(b,j){b.classList.toggle('is-cur',j===i);b.classList.toggle('is-done',j<i);b.setAttribute('aria-pressed',j===i);});
      ph.querySelector('[data-ph-when]').textContent=p[1];ph.querySelector('[data-ph-name]').innerHTML=p[0];ph.querySelector('[data-ph-do]').innerHTML=p[2].map(function(x){return '<li>'+x+'</li>';}).join('');
      ph.querySelector('[data-ph-del]').textContent=p[3];ph.querySelector('[data-ph-sign]').textContent=p[4];ph.querySelector('[data-ph-bar]').style.width=Math.round((i+1)/PH.length*100)+'%';}
    pb.forEach(function(b){b.addEventListener('click',function(){phdraw(+b.getAttribute('data-ph'));});});phdraw(0);}

  /* --- 13 quiz --- */
  var qz=document.querySelector('[data-quiz]');
  if(qz){var ans={};
    qz.addEventListener('click',function(e){var b=e.target.closest('[data-q]');if(!b)return;var k=b.getAttribute('data-q');ans[k]=+b.getAttribute('data-a');
      press([].slice.call(qz.querySelectorAll('[data-q="'+k+'"]')),b);
      var n=Object.keys(ans).length,y=Object.keys(ans).reduce(function(s,x){return s+ans[x];},0),txt;
      qz.querySelector('[data-quiz-score]').textContent=y+' / 6';
      txt=n<6?'Keep going: '+(6-n)+' question'+(6-n===1?'':'s')+' left.':y>=4?'<b>You are ready.</b> Your projects have outgrown spreadsheets. Odoo Project with timesheets and billing will pay back quickly.':
        y>=2?'<b>Nearly there.</b> Start with projects, stages and timesheets, then add planning and billing as you grow.':'<b>Start simple.</b> Odoo Project can grow with you. A short call will show what is worth setting up now.';
      qz.querySelector('[data-quiz-txt]').innerHTML=txt;qz.classList.toggle('is-done',n===6);});}
})();
</script>
'''

CTA = ("Let's Build Your Project Workflow in Odoo",
       "Tell us how your team plans, delivers and bills projects today. We'll show you one of your live projects in Odoo Project and recommend the right setup.")
