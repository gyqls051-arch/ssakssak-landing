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
        setOpen(!dd.classList.contains('open'));
      });

      // 호버로 열고, 벗어나도 350ms 유예 후에 닫기 (틈 지나갈 때 바로 안 사라지게)
      if(canHover){
        var closeTimer=null;
        dd.addEventListener('mouseenter',function(){
          if(closeTimer){ clearTimeout(closeTimer); closeTimer=null; }
          setOpen(true);
        });
        dd.addEventListener('mouseleave',function(){
          closeTimer=setTimeout(function(){ setOpen(false); closeTimer=null; },350);
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
