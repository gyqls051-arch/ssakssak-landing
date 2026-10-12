// 싹싹김치 공용 스크립트 — 내비 드롭다운(자료실 하위 카테고리)
(function(){
  function init(){
    var dds=document.querySelectorAll('.dd');
    if(!dds.length) return;

    var canHover=window.matchMedia&&window.matchMedia('(hover:hover) and (pointer:fine)').matches;

    dds.forEach(function(dd){
      var btn=dd.querySelector('.dd-btn');
      if(!btn) return;

      function setOpen(open){
        dd.classList.toggle('open',open);
        btn.setAttribute('aria-expanded',open?'true':'false');
      }

      btn.addEventListener('click',function(e){
        e.preventDefault();
        // 마우스 환경: 클릭 = 그 드롭다운의 '한눈에 보기' 링크로 이동 (메뉴는 호버로 열림)
        // 터치 환경: 첫 탭 = 메뉴 열기
        if(canHover){
          var all=dd.querySelector('.dd-all');
          window.location.href=all?all.getAttribute('href'):'archive.html';
          return;
        }
        setOpen(!dd.classList.contains('open'));
      });

      // 호버로 열기 — 다른 메뉴는 즉시 닫고(겹침 방지), 벗어나면 짧은 유예 후 닫기
      if(canHover){
        var closeTimer=null;
        dd.addEventListener('mouseenter',function(){
          dds.forEach(function(other){
            if(other!==dd && other.classList.contains('open')){
              other.classList.remove('open');
              var ob=other.querySelector('.dd-btn');
              if(ob) ob.setAttribute('aria-expanded','false');
            }
          });
          if(closeTimer){ clearTimeout(closeTimer); closeTimer=null; }
          setOpen(true);
        });
        dd.addEventListener('mouseleave',function(){
          closeTimer=setTimeout(function(){ setOpen(false); closeTimer=null; },160);
        });
      }
    });

    // 바깥 클릭으로 닫기
    document.addEventListener('click',function(e){
      document.querySelectorAll('.dd.open').forEach(function(dd){
        if(!dd.contains(e.target)){
          dd.classList.remove('open');
          var b=dd.querySelector('.dd-btn');
          if(b) b.setAttribute('aria-expanded','false');
        }
      });
    });

    // ESC로 닫기
    document.addEventListener('keydown',function(e){
      if(e.key!=='Escape') return;
      document.querySelectorAll('.dd.open').forEach(function(dd){
        dd.classList.remove('open');
        var b=dd.querySelector('.dd-btn');
        if(b){ b.setAttribute('aria-expanded','false'); b.focus(); }
      });
    });
  }
  if(document.readyState==='loading'){ document.addEventListener('DOMContentLoaded',init); }
  else{ init(); }
})();
