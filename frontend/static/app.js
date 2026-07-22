const API_URL='http://127.0.0.1:8000/api';let currentProperty=null,currentUser=null,currentWorkspaceId=1;
const pipelineStatuses=['Propiedad cargada','Contenido generado','Revisión pendiente','Aprobado','Publicado','Midiendo'];
function toast(msg){const t=document.getElementById('toast');t.innerText=msg;t.classList.remove('hidden');setTimeout(()=>t.classList.add('hidden'),2600)}
function load(btn,on){if(!btn)return;if(on){btn.dataset.old=btn.innerHTML;btn.disabled=true;btn.innerHTML='Procesando...'}else{btn.disabled=false;btn.innerHTML=btn.dataset.old||btn.innerHTML}}
function setAuth(m){document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('active'));if(m==='login'){loginTab.classList.add('active');loginForm.classList.remove('hidden');registerForm.classList.add('hidden')}else{registerTab.classList.add('active');registerForm.classList.remove('hidden');loginForm.classList.add('hidden')}}
async function login(){try{if(!loginEmail.value||!loginPassword.value){toast('Completá email y contraseña.');return}load(loginBtn,true);const r=await fetch(API_URL+'/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:loginEmail.value,password:loginPassword.value})});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Error');currentUser=d.user;enter()}catch(e){toast(e.message||'No se pudo iniciar sesión')}finally{load(loginBtn,false)}}
async function register(){try{if(!regName.value||!regOrg.value||!regEmail.value||!regPassword.value){toast('Completá todos los campos.');return}load(registerBtn,true);const r=await fetch(API_URL+'/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:regName.value,organization_name:regOrg.value,email:regEmail.value,password:regPassword.value})});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Error');currentUser=d.user;enter()}catch(e){toast(e.message||'No se pudo crear cuenta')}finally{load(registerBtn,false)}}
function enter(){currentWorkspaceId=currentUser.workspace_id||1;localStorage.setItem('marketprop_workspace_id',currentWorkspaceId);authScreen.classList.add('hidden');appScreen.classList.remove('hidden');welcomeTitle.innerText='Hola, '+(currentUser.organization_name||currentUser.name);orgName.innerText=currentUser.organization_name;planName.innerText=currentUser.plan;toast('Bienvenido a MarketProp');renderAllDashboards();/* admin-only: loadWorkspaceDashboard() */}
function logout(){location.reload()}
function show(id,btn){document.querySelectorAll('.section').forEach(s=>s.classList.remove('active-section'));document.getElementById(id).classList.add('active-section');document.querySelectorAll('.nav').forEach(n=>n.classList.remove('active'));if(btn)btn.classList.add('active'); if(['command','pipeline','calendar','sources','stats'].includes(id)) renderAllDashboards(); if(id==='realData') loadRealDataDashboard(); if(id==='workspace') /* admin-only: loadWorkspaceDashboard() */}
function notifySoon(){toast('Función preparada para el próximo sprint.')}
async function generateContent(){const url=propertyUrl.value.trim();if(!url){toast('Pegá el link de una propiedad.');return}if(!url.startsWith('http://')&&!url.startsWith('https://')){toast('El link debe empezar con http:// o https://');return}results.innerHTML='<h3>Contenido</h3><p>Generando contenido con MarketMind...</p>';scan.innerHTML='';status.innerText='MarketMind está coordinando agentes...';load(generateBtn,true);for(const s of ['Agente Propiedad analiza el link','Agente Copy define el enfoque','MarketMind elige agente, proveedor y modelo','Agente Evaluador puntúa calidad','Contenido listo']){await new Promise(r=>setTimeout(r,220));scan.innerHTML+='✓ '+s+'<br>'}try{const r=await fetch(API_URL+'/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url,style:globalStyle.value})});const d=await r.json();if(!r.ok)throw new Error(d.detail||'No se pudo generar');currentProperty=d.property;renderResults(d.content);status.innerText='Contenido generado correctamente.';toast('Contenido generado')}catch(e){toast(e.message||'Error al generar');status.innerText='Error'}finally{load(generateBtn,false)}}
function renderResults(c){const names={facebook:'Facebook',instagram:'Instagram',tiktok:'TikTok',whatsapp:'WhatsApp',mercado_libre:'Mercado Libre',meta_ads:'Meta Ads'};const logos={facebook:'f',instagram:'IG',tiktok:'TK',whatsapp:'WA',mercado_libre:'ML',meta_ads:'Meta'};let h='<h3>Contenido generado</h3><div class="result-grid">';Object.keys(c).forEach(k=>{let v=c[k].text;if(typeof v==='object')v=JSON.stringify(v,null,2);h+=`<div class="result-card"><h3 class="platform-title"><span class="platform-logo ${k}">${logos[k]}</span>${names[k]}</h3><span class="style-badge">${c[k].agent||'agente'} · ${c[k].provider||'mock'} · ${c[k].model||'modelo'} · ${c[k].style}</span><p class="score">MarketMind Score: ${c[k].score}/100</p><pre id="text-${k}">${esc(v)}</pre><div class="actions"><button onclick="copyResult('${k}',this)">Copiar</button><button class="outline" onclick="variation('${k}','auto',this)">Dame otra</button><button class="outline" onclick="variation('${k}','premium',this)">Premium</button><button class="outline" onclick="variation('${k}','urgencia',this)">Urgencia</button><button class="outline" onclick="variation('${k}','inversor',this)">Inversor</button></div></div>`});results.innerHTML=h+'</div>'}
async function variation(platform,style,btn){if(!currentProperty){toast('Primero generá contenido.');return}try{load(btn,true);const r=await fetch(API_URL+'/variation',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({platform,property_data:currentProperty,style})});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Error');let v=d.variation.text;if(typeof v==='object')v=JSON.stringify(v,null,2);document.getElementById('text-'+platform).innerText=v;if(btn){const oldText=btn.innerHTML;btn.innerHTML='✓ Actualizado';setTimeout(()=>btn.innerHTML=oldText,1200)}toast('Nueva variación generada')}catch(e){toast(e.message||'Error')}finally{load(btn,false)}}
function copyResult(k,btn){const el=document.getElementById('text-'+k);if(!el){toast('No hay contenido');return}navigator.clipboard.writeText(el.innerText).then(()=>{const old=btn.innerHTML;btn.innerHTML='✓ Copiado';btn.classList.add('copied');setTimeout(()=>{btn.innerHTML=old;btn.classList.remove('copied')},1400);toast('Copiado')})}
async function runHookAgent(){if(!hookPrompt.value.trim()){toast('Escribí una idea para Agente Hook.');return}hookAgentResult.innerHTML='Agente Hook está analizando...';await new Promise(r=>setTimeout(r,650));hookAgentResult.innerHTML='<b>Agente Hook</b><br><br>No empezaría mostrando la propiedad. Empezaría con una tensión o curiosidad.<br><br><b>Hook recomendado:</b><br>“Antes de comprar una propiedad, mirá este detalle que casi nadie revisa.”<br><br><b>Hook Score:</b> 92/100<br><b>Índice de novedad:</b> 88/100<br><b>Saturación:</b> 19/100<br><br><b>Mi consejo:</b> usalo como primera frase del Reel y recién después mostrás la propiedad.';toast('Agente Hook respondió')}
async function loadProviderStatus(){try{const r=await fetch(API_URL+'/marketmind/providers');const d=await r.json();toast(`Demo: ${d.demo_mode} · OpenAI: ${d.providers.openai.available} · Claude: ${d.providers.anthropic.available} · Gemini: ${d.providers.gemini.available}`)}catch(e){toast('No pude leer proveedores')}}
async function renderCommandCenter(){
 try{
  const r=await fetch(API_URL+'/analytics/command-center');
  const d=await r.json();

  const socialMetrics=(d.social_metrics||[]);
  const social='<div class="restore-block"><div class="panel-head mini"><div><span class="pill">Restaurado · Redes sociales</span><h3>Métricas de redes</h3><p>Views, alcance, seguidores, engagement, DMs y señales que ya estaban en la lógica anterior.</p></div></div><div class="metric-grid social-metrics">'+socialMetrics.map(k=>`
    <div class="metric-card restored">
      <span>${esc(k.label)}</span>
      <b>${esc(k.value)}</b>
      <p>${esc(k.detail)}</p>
      <em>${esc(k.delta)}</em>
    </div>`).join('')+'</div></div>';

  const kpis='<div class="restore-block"><div class="panel-head mini"><div><span class="pill">MarketProp · Inmobiliario</span><h3>Métricas comerciales</h3><p>KPIs propios del negocio inmobiliario y del motor MarketMind.</p></div></div><div class="metric-grid command-metrics">'+d.kpis.map(k=>`
    <div class="metric-card polished">
      <span>${esc(k.label)}</span>
      <b>${esc(k.value)}</b>
      <p>${esc(k.detail)}</p>
      <em>${esc(k.delta)}</em>
    </div>`).join('')+'</div></div>';

  const quality=`
    <div class="quality-shell">
      <div class="quality-main">
        <span class="pill">Quality Gate</span>
        <h3>${d.quality.score}% de calidad general</h3>
        <p>MarketMind revisa hook, CTA, claridad, plataforma y originalidad antes de aprobar contenido.</p>
        <div class="quality-bar"><span style="width:${d.quality.score}%"></span></div>
      </div>
      <div class="quality-cards">
        <div><b>${d.quality.ready}</b><span>publicables hoy</span></div>
        <div><b>${d.quality.blocked}</b><span>bloqueos</span></div>
        <div><b>${d.quality.weak_hooks}</b><span>hooks débiles</span></div>
        <div><b>${d.quality.weak_cta}</b><span>CTAs flojos</span></div>
      </div>
    </div>`;

  const funnel=`
    <div class="chart-card-soft">
      <div class="panel-head mini"><div><span class="pill">Funnel comercial</span><h3>Vista → DM → visita</h3></div></div>
      <div class="funnel-list">${d.funnel.map(x=>`
        <div class="funnel-row">
          <div><b>${esc(x.label)}</b><span>${esc(x.value)}</span></div>
          <div class="quality-bar small"><span style="width:${x.pct}%"></span></div>
        </div>`).join('')}</div>
    </div>`;

  const formats=`
    <div class="chart-card-soft">
      <div class="panel-head mini"><div><span class="pill">Formatos</span><h3>Qué conviene publicar</h3></div></div>
      <div class="format-bars">${d.format_reach.map(x=>`
        <div class="format-row">
          <div><b>${esc(x.label)}</b><span>${esc(x.detail)}</span></div>
          <div class="quality-bar small"><span style="width:${x.value}%"></span></div>
          <strong>${x.value}</strong>
        </div>`).join('')}</div>
    </div>`;

  const signals=`
    <div class="chart-card-soft">
      <div class="panel-head mini"><div><span class="pill">Señales por propiedad</span><h3>Oportunidades comerciales</h3></div></div>
      <div class="signal-grid">${d.property_signals.map(x=>`
        <div class="signal-card">
          <span>${esc(x.signal)}</span>
          <h3>${esc(x.title)}</h3>
          <p>${esc(x.action)}</p>
          <b>${x.score}/100</b>
        </div>`).join('')}</div>
    </div>`;

  const slots=`
    <div class="chart-card-soft">
      <div class="panel-head mini"><div><span class="pill">Horarios</span><h3>Mejores slots mock</h3></div></div>
      <div class="slot-grid">${d.weekly_slots.map(x=>`
        <div class="slot-card">
          <b>${esc(x.day)}</b><span>${esc(x.hour)}</span>
          <div class="quality-bar tiny"><span style="width:${x.score}%"></span></div>
        </div>`).join('')}</div>
    </div>`;

  const alerts='<div class="card-list">'+d.alerts.map(a=>`
    <div class="alert-card ${esc(a.level)}">
      <h3>${esc(a.title)}</h3>
      <p>${esc(a.text)}</p>
      <span>${esc(a.level)}</span>
    </div>`).join('')+'</div>';

  const insights='<div class="source-grid">'+d.insights.map(i=>`
    <div class="insight-card">
      <span>MarketMind Insight</span>
      <h3>${esc(i.title)}</h3>
      <p>${esc(i.text)}</p>
    </div>`).join('')+'</div>';

  commandContent.innerHTML=
    social+
    kpis+
    '<div class="command-grid polished-grid">'+quality+funnel+'</div>'+
    '<div class="command-grid polished-grid">'+formats+slots+'</div>'+
    signals+
    '<br><h3>Alertas inteligentes</h3>'+alerts+
    '<br><h3>Insights accionables</h3>'+insights;

  statsContent.innerHTML=`
    <div><b>${d.quality.score}%</b><span>Quality Gate</span></div>
    <div><b>${d.quality.ready}</b><span>Publicables</span></div>
    <div><b>${d.quality.blocked}</b><span>Bloqueos</span></div>`;
 }catch(e){commandContent.innerHTML='<p>No pude cargar Command Center.</p>'}
}
async function renderPipeline(){
 try{
  const r=await fetch(API_URL+'/analytics/pipeline-detail');
  const d=await r.json();
  pipelineBoard.innerHTML=d.statuses.map(st=>{
    const items=d.items.filter(x=>x.status===st);
    return `<div class="pipeline-col polished operational">
      <h3>${esc(st)}<span>${items.length}</span></h3>
      ${items.map(x=>`<div class="pipeline-card operational-card">
        <span>${esc(x.platform)} · ${esc(x.format)} · ${esc(x.owner||'Equipo')}</span>
        <h3>${esc(x.property)}</h3>
        <p><b>Objetivo:</b> ${esc(x.objective)}</p>
        <p><b>Próxima acción:</b> ${esc(x.next_action)}</p>
        <p><b>Fuente:</b> ${esc(x.source)}</p>
        <div class="quality-bar tiny"><span style="width:${x.score}%"></span></div>
        <small>Score ${x.score}/100 · ${esc(x.blocker)}</small>
      </div>`).join('')||'<p>Vacío</p>'}
    </div>`
  }).join('')
 }catch(e){pipelineBoard.innerHTML='<p>No pude cargar el pipeline.</p>'}
}
async function renderCalendar(){
 try{
  const r=await fetch(API_URL+'/analytics/calendar-detail');
  const d=await r.json();
  const days=['Lun','Mar','Mié','Jue','Vie','Sáb','Dom'];
  calendarGrid.innerHTML=days.map(day=>{
    const items=d.items.filter(x=>x.day===day);
    return `<div class="calendar-day polished">
      <h3>${day}<span>${items.length}</span></h3>
      ${items.map(x=>`<div class="calendar-item polished">
        <span>${esc(x.time)} · ${esc(x.platform)}</span>
        <h4>${esc(x.title)}</h4>
        <p>${esc(x.property)} · ${esc(x.goal)}</p>
        <div class="quality-bar tiny"><span style="width:${x.score}%"></span></div>
        <small>Score ${x.score}/100</small>
      </div>`).join('')||'<p>Sin publicaciones</p>'}
    </div>`
  }).join('')
 }catch(e){calendarGrid.innerHTML='<p>No pude cargar calendario.</p>'}
}
async function renderSources(){
 try{
  const r=await fetch(API_URL+'/analytics/marketdna-sources-detail');
  const d=await r.json();
  sourcesGrid.innerHTML=d.items.map(s=>`<div class="source-card polished-source">
    <span>${esc(s.type)} · ${esc(s.status)}</span>
    <h3>${esc(s.name)}</h3>
    <p>${esc(s.value)}</p>
    <div class="tags">${s.signals.map(t=>`<em>${esc(t)}</em>`).join('')}</div>
  </div>`).join('')
 }catch(e){sourcesGrid.innerHTML='<p>No pude cargar fuentes MarketDNA.</p>'}
}
async function createProperty(){const title=newPropertyTitle.value.trim();if(!title){toast('Poné un título de propiedad');return}const url=newPropertyUrl.value.trim();try{await apiPost('/data/properties',{title,url,location:'Rosario',property_type:'Propiedad',price:'',notes:'Creada desde MarketProp'});newPropertyTitle.value='';newPropertyUrl.value='';toast('Propiedad guardada en base real');loadPropertiesReal();loadRealDataDashboard()}catch(e){toast('No se pudo guardar en base real')}}
function renderAllDashboards(){renderCommandCenter();renderPipeline();renderCalendar();renderSources();loadPropertiesReal();loadRealDataDashboard();/* admin-only: loadWorkspaceDashboard() */}
function esc(t){return String(t).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}


// v0.3.10.1 SaaS Foundation - persistent data layer
async function apiGet(path){const r=await fetch(API_URL+path,{headers:{'x-workspace-id':String(currentWorkspaceId||1)}});if(!r.ok)throw new Error(path);return await r.json()}
async function apiPost(path,payload){const r=await fetch(API_URL+path,{method:'POST',headers:{'Content-Type':'application/json','x-workspace-id':String(currentWorkspaceId||1)},body:JSON.stringify(payload)});if(!r.ok)throw new Error(path);return await r.json()}
async function loadPropertiesReal(){
  if(!document.getElementById('propertyList')) return;
  try{const props=await apiGet('/data/properties');propertyList.innerHTML=props.map(p=>`<div class="source-card"><h3>${esc(p.title)}</h3><p>${esc(p.location||'Sin zona')} · ${esc(p.property_type||'Tipo')} · ${esc(p.price||'Sin precio')}</p><small>${esc(p.url||'Sin link')}</small></div>`).join('')}
  catch(e){}
}
async function loadRealDataDashboard(){
  const holder=document.getElementById('realDataContent'); if(!holder) return;
  try{const [props,contents,pipeline,calendar,sources]=await Promise.all([apiGet('/data/properties'),apiGet('/data/contents'),apiGet('/data/pipeline'),apiGet('/data/calendar'),apiGet('/data/sources')]);
  holder.innerHTML=`
    <div class="metric-grid command-metrics">
      <div class="metric-card polished"><span>Propiedades guardadas</span><b>${props.length}</b><p>Persisten en SQLite</p><em>real local</em></div>
      <div class="metric-card polished"><span>Contenidos guardados</span><b>${contents.length}</b><p>No se pierden al cerrar</p><em>real local</em></div>
      <div class="metric-card polished"><span>Pipeline real</span><b>${pipeline.length}</b><p>Items guardados</p><em>real local</em></div>
      <div class="metric-card polished"><span>Calendario real</span><b>${calendar.length}</b><p>Publicaciones guardadas</p><em>real local</em></div>
    </div>
    <div class="command-grid polished-grid">
      <div class="chart-card-soft"><div class="panel-head mini"><div><span class="pill">Propiedades reales</span><h3>Base de propiedades</h3></div></div>${props.map(p=>`<div class="db-row"><b>${esc(p.title)}</b><span>${esc(p.location||'Sin zona')} · ${esc(p.property_type||'Tipo')} · ${esc(p.price||'Sin precio')}</span></div>`).join('')}</div>
      <div class="chart-card-soft"><div class="panel-head mini"><div><span class="pill">Contenido real</span><h3>Contenido guardado</h3></div></div>${contents.map(c=>`<div class="db-row"><b>${esc(c.platform)} · ${esc(c.title||'Contenido')}</b><span>${esc((c.body||'').slice(0,120))}...</span></div>`).join('')}</div>
    </div>
    <div class="command-grid polished-grid">
      <div class="chart-card-soft"><div class="panel-head mini"><div><span class="pill">Pipeline real</span><h3>Estados guardados</h3></div></div>${pipeline.map(p=>`<div class="db-row"><b>${esc(p.status)} · ${esc(p.property_title)}</b><span>${esc(p.next_action||'Sin próxima acción')}</span></div>`).join('')}</div>
      <div class="chart-card-soft"><div class="panel-head mini"><div><span class="pill">MarketDNA real local</span><h3>Fuentes guardadas</h3></div></div>${sources.map(s=>`<div class="db-row"><b>${esc(s.name)}</b><span>${esc(s.value||'Sin detalle')}</span></div>`).join('')}</div>
    </div>`}
  catch(e){holder.innerHTML='<p>No pude cargar la base de datos local. Revisá que el backend esté prendido.</p>'}
}
async function createDemoProperty(){
  const title='Propiedad nueva '+new Date().toLocaleTimeString();
  await apiPost('/data/properties',{title,url:'https://www.ejemplo.com/propiedad-nueva',location:'Rosario',property_type:'Departamento',price:'USD 100.000',notes:'Creada desde la app en v0.3.10.1'});
  await apiPost('/data/pipeline',{property_title:title,platform:'Instagram',format:'Reel',objective:'Generar consulta',status:'Propiedad cargada',owner:'Agus',score:82,next_action:'Generar contenido multired',blocker:'Sin bloqueo',source:'Alta manual'});
  toast('Propiedad guardada en la base real local');loadPropertiesReal();loadRealDataDashboard();
}


// v0.3.10.1 Workspace / Multiuser Foundation
async function /* admin-only: loadWorkspaceDashboard() */{
  const holder=document.getElementById('workspaceContent'); if(!holder) return;
  try{
    const d=await apiGet('/workspace/current');
    const plan=d.plan||{};
    const contentLimit=plan.monthly_content_limit||500;
    const aiLimit=plan.ai_credit_limit||100000;
    const seatsLimit=plan.seats_limit||2;
    const contentPct=Math.min(100,Math.round((d.usage.content_generated/contentLimit)*100));
    const aiPct=Math.min(100,Math.round((d.usage.ai_credits_used/aiLimit)*100));
    holder.innerHTML=`
      <div class="workspace-hero">
        <div><span class="pill">Workspace real local</span><h2>${esc(d.workspace.name)}</h2><p>Slug: ${esc(d.workspace.slug)} · Estado: ${esc(d.workspace.status)} · ID: ${d.workspace.id}</p></div>
        <div class="score-orb">${esc(d.workspace.plan)}</div>
      </div>
      <div class="metric-grid command-metrics">
        <div class="metric-card polished"><span>Miembros</span><b>${d.members.length}/${seatsLimit}</b><p>Usuarios del workspace</p><em>pre multiusuario</em></div>
        <div class="metric-card polished"><span>Contenido mensual</span><b>${d.usage.content_generated}/${contentLimit}</b><p>Límite por plan</p><em>${contentPct}% usado</em></div>
        <div class="metric-card polished"><span>Créditos IA</span><b>${d.usage.ai_credits_used}</b><p>Sobre ${aiLimit}</p><em>${aiPct}% usado</em></div>
        <div class="metric-card polished"><span>Datos del workspace</span><b>${d.counts.properties+d.counts.contents+d.counts.pipeline+d.counts.calendar+d.counts.sources}</b><p>Registros separados</p><em>workspace_id</em></div>
      </div>
      <div class="command-grid polished-grid">
        <div class="chart-card-soft"><div class="panel-head mini"><div><span class="pill">Equipo</span><h3>Miembros y roles</h3></div></div>${d.members.map(m=>`<div class="db-row"><b>${esc(m.name)} · ${esc(m.role)}</b><span>${esc(m.email)} · ${esc(m.status)}</span></div>`).join('')}</div>
        <div class="chart-card-soft"><div class="panel-head mini"><div><span class="pill">Plan</span><h3>Suscripción preparada</h3></div></div>
          <div class="db-row"><b>${esc(plan.plan_name||d.workspace.plan)} · ${esc(plan.status||'trial')}</b><span>Contenido: ${contentLimit}/mes · Créditos IA: ${aiLimit} · Seats: ${seatsLimit}</span></div>
          <div class="quality-bar tiny"><span style="width:${contentPct}%"></span></div><small>Uso contenido ${contentPct}%</small>
          <div class="quality-bar tiny"><span style="width:${aiPct}%"></span></div><small>Uso IA ${aiPct}%</small>
        </div>
      </div>
      <div class="command-grid polished-grid">
        <div class="chart-card-soft"><div class="panel-head mini"><div><span class="pill">Datos separados</span><h3>Conteo por entidad</h3></div></div>
          ${Object.keys(d.counts).map(k=>`<div class="db-row"><b>${esc(k)}</b><span>${d.counts[k]} registros en este workspace</span></div>`).join('')}
        </div>
        <div class="chart-card-soft"><div class="panel-head mini"><div><span class="pill">Arquitectura</span><h3>Preparado para SaaS</h3></div></div>
          <div class="db-row"><b>workspace_id</b><span>Propiedades, contenido, pipeline, calendario y MarketDNA quedan asociados a una inmobiliaria.</span></div>
          <div class="db-row"><b>Roles</b><span>Owner / admin / member listo para evolucionar a permisos reales.</span></div>
          <div class="db-row"><b>Planes</b><span>Básico, Pro y Business ya pueden tener límites separados.</span></div>
        </div>
      </div>`;
  }catch(e){holder.innerHTML='<p>No pude cargar Workspace. Revisá backend.</p>'}
}
async function addDemoMember(){
  const stamp=new Date().toLocaleTimeString().replaceAll(':','');
  try{await apiPost('/workspace/members',{name:'Miembro demo '+stamp,email:'miembro'+stamp+'@marketprop.local',role:'member'});toast('Miembro demo agregado al workspace');/* admin-only: loadWorkspaceDashboard() */}catch(e){toast('No pude agregar miembro')}
}
