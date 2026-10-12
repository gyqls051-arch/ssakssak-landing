# -*- coding: utf-8 -*-
# 놀이터 페이지 스펙 3 — 타로 카드 뽑기
# 공통 템플릿은 gen_pages.py. BODY 안의 마크업은 들여쓰기 자유.

TAROT_CSS = r"""
  .tr-modes{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px}
  .tr-mode{flex:1;min-width:160px;padding:16px 14px;border:1.5px solid var(--line);border-radius:14px;background:var(--bg);cursor:pointer;text-align:center;font-family:inherit;transition:border-color .2s,background .2s}
  .tr-mode b{display:block;font-size:15px;font-weight:900;color:var(--ink)}
  .tr-mode span{display:block;font-size:12px;color:var(--muted);font-weight:700;margin-top:4px}
  .tr-mode.on{border-color:var(--pink);background:var(--tint-p)}
  .tr-deck{display:grid;grid-template-columns:repeat(auto-fill,minmax(56px,1fr));gap:8px;margin-top:18px}
  .tr-card{aspect-ratio:2/3.1;border-radius:9px;background:linear-gradient(135deg,#332a5e 0%,#1d1840 100%);border:1.5px solid #4c4187;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:20px;color:#9b8ee8;transition:transform .2s,box-shadow .2s,opacity .2s;user-select:none}
  .tr-card:hover{transform:translateY(-6px) scale(1.05);box-shadow:0 10px 22px rgba(60,45,140,.35);border-color:#8f7ee8}
  .tr-card.picked{opacity:.18;pointer-events:none;transform:scale(.94)}
  .tr-hint{font-size:13px;font-weight:800;color:var(--muted);margin-top:14px;text-align:center}
  .tr-result{display:none;margin-top:24px}
  .tr-faces{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px}
  .tr-slot{background:var(--bg);border:1px solid var(--line);border-radius:18px;padding:18px;text-align:center;animation:trIn .5s ease both}
  @keyframes trIn{from{opacity:0;transform:translateY(14px) rotateY(40deg)}to{opacity:1;transform:none}}
  .tr-pos{font-size:11.5px;font-weight:800;color:var(--muted);letter-spacing:.06em}
  .tr-face{width:104px;aspect-ratio:2/3.1;margin:12px auto;border-radius:12px;background:linear-gradient(160deg,#4a3f92 0%,#2a2258 100%);border:1.5px solid #6f5fd0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;box-shadow:0 10px 26px rgba(60,45,140,.3)}
  .tr-face .em{font-size:38px;line-height:1}
  .tr-face .nm{font-size:12px;font-weight:900;color:#e6e1ff}
  .tr-face .en{font-size:9.5px;font-weight:700;color:#9b8ee8;letter-spacing:.08em}
  .tr-face.rev .em{transform:rotate(180deg)}
  .tr-rev-tag{display:inline-block;font-size:10.5px;font-weight:900;color:#fff;background:#b0455a;border-radius:99px;padding:2px 9px;margin-top:2px}
  .tr-mean{font-size:14px;font-weight:800;color:var(--ink);margin-top:8px;line-height:1.6}
  .tr-sub{font-size:12.5px;color:var(--muted);margin-top:5px;line-height:1.6}
  .tr-btns{display:flex;gap:10px;margin-top:20px;flex-wrap:wrap}
"""

TAROT_BODY = r"""
      <div class="tr-modes">
        <button class="tr-mode on" id="tr-m1"><b>🌙 오늘의 운세</b><span>카드 1장</span></button>
        <button class="tr-mode" id="tr-m3"><b>🔮 과거·현재·미래</b><span>카드 3장</span></button>
      </div>
      <div id="tr-pick">
        <div class="tr-deck" id="tr-deck"></div>
        <div class="tr-hint" id="tr-hint">끌리는 카드를 1장 골라보세요</div>
      </div>
      <div class="tr-result" id="tr-result">
        <div class="tr-faces" id="tr-faces"></div>
        <div class="tr-btns">
          <button class="btn btn-primary" id="tr-copy" style="padding:11px 20px;border-radius:10px;border:0;font-size:14px">결과 복사하기</button>
          <button class="btn btn-ghost" id="tr-again" style="padding:11px 20px;border-radius:10px;font-size:14px">다시 뽑기</button>
        </div>
      </div>
      <div class="status-line"><span class="dot" id="tr-dot"></span><span id="tr-status">뽑기 방식을 고르고 카드를 선택하세요</span></div>
"""

