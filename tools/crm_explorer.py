"""
Interactive Odoo CRM explorer for odoo-crm.html: a faithful, working copy of the
Odoo 20 CRM screens (pipeline, opportunity form, list, activities, reporting)
running on sample data. Colours, layout and wording follow the real app
(demo.odoo.com). Styles: the "ox-" rules in dist/assets/crm.css.
"""


def ic(paths, size=16, sw=1.8):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (size, size, sw, paths))


SEARCH = ic('<circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/>', 15, 2)
FUNNEL = ic('<path d="M4 5h16l-6 7v6l-4 2v-8z"/>', 12, 2.2)
V_KANBAN = ic('<rect x="4" y="4" width="4.5" height="16" rx="1"/><rect x="10" y="4" width="4.5" height="10" rx="1"/><rect x="16" y="4" width="4" height="7" rx="1"/>', 16, 1.9)
V_LIST = ic('<path d="M5 6h14M5 12h14M5 18h14"/>', 16, 2)
V_ACT = ic('<circle cx="12" cy="12" r="8"/><path d="M12 8v4.5l3 2"/>', 16, 1.9)
V_GRAPH = ic('<path d="M6 19V11M12 19V6M18 19v-5"/>', 16, 2.4)


def frame(app_icon):
    views = [("kanban", "Kanban", V_KANBAN), ("list", "List", V_LIST), ("activity", "Activity", V_ACT), ("graph", "Graph", V_GRAPH)]
    switch = "".join('<button type="button" class="ox-vbtn%s" data-ox-view="%s" aria-label="%s view" title="%s" aria-pressed="%s">%s</button>'
                     % (" is-on" if k == "kanban" else "", k, n, n, "true" if k == "kanban" else "false", svg) for k, n, svg in views)
    return ('<div class="ox" data-ox>'
            '<div class="ox-nav"><span class="ox-app">%s<b>CRM</b></span><span class="ox-menu">Sales</span><span class="ox-menu">Reporting</span>'
            '<span class="ox-menu">Configuration</span><span class="ox-nav-r"><span class="ox-company">Your Company</span><span class="ox-av" style="--c:#6B5B95">Y</span></span></div>'
            '<div class="ox-cp"><div class="ox-cp-l"><button type="button" class="ox-new" data-ox-new>New</button><span class="ox-crumb" data-ox-crumb>Pipeline</span></div>'
            '<label class="ox-search">%s<span class="ox-facet">%sMy Pipeline</span><input type="search" placeholder="Search..." aria-label="Search opportunities" data-ox-q></label>'
            '<div class="ox-views">%s</div></div>'
            '<div class="ox-body" data-ox-body></div></div>'
            '<p class="ox-hint"><span class="ox-hint-dot"></span>Live preview with sample data. Drag a card to another stage, open an opportunity, or switch views.</p>'
            % (app_icon, SEARCH, FUNNEL, switch))


