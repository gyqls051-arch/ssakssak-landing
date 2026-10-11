# -*- coding: utf-8 -*-
# gen_pages.py 페이지 데이터 C — 퇴직금 / HEIC / 영상→GIF

PAGES = [
# ============================================================ 퇴직금 계산기
{
 'slug':'severance','name':'퇴직금 계산기','cat':'life',
 'title':'퇴직금 계산기 무료 — 예상 퇴직금·미사용 연차수당 (싹싹김치)',
 'desc':'입사일·퇴사일·최근 3개월 급여로 예상 퇴직금을 계산. 미사용 연차수당까지 함께. 근로기준법 평균임금 방식 무료 계산기.',
 'og_title':'퇴직금 계산기 무료 — 싹싹김치',
 'og_desc':'입퇴사일과 급여만 넣으면 예상 퇴직금 계산.',
 'h1':'퇴직금 계산기','pen':'내 퇴직금, 미리 계산해보기.',
 'pdesc':'입사일·퇴사일과 최근 3개월 급여를 넣으면 근로기준법 <b>평균임금 방식</b>으로 예상 퇴직금을 계산합니다. 미사용 연차수당도 같이 볼 수 있어요.',
 'css':"""
  .sv-grid{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start}
  .sv-field{margin-bottom:14px}
  .sv-field label{display:block;font-size:12.5px;font-weight:800;color:var(--faint);margin-bottom:7px}
  .sv-field input{width:100%;box-sizing:border-box;font-family:inherit;font-size:15px;font-weight:700;color:var(--ink);background:var(--bg2);border:1px solid var(--line);border-radius:12px;padding:11px 14px;outline:none}
  .sv-field input:focus{border-color:var(--accent)}
  .sv-result{background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:20px}
  .sv-big{font-size:40px;font-weight:900;letter-spacing:-.03em;color:var(--accent);line-height:1.15}
  .sv-big small{font-size:15px;font-weight:800;color:var(--faint)}
  .sv-rows{margin-top:14px;border-top:1px solid var(--line);padding-top:12px;display:flex;flex-direction:column;gap:8px}
  .sv-row{display:flex;justify-content:space-between;font-size:13.5px}
  .sv-row span{color:var(--muted);font-weight:600}
  .sv-row b{font-weight:800;font-variant-numeric:tabular-nums}
  .sv-note{font-size:11.5px;color:var(--faint);margin-top:12px;line-height:1.6}
  .sv-card{background:var(--bg2);border:1px solid var(--line);border-radius:18px;padding:20px;margin-top:26px}
  .sv-card h3{margin:0 0 12px;font-size:14.5px;font-weight:900}
  .sv-flex{display:flex;gap:10px;flex-wrap:wrap;align-items:flex-end}
  @media (max-width:700px){.sv-grid{grid-template-columns:1fr}}
 """,
 'body':"""      <div class="sv-grid">
        <div>
          <div class="sv-field"><label>입사일</label><input type="date" id="svIn"></div>
          <div class="sv-field"><label>퇴사일 (마지막 근무일)</label><input type="date" id="svOut"></div>
          <div class="sv-field"><label>최근 3개월 급여 합계 (세전, 만원)</label><input type="number" id="svPay" value="900" min="0"></div>
          <div class="sv-field"><label>연간 상여금 총액 (만원, 없으면 0)</label><input type="number" id="svBonus" value="0" min="0"></div>
          <div class="sv-field"><label>연차수당 등 기타 연간 수당 (만원, 없으면 0)</label><input type="number" id="svEtc" value="0" min="0"></div>
        </div>
        <div class="sv-result">
          <div style="font-size:12.5px;font-weight:800;color:var(--faint)">예상 퇴직금</div>
          <div class="sv-big" id="svNet">—</div>
          <div class="sv-rows" id="svRows"></div>
          <div class="sv-note">퇴직금 = 평균임금 × 30일 × (재직일수 ÷ 365). 평균임금 = 퇴사 전 3개월간 받은 임금총액 ÷ 그 기간의 총 일수. 상여·연차수당은 연간액의 3/12를 3개월 임금에 가산합니다.</div>
        </div>
      </div>

      <div class="sv-card">
        <h3>🌴 미사용 연차수당 계산</h3>
        <div class="sv-flex">
          <div class="sv-field" style="margin:0;flex:1;min-width:140px"><label>월 통상임금 (만원)</label><input type="number" id="alPay" value="300" min="0"></div>
          <div class="sv-field" style="margin:0;flex:1;min-width:120px"><label>미사용 연차 (일)</label><input type="number" id="alDays" value="10" min="0" max="50"></div>
        </div>
        <div class="sv-rows" id="alRows"></div>
      </div>
      <div class="status-line"><span class="dot ready" id="dot"></span><span id="st">재직 1년 이상부터 퇴직금이 발생합니다</span></div>""",
 'notice':[
   '퇴직금은 <b>계속근로 1년 이상</b> + 4주 평균 주 15시간 이상 근무 시 발생합니다. 1년 미만이면 퇴직금이 없습니다.',
   '평균임금이 통상임금보다 낮으면 통상임금으로 계산합니다 — 이 계산기는 평균임금 기준 근사치입니다.',
   '3개월 일수는 실제 달력 일수(89~92일)로 계산합니다. 퇴직소득세는 별도라 세전 금액입니다.',
   "도구는 '있는 그대로' 제공됩니다. <a href=\"terms.html\">이용약관</a>",
 ],
 'script':"""<script>
(function(){
"use strict";
var din=document.getElementById('svIn'),dout=document.getElementById('svOut'),
    pay=document.getElementById('svPay'),bonus=document.getElementById('svBonus'),etc=document.getElementById('svEtc'),
    net=document.getElementById('svNet'),rows=document.getElementById('svRows'),
    alPay=document.getElementById('alPay'),alDays=document.getElementById('alDays'),alRows=document.getElementById('alRows');
function won(n){return Math.round(n).toLocaleString('ko-KR');}
function calc(){
  if(!din.value||!dout.value){net.textContent='—';rows.innerHTML='';return;}
  var a=din.value.split('-'),b=dout.value.split('-');
  var d1=new Date(+a[0],+a[1]-1,+a[2]),d2=new Date(+b[0],+b[1]-1,+b[2]);
  var days=Math.round((d2-d1)/86400000)+1;
  if(days<=0){net.textContent='—';rows.innerHTML='<div class="sv-row"><span>퇴사일이 입사일보다 빠릅니다</span></div>';return;}
  // 3개월 기간 실 일수: 퇴사일 전날까지 3개월
  var d3s=new Date(d2.getFullYear(),d2.getMonth()-3,d2.getDate()+1);
  var span3=Math.round((new Date(d2.getFullYear(),d2.getMonth(),d2.getDate()+1)-d3s)/86400000);
  var p3=(parseFloat(pay.value)||0);          // 3개월 급여 (만원)
  var bn=(parseFloat(bonus.value)||0)*3/12;   // 상여 3/12
  var et=(parseFloat(etc.value)||0)*3/12;     // 기타 3/12
  var total3=p3+bn+et;                        // 3개월 임금총액 (만원)
  var avg=total3/span3;                       // 1일 평균임금 (만원)
  var sev=avg*30*(days/365);
  if(days<365){
    net.innerHTML='발생 안 함';
    rows.innerHTML='<div class="sv-row"><span>재직일수</span><b>'+days+'일 (1년 미만)</b></div>'+
      '<div class="sv-row"><span>계속근로 1년 이상부터 퇴직금이 발생합니다</span></div>';
    return;
  }
  net.innerHTML='약 '+won(sev)+'<small> 만원</small>';
  var r='';
  r+='<div class="sl-row sv-row"><span>재직일수</span><b>'+days.toLocaleString()+'일 (약 '+(days/365).toFixed(1)+'년)</b></div>';
  r+='<div class="sv-row"><span>3개월 임금총액</span><b>'+won(total3)+'만</b></div>';
  r+='<div class="sv-row"><span>1일 평균임금</span><b>'+won(avg)+'만</b></div>';
  r+='<div class="sv-row"><span>계산식</span><b>'+won(avg)+'×30×'+days+'/365</b></div>';
  rows.innerHTML=r;
}
function alCalc(){
  var p=parseFloat(alPay.value)||0, d=parseFloat(alDays.value)||0;
  var hourly=p/209;                            // 통상시급 (만원) — 월 209시간 기준
  var daily=hourly*8;
  var amt=daily*d;
  alRows.innerHTML='<div class="sv-row"><span>1일 통상임금 (월 '+won(p)+'만 ÷ 209h × 8h)</span><b>'+won(daily)+'만</b></div>'+
    '<div class="sv-row"><span>미사용 연차수당 '+d+'일</span><b style="color:var(--accent)">약 '+won(amt)+'만</b></div>';
}
[din,dout,pay,bonus,etc].forEach(function(el){el.addEventListener('input',calc);el.addEventListener('change',calc);});
[alPay,alDays].forEach(function(el){el.addEventListener('input',alCalc);});
alCalc();
})();
</script>""",
},

# ============================================================ HEIC 변환
{
 'slug':'heic','name':'HEIC 변환','cat':'screen',
 'title':'HEIC JPG 변환 무료 — 아이폰 사진 변환 (싹싹김치)',
 'desc':'아이폰 HEIC 사진을 JPG·PNG·WebP로 즉시 변환. 여러 장 일괄 변환 지원. 서버 업로드 없이 브라우저에서 100% 처리되는 무료 HEIC 변환기.',
 'og_title':'HEIC→JPG 변환 무료 — 싹싹김치',
 'og_desc':'아이폰 사진이 안 열릴 때. 브라우저에서 바로 JPG로.',
 'h1':'HEIC 변환','pen':'아이폰 사진, 윈도우에서도 열리게.',
 'pdesc':'아이폰에서 옮긴 <b>HEIC 사진</b>이 윈도우에서 안 열릴 때 — JPG·PNG·WebP로 바꿔드립니다. 사진은 서버에 올라가지 않고 이 창 안에서만 변환됩니다.',
 'extra_head':'<script defer src="js/vendor/heic2any.min.js"></script>',
 'css':"""
  .drop{border:2px dashed var(--line);border-radius:18px;padding:38px 20px;text-align:center;color:var(--muted);font-weight:700;font-size:14px;cursor:pointer;transition:all .15s ease;background:var(--bg2)}
  .drop:hover,.drop.over{border-color:var(--accent);background:var(--soft);color:var(--accent)}
  .drop b{color:var(--accent)}
  .flist{margin-top:18px;display:flex;flex-direction:column;gap:10px}
  .fitem{display:flex;align-items:center;gap:14px;background:var(--bg2);border:1px solid var(--line);border-radius:14px;padding:10px 14px}
  .fitem img{width:52px;height:52px;object-fit:cover;border-radius:9px;flex:none}
  .fitem .nm{flex:1;min-width:0;font-size:13.5px;font-weight:700;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
  .fitem .sub{font-size:11.5px;color:var(--faint);font-weight:600;margin-top:2px}
  .fitem .act{flex:none}
  .fitem .err{color:var(--accent);font-size:12px;font-weight:700}
  .tool-row{display:flex;gap:10px;align-items:center;margin-top:18px;flex-wrap:wrap}
  .heic-opts{display:flex;gap:16px;flex-wrap:wrap;margin-top:16px;align-items:center}
  .heic-opt{display:flex;align-items:center;gap:8px;font-size:12.5px;font-weight:700;color:var(--faint)}
  .heic-opt select{font-family:inherit;font-size:13.5px;font-weight:600;color:var(--ink);background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:8px 12px;outline:none}
 """,
 'body':"""      <div class="drop" id="drop">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom:8px"><rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="9" cy="9" r="2"/><path d="m21 15-4.5-4.5L6 21"/></svg>
        <div><b>HEIC 파일</b>을 끌어놓거나 클릭해서 선택하세요</div>
        <div style="font-size:12px;font-weight:600;color:var(--faint);margin-top:4px">아이폰에서 옮긴 .heic / .heif — 여러 장 가능</div>
      </div>
      <input type="file" id="fi" accept=".heic,.heif,image/heic,image/heif" multiple hidden>
      <div class="heic-opts">
        <label class="heic-opt">변환 형식
          <select id="heicFmt"><option value="image/jpeg" selected>JPG</option><option value="image/png">PNG</option><option value="image/webp">WebP</option></select>
        </label>
        <label class="heic-opt">품질
          <select id="heicQ"><option value="0.8">80%</option><option value="0.92" selected>92%</option><option value="1">100%</option></select>
        </label>
      </div>
      <div class="flist" id="flist"></div>
      <div class="status-line"><span class="dot" id="dot"></span><span id="st">HEIC 파일을 넣어주세요</span></div>""",
 'notice':[
   '사진은 서버에 업로드되지 않고 브라우저 안에서만 변환됩니다 — 개인 사진도 안심하고 변환하세요.',
   '아이폰에서 <b>설정 → 카메라 → 포맷 → 높은 호환성</b>으로 바꾸면 앞으로 찍는 사진은 처음부터 JPG로 저장됩니다.',
   '일부 HEIC(연사·버스트 등 다중 이미지)는 첫 장만 변환되거나 실패할 수 있습니다.',
   "도구는 '있는 그대로' 제공됩니다. <a href=\"terms.html\">이용약관</a>",
 ],
 'script':"""<script>
(function(){
"use strict";
var drop=document.getElementById('drop'),fi=document.getElementById('fi'),
    list=document.getElementById('flist'),fmt=document.getElementById('heicFmt'),q=document.getElementById('heicQ'),
    st=document.getElementById('st'),dot=document.getElementById('dot');
var busy=0;
function ext(){return fmt.value==='image/png'?'png':fmt.value==='image/webp'?'webp':'jpg';}
function setSt(msg,cls){st.textContent=msg;dot.className='dot'+(cls?' '+cls:'');}
function addFiles(files){
  var arr=[].slice.call(files).filter(function(f){
    return /\\.hei[cf]$/i.test(f.name)||f.type==='image/heic'||f.type==='image/heif';
  });
  if(!arr.length){setSt('HEIC/HEIF 파일만 넣어주세요','warn');return;}
  arr.forEach(convert);
}
function convert(file){
  var it=document.createElement('div');it.className='fitem';
  it.innerHTML='<div style="width:52px;height:52px;border-radius:9px;background:var(--line);flex:none;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:800;color:var(--faint)">HEIC</div>'+
    '<div class="nm">'+file.name+'<div class="sub">변환 중…</div></div>';
  list.appendChild(it);busy++;
  setSt('변환 중… ('+busy+'개 진행)');
  heic2any({blob:file,toType:fmt.value,quality:parseFloat(q.value)}).then(function(out){
    var blob=Array.isArray(out)?out[0]:out;
    var url=URL.createObjectURL(blob);
    var base=file.name.replace(/\\.[^.]+$/,'')+'.'+ext();
    it.innerHTML='<img src="'+url+'" alt=""><div class="nm">'+base+
      '<div class="sub">'+file.name+' → '+base+' · '+(blob.size/1024).toFixed(0)+'KB</div></div>'+
      '<a class="btn btn-primary btn-sm act" href="'+url+'" download="'+base+'">다운로드</a>';
    done();
  }).catch(function(e){
    it.innerHTML='<div style="width:52px;height:52px;border-radius:9px;background:var(--chip-o);flex:none"></div>'+
      '<div class="nm">'+file.name+'<div class="sub err">변환 실패 — 지원하지 않는 HEIC 형식일 수 있어요</div></div>';
    done();
  });
}
function done(){busy--;
  if(busy<=0)setSt('완료 — 다운로드 버튼으로 저장하세요','ready');}
drop.addEventListener('click',function(){fi.click();});
fi.addEventListener('change',function(){addFiles(fi.files);fi.value='';});
['dragover','dragenter'].forEach(function(ev){drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.add('over');});});
['dragleave','drop'].forEach(function(ev){drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.remove('over');});});
drop.addEventListener('drop',function(e){addFiles(e.dataTransfer.files);});
})();
</script>""",
},

# ============================================================ 영상→GIF
{
 'slug':'video-gif','name':'영상→GIF','cat':'video',
 'title':'동영상 GIF 변환 무료 — 움짤 만들기 (싹싹김치)',
 'desc':'MP4·웹엠 영상을 GIF 움짤로 변환. 시작점·길이·크기·FPS 조절 후 프레임 캡처 방식으로 변환. 서버 업로드 없이 브라우저에서 처리되는 무료 GIF 메이커.',
 'og_title':'동영상→GIF 변환 무료 — 싹싹김치',
 'og_desc':'영상 구간을 골라 움짤로. 업로드 없이 브라우저에서.',
 'h1':'영상→GIF','pen':'밈 만들기, 여기서 끝.',
 'pdesc':'짧은 영상 구간을 골라 <b>GIF 움짤</b>로 만듭니다. 파일이 서버로 가지 않고 이 창에서 프레임을 캡처해 인코딩하니 큰 파일도 안심하고 넣으세요.',
 'extra_head':'<script src="js/vendor/gif.js"></script>',
 'css':"""
  .gv-grid{display:grid;grid-template-columns:1.2fr 1fr;gap:24px;align-items:start}
  .gv-video{width:100%;border-radius:14px;background:#000;max-height:300px}
  .gv-field{margin-bottom:12px}
  .gv-field label{display:block;font-size:12px;font-weight:800;color:var(--faint);margin-bottom:6px}
  .gv-field input[type=number],.gv-field select{width:100%;box-sizing:border-box;font-family:inherit;font-size:14px;font-weight:700;color:var(--ink);background:var(--bg2);border:1px solid var(--line);border-radius:10px;padding:9px 12px;outline:none}
  .gv-2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .gv-bar{height:10px;background:var(--bg2);border:1px solid var(--line);border-radius:99px;overflow:hidden;margin-top:14px}
  .gv-bar i{display:block;height:100%;width:0;background:var(--accent);transition:width .2s ease}
  .gv-out{margin-top:16px;text-align:center}
  .gv-out img{max-width:100%;border-radius:14px;border:1px solid var(--line)}
  .drop{border:2px dashed var(--line);border-radius:18px;padding:30px 20px;text-align:center;color:var(--muted);font-weight:700;font-size:14px;cursor:pointer;transition:all .15s ease;background:var(--bg2);margin-bottom:18px}
  .drop:hover,.drop.over{border-color:var(--accent);background:var(--soft);color:var(--accent)}
  .drop b{color:var(--accent)}
  .tool-row{display:flex;gap:10px;align-items:center;margin-top:14px;flex-wrap:wrap}
  @media (max-width:700px){.gv-grid{grid-template-columns:1fr}}
 """,
 'body':"""      <div class="drop" id="drop"><b>영상 파일</b>을 끌어놓거나 클릭해서 선택하세요<div style="font-size:12px;font-weight:600;color:var(--faint);margin-top:4px">MP4·WebM·MOV(브라우저 재생 가능한 것) — 최대 10초 구간</div></div>
      <input type="file" id="fi" accept="video/*" hidden>
      <div class="gv-grid" id="gvGrid" style="display:none">
        <div>
          <video class="gv-video" id="vid" controls muted playsinline></video>
          <div class="gv-bar"><i id="bar"></i></div>
          <div class="gv-out" id="gvOut"></div>
        </div>
        <div>
          <div class="gv-2">
            <div class="gv-field"><label>시작 (초)</label><input type="number" id="gStart" value="0" min="0" step="0.1"></div>
            <div class="gv-field"><label>길이 (초, 최대 10)</label><input type="number" id="gLen" value="3" min="0.5" max="10" step="0.5"></div>
          </div>
          <div class="gv-2">
            <div class="gv-field"><label>가로 크기</label><select id="gW"><option value="320">320px</option><option value="480" selected>480px</option><option value="640">640px</option></select></div>
            <div class="gv-field"><label>프레임 (fps)</label><select id="gF"><option value="10">10</option><option value="15" selected>15</option><option value="24">24</option></select></div>
          </div>
          <div class="gv-field"><label>품질 (낮을수록 고화질·대용량)</label><select id="gQ"><option value="10" selected>보통</option><option value="5">좋음</option><option value="20">작은 용량</option></select></div>
          <div class="tool-row">
            <button class="btn btn-primary" id="gGo">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l2.5 6L21 11l-5.5 2L13 19l-2.5-6L5 11l5.5-2z"/></svg>
              GIF로 변환
            </button>
          </div>
        </div>
      </div>
      <div class="status-line"><span class="dot" id="dot"></span><span id="st">영상을 넣어주세요</span></div>""",
 'notice':[
   '영상은 서버에 업로드되지 않고 브라우저 안에서 프레임을 캡처해 GIF로 인코딩합니다.',
   'GIF는 길수록·클수록 용량이 기하급수로 커집니다 — 3초·480px·15fps면 보통 3~8MB입니다.',
   '소리는 GIF에 담기지 않습니다. 변환 시간은 구간 길이의 2~5배 정도 걸립니다.',
   "도구는 '있는 그대로' 제공됩니다. <a href=\"terms.html\">이용약관</a>",
 ],
 'script':"""<script>
(function(){
"use strict";
var drop=document.getElementById('drop'),fi=document.getElementById('fi'),vid=document.getElementById('vid'),
    grid=document.getElementById('gvGrid'),go=document.getElementById('gGo'),bar=document.getElementById('bar'),
    out=document.getElementById('gvOut'),st=document.getElementById('st'),dot=document.getElementById('dot');
var url=null,busy=false;
function setSt(msg,cls){st.textContent=msg;dot.className='dot'+(cls?' '+cls:'');}
function load(file){
  if(!file||file.type.indexOf('video/')!==0){setSt('영상 파일을 넣어주세요','warn');return;}
  if(url)URL.revokeObjectURL(url);
  url=URL.createObjectURL(file);vid.src=url;
  grid.style.display='';out.innerHTML='';
  setSt('준비 완료 — 구간을 고르고 변환을 눌러주세요','ready');
}
drop.addEventListener('click',function(){fi.click();});
fi.addEventListener('change',function(){load(fi.files[0]);fi.value='';});
['dragover','dragenter'].forEach(function(ev){drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.add('over');});});
['dragleave','drop'].forEach(function(ev){drop.addEventListener(ev,function(e){e.preventDefault();drop.classList.remove('over');});});
drop.addEventListener('drop',function(e){load(e.dataTransfer.files[0]);});
function seek(t){return new Promise(function(res,rej){
  var to=setTimeout(function(){rej(new Error('seek timeout'));},8000);
  vid.onseeked=function(){clearTimeout(to);res();};
  vid.currentTime=t;
});}
go.addEventListener('click',async function(){
  if(busy||!vid.src)return;
  if(!isFinite(vid.duration)){setSt('영상을 재생할 수 없습니다','warn');return;}
  busy=true;go.disabled=true;out.innerHTML='';
  var start=Math.max(0,parseFloat(document.getElementById('gStart').value)||0);
  var len=Math.min(10,Math.max(0.5,parseFloat(document.getElementById('gLen').value)||3));
  var W=parseInt(document.getElementById('gW').value,10);
  var fps=parseInt(document.getElementById('gF').value,10);
  var qual=parseInt(document.getElementById('gQ').value,10);
  if(start>=vid.duration){setSt('시작 지점이 영상 길이를 넘었어요','warn');busy=false;go.disabled=false;return;}
  len=Math.min(len,vid.duration-start);
  var H=Math.round(W*vid.videoHeight/vid.videoWidth);
  var cv=document.createElement('canvas');cv.width=W;cv.height=H;
  var cx=cv.getContext('2d');
  var gif=new GIF({workers:2,quality:qual,width:W,height:H,workerScript:'js/vendor/gif.worker.js'});
  var frames=Math.max(1,Math.round(len*fps)),delay=Math.round(1000/fps);
  try{
    vid.pause();
    for(var i=0;i<frames;i++){
      await seek(Math.min(start+i/fps,vid.duration-0.05));
      cx.drawImage(vid,0,0,W,H);
      gif.addFrame(cx,{copy:true,delay:delay});
      bar.style.width=Math.round((i+1)/frames*50)+'%';
      setSt('프레임 캡처 중… '+(i+1)+'/'+frames);
    }
  }catch(e){
    setSt('캡처 실패: 영상 형식이 맞지 않을 수 있어요','warn');
    busy=false;go.disabled=false;bar.style.width='0';return;
  }
  gif.on('progress',function(p){
    bar.style.width=(50+Math.round(p*50))+'%';
    setSt('GIF 인코딩 중… '+Math.round(p*100)+'%');
  });
  gif.on('finished',function(blob){
    var u=URL.createObjectURL(blob);
    out.innerHTML='<img src="'+u+'" alt="생성된 GIF"><div class="tool-row" style="justify-content:center">'+
      '<a class="btn btn-primary" href="'+u+'" download="ssak-gif.gif">GIF 다운로드 ('+(blob.size/1048576).toFixed(1)+'MB)</a></div>';
    bar.style.width='100%';
    setSt('완성! 마음에 들 때까지 옵션 바꿔 다시 만들 수 있어요','ready');
    busy=false;go.disabled=false;
  });
  gif.render();
});
})();
</script>""",
},
]
