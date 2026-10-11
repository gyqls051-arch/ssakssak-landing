# -*- coding: utf-8 -*-
# 놀이터 페이지 스펙 2/2 (후반) — 혈액형 성격 + 이상형/음식 월드컵

BLOOD_CSS = r"""
  .bl-types{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px}
  @media (max-width:560px){.bl-types{grid-template-columns:repeat(2,1fr)}}
  .bl-type{padding:22px 10px;border:1px solid var(--line);border-radius:16px;background:var(--bg);cursor:pointer;text-align:center;transition:border-color .15s,transform .15s;font-family:inherit}
  .bl-type:hover{border-color:var(--pink);transform:translateY(-2px)}
  .bl-type .bt{font-size:30px;font-weight:900;color:var(--pink)}
  .bl-type .bn{font-size:12.5px;font-weight:800;color:var(--muted);margin-top:4px}
  .bl-card{background:var(--bg);border:1px solid var(--line);border-radius:16px;padding:18px;margin-bottom:12px}
  .bl-card h3{margin:0 0 8px;font-size:14px;font-weight:900}
  .bl-card p{margin:0;font-size:14px;line-height:1.75}
  .bl-card .tag{display:inline-block;font-size:11.5px;font-weight:800;padding:4px 10px;border-radius:99px;margin:2px 4px 2px 0}
  .bl-matrix{width:100%;border-collapse:collapse;margin-top:8px}
  .bl-matrix th,.bl-matrix td{padding:10px 8px;text-align:center;font-size:13px;font-weight:700;border-bottom:1px solid var(--line)}
  .bl-matrix th{color:var(--muted);font-size:12px;font-weight:800}
  .bl-matrix td:first-child{font-weight:900;color:var(--pink)}
  .bl-score{font-weight:900}
"""

BLOOD_BODY = r"""
      <p style="font-size:14px;color:var(--muted);margin:0 0 18px;line-height:1.7">혈액형을 고르면 <b style="color:var(--ink)">성향 분석과 궁합</b>을 보여드립니다. 과학적 근거는 없지만 재밌잖아요 — 한국식 혈액형 성격론 그대로.</p>
      <div class="bl-types" id="bl-types"></div>
      <div id="bl-result" style="display:none"></div>
      <div class="bl-card" id="bl-mx-wrap" style="margin-top:8px">
        <h3>혈액형 궁합표 — 나(왼쪽) × 상대(위쪽)</h3>
        <table class="bl-matrix" id="bl-mx"></table>
      </div>
"""

