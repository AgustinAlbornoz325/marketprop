const API_URL='http://127.0.0.1:8000/api';let currentProperty=null,currentUser=null;
const pipelineStatuses=['Propiedad cargada','Contenido generado','Revisión pendiente','Aprobado','Publicado','Midiendo'];
function toast(msg){const t=document.getElementById('toast');t.innerText=msg;t.classList.remove('hidden');setTimeout(()=>t.classList.add('hidden'),2600)}
function load(btn,on){if(!btn)return;if(on){btn.dataset.old=btn.innerHTML;btn.disabled=true;btn.innerHTML='Procesando...'}else{btn.disabled=false;btn.innerHTML=btn.dataset.old||btn.innerHTML}}
function setAuth(m){document.querySelectorAll('.tabs button').forEach(b=>b.classList.remove('active'));if(m==='login'){loginTab.classList.add('active');loginForm.classList.remove('hidden');registerForm.classList.add('hidden')}else{registerTab.classList.add('active');registerForm.classList.remove('hidden');loginForm.classList.add('hidden')}}
async function login(){try{if(!loginEmail.value||!loginPassword.value){toast('Completá email y contraseña.');return}load(loginBtn,true);const r=await fetch(API_URL+'/auth/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:loginEmail.value,password:loginPassword.value})});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Error');currentUser=d.user;enter()}catch(e){toast(e.message||'No se pudo iniciar sesión')}finally{load(loginBtn,false)}}
async function register(){try{if(!regName.value||!regOrg.value||!regEmail.value||!regPassword.value){toast('Completá todos los campos.');return}load(registerBtn,true);const r=await fetch(API_URL+'/auth/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:regName.value,organization_name:regOrg.value,email:regEmail.value,password:regPassword.value})});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Error');currentUser=d.user;enter()}catch(e){toast(e.message||'No se pudo crear cuenta')}finally{load(registerBtn,false)}}
function enter(){authScreen.classList.add('hidden');appScreen.classList.remove('hidden');welcomeTitle.innerText='Hola, '+(currentUser.organization_name||currentUser.name);orgName.innerText=currentUser.organization_name;planName.innerText=currentUser.plan;toast('Bienvenido a MarketProp');renderAllDashboards()}
function logout(){location.reload()}
function show(id,btn){document.querySelectorAll('.section').forEach(s=>s.classList.remove('active-section'));document.getElementById(id).classList.add('active-section');document.querySelectorAll('.nav').forEach(n=>n.classList.remove('active'));if(btn)btn.classList.add('active'); if(['command','pipeline','calendar','sources','stats'].includes(id)) renderAllDashboards()}
function notifySoon(){toast('Función preparada para el próximo sprint.')}
async function generateContent(){const url=propertyUrl.value.trim();if(!url){toast('Pegá el link de una propiedad.');return}if(!url.startsWith('http://')&&!url.startsWith('https://')){toast('El link debe empezar con http:// o https://');return}results.innerHTML='<h3>Contenido</h3><p>Generando contenido con MarketMind...</p>';scan.innerHTML='';status.innerText='MarketMind está coordinando agentes...';load(generateBtn,true);for(const s of ['Agente Propiedad analiza el link','Agente Copy define el enfoque','MarketMind elige agente, proveedor y modelo','Agente Evaluador puntúa calidad','Contenido listo']){await new Promise(r=>setTimeout(r,220));scan.innerHTML+='✓ '+s+'<br>'}try{const r=await fetch(API_URL+'/generate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url,style:globalStyle.value})});const d=await r.json();if(!r.ok)throw new Error(d.detail||'No se pudo generar');currentProperty=d.property;renderResults(d.content);status.innerText='Contenido generado correctamente.';toast('Contenido generado')}catch(e){toast(e.message||'Error al generar');status.innerText='Error'}finally{load(generateBtn,false)}}
function renderResults(c){const names={facebook:'Facebook',instagram:'Instagram',tiktok:'TikTok',whatsapp:'WhatsApp',mercado_libre:'Mercado Libre',meta_ads:'Meta Ads'};let h='<h3>Contenido generado</h3><div class="result-grid">';Object.keys(c).forEach(k=>{let v=c[k].text;if(typeof v==='object')v=JSON.stringify(v,null,2);h+=`<div class="result-card"><h3>${names[k]}</h3><span class="style-badge">${c[k].agent||'agente'} · ${c[k].provider||'mock'} · ${c[k].model||'modelo'} · ${c[k].style}</span><p class="score">MarketMind Score: ${c[k].score}/100</p><pre id="text-${k}">${esc(v)}</pre><div class="actions"><button onclick="copyResult('${k}',this)">Copiar</button><button class="outline" onclick="variation('${k}','auto',this)">Dame otra</button><button class="outline" onclick="variation('${k}','premium',this)">Premium</button><button class="outline" onclick="variation('${k}','urgencia',this)">Urgencia</button><button class="outline" onclick="variation('${k}','inversor',this)">Inversor</button></div></div>`});results.innerHTML=h+'</div>'}
async function variation(platform,style,btn){if(!currentProperty){toast('Primero generá contenido.');return}try{load(btn,true);const r=await fetch(API_URL+'/variation',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({platform,property_data:currentProperty,style})});const d=await r.json();if(!r.ok)throw new Error(d.detail||'Error');let v=d.variation.text;if(typeof v==='object')v=JSON.stringify(v,null,2);document.getElementById('text-'+platform).innerText=v;if(btn){const oldText=btn.innerHTML;btn.innerHTML='✓ Actualizado';setTimeout(()=>btn.innerHTML=oldText,1200)}toast('Nueva variación generada')}catch(e){toast(e.message||'Error')}finally{load(btn,false)}}
function copyResult(k,btn){const el=document.getElementById('text-'+k);if(!el){toast('No hay contenido');return}navigator.clipboard.writeText(el.innerText).then(()=>{const old=btn.innerHTML;btn.innerHTML='✓ Copiado';btn.classList.add('copied');setTimeout(()=>{btn.innerHTML=old;btn.classList.remove('copied')},1400);toast('Copiado')})}
async function runHookAgent(){if(!hookPrompt.value.trim()){toast('Escribí una idea para Agente Hook.');return}hookAgentResult.innerHTML='Agente Hook está analizando...';await new Promise(r=>setTimeout(r,650));hookAgentResult.innerHTML='<b>Agente Hook</b><br><br>No empezaría mostrando la propiedad. Empezaría con una tensión o curiosidad.<br><br><b>Hook recomendado:</b><br>“Antes de comprar una propiedad, mirá este detalle que casi nadie revisa.”<br><br><b>Hook Score:</b> 92/100<br><b>Índice de novedad:</b> 88/100<br><b>Saturación:</b> 19/100<br><br><b>Mi consejo:</b> usalo como primera frase del Reel y recién después mostrás la propiedad.';toast('Agente Hook respondió')}
async function loadProviderStatus(){try{const r=await fetch(API_URL+'/marketmind/providers');const d=await r.json();toast(`Demo: ${d.demo_mode} · OpenAI: ${d.providers.openai.available} · Claude: ${d.providers.anthropic.available} · Gemini: ${d.providers.gemini.available}`)}catch(e){toast('No pude leer proveedores')}}
async function renderCommandCenter(){
 try{
  const r=await fetch(API_URL+'/analytics/command-center');
  const d=await r.json();

  const kpis='<div class="metric-grid command-metrics">'+d.kpis.map(k=>`
    <div class="metric-card polished">
      <span>${esc(k.label)}</span>
      <b>${esc(k.value)}</b>
      <p>${esc(k.detail)}</p>
      <em>${esc(k.delta)}</em>
    </div>`).join('')+'</div>';

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
  const r=await fetch(API_URL+'/analytics/pipeline');
  const d=await r.json();
  pipelineBoard.innerHTML=pipelineStatuses.map(st=>{
    const items=d.items.filter(x=>x.status===st);
    return `<div class="pipeline-col polished">
      <h3>${st}<span>${items.length}</span></h3>
      ${items.map(x=>`<div class="pipeline-card">
        <span>${esc(x.platform)} · ${esc(x.format)} · ${esc(x.owner||'Equipo')}</span>
        <h3>${esc(x.property)}</h3>
        <p>${esc(x.objective)}</p>
        <div class="quality-bar tiny"><span style="width:${x.score}%"></span></div>
        <small>Score ${x.score}/100</small>
      </div>`).join('')||'<p>Vacío</p>'}
    </div>`
  }).join('')
 }catch(e){}
}
async function renderCalendar(){try{const r=await fetch(API_URL+'/analytics/calendar');const d=await r.json();calendarGrid.innerHTML=d.items.map(x=>`<div class="day-card"><span>${esc(x.day)} · ${esc(x.time)}</span><h3>${esc(x.title)}</h3><p>${esc(x.platform)}</p></div>`).join('')}catch(e){}}
async function renderSources(){try{const r=await fetch(API_URL+'/marketdna/sources');const d=await r.json();sourcesGrid.innerHTML=d.items.map(s=>`<div class="source-card"><span>${esc(s.type)}</span><h3>${esc(s.name)}</h3><p>${esc(s.summary)}</p><div class="tags">${s.tags.map(t=>`<span>${esc(t)}</span>`).join('')}</div></div>`).join('')}catch(e){}}
async function createProperty(){const title=newPropertyTitle.value.trim();if(!title){toast('Poné un título de propiedad');return}const url=newPropertyUrl.value.trim();try{const r=await fetch(API_URL+'/properties',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title,url})});const d=await r.json();propertyList.innerHTML+=`<div class="source-card"><h3>${esc(d.item.title)}</h3><p>${esc(d.item.url||'Sin link')}</p></div>`;newPropertyTitle.value='';newPropertyUrl.value='';toast('Propiedad creada en demo')}catch(e){toast('No se pudo crear')}}
function renderAllDashboards(){renderCommandCenter();renderPipeline();renderCalendar();renderSources()}
function esc(t){return String(t).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]))}
