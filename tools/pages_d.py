# -*- coding: utf-8 -*-
# 놀이터 페이지 스펙 2/2 — 사주(무료 사주 보기) + 성격유형 테스트(MBTI형)
# 공통 템플릿은 gen_pages.py. BODY 안의 마크업은 들여쓰기 자유.

SAJU_CSS = r"""
  .sj-form{display:flex;gap:12px;flex-wrap:wrap;align-items:flex-end}
  .sj-field{display:flex;flex-direction:column;gap:6px}
  .sj-field label{font-size:12.5px;font-weight:800;color:var(--muted)}
  .sj-field input,.sj-field select{padding:12px 14px;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--ink);font-size:14px;font-family:inherit;font-weight:600}
  .sj-cal{display:flex;gap:8px}
  .sj-cal label{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:700;cursor:pointer;padding:10px 14px;border:1px solid var(--line);border-radius:10px;background:var(--bg)}
  .sj-cal input{accent-color:var(--accent)}
  .sj-pillars{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:22px}
  .sj-pillar{background:var(--bg);border:1px solid var(--line);border-radius:14px;overflow:hidden;text-align:center}
  .sj-pillar .lbl{font-size:11px;font-weight:800;color:var(--muted);padding:8px 0 4px;letter-spacing:.04em}
  .sj-pillar .gan{font-size:34px;font-weight:900;line-height:1.1;padding:6px 0 2px}
  .sj-pillar .kor{font-size:12px;color:var(--muted);font-weight:700;padding-bottom:10px}
  .sj-pillar .zhi{border-top:1px dashed var(--line);font-size:26px;font-weight:900;padding:8px 0 2px}
  .sj-pillar.day{background:var(--tint-o);border-color:var(--accent)}
  .sj-pillar.day .lbl{color:var(--accent)}
  .sj-wx{display:flex;flex-direction:column;gap:8px;margin-top:18px}
  .sj-wx-row{display:grid;grid-template-columns:34px 1fr 44px;align-items:center;gap:10px;font-size:13px;font-weight:800}
  .sj-wx-bar{height:10px;border-radius:99px;background:var(--line);overflow:hidden}
  .sj-wx-bar i{display:block;height:100%;border-radius:99px}
  .sj-reading{margin-top:20px;display:grid;gap:12px}
  .sj-block{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:16px 18px}
  .sj-block b.t{display:block;font-size:13px;font-weight:900;margin-bottom:6px}
  .sj-block p{font-size:14px;line-height:1.75;color:var(--ink);margin:0}
  .sj-badge{display:inline-block;font-size:11.5px;font-weight:800;padding:4px 10px;border-radius:99px;background:var(--tint-y);color:var(--yellow-ink);margin-left:8px;vertical-align:middle}
"""

SAJU_BODY = r"""
      <p style="font-size:14px;color:var(--muted);margin:0 0 18px;line-height:1.7">생년월일(과 태어난 시간)을 넣으면 <b style="color:var(--ink)">사주팔자</b>를 바로 뽑아드립니다. 양력·음력 둘 다 되고, 계산은 전부 이 브라우저 안에서 끝나요.</p>
      <div class="sj-form">
        <div class="sj-cal">
          <label><input type="radio" name="cal" value="solar" checked>양력</label>
          <label><input type="radio" name="cal" value="lunar">음력</label>
        </div>
        <div class="sj-field" style="flex:1;min-width:170px">
          <label for="sj-date">생년월일</label>
          <input type="date" id="sj-date" min="1900-01-01" max="2099-12-31">
        </div>
        <div class="sj-field">
          <label for="sj-hour">태어난 시간</label>
          <select id="sj-hour">
            <option value="">시간 모름</option>
            <option value="0">자시 (23~01시)</option><option value="2">축시 (01~03시)</option>
            <option value="4">인시 (03~05시)</option><option value="6">묘시 (05~07시)</option>
            <option value="8">진시 (07~09시)</option><option value="10">사시 (09~11시)</option>
            <option value="12" selected>오시 (11~13시)</option><option value="14">미시 (13~15시)</option>
            <option value="16">신시 (15~17시)</option><option value="18">유시 (17~19시)</option>
            <option value="20">술시 (19~21시)</option><option value="22">해시 (21~23시)</option>
          </select>
        </div>
        <button class="btn btn-primary" id="sj-go" style="padding:12px 22px;border-radius:10px;border:0;font-size:14px">사주 보기</button>
      </div>

      <div id="sj-out" style="display:none">
        <div class="sj-pillars" id="sj-pillars"></div>
        <div class="sj-wx" id="sj-wx"></div>
        <div class="sj-reading" id="sj-reading"></div>
      </div>
      <div class="status-line"><span class="dot" id="sj-dot"></span><span id="sj-status">생년월일을 고르고 사주 보기를 누르세요</span></div>
"""