BLOOD_SCRIPT = r"""
<script>
(function(){
  var DATA={
    'A':{nick:'완벽주의 신중파',line:'꼼꼼하고 책임감 강한 완벽주의자. 배려 깊은데 속마음은 잘 안 보여줘요.',
      good:'꼼꼼함 · 책임감 · 성실 · 배려',bad:'걱정 과다 · 완벽 강박 · 스트레스 축적',
      love:'좋아하면 상대를 세심하게 챙기는 헌신형. 다가가는 속도는 느리지만 한번 빠지면 깊어요.',
      best:'O형 — 큰 그릇의 O형이 A형의 예민함을 받아줍니다',worst:'B형 — 자유분방한 B형이 A형에겐 답답하게 느껴질 수 있어요'},
    'B':{nick:'자유로운 마이웨이',line:'호기심 많고 솔직한 개성파. 좋아하는 것엔 불타오르고, 싫은 건 눈길도 안 줘요.',
      good:'낙천적 · 솔직 · 독창성 · 집중력',bad:'마이웨이 · 뒤끝 없지만 앞끝도 없음 · 규칙 무시',
      love:'좋아하면 확실히 표현하는 직진형. 밀당 없이 담백해서 상대가 헷갈릴 일이 없어요.',
      best:'AB형 — 독특한 AB형과 개성파 B형이 서로 존중합니다',worst:'A형 — 신중한 A형 눈엔 B형이 너무 제멋대로 보일 수 있어요'},
    'O':{nick:'쿨한 리더십',line:'털털하고 스케일 큰 리더형. 의리 있고 결단 빠른데, 의외로 서운한 건 오래 기억해요.',
      good:'대범함 · 리더십 · 결단력 · 의리',bad:'자존심 강함 · 성급함 · 서운함 축적',
      love:'좋아하면 올인하는 불도저형. 스킨십도 표현도 스케일이 커요.',
      best:'A형 — 꼼꼼한 A형이 O형의 빈틈을 채워주는 국민 조합',worst:'AB형 — 둘 다 개성이 강해 방향이 어긋나기 쉬워요'},
    'AB':{nick:'재능 많은 천재형',line:'이성과 감성이 공존하는 독특한 캐릭터. 재능이 많은데 기분파라 일관성이 관건이에요.',
      good:'재능 다방면 · 객관적 · 독창적',bad:'기분파 · 관계 거리두기 · 피곤함 호소',
      love:'적당한 거리를 두면서도 깊게 사랑하는 신비형. 알기 어려운 매력이 상대를 끌어당겨요.',
      best:'B형 — 서로의 개성을 간섭하지 않는 조합',worst:'O형 — 직진 O형에게 AB형의 거리두기는 차갑게 느껴져요'}};
  var MX={'A':{'A':70,'B':40,'O':95,'AB':65},'B':{'A':40,'B':75,'O':80,'AB':90},'O':{'A':95,'B':80,'O':80,'AB':60},'AB':{'A':65,'B':90,'O':60,'AB':85}};
  var order=['A','B','O','AB'];
  var bt=document.getElementById('bl-types');
  order.forEach(function(t){
    var b=document.createElement('button');
    b.className='bl-type';
    b.innerHTML='<div class="bt">'+t+'</div><div class="bn">'+DATA[t].nick+'</div>';
    b.onclick=function(){show(t);};
    bt.appendChild(b);
  });
  var mx='<tr><th></th>'+order.map(function(t){return '<th>'+t+'형</th>'}).join('')+'</tr>';
  order.forEach(function(a){
    mx+='<tr><td>'+a+'형</td>'+order.map(function(b){
      var v=MX[a][b],c=v>=85?'var(--green-ink)':v>=70?'var(--yellow-ink)':'var(--muted)';
      return '<td><span class="bl-score" style="color:'+c+'">'+v+'</span></td>';
    }).join('')+'</tr>';
  });
  document.getElementById('bl-mx').innerHTML=mx;
  function show(t){
    var d=DATA[t];
    document.getElementById('bl-result').style.display='block';
    document.getElementById('bl-result').innerHTML=
      '<div class="bl-card" style="border-color:var(--pink);background:var(--chip-pk)"><h3>'+t+'형 — '+d.nick+'</h3><p style="font-size:15px">'+d.line+'</p></div>'
      +'<div class="bl-card"><h3>장점 · 단점</h3><p><span class="tag" style="background:var(--chip-g);color:var(--green-ink)">장점 '+d.good+'</span></p><p style="margin-top:6px"><span class="tag" style="background:var(--chip-o);color:var(--accent)">단점 '+d.bad+'</span></p></div>'
      +'<div class="bl-card"><h3>연애 스타일</h3><p>'+d.love+'</p></div>'
      +'<div class="bl-card"><h3>궁합</h3><p><b style="color:var(--green-ink)">최고:</b> '+d.best+'</p><p style="margin-top:6px"><b style="color:var(--accent)">아쉬움:</b> '+d.worst+'</p></div>';
    document.getElementById('bl-result').scrollIntoView({behavior:'smooth',block:'nearest'});
  }
})();
</script>
"""

WC_CSS = r"""
  .wc-sets{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
  @media (max-width:560px){.wc-sets{grid-template-columns:1fr}}
  .wc-set{padding:18px;border:1px solid var(--line);border-radius:14px;background:var(--bg);cursor:pointer;text-align:left;font-family:inherit;transition:border-color .15s}
  .wc-set:hover{border-color:var(--pink)}
  .wc-set b{font-size:15px;font-weight:900;display:block}
  .wc-set span{font-size:12.5px;color:var(--muted);font-weight:600}
  .wc-round{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px}
  .wc-round b{font-size:15px;font-weight:900}
  .wc-round span{font-size:12.5px;font-weight:800;color:var(--muted)}
  .wc-vs{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;align-items:stretch}
  .wc-card{padding:34px 12px;border:1px solid var(--line);border-radius:18px;background:var(--bg);cursor:pointer;text-align:center;font-family:inherit;transition:transform .15s,border-color .15s,background .15s}
  .wc-card:hover{border-color:var(--pink);transform:translateY(-3px);background:var(--chip-pk)}
  .wc-card .em{font-size:52px;line-height:1;display:block}
  .wc-card .nm{font-size:16px;font-weight:900;display:block;margin-top:12px}
  .wc-vsmark{align-self:center;font-size:14px;font-weight:900;color:var(--faint)}
  .wc-result{text-align:center;padding:14px 0}
  .wc-crown{font-size:60px}
  .wc-winner{font-size:26px;font-weight:900;margin:10px 0 4px}
  .wc-sub{font-size:13.5px;color:var(--muted);font-weight:700}
  .wc-finalist{margin-top:16px;display:grid;gap:6px;text-align:left}
"""