JS = r'''<script>
(function(){
  var root=document.querySelector('[data-ox]'); if(!root) return;
  var body=root.querySelector('[data-ox-body]'), crumb=root.querySelector('[data-ox-crumb]'), q=root.querySelector('[data-ox-q]');
  var STAGES=['New','Qualified','Proposition','Won'], PROB={New:10,Qualified:30,Proposition:60,Won:100};
  var PEOPLE={A:{n:'Anita Rao',c:'#B5567E'},R:{n:'Rahul Menon',c:'#3E7CB1'},M:{n:'Meera Iyer',c:'#4C9F70'}};
  var TAG={Product:'red',Design:'purple',Information:'blue',Consulting:'green',Services:'yellow',Other:'sky'};
  var ICON={
    call:'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    email:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    meeting:'<circle cx="9" cy="8" r="3"/><path d="M3 19c.6-3 3-5 6-5s5.4 2 6 5"/><path d="M16 5a3 3 0 0 1 0 6M18 14c1.6.6 2.6 2.2 3 4.5"/>',
    todo:'<path d="M5 12l4 4L19 6"/>', none:'<circle cx="12" cy="12" r="8"/><path d="M12 8v4.5l3 2"/>',
    star:'<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.9 6.8 19.6l1-5.8L3.5 9.7l5.9-.8z"/>'
  };
  function svg(k,s){return '<svg width="'+(s||14)+'" height="'+(s||14)+'" viewBox="0 0 24 24" fill="'+(k==='star'?'currentColor':'none')+'" stroke="currentColor" stroke-width="'+(k==='star'?0:2)+'" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICON[k]+'</svg>';}
  var D=[
    {id:1,name:'CRM rollout for 2 showrooms',cust:'Nair Textiles',email:'purchase@nairtextiles.in',phone:'+91 98450 21734',rev:480000,stage:'New',tags:['Product'],pri:1,sp:'A',act:{t:'call',s:'Discovery call',due:'today'}},
    {id:2,name:'Annual support contract',cust:'Kaveri Foods',email:'it@kaverifoods.in',phone:'+91 99620 45810',rev:210000,stage:'New',tags:['Services'],pri:0,sp:'R',act:null},
    {id:3,name:'ERP for 3 branches',cust:'Shree Distributors',email:'ops@shreedist.in',phone:'+91 97890 11223',rev:1200000,stage:'Qualified',tags:['Consulting'],pri:3,sp:'M',act:{t:'call',s:'Call to confirm requirements',due:'overdue'}},
    {id:4,name:'Quote for 40 POS terminals',cust:'Bluebay Retail',email:'accounts@bluebayretail.in',phone:'+91 90030 77881',rev:640000,stage:'Qualified',tags:['Product'],pri:2,sp:'A',act:{t:'meeting',s:'Demo with store managers',due:'planned'}},
    {id:5,name:'Warehouse barcode setup',cust:'Arun Logistics',email:'admin@arunlogistics.in',phone:'+91 94440 62109',rev:360000,stage:'Proposition',tags:['Information'],pri:2,sp:'R',act:{t:'call',s:'Follow up on proposal',due:'planned'}},
    {id:6,name:'Clinic group onboarding',cust:'Sunrise Clinics',email:'hello@sunriseclinics.in',phone:'+91 98840 35670',rev:525000,stage:'Proposition',tags:['Consulting'],pri:3,sp:'M',act:{t:'email',s:'Send revised quotation',due:'overdue'}},
    {id:7,name:'Export pricing module',cust:'Indus Exports',email:'trade@indusexports.in',phone:'+91 99400 18842',rev:290000,stage:'Proposition',tags:['Product','Other'],pri:0,sp:'A',act:{t:'email',s:'Share sample pricelist',due:'today'}},
    {id:8,name:'Dealer portal',cust:'Orbit Motors',email:'sales@orbitmotors.in',phone:'+91 90940 55123',rev:980000,stage:'Won',tags:['Information','Other'],pri:2,sp:'R',act:null}
  ];
  D.forEach(function(o){o.log=[{who:'Unisas Bot',txt:'Lead/Opportunity created'}];});
  var DUE={overdue:{c:'red',w:'2 days overdue'},today:{c:'orange',w:'Today'},planned:{c:'green',w:'Tomorrow'}};
  var st={view:'kanban',open:null};
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function inr(n,dec){return '₹ '+n.toLocaleString('en-IN',dec?{minimumFractionDigits:2,maximumFractionDigits:2}:{maximumFractionDigits:0});}
  function rows(){var t=q.value.trim().toLowerCase();return D.filter(function(o){return !o.lost&&(!t||(o.name+' '+o.cust).toLowerCase().indexOf(t)>-1);});}
  function av(k,cls){var p=PEOPLE[k];return '<span class="ox-av '+(cls||'')+'" style="--c:'+p.c+'" title="'+p.n+'">'+p.n[0]+'</span>';}
  function logo(o){return '<span class="ox-logo">'+o.cust[0]+'</span>';}
  function tags(o){return o.tags.map(function(t){return '<span class="ox-tag ox-tag--'+TAG[t]+'">'+t+'</span>';}).join('');}
  function stars(o,big){var h='';for(var i=1;i<=3;i++)h+='<span class="ox-star'+(i<=o.pri?' is-on':'')+'">'+svg('star',big?17:15)+'</span>';return '<span class="ox-stars">'+h+'</span>';}
  function actIcon(o){return o.act?'<span class="ox-act ox-act--'+DUE[o.act.due].c+'" title="'+esc(o.act.s)+'">'+svg(o.act.t)+'</span>':'<span class="ox-act ox-act--none" title="No activity">'+svg('none')+'</span>';}
  function card(o){
    return '<article class="ox-card" draggable="true" tabindex="0" data-id="'+o.id+'"><b class="ox-c-name">'+esc(o.name)+'</b><span class="ox-c-rev">'+inr(o.rev,1)+'</span>'+
      '<span class="ox-c-cust">'+logo(o)+esc(o.cust)+'</span><span class="ox-tags">'+tags(o)+'</span>'+
      '<span class="ox-c-foot">'+stars(o)+actIcon(o)+'<span class="ox-team">Sales</span>'+av(o.sp)+'</span></article>';
  }
  function kanban(list){
    return '<div class="ox-kanban">'+STAGES.map(function(s){
      var c=list.filter(function(o){return o.stage===s;}), tot=c.reduce(function(a,o){return a+o.rev;},0), n=c.length||1,
          k={green:0,orange:0,red:0,none:0};
      c.forEach(function(o){k[o.act?DUE[o.act.due].c:'none']++;});
      var bar=c.length?['green','orange','red','none'].map(function(x){return k[x]?'<i class="ox-p-'+x+'" style="flex:'+k[x]+'"></i>':'';}).join(''):'<i class="ox-p-none" style="flex:1"></i>';
      return '<section class="ox-col" data-stage="'+s+'"><header><b>'+s+'</b><span class="ox-plus" aria-hidden="true">+</span></header>'+
        '<div class="ox-prog"><span class="ox-bar">'+bar+'</span><b>'+inr(tot)+'</b></div><div class="ox-cards">'+c.map(card).join('')+'</div></section>';
    }).join('')+'</div>';
  }
  function list(list){
    var tot=list.reduce(function(a,o){return a+o.rev;},0);
    return '<div class="ox-scroll"><table class="ox-table"><thead><tr><th class="ox-chk"><span class="ox-cb"></span></th><th>Opportunity</th><th>Customer</th><th>Email</th><th>Salesperson</th><th>Next Activity</th><th class="ox-num">Expected Revenue</th><th>Stage</th></tr></thead><tbody>'+
      list.map(function(o){return '<tr data-id="'+o.id+'" tabindex="0"><td class="ox-chk"><span class="ox-cb"></span></td><td><b>'+esc(o.name)+'</b></td><td>'+esc(o.cust)+'</td><td class="ox-muted">'+o.email+'</td><td><span class="ox-sp">'+av(o.sp,'is-sm')+PEOPLE[o.sp].n+'</span></td>'+
        '<td>'+(o.act?'<span class="ox-due ox-due--'+DUE[o.act.due].c+'">'+esc(o.act.s)+'</span>':'<span class="ox-muted">None</span>')+'</td><td class="ox-num">'+inr(o.rev,1)+'</td><td><span class="ox-stage-pill">'+o.stage+'</span></td></tr>';}).join('')+
      '</tbody><tfoot><tr><td></td><td colspan="5"></td><td class="ox-num"><b>'+inr(tot,1)+'</b></td><td></td></tr></tfoot></table></div>';
  }
  function activity(list){
    var T=[['email','Email'],['call','Call'],['meeting','Meeting'],['todo','To-Do']];
    return '<div class="ox-scroll"><table class="ox-acts"><thead><tr><th></th>'+T.map(function(t){
      var n=list.filter(function(o){return o.act&&o.act.t===t[0];}), k={green:0,orange:0,red:0};
      n.forEach(function(o){k[DUE[o.act.due].c]++;});
      var bar=n.length?'<span class="ox-bar">'+['green','orange','red'].map(function(x){return k[x]?'<i class="ox-p-'+x+'" style="flex:'+k[x]+'"></i>':'';}).join('')+'</span>':'';
      return '<th><span>'+t[1]+'</span>'+bar+'</th>';}).join('')+'</tr></thead><tbody>'+
      list.map(function(o){return '<tr><td class="ox-a-rec" data-id="'+o.id+'" tabindex="0">'+av(o.sp)+'<span><b>'+esc(o.name)+'</b><small>'+esc(o.cust)+'</small></span><span class="ox-a-meta"><small>'+inr(o.rev,1)+'</small><span class="ox-stage-pill">'+o.stage+'</span></span></td>'+
        T.map(function(t){return o.act&&o.act.t===t[0]?'<td class="ox-a-cell ox-a--'+DUE[o.act.due].c+'"><b>'+esc(o.act.s)+'</b><small>'+DUE[o.act.due].w+'</small></td>':'<td></td>';}).join('')+'</tr>';}).join('')+
      '</tbody></table></div><p class="ox-sched">+ Schedule activity</p>';
  }
  var measure='rev';
  function graph(list){
    var v=STAGES.map(function(s){var c=list.filter(function(o){return o.stage===s;});return measure==='rev'?c.reduce(function(a,o){return a+o.rev;},0):c.length;});
    var max=Math.max.apply(null,v.concat([1])), step=measure==='rev'?Math.ceil(max/4/100000)*100000||100000:Math.ceil(max/4)||1, top=step*4;
    var ticks=[4,3,2,1,0].map(function(i){var n=step*i;return '<span>'+(measure==='rev'?(n?(n/100000)+'L':'0'):n)+'</span>';}).join('');
    return '<div class="ox-gtools"><span class="ox-measure"><button type="button" data-m="count" class="'+(measure==='count'?'is-on':'')+'">Count</button><button type="button" data-m="rev" class="'+(measure==='rev'?'is-on':'')+'">Expected Revenue</button></span>'+
      '<span class="ox-stacked"><i></i>Stacked</span></div><div class="ox-chart"><div class="ox-yaxis">'+ticks+'</div><div class="ox-plot">'+
      v.map(function(x,i){return '<div class="ox-gcol"><span class="ox-gwrap"><span class="ox-gbar" style="--h:'+(x/top*100).toFixed(2)+'" title="'+STAGES[i]+': '+(measure==='rev'?inr(x):x)+'"><em>'+(measure==='rev'?inr(x):x)+'</em></span></span><small>'+STAGES[i]+'</small></div>';}).join('')+
      '</div></div><p class="ox-legend"><i></i>'+(measure==='rev'?'Expected Revenue':'Count')+' by Stage</p>';
  }
  function form(o){
    var i=STAGES.indexOf(o.stage);
    var bar=STAGES.map(function(s,j){return '<button type="button" class="ox-sb'+(j===i?' is-cur':'')+(j<i?' is-done':'')+'" data-stage="'+s+'">'+s+'</button>';}).join('');
    var ribbon=o.lost?'<span class="ox-ribbon is-lost">LOST</span>':(o.stage==='Won'?'<span class="ox-ribbon">WON</span>':'');
    var btns='<button type="button" class="ox-pbtn">New Quotation</button>'+(o.lost?'<button type="button" class="ox-sbtn" data-do="restore">Restore</button>':(o.stage!=='Won'?'<button type="button" class="ox-pbtn" data-do="won">Won</button><button type="button" class="ox-sbtn" data-do="lost">Lost</button>':''));
    var act=o.act?'<div class="ox-pa"><span class="ox-pa-ic ox-act--'+DUE[o.act.due].c+'">'+svg(o.act.t,13)+'</span><div><p><b class="ox-pa-due ox-t-'+DUE[o.act.due].c+'">'+DUE[o.act.due].w+':</b> <b>'+esc(o.act.s)+'</b> for '+PEOPLE[o.sp].n+'</p>'+
      '<p class="ox-pa-do"><button type="button" data-do="done">✓ Done</button><span>Edit</span><span>Cancel</span></p></div></div>':'<p class="ox-muted ox-pa-none">No planned activities.</p>';
    var log=o.log.slice().reverse().map(function(l){var pk=Object.keys(PEOPLE).filter(function(k){return PEOPLE[k].n===l.who;})[0];return '<div class="ox-msg">'+(pk?av(pk,'is-msg'):'<span class="ox-av is-bot">U</span>')+'<div><p><b>'+l.who+'</b> <small>just now</small></p><p>'+l.txt+'</p></div></div>';}).join('');
    return '<div class="ox-form"><div class="ox-f-main"><div class="ox-f-bar"><span class="ox-f-btns">'+btns+'</span><span class="ox-sbar">'+bar+'</span></div>'+
      '<div class="ox-sheet">'+ribbon+'<h3>'+esc(o.name)+'</h3><div class="ox-f-rev"><span><small>Expected Revenue</small><b>'+inr(o.rev,1)+'</b></span><span class="ox-at">at</span><span><small>Probability</small><b>'+(o.lost?0:PROB[o.stage]).toFixed(2)+' %</b></span></div>'+
      '<dl class="ox-fields"><div><dt>Contact</dt><dd>'+esc(o.cust)+'</dd></div><div><dt>Salesperson</dt><dd>'+av(o.sp,'is-sm')+PEOPLE[o.sp].n+'</dd></div>'+
      '<div><dt>Email</dt><dd>'+o.email+'</dd></div><div><dt>Expected Closing</dt><dd>End of month '+stars(o,1)+'</dd></div>'+
      '<div><dt>Phone</dt><dd>'+o.phone+'</dd></div><div><dt>Tags</dt><dd>'+tags(o)+'</dd></div></dl>'+
      '<div class="ox-ftabs"><span class="is-on">Notes</span><span>Extra Info</span></div><p class="ox-muted ox-desc">Customer wants one system for sales, stock and invoicing across all branches.</p></div></div>'+
      '<aside class="ox-chatter"><div class="ox-ch-btns"><span class="ox-pbtn">Send message</span><span class="ox-sbtn">Log note</span><span class="ox-sbtn">Activity</span></div>'+
      '<p class="ox-ch-sep">Planned Activities</p>'+act+'<p class="ox-ch-sep">Today</p>'+log+'</aside></div>';
  }
  function render(){
    var l=rows();
    root.querySelectorAll('[data-ox-view]').forEach(function(b){var on=!st.open&&b.getAttribute('data-ox-view')===st.view;b.classList.toggle('is-on',on);b.setAttribute('aria-pressed',on);});
    if(st.open){var o=D.filter(function(x){return x.id===st.open;})[0];crumb.innerHTML='<a href="#" data-ox-back>Pipeline</a><span>'+esc(o.name)+'</span>';body.innerHTML=form(o);return;}
    crumb.textContent={kanban:'Pipeline',list:'Pipeline',activity:'Pipeline',graph:'Pipeline Analysis'}[st.view];
    body.innerHTML=l.length?{kanban:kanban,list:list,activity:activity,graph:graph}[st.view](l):'<p class="ox-empty">No opportunity matches “'+esc(q.value)+'”.</p>';
  }
  function find(id){return D.filter(function(x){return x.id===+id;})[0];}
  function move(o,s){if(o.stage===s)return;o.log.push({who:PEOPLE[o.sp].n,txt:'Stage changed: '+o.stage+' → <b>'+s+'</b>'});o.stage=s;}
  root.addEventListener('click',function(e){
    var v=e.target.closest('[data-ox-view]'); if(v){st.view=v.getAttribute('data-ox-view');st.open=null;render();return;}
    if(e.target.closest('[data-ox-back]')){e.preventDefault();st.open=null;render();return;}
    var m=e.target.closest('[data-m]'); if(m){measure=m.getAttribute('data-m');render();return;}
    var o=st.open&&find(st.open);
    var sb=e.target.closest('.ox-sb'); if(sb&&o&&!o.lost){move(o,sb.getAttribute('data-stage'));render();return;}
    var d=e.target.closest('[data-do]');
    if(d&&o){var a=d.getAttribute('data-do');
      if(a==='won')move(o,'Won');
      if(a==='lost'){o.lost=true;o.log.push({who:PEOPLE[o.sp].n,txt:'Marked as <b>lost</b>'});}
      if(a==='restore'){o.lost=false;o.log.push({who:PEOPLE[o.sp].n,txt:'Restored'});}
      if(a==='done'){o.log.push({who:PEOPLE[o.sp].n,txt:'<b>'+o.act.s+'</b> done'});o.act=null;}
      render();return;}
    var r=e.target.closest('.ox-card,[data-id]'); if(r&&r.getAttribute('data-id')){st.open=+r.getAttribute('data-id');render();}
  });
  root.addEventListener('keydown',function(e){if(e.key==='Enter'){var r=e.target.closest&&e.target.closest('[data-id]');if(r){st.open=+r.getAttribute('data-id');render();}}});
  root.querySelector('[data-ox-new]').addEventListener('click',function(){st.open=null;st.view='kanban';render();var c=body.querySelector('.ox-col');if(c)c.classList.add('is-flash');});
  q.addEventListener('input',function(){st.open=null;render();});
  /* drag and drop between stages */
  var dragId=null;
  body.addEventListener('dragstart',function(e){var c=e.target.closest('.ox-card');if(!c)return;dragId=c.getAttribute('data-id');c.classList.add('is-drag');e.dataTransfer.effectAllowed='move';try{e.dataTransfer.setData('text/plain',dragId);}catch(x){}});
  body.addEventListener('dragend',function(){dragId=null;body.querySelectorAll('.is-drag,.is-over').forEach(function(x){x.classList.remove('is-drag','is-over');});});
  body.addEventListener('dragover',function(e){var col=e.target.closest('.ox-col');if(col&&dragId){e.preventDefault();body.querySelectorAll('.ox-col.is-over').forEach(function(x){if(x!==col)x.classList.remove('is-over');});col.classList.add('is-over');}});
  body.addEventListener('drop',function(e){var col=e.target.closest('.ox-col');if(col&&dragId){e.preventDefault();move(find(dragId),col.getAttribute('data-stage'));dragId=null;render();}});
  render();
})();
</script>
'''