SAJU_SCRIPT = r"""
<script src="js/vendor/lunar.js"></script>
<script>
(function(){
  var GAN='甲乙丙丁戊己庚辛壬癸', ZHI='子丑寅卯辰巳午未申酉戌亥';
  var GAN_K=['갑','을','병','정','무','기','경','신','임','계'];
  var ZHI_K=['자','축','인','묘','진','사','오','미','신','유','술','해'];
  var GAN_WX=['목','목','화','화','토','토','금','금','수','수'];
  var ZHI_WX=['수','토','목','목','토','화','화','토','금','금','토','수'];
  var WX_COLOR={'목':'#2f8f4e','화':'#e85d2c','토':'#c98f12','금':'#8a93a6','수':'#3f7cc4'};
  var DAYGAN_DESC={
    '甲':'큰 나무처럼 곧게 뻗는 힘. 정직하고 원칙적이며, 한번 뿌리내린 목표는 끝까지 밀고 나가는 추진력이 있습니다. 고집이 세다는 소리를 듣기도 하지만 그게 곧 저력이에요.',
    '乙':'덩굴·풀처럼 유연하고 끈질긴 생명력. 겉은 부드러운데 속은 단단해서, 환경에 적응하면서도 결국 자기 방향대로 자랍니다. 사람 사이에서 살아남는 지혜가 탁월해요.',
    '丙':'태양처럼 환하고 넓은 기운. 숨기는 게 없이 시원시원하고, 주위를 밝히는 존재감이 있습니다. 감정 표현이 솔직해서 미워할래야 미워할 수 없는 타입이에요.',
    '丁':'촛불·달빛처럼 은은하지만 꺼지지 않는 불. 섬세하고 배려 깊으며, 보이지 않는 곳에서 사람을 챙기는 따뜻함이 있습니다. 집중하면 끝까지 파고드는 집요함도 강해요.',
    '戊':'큰 산처럼 묵직하고 든든한 존재감. 믿음직하고 포용력이 커서 주변 사람들이 기대는 타입. 변화보다 안정을 좋아하고, 한번 결심하면 좀처럼 흔들리지 않아요.',
    '己':'논밭의 흙처럼 만물을 품는 기운. 실용적이고 꼼꼼하며, 티 안 내고 묵묵히 실속을 챙기는 재주가 있습니다. 겉으론 온순해 보여도 속으론 계산이 빠른 편이에요.',
    '庚':'쇳덩이·도끼처럼 강하고 결단력 있는 기질. 의리와 정의감이 뚜렷하고, 격식보다 실제를 중시합니다. 무뚝뚝해 보여도 속정은 깊고, 밀어붙이는 힘이 제일 세요.',
    '辛':'보석·침처럼 예리하고 완성도 높은 기질. 심미안과 분석력이 뛰어나고, 작은 결함도 놓치지 않습니다. 자존심이 강하고 예민하지만, 그 예민함이 실력을 만들어요.',
    '壬':'큰 바다·강처럼 넓고 깊은 기운. 지혜롭고 포용력이 커서 어떤 상황에도 흘러가듯 적응합니다. 생각이 깊고 스케일이 큰데, 가끔은 너무 깊게 생각해서 지치기도 해요.',
    '癸':'이슬·안개처럼 조용히 스며드는 기운. 감수성이 풍부하고 직관이 날카로우며, 겉으로 조용해도 내면의 세계가 매우 큽니다. 인내심 있게 기다리다 기회를 잡는 타입이에요.'};
  var WX_DESC={
    '목':'계획·성장·인내 — 새로운 걸 싹틔우는 추진력',
    '화':'표현·열정·명예 — 드러내고 빛내는 에너지',
    '토':'안정·중재·신용 — 중심을 잡고 품어주는 힘',
    '금':'결단·의리·정리 — 자르고 정하는 결정력',
    '수':'지혜·유연·저장 — 흐르고 스며드는 적응력'};
  var WX_SANG={'목':'화','화':'토','토':'금','금':'수','수':'목'};
  var WX_GEUK={'목':'토','토':'수','수':'화','화':'금','금':'목'};

  function ganWx(g){return GAN_WX[GAN.indexOf(g)];}
  function zhiWx(z){return ZHI_WX[ZHI.indexOf(z)];}

  document.getElementById('sj-go').addEventListener('click',function(){
    var st=document.getElementById('sj-status'), dot=document.getElementById('sj-dot');
    var dv=document.getElementById('sj-date').value;
    if(!dv){st.textContent='생년월일을 먼저 골라주세요';dot.className='dot warn';return;}
    var p=dv.split('-'),y=+p[0],m=+p[1],d=+p[2];
    var hv=document.getElementById('sj-hour').value;
    var isLunar=document.querySelector('input[name=cal]:checked').value==='lunar';
    var lunar;
    try{
      if(isLunar){ lunar = hv===''?Lunar.fromYmd(y,m,d):Lunar.fromYmdHms(y,m,d,+hv,0,0); }
      else{ lunar = hv===''?Solar.fromYmd(y,m,d).getLunar():Solar.fromYmdHms(y,m,d,+hv,0,0).getLunar(); }
    }catch(e){ st.textContent='이 날짜는 계산할 수 없어요 — 1900~2099년 사이로 입력해주세요'; dot.className='dot warn'; return; }
    var ec=lunar.getEightChar();
    var pillars=[{lbl:'연주(년주)',gz:ec.getYear()},{lbl:'월주',gz:ec.getMonth()},{lbl:'일주',gz:ec.getDay(),day:true}];
    if(hv!=='')pillars.push({lbl:'시주',gz:ec.getTime()});
    var html='';
    pillars.forEach(function(pl){
      var g=pl.gz.charAt(0),z=pl.gz.charAt(1);
      html+='<div class="sj-pillar'+(pl.day?' day':'')+'"><div class="lbl">'+pl.lbl+'</div>'
        +'<div class="gan" style="color:'+WX_COLOR[ganWx(g)]+'">'+g+'</div><div class="kor">'+GAN_K[GAN.indexOf(g)]+' · '+ganWx(g)+'</div>'
        +'<div class="zhi" style="color:'+WX_COLOR[zhiWx(z)]+'">'+z+'</div><div class="kor">'+ZHI_K[ZHI.indexOf(z)]+' · '+zhiWx(z)+'</div></div>';
    });
    document.getElementById('sj-pillars').innerHTML=html;

    var cnt={'목':0,'화':0,'토':0,'금':0,'수':0},tot=0;
    pillars.forEach(function(pl){var g=pl.gz.charAt(0),z=pl.gz.charAt(1);cnt[ganWx(g)]++;cnt[zhiWx(z)]++;tot+=2;});
    var wxHtml='',mx=0,mn=tot;
    Object.keys(cnt).forEach(function(k){if(cnt[k]>mx)mx=cnt[k];if(cnt[k]<mn)mn=cnt[k];});
    var topEls=[],missEls=[];
    Object.keys(cnt).forEach(function(k){if(cnt[k]===mx&&mx>0)topEls.push(k);if(cnt[k]===0)missEls.push(k);});
    Object.keys(cnt).forEach(function(k){
      wxHtml+='<div class="sj-wx-row"><span style="color:'+WX_COLOR[k]+'">'+k+'</span><div class="sj-wx-bar"><i style="width:'+Math.round(cnt[k]/tot*100)+'%;background:'+WX_COLOR[k]+'"></i></div><span>'+cnt[k]+'/'+tot+'</span></div>';
    });
    document.getElementById('sj-wx').innerHTML=wxHtml;

    var dayGan=ec.getDayGan?ec.getDayGan():ec.getDay().charAt(0);
    var dayWx=ganWx(dayGan);
    var y=new Date().getFullYear();
    var seun=Solar.fromYmd(y,6,1).getLunar().getYearInGanZhi();
    var seunWx=ganWx(seun.charAt(0));
    var rel,relTxt;
    if(WX_SANG[dayWx]===seunWx){rel='내가 생하는 해';relTxt='내 기운이 밖으로 새는 해 — 무리한 확장보다 실력을 다지는 게 이득이에요.';}
    else if(WX_SANG[seunWx]===dayWx){rel='나를 생해주는 해';relTxt='어디선가 도움이 들어오는 해 — 배우고, 사람을 만나고, 제안을 받아들이기 좋아요.';}
    else if(WX_GEUK[dayWx]===seunWx){rel='내가 극하는 해';relTxt='주도권을 쥐는 해 — 재물·성과를 내기 좋지만, 욕심이 과하면 빈틈이 생겨요.';}
    else if(WX_GEUK[seunWx]===dayWx){rel='나를 극하는 해';relTxt='압박이 커지는 해 — 무리한 승부보다 몸과 멘탈 관리가 우선이에요. 지키는 해로 쓰세요.';}
    else{rel='같은 기운의 해';relTxt='나와 같은 성질의 해 — 내 방식대로 밀어붙이기 좋지만, 고집은 줄이는 게 좋아요.';}

    var read='';
    read+='<div class="sj-block"><b class="t">일간 '+dayGan+'('+dayWx+') — 당신의 바탕<span class="sj-badge">'+dayWx+' 기운</span></b><p>'+DAYGAN_DESC[dayGan]+'</p></div>';
    var wxTxt='오행 중 <b>'+topEls.join('·')+'</b> 기운이 가장 많아요 ('+WX_DESC[topEls[0]]+'). ';
    if(missEls.length)wxTxt+='<b>'+missEls.join('·')+'</b> 기운이 없어서, '+missEls.map(function(k){return WX_DESC[k].split(' — ')[0]}).join('·')+' 쪽은 의식적으로 채우면 좋아요.';
    else wxTxt+='없는 오행 없이 골고루 갖춰진 균형형 사주예요.';
    read+='<div class="sj-block"><b class="t">오행 분포 해석</b><p>'+wxTxt+'</p></div>';
    read+='<div class="sj-block"><b class="t">'+y+'년 '+seun+'년 운세<span class="sj-badge">'+rel+'</span></b><p>'+relTxt+'</p></div>';
    document.getElementById('sj-reading').innerHTML=read;
    document.getElementById('sj-out').style.display='block';
    st.textContent=(isLunar?'음력':'양력')+' '+dv.replace(/-/g,'.')+(hv===''?' · 시간 모름':' · '+document.querySelector('#sj-hour option:checked').textContent.split(' ')[0]);
    dot.className='dot ready';
  });
  document.getElementById('sj-date').value='1995-06-15';
})();
</script>
"""

