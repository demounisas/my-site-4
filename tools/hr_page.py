"""
Odoo HR page (odoo-hr.html). Every screen is modelled on the real Odoo 20 Employees app
(demo.odoo.com/odoo/employees and the apps around it): the employee kanban with its department
side panel, the list view, the employee form (Resume, Work Information, Private Information,
HR Settings) with its org chart, Departments, the org chart hierarchy, activity plans for
onboarding and offboarding, the departure wizard, time off validation types, working schedules,
attendance, access rights, skills and appraisals.
Sample company: a 42-person appliance maker with a head office in Chennai and a plant in
Coimbatore, so the same employees appear in every section. Shared Odoo look: odoo-ui.css.
Page styles: hr.css.

hero(g) and build(g) get the build script's globals.
"""
import json

from crm_explorer import ic, SEARCH, V_KANBAN, V_LIST

TICK = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M5 13l4 4L19 7" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def head(eyebrow, title, sub="", cls=""):
    return ('<div class="hr-head%s"><p class="hr-eyebrow mono">%s</p><h2 class="hr-title">%s</h2>%s</div>'
            % (" " + cls if cls else "", eyebrow, title, '<p class="hr-sub">%s</p>' % sub if sub else ""))


def sec(body, cls="", sid=""):
    return '<section class="hr-sec %s"%s><div class="container">%s</div></section>\n' % (cls, ' id="%s"' % sid if sid else "", body)


def data(sid, obj):
    """JSON for the page script, safe inside a <script> element."""
    return '<script type="application/json" id="%s">%s</script>' % (sid, json.dumps(obj).replace("</", "<\\/"))


def ox_head(crumb_a, crumb_b, right=""):
    return ('<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>%s</a><span>%s</span></span></div><span></span>%s</div>'
            % (crumb_a, crumb_b, right or "<span></span>"))


# ------------------------------------------------------------------ shared sample data
DEPTS = [
    {"k": "mgmt", "n": "Management", "mgr": 1, "parent": "", "loc": "Chennai HQ"},
    {"k": "sales", "n": "Sales", "mgr": 3, "parent": "mgmt", "loc": "Chennai HQ"},
    {"k": "prod", "n": "Production", "mgr": 6, "parent": "mgmt", "loc": "Coimbatore Plant"},
    {"k": "qc", "n": "Quality", "mgr": 9, "parent": "prod", "loc": "Coimbatore Plant"},
    {"k": "store", "n": "Stores &amp; Logistics", "mgr": 10, "parent": "prod", "loc": "Coimbatore Plant"},
    {"k": "acct", "n": "Accounts &amp; Admin", "mgr": 11, "parent": "mgmt", "loc": "Chennai HQ"},
    {"k": "hr", "n": "Human Resources", "mgr": 2, "parent": "mgmt", "loc": "Chennai HQ"},
]
# presence: in (checked in), out (not checked in), off (on time off)
EMPS = [
    {"id": 1, "n": "Arjun Mehta", "job": "Managing Director", "d": "mgmt", "m": 0, "loc": "Chennai HQ", "type": "Employee", "p": "in", "c": "#3E7CB1", "tags": ["Leadership"], "join": "Jun 1, 2014", "att": 171.5, "to": 14},
    {"id": 2, "n": "Lakshmi Iyer", "job": "HR Manager", "d": "hr", "m": 1, "loc": "Chennai HQ", "type": "Employee", "p": "in", "c": "#8E4F83", "tags": ["Leadership"], "join": "Mar 15, 2018", "att": 166.0, "to": 11},
    {"id": 3, "n": "Kavya Nair", "job": "Sales Manager", "d": "sales", "m": 1, "loc": "Chennai HQ", "type": "Employee", "p": "in", "c": "#B5567E", "tags": ["Leadership", "Field"], "join": "Aug 2, 2019", "att": 168.5, "to": 8},
    {"id": 4, "n": "Priya Raman", "job": "Sales Executive", "d": "sales", "m": 3, "loc": "Chennai HQ", "type": "Employee", "p": "in", "c": "#4C9F70", "tags": ["Field"], "join": "Jul 4, 2022", "att": 162.5, "to": 9},
    {"id": 5, "n": "Mohammed Irfan", "job": "Sales Executive", "d": "sales", "m": 3, "loc": "Chennai HQ", "type": "Employee", "p": "out", "c": "#C98600", "tags": ["Field"], "join": "Jan 9, 2024", "att": 151.0, "to": 6},
    {"id": 6, "n": "Ravi Kumar", "job": "Production Head", "d": "prod", "m": 1, "loc": "Coimbatore Plant", "type": "Employee", "p": "in", "c": "#1F8A78", "tags": ["Leadership", "Shift A"], "join": "Feb 20, 2016", "att": 178.0, "to": 12},
    {"id": 7, "n": "Suresh Babu", "job": "Line Supervisor", "d": "prod", "m": 6, "loc": "Coimbatore Plant", "type": "Worker", "p": "in", "c": "#6B5B95", "tags": ["Shift A"], "join": "Nov 3, 2020", "att": 184.5, "to": 7},
    {"id": 8, "n": "Anitha Selvam", "job": "Machine Operator", "d": "prod", "m": 7, "loc": "Coimbatore Plant", "type": "Worker", "p": "off", "c": "#E07A5F", "tags": ["Shift B"], "join": "Mar 12, 2023", "att": 139.0, "to": 2},
    {"id": 9, "n": "Fathima Begum", "job": "Quality Lead", "d": "qc", "m": 6, "loc": "Coimbatore Plant", "type": "Employee", "p": "in", "c": "#3D8DAE", "tags": ["Shift A"], "join": "Jun 18, 2021", "att": 170.0, "to": 10},
    {"id": 10, "n": "Senthil Murugan", "job": "Stores In-charge", "d": "store", "m": 6, "loc": "Coimbatore Plant", "type": "Employee", "p": "out", "c": "#7A6C5D", "tags": ["Shift A"], "join": "Jan 15, 2021", "att": 158.5, "to": 4},
    {"id": 11, "n": "Deepa Krishnan", "job": "Accounts Manager", "d": "acct", "m": 1, "loc": "Chennai HQ", "type": "Employee", "p": "in", "c": "#B7791F", "tags": ["Leadership"], "join": "Apr 6, 2017", "att": 165.0, "to": 13},
    {"id": 12, "n": "Vignesh Rao", "job": "Accounts Executive", "d": "acct", "m": 11, "loc": "Chennai HQ", "type": "Employee", "p": "in", "c": "#5A7D9A", "tags": [], "join": "Feb 1, 2024", "att": 160.0, "to": 5},
    {"id": 13, "n": "Nisha George", "job": "HR Executive", "d": "hr", "m": 2, "loc": "Chennai HQ", "type": "Trainee", "p": "in", "c": "#C2567B", "tags": [], "join": "Sep 1, 2025", "att": 163.5, "to": 3},
]
TAGCOL = {"Leadership": "purple", "Field": "blue", "Shift A": "green", "Shift B": "yellow"}


# ------------------------------------------------------------------ hero
def hero(g):
    crumb = ('<nav class="mp-crumb mono" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span>'
             '<a href="index.html#modules">Solutions</a><span>/</span><span aria-current="page">HR</span></nav>')
    points = "".join('<li>%s%s</li>' % (TICK, p) for p in ["One record for every employee", "Leave, attendance &amp; approvals", "Built for teams of 10 to 500"])
    copy = ('<div class="hr-hero-copy">%s<p class="hr-eyebrow mono">ODOO HR IMPLEMENTATION</p>'
            '<h1 class="hr-h1">HR Software for Small Businesses <span>Configured to Fit Your Workflows</span> with Odoo</h1>'
            '<p class="hr-lead">Unisas sets up Odoo Employees, Time Off and Attendances around the way your company already works, so every employee record, '
            'leave request and approval lives in one place. Managers approve from their phone, employees serve themselves, and HR stops chasing spreadsheets.</p>'
            '<ul class="hr-hero-points">%s</ul>'
            '<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Discuss Odoo HR %s</a>'
            '<a href="#explore" class="btn btn-ghost">Try the employee demo</a></div></div>' % (crumb, points, g["ARROW"]))
    def node(ini, name, role, c, cls=""):
        return '<div class="hr-hv-n %s"><span class="hr-hv-av" style="--c:%s">%s</span><b>%s</b><small>%s</small></div>' % (cls, c, ini, name, role)
    tree = ('<div class="hr-hv-tree">' + node("AM", "Arjun Mehta", "Managing Director", "#3E7CB1", "is-top has-kids")
            + '<div class="hr-hv-row"><div class="hr-hv-br">' + node("KN", "Kavya Nair", "Sales Manager", "#B5567E", "has-kids")
            + '<div class="hr-hv-kids">' + node("PR", "Priya Raman", "Sales Executive", "#4C9F70", "is-me") + node("SK", "Sanjay K", "Sales Executive", "#C98600") + '</div></div>'
            + '<div class="hr-hv-br">' + node("RM", "Rahul Menon", "Operations Manager", "#714B67", "has-kids")
            + '<div class="hr-hv-kids">' + node("DS", "Divya S", "Accounts", "#2F6BD8") + node("IA", "Imran A", "Warehouse", "#1F8A78") + '</div></div></div></div>')
    days = "".join('<li class="%s"><small>%s</small><b>%d</b>%s</li>' % ("is-off" if d in (22, 23) else ("is-we" if d > 23 else ""), w, d, "<em>PTO</em>" if d in (22, 23) else "")
                   for w, d in zip(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], range(19, 26)))
    bot = ('<div class="hr-hv-bot"><div class="hr-hv-pop"><p><b>Priya Raman</b><span class="hr-hv-live"><i></i>Checked in 09:02</span></p>'
           '<ul><li><b>162.5 h</b>attendance</li><li><b>9 days</b>time off left</li><li><b>6</b>skills</li></ul></div>'
           '<div class="hr-hv-wk"><p><b>Time Off</b><small>Oct 19 &ndash; 25</small></p><ol>' + days + '</ol>'
           '<p class="hr-hv-ok">' + TICK + 'Approved by Kavya Nair</p></div></div>')
    return ('<section class="hr-hero">' + copy + '<div class="hr-hero-vis hr-hv" aria-label="An organisation chart in Odoo Employees, with one employee&rsquo;s attendance and approved time off">'
            + tree + bot + '</div></section>')