TAROT_SCRIPT = r"""
<script>
(function(){
  // [한국어 이름, 영어 이름, 이모지, 정방향 키워드, 역방향 키워드, 정방향 한줄, 역방향 한줄]
  var CARDS=[
    ['바보','The Fool','🚶','새 출발·모험','무모함·준비 부족','새로운 시작의 신호 — 일단 발부터 내딛어 보세요.','생각 없이 뛰어들면 위험 — 준비부터 챙기기.'],
    ['마법사','The Magician','🪄','재능·행동력','재능 낭비·속임수','이미 다 가지고 있어요 — 지금 움직이면 됨.','능력은 있는데 엉뚱한 데 쓰는 중? 방향 점검.'],
    ['여사제','The High Priestess','🌙','직관·비밀','혼란·표면 판단','겉보다 속 — 직감이 정답에 가까워요.','뭔가 숨겨진 게 있어요. 성급한 판단 금지.'],
    ['여제','The Empress','👸','풍요·애정','의존·과한 배려','사랑·풍요가 들어오는 카드 — 받아들이세요.','남 챙기느라 나를 못 챙기는 중일지도.'],
    ['황제','The Emperor','🤴','안정·리더십','고집·강압','주도권 잡고 밀면 자리 잡는 카드.','고집이 세지고 있진 않나요 — 유연하게.'],
    ['교황','The Hierophant','📿','가르침·전통','고정관념·형식','배우거나 조언 구하기 좋은 때 — 멘토 찾기.','틀에 갇히지 말 것 — 나만의 방식도 답.'],
    ['연인','The Lovers','💞','사랑·선택','불화·잘못된 선택','마음이 가는 쪽이 정답 — 관계에 진심을.','선택 앞에서 흔들리는 중 — 기준 정하기.'],
    ['전차','The Chariot','🏇','추진력·승리','통제 상실','멈추지 말고 그대로 — 승리가 가까워요.','페달만 밟고 핸들 놓침 — 방향 다시 확인.'],
    ['힘','Strength','🦁','용기·인내','자신감 부족','부드러운 힘이 진짜 힘 — 흔들려도 버텨요.','지금 약해 보여도 그건 착각 — 자신감 회복.'],
    ['은둔자','The Hermit','🏮','성찰·내면의 답','고립·왕고집','혼자만의 시간에서 답이 나와요 — 잠깐 멈춰보기.','너무 들어가 있나요 — 밖으로 나올 시간.'],
    ['운명의 수레바퀴','Wheel of Fortune','🎡','전환점·행운','정체·불운','흐름이 바뀌는 중 — 기회가 오면 잡아요.','내리막도 사이클의 일부 — 곧 다시 올라와요.'],
    ['정의','Justice','⚖️','공정·균형','불공정·편파','정당한 게 이기는 카드 — 원칙대로 가세요.','억울한 상황일 수도 — 증거·기록 챙기기.'],
    ['매달린 남자','The Hanged Man','🙃','희생·관점 전환','헛된 희생','뒤집어 보면 보이는 답 — 관점 바꾸기.','희생만 하고 결과 없음 — 그만 끊을 때.'],
    ['죽음','Death','💀','끝과 새 시작','변화 거부·집착','뭔가 끝나는 건 새 시작의 문 — 놓아주세요.','이미 끝난 걸 붙잡는 중 — 손 놓기.'],
    ['절제','Temperance','🏺','조화·절제','불균형·과함','적당히 섞으면 최고의 맛 — 밸런스가 답.','뭔가 과한 상태 — 하나 줄이면 딱 맞아요.'],
    ['악마','The Devil','😈','유혹·속박','해방·깨달음','끌리는 게 있으면 알아차리기 — 유혹 주의.','끊어야 할 걸 아는 카드 — 사슬 풀기 시작.'],
    ['탑','The Tower','🗼','급격한 변화','변화 회피','무너지는 것도 기회 — 새로 세울 수 있어요.','버티는 게 더 큰 피해 — 차라리 부수기.'],
    ['별','The Star','⭐','희망·치유','실망·불신','바라던 게 보이기 시작 — 희망 가지세요.','지금은 안 보여도 별은 있어요 — 조금만 더.'],
    ['달','The Moon','🌕','불안·환상','혼란 해소','안갯속 — 확실하지 않으면 서두르지 마세요.','혼란이 걷히는 중 — 진실이 보여요.'],
    ['태양','The Sun','☀️','성공·기쁨','일시적 침체','가장 밝은 카드 — 잘되는 시기, 즐기세요.','구름 낀 태양 — 금방 다시 밝아져요.'],
    ['심판','Judgement','🎺','부활·깨달음','후회·자기 의심','다시 일어설 시간 — 기회는 마지막이 아니에요.','과거에 얽매이지 말 것 — 앞으로 가기.'],
    ['세계','The World','🌍','완성·성취','미완성·지연','한 챕터 완성 — 잘 마무리하고 다음으로.','거의 다 왔는데 뭔가 부족 — 마지막 한 걸음.']
  ];
  var POS3=['지난 일','지금','다가올 일'];
  var mode=1, picked=[], order=[];
  var deck=document.getElementById('tr-deck'), hint=document.getElementById('tr-hint');
  var st=document.getElementById('tr-status'), dot=document.getElementById('tr-dot');

  function shuffle(){order=CARDS.map(function(_,i){return i;});
    for(var i=order.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=order[i];order[i]=order[j];order[j]=t;}}
  function renderDeck(){
    deck.innerHTML='';
    order.forEach(function(ci){
      var d=document.createElement('div');
      d.className='tr-card';d.textContent='☾';
      d.addEventListener('click',function(){pick(d,ci);});
      deck.appendChild(d);
    });
  }
  function setMode(n){
    mode=n;picked=[];
    document.getElementById('tr-m1').className='tr-mode'+(n===1?' on':'');
    document.getElementById('tr-m3').className='tr-mode'+(n===3?' on':'');
    document.getElementById('tr-result').style.display='none';
    document.getElementById('tr-pick').style.display='block';
    hint.textContent='끌리는 카드를 '+n+'장 골라보세요';
    st.textContent='뽑기 방식: '+(n===1?'오늘의 운세 (1장)':'과거·현재·미래 (3장)');
    dot.className='dot ready';
    shuffle();
    renderDeck();
  }
  function pick(el,ci){
    if(picked.length>=mode)return;
    picked.push({card:ci,rev:Math.random()<0.4});
    el.classList.add('picked');
    if(picked.length<mode){hint.textContent='좋아요, '+(mode-picked.length)+'장 더 골라주세요';}
    else{reveal();}
  }
  function reveal(){
    document.getElementById('tr-pick').style.display='none';
    var h='';
    picked.forEach(function(pk,i){
      var c=CARDS[pk.card];
      var pos=mode===1?'오늘의 카드':POS3[i];
      h+='<div class="tr-slot" style="animation-delay:'+(i*0.15)+'s">'
        +'<div class="tr-pos">'+pos+'</div>'
        +'<div class="tr-face'+(pk.rev?' rev':'')+'"><div class="em">'+c[2]+'</div><div class="nm">'+c[0]+'</div><div class="en">'+c[1]+'</div></div>'
        +(pk.rev?'<span class="tr-rev-tag">역방향</span>':'')
        +'<div class="tr-mean">'+(pk.rev?c[4]:c[3])+'</div>'
        +'<div class="tr-sub">'+(pk.rev?c[6]:c[5])+'</div></div>';
    });
    document.getElementById('tr-faces').innerHTML=h;
    document.getElementById('tr-result').style.display='block';
    var lines=picked.map(function(pk,i){var c=CARDS[pk.card];var pos=mode===1?'오늘':POS3[i];return pos+': '+c[2]+' '+c[0]+(pk.rev?'(역방향)':'')+' — '+(pk.rev?c[4]:c[3]);});
    window._trTxt='싹싹김치 타로 결과:\n'+lines.join('\n')+'\n나도 뽑기 → https://www.ssakkimchi.com/tarot.html';
    st.textContent='카드가 펼쳐졌어요 — 마음에 새겨두세요';
    dot.className='dot ready';
  }
  document.getElementById('tr-m1').addEventListener('click',function(){setMode(1);});
  document.getElementById('tr-m3').addEventListener('click',function(){setMode(3);});
  document.getElementById('tr-again').addEventListener('click',function(){setMode(mode);});
  document.getElementById('tr-copy').addEventListener('click',function(){
    var b=this;
    (navigator.clipboard?navigator.clipboard.writeText(window._trTxt):Promise.reject()).then(function(){b.textContent='복사됨!';}).catch(function(){prompt('복사하세요',window._trTxt);});
  });
  setMode(1);
})();
</script>
"""

