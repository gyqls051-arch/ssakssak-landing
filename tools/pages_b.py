# -*- coding: utf-8 -*-
# gen_pages.py 페이지 데이터 B — 키보드·마우스 테스트 / 디데이 / 실수령액

PAGES = [
# ============================================================ 키보드·마우스 테스트
{
 'slug':'input-test','name':'키보드·마우스 테스트','cat':'screen',
 'title':'키보드 테스트·마우스 테스트 무료 — 입력기기 점검 (싹싹김치)',
 'desc':'키 하나하나 눌러보며 고장 키를 찾고, 마우스 버튼·휠·더블클릭 속도까지 점검. 새 키보드·마우스 불량 확인용 무료 테스트 도구.',
 'og_title':'키보드·마우스 테스트 무료 — 싹싹김치',
 'og_desc':'키 입력·버튼·휠·더블클릭 점검. 브라우저에서 바로.',
 'h1':'키보드·마우스 테스트','pen':'새 키보드 왔으면 여기서부터.',
 'pdesc':'키보드를 사거나 키가 이상할 때 — 아래 키 배열을 전부 눌러보세요. <b>반응한 키는 초록색</b>으로 표시되고, 입력 정보가 실시간으로 뜹니다.',
 'css':"""
  .it-sec{margin-top:8px}
  .it-sec+.it-sec{margin-top:30px;border-top:1px solid var(--line);padding-top:26px}
  .it-h{font-size:15px;font-weight:900;margin:0 0 14px;display:flex;align-items:center;gap:8px}
  .it-last{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin-bottom:16px}
  .it-cell{background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:10px 12px;text-align:center}
  .it-cell .v{font-size:16px;font-weight:800;font-family:Consolas,monospace;word-break:break-all}
  .it-cell .k{font-size:11px;font-weight:700;color:var(--faint);margin-top:2px}
  .kbd{display:flex;flex-direction:column;gap:6px;user-select:none}
  .kbd-row{display:flex;gap:6px}
  .kb{flex:1;min-width:0;height:38px;display:flex;align-items:center;justify-content:center;background:var(--bg2);border:1px solid var(--line);border-radius:8px;font-size:12px;font-weight:700;color:var(--muted);font-family:Consolas,monospace;transition:all .1s ease}
  .kb.down{background:var(--accent);border-color:var(--accent);color:#fff}
  .kb.ok{background:var(--chip-g);border-color:var(--green);color:var(--green-ink)}
  .kb.w2{flex:1.6}.kb.w3{flex:2.4}.kb.w6{flex:6}
  .mouse-zone{position:relative;height:210px;background:var(--bg2);border:1px dashed var(--line);border-radius:16px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;cursor:crosshair;user-select:none;overflow:hidden}
  .mz-btns{display:flex;gap:14px}
  .mz-btn{padding:10px 22px;border-radius:12px;border:1px solid var(--line);background:var(--card);font-size:13px;font-weight:800;color:var(--muted);transition:all .1s ease}
  .mz-btn.hit{background:var(--chip-g);border-color:var(--green);color:var(--green-ink)}
  .mz-btn.down{background:var(--accent);border-color:var(--accent);color:#fff}
  .mz-info{font-size:12.5px;font-weight:600;color:var(--faint);font-family:Consolas,monospace}
  .mz-dot{position:absolute;width:8px;height:8px;border-radius:50%;background:var(--accent);opacity:.55;pointer-events:none}
  .it-stats{display:flex;gap:18px;flex-wrap:wrap;margin-top:12px;font-size:12.5px;font-weight:700;color:var(--faint)}
  .it-stats b{color:var(--ink)}
  .tool-row{display:flex;gap:10px;align-items:center;margin-top:16px;flex-wrap:wrap}
 """,
 'body':"""      <div class="it-sec">
        <h3 class="it-h">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="12" rx="2.5"/><path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M6 14h.01M18 14h.01M9 14h6"/></svg>
          키보드 테스트
        </h3>
        <div class="it-last">
          <div class="it-cell"><div class="v" id="kKey">—</div><div class="k">마지막 키 (key)</div></div>
          <div class="it-cell"><div class="v" id="kCode">—</div><div class="k">물리 위치 (code)</div></div>
          <div class="it-cell"><div class="v" id="kCnt">0</div><div class="k">입력 횟수</div></div>
          <div class="it-cell"><div class="v" id="kHit">0/58</div><div class="k">확인된 키</div></div>
        </div>
        <div class="kbd" id="kbd"></div>
        <div class="tool-row">
          <button class="btn btn-ghost btn-sm" id="kReset">키 기록 초기화</button>
        </div>
      </div>

      <div class="it-sec">
        <h3 class="it-h">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--accent)" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="3" width="12" height="18" rx="6"/><path d="M12 7v4"/></svg>
          마우스 테스트
        </h3>
        <div class="mouse-zone" id="mz">
          <div class="mz-btns">
            <span class="mz-btn" id="bL">좌클릭</span>
            <span class="mz-btn" id="bM">휠클릭</span>
            <span class="mz-btn" id="bR">우클릭</span>
          </div>
          <div class="mz-info" id="mzInfo">이 영역에서 클릭·휠·더블클릭을 해보세요</div>
        </div>
        <div class="it-stats">
          <span>좌클릭 <b id="cL">0</b></span>
          <span>휠클릭 <b id="cM">0</b></span>
          <span>우클릭 <b id="cR">0</b></span>
          <span>더블클릭 <b id="cD">0</b> (최근 간격 <b id="cDms">—</b>)</span>
          <span>휠 스크롤 <b id="cW">0</b>회</span>
          <span>포인터 <b id="cP">—</b></span>
        </div>
      </div>
      <div class="status-line"><span class="dot ready" id="dot"></span><span id="st">키보드 영역은 페이지 어디서든 입력이 감지됩니다</span></div>""",
 'notice':[
   '키 배열에 없는 기능키(F1~F12 등)도 위쪽 입력 정보에서 code 값으로 확인할 수 있습니다.',
   '노트북은 Fn 조합키가 브라우저까지 전달되지 않을 수 있습니다 — 이 도구가 아니라 OS가 먼저 가로채는 정상 동작입니다.',
   '마우스 우클릭은 이 영역에서 컨텍스트 메뉴를 막고 버튼만 감지합니다.',
   "도구는 '있는 그대로' 제공됩니다. <a href=\"terms.html\">이용약관</a>",
 ],
 'script':"""<script>
(function(){
"use strict";
var ROWS=[
 ['Backquote','Digit1','Digit2','Digit3','Digit4','Digit5','Digit6','Digit7','Digit8','Digit9','Digit0','Minus','Equal','Backspace'],
 ['Tab','KeyQ','KeyW','KeyE','KeyR','KeyT','KeyY','KeyU','KeyI','KeyO','KeyP','BracketLeft','BracketRight','Backslash'],
 ['CapsLock','KeyA','KeyS','KeyD','KeyF','KeyG','KeyH','KeyJ','KeyK','KeyL','Semicolon','Quote','Enter'],
 ['ShiftLeft','KeyZ','KeyX','KeyC','KeyV','KeyB','KeyN','KeyM','Comma','Period','Slash','ShiftRight'],
 ['Space','ArrowLeft','ArrowUp','ArrowDown','ArrowRight']
];
var LABELS={Backquote:'`',Digit1:'1',Digit2:'2',Digit3:'3',Digit4:'4',Digit5:'5',Digit6:'6',Digit7:'7',Digit8:'8',Digit9:'9',Digit0:'0',Minus:'-',Equal:'=',Backspace:'←',
Tab:'Tab',KeyQ:'Q',KeyW:'W',KeyE:'E',KeyR:'R',KeyT:'T',KeyY:'Y',KeyU:'U',KeyI:'I',KeyO:'O',KeyP:'P',BracketLeft:'[',BracketRight:']',Backslash:'\\\\',
CapsLock:'Caps',KeyA:'A',KeyS:'S',KeyD:'D',KeyF:'F',KeyG:'G',KeyH:'H',KeyJ:'J',KeyK:'K',KeyL:'L',Semicolon:';',Quote:"'",Enter:'Enter',
ShiftLeft:'Shift',KeyZ:'Z',KeyX:'X',KeyC:'C',KeyV:'V',KeyB:'B',KeyN:'N',KeyM:'M',Comma:',',Period:'.',Slash:'/',ShiftRight:'Shift',
Space:'Space',ArrowLeft:'◀',ArrowUp:'▲',ArrowDown:'▼',ArrowRight:'▶'};
var WID={Backspace:'w2',Tab:'w2',Backslash:'w2',CapsLock:'w2',Enter:'w3',ShiftLeft:'w3',ShiftRight:'w3',Space:'w6'};
var kbd=document.getElementById('kbd'),hit={},cells={},total=0;
ROWS.forEach(function(r){
  var row=document.createElement('div');row.className='kbd-row';
  r.forEach(function(code){
    total++;
    var k=document.createElement('div');k.className='kb'+(WID[code]?' '+WID[code]:'');
    k.id='kb-'+code;k.textContent=LABELS[code]||code;
    row.appendChild(k);cells[code]=k;
  });
  kbd.appendChild(row);
});
var kKey=document.getElementById('kKey'),kCode=document.getElementById('kCode'),
    kCnt=document.getElementById('kCnt'),kHit=document.getElementById('kHit'),cnt=0;
function hitCount(){var n=0;for(var k in hit)if(hit[k])n++;return n;}
document.addEventListener('keydown',function(e){
  var tag=(e.target&&e.target.tagName)||'';
  if(tag==='INPUT'||tag==='TEXTAREA'||tag==='SELECT')return;
  kKey.textContent=e.key===' '?'Space':e.key;
  kCode.textContent=e.code;cnt++;kCnt.textContent=cnt;
  var c=cells[e.code];
  if(c){hit[e.code]=1;c.classList.add('ok');}
  kHit.textContent=hitCount()+'/'+total;
  if(e.code==='Space'||e.code==='Tab'||e.code.indexOf('Arrow')===0)e.preventDefault();
});
document.getElementById('kReset').addEventListener('click',function(){
  hit={};cnt=0;kCnt.textContent='0';kHit.textContent='0/'+total;
  kKey.textContent='—';kCode.textContent='—';
  Object.keys(cells).forEach(function(k){cells[k].classList.remove('ok');});
});
var mz=document.getElementById('mz'),mzInfo=document.getElementById('mzInfo');
var btns={0:document.getElementById('bL'),1:document.getElementById('bM'),2:document.getElementById('bR')};
var cnts={L:0,M:0,R:0,D:0,W:0},lastClick=0;
var cL=document.getElementById('cL'),cM=document.getElementById('cM'),cR=document.getElementById('cR'),
    cD=document.getElementById('cD'),cDms=document.getElementById('cDms'),
    cW=document.getElementById('cW'),cP=document.getElementById('cP');
mz.addEventListener('contextmenu',function(e){e.preventDefault();});
mz.addEventListener('mousedown',function(e){
  var b=btns[e.button];if(!b)return;
  b.classList.add('down');b.classList.add('hit');
  if(e.button===0){cnts.L++;cL.textContent=cnts.L;
    var now=performance.now(),gap=now-lastClick;lastClick=now;
    if(gap<300){cnts.D++;cD.textContent=cnts.D;cDms.textContent=Math.round(gap)+'ms';}
  }
  if(e.button===1){cnts.M++;cM.textContent=cnts.M;e.preventDefault();}
  if(e.button===2){cnts.R++;cR.textContent=cnts.R;}
  var d=document.createElement('div');d.className='mz-dot';
  var r=mz.getBoundingClientRect();
  d.style.left=(e.clientX-r.left-4)+'px';d.style.top=(e.clientY-r.top-4)+'px';
  mz.appendChild(d);
  setTimeout(function(){d.remove();},1600);
});
mz.addEventListener('mouseup',function(e){var b=btns[e.button];if(b)b.classList.remove('down');});
mz.addEventListener('mousemove',function(e){
  var r=mz.getBoundingClientRect();
  cP.textContent=Math.round(e.clientX-r.left)+','+Math.round(e.clientY-r.top);
});
mz.addEventListener('wheel',function(e){
  e.preventDefault();cnts.W++;cW.textContent=cnts.W;
  mzInfo.textContent='휠 '+(e.deltaY>0?'↓ 아래로':'↑ 위로')+' (deltaY '+Math.round(e.deltaY)+')';
},{passive:false});
})();
</script>""",
},

# ============================================================ 디데이 계산기
{
 'slug':'dday','name':'디데이 계산기','cat':'life',
 'title':'디데이 계산기 무료 — 날짜 차이·기념일·N일 후 계산 (싹싹김치)',
 'desc':'목표일까지 며칠 남았는지, 두 날짜 사이 일수, 100일·1주년 기념일, N일 후 날짜까지 한 화면에서 계산하는 무료 디데이 계산기.',
 'og_title':'디데이·날짜 계산기 무료 — 싹싹김치',
 'og_desc':'D-day, 날짜 차이, 기념일, N일 후까지 한 화면에서.',
 'h1':'디데이 계산기','pen':'수능·전역일·기념일, 며칠 남았지?',
 'pdesc':'목표일을 고르면 <b>D-day</b>와 요일이 바로 뜨고, 100일·1주년 같은 기념일도 자동으로 계산해줍니다. 수능, 전역일, 여행, 프로젝트 마감까지.',
 'css':"""
  .dd-grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start}
  .dd-card{background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:20px}
  .dd-card h3{margin:0 0 12px;font-size:14.5px;font-weight:900}
  .dd-card input[type=date],.dd-card input[type=number]{font-family:inherit;font-size:15px;font-weight:700;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:12px;padding:11px 14px;outline:none;width:100%;box-sizing:border-box}
  .dd-card input:focus{border-color:var(--accent)}
  .dd-big{font-size:52px;font-weight:900;letter-spacing:-.03em;line-height:1.1;margin-top:6px}
  .dd-big .u{font-size:20px;font-weight:800;color:var(--faint);margin-left:4px}
  .dd-sub{font-size:13px;font-weight:600;color:var(--muted);margin-top:6px}
  .dd-list{margin-top:14px;border-top:1px solid var(--line);padding-top:12px;display:flex;flex-direction:column;gap:7px}
  .dd-item{display:flex;justify-content:space-between;font-size:13px}
  .dd-item b{font-weight:800}
  .dd-item span{color:var(--muted);font-weight:600}
  .dd-item.past b{color:var(--faint)}
  .dd-item.today b{color:var(--accent)}
  @media (max-width:700px){.dd-grid{grid-template-columns:1fr}}
 """,
 'body':"""      <div class="dd-grid">
        <div class="dd-card">
          <h3>📌 디데이</h3>
          <input type="date" id="dTarget">
          <div class="dd-big" id="dBig">D-?</div>
          <div class="dd-sub" id="dSub">목표일을 고르면 계산됩니다</div>
        </div>
        <div class="dd-card">
          <h3>⏱ N일 계산</h3>
          <div style="display:flex;gap:8px;align-items:center">
            <input type="number" id="nDays" value="100" min="-36500" max="36500" style="flex:1">
            <button class="btn btn-ghost btn-sm" id="nCalc">계산</button>
          </div>
          <div class="dd-sub" id="nOut" style="margin-top:12px;font-size:14px">오늘부터 N일 후/전 날짜</div>
          <div class="dd-list" id="nChips"></div>
        </div>
      </div>
      <div class="dd-card" style="margin-top:26px">
        <h3>🎉 기념일 목록 <span style="font-weight:600;color:var(--faint);font-size:12px">— 디데이 날짜 기준</span></h3>
        <div class="dd-list" id="anniv"></div>
      </div>
      <div class="status-line"><span class="dot ready" id="dot"></span><span id="st">날짜만 고르면 끝 — 계산은 전부 자동입니다</span></div>""",
 'notice':[
   'D-day는 오늘 기준입니다 — D-1이면 내일, D+1이면 어제가 목표일입니다.',
   '두 날짜 차이 계산: 디데이 목표일과 오늘의 차이가 곧 일수입니다.',
   '기념일 목록은 목표일 기준 +100일·+200일…+1000일과 1·2·3주년을 보여줍니다 (연애·입사 기념일처럼 "지난 날짜"를 넣으면 됩니다).',
   "도구는 '있는 그대로' 제공됩니다. <a href=\"terms.html\">이용약관</a>",
 ],
 'script':"""<script>
(function(){
"use strict";
var t=document.getElementById('dTarget'),big=document.getElementById('dBig'),sub=document.getElementById('dSub'),
    ann=document.getElementById('anniv'),nIn=document.getElementById('nDays'),nOut=document.getElementById('nOut'),
    nChips=document.getElementById('nChips');
var WD=['일','월','화','수','목','금','토'];
function day(d){return new Date(d.getFullYear(),d.getMonth(),d.getDate());}
function today(){return day(new Date());}
function fmt(d){return d.getFullYear()+'년 '+(d.getMonth()+1)+'월 '+d.getDate()+'일 ('+WD[d.getDay()]+')';}
function diff(a,b){return Math.round((day(a)-day(b))/86400000);}
var saved=null;try{saved=localStorage.getItem('ssak-dday');}catch(e){}
if(saved)t.value=saved;
function calc(){
  if(!t.value){big.textContent='D-?';sub.textContent='목표일을 고르면 계산됩니다';ann.innerHTML='<div class="dd-item"><span>목표일을 먼저 골라주세요</span></div>';return;}
  try{localStorage.setItem('ssak-dday',t.value);}catch(e){}
  var parts=t.value.split('-'),target=new Date(+parts[0],+parts[1]-1,+parts[2]);
  var d=diff(target,today());
  if(d===0)big.innerHTML='D-DAY';
  else if(d>0)big.innerHTML='D-'+d;
  else big.innerHTML='D+'+(-d);
  sub.textContent=fmt(target)+(d>0?' · '+d+'일 남음':d<0?' · '+(-d)+'일 지남':' · 바로 오늘!');
  var rows='';
  [100,200,300,365,500,730,1000,1095,1825].forEach(function(n){
    var isYear=(n===365||n===730||n===1095||n===1825);
    var label=isYear?(n/365)+'주년':n+'일';
    var dt=new Date(target.getFullYear(),target.getMonth(),target.getDate()+n);
    var dleft=diff(dt,today());
    var cls=dleft===0?'today':dleft<0?'past':'';
    var tail=dleft===0?'오늘!':dleft>0?'D-'+dleft:'지남';
    rows+='<div class="dd-item '+cls+'"><b>'+label+'</b><span>'+fmt(dt)+' · '+tail+'</span></div>';
  });
  ann.innerHTML=rows;
}
function nCalc(){
  var n=parseInt(nIn.value,10);if(isNaN(n)){nOut.textContent='숫자를 입력하세요';return;}
  var d=new Date();d.setDate(d.getDate()+n);
  nOut.innerHTML='<b style="font-size:17px">'+fmt(d)+'</b>';
}
['30','100','365'].forEach(function(v){
  var b=document.createElement('button');b.className='btn btn-ghost btn-sm';
  b.textContent='+'+v+'일';b.style.padding='4px 10px';b.style.fontSize='12px';
  b.addEventListener('click',function(){nIn.value=v;nCalc();});
  nChips.appendChild(b);
});
var mb=document.createElement('button');mb.className='btn btn-ghost btn-sm';
mb.textContent='-30일';mb.style.padding='4px 10px';mb.style.fontSize='12px';
mb.addEventListener('click',function(){nIn.value=-30;nCalc();});
nChips.appendChild(mb);
document.getElementById('nCalc').addEventListener('click',nCalc);
nIn.addEventListener('keydown',function(e){if(e.key==='Enter')nCalc();});
t.addEventListener('change',calc);t.addEventListener('input',calc);
calc();nCalc();
})();
</script>""",
},

# ============================================================ 실수령액 계산기
{
 'slug':'salary','name':'실수령액 계산기','cat':'life',
 'title':'연봉 실수령액 계산기 무료 — 2025 월급 실수령 (싹싹김치)',
 'desc':'연봉·월급을 넣으면 4대보험과 소득세를 뺀 월 실수령액을 계산. 2025년 국민연금 4.75%·건강보험 3.545%·고용보험 0.9% 반영 무료 계산기.',
 'og_title':'연봉 실수령액 계산기 무료 — 싹싹김치',
 'og_desc':'4대보험·세금 다 빼면 월에 얼마? 2025년 요율 반영.',
 'h1':'실수령액 계산기','pen':'연봉 5천, 통장엔 얼마?',
 'pdesc':'연봉이나 월급을 넣으면 <b>4대보험과 소득세를 뺀 실수령액</b>이 나옵니다. 2025년 요율 기준으로 국민연금·건강보험·장기요양·고용보험·소득세·지방소득세를 계산합니다.',
 'css':"""
  .sl-grid{display:grid;grid-template-columns:1fr 1.2fr;gap:26px;align-items:start}
  .sl-field{margin-bottom:16px}
  .sl-field label{display:block;font-size:12.5px;font-weight:800;color:var(--faint);margin-bottom:7px}
  .sl-field input,.sl-field select{width:100%;box-sizing:border-box;font-family:inherit;font-size:16px;font-weight:700;color:var(--ink);background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:12px 14px;outline:none}
  .sl-field input:focus{border-color:var(--accent)}
  .sl-tabs{display:flex;gap:6px;background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:4px;margin-bottom:16px}
  .sl-tab{flex:1;text-align:center;padding:8px 0;border-radius:9px;font-size:13px;font-weight:800;color:var(--muted);cursor:pointer;transition:all .15s ease}
  .sl-tab.on{background:var(--card);color:var(--ink);box-shadow:0 2px 8px var(--shadow)}
  .sl-result{background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:20px}
  .sl-net{font-size:46px;font-weight:900;letter-spacing:-.03em;color:var(--accent);line-height:1.15}
  .sl-net small{font-size:16px;font-weight:800;color:var(--faint)}
  .sl-rows{margin-top:16px;border-top:1px solid var(--line);padding-top:12px;display:flex;flex-direction:column;gap:8px}
  .sl-row{display:flex;justify-content:space-between;font-size:13.5px}
  .sl-row span{color:var(--muted);font-weight:600}
  .sl-row b{font-weight:800;font-variant-numeric:tabular-nums}
  .sl-row.total{border-top:1px dashed var(--line);padding-top:9px;font-size:14.5px}
  .sl-note{font-size:11.5px;color:var(--faint);margin-top:12px;line-height:1.6}
  @media (max-width:700px){.sl-grid{grid-template-columns:1fr}}
 """,
 'body':"""      <div class="sl-grid">
        <div>
          <div class="sl-tabs">
            <div class="sl-tab on" id="tabY">연봉 입력</div>
            <div class="sl-tab" id="tabM">월급 입력</div>
          </div>
          <div class="sl-field">
            <label id="amtLabel">연봉 (세전, 만원)</label>
            <input type="number" id="slAmt" value="5000" min="0" step="10">
          </div>
          <div class="sl-field">
            <label>비과세 식대 (월, 만원 — 최대 20)</label>
            <input type="number" id="slMeal" value="20" min="0" max="20">
          </div>
          <div class="sl-field">
            <label>부양가족 수 (본인 포함)</label>
            <select id="slFam"><option value="1" selected>1명 (나 혼자)</option><option value="2">2명</option><option value="3">3명</option><option value="4">4명</option><option value="5">5명 이상</option></select>
          </div>
          <div class="sl-field">
            <label>20세 이하 자녀 수</label>
            <select id="slKid"><option value="0" selected>없음</option><option value="1">1명</option><option value="2">2명</option><option value="3">3명 이상</option></select>
          </div>
        </div>
        <div class="sl-result">
          <div style="font-size:12.5px;font-weight:800;color:var(--faint)">예상 월 실수령액</div>
          <div class="sl-net" id="slNet">—</div>
          <div class="sl-rows" id="slRows"></div>
          <div class="sl-note">2025년 요율 기준 (국민연금 4.75%, 건강보험 3.545%, 장기요양 건보의 12.95%, 고용보험 0.9%). 소득세는 연말정산 방식으로 추정한 근사치로, 회사의 간이세액표 적용과 수십만 원 차이가 날 수 있습니다.</div>
        </div>
      </div>
      <div class="status-line"><span class="dot ready" id="dot"></span><span id="st">숫자만 바꾸면 바로 다시 계산됩니다</span></div>""",
 'notice':[
   '4대보험은 <b>2025년 근로자 부담분</b> 기준입니다 (국민연금 4.75%·상한 월 617만, 건강보험 3.545%, 장기요양 건보의 12.95%, 고용보험 0.9%).',
   '소득세는 근로소득공제·인적공제·근로소득세액공제를 적용한 <b>연 단위 추정치의 1/12</b>입니다. 실제 월 원천징수는 간이세액표라 다를 수 있습니다.',
   '상여·성과급이 따로 있는 경우 연봉에 포함해 넣으세요. 비과세 항목(식대 20만·차량유지비 등)이 많으면 실수령이 더 늘어납니다.',
   "도구는 '있는 그대로' 제공됩니다. <a href=\"terms.html\">이용약관</a>",
 ],
 'script':"""<script>
(function(){
"use strict";
var amt=document.getElementById('slAmt'),meal=document.getElementById('slMeal'),
    fam=document.getElementById('slFam'),kid=document.getElementById('slKid'),
    net=document.getElementById('slNet'),rows=document.getElementById('slRows'),
    tabY=document.getElementById('tabY'),tabM=document.getElementById('tabM'),
    lbl=document.getElementById('amtLabel');
var mode='Y';
function won(n){return Math.round(n).toLocaleString('ko-KR');}
function calc(){
  var v=parseFloat(amt.value)||0;
  var annual=(mode==='Y')?v:v*12;                    // 만원
  var monthly=annual/12;                            // 만원
  var mealM=Math.min(Math.max(parseFloat(meal.value)||0,0),20);
  var taxableM=Math.max(monthly-mealM,0);           // 과세 대상 월
  var pensionBase=Math.min(taxableM,617);           // 국민연금 상한(2025)
  var pension=taxableM*0.0475; if(taxableM>617)pension=617*0.0475;
  var health=taxableM*0.03545;
  var care=health*0.1295;
  var emp=taxableM*0.009;
  var insTotal=pension+health+care+emp;             // 만원/월
  // --- 소득세: 연 단위 추정 ---
  var g=annual-mealM*12;                            // 총급여(과세)
  var ded;                                          // 근로소득공제
  if(g<=500)ded=g*0.7;
  else if(g<=1500)ded=350+(g-500)*0.4;
  else if(g<=4500)ded=750+(g-1500)*0.15;
  else if(g<=10000)ded=1200+(g-4500)*0.05;
  else ded=1475+(g-10000)*0.02;
  ded=Math.min(ded,2000);
  var famN=parseInt(fam.value,10)||1;
  var taxable=Math.max(g-ded-150*famN-(insTotal*12),0); // 근소공제+인적+보험료공제(만원)
  var t=taxable;                                    // 산출세액 (만원)
  var tax;
  if(t<=1400)tax=t*0.06;
  else if(t<=5000)tax=84+(t-1400)*0.15;
  else if(t<=8800)tax=624+(t-5000)*0.24;
  else if(t<=15000)tax=1536+(t-8800)*0.35;
  else if(t<=30000)tax=3706+(t-15000)*0.38;
  else if(t<=50000)tax=9406+(t-30000)*0.40;
  else if(t<=100000)tax=17406+(t-50000)*0.42;
  else tax=38406+(t-100000)*0.45;
  // 근로소득세액공제: 산출세액 130만 이하 55%, 초과 71.5만+초과분 30% (한도 74만→66만 단순화)
  var credit=(tax<=130)?tax*0.55:71.5+(tax-130)*0.30;
  credit=Math.min(credit,74);
  tax=Math.max(tax-credit,0);
  var kidN=parseInt(kid.value,10)||0;
  if(kidN===1)tax=Math.max(tax-15,0);else if(kidN===2)tax=Math.max(tax-35,0);else if(kidN>=3)tax=Math.max(tax-35-30*(kidN-2),0);
  var incM=tax/12;                                  // 월 소득세(만원)
  var localM=incM*0.1;
  var deductM=insTotal+incM+localM;
  var netM=monthly-deductM;
  net.innerHTML='약 '+won(netM)+'<small> 만원</small>';
  var r='';
  r+='<div class="sl-row"><span>세전 월급</span><b>'+won(monthly)+'만</b></div>';
  r+='<div class="sl-row"><span>국민연금 4.75%</span><b>-'+won(pension)+'만</b></div>';
  r+='<div class="sl-row"><span>건강보험 3.545%</span><b>-'+won(health)+'만</b></div>';
  r+='<div class="sl-row"><span>장기요양보험</span><b>-'+won(care)+'만</b></div>';
  r+='<div class="sl-row"><span>고용보험 0.9%</span><b>-'+won(emp)+'만</b></div>';
  r+='<div class="sl-row"><span>소득세 (추정)</span><b>-'+won(incM)+'만</b></div>';
  r+='<div class="sl-row"><span>지방소득세</span><b>-'+won(localM)+'만</b></div>';
  r+='<div class="sl-row total"><span>공제 합계</span><b>-'+won(deductM)+'만</b></div>';
  r+='<div class="sl-row"><span>연 실수령 추정</span><b>약 '+won(netM*12)+'만</b></div>';
  rows.innerHTML=r;
}
tabY.addEventListener('click',function(){mode='Y';tabY.classList.add('on');tabM.classList.remove('on');lbl.textContent='연봉 (세전, 만원)';calc();});
tabM.addEventListener('click',function(){mode='M';tabM.classList.add('on');tabY.classList.remove('on');lbl.textContent='월급 (세전, 만원)';calc();});
[amt,meal,fam,kid].forEach(function(el){el.addEventListener('input',calc);el.addEventListener('change',calc);});
calc();
})();
</script>""",
},
]