# ------------------------------------------------------------------ sections
def build(g):
    out = ""
    app_icon = g["TILE_ICONS"][0]

    # 1 ---- scattered information: one employee, many versions
    sources = [("Employee master.xlsx", "HR laptop", "3 months ago"), ("Payroll sheet", "Accounts", "Monthly"), ("Biometric machine", "Coimbatore gate", "Daily"),
               ("Email &amp; WhatsApp", "Leave requests", "Every day"), ("Personnel file", "Cabinet in HR room", "At joining"), ("Leave register", "Notebook", "When someone remembers")]
    conflicts = [("Mobile", [("Employee master", "+91 98400 11223"), ("WhatsApp", "+91 90030 55821")], 1, "Changed her number in June; only WhatsApp knew."),
                 ("Department", [("Employee master", "Marketing"), ("Payroll sheet", "Sales")], 1, "Moved to Sales last year; the master sheet was never updated."),
                 ("Manager", [("Employee master", "Arjun Mehta"), ("Email", "Kavya Nair")], 1, "Kavya approves her leave by email, so Kavya is her manager."),
                 ("Date of joining", [("Personnel file", "04/07/2022"), ("Payroll sheet", "07/04/2022")], 0, "Same date, two formats: 4 July 2022."),
                 ("Leave balance", [("Leave register", "12 days"), ("Email approvals", "9 days")], 1, "Three approved days by email never reached the register."),
                 ("Bank account", [("Payroll sheet", "HDFC &middot;&middot;&middot; 4412"), ("Personnel file", "SBI &middot;&middot;&middot; 0937")], 0, "Salary goes to HDFC; the SBI account is from her previous job.")]
    src = "".join('<li><b>%s</b><small>%s</small><span>%s</span></li>' % s for s in sources)
    rows = "".join('<li class="hr-cf" data-cf="%d"><span class="hr-cf-f">%s</span><span class="hr-cf-opts">%s</span></li>'
                   % (i, f, "".join('<button type="button" data-pick="%d"><small>%s</small>%s</button>' % (j, s, v) for j, (s, v) in enumerate(opts)))
                   for i, (f, opts, ok, why) in enumerate(conflicts))
    out += sec(head("THE PROBLEM", "Is Employee Information Scattered Across Too Many Systems?",
                    "In most small companies one employee lives in six places, and each place has a slightly different answer. "
                    "Here is Priya, a sales executive, as she exists today. Pick the right value for each field and watch one Odoo record take shape.", "is-center")
               + '<div class="hr-scat" data-scat><ul class="hr-srcs">%s</ul><div class="hr-cfs ox-solo"><p class="hr-cfs-h"><b>Priya Raman: six fields that disagree</b><small data-cf-n>0 of 6 resolved</small></p>'
                 '<ol>%s</ol><p class="hr-cf-why" data-cf-why aria-live="polite">Choose the value you think is right.</p></div>'
                 '<div class="hr-one ox-solo"><p class="mono">ODOO &middot; EMPLOYEE</p><b>Priya Raman</b><small>Sales Executive</small><dl data-cf-rec></dl><p class="hr-one-res" data-cf-res></p></div></div>'
                 % (src, rows) + data("hr-cf", conflicts), "hr-sec--scat")

    # 2 ---- the central hub: Employees explorer
    menu = "".join('<button type="button" class="hr-menu%s" data-ex-menu="%s" aria-pressed="%s">%s</button>' % (" is-on" if k == "emp" else "", k, "true" if k == "emp" else "false", n)
                   for k, n in [("emp", "Employees"), ("dept", "Departments"), ("org", "Org Chart")])
    views = "".join('<button type="button" class="ox-vbtn%s" data-ex-view="%s" aria-label="%s view" aria-pressed="%s">%s</button>' % (" is-on" if k == "kanban" else "", k, n, "true" if k == "kanban" else "false", svg)
                    for k, n, svg in [("kanban", "Kanban", V_KANBAN), ("list", "List", V_LIST)])
    out += sec(head("ONE PLACE FOR YOUR PEOPLE", "How Can Odoo Create a Central Hub for Your Workforce?",
                    "This is the Odoo Employees app with sample staff from a Chennai manufacturer. Filter by department, open an employee, move through the tabs, "
                    "and use the org chart on the right to jump to their manager or team.", "is-center")
               + '<div class="ox hr-ox hr-ex" data-ex><div class="ox-nav"><span class="ox-app">%s<b>Employees</b></span><span class="hr-menus" role="group" aria-label="Employees menu">%s</span>'
                 '<span class="ox-menu">Reporting</span><span class="ox-menu">Configuration</span><span class="ox-nav-r"><span class="ox-company">Your Company</span><span class="ox-av" style="--c:#8E4F83">L</span></span></div>'
                 '<div class="ox-cp"><div class="ox-cp-l"><button type="button" class="ox-new" data-ex-new>New</button><span class="ox-crumb ox-crumb--stack" data-ex-crumb></span></div>'
                 '<label class="ox-search">%s<span class="ox-facet" data-ex-facet hidden></span><input type="search" placeholder="Search..." aria-label="Search employees" data-ex-q></label>'
                 '<div class="ox-views" data-ex-views>%s</div></div><div class="ox-body hr-ex-body" data-ex-body></div></div>'
                 '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview with sample data. Pick a department, open an employee, or launch an onboarding plan.</p>'
                 % (app_icon, menu, SEARCH, views) + data("hr-emps", EMPS) + data("hr-depts", DEPTS) + data("hr-tagcol", TAGCOL), "hr-sec--explore", "explore")

    # 3 ---- structure records around your organization
    layers = [("Company", "Your Company Pvt Ltd", "One company, or several if you run separate legal entities with their own payroll."),
              ("Work locations", "Chennai HQ &middot; Coimbatore Plant &middot; Home", "Where people work, used for attendance, time off rules and reporting."),
              ("Departments", "7, nested under Management", "Each with a manager, so approvals and reports follow the hierarchy."),
              ("Job positions", "18 positions", "Sales Executive, Machine Operator and so on, shared with Recruitment."),
              ("Employee types", "Employee &middot; Worker &middot; Trainee &middot; Contractor", "Separates staff on payroll from contract and trainee workers."),
              ("Tags", "Shift A &middot; Shift B &middot; Field &middot; Leadership", "Free labels for groups that cut across departments.")]
    ly = "".join('<li><button type="button" class="hr-ly%s" data-ly="%d" aria-pressed="%s"><span class="mono">%02d</span><b>%s</b></button></li>'
                 % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", i + 1, n) for i, (n, v, x) in enumerate(layers))
    out += sec(head("YOUR STRUCTURE", "How Does Unisas Structure Employee Records Around Your Organization?",
                    "Before a single employee is imported we agree the structure: companies, locations, departments, positions and types. "
                    "Get this right and approvals, reports and access rules follow on their own. Click a department to see its record.", "is-center")
               + '<div class="hr-str"><div class="hr-tree ox-solo" data-tree><p class="hr-tree-h"><b>Your Company</b><small>Departments</small></p><ul class="hr-tree-l" data-tree-l></ul></div>'
                 '<div class="ox hr-ox hr-dept" data-dcard>%s<div class="hr-dept-b" data-dcard-b aria-live="polite"></div></div>'
                 '<div class="hr-layers"><ol>%s</ol><div class="hr-ly-card" data-ly-card aria-live="polite"></div></div></div>'
                 % (ox_head("Departments", "Department"), ly) + data("hr-layers", layers), "hr-sec--str")

    # 4 ---- onboarding, changes, offboarding
    onb = [("HR Officer", "Collect Aadhaar, PAN, bank details and photo", "Before day 1"), ("Admin", "Create user, email and badge ID", "Day 1"),
           ("Manager", "Plan the first week and introduce the team", "Day 1"), ("Employee", "Sign offer letter and policies in Odoo Sign", "Day 1"),
           ("Coach", "Safety induction on the line", "Day 2"), ("HR Officer", "Enrol for PF and ESI", "Week 1"), ("Manager", "30-day check-in", "Day 30")]
    off = [("Manager", "Exit interview"), ("Admin", "Collect laptop, ID card and keys"), ("Accounts", "Full and final settlement"),
           ("HR Officer", "Issue relieving and experience letters"), ("Admin", "Archive user and revoke access")]
    tabs4 = "".join('<button type="button" role="tab" class="hr-lt%s" data-lt="%s" aria-selected="%s">%s<small>%s</small></button>'
                    % (" is-on" if k == "on" else "", k, "true" if k == "on" else "false", n, x) for k, n, x in
                    [("on", "Onboarding", "Karthik joins the plant"), ("chg", "Change", "Priya is promoted"), ("off", "Offboarding", "Senthil resigns")])
    out += sec(head("JOINERS, MOVERS, LEAVERS", "How Can Odoo Simplify Onboarding, Employee Changes and Offboarding?",
                    "Odoo runs each event as a plan of activities assigned to the right people, and records every change on the employee. "
                    "Try all three: tick off an onboarding plan, promote someone, and register a departure.", "is-center")
               + '<div class="hr-life" data-life><div class="hr-lts" role="tablist" aria-label="Employee events">%s</div><div class="hr-life-b" data-life-b aria-live="polite"></div></div>'
                 % tabs4 + data("hr-onb", onb) + data("hr-off", off), "hr-sec--life")

    # 5 ---- workflows, roles and approvals
    modes = ["No Validation", "By Employee's Approver", "By Time Off Officer", "By Employee's Approver and Time Off Officer"]
    rtypes = [("Paid Time Off", 3), ("Sick Time Off", 1), ("Compensatory Days", 1), ("Unpaid", 3)]
    sel = "".join('<option value="%d">%s</option>' % (i, t) for i, (t, d) in enumerate(rtypes))
    mod = "".join('<option value="%d">%s</option>' % (i, m) for i, m in enumerate(modes))
    who = "".join('<option value="%d">%s</option>' % (e, n) for e, n in [(4, "Priya Raman &middot; Sales"), (8, "Anitha Selvam &middot; Production"), (12, "Vignesh Rao &middot; Accounts")])
    matrix = [("Employee", "Requests time off, logs attendance, submits expenses", "Own record"),
              ("Manager (Approver)", "Approves their team's time off, attendance and expenses", "Their team"),
              ("Time Off Officer", "Second approval, allocations, public holidays", "Everyone's time off"),
              ("HR Officer", "Creates and updates employee records, runs plans", "All employees"),
              ("HR Administrator", "Configuration, access rights, sensitive fields", "Everything")]
    out += sec(head("ROLES &amp; APPROVALS", "How Does Unisas Configure HR Workflows, Roles and Approval Responsibilities?",
                    "Each request type gets its own approval rule, and each employee their own approver, so requests reach the right person without anyone forwarding emails. "
                    "Set a rule, pick an employee and follow the request.", "is-center")
               + '<div class="hr-appr" data-appr><div class="ox hr-ox">%s<div class="hr-appr-f"><label><span>Time Off Type</span><select data-ap="type">%s</select></label>'
                 '<label><span>Approval</span><select data-ap="mode">%s</select></label><label><span>Employee</span><select data-ap="emp">%s</select></label>'
                 '<button type="button" class="ox-pbtn" data-ap-go>Submit request</button></div><ol class="hr-chain" data-ap-chain aria-live="polite"></ol></div>'
                 '<div class="hr-roles ox-solo"><p class="hr-roles-h"><b>Who does what</b><small>Set per user in Settings &rsaquo; Users</small></p><ul>%s</ul></div></div>'
                 % (ox_head("Time Off", "New Request"), sel, mod, who, "".join('<li><b>%s</b><span>%s</span><em>%s</em></li>' % m for m in matrix))
               + data("hr-rtypes", rtypes) + data("hr-modes", modes), "hr-sec--appr")

    # 6 ---- attendance, time off and working schedules
    scheds = [("Standard 48 hours/week", "Mon&ndash;Sat 09:00&ndash;18:00, 1 h lunch", [8, 8, 8, 8, 8, 8]),
              ("Office 40 hours/week", "Mon&ndash;Fri 09:30&ndash;18:30, 1 h lunch", [8, 8, 8, 8, 8, 0]),
              ("Shift B 45 hours/week", "Mon&ndash;Sat 14:00&ndash;22:00, 30 min break", [7.5, 7.5, 7.5, 7.5, 7.5, 7.5])]
    att = [["Mon 19", "08:56", "18:20", 8.4], ["Tue 20", "09:04", "18:04", 8.0], ["Wed 21", "08:50", "19:20", 9.5], ["Thu 22", "09:01", "18:07", 8.1], ["Fri 23", "09:10", "17:46", 7.6], ["Sat 24", "09:00", "18:00", 8.0]]
    sc = "".join('<label class="hr-sch"><input type="radio" name="hr-sch" value="%d"%s><span><b>%s</b><small>%s</small></span></label>' % (i, " checked" if i == 0 else "", n, x) for i, (n, x, h) in enumerate(scheds))
    out += sec(head("ATTENDANCE, TIME OFF &amp; SCHEDULES", "How Can Odoo Connect Attendance, Time Off and Employee Work Schedules?",
                    "The working schedule says how many hours each day should have. Attendance records what was worked, time off fills the gaps, and the difference becomes extra hours. "
                    "Change the schedule or add a day off and the week recalculates.", "is-center")
               + '<div class="hr-wk" data-wk><div class="hr-wk-side"><p class="hr-wk-h">Working Hours</p>%s<p class="hr-wk-h">This week</p>'
                 '<label class="hr-tg"><input type="checkbox" data-wk-sick><span class="hr-sw" aria-hidden="true"></span><span>Sick Time Off on Thursday</span></label>'
                 '<label class="hr-tg"><input type="checkbox" data-wk-hol><span class="hr-sw" aria-hidden="true"></span><span>Public holiday on Friday (Ayudha Puja)</span></label></div>'
                 '<div class="ox hr-ox hr-wk-main">%s<div class="hr-wk-grid" data-wk-grid></div><div class="hr-wk-tot" data-wk-tot aria-live="polite"></div></div></div>'
                 % (sc, ox_head("Attendances", "Suresh Babu &middot; Week 43")) + data("hr-sched", scheds) + data("hr-att", att), "hr-sec--wk")

    # 7 ---- access and sensitive information
    roles = [("self", "Priya (herself)"), ("peer", "A colleague"), ("mgr", "Her manager"), ("officer", "HR Officer"), ("admin", "HR Administrator")]
    # field, value, who can see (r) and edit (w)
    fields = [("Work email &amp; phone", "priya.raman@yourcompany.in", "self peer mgr officer admin", "officer admin"),
              ("Department &amp; manager", "Sales &middot; Kavya Nair", "self peer mgr officer admin", "officer admin"),
              ("Private address", "14, 3rd Cross St, Adyar, Chennai", "self officer admin", "self officer admin"),
              ("Emergency contact", "Raman K &middot; +91 94441 20387", "self mgr officer admin", "self officer admin"),
              ("Bank account", "HDFC Bank &middot;&middot;&middot; 4412", "self officer admin", "officer admin"),
              ("Aadhaar &amp; PAN", "XXXX XXXX 7731 &middot; ABCPR1234K", "self officer admin", "officer admin"),
              ("Salary (contract wage)", "&#8377; 42,000.00 / month", "admin", "admin"),
              ("Time off reason", "Sick: medical certificate attached", "self mgr officer admin", "officer admin"),
              ("Appraisal feedback", "Exceeds expectations; ready for a senior role", "self mgr admin", "mgr admin")]
    groups = {"self": [("Employees", "&mdash;"), ("Time Off", "&mdash;"), ("Attendances", "&mdash;"), ("Appraisals", "&mdash;"), ("Payroll", "&mdash;")],
              "peer": [("Employees", "&mdash;"), ("Time Off", "&mdash;"), ("Attendances", "&mdash;"), ("Appraisals", "&mdash;"), ("Payroll", "&mdash;")],
              "mgr": [("Employees", "&mdash;"), ("Time Off", "Approver"), ("Attendances", "Approver"), ("Appraisals", "Manager"), ("Payroll", "&mdash;")],
              "officer": [("Employees", "Officer: Manage all employees"), ("Time Off", "Officer"), ("Attendances", "Officer"), ("Appraisals", "&mdash;"), ("Payroll", "&mdash;")],
              "admin": [("Employees", "Administrator"), ("Time Off", "Administrator"), ("Attendances", "Administrator"), ("Appraisals", "Administrator"), ("Payroll", "Administrator")]}
    notes = {"self": "Employees see and update their own private details from <b>My Profile</b>, but cannot change their salary, department or bank account.",
             "peer": "Colleagues see a public profile: name, job, work contact and team. Nothing private.",
             "mgr": "Managers see what they need to manage: their team's time off, attendance and appraisals, not bank accounts or salary.",
             "officer": "HR Officers maintain records and private details. Salary sits in the contract, which only Payroll administrators open.",
             "admin": "Administrators see everything and every change is tracked in the chatter, so access to sensitive fields leaves a trail."}
    rb = "".join('<button type="button" class="hr-role%s" data-role="%s" aria-pressed="%s">%s</button>' % (" is-on" if k == "self" else "", k, "true" if k == "self" else "false", n) for k, n in roles)
    out += sec(head("ACCESS &amp; PRIVACY", "How Should Employee Access and Sensitive HR Information Be Controlled?",
                    "Bank details, identity numbers and salaries should be seen only by the people who need them. Odoo controls this per app and per field. "
                    "Look at Priya&rsquo;s record as different people would.", "is-center")
               + '<div class="hr-acc" data-acc><div class="hr-roles-b" role="group" aria-label="View as">%s</div><div class="hr-acc-g">'
                 '<div class="ox hr-ox">%s<table class="hr-acc-t" data-acc-t></table></div>'
                 '<div class="hr-acc-side"><div class="ox-solo hr-rights"><p class="hr-rights-h"><b>Access Rights</b><small data-acc-who></small></p><dl data-acc-g></dl></div><p class="hr-acc-note" data-acc-note aria-live="polite"></p></div></div></div>'
                 % (rb, ox_head("Employees", "Priya Raman")) + data("hr-fields", fields) + data("hr-groups", groups) + data("hr-notes", notes), "hr-sec--acc")

    # 8 ---- data migration: spreadsheet clean-up
    sheet = [["E001", "Arjun Mehta", "Management", "", "98410 22314", "01-06-2014", "18"],
             ["E014", "Priya Raman", "Sales", "Kavya Nair", "90030 55821", "04-07-2022", "9"],
             ["E027", "Anitha Selvam", "Prodn", "Suresh Babu", "97899 40112", "12/03/2023", "6"],
             ["E031", "Senthil M", "Stores", "Ravi Kumar", "94440 62109", "", "4"],
             ["E032", "Senthil Murugan", "Stores &amp; Logistics", "Ravi Kumar", "94440 62109", "15-01-2021", "4"],
             ["E040", "Vignesh Rao", "Accounts &amp; Admin", "Deepa K", "99620 71845", "2024-02-01", "5"]]
    issues = [("dept", "Department &lsquo;Prodn&rsquo; does not exist", "Map to Production", [[2, 2, "Production"]]),
              ("dup", "E031 and E032 share a mobile number", "Merge into E032", [[3, -1, ""]]),
              ("mgr", "Manager &lsquo;Deepa K&rsquo; not found", "Link to Deepa Krishnan", [[5, 3, "Deepa Krishnan"]]),
              ("date", "Dates in three formats", "Convert to DD-MM-YYYY", [[2, 5, "12-03-2023"], [5, 5, "01-02-2024"]])]
    load = [("Departments &amp; job positions", "7 &middot; 18"), ("Work locations &amp; schedules", "3 &middot; 3"), ("Employees, managers first", "42"),
            ("Users &amp; access rights", "29"), ("Opening leave balances", "42 allocations"), ("Documents", "Offer letters, ID proofs")]
    th = "".join("<th>%s</th>" % h for h in ["Emp Code", "Name", "Department", "Manager", "Mobile", "Joined", "Leave"])
    out += sec(head("DATA MIGRATION", "How Does Unisas Bring Existing Employee Data Into Odoo?",
                    "Most HR data arrives as a spreadsheet with years of small inconsistencies. We clean it before it goes in, with you deciding every merge. "
                    "Fix each issue and import.", "is-center")
               + '<div class="hr-mig" data-mig><div class="hr-sheet ox-solo"><p class="hr-sheet-h"><span class="hr-xls">XLS</span><b>employees_master_2026.xlsx</b><small>42 rows &middot; showing 6</small></p>'
                 '<div class="ox-scroll"><table class="hr-sheet-t"><thead><tr><th></th>%s</tr></thead><tbody data-mig-rows></tbody></table></div></div>'
                 '<div class="hr-iss ox-solo"><p class="hr-iss-h"><b>Issues found</b><small data-mig-n></small></p><ul data-mig-iss></ul>'
                 '<button type="button" class="ox-pbtn hr-mig-go" data-mig-go disabled>Import 42 employees</button><p class="hr-mig-res" data-mig-res aria-live="polite"></p></div>'
                 '<ol class="hr-load">%s</ol></div>'
                 % (th, "".join('<li><span class="mono">%02d</span><b>%s</b><em>%s</em></li>' % (i + 1, a, b) for i, (a, b) in enumerate(load)))
               + data("hr-sheet", sheet) + data("hr-iss", issues), "hr-sec--mig")

    # 9 ---- skills, development, performance
    skills = ["English", "Hindi", "Odoo Sales", "Negotiation", "CNC Operation", "Forklift Licence", "First Aid", "GST &amp; Tally"]
    matrix9 = [["Priya Raman", "#4C9F70", [3, 2, 3, 2, 0, 0, 1, 0]], ["Mohammed Irfan", "#C98600", [2, 3, 1, 3, 0, 0, 0, 0]], ["Kavya Nair", "#B5567E", [3, 2, 3, 3, 0, 0, 1, 1]],
               ["Suresh Babu", "#6B5B95", [1, 1, 0, 0, 3, 2, 3, 0]], ["Anitha Selvam", "#E07A5F", [1, 0, 0, 0, 2, 0, 1, 0]], ["Senthil Murugan", "#7A6C5D", [1, 2, 0, 1, 1, 3, 2, 1]],
               ["Fathima Begum", "#3D8DAE", [3, 2, 0, 0, 2, 0, 3, 0]], ["Vignesh Rao", "#5A7D9A", [3, 3, 1, 0, 0, 0, 0, 3]]]
    goals = [("Close &#8377; 40 lakh of new business", 80), ("Learn Odoo CRM reporting", 100), ("Mentor the new sales executive", 50)]
    t9 = "".join('<button type="button" class="hr-vtab%s" data-sk-tab="%s" aria-pressed="%s">%s</button>' % (" is-on" if k == "sk" else "", k, "true" if k == "sk" else "false", n) for k, n in [("sk", "Skills"), ("ap", "Appraisals")])
    out += sec(head("SKILLS &amp; PERFORMANCE", "How Can Odoo Help Track Employee Skills, Development and Performance?",
                    "Skills live on each employee with a level, so you can find who can cover a machine or a customer in seconds. Appraisals bring goals, both sides&rsquo; feedback and a final rating into one document.", "is-center")
               + '<div class="ox hr-ox hr-sk" data-sk><div class="ox-nav"><span class="ox-app">%s<b>Employees</b></span><span class="hr-vtabs" role="group" aria-label="Report">%s</span>'
                 '<span class="ox-nav-r"><span class="ox-company">Your Company</span><span class="ox-av" style="--c:#8E4F83">L</span></span></div><div class="hr-sk-b" data-sk-b></div></div>'
                 % (app_icon, t9) + data("hr-skills", skills) + data("hr-matrix", matrix9) + data("hr-goals", goals), "hr-sec--sk")

    # 10 ---- wider HR processes: the employee record at the centre
    apps = [("Recruitment", "#8E4F83", "Applicant &rarr; employee", "Job position, contact details, documents and the signed offer", "Headcount and open positions per department",
             "Karthik S hired as Machine Operator: employee created with his CV, offer and joining date."),
            ("Sign", "#1F8A78", "Offer letters &amp; policies", "Signed offer letter, NDA and policy acknowledgements", "Name, address and job title to fill the template",
             "Offer letter signed on his phone; the PDF is attached to his employee record."),
            ("Payroll", "#3E7CB1", "Salary &amp; statutory", "Payslips, PF and ESI numbers, tax regime", "Contract wage, attendance, unpaid leave and bank account",
             "October payslip: 26 working days, 1 unpaid day, PF and ESI deducted, posted to accounting."),
            ("Expenses", "#C98600", "Claims &amp; travel", "Reimbursements paid with salary or by bank", "Employee, manager as approver, bank account",
             "Priya's fuel claim of &#8377; 2,340 approved by Kavya and added to her payslip."),
            ("Timesheets", "#5A7D9A", "Time on projects", "Hours per project and task, billable or not", "Employee cost per hour and working schedule",
             "Installation team logs 42 h on the Bluebay project; cost flows to the project's margin."),
            ("Fleet", "#7A6C5D", "Company vehicles", "Assigned vehicle, fuel and service logs", "Driver = employee, released on exit",
             "Delivery van TN 38 BX 4412 assigned to Senthil; returned in his offboarding plan."),
            ("Documents", "#B5567E", "HR file", "ID proofs, certificates and letters in an Employees folder", "Access follows the employee's privacy rules",
             "Anitha's forklift certificate expires in 30 days; a renewal activity is scheduled for HR."),
            ("Appraisals", "#E07A5F", "Reviews &amp; goals", "Ratings, goals and feedback history", "Manager, department and skills",
             "Annual review cycle launched for 42 employees; managers get one appraisal per team member.")]
    nodes = "".join('<li style="--k:%d;--c:%s"><button type="button" class="hr-node%s" data-node="%d" aria-pressed="%s"><i></i><b>%s</b><small>%s</small></button></li>'
                    % (i, c, " is-on" if i == 0 else "", i, "true" if i == 0 else "false", n, t) for i, (n, c, t, a, b, x) in enumerate(apps))
    out += sec(head("WIDER HR PROCESSES", "How Does Unisas Connect Employee Management With Your Wider HR Processes?",
                    "The employee record is the hub. Hiring creates it, payroll and expenses read from it, appraisals and documents write back to it. Pick an app to see what flows each way.", "is-center")
               + '<div class="hr-hub" data-hub><div class="hr-ring" style="--n:%d"><div class="hr-core"><span>%s</span><b>Employee record</b><small class="mono">ONE DATABASE</small></div><ul>%s</ul></div>'
                 '<div class="hr-hub-card ox-solo" aria-live="polite"><p class="mono" data-hub-k></p><h3 data-hub-n></h3><dl><div><dt>Into the employee record</dt><dd data-hub-in></dd></div>'
                 '<div><dt>Read from the employee record</dt><dd data-hub-out></dd></div></dl><p class="hr-hub-ex" data-hub-ex></p></div></div>'
                 % (len(apps), app_icon, nodes) + data("hr-apps", apps), "hr-sec--hub")

    # 11 ---- which apps to implement
    qs = [("shift", "Staff work in shifts or on a factory floor"), ("leave", "Leave requests arrive by phone or WhatsApp"), ("hire", "We hire more than 10 people a year"),
          ("pay", "We run salaries in-house"), ("exp", "Staff travel and claim expenses"), ("time", "We track time on projects or bill clients for it"),
          ("rev", "We run yearly reviews"), ("car", "We have company vehicles")]
    happs = [("emp", "Employees", "#8E4F83", "", 1), ("leave", "Time Off", "#5DC1AA", "leave", 1), ("att", "Attendances", "#1F8A78", "shift", 1),
             ("rec", "Recruitment", "#B5567E", "hire", 1), ("pay", "Payroll", "#3E7CB1", "pay", 2), ("exp", "Expenses", "#C98600", "exp", 1),
             ("ts", "Timesheets", "#5A7D9A", "time", 1), ("apr", "Appraisals", "#E07A5F", "rev", 2), ("plan", "Planning", "#6B5B95", "shift", 2), ("fleet", "Fleet", "#7A6C5D", "car", 2)]
    ql = "".join('<li><label class="hr-q"><input type="checkbox" data-q="%s"><span class="hr-q-box" aria-hidden="true">%s</span><span>%s</span></label></li>' % (k, TICK, t) for k, t in qs)
    al = "".join('<li class="hr-app" data-app="%s" style="--c:%s"><span class="hr-app-ic">%s</span><b>%s</b><em data-app-st></em></li>' % (k, c, n[0], n) for k, n, c, q, ph in happs)
    out += sec(head("CHOOSING APPS", "Which Odoo HR Applications Should Your Business Actually Implement?",
                    "Not all of them, and not all at once. Start with what removes the most manual work, then add the rest once the basics run smoothly. "
                    "Tick what applies to you.", "is-center")
               + '<div class="hr-pick" data-apppick><ul class="hr-qs">%s</ul><div class="hr-apps-w ox-solo"><p class="hr-apps-h"><b>Your recommended setup</b><small data-pick-sum></small></p>'
                 '<ul class="hr-apps">%s</ul><p class="hr-legend"><span class="is-1">Phase 1</span><span class="is-2">Phase 2</span><span class="is-0">Not needed yet</span></p></div></div>'
                 % (ql, al) + data("hr-happs", happs), "hr-sec--pick")

    # 12 ---- what Unisas handles
    raci = [("disc", "Discover", [("HR process workshops with HR and managers", "u"), ("Leave, attendance and approval policies agreed", "b"), ("Access rights by role", "u"), ("Sign-off on the design", "y")]),
            ("cfg", "Configure", [("Departments, positions and locations", "u"), ("Time off types, allocations and holidays", "u"), ("Working schedules and attendance devices", "u"), ("Activity plans for joiners and leavers", "u"), ("Letter and contract templates", "b")]),
            ("data", "Data", [("Employee spreadsheet export", "y"), ("Cleaning, merging and mapping", "u"), ("Opening leave balances checked", "b"), ("Import and verification", "u")]),
            ("go", "Train &amp; go live", [("Training for HR, managers and employees", "u"), ("Mobile app and kiosk set up", "u"), ("Parallel month of leave and attendance", "b"), ("Go-live announcement to staff", "y")]),
            ("after", "After go-live", [("Hypercare for the first month", "u"), ("New policies and changes", "b"), ("Quarterly review of HR reports", "u")])]
    rt = "".join('<button type="button" class="hr-rt%s" data-rt="%d" aria-pressed="%s">%s</button>' % (" is-on" if i == 0 else "", i, "true" if i == 0 else "false", n) for i, (k, n, r) in enumerate(raci))
    out += sec(head("WHAT WE HANDLE", "What Does Unisas Handle During HR System Implementation?",
                    "Almost all of it. You bring the decisions and the data; we do the configuration, cleaning, testing and training. Here is who does what in each phase.", "is-center")
               + '<div class="hr-raci ox-solo" data-raci><div class="hr-rts" role="group" aria-label="Phase">%s</div><table class="hr-raci-t"><thead><tr><th>Task</th><th>Unisas</th><th>Together</th><th>You</th></tr></thead><tbody data-raci-b></tbody></table>'
                 '<p class="hr-raci-sum" data-raci-sum></p></div>' % rt + data("hr-raci", raci), "hr-sec--raci")

    # 13 ---- plan the setup
    out += sec('<div class="hr-plan"><div>%s<div class="cta-row"><a href="#get-demo" class="btn btn-primary btn-red" data-svc-cta="implementation">Plan my HR setup %s</a></div></div>'
               '<div class="hr-pl ox-solo" data-pl><p class="hr-pl-h"><b>HR setup planner</b><small>A first estimate. We confirm it after a short call.</small></p>'
               '<div class="hr-pl-in"><label><span>Employees <b data-pl-o="emp">40</b></span><input type="range" min="5" max="500" step="5" value="40" data-pl="emp"></label>'
               '<label><span>Locations <b data-pl-o="loc">2</b></span><input type="range" min="1" max="10" value="2" data-pl="loc"></label>'
               '<label><span>Current records</span><select data-pl="src"><option value="1">Excel sheets</option><option value="0">Paper files</option><option value="2">Another HR software</option></select></label>'
               '<div class="hr-pl-chk"><label><input type="checkbox" data-pl-x="shift" checked> Shift workers and biometric devices</label><label><input type="checkbox" data-pl-x="pay"> Payroll in Odoo</label>'
               '<label><input type="checkbox" data-pl-x="rec"> Recruitment and appraisals</label></div></div>'
               '<div class="hr-pl-out"><div class="hr-pl-wk" data-pl-wk></div><ol class="hr-pl-road" data-pl-road></ol><p class="hr-pl-tot" data-pl-tot aria-live="polite"></p></div></div></div>'
               % (head("PLAN YOUR SETUP", "How Can We Plan an Odoo HR Setup Around Your Workforce?",
                       "Size, locations, shifts and payroll decide the plan more than anything else. Most small businesses go live with Employees, Time Off and Attendances "
                       "in a few weeks, then add payroll once a clean month of attendance is in. Try the planner, then talk it through with us."), g["ARROW"]), "hr-sec--plan")

    # 14 ---- why Unisas
    why = [("Built around how you work", "We map your leave rules, shifts and approvals first, then configure Odoo to them, so nobody has to learn a new process on day one.",
            '<span class="ox-sbar is-mini"><span class="ox-sb is-done">To Approve</span><span class="ox-sb is-cur">Approved</span></span>'),
           ("Indian HR rules understood", "Leave policies, PF and ESI, professional tax and labour-law registers set up the way your auditor and payroll partner expect.",
            '<span class="hr-why-chips"><span>PF</span><span>ESI</span><span>PT</span><span>TDS</span></span>'),
           ("Small-business sized", "Fixed scope and a short timeline. We start with the apps that save time now and add the rest when you are ready.",
            '<span class="hr-why-chips"><span>Employees</span><span>Time Off</span><span>Attendances</span></span>'),
           ("Support after go-live", "A named consultant for the first month and a support desk after, for new policies, new locations and new joiners.",
            '<span class="hr-why-live"><i></i>Hypercare &middot; Active</span>')]
    out += sec(head("WHY UNISAS", "Why Choose Unisas for Your Odoo HR Implementation?",
                    "One team that understands both people processes and Odoo, from the first workshop to long after go-live.", "is-center")
               + '<ol class="hr-why">%s</ol>' % "".join('<li><span class="hr-why-top ox-solo" aria-hidden="true">%s</span><h3>%s</h3><p>%s</p></li>' % (b, t, x) for t, x, b in why), "hr-sec--why")

    return out + JS


FAQ = [("Is Odoo HR suitable for a small business with 10 to 50 employees?",
        "Yes. Odoo Employees, Time Off and Attendances work well for small teams, and you pay only for the apps you use. Most of our small-business clients start with those three and add Payroll or Recruitment later."),
       ("Can employees apply for leave and check in from their phones?",
        "Yes. Employees use the Odoo mobile app or browser to request time off, see their balance and check in, with geolocation if you want it. Managers approve from the same app."),
       ("Can Odoo connect to our biometric attendance machine?",
        "Usually, yes. Most common biometric devices can push check-ins to Odoo through a connector or a scheduled import. We confirm your device model during scoping."),
       ("Does Odoo payroll handle PF, ESI and professional tax?",
        "Odoo Payroll with the Indian localization supports salary structures with PF, ESI and professional tax. We validate the rules with your accountant before the first payroll run, or keep payroll with your current provider and send attendance from Odoo."),
       ("How do you keep salary and personal details private?",
        "Access rights are set per role. Employees see their own record, managers see their team's time off and appraisals, and only HR and payroll administrators see bank accounts, identity numbers and salaries."),
       ("How long does an Odoo HR implementation take?",
        "For a company of up to 100 people, Employees, Time Off and Attendances typically go live in 4 to 6 weeks. Payroll adds 3 to 4 weeks, including a parallel month to compare payslips."),
       ("Can we move our existing employee data and leave balances?",
        "Yes. We import employees, departments, managers and documents from your spreadsheets or current software, and load each person's leave balance as an opening allocation, checked with you before go-live.")]

CTA = ("Let's Map Your HR Processes to Odoo",
       "Tell us how your team handles employee records, leave and attendance today. We'll show you the same processes in Odoo and recommend the apps and setup that fit your business.")


JS = r'''<script>
(function(){
  function J(id){var e=document.getElementById(id);return e?JSON.parse(e.textContent):null;}
  function press(group,el){group.forEach(function(b){var on=b===el;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});}
  function num(n,d){return n.toLocaleString('en-IN',{minimumFractionDigits:d||0,maximumFractionDigits:d||0});}
  function ini(n){return n.split(' ').map(function(w){return w[0];}).slice(0,2).join('');}
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}

  /* --- 1 scattered data --- */
  (function(){var box=document.querySelector('[data-scat]');if(!box)return;var C=J('hr-cf'),pick={};
    function draw(){var n=Object.keys(pick).length,right=0;
      box.querySelector('[data-cf-n]').textContent=n+' of '+C.length+' resolved';
      box.querySelector('[data-cf-rec]').innerHTML=C.map(function(c,i){var p=pick[i];if(p!==undefined&&p===c[2])right++;
        return '<div class="'+(p===undefined?'is-empty':(p===c[2]?'is-ok':'is-bad'))+'"><dt>'+c[0]+'</dt><dd>'+(p===undefined?'&mdash;':c[1][p][1])+'</dd></div>';}).join('');
      box.querySelector('[data-cf-res]').innerHTML=n<C.length?'':(right===C.length?'<b>One record, one answer.</b> Payroll, managers and the employee now all read the same value.':'<b>'+right+' of 6 right.</b> Red fields would have gone into payroll wrong. This is why we verify with each source.');
      box.querySelectorAll('[data-cf]').forEach(function(li){var i=+li.getAttribute('data-cf');li.querySelectorAll('[data-pick]').forEach(function(b){var j=+b.getAttribute('data-pick');
        b.classList.toggle('is-on',pick[i]===j);b.classList.toggle('is-ok',pick[i]!==undefined&&j===C[i][2]);b.classList.toggle('is-bad',pick[i]===j&&j!==C[i][2]);});});}
    box.addEventListener('click',function(e){var b=e.target.closest('[data-pick]');if(!b)return;var i=+b.closest('[data-cf]').getAttribute('data-cf');pick[i]=+b.getAttribute('data-pick');
      box.querySelector('[data-cf-why]').innerHTML='<b>'+C[i][0]+':</b> '+C[i][3];draw();});
    draw();})();

  /* --- 2 employees explorer --- */
  (function(){var ex=document.querySelector('[data-ex]');if(!ex)return;
    var E=J('hr-emps'),D=J('hr-depts'),TC=J('hr-tagcol'),body=ex.querySelector('[data-ex-body]'),crumb=ex.querySelector('[data-ex-crumb]'),q=ex.querySelector('[data-ex-q]'),facet=ex.querySelector('[data-ex-facet]');
    var menus=[].slice.call(ex.querySelectorAll('[data-ex-menu]')),vbs=[].slice.call(ex.querySelectorAll('[data-ex-view]'));
    var st={menu:'emp',view:'kanban',dept:'',open:null,tab:'resume',plan:false};
    var DK={};D.forEach(function(d){DK[d.k]=d;});
    var PL={on:[['HR Officer','Collect documents'],['Admin','Create user and badge'],['Manager','Plan first week'],['Employee','Sign offer letter']],off:[['Manager','Exit interview'],['Admin','Collect laptop and ID card'],['Accounts','Full and final settlement']]};
    E.forEach(function(e){e.acts=[];e.log=[{w:'Lakshmi Iyer',t:'Employee created'}];});
    function emp(id){return E.filter(function(e){return e.id===id;})[0];}
    function av(e,cls){return '<span class="hr-av '+(cls||'')+'" style="--c:'+e.c+'">'+ini(e.n)+'</span>';}
    function pres(e){return e.p==='in'?'<span class="hr-pr is-in" title="Present"></span>':(e.p==='off'?'<span class="hr-pr is-off" title="On time off">&#9992;</span>':'<span class="hr-pr is-out" title="Not checked in"></span>');}
    function mail(e){return e.n.toLowerCase().split(' ')[0]+'.'+e.n.toLowerCase().split(' ').slice(-1)[0]+'@yourcompany.in';}
    function phone(e){return '+91 9'+(8400000000+e.id*731557).toString().slice(0,4)+' '+(10000+e.id*3917).toString().slice(0,5);}
    function tags(e){return e.tags.map(function(t){return '<span class="ox-tag ox-tag--'+TC[t]+'">'+t+'</span>';}).join('');}
    function list(){var t=q.value.trim().toLowerCase();return E.filter(function(e){return (!st.dept||e.d===st.dept)&&(!t||(e.n+' '+e.job+' '+DK[e.d].n).toLowerCase().indexOf(t)>-1);});}
    function side(){var c={};E.forEach(function(e){c[e.d]=(c[e.d]||0)+1;});
      return '<aside class="hr-side"><p class="hr-side-h">Department</p><button type="button" data-dep="" class="'+(st.dept?'':'is-on')+'">All <small>'+E.length+'</small></button>'+
        D.map(function(d){return '<button type="button" data-dep="'+d.k+'" class="'+(st.dept===d.k?'is-on':'')+(d.parent&&d.parent!=='mgmt'?' is-sub':'')+'">'+d.n+' <small>'+c[d.k]+'</small></button>';}).join('')+'</aside>';}
    function kanban(L){return '<div class="hr-kb">'+side()+'<div class="hr-cards">'+(L.length?L.map(function(e){
        return '<article class="hr-card" data-emp="'+e.id+'" tabindex="0">'+av(e,'is-lg')+'<div class="hr-card-b"><b>'+e.n+'</b><span>'+e.job+'</span><small>'+mail(e)+'</small><small>'+phone(e)+'</small><span class="ox-tags">'+tags(e)+'</span></div>'+pres(e)+'</article>';}).join(''):'<p class="ox-empty">No employee matches.</p>')+'</div></div>';}
    function table(L){return '<div class="ox-scroll"><table class="ox-table"><thead><tr><th class="ox-chk"><span class="ox-cb"></span></th><th>Employee Name</th><th>Work Phone</th><th>Work Email</th><th>Department</th><th>Job Position</th><th>Manager</th></tr></thead><tbody>'+
      L.map(function(e){var m=emp(e.m);return '<tr data-emp="'+e.id+'" tabindex="0"><td class="ox-chk"><span class="ox-cb"></span></td><td><span class="ox-sp">'+av(e,'is-sm')+'<b>'+e.n+'</b></span></td><td>'+phone(e)+'</td><td class="ox-muted">'+mail(e)+'</td><td>'+DK[e.d].n+'</td><td>'+e.job+'</td><td>'+(m?'<span class="ox-sp">'+av(m,'is-sm')+m.n+'</span>':'')+'</td></tr>';}).join('')+'</tbody></table></div>';}
    function depts(){return '<div class="hr-dk">'+D.map(function(d){var n=E.filter(function(e){return e.d===d.k;}),off=n.filter(function(e){return e.p==='off';}).length,m=emp(d.mgr);
        return '<article class="hr-dc" data-dep-open="'+d.k+'" tabindex="0"><header><b>'+d.n+'</b><small>'+(d.parent?DK[d.parent].n+' / ':'')+d.loc+'</small></header><div class="hr-dc-b"><span class="ox-pbtn">'+n.length+' Employees</span>'+
          '<dl><div><dt>Manager</dt><dd>'+m.n+'</dd></div><div><dt>Absence</dt><dd class="'+(off?'is-warn':'')+'">'+off+'</dd></div><div><dt>Time Off Requests</dt><dd>'+(d.k==='prod'?2:(d.k==='sales'?1:0))+'</dd></div></dl></div></article>';}).join('')+'</div>';}
    function org(){function node(e){var kids=E.filter(function(x){return x.m===e.id;});
        return '<li><button type="button" class="hr-on" data-emp="'+e.id+'">'+av(e,'is-sm')+'<span><b>'+e.n+'</b><small>'+e.job+'</small></span>'+(kids.length?'<em>'+kids.length+'</em>':'')+'</button>'+(kids.length?'<ul>'+kids.map(node).join('')+'</ul>':'')+'</li>';}
      return '<div class="ox-scroll"><ul class="hr-org">'+node(emp(1))+'</ul></div>';}
    function form(e){var m=emp(e.m),mm=m&&emp(m.m),team=E.filter(function(x){return x.m===e.id;});
      var tabs=[['resume','Resume'],['work','Work Information'],['private','Private Information'],['hr','HR Settings']].map(function(t){return '<button type="button" data-tab="'+t[0]+'" class="'+(st.tab===t[0]?'is-on':'')+'">'+t[1]+'</button>';}).join('');
      var tb;
      if(st.tab==='resume')tb='<div class="hr-res"><div><p class="hr-gi-h">Resume</p><ul class="hr-rl"><li><b>'+e.job+'</b><small>Your Company &middot; '+e.join+' &ndash; present</small></li>'+
        (e.id>1?'<li><b>'+(e.d==='prod'||e.d==='qc'||e.d==='store'?'Technician':(e.d==='sales'?'Sales Associate':'Executive'))+'</b><small>Previous employer &middot; 3 years</small></li>':'')+'<li><b>'+(e.d==='prod'||e.d==='qc'?'Diploma in Mechanical Engineering':(e.d==='acct'?'B.Com':'Bachelor’s degree'))+'</b><small>Education</small></li></ul></div>'+
        '<div><p class="hr-gi-h">Skills</p><ul class="hr-skl">'+(e.d==='sales'?[['Languages','English','Expert',100],['Languages','Hindi','Intermediate',60],['Sales','Negotiation','Advanced',80]]:(e.d==='prod'||e.d==='qc'||e.d==='store'?[['Machines','CNC Operation','Advanced',80],['Safety','First Aid','Certified',100],['Languages','English','Beginner',30]]:[['Languages','English','Expert',100],['Software','Odoo','Intermediate',60],['Finance','GST &amp; Tally','Advanced',80]])).map(function(s){return '<li><small>'+s[0]+'</small><b>'+s[1]+'</b><span><i style="--w:'+s[3]+'"></i></span><em>'+s[2]+'</em></li>';}).join('')+'</ul></div></div>';
      if(st.tab==='work')tb='<div class="hr-gi"><div><p class="hr-gi-h">Location</p><dl><div><dt>Work Address</dt><dd>'+(e.loc==='Chennai HQ'?'Your Company, Guindy, Chennai':'Your Company, SIDCO, Coimbatore')+'</dd></div><div><dt>Work Location</dt><dd>'+e.loc+'</dd></div></dl>'+
        '<p class="hr-gi-h">Approvers</p><dl><div><dt>Time Off</dt><dd>'+(m?m.n:'Lakshmi Iyer')+'</dd></div><div><dt>Attendance</dt><dd>'+(m?m.n:'Lakshmi Iyer')+'</dd></div><div><dt>Expense</dt><dd>'+(m?m.n:'Deepa Krishnan')+'</dd></div></dl></div>'+
        '<div><p class="hr-gi-h">Schedule</p><dl><div><dt>Working Hours</dt><dd>'+(e.tags.indexOf('Shift B')>-1?'Shift B 45 hours/week':(e.loc==='Chennai HQ'?'Office 40 hours/week':'Standard 48 hours/week'))+'</dd></div><div><dt>Timezone</dt><dd>Asia/Kolkata</dd></div></dl></div></div>';
      if(st.tab==='private')tb='<div class="hr-gi"><div><p class="hr-gi-h">Private Contact</p><dl><div><dt>Private Address</dt><dd>'+(e.loc==='Chennai HQ'?'Chennai, Tamil Nadu':'Coimbatore, Tamil Nadu')+'</dd></div><div><dt>Private Phone</dt><dd>+91 9xxxx x'+(1000+e.id*37)+'</dd></div><div><dt>Bank Account</dt><dd>HDFC Bank &middot;&middot;&middot; '+(4400+e.id*13)+'</dd></div></dl>'+
        '<p class="hr-gi-h">Emergency</p><dl><div><dt>Contact</dt><dd>Family member</dd></div></dl></div><div><p class="hr-gi-h">Citizenship</p><dl><div><dt>Nationality</dt><dd>India</dd></div><div><dt>Identification No</dt><dd>XXXX XXXX '+(7000+e.id*41)+'</dd></div></dl>'+
        '<p class="hr-lock">&#128274; Only HR Officers and the employee see this tab.</p></div></div>';
      if(st.tab==='hr')tb='<div class="hr-gi"><div><p class="hr-gi-h">Status</p><dl><div><dt>Employee Type</dt><dd>'+e.type+'</dd></div><div><dt>Related User</dt><dd>'+(e.type==='Worker'?'<span class="ox-muted">None (kiosk only)</span>':e.n)+'</dd></div></dl></div>'+
        '<div><p class="hr-gi-h">Attendance / Point of Sale</p><dl><div><dt>Badge ID</dt><dd class="mono">0410'+(2200+e.id)+'</dd></div><div><dt>PIN Code</dt><dd>&bull;&bull;&bull;&bull;</dd></div></dl></div></div>';
      var acts=e.acts.length?e.acts.map(function(a,i){return '<div class="ox-pa"><span class="ox-pa-ic ox-act--orange">&#9711;</span><div><p><b class="ox-t-orange">Due in '+(i+1)+' days:</b> <b>'+a[1]+'</b> for '+a[0]+'</p></div></div>';}).join(''):'<p class="ox-muted ox-pa-none">No planned activities.</p>';
      var planBox=st.plan?'<div class="hr-planbox"><p><b>Launch Plan</b></p><button type="button" class="ox-pbtn" data-plan="on">Onboarding</button><button type="button" class="ox-sbtn" data-plan="off">Offboarding</button><button type="button" class="ox-sbtn" data-plan-x>Cancel</button></div>':'';
      var chart='<div class="hr-oc"><p class="hr-gi-h">Organization Chart</p>'+(mm?'<button type="button" class="hr-oc-n is-up" data-emp="'+mm.id+'">'+av(mm,'is-sm')+'<span><b>'+mm.n+'</b><small>'+mm.job+'</small></span></button>':'')+
        (m?'<button type="button" class="hr-oc-n is-up" data-emp="'+m.id+'">'+av(m,'is-sm')+'<span><b>'+m.n+'</b><small>'+m.job+'</small></span></button>':'')+
        '<div class="hr-oc-n is-me">'+av(e,'is-sm')+'<span><b>'+e.n+'</b><small>'+e.job+'</small></span></div>'+
        (team.length?'<div class="hr-oc-team">'+team.map(function(t){return '<button type="button" class="hr-oc-n" data-emp="'+t.id+'">'+av(t,'is-sm')+'<span><b>'+t.n+'</b><small>'+t.job+'</small></span></button>';}).join('')+'</div>':'')+'</div>';
      return '<div class="ox-form hr-form"><div class="ox-f-main"><div class="ox-f-bar"><span class="ox-f-btns"><button type="button" class="ox-sbtn" data-plan-open>Launch Plan</button></span>'+
        '<span class="hr-smart"><span class="hr-sb"><b>'+num(e.att,1)+' h</b>Attendance</span><span class="hr-sb"><b>'+e.to+' days</b>Time Off</span><span class="hr-sb"><b>'+(3+e.id%4)+'</b>Documents</span></span></div>'+planBox+
        '<div class="ox-sheet"><div class="hr-f-top"><div><h3>'+e.n+' '+pres(e)+'</h3><p class="hr-f-job">'+e.job+'</p><span class="ox-tags">'+tags(e)+'</span></div>'+av(e,'is-xl')+'</div>'+
        '<dl class="ox-fields"><div><dt>Work Email</dt><dd>'+mail(e)+'</dd></div><div><dt>Department</dt><dd>'+DK[e.d].n+'</dd></div>'+
        '<div><dt>Work Phone</dt><dd>'+phone(e)+'</dd></div><div><dt>Job Position</dt><dd>'+e.job+'</dd></div>'+
        '<div><dt>Company</dt><dd>Your Company</dd></div><div><dt>Manager</dt><dd>'+(m?av(m,'is-sm')+m.n:'')+'</dd></div>'+
        '<div><dt>Joined</dt><dd>'+e.join+'</dd></div><div><dt>Coach</dt><dd>'+(m?av(m,'is-sm')+m.n:'')+'</dd></div></dl>'+
        '<div class="ox-ftabs hr-ftabs">'+tabs+'</div><div class="hr-tab-b">'+tb+'</div></div></div>'+
        '<aside class="ox-chatter">'+chart+'<p class="ox-ch-sep">Planned Activities</p>'+acts+'<p class="ox-ch-sep">Today</p>'+e.log.slice().reverse().map(function(l){return '<div class="ox-msg"><span class="hr-av is-sm" style="--c:#8E4F83">'+ini(l.w)+'</span><div><p><b>'+l.w+'</b> <small>just now</small></p><p>'+l.t+'</p></div></div>';}).join('')+'</aside></div>';}
    function render(){
      ex.querySelector('[data-ex-views]').hidden=st.menu!=='emp'||!!st.open;vbs.forEach(function(b){var on=b.getAttribute('data-ex-view')===st.view;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
      menus.forEach(function(b){var on=b.getAttribute('data-ex-menu')===st.menu;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
      facet.hidden=!st.dept;facet.innerHTML=st.dept?'Department: '+DK[st.dept].n+' <button type="button" data-dep="" aria-label="Remove filter">&times;</button>':'';
      if(st.open){var e=emp(st.open);crumb.innerHTML='<a href="#" data-back>Employees</a><span>'+e.n+'</span>';body.innerHTML=form(e);return;}
      crumb.innerHTML='<span>'+{emp:'Employees',dept:'Departments',org:'Organization Chart'}[st.menu]+'</span>';
      body.innerHTML=st.menu==='dept'?depts():(st.menu==='org'?org():(st.view==='list'?table(list()):kanban(list())));}
    menus.forEach(function(b){b.addEventListener('click',function(){st.menu=b.getAttribute('data-ex-menu');st.open=null;render();});});
    vbs.forEach(function(b){b.addEventListener('click',function(){st.view=b.getAttribute('data-ex-view');render();});});
    ex.querySelector('[data-ex-new]').addEventListener('click',function(){st.menu='emp';st.open=null;st.dept='';q.value='';render();});
    q.addEventListener('input',function(){st.menu='emp';st.open=null;render();});
    ex.addEventListener('click',function(e){
      var d=e.target.closest('[data-dep]');if(d){st.dept=d.getAttribute('data-dep');st.menu='emp';st.open=null;render();return;}
      var dp=e.target.closest('[data-dep-open]');if(dp){st.dept=dp.getAttribute('data-dep-open');st.menu='emp';render();return;}
      if(e.target.closest('[data-back]')){e.preventDefault();st.open=null;render();return;}
      var t=e.target.closest('[data-tab]');if(t){st.tab=t.getAttribute('data-tab');render();return;}
      if(e.target.closest('[data-plan-open]')){st.plan=true;render();return;}
      if(e.target.closest('[data-plan-x]')){st.plan=false;render();return;}
      var p=e.target.closest('[data-plan]');if(p&&st.open){var em=emp(st.open),k=p.getAttribute('data-plan');em.acts=PL[k].slice();em.log.push({w:'Lakshmi Iyer',t:'Plan <b>'+(k==='on'?'Onboarding':'Offboarding')+'</b> launched: '+PL[k].length+' activities scheduled'});st.plan=false;render();return;}
      var r=e.target.closest('[data-emp]');if(r){st.open=+r.getAttribute('data-emp');st.menu='emp';st.tab='resume';st.plan=false;render();}
    });
    ex.addEventListener('keydown',function(e){if(e.key!=='Enter')return;var r=e.target.closest&&e.target.closest('article[data-emp],tr[data-emp],[data-dep-open]');if(r){e.preventDefault();r.click();}});
    render();})();

  /* --- 3 structure --- */
  (function(){var tr=document.querySelector('[data-tree]');if(!tr)return;var E=J('hr-emps'),D=J('hr-depts'),L=J('hr-layers'),cur='prod',card=document.querySelector('[data-dcard-b]');
    function emp(id){return E.filter(function(e){return e.id===id;})[0];}
    function lvl(d){var n=0;while(d.parent){n++;d=D.filter(function(x){return x.k===d.parent;})[0];}return n;}
    function draw(){tr.querySelector('[data-tree-l]').innerHTML=D.map(function(d){var n=E.filter(function(e){return e.d===d.k;}).length;
        return '<li style="--l:'+lvl(d)+'"><button type="button" data-dk="'+d.k+'" class="'+(d.k===cur?'is-on':'')+'" aria-pressed="'+(d.k===cur)+'"><b>'+d.n+'</b><small>'+n+'</small></button></li>';}).join('');
      var d=D.filter(function(x){return x.k===cur;})[0],m=emp(d.mgr),par=D.filter(function(x){return x.k===d.parent;})[0],P=E.filter(function(e){return e.d===cur;});
      card.innerHTML='<div class="hr-dept-s"><h3>'+d.n+'</h3><dl class="ox-fields"><div><dt>Manager</dt><dd><span class="hr-av is-sm" style="--c:'+m.c+'">'+ini(m.n)+'</span>'+m.n+'</dd></div><div><dt>Parent Department</dt><dd>'+(par?par.n:'<span class="ox-muted">None</span>')+'</dd></div>'+
        '<div><dt>Company</dt><dd>Your Company</dd></div><div><dt>Work Location</dt><dd>'+d.loc+'</dd></div></dl><p class="hr-gi-h">Employees ('+P.length+')</p><ul class="hr-dept-e">'+
        P.map(function(e){return '<li><span class="hr-av is-sm" style="--c:'+e.c+'">'+ini(e.n)+'</span><b>'+e.n+'</b><span>'+e.job+'</span><em>'+e.type+'</em></li>';}).join('')+'</ul>'+
        '<p class="hr-dept-note">Time off and attendance for this team route to <b>'+m.n+'</b> by default.</p></div>';}
    tr.addEventListener('click',function(e){var b=e.target.closest('[data-dk]');if(b){cur=b.getAttribute('data-dk');draw();}});draw();
    var lb=[].slice.call(document.querySelectorAll('[data-ly]')),lc=document.querySelector('[data-ly-card]');
    function ld(i){lc.innerHTML='<b>'+L[i][1]+'</b><span>'+L[i][2]+'</span>';}
    lb.forEach(function(b){b.addEventListener('click',function(){press(lb,b);ld(+b.getAttribute('data-ly'));});});ld(0);})();

  /* --- 4 joiners, movers, leavers --- */
  (function(){var lf=document.querySelector('[data-life]');if(!lf)return;var ON=J('hr-onb'),OFF=J('hr-off'),b=lf.querySelector('[data-life-b]'),tabs=[].slice.call(lf.querySelectorAll('[data-lt]'));
    var st={tab:'on',done:{},chg:{job:'Sales Executive',loc:'Chennai HQ',mgr:'Kavya Nair'},saved:null,dep:null};
    function on(){var n=Object.keys(st.done).filter(function(k){return st.done[k];}).length;
      return '<div class="hr-l-grid"><div class="ox hr-ox">'+'<div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Karthik S</a><span>Onboarding plan</span></span></div><span></span><span></span></div>'+
        '<ul class="hr-acts">'+ON.map(function(a,i){return '<li class="'+(st.done[i]?'is-done':'')+'"><label><input type="checkbox" data-od="'+i+'"'+(st.done[i]?' checked':'')+'><span class="hr-chk" aria-hidden="true">✓</span><span><b>'+a[1]+'</b><small>'+a[0]+' &middot; '+a[2]+'</small></span></label></li>';}).join('')+'</ul></div>'+
        '<div class="hr-l-side ox-solo"><p class="hr-gi-h">Progress</p><p class="hr-l-big">'+n+' <small>of '+ON.length+'</small></p><span class="hr-bar"><i style="--w:'+(n/ON.length*100)+'"></i></span>'+
        '<p class="hr-l-note">'+(n===ON.length?'<b>Onboarding complete.</b> Karthik has his badge, user and signed documents, and his manager has a 30-day check-in booked.':'Each activity lands in the right person&rsquo;s Odoo inbox with a due date, so nothing depends on HR remembering.')+'</p></div></div>';}
    function chg(){var c=st.chg,opt=function(k,v){return v.map(function(x){return '<option'+(x===c[k]?' selected':'')+'>'+x+'</option>';}).join('');};
      var log=st.saved?st.saved.map(function(l){return '<li><b>'+l[0]+':</b> '+l[1]+' &rarr; <b>'+l[2]+'</b></li>';}).join(''):'';
      return '<div class="hr-l-grid"><div class="ox hr-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Employees</a><span>Priya Raman</span></span></div><span></span><span><button type="button" class="ox-pbtn" data-save>Save</button></span></div>'+
        '<div class="hr-chg"><label><span>Job Position</span><select data-c="job">'+opt('job',['Sales Executive','Senior Sales Executive','Area Sales Manager'])+'</select></label>'+
        '<label><span>Work Location</span><select data-c="loc">'+opt('loc',['Chennai HQ','Coimbatore Plant'])+'</select></label>'+
        '<label><span>Manager</span><select data-c="mgr">'+opt('mgr',['Kavya Nair','Arjun Mehta'])+'</select></label></div></div>'+
        '<div class="hr-l-side ox-solo"><p class="hr-gi-h">Chatter</p>'+(log?'<div class="ox-msg"><span class="hr-av is-sm" style="--c:#8E4F83">LI</span><div><p><b>Lakshmi Iyer</b> <small>just now</small></p><ul class="hr-track">'+log+'</ul></div></div>':'<p class="hr-l-note">Change a field and save. Odoo tracks the old and new value, who changed it and when.</p>')+
        (st.saved&&st.saved.length?'<p class="hr-l-note">Approvers follow automatically: her time off now goes to <b>'+c.mgr+'</b>.</p>':'')+'</div></div>';}
    function off(){var d=st.dep;
      return '<div class="hr-l-grid"><div class="ox hr-ox"><div class="ox-cp"><div class="ox-cp-l"><span class="ox-crumb ox-crumb--stack"><a>Employees</a><span>Senthil Murugan</span></span></div><span></span><span></span></div>'+
        (d?'<div class="hr-arch"><span class="ox-ribbon is-lost">ARCHIVED</span><p><b>Senthil Murugan</b> archived on Oct 31</p><p class="ox-muted">Departure reason: '+d+'</p></div>':
        '<div class="hr-dep"><p class="hr-dep-h">Register Departure</p><label><span>Departure Reason</span><select data-dr><option>Resigned</option><option>Retired</option><option>Fired</option></select></label>'+
        '<label><span>Departure Date</span><input type="text" value="Oct 31, 2026" readonly></label><label class="hr-dep-c"><input type="checkbox" checked> Archive the related user</label>'+
        '<label class="hr-dep-c"><input type="checkbox" checked> Release company vehicle</label><button type="button" class="ox-pbtn" data-dep-go>Apply</button></div>')+'</div>'+
        '<div class="hr-l-side ox-solo"><p class="hr-gi-h">Offboarding plan</p>'+(d?'<ul class="hr-acts is-mini">'+OFF.map(function(a){return '<li><span><b>'+a[1]+'</b><small>'+a[0]+'</small></span></li>';}).join('')+'</ul>':'<p class="hr-l-note">The departure wizard archives the employee and their user, keeps the full history for audits, and launches the offboarding plan.</p>')+'</div></div>';}
    function draw(){tabs.forEach(function(t){var o=t.getAttribute('data-lt')===st.tab;t.classList.toggle('is-on',o);t.setAttribute('aria-selected',o);});b.innerHTML={on:on,chg:chg,off:off}[st.tab]();}
    tabs.forEach(function(t){t.addEventListener('click',function(){st.tab=t.getAttribute('data-lt');draw();});});
    b.addEventListener('change',function(e){var o=e.target.closest('[data-od]');if(o){st.done[o.getAttribute('data-od')]=o.checked;draw();return;}var c=e.target.closest('[data-c]');if(c){st.chg[c.getAttribute('data-c')]=c.value;}});
    b.addEventListener('click',function(e){if(e.target.closest('[data-save]')){var base={job:'Sales Executive',loc:'Chennai HQ',mgr:'Kavya Nair'},lab={job:'Job Position',loc:'Work Location',mgr:'Manager'};
        st.saved=Object.keys(base).filter(function(k){return st.chg[k]!==base[k];}).map(function(k){return [lab[k],base[k],st.chg[k]];});if(st.saved.some(function(l){return l[0]==='Manager';}))st.saved.push(['Time Off Approver','Kavya Nair',st.chg.mgr]);draw();}
      if(e.target.closest('[data-dep-go]')){st.dep=b.querySelector('[data-dr]').value;draw();}});
    draw();})();

  /* --- 5 approvals --- */
  (function(){var ap=document.querySelector('[data-appr]');if(!ap)return;var RT=J('hr-rtypes'),MO=J('hr-modes'),E=J('hr-emps'),ch=ap.querySelector('[data-ap-chain]'),steps=[],at=0;
    var mgr={4:'Kavya Nair',8:'Suresh Babu',12:'Deepa Krishnan'},nm={4:'Priya Raman',8:'Anitha Selvam',12:'Vignesh Rao'};
    function sync(){ap.querySelector('[data-ap="mode"]').value=RT[+ap.querySelector('[data-ap="type"]').value][1];}
    function draw(){ch.innerHTML=steps.map(function(s,i){var state=i<at?'is-done':(i===at?'is-cur':'');
      return '<li class="'+state+'"><span class="hr-ch-dot">'+(i<at?'✓':i+1)+'</span><span><b>'+s[0]+'</b><small>'+s[1]+'</small></span>'+(i===at&&s[2]?'<button type="button" class="ox-pbtn" data-ap-ok>'+s[2]+'</button>':'')+'</li>';}).join('');}
    function go(){var t=+ap.querySelector('[data-ap="type"]').value,m=+ap.querySelector('[data-ap="mode"]').value,e=+ap.querySelector('[data-ap="emp"]').value;
      steps=[[nm[e]+' requests '+RT[t][0],'2 days &middot; Oct 23 to 24','']];
      if(m===1||m===3)steps.push(['Approval by '+mgr[e],'Employee&rsquo;s Time Off approver (their manager)','Approve as '+mgr[e]]);
      if(m===2||m===3)steps.push([m===3?'Second approval by Lakshmi Iyer':'Approval by Lakshmi Iyer','Time Off Officer','Validate as Lakshmi Iyer']);
      steps.push([m===0?'Approved automatically':'Approved','Balance updated, calendar blocked, payroll informed','']);at=m===0?steps.length:1;draw();}
    ap.querySelector('[data-ap="type"]').addEventListener('change',function(){sync();});
    ap.querySelector('[data-ap-go]').addEventListener('click',go);
    ap.addEventListener('click',function(e){if(e.target.closest('[data-ap-ok]')){at++;if(at===steps.length-1)at=steps.length;draw();}});
    sync();go();})();

  /* --- 6 attendance and schedules --- */
  (function(){var wk=document.querySelector('[data-wk]');if(!wk)return;var S=J('hr-sched'),A=J('hr-att');
    function draw(){var s=S[+wk.querySelector('input[name="hr-sch"]:checked').value],sick=wk.querySelector('[data-wk-sick]').checked,hol=wk.querySelector('[data-wk-hol]').checked,ex=0,wo=0,to=0;
      wk.querySelector('[data-wk-grid]').innerHTML='<div class="hr-wk-r is-h"><span>Day</span><span>Check in / out</span><span>Expected vs worked</span><span class="ox-num">Worked</span></div>'+A.map(function(a,i){
        var e=s[2][i],w=a[3],t=0,tag='';if(hol&&i===4){e=0;w=0;tag='<em class="is-hol">Public holiday</em>';}if(sick&&i===3){t=e;w=0;tag='<em class="is-off">Sick Time Off</em>';}
        if(!e&&!tag&&s[2][i]===0){w=0;tag='<em>Day off</em>';}
        ex+=e;wo+=w;to+=t;var mx=10;
        return '<div class="hr-wk-r"><span>'+a[0]+'</span><span class="mono">'+(w?a[1]+' &rarr; '+a[2]:'&mdash;')+'</span><span class="hr-wk-b"><i class="is-e" style="--w:'+(e/mx*100)+'"></i><i class="is-w'+(w>e?' is-over':'')+'" style="--w:'+(w/mx*100)+'"></i>'+(t?'<i class="is-t" style="--w:'+(t/mx*100)+'"></i>':'')+tag+'</span><span class="ox-num">'+(w?num(w,1)+' h':'')+'</span></div>';}).join('');
      var extra=wo+to-ex;
      wk.querySelector('[data-wk-tot]').innerHTML='<div><small>Expected</small><b>'+num(ex,1)+' h</b></div><div><small>Worked</small><b>'+num(wo,1)+' h</b></div><div><small>Time Off</small><b>'+num(to,1)+' h</b></div><div class="'+(extra>0?'is-ot':(extra<0?'is-short':''))+'"><small>Extra Hours</small><b>'+(extra>0?'+':'')+num(extra,1)+' h</b></div>';}
    wk.addEventListener('change',draw);draw();})();

  /* --- 7 access --- */
  (function(){var ac=document.querySelector('[data-acc]');if(!ac)return;var F=J('hr-fields'),G=J('hr-groups'),N=J('hr-notes'),rb=[].slice.call(ac.querySelectorAll('[data-role]'));
    var who={self:'Priya Raman',peer:'Mohammed Irfan',mgr:'Kavya Nair',officer:'Nisha George',admin:'Lakshmi Iyer'};
    function draw(r){ac.querySelector('[data-acc-t]').innerHTML='<tbody>'+F.map(function(f){var see=f[2].split(' ').indexOf(r)>-1,ed=f[3].split(' ').indexOf(r)>-1;
        return '<tr class="'+(see?'':'is-hid')+'"><th>'+f[0]+'</th><td>'+(see?f[1]:'<span class="hr-mask">'+f[1]+'</span>')+'</td><td class="ox-num">'+(see?(ed?'<span class="hr-perm is-w">Can edit</span>':'<span class="hr-perm">Read only</span>'):'<span class="hr-perm is-x">&#128274; Hidden</span>')+'</td></tr>';}).join('')+'</tbody>';
      ac.querySelector('[data-acc-who]').textContent=who[r];
      ac.querySelector('[data-acc-g]').innerHTML=G[r].map(function(g){return '<div><dt>'+g[0]+'</dt><dd class="'+(g[1]==='&mdash;'?'ox-muted':'')+'">'+g[1]+'</dd></div>';}).join('');
      ac.querySelector('[data-acc-note]').innerHTML=N[r];}
    rb.forEach(function(b){b.addEventListener('click',function(){press(rb,b);draw(b.getAttribute('data-role'));});});draw('self');})();

  /* --- 8 migration --- */
  (function(){var mg=document.querySelector('[data-mig]');if(!mg)return;var S=J('hr-sheet'),I=J('hr-iss'),fixed={},bad={2:[2,5],3:[0,1,5],4:[4],5:[3,5]},gone={};
    function draw(){var hot={};Object.keys(bad).forEach(function(r){bad[r].forEach(function(c){hot[r+'-'+c]=1;});});
      if(fixed.dept)delete hot['2-2'];if(fixed.dup){delete hot['3-0'];delete hot['3-1'];delete hot['3-5'];delete hot['4-4'];}if(fixed.mgr)delete hot['5-3'];if(fixed.date){delete hot['2-5'];delete hot['5-5'];}
      mg.querySelector('[data-mig-rows]').innerHTML=S.map(function(r,i){if(gone[i])return '<tr class="is-gone"><td>'+(i+2)+'</td><td colspan="7">Merged into E032</td></tr>';
        return '<tr><td>'+(i+2)+'</td>'+r.map(function(v,c){var k=i+'-'+c,f=!hot[k]&&bad[i]&&bad[i].indexOf(c)>-1;return '<td class="'+(hot[k]?'is-bad':(f?'is-fix':''))+'">'+(v||'<i>empty</i>')+'</td>';}).join('')+'</tr>';}).join('');
      var left=I.filter(function(x){return !fixed[x[0]];}).length;
      mg.querySelector('[data-mig-n]').textContent=left?left+' to fix':'All clear';
      mg.querySelector('[data-mig-iss]').innerHTML=I.map(function(x){return '<li class="'+(fixed[x[0]]?'is-done':'')+'"><span>'+x[1]+'</span>'+(fixed[x[0]]?'<em>✓ '+x[2]+'</em>':'<button type="button" class="ox-sbtn" data-fix="'+x[0]+'">'+x[2]+'</button>')+'</li>';}).join('');
      mg.querySelector('[data-mig-go]').disabled=!!left;}
    mg.addEventListener('click',function(e){var f=e.target.closest('[data-fix]');if(f){var k=f.getAttribute('data-fix'),x=I.filter(function(i){return i[0]===k;})[0];fixed[k]=1;
        x[3].forEach(function(c){if(c[1]<0)gone[c[0]]=1;else S[c[0]][c[1]]=c[2];});draw();return;}
      if(e.target.closest('[data-mig-go]')){mg.querySelector('[data-mig-res]').innerHTML='<b>42 employees imported</b> with departments, managers and opening leave balances. Every manager link resolved.';e.target.closest('[data-mig-go]').disabled=true;}});
    draw();})();

  /* --- 9 skills and appraisals --- */
  (function(){var sk=document.querySelector('[data-sk]');if(!sk)return;var K=J('hr-skills'),M=J('hr-matrix'),G=J('hr-goals'),b=sk.querySelector('[data-sk-b]'),tb=[].slice.call(sk.querySelectorAll('[data-sk-tab]'));
    var st={tab:'sk',col:4,rating:3,stage:1,goals:G.map(function(g){return g[1];})},LV=['','Beginner','Intermediate','Expert'],RT=['Needs improvement','Meets expectations','Exceeds expectations','Strongly exceeds'];
    function skills(){var rows=M.slice().sort(function(a,b){return b[2][st.col]-a[2][st.col];}),cover=rows.filter(function(r){return r[2][st.col]>=2;});
      return '<div class="hr-mx-bar"><span class="ox-crumb">Skills Inventory</span><span class="ox-facet">Skill: '+K[st.col]+'</span></div><div class="ox-scroll"><table class="hr-mx"><thead><tr><th>Employee</th>'+
        K.map(function(k,i){return '<th><button type="button" data-col="'+i+'" class="'+(i===st.col?'is-on':'')+'" aria-pressed="'+(i===st.col)+'">'+k+'</button></th>';}).join('')+'</tr></thead><tbody>'+
        rows.map(function(r){return '<tr><th><span class="hr-av is-sm" style="--c:'+r[1]+'">'+ini(r[0])+'</span>'+r[0]+'</th>'+r[2].map(function(v,i){return '<td class="'+(i===st.col?'is-col':'')+'"><span class="hr-lv lv-'+v+'" title="'+(LV[v]||'None')+'">'+'<i></i><i></i><i></i></span></td>';}).join('')+'</tr>';}).join('')+
        '</tbody></table></div><p class="hr-mx-note"><b>'+cover.length+' people</b> can cover '+K[st.col]+' at Intermediate or above: '+cover.map(function(r){return r[0];}).join(', ')+'.</p>';}
    function appr(){var stages=['To Start','Appraisal Sent','Done'];
      return '<div class="hr-ap"><div class="ox-f-bar"><span class="ox-f-btns">'+(st.stage<2?'<button type="button" class="ox-pbtn" data-ap-done>Mark as Done</button>':'<button type="button" class="ox-sbtn" data-ap-re>Reopen</button>')+'</span><span class="ox-sbar is-mini">'+
        stages.map(function(s,i){return '<span class="ox-sb'+(i===st.stage?' is-cur':'')+(i<st.stage?' is-done':'')+'">'+s+'</span>';}).join('')+'</span></div>'+
        '<div class="ox-sheet">'+(st.stage===2?'<span class="ox-ribbon">DONE</span>':'')+'<div class="hr-f-top"><div><h3>Priya Raman</h3><p class="hr-f-job">Annual Appraisal &middot; Oct 2026 &middot; Manager: Kavya Nair</p></div><span class="hr-av is-xl" style="--c:#4C9F70">PR</span></div>'+
        '<p class="hr-gi-h">Goals</p><ul class="hr-goals">'+G.map(function(g,i){return '<li><span>'+g[0]+'</span><input type="range" min="0" max="100" step="10" value="'+st.goals[i]+'" data-goal="'+i+'" aria-label="Progress"'+(st.stage===2?' disabled':'')+'><b>'+st.goals[i]+'%</b></li>';}).join('')+'</ul>'+
        '<div class="hr-fb"><div><p class="hr-gi-h">Employee&rsquo;s Feedback</p><p>Strong quarter in Coimbatore. I would like to take on key accounts and learn the CRM reports.</p></div><div><p class="hr-gi-h">Manager&rsquo;s Feedback</p><p>Consistent closer, trusted by customers. Ready to mentor new joiners.</p></div></div>'+
        '<p class="hr-gi-h">Final Rating</p><div class="hr-rate" role="group" aria-label="Final rating">'+RT.map(function(r,i){return '<button type="button" data-rate="'+i+'" class="'+(i===st.rating?'is-on':'')+'" aria-pressed="'+(i===st.rating)+'"'+(st.stage===2?' disabled':'')+'>'+r+'</button>';}).join('')+'</div></div></div>';}
    function draw(){b.innerHTML=st.tab==='sk'?skills():appr();}
    tb.forEach(function(t){t.addEventListener('click',function(){press(tb,t);st.tab=t.getAttribute('data-sk-tab');draw();});});
    b.addEventListener('click',function(e){var c=e.target.closest('[data-col]');if(c){st.col=+c.getAttribute('data-col');draw();return;}
      var r=e.target.closest('[data-rate]');if(r){st.rating=+r.getAttribute('data-rate');draw();return;}
      if(e.target.closest('[data-ap-done]')){st.stage=2;draw();return;}if(e.target.closest('[data-ap-re]')){st.stage=1;draw();}});
    b.addEventListener('input',function(e){var g=e.target.closest('[data-goal]');if(g){st.goals[+g.getAttribute('data-goal')]=+g.value;g.nextElementSibling.textContent=g.value+'%';}});
    draw();})();

  /* --- 10 hub --- */
  (function(){var hb=document.querySelector('[data-hub]');if(!hb)return;var A=J('hr-apps'),nb=[].slice.call(hb.querySelectorAll('[data-node]'));
    function draw(i){var a=A[i];hb.querySelector('[data-hub-k]').innerHTML=a[2].toUpperCase();hb.querySelector('[data-hub-k]').style.color=a[1];hb.querySelector('[data-hub-n]').innerHTML=a[0];
      hb.querySelector('[data-hub-in]').innerHTML=a[3];hb.querySelector('[data-hub-out]').innerHTML=a[4];hb.querySelector('[data-hub-ex]').innerHTML='<b>Example:</b> '+a[5];}
    nb.forEach(function(b){b.addEventListener('click',function(){press(nb,b);draw(+b.getAttribute('data-node'));});});draw(0);})();

  /* --- 11 app picker --- */
  (function(){var pk=document.querySelector('[data-apppick]');if(!pk)return;var H=J('hr-happs');
    function draw(){var on={};pk.querySelectorAll('[data-q]').forEach(function(q){on[q.getAttribute('data-q')]=q.checked;});var n1=0,n2=0;
      H.forEach(function(a){var ph=a[3]===''||(a[0]==='leave')?1:(on[a[3]]?a[4]:0);if(a[0]==='leave'&&!on.leave)ph=1;
        var li=pk.querySelector('[data-app="'+a[0]+'"]');li.className='hr-app is-'+ph;li.querySelector('[data-app-st]').textContent=ph===1?'Phase 1':(ph===2?'Phase 2':'Not yet');if(ph===1)n1++;if(ph===2)n2++;});
      pk.querySelector('[data-pick-sum]').textContent=n1+' apps to start, '+n2+' later';}
    pk.addEventListener('change',draw);draw();})();

  /* --- 12 who does what --- */
  (function(){var rc=document.querySelector('[data-raci]');if(!rc)return;var R=J('hr-raci'),bt=[].slice.call(rc.querySelectorAll('[data-rt]'));
    function draw(i){var rows=R[i][2],u=rows.filter(function(r){return r[1]==='u';}).length;
      rc.querySelector('[data-raci-b]').innerHTML=rows.map(function(r){return '<tr><td>'+r[0]+'</td>'+['u','b','y'].map(function(k){return '<td class="ox-num">'+(r[1]===k?'<span class="hr-dot is-'+k+'"></span>':'')+'</td>';}).join('')+'</tr>';}).join('');
      rc.querySelector('[data-raci-sum]').innerHTML='Unisas leads <b>'+u+' of '+rows.length+'</b> tasks in this phase.';}
    bt.forEach(function(b){b.addEventListener('click',function(){press(bt,b);draw(+b.getAttribute('data-rt'));});});draw(0);})();

  /* --- 13 planner --- */
  (function(){var pl=document.querySelector('[data-pl]');if(!pl)return;
    function draw(){var emp=+pl.querySelector('[data-pl="emp"]').value,loc=+pl.querySelector('[data-pl="loc"]').value,src=+pl.querySelector('[data-pl="src"]').value,x={};
      pl.querySelectorAll('[data-pl-x]').forEach(function(c){x[c.getAttribute('data-pl-x')]=c.checked;});
      pl.querySelector('[data-pl-o="emp"]').textContent=emp;pl.querySelector('[data-pl-o="loc"]').textContent=loc;
      var P=[['Discover &amp; design',1+(emp>150?1:0)+(loc>3?1:0),'Policies, approvals, structure'],['Configure',1+(x.shift?1:0)+(loc>2?1:0),'Employees, Time Off'+(x.shift?', Attendances, devices':'')],
             ['Migrate data',1+(src===0?1:0)+(emp>200?1:0),src===0?'Digitise paper files':'Clean and import'],['Train &amp; go live',1+(emp>100?1:0),'HR, managers, employees']];
      if(x.rec)P.push(['Recruitment &amp; appraisals',2,'Phase 2 apps']);if(x.pay)P.push(['Payroll &amp; parallel run',4,'After one clean month']);
      var s=0;P.forEach(function(p){p.s=s;s+=p[1];});
      pl.querySelector('[data-pl-wk]').innerHTML=Array.apply(null,{length:s}).map(function(_,i){return '<span>W'+(i+1)+'</span>';}).join('');
      pl.querySelector('[data-pl-wk]').style.setProperty('--n',s);
      pl.querySelector('[data-pl-road]').style.setProperty('--n',s);
      pl.querySelector('[data-pl-road]').innerHTML=P.map(function(p,i){return '<li><span><b>'+p[0]+'</b><small>'+p[2]+'</small></span><span class="hr-pl-tr"><i style="--s:'+p.s+';--l:'+p[1]+'" class="'+(i>=4?'is-2':'')+'">'+p[1]+' wk</i></span></li>';}).join('');
      var core=P.slice(0,4).reduce(function(a,p){return a+p[1];},0);
      pl.querySelector('[data-pl-tot]').innerHTML='Core HR live in about <b>'+core+' weeks</b>'+(s>core?', everything in <b>'+s+' weeks</b>':'')+'.';}
    pl.addEventListener('input',draw);pl.addEventListener('change',draw);draw();})();
})();
</script>
'''