PAGES = [
  dict(
    slug='tarot', cat='play', name='타로 카드',
    title='오늘의 타로 무료 — 카드 뽑기로 보는 운세 (싹싹김치)',
    desc='끌리는 카드를 고르면 오늘의 운세가 나와요. 메이저 아르카나 22장, 정방향·역방향 해석, 1장 오늘의 운세 / 3장 과거·현재·미래 — 설치·가입 없이 바로 뽑는 무료 타로.',
    og_title='타로 카드 뽑기 — 오늘의 운세·과거 현재 미래',
    og_desc='끌리는 카드를 고르세요. 대답은 카드가 알아요.',
    h1='타로 카드 뽑기', pen='끌리는 카드를 고르세요. 대답은 카드가 알아요.',
    pdesc='<b>오늘의 운세 1장</b>이나 <b>과거·현재·미래 3장</b> 뽑기. 22장의 메이저 아르카나가 뒤섞여 있어요 — 끌리는 카드가 곧 오늘의 답입니다.',
    body=TAROT_BODY, css=TAROT_CSS, script=TAROT_SCRIPT,
    notice=[
      '타로 해석은 전통 키워드를 쉽게 푼 <b>재미용</b>입니다 — 중요한 결정은 본인의 판단으로.',
      '뽑은 카드·선택 기록은 저장·전송되지 않습니다.',
      '카드 섞기와 역방향 여부는 매번 랜덤이라, 다시 뽑으면 다른 카드가 나올 수 있어요.'],
  ),
]