MBTI_CSS = r"""
  .mb-progress{height:8px;border-radius:99px;background:var(--line);overflow:hidden;margin-bottom:22px}
  .mb-progress i{display:block;height:100%;background:linear-gradient(90deg,var(--pink),var(--purple));border-radius:99px;transition:width .25s}
  .mb-q{font-size:19px;font-weight:900;line-height:1.5;margin-bottom:20px;min-height:58px}
  .mb-ans{display:grid;gap:10px}
  .mb-ans button{text-align:left;padding:16px 18px;border:1px solid var(--line);border-radius:14px;background:var(--bg);color:var(--ink);font-size:15px;font-weight:700;cursor:pointer;font-family:inherit;transition:border-color .15s,background .15s}
  .mb-ans button:hover{border-color:var(--pink);background:var(--chip-pk)}
  .mb-type{font-size:44px;font-weight:900;letter-spacing:.04em;background:linear-gradient(90deg,var(--pink),var(--purple));-webkit-background-clip:text;background-clip:text;color:transparent}
  .mb-nick{font-size:20px;font-weight:900;margin-top:2px}
  .mb-axes{display:grid;gap:10px;margin:18px 0}
  .mb-ax{display:grid;grid-template-columns:28px 1fr 28px;gap:10px;align-items:center;font-size:13px;font-weight:900}
  .mb-ax .bar{height:10px;border-radius:99px;background:var(--line);position:relative;overflow:hidden}
  .mb-ax .bar i{position:absolute;top:0;bottom:0;background:var(--pink);border-radius:99px}
  .mb-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  @media (max-width:560px){.mb-grid{grid-template-columns:1fr}}
  .mb-card{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:14px 16px;font-size:13.5px;line-height:1.65}
  .mb-card b{display:block;font-size:12px;font-weight:900;color:var(--muted);margin-bottom:5px;letter-spacing:.04em}
"""