# ---------------------------------------------------------------- Odoo Project Gantt (process section)
GANTT_DAYS = 42          # Mon 5 Oct to Sun 15 Nov, one column per day, as Odoo's Month scale
GANTT_TODAY = 16         # Wed 21 Oct
PROJECT_ICON = ('<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><path d="M3.5 12.5l5 5L20.5 5.5" fill="none" stroke="#1BA39C" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>'
                '<path d="M8.5 17.5L20.5 5.5" fill="none" stroke="#714B67" stroke-width="3.4" stroke-linecap="round"/></svg>')
PEOPLE = {"A": ("Anita Rao", "Functional Consultant", "#B5567E"), "R": ("Rahul Menon", "Odoo Developer", "#3E7CB1"), "M": ("Meera Iyer", "Project Manager", "#4C9F70")}
# (assignee, task, hours, start day, length in days, state, description)
TASKS = [("A", "Discover", 16, 0, 5, "done", "Workshops with your sales team to map how leads arrive, how deals progress and what managers need to see."),
         ("A", "Design", 24, 7, 5, "done", "Pipeline stages, assignment rules, automations and reports agreed with you and signed off."),
         ("A", "Train", 16, 29, 4, "todo", "Salespeople and managers learn on their own pipeline, not a generic demo."),
         ("R", "Configure", 40, 14, 12, "doing", "Odoo CRM, sales teams, email templates and dashboards set up on a test database."),
         ("R", "Migrate &amp; connect", 32, 17, 13, "doing", "Existing leads and customers imported; website, email and WhatsApp connected."),
         ("M", "Go live &amp; hypercare", 20, 35, 7, "todo", "Switch-over, close support for the first weeks, and rules refined as the team settles in.")]