WC_BODY = r"""
      <div id="wc-home">
        <p style="font-size:14px;color:var(--muted);margin:0 0 18px;line-height:1.7">하나만 고르세요. <b style="color:var(--ink)">16강부터 결승까지</b> 토너먼트로 최애를 뽑아봅니다.</p>
        <div class="wc-sets" id="wc-sets"></div>
      </div>
      <div id="wc-game" style="display:none">
        <div class="wc-round"><b id="wc-round"></b><span id="wc-count"></span></div>
        <div class="wc-vs">
          <button class="wc-card" id="wc-l"><span class="em"></span><span class="nm"></span></button>
          <span class="wc-vsmark">VS</span>
          <button class="wc-card" id="wc-r"><span class="em"></span><span class="nm"></span></button>
        </div>
      </div>
      <div id="wc-result" style="display:none" class="wc-result"></div>
"""

WC_SCRIPT = r"""
<script>
(function(){
  var SETS={
    '라면 월드컵':{sub:'신라면·짜파게티·불닭… 16강',items:[['🍜','신라면'],['🍜','진라면'],['🍜','짜파게티'],['🔥','불닭볶음면'],['🍜','너구리'],['🍜','안성탕면'],['🧀','치즈볶음면'],['🍜','삼양라면'],['🍜','육개장 사발면'],['🦐','새우탕면'],['🍜','참깨라면'],['🍜','미역국라면'],['🌶','열라면'],['🍜','짜왕'],['🍜','틈새라면'],['🍜','비빔면']]},
    '치킨 월드컵':{sub:'후라이드·양념·뿌링클… 16강',items:[['🍗','후라이드'],['🍗','양념치킨'],['🧀','뿌링클'],['🍗','간장치킨'],['🌶','슈프림 양념'],['🍯','허니콤보'],['🍗','마늘치킨'],['🧄','갈릭치킨'],['🌶','핫양념'],['🍗','크리스피'],['🧈','버터구이'],['🍗','파닭'],['🍗','고추바사삭'],['🍗','데리야끼'],['🍗','카레치킨'],['🍗','로제치킨']]},
    '디저트 월드컵':{sub:'빵·케이크·떡… 16강',items:[['🍰','딸기케이크'],['🧁','티라미수'],['🍮','푸딩'],['🥐','크로아상'],['🍩','도넛'],['🧇','와플'],['🍪','쿠키'],['🥞','팬케이크'],['🍡','인절미'],['🍨','아이스크림'],['🍫','브라우니'],['🧁','마카롱'],['🍞','소금빵'],['🥧','에그타르트'],['🍭','약과'],['🍧','빙수']]},
    '여행지 월드컵':{sub:'국내·해외 명소 16강',items:[['🌊','제주도'],['🏙','서울'],['🗼','도쿄'],['⛩','오사카'],['🏝','발리'],['🗽','뉴욕'],['🗼','파리'],['🏛','로마'],['🌉','샌프란시스코'],['🏖','다낭'],['🌃','홍콩'],['🎡','방콕'],['🏰','런던'],['🌊','부산'],['⛰','스위스'],['🏜','두바이']]}
  };
  var st={queue:[],winners:[],semi:null,final2:null,setName:''};
  var home=document.getElementById('wc-home'),game=document.getElementById('wc-game'),res=document.getElementById('wc-result');
  var setsEl=document.getElementById('wc-sets');
  Object.keys(SETS).forEach(function(name){
    var b=document.createElement('button');
    b.className='wc-set';
    b.innerHTML='<b>'+name+'</b><span>'+SETS[name].sub+'</span>';
    b.onclick=function(){start(name);};
    setsEl.appendChild(b);
  });
  function shuf(a){a=a.slice();for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;}
  function start(name){
    st.queue=shuf(SETS[name].items);st.stageSize=st.queue.length;st.winners=[];st.semi=null;st.final2=null;st.setName=name;
    home.style.display='none';res.style.display='none';game.style.display='block';
    nextMatch();
  }
  function nextMatch(){
    if(st.queue.length===0){
      if(st.winners.length===1){finish(st.winners[0]);return;}
      if(st.winners.length===4)st.semi=st.winners.slice();
      if(st.winners.length===2)st.final2=st.winners.slice();
      st.queue=st.winners.slice();st.winners=[];
      st.stageSize=st.queue.length;
    }
    var stage=st.stageSize;
    var names={16:'16강',8:'8강',4:'준결승',2:'결승'};
    document.getElementById('wc-round').textContent=st.setName+' · '+(names[stage]||stage+'강');
    document.getElementById('wc-count').textContent=Math.ceil(st.queue.length/2)+'경기 남음';
    setCard('wc-l',st.queue[0]);setCard('wc-r',st.queue[1]);
  }
  function setCard(id,it){
    var el=document.getElementById(id);
    el.querySelector('.em').textContent=it[0];
    el.querySelector('.nm').textContent=it[1];
  }
  function pick(idx){
    var w=st.queue.splice(0,2)[idx];
    st.winners.push(w);
    nextMatch();
  }
  document.getElementById('wc-l').onclick=function(){pick(0);};
  document.getElementById('wc-r').onclick=function(){pick(1);};
  function finish(w){
    game.style.display='none';res.style.display='block';
    var rows='';
    if(st.final2){
      var ru=st.final2.filter(function(x){return x!==w})[0];
      if(ru)rows+='<div class="mb-card" style="display:flex;gap:10px;align-items:center"><span style="font-size:11.5px;font-weight:900;color:var(--muted)">준우승</span><span style="font-size:20px">'+ru[0]+'</span><b style="font-size:14px">'+ru[1]+'</b></div>';
    }
    if(st.semi){
      st.semi.filter(function(x){return st.final2.indexOf(x)<0}).forEach(function(x){
        rows+='<div class="mb-card" style="display:flex;gap:10px;align-items:center"><span style="font-size:11.5px;font-weight:900;color:var(--muted)">4강</span><span style="font-size:20px">'+x[0]+'</span><b style="font-size:14px">'+x[1]+'</b></div>';
      });
    }
    res.innerHTML='<div class="wc-crown">'+w[0]+'</div>'
      +'<div class="wc-winner">'+w[1]+'</div>'
      +'<div class="wc-sub">'+st.setName+' 우승!</div>'
      +(rows?'<div class="wc-finalist">'+rows+'</div>':'')
      +'<div style="display:flex;gap:10px;justify-content:center;margin-top:20px;flex-wrap:wrap">'
      +'<button class="btn btn-primary" id="wc-again" style="padding:11px 22px;border-radius:10px;border:0;font-size:14px">같은 주제로 다시</button>'
      +'<button class="btn btn-ghost" id="wc-home-btn" style="padding:11px 22px;border-radius:10px;font-size:14px">다른 주제</button></div>';
    document.getElementById('wc-again').onclick=function(){start(st.setName);};
    document.getElementById('wc-home-btn').onclick=function(){res.style.display='none';home.style.display='block';};
  }
})();
</script>
"""