MBTI_BODY = r"""
      <div id="mb-intro">
        <p style="font-size:14px;color:var(--muted);margin:0 0 18px;line-height:1.7">24개의 짧은 질문에 솔직하게 답하면 <b style="color:var(--ink)">16가지 성격유형</b> 중 어디에 가까운지 보여드립니다. 정답은 없어요 — 고민 말고 더 끌리는 쪽을 고르세요.</p>
        <button class="btn btn-primary" id="mb-start" style="padding:13px 26px;border-radius:12px;border:0;font-size:15px">테스트 시작</button>
      </div>
      <div id="mb-quiz" style="display:none">
        <div class="mb-progress"><i id="mb-bar" style="width:0%"></i></div>
        <div style="font-size:12px;font-weight:800;color:var(--muted);margin-bottom:10px" id="mb-step">1 / 24</div>
        <div class="mb-q" id="mb-q"></div>
        <div class="mb-ans">
          <button id="mb-a"></button>
          <button id="mb-b"></button>
        </div>
      </div>
      <div id="mb-result" style="display:none">
        <div class="mb-type" id="mb-type"></div>
        <div class="mb-nick" id="mb-nick"></div>
        <div class="mb-axes" id="mb-axes"></div>
        <div class="mb-grid" id="mb-cards"></div>
        <div style="display:flex;gap:10px;margin-top:18px;flex-wrap:wrap">
          <button class="btn btn-primary" id="mb-copy" style="padding:11px 20px;border-radius:10px;border:0;font-size:14px">결과 복사하기</button>
          <button class="btn btn-ghost" id="mb-retry" style="padding:11px 20px;border-radius:10px;font-size:14px">다시 하기</button>
        </div>
      </div>
"""

