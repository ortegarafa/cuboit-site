/* Cuboit — tema, menu, simulador e formulário */
(function(){
  var root=document.documentElement;
  var $=function(id){return document.getElementById(id)};
  var lang=root.lang||'pt-BR', en=lang.indexOf('en')===0;
  var T=en
    ? {perMonth:'/mo', toDark:'Switch to dark mode', toLight:'Switch to light mode',
       sending:'Sending…', noEndpoint:'The form is not connected yet. Please email contato@cuboit.com.br.',
       fail:'We could not send your request. Please try again or email contato@cuboit.com.br.',
       badPhone:'Enter a valid phone number for the selected country.', noCountry:'No country found', country:'Country'}
    : {perMonth:'/mês', toDark:'Ativar modo escuro', toLight:'Ativar modo claro',
       sending:'Enviando…', noEndpoint:'O formulário ainda não está conectado. Escreva para contato@cuboit.com.br.',
       fail:'Não foi possível enviar. Tente de novo ou escreva para contato@cuboit.com.br.',
       badPhone:'Informe um telefone válido para o país selecionado.', noCountry:'Nenhum país encontrado', country:'País'};

  // Tema: segue o sistema até a pessoa escolher; a escolha fica salva neste navegador
  var mq=window.matchMedia?window.matchMedia('(prefers-color-scheme: dark)'):null;
  var themeBtn=$('themeBtn');
  function current(){return root.getAttribute('data-theme')||(mq&&mq.matches?'dark':'light')}
  function paint(){
    if(!themeBtn)return;
    var m=current();
    themeBtn.setAttribute('data-mode',m);
    themeBtn.setAttribute('aria-label',m==='dark'?T.toLight:T.toDark);
    themeBtn.title=themeBtn.getAttribute('aria-label');
  }
  if(themeBtn){
    themeBtn.addEventListener('click',function(){
      var next=current()==='dark'?'light':'dark';
      root.setAttribute('data-theme',next);
      try{localStorage.setItem('cuboit-theme',next)}catch(e){}
      paint();
    });
    if(mq&&mq.addEventListener)mq.addEventListener('change',paint);
    paint();
  }

  // Menu mobile
  var btn=$('menuBtn'),menu=$('menu');
  if(btn&&menu)btn.addEventListener('click',function(){var o=menu.classList.toggle('open');btn.setAttribute('aria-expanded',o)});
  if(menu)menu.addEventListener('click',function(e){if(e.target.tagName==='A'){menu.classList.remove('open');btn.setAttribute('aria-expanded','false')}});

  // Simulador: moeda definida em <html data-currency>
  var cur=root.getAttribute('data-currency')||'BRL';
  var nf=new Intl.NumberFormat(lang);
  var m0=new Intl.NumberFormat(lang,{style:'currency',currency:cur,maximumFractionDigits:0});
  var m2=new Intl.NumberFormat(lang,{style:'currency',currency:cur,minimumFractionDigits:2,maximumFractionDigits:2});
  var m3=new Intl.NumberFormat(lang,{style:'currency',currency:cur,minimumFractionDigits:3,maximumFractionDigits:4});
  function calc(){
    var r=+$('req').value,n=+$('msgs').value,b=+$('big').value,s=+$('small').value,p=+$('share').value/100;
    $('reqO').textContent=nf.format(r);$('msgsO').textContent=n;
    $('bigO').textContent=m3.format(b);$('smallO').textContent=m3.format(s);$('shareO').textContent=Math.round(p*100)+'%';
    // cada mensagem relê o histórico: a k-ésima custa ~ (1 + 0,25·(k-1)) × custo da primeira
    var f=n+0.25*n*(n-1)/2, perBig=b*f, perMix=p*s*f+(1-p)*b*f;
    $('pBig').textContent=m2.format(perBig);$('pMix').textContent=m2.format(perMix);
    var big=r*perBig, mix=r*perMix, save=big-mix;
    $('cBig').textContent=m0.format(big)+T.perMonth;$('cMix').textContent=m0.format(mix)+T.perMonth;
    $('barMix').style.width=Math.max(2,mix/big*100)+'%';
    $('pct').textContent=Math.round(save/big*100)+'%';$('abs').textContent=m0.format(save)+T.perMonth;
  }
  if($('req')){['req','msgs','big','small','share'].forEach(function(id){$(id).addEventListener('input',calc)});calc();}

  // Telefone: país com bandeira + DDI separado + máscara por país
  // [código ISO, DDI, máscaras por quantidade de dígitos ('#' = dígito)]
  var COUNTRIES=[
    ['BR','55',{10:'(##) ####-####',11:'(##) #####-####'}],['US','1',{10:'(###) ###-####'}],['PT','351',{9:'### ### ###'}],
    ['AR','54',{10:'## ####-####'}],['CL','56',{9:'# #### ####'}],['CO','57',{10:'### ### ####'}],['MX','52',{10:'## #### ####'}],
    ['PE','51',{9:'### ### ###'}],['UY','598',{8:'#### ####'}],['PY','595',{9:'### ### ###'}],['BO','591',{8:'# ### ####'}],
    ['EC','593',{9:'## ### ####'}],['VE','58',{10:'### ###-####'}],['CA','1',{10:'(###) ###-####'}],['GB','44',{10:'#### ######'}],
    ['IE','353',{9:'## ### ####'}],['ES','34',{9:'### ## ## ##'}],['FR','33',{9:'# ## ## ## ##'}],['DE','49',{}],['IT','39',{}],
    ['NL','31',{9:'# ########'}],['BE','32',{9:'### ## ## ##'}],['CH','41',{9:'## ### ## ##'}],['AT','43',{}],['SE','46',{}],
    ['NO','47',{8:'### ## ###'}],['DK','45',{8:'## ## ## ##'}],['PL','48',{9:'### ### ###'}],['AO','244',{9:'### ### ###'}],
    ['MZ','258',{9:'## ### ####'}],['CV','238',{7:'### ## ##'}],['ZA','27',{9:'## ### ####'}],['AE','971',{9:'## ### ####'}],
    ['IL','972',{9:'##-###-####'}],['IN','91',{10:'##### #####'}],['CN','86',{11:'### #### ####'}],['JP','81',{10:'##-####-####'}],
    ['AU','61',{9:'### ### ###'}],['NZ','64',{}]
  ];
  var LIMITS={BR:[10,11],US:[10,10],CA:[10,10]};
  var phoneBox=$('phone');
  if(phoneBox){
    var names=null;try{names=new Intl.DisplayNames([lang],{type:'region'})}catch(e){}
    var nameOf=function(c){try{return names?names.of(c):c}catch(e){return c}};
    var flagUrl=function(c){return 'https://cdn.jsdelivr.net/npm/flag-icons@7.2.3/flags/4x3/'+c.toLowerCase()+'.svg'};
    var def=phoneBox.getAttribute('data-default')||'BR';
    var top=[def,'BR','US','PT'].filter(function(c,i,a){return a.indexOf(c)===i});
    var list=COUNTRIES.map(function(c){return {code:c[0],dial:c[1],masks:c[2],name:nameOf(c[0])}});
    list.sort(function(a,b){var ia=top.indexOf(a.code),ib=top.indexOf(b.code);
      if(ia>-1||ib>-1)return (ia<0?99:ia)-(ib<0?99:ib);return a.name.localeCompare(b.name,lang)});
    var byCode={};list.forEach(function(c){byCode[c.code]=c});
    var ddiBtn=$('ddiBtn'),pop=$('ddiPop'),search=$('ddiSearch'),ul=$('ddiList'),tel=$('telefone');
    var sel=byCode[def]||list[0], shown=[], active=0;

    function digits(v){return v.replace(/\D/g,'')}
    function limits(c){if(LIMITS[c.code])return LIMITS[c.code];var k=Object.keys(c.masks).map(Number);
      return k.length?[Math.min.apply(null,k),Math.max.apply(null,k)]:[6,14]}
    function format(c,d){
      var lim=limits(c);d=d.slice(0,lim[1]);
      var ks=Object.keys(c.masks).map(Number).sort(function(a,b){return a-b}),m=null;
      for(var i=0;i<ks.length;i++){if(d.length<=ks[i]){m=c.masks[ks[i]];break}}
      if(!m&&ks.length)m=c.masks[ks[ks.length-1]];
      if(!m)return d.replace(/(\d{3})(?=\d)/g,'$1 ');
      var out='',j=0;
      for(var k=0;k<m.length&&j<d.length;k++){out+=m[k]==='#'?d[j++]:m[k]}
      return out;
    }
    function sync(){
      var d=digits(tel.value),lim=limits(sel);
      $('pais').value=sel.code;$('ddi').value='+'+sel.dial;
      $('telFmt').value=d?'+'+sel.dial+' '+tel.value:'';
      $('tel164').value=d?'+'+sel.dial+d.replace(/^0+/,''):'';
      tel.setCustomValidity(d&&(d.length<lim[0]||d.length>lim[1])?T.badPhone:'');
    }
    function setCountry(c){
      sel=c;$('ddiFlag').src=flagUrl(c.code);$('ddiCode').textContent='+'+c.dial;
      ddiBtn.setAttribute('aria-label',T.country+': '+c.name+' +'+c.dial);
      var ex={BR:'11912345678',US:'5551234567',CA:'4165551234'}[c.code]||'912345678901234'.slice(0,limits(c)[1]);
      tel.placeholder=format(c,ex);
      tel.value=format(c,digits(tel.value));sync();
    }
    function render(){
      var q=search.value.trim().toLowerCase().replace(/^\+/,'');
      shown=list.filter(function(c){return !q||c.name.toLowerCase().indexOf(q)>-1||c.dial.indexOf(q)===0||c.code.toLowerCase()===q});
      ul.innerHTML='';
      if(!shown.length){var li=document.createElement('li');li.className='none';li.textContent=T.noCountry;ul.appendChild(li);return}
      shown.forEach(function(c,i){
        var li=document.createElement('li');li.setAttribute('role','option');li.id='ddi-'+c.code;
        li.setAttribute('aria-selected',c===sel?'true':'false');if(i===active)li.classList.add('active');
        var img=document.createElement('img');img.className='cflag';img.alt='';img.loading='lazy';img.src=flagUrl(c.code);
        var nm=document.createElement('span');nm.textContent=c.name;
        var dl=document.createElement('small');dl.textContent='+'+c.dial;
        li.appendChild(img);li.appendChild(nm);li.appendChild(dl);
        li.addEventListener('mousedown',function(e){e.preventDefault();choose(c)});
        ul.appendChild(li);
      });
      var a=ul.children[active];if(a&&a.scrollIntoView)a.scrollIntoView({block:'nearest'});
    }
    function open(){pop.hidden=false;ddiBtn.setAttribute('aria-expanded','true');search.value='';active=Math.max(0,list.indexOf(sel));render();search.focus()}
    function close(focusBtn){pop.hidden=true;ddiBtn.setAttribute('aria-expanded','false');if(focusBtn)ddiBtn.focus()}
    function choose(c){setCountry(c);close(false);tel.focus()}
    ddiBtn.addEventListener('click',function(){pop.hidden?open():close(true)});
    search.addEventListener('input',function(){active=0;render()});
    search.addEventListener('keydown',function(e){
      if(e.key==='ArrowDown'){e.preventDefault();active=Math.min(active+1,shown.length-1);render()}
      else if(e.key==='ArrowUp'){e.preventDefault();active=Math.max(active-1,0);render()}
      else if(e.key==='Enter'){e.preventDefault();if(shown[active])choose(shown[active])}
      else if(e.key==='Escape'){e.preventDefault();close(true)}
    });
    document.addEventListener('mousedown',function(e){if(!pop.hidden&&!phoneBox.contains(e.target))close(false)});
    tel.addEventListener('input',function(){
      var v=tel.value.trim();
      // número colado com +DDI: troca o país automaticamente
      if(v.charAt(0)==='+'){var d=digits(v),hit=null;
        list.forEach(function(c){if(d.indexOf(c.dial)===0&&(!hit||c.dial.length>hit.dial.length))hit=c});
        if(hit&&!(hit.dial===sel.dial)){sel=hit}
        if(hit){tel.value=d.slice(hit.dial.length);setCountry(sel);return}
      }
      tel.value=format(sel,digits(v));sync();
    });
    setCountry(sel);
    phoneBox.resetCountry=function(){tel.value='';setCountry(byCode[def]||list[0])};
  }

  // Formulário: envia para o serviço em data-endpoint e só confirma quando o envio dá certo
  var form=$('leadForm'), ok=$('okMsg'), err=$('errMsg');
  if(form)form.addEventListener('submit',function(e){
    e.preventDefault();
    ok.classList.remove('show');err.classList.remove('show');
    if(!form.checkValidity()){form.reportValidity();return}
    var url=form.getAttribute('data-endpoint');
    if(!url){err.textContent=T.noEndpoint;err.classList.add('show');return}
    var submit=form.querySelector('button[type=submit]'), label=submit.textContent;
    submit.disabled=true;submit.textContent=T.sending;
    var data=new FormData(form);data.append('idioma',lang);
    fetch(url,{method:'POST',body:data,headers:{Accept:'application/json'}})
      .then(function(r){if(!r.ok)throw new Error(r.status);ok.classList.add('show');form.reset();if(phoneBox&&phoneBox.resetCountry)phoneBox.resetCountry()})
      .catch(function(){err.textContent=T.fail;err.classList.add('show')})
      .then(function(){submit.disabled=false;submit.textContent=label});
  });
})();