PAGES = [
  dict(
    slug='blood', cat='play', name='혈액형 성격',
    title='혈액형 성격 테스트 무료 — A·B·O·AB형 성향과 궁합 (싹싹김치)',
    desc='혈액형별 성격 분석과 궁합표. A·B·O·AB형 장점·단점·연애 스타일부터 혈액형 궁합 매트릭스까지 — 가입 없이 바로 보는 무료 혈액형 테스트.',
    og_title='혈액형 성격 테스트 — A·B·O·AB 성향·궁합',
    og_desc='내 혈액형 성향과 최고의 궁합 혈액형까지 한 번에.',
    h1='혈액형 성격 테스트', pen='과학은 아니지만, 재밌잖아요.',
    pdesc='A·B·O·AB를 고르면 <b>성향 분석·장단점·연애 스타일·궁합</b>을 보여드립니다. 4×4 혈액형 궁합표도 같이.',
    body=BLOOD_BODY, css=BLOOD_CSS, script=BLOOD_SCRIPT,
    notice=[
      '혈액형 성격론은 <b>과학적 근거가 없는</b> 문화적 재미입니다 — 사람을 혈액형으로 판단하진 마세요.',
      '선택한 혈액형은 저장·전송되지 않습니다.',
      '궁합 점수는 한국식 혈액형 성격론의 통념을 점수화한 것으로, 실제 관계와 무관합니다.'],
  ),
  dict(
    slug='worldcup', cat='play', name='이상형 월드컵',
    title='이상형 월드컵 만들기 무료 — 음식·여행지 토너먼트 (싹싹김치)',
    desc='16강 토너먼트로 최애를 뽑는 이상형 월드컵. 라면·치킨·디저트·여행지 카드셋 중 골라서 하나씩 선택하면 우승이 정해집니다 — 설치 없이 바로 플레이.',
    og_title='이상형 월드컵 — 16강 토너먼트로 최애 뽑기',
    og_desc='라면·치킨·디저트·여행지. 하나만 고를 수 있다면?',
    h1='이상형 월드컵', pen='하나만 고르세요. 양보 없이.',
    pdesc='주제를 골라 <b>16강부터 결승까지</b> 이판사판 토너먼트. 라면·치킨·디저트·여행지 — 당신의 최애는 뭔가요?',
    body=WC_BODY, css=WC_CSS, script=WC_SCRIPT,
    notice=[
      '모든 대진은 매번 랜덤으로 섞입니다 — 같은 주제라도 결과가 달라질 수 있어요.',
      '선택 기록은 저장·전송되지 않습니다.',
      '연예인·실제 인물 카드는 초상권 문제로 넣지 않습니다 — 음식·여행지 등 사물 테마만 제공해요.'],
  ),
]