MBTI_SCRIPT = r"""
<script>
(function(){
  var Q=[
    ['주말에 에너지를 충전하는 방법은?','사람들을 만나 수다 떨기','혼자 또는 소수랑 조용히 쉬기','E','I'],
    ['모임에서 나는 보통…','먼저 말을 거는 편','다가와 주길 기다리는 편','E','I'],
    ['새로운 사람들과 있을 때…','금방 편해지고 말이 많아짐','시간이 걸리고 조심스러워짐','E','I'],
    ['일할 때 나는…','말하면서 생각을 정리하는 편','머릿속으로 정리한 뒤 말하는 편','E','I'],
    ['오래 쉬고 나면…','사람들이 그리워서 나가고 싶음','집콕의 여운이 아쉬움','E','I'],
    ['파티가 끝나고 나면…','기분이 업되어 있음','좋았지만 에너지가 빠짐','E','I'],
    ['정보를 받아들일 때 나는…','눈에 보이는 사실·경험을 믿음','직감·가능성·의미를 더 봄','S','N'],
    ['설명을 들을 때 선호하는 건…','구체적인 예시와 순서','큰 그림과 핵심 개념','S','N'],
    ['새 아이디어를 들으면…','"그래서 실제로 되는 게 뭔데?"','"오, 그럼 이런 것도 되겠네?"','S','N'],
    ['나는 주로…','지금 현실에 집중하는 편','미래·상상에 빠지는 편','S','N'],
    ['여행 계획을 세우면…','검증된 맛집·코스 위주','즉흥적으로 새로운 데 찾기','S','N'],
    ['기억에 더 잘 남는 건…','있었던 일의 디테일','그때의 분위기와 느낌','S','N'],
    ['친구가 고민 상담하면…','해결책과 현실적 조언부터','일단 공감하고 감정부터','T','F'],
    ['결정할 때 더 중요한 건…','논리·기준·공정함','사람·관계·마음','T','F'],
    ['칭찬받고 싶은 말은…','"너 진짜 똑똑하다"','"너 진짜 따뜻하다"','T','F'],
    ['의견 충돌이 생기면…','옳고 그름을 끝까지 따짐','분위기를 해치지 않게 조율','T','F'],
    ['규칙과 원칙은…','대체로 지켜야 하는 것','상황과 사람에 따라 유연하게','T','F'],
    ['비판할 일이 생기면…','돌려 말하지 않고 직설적으로','상처받지 않게 완곡하게','T','F'],
    ['약속이 생기면…','일정표에 바로 정리하는 편','대충 기억했다가 즉흥으로','J','P'],
    ['마감이 다가오면…','미리미리 끝내야 마음 편함','데드라인 직전에 집중력 폭발','J','P'],
    ['계획 없는 하루는…','불안하고 어색함','자유롭고 신남','J','P'],
    ['물건 정리 스타일은…','제자리·정돈이 기본','어디 뒀는지는 나만 아는 정리','J','P'],
    ['결정을 내린 뒤에는…','마음이 후련하고 그대로 진행','혹시 다른 선택이 낫나 재고','J','P'],
    ['여행 가방을 쌀 때…','며칠 전부터 리스트 만들어 챙김','전날 밤에 필요한 것만 대충','J','P']
  ];
  var TYPES={
    'ISTJ':['청렴결백 논리주의자','한번 맡은 일은 끝까지 해내는 책임감의 화신. 원칙과 사실을 중시하고, 실수를 용납하지 않아 주변에 든든한 기둥 같은 존재예요.','체계적 · 꼼꼼함 · 의리','융통성 부족 · 감정 표현 서툼','ESFP, ENFP','ENFP'],
    'ISFJ':['용감한 수호자','조용히 묵묵히 사람을 챙기는 헌신형. 기억력이 좋아 주변의 작은 변화도 놓치지 않고, 배려의 디테일이 남달라요.','헌신 · 세심함 · 인내','거절 못함 · 자기희생 과다','ESFP, ESTP','ESTP'],
    'INFJ':['통찰력 있는 옹호자','겉은 조용한데 속은 깊은 이상가. 사람의 본질을 꿰뚫어 보는 직관력으로 의미 있는 변화를 만들고 싶어 해요.','통찰력 · 원칙 · 헌신','완벽주의 · 번아웃','ENFP, ENTP','ESTP'],
    'INTJ':['전략가','큰 그림을 설계하는 독립적 전략가. 비효율을 참지 못하고, 모든 것에 "더 나은 방법"을 찾는 개선 강박이 있어요.','분석력 · 독립심 · 추진력','융통성 · 감정 무시','ENFP, ENTP','ESFJ'],
    'ISTP':['만능 재주꾼','손으로 직접 만지고 분해해야 직성이 풀리는 실용주의자. 위기 상황에서 침착하게 문제를 해결하는 능력이 탁월해요.','침착함 · 실용성 · 관찰력','표현 부족 · 장기계획 약함','ESFJ, ESTJ','ESFJ'],
    'ISFP':['호기심 많은 예술가','조용히 자기 세계를 아름답게 꾸미는 감성형. 틀에 갇히길 거부하고, 지금 이 순간을 진심으로 즐기는 사람이에요.','감수성 · 겸손 · 유연성','우유부단 · 스트레스 회피','ENFJ, ESFJ','ENTJ'],
    'INFP':['열정적인 중재자','내면의 가치에 진심인 몽상가. 겉으론 조용해 보여도 신념 앞에선 누구보다 단단하고, 사람의 가능성을 믿어주는 존재예요.','공감력 · 진정성 · 창의력','현실 회피 · 번아웃','ENFJ, ENTJ','ESTJ'],
    'INTP':['논리학자','왜?를 멈추지 않는 아이디어 제조기. 틀에 박힌 논리를 싫어하고, 개념을 뜯어보며 새로운 해석을 만드는 걸 즐겨요.','분석력 · 창의성 · 객관성','실행력 · 감정 표현','ENTJ, ESTJ','ESFJ'],
    'ESTP':['활동적인 사업가','몸이 먼저 반응하는 행동파. 돌파력과 순발력이 뛰어나고, 지루한 이론보다 당장 해보는 쪽을 택해요.','추진력 · 순발력 · 현실감각','인내심 · 계획 부족','ISFJ, ISTJ','ISFJ'],
    'ESFP':['자유로운 연예인','어디서든 분위기 메이커. 사람과 놀이와 맛있는 것을 사랑하고, 주변까지 밝게 물들이는 전염성이 있어요.','친화력 · 낙관 · 순발력','집중력 · 장기계획','ISFJ, ISTJ','ISTJ'],
    'ENFP':['재기발랄한 활동가','호기심 폭발하는 아이디어 폭죽. 사람과 가능성을 사랑해서, 만나는 사람마다 영감을 주고받는 사람이에요.','열정 · 창의력 · 소통력','산만함 · 끈기 부족','INFJ, INTJ','ISTJ'],
    'ENTP':['논쟁을 즐기는 변론가','틀을 부수는 걸 좋아하는 발명가형. 어떤 주제든 뒤집어 보는 지적 유희를 즐기고, 새 프로젝트에 불을 붙이는 능력이 있어요.','독창성 · 토론력 · 적응력','마무리 부실 · 논쟁 과다','INFJ, INTJ','ISFJ'],
    'ESTJ':['엄격한 경영자','질서와 시스템의 수호자. 무엇이든 조직화해서 굴리는 능력이 탁월하고, 말보다 결과로 증명하는 사람이에요.','조직력 · 책임감 · 결단력','융통성 · 감정 배려','ISFP, ISTP','INFP'],
    'ESFJ':['사교적인 외교관','모두가 챙겨지는 자리를 만드는 살림꾼. 사람의 기분을 읽는 감각이 뛰어나고, 공동체의 접착제 역할을 해요.','배려 · 조직력 · 헌신','비판 취약 · 타인 의존','ISFP, ISTP','INTP'],
    'ENFJ':['정의로운 옹호자','사람을 이끌고 키우는 타고난 리더. 카리스마와 공감력을 겸비해서, 주변 사람의 성장을 자기 일처럼 챙겨요.','리더십 · 공감 · 추진력','자기 돌봄 부족 · 과민','INFP, ISFP','ISTP'],
    'ENTJ':['대담한 통솔자','목표를 향해 조직을 이끄는 타고난 지휘관. 효율과 성과의 기준이 높고, 불가능해 보이는 것도 플랜으로 부숴요.','리더십 · 전략 · 추진력','감정 무시 · 독단','INFP, INTP','ISFP']
  };
  var i=0,score={E:0,I:0,S:0,N:0,T:0,F:0,J:0,P:0};
  function showQ(){
    document.getElementById('mb-step').textContent=(i+1)+' / '+Q.length;
    document.getElementById('mb-bar').style.width=(i/Q.length*100)+'%';
    document.getElementById('mb-q').textContent='Q'+(i+1)+'. '+Q[i][0];
    document.getElementById('mb-a').textContent='A. '+Q[i][1];
    document.getElementById('mb-b').textContent='B. '+Q[i][2];
  }
  function answer(k){score[Q[i][k==='a'?3:4]]++; i++; if(i<Q.length)showQ(); else result();}
  function result(){
    var t=(score.E>=score.I?'E':'I')+(score.S>=score.N?'S':'N')+(score.T>=score.F?'T':'F')+(score.J>=score.P?'J':'P');
    var ty=TYPES[t];
    document.getElementById('mb-quiz').style.display='none';
    document.getElementById('mb-type').textContent=t;
    document.getElementById('mb-nick').textContent=ty[0];
    var axes=[['E','I'],['S','N'],['T','F'],['J','P']],ah='';
    axes.forEach(function(ax){
      var a=score[ax[0]],b=score[ax[1]],tot=a+b||1,pc=Math.round(a/tot*100);
      ah+='<div class="mb-ax"><span style="color:var(--pink)">'+ax[0]+'</span><div class="bar"><i style="width:'+pc+'%"></i></div><span style="text-align:right;color:var(--purple)">'+ax[1]+'</span></div>';
    });
    document.getElementById('mb-axes').innerHTML=ah;
    document.getElementById('mb-cards').innerHTML=
      '<div class="mb-card"><b>이런 사람</b>'+ty[1]+'</div>'
      +'<div class="mb-card"><b>강점</b>'+ty[2]+'</div>'
      +'<div class="mb-card"><b>약점</b>'+ty[3]+'</div>'
      +'<div class="mb-card"><b>잘 맞는 유형 / 거리두기 유형</b>'+ty[4]+' / '+ty[5]+'</div>';
    document.getElementById('mb-result').style.display='block';
    window._mbType=t;
  }
  document.getElementById('mb-start').addEventListener('click',function(){
    document.getElementById('mb-intro').style.display='none';
    document.getElementById('mb-quiz').style.display='block';
    showQ();
  });
  document.getElementById('mb-a').addEventListener('click',function(){answer('a');});
  document.getElementById('mb-b').addEventListener('click',function(){answer('b');});
  document.getElementById('mb-retry').addEventListener('click',function(){location.reload();});
  document.getElementById('mb-copy').addEventListener('click',function(){
    var t=window._mbType,ty=TYPES[t];
    var txt='싹싹김치 성격유형 테스트 결과: '+t+' — '+ty[0]+'\n'+ty[1]+'\n나도 테스트 → https://www.ssakkimchi.com/mbti.html';
    (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(function(){
      document.getElementById('mb-copy').textContent='복사됨!';
    }).catch(function(){prompt('복사하세요',txt);});
  });
})();
</script>
"""

