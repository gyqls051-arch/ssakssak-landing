# -*- coding: utf-8 -*-
# gen_pages.py 페이지 데이터 A — QR / 비밀번호 / 불량화소

PAGES = [
# ============================================================ QR 생성기
{
 'slug':'qr','name':'QR 생성기','cat':'life',
 'title':'QR 코드 만들기 무료 — 링크·와이파이 QR 생성기 (싹싹김치)',
 'desc':'URL·텍스트·와이파이 정보를 QR 코드로 즉시 변환. 크기·오류정정 수준 조절, PNG 다운로드. 서버 업로드 없이 브라우저에서 100% 생성되는 무료 QR 생성기.',
 'og_title':'QR 코드 생성기 무료 — 싹싹김치',
 'og_desc':'링크·텍스트를 QR로 즉시 변환. 브라우저에서 바로, 무료.',
 'h1':'QR 생성기','pen':'주소 넣으면 뚝딱, QR 완성.',
 'pdesc':'URL·텍스트·와이파이 정보를 <b>QR 코드</b>로 바로 만듭니다. 명함, 메뉴판, 와이파이 공유, 인쇄물에 바로 쓸 수 있어요.',
 'extra_head':'<script defer src="js/vendor/qrcode.min.js"></script>',
 'css':"""
  .qr-in{width:100%;box-sizing:border-box;font-family:inherit;font-size:15px;color:var(--ink);background:var(--bg2);border:1px solid var(--line);border-radius:14px;padding:14px 16px;outline:none}
  .qr-in:focus{border-color:var(--accent)}
  .qr-grid{display:grid;grid-template-columns:1fr 280px;gap:26px;align-items:start}
  .qr-opts{display:flex;gap:16px;flex-wrap:wrap;margin-top:16px}
  .qr-opt{display:flex;flex-direction:column;gap:6px;font-size:12px;font-weight:700;color:var(--faint)}
  .qr-opt select{font-family:inherit;font-size:13.5px;font-weight:600;color:var(--ink);background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:8px 12px;outline:none}
  .qr-stage{background:var(--bg2);border:1px dashed var(--line);border-radius:18px;padding:22px;display:flex;align-items:center;justify-content:center;min-height:280px}
  .qr-stage img{max-width:100%;image-rendering:pixelated;border-radius:8px}
  .qr-empty{color:var(--faint);font-size:13.5px;font-weight:600;text-align:center}
  .tool-row{display:flex;gap:10px;align-items:center;margin-top:20px;flex-wrap:wrap}
  @media (max-width:700px){.qr-grid{grid-template-columns:1fr}}
 """,
 'body':"""      <div class="qr-grid">
        <div>
          <input class="qr-in" id="qrText" type="text" placeholder="링크 또는 텍스트 입력 — 예: https://www.ssakkimchi.com" maxlength="2000">
          <div class="qr-opts">
            <label class="qr-opt">크기
              <select id="qrSize"><option value="6">보통</option><option value="8" selected>크게</option><option value="12">인쇄용</option></select>
            </label>
            <label class="qr-opt">오류 정정
              <select id="qrEcc"><option value="L">L (7%)</option><option value="M" selected>M (15%)</option><option value="Q">Q (25%)</option><option value="H">H (30%)</option></select>
            </label>
            <label class="qr-opt">여백
              <select id="qrMargin"><option value="2">좁게</option><option value="4" selected>보통</option><option value="8">넓게</option></select>
            </label>
          </div>
          <div class="tool-row">
            <button class="btn btn-primary" id="qrDl" disabled>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12m0 0 4-4m-4 4-4-4M4 21h16"/></svg>
              PNG 다운로드
            </button>
          </div>
          <div class="status-line"><span class="dot" id="dot"></span><span id="st">텍스트를 입력하면 QR이 바로 만들어집니다</span></div>
        </div>
        <div class="qr-stage" id="qrStage"><span class="qr-empty">QR 미리보기</span></div>
      </div>""",
 'notice':[
   '입력한 내용은 서버로 전송되지 않습니다 — 브라우저 안에서만 QR이 생성됩니다.',
   '오류 정정 수준을 높이면(H) QR 일부가 가려져도 읽히지만 코드가 커집니다. 인쇄물엔 Q 이상을 권장합니다.',
   '와이파이 공유용은 <code>WIFI:T:WPA;S:네트워크명;P:비밀번호;;</code> 형식으로 입력하면 스마트폰 카메라로 바로 접속됩니다.',
   "도구는 '있는 그대로' 제공됩니다. <a href=\"terms.html\">이용약관</a>",
 ],
 'script':"""<script>
(function(){
"use strict";
var inp=document.getElementById('qrText'),stage=document.getElementById('qrStage'),
    size=document.getElementById('qrSize'),ecc=document.getElementById('qrEcc'),margin=document.getElementById('qrMargin'),
    dl=document.getElementById('qrDl'),st=document.getElementById('st'),dot=document.getElementById('dot');
var dataUrl='';
function render(){
  var txt=inp.value;
  if(!txt.trim()){stage.innerHTML='<span class="qr-empty">QR 미리보기</span>';dl.disabled=true;dataUrl='';
    st.textContent='텍스트를 입력하면 QR이 바로 만들어집니다';dot.className='dot';return;}
  try{
    var qr=qrcode(0,ecc.value);qr.addData(txt);qr.make();
    dataUrl=qr.createDataURL(parseInt(size.value,10),parseInt(margin.value,10));
    stage.innerHTML='';
    var img=document.createElement('img');img.src=dataUrl;img.alt='생성된 QR 코드';
    stage.appendChild(img);dl.disabled=false;
    st.textContent='생성 완료 — 다운로드해서 바로 쓰세요';dot.className='dot ready';
  }catch(e){
    stage.innerHTML='<span class="qr-empty">내용이 너무 깁니다 — 줄여 주세요</span>';dl.disabled=true;dataUrl='';
    st.textContent='QR 생성 실패: 내용이 최대 길이를 넘었어요';dot.className='dot warn';
  }
}
dl.addEventListener('click',function(){
  if(!dataUrl)return;
  var a=document.createElement('a');a.href=dataUrl;a.download='qrcode.png';
  document.body.appendChild(a);a.click();a.remove();
  st.textContent='다운로드했어요';
});
[inp,size,ecc,margin].forEach(function(el){el.addEventListener('input',render);el.addEventListener('change',render);});
})();
</script>""",
},

# ============================================================ 비밀번호 생성기
{
 'slug':'password','name':'비밀번호 생성기','cat':'life',
 'title':'강력한 비밀번호 생성기 무료 — 랜덤 암호 만들기 (싹싹김치)',
 'desc':'길이·문자 종류를 골라 안전한 랜덤 비밀번호를 한 번에 생성. 강도 측정, 복사까지. 브라우저 안에서만 생성되는 무료 비밀번호 생성기.',
 'og_title':'비밀번호 생성기 무료 — 싹싹김치',
 'og_desc':'안전한 랜덤 비밀번호 즉시 생성. 서버 전송 없이 브라우저에서.',
 'h1':'비밀번호 생성기','pen':'추측 불가능한 암호, 한 클릭에.',
 'pdesc':'길이와 문자 종류를 고르면 <b>암호학적 난수</b>로 안전한 비밀번호를 만듭니다. 생성된 암호는 이 창을 벗어나지 않습니다.',
 'css':"""
  .pw-out{display:flex;gap:10px;align-items:center;background:var(--bg2);border:1px solid var(--line);border-radius:16px;padding:16px 18px}
  .pw-out code{flex:1;font-family:Consolas,monospace;font-size:19px;font-weight:700;letter-spacing:.04em;word-break:break-all;min-height:28px}
  .pw-meter{height:8px;background:var(--bg2);border:1px solid var(--line);border-radius:99px;margin-top:14px;overflow:hidden}
  .pw-meter i{display:block;height:100%;width:0;border-radius:99px;background:var(--accent);transition:width .25s ease,background .25s ease}
  .pw-meter-label{display:flex;justify-content:space-between;font-size:12px;font-weight:700;color:var(--faint);margin-top:6px}
  .pw-opts{display:flex;gap:14px;flex-wrap:wrap;margin-top:18px}
  .pw-opt{display:flex;align-items:center;gap:7px;font-size:13.5px;font-weight:600;color:var(--muted);cursor:pointer;user-select:none}
  .pw-opt input{accent-color:var(--accent);width:16px;height:16px;cursor:pointer}
  .pw-len{display:flex;align-items:center;gap:12px;margin-top:18px}
  .pw-len input[type=range]{flex:1;accent-color:var(--accent)}
  .pw-len b{min-width:64px;text-align:right;font-size:15px}
  .tool-row{display:flex;gap:10px;align-items:center;margin-top:20px;flex-wrap:wrap}
 """,
 'body':"""      <div class="pw-out"><code id="pwOut">—</code>
        <button class="btn btn-ghost btn-sm" id="pwCopy">복사</button>
      </div>
      <div class="pw-meter"><i id="pwBar"></i></div>
      <div class="pw-meter-label"><span id="pwLabel">옵션을 고르고 생성을 눌러주세요</span><span id="pwBits"></span></div>
      <div class="pw-len">
        <span style="font-size:13px;font-weight:700;color:var(--faint)">길이</span>
        <input type="range" id="pwLen" min="4" max="64" value="20">
        <b id="pwLenV">20자</b>
      </div>
      <div class="pw-opts">
        <label class="pw-opt"><input type="checkbox" id="oUpper" checked> 대문자 A-Z</label>
        <label class="pw-opt"><input type="checkbox" id="oLower" checked> 소문자 a-z</label>
        <label class="pw-opt"><input type="checkbox" id="oDigit" checked> 숫자 0-9</label>
        <label class="pw-opt"><input type="checkbox" id="oSym" checked> 기호 !@#$%</label>
        <label class="pw-opt"><input type="checkbox" id="oAmbig"> 헷갈리는 문자 제외 (l1IO0)</label>
      </div>
      <div class="tool-row">
        <button class="btn btn-primary" id="pwGen">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 2l-2 2m-7.6 7.6a5.5 5.5 0 1 1-7.8 7.8 5.5 5.5 0 0 1 7.8-7.8Zm0 0L19 4m-3.5 3.5L18 10"/></svg>
          새 비밀번호 생성
        </button>
      </div>
      <div class="status-line"><span class="dot" id="dot"></span><span id="st">crypto.getRandomValues 기반 — 예측 불가능한 난수</span></div>""",
 'notice':[
   '생성된 비밀번호는 서버로 전송되지 않고 이 창 안에서만 존재합니다.',
   '16자 이상 + 문자 종류 3개 이상이면 대부분의 서비스에서 "매우 강력"으로 평가됩니다.',
   '사이트마다 다른 비밀번호를 쓰세요 — 하나가 유출돼도 다른 계정이 안전합니다.',
   "도구는 '있는 그대로' 제공됩니다. <a href=\"terms.html\">이용약관</a>",
 ],
 'script':"""<script>
(function(){
"use strict";
var out=document.getElementById('pwOut'),bar=document.getElementById('pwBar'),
    label=document.getElementById('pwLabel'),bits=document.getElementById('pwBits'),
    len=document.getElementById('pwLen'),lenV=document.getElementById('pwLenV'),
    gen=document.getElementById('pwGen'),cp=document.getElementById('pwCopy'),
    st=document.getElementById('st'),dot=document.getElementById('dot');
var U='ABCDEFGHJKLMNPQRSTUVWXYZ',Ua='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
var L='abcdefghijkmnpqrstuvwxyz',La='abcdefghijklmnopqrstuvwxyz';
var D='23456789',Da='0123456789';
var S='!@#$%^&*()-_=+[]{};:,.?/';
function pick(set){var a=new Uint32Array(1);crypto.getRandomValues(a);return set[a[0]%set.length];}
function make(){
  var pool='';
  if(document.getElementById('oUpper').checked)pool+=document.getElementById('oAmbig').checked?U:Ua;
  if(document.getElementById('oLower').checked)pool+=document.getElementById('oAmbig').checked?L:La;
  if(document.getElementById('oDigit').checked)pool+=document.getElementById('oAmbig').checked?D:Da;
  if(document.getElementById('oSym').checked)pool+=S;
  if(!pool){out.textContent='—';label.textContent='문자 종류를 하나 이상 고르세요';bar.style.width='0';bits.textContent='';return;}
  var n=parseInt(len.value,10),pw='';
  for(var i=0;i<n;i++)pw+=pick(pool);
  out.textContent=pw;
  var ent=Math.round(n*Math.log2(pool.length));
  bits.textContent='엔트로피 약 '+ent+'비트';
  var pct=Math.min(100,ent/128*100);
  bar.style.width=pct+'%';
  var lv=ent<40?'매우 약함':ent<60?'약함':ent<80?'보통':ent<110?'강함':'매우 강함';
  bar.style.background=ent<40?'#e85d2c':ent<60?'#f6863c':ent<80?'#c98f12':ent<110?'#5cb878':'#2f8f4e';
  label.textContent='강도: '+lv;
  st.textContent='생성 완료 — 복사해서 바로 쓰세요';dot.className='dot ready';
}
cp.addEventListener('click',function(){
  var t=out.textContent;if(t==='—'||!t){st.textContent='먼저 생성해 주세요';return;}
  var done=function(){st.textContent='클립보드에 복사했어요';};
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done).catch(done);}
  else{done();}
});
len.addEventListener('input',function(){lenV.textContent=len.value+'자';make();});
document.querySelectorAll('.pw-opt input').forEach(function(c){c.addEventListener('change',make);});
gen.addEventListener('click',make);
make();
})();
</script>""",
},

# ============================================================ 불량화소 체크
{
 'slug':'pixel-test','name':'불량화소 체크','cat':'screen',
 'title':'모니터 불량화소 테스트 무료 — 데드픽셀 검사 (싹싹김치)',
 'desc':'전체화면 단색으로 모니터 불량화소·빛샘을 검사. 검정·흰색·RGB 단색 화면을 순서대로 띄워 데드픽셀과 스턱픽셀을 찾는 무료 모니터 테스트.',
 'og_title':'모니터 불량화소 체크 무료 — 싹싹김치',
 'og_desc':'전체화면 단색 테스트로 데드픽셀·빛샘 검사. 브라우저에서 바로.',
 'h1':'불량화소 체크','pen':'새 모니터, 사자마자 점검하세요.',
 'pdesc':'모니터를 사거나 반품 기간이 얼마 안 남았을 때 — <b>단색 화면</b>을 띄워 안 켜지는 점(데드픽셀)과 안 꺼지는 점(스턱픽셀)을 확인하세요.',
 'css':"""
  .px-colors{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}
  .px-color{height:86px;border-radius:14px;border:1px solid var(--line);cursor:pointer;display:flex;align-items:flex-end;padding:10px;font-size:12px;font-weight:800;transition:transform .12s ease}
  .px-color:hover{transform:translateY(-2px)}
  .px-overlay{position:fixed;inset:0;z-index:9999;display:none;cursor:pointer}
  .px-overlay.on{display:block}
  .px-hint{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);background:rgba(0,0,0,.72);color:#fff;font-size:13px;font-weight:600;padding:9px 18px;border-radius:99px;pointer-events:none}
  .px-hint b{color:#9fe8b4}
  .tool-row{display:flex;gap:10px;align-items:center;margin-top:20px;flex-wrap:wrap}
 """,
 'body':"""      <div class="px-colors" id="pxColors"></div>
      <div class="tool-row">
        <button class="btn btn-primary" id="pxStart">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/></svg>
          전체화면 검사 시작
        </button>
      </div>
      <div class="status-line"><span class="dot ready" id="dot"></span><span id="st">시작 후 화면 클릭·→키로 색 변경, ESC로 종료</span></div>
      <div class="px-overlay" id="pxOv"><div class="px-hint" id="pxHint"></div></div>""",
 'notice':[
   '전체화면에서 <b>검정</b>: 안 꺼지는 점(스턱픽셀)·빛샘 확인. <b>흰색</b>: 안 켜지는 점(데드픽셀) 확인. RGB 단색에서 특정 색만 안 나오는 점도 찾을 수 있습니다.',
   '불량화소 기준은 제조사마다 다릅니다 — 보통 중앙부 1개·전체 3~5개 이상부터 무상 교환 대상입니다. 구매처 정책을 확인하세요.',
   '화면 클릭이나 ←→키로 색을 바꾸고, ESC(또는 전체화면 해제)로 종료합니다.',
   "도구는 '있는 그대로' 제공됩니다. <a href=\"terms.html\">이용약관</a>",
 ],
 'script':"""<script>
(function(){
"use strict";
var COLORS=[
 {n:'검정 (빛샘·스턱픽셀)',c:'#000000',t:'#999'},
 {n:'흰색 (데드픽셀)',c:'#ffffff',t:'#888'},
 {n:'빨강',c:'#e8281e',t:'#fff'},
 {n:'초록',c:'#1faf54',t:'#fff'},
 {n:'파랑',c:'#1f66e0',t:'#fff'},
 {n:'청록',c:'#1fb8c8',t:'#fff'},
 {n:'자홍',c:'#c838c8',t:'#fff'},
 {n:'노랑',c:'#f0d020',t:'#5a5000'}
];
var wrap=document.getElementById('pxColors'),ov=document.getElementById('pxOv'),hint=document.getElementById('pxHint');
var idx=0;
COLORS.forEach(function(col,i){
  var d=document.createElement('div');d.className='px-color';
  d.style.background=col.c;d.style.color=col.t;
  d.textContent=col.n.split(' ')[0];
  d.addEventListener('click',function(){open(i);});
  wrap.appendChild(d);
});
function show(){ov.style.background=COLORS[idx].c;
  hint.innerHTML='<b>'+COLORS[idx].n+'</b> · 클릭/←→ 색 변경 · ESC 종료';}
function open(i){idx=i;show();ov.classList.add('on');
  if(ov.requestFullscreen)ov.requestFullscreen().catch(function(){});}
function close(){ov.classList.remove('on');
  if(document.fullscreenElement)document.exitFullscreen().catch(function(){});}
document.getElementById('pxStart').addEventListener('click',function(){open(0);});
ov.addEventListener('click',function(){idx=(idx+1)%COLORS.length;show();});
document.addEventListener('keydown',function(e){
  if(!ov.classList.contains('on'))return;
  if(e.key==='ArrowRight'||e.key===' '){idx=(idx+1)%COLORS.length;show();e.preventDefault();}
  else if(e.key==='ArrowLeft'){idx=(idx-1+COLORS.length)%COLORS.length;show();}
});
document.addEventListener('fullscreenchange',function(){
  if(!document.fullscreenElement&&ov.classList.contains('on'))close();
});
})();
</script>""",
},
]