STATE = {"done": "Done", "doing": "In Progress", "todo": "Planned"}


def _date(d):
    return ("Oct %d" % (5 + d)) if d < 27 else ("Nov %d" % (d - 26))


def gantt():
    n = GANTT_DAYS
    days = "".join('<span class="%s">%02d</span>' % (" ".join(c for c in ("is-we" if d % 7 in (5, 6) else "", "is-today" if d == GANTT_TODAY else "") if c),
                                                     5 + d if d < 27 else d - 26) for d in range(n))
    cols = "".join('<i class="ox-gt-we" style="--d:%d"></i>' % d for d in range(n) if d % 7 in (5, 6))
    cols += '<i class="ox-gt-today" style="--d:%d"></i>' % GANTT_TODAY
    rows = ""
    for key in "ARM":
        name, role, colour = PEOPLE[key]
        tasks = [t for t in TASKS if t[0] == key]
        hours = sum(t[2] for t in tasks)
        done = sum(t[2] for t in tasks if t[5] == "done") + sum(t[2] // 2 for t in tasks if t[5] == "doing")
        s0, s1 = min(t[3] for t in tasks), max(t[3] + t[4] for t in tasks)
        rows += ('<div class="ox-gt-row is-group"><div class="ox-gt-label"><span class="ox-gt-caret">&#9662;</span><span class="ox-av" style="--c:%s">%s</span>'
                 '<span class="ox-gt-who"><b>%s</b><small>%s</small></span><span class="ox-gt-h">%dh</span><span class="ox-gt-load"><i style="width:%d%%"></i></span></div>'
                 '<div class="ox-gt-track"><span class="ox-gt-sum" style="--s:%d;--l:%d"><em>%d</em></span></div></div>'
                 % (colour, name[0], name, role, hours, round(done * 100 / hours), s0, s1 - s0, len(tasks)))
        for _k, task, h, s, l, state, desc in tasks:
            up = TASKS.index((_k, task, h, s, l, state, desc)) >= 3   # lower rows open the popover upwards
            pop = ('<span class="ox-gt-pop%s%s" role="tooltip"><b>%s</b><span>%s &rarr; %s</span><span>Assignee: %s</span><span>Allocated: %dh &middot; %s</span><small>%s</small></span>'
                   % (" is-end" if s + l > n - 12 else "", " is-up" if up else "", task, _date(s), _date(s + l - 1), name, h, STATE[state], desc))
            ms = '<span class="ox-gt-ms" style="--s:%d" title="Go-live milestone"></span>' % s if task.startswith("Go live") else ""
            rows += ('<div class="ox-gt-row"><div class="ox-gt-label is-task"><span>%s</span><span class="ox-gt-h">%dh</span></div>'
                     '<div class="ox-gt-track">%s<button type="button" class="ox-gt-bar is-%s%s" style="--s:%d;--l:%d" aria-label="%s, %s to %s">%s%s</button></div></div>'
                     % (task, h, ms, state, " has-ms" if ms else "", s, l, task.replace("&amp;", "and"), _date(s), _date(s + l - 1), task, pop))
    load = [sum(1 for t in TASKS if t[3] <= d < t[3] + t[4]) if d % 7 not in (5, 6) else 0 for d in range(n)]
    total = "".join('<i class="ox-gt-tot" style="--d:%d;--k:%d"></i>' % (d, k) for d, k in enumerate(load) if k)
    rows += ('<div class="ox-gt-row is-total"><div class="ox-gt-label"><b>Total</b><span class="ox-gt-h">%dh</span><span class="ox-gt-load"><i style="width:38%%"></i></span></div>'
             '<div class="ox-gt-track">%s</div></div>' % (sum(t[2] for t in TASKS), total))
    views = "".join('<span class="ox-vbtn%s" aria-hidden="true">%s</span>' % (" is-on" if i == 2 else "", svg)
                    for i, svg in enumerate([V_KANBAN, V_LIST, ic('<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 10h6M8 14h8"/>', 16, 1.9), V_ACT, V_GRAPH]))
    return ('<div class="ox ox-gt" style="--n:%d">'
            '<div class="ox-nav"><span class="ox-app">%s<b>Project</b></span><span class="ox-menu">Projects</span><span class="ox-menu">Tasks</span><span class="ox-menu">Reporting</span>'
            '<span class="ox-menu">Configuration</span><span class="ox-nav-r"><span class="ox-company">Your Company</span><span class="ox-av" style="--c:#6B5B95">Y</span></span></div>'
            '<div class="ox-cp"><div class="ox-cp-l"><span class="ox-new">New</span><span class="ox-crumb ox-crumb--stack"><a>CRM Implementation</a><span>Tasks</span></span></div>'
            '<span class="ox-search">%s<span class="ox-facet ox-facet--teal">%sAssignees</span><span class="ox-ph">Search...</span></span><div class="ox-views">%s</div></div>'
            '<div class="ox-gt-tools"><span class="ox-sbtn">&larr;</span><span class="ox-sbtn">&rarr;</span><span class="ox-sbtn">Month &#9662;</span><span class="ox-sbtn">Today</span></div>'
            '<div class="ox-scroll"><div class="ox-gt-grid"><div class="ox-gt-head"><div class="ox-gt-label is-head">Planning</div><div class="ox-gt-track">'
            '<div class="ox-gt-months"><span style="--d:27">October 2026</span><span style="--d:15">November 2026</span></div><div class="ox-gt-days">%s</div></div></div>'
            '<div class="ox-gt-body"><div class="ox-gt-cols" aria-hidden="true">%s</div>%s</div></div></div></div>'
            '<p class="ox-hint"><span class="ox-hint-dot"></span>A typical CRM rollout in Odoo Project. Hover or tap a task to see what happens in that phase.</p>'
            % (n, PROJECT_ICON, SEARCH, ic('<path d="M12 4l8 4-8 4-8-4z"/><path d="M4 12l8 4 8-4M4 16l8 4 8-4"/>', 12, 2.2), views, days, cols, rows))