PAGES = [
  dict(
    slug='saju', cat='play', name='무료 사주',
    title='무료 사주 보기 — 생년월일로 뽑는 사주팔자·오행 분석 (싹싹김치)',
    desc='생년월일만 넣으면 사주팔자가 바로 나옵니다. 양력·음력 지원, 오행 분포와 일간 성향, 올해 운세까지 — 설치·가입 없이 브라우저에서 보는 무료 사주.',
    og_title='무료 사주 보기 — 사주팔자·오행·올해 운세',
    og_desc='생년월일을 넣으면 팔자가 바로 나옵니다. 서버 업로드 없이 브라우저에서 계산.',
    h1='무료 사주 보기', pen='태어난 순간에 적힌 여덟 글자를 펼쳐봅니다.',
    pdesc='생년월일시를 넣으면 <b>사주팔자 네 기둥</b>과 오행 분포, 일간 성향, 올해 운세를 정리해드립니다. 양력·음력 둘 다 되고, 입력한 정보는 서버에 안 올라가요.',
    body=SAJU_BODY, css=SAJU_CSS, script=SAJU_SCRIPT,
    notice=[
      '이 결과는 전통 명리학 기반 <b>참고·재미용</b>입니다. 중요한 결정은 본인의 판단으로 하세요.',
      '입력한 생년월일은 어디에도 저장·전송되지 않습니다 — 계산은 100% 이 브라우저 안에서 끝납니다.',
      '시간을 모르면 시주 없이 6자로 봅니다. 해석의 정밀도는 조금 낮아져요.',
      '계산 엔진: lunar-javascript (MIT) — 음력 변환·팔자 추출을 정통 방식으로 처리합니다.'],
  ),
  dict(
    slug='mbti', cat='play', name='성격유형 테스트',
    title='성격유형 테스트 무료 — 24문항으로 알아보는 나의 유형 (싹싹김치)',
    desc='24개 질문에 답하면 16가지 성격유형 중 내 유형을 보여드립니다. 강점·약점·잘 맞는 유형까지 — 가입 없이 바로 하는 무료 성격유형 검사.',
    og_title='성격유형 테스트 — 24문항으로 보는 내 유형',
    og_desc='16가지 유형 중 나는 어디? 결과 복사해서 친구랑 비교해보세요.',
    h1='성격유형 테스트', pen='고민 말고, 더 끌리는 쪽으로.',
    pdesc='E/I · S/N · T/F · J/P <b>네 축 24문항</b>으로 내 성향을 분석합니다. 유형별 별칭과 설명, 강점·약점, 궁합 좋은 유형까지 한 번에.',
    body=MBTI_BODY, css=MBTI_CSS, script=MBTI_SCRIPT,
    notice=[
      '이 테스트는 <b>공식 MBTI® 검사가 아닌</b> 유사 성격유형 테스트입니다. 재미와 자기 이해용으로 봐주세요.',
      '응답 내용은 저장·전송되지 않습니다 — 채점은 전부 브라우저에서 끝납니다.',
      '유형은 선천적 성격 진단이 아니라 "지금 나의 경향"에 가까워요. 몇 달 뒤에 다시 하면 달라질 수도 있어요.'],
  ),
]
