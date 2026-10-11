# -*- coding: utf-8 -*-
# 싹싹김치 웹도구 페이지 생성기 — python tools/gen_pages.py
# 새 도구 페이지를 공통 템플릿으로 생성한다. 생성 후 archive/index/nav/thumbs도 갱신해야 함.
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATS = {
    'video':  ('cat-video',  '영상 도구',  '#cat-video'),
    'doc':    ('cat-doc',    '문서 도구',  '#cat-doc'),
    'screen': ('cat-screen', '화면 도구',  '#cat-screen'),
    'life':   ('cat-life',   '생활 도구',  '#cat-life'),
}
CAT_ICONS = {
    'video':  '<rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/>',
    'doc':    '<path d="M14 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7l-5-5Z"/><path d="M14 2v5h5"/>',
    'screen': '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M12 17v4M8 21h8"/>',
    'life':   '<path d="M12 20.5S4.5 15.5 2.8 10.6C1.6 7.2 3.6 4.5 6.6 4.5c2.2 0 3.9 1.2 5.4 3.4 1.5-2.2 3.2-3.4 5.4-3.4 3 0 5 2.7 3.8 6.1C19.5 15.5 12 20.5 12 20.5Z"/>',
}

HEAD = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>@@TITLE@@</title>
<meta name="description" content="@@DESC@@">
<meta name="theme-color" content="#faf7f1">
<link rel="canonical" href="https://www.ssakkimchi.com/@@SLUG@@.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="싹싹김치">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="@@OGT@@">
<meta property="og:description" content="@@OGD@@">
<meta property="og:url" content="https://www.ssakkimchi.com/@@SLUG@@.html">
<meta property="og:image" content="https://www.ssakkimchi.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"WebApplication","name":"싹싹김치 @@PNAME@@","url":"https://www.ssakkimchi.com/@@SLUG@@.html","image":"https://www.ssakkimchi.com/og-image.png","description":"@@DESC@@","applicationCategory":"UtilitiesApplication","operatingSystem":"Web","inLanguage":"ko","offers":{"@type":"Offer","price":"0","priceCurrency":"KRW"},"publisher":{"@type":"Organization","name":"싹싹김치","url":"https://www.ssakkimchi.com/"}}
</script>
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"자료실","item":"https://www.ssakkimchi.com/archive.html"},{"@type":"ListItem","position":2,"name":"@@CATNAME@@","item":"https://www.ssakkimchi.com/archive.html@@CATANCHOR@@"},{"@type":"ListItem","position":3,"name":"@@PNAME@@"}]}
</script>
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🥬</text></svg>">
<link rel="preconnect" href="https://cdn.jsdelivr.net">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Nanum+Pen+Script&display=swap">
<link rel="stylesheet" href="ssak.css">
<script>
  (function(){
    var KEY='ssak-theme', root=document.documentElement;
    try{
      var saved=localStorage.getItem(KEY);
      if(saved==='dark'||saved==='light'){ root.setAttribute('data-theme',saved); }
      else if(window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches){ root.setAttribute('data-theme','dark'); }
      else { root.setAttribute('data-theme','light'); }
    }catch(e){ root.setAttribute('data-theme','light'); }
    window.toggleTheme=function(){
      var cur=root.getAttribute('data-theme')==='dark'?'dark':'light';
      var next=cur==='dark'?'light':'dark';
      root.setAttribute('data-theme',next);
      try{ localStorage.setItem(KEY,next); }catch(e){}
    };
  })();
</script>
<script defer src="ssak.js"></script>
@@EXTRAHEAD@@
<style>
  .tool{background:var(--card);border:1px solid var(--line);border-radius:28px;padding:30px;margin-top:26px;box-shadow:0 14px 40px var(--shadow)}
  .status-line{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:600;color:var(--muted);margin-top:16px;min-height:20px}
  .dot{width:8px;height:8px;border-radius:50%;background:var(--faint);flex:none}
  .dot.ready{background:var(--green)}
  .dot.warn{background:var(--accent)}
@@CSS@@
  @media (max-width:620px){.tool{padding:22px 16px}}
</style>
</head>
<body>
"""

NAV = """  <nav class="nav">
    <div class="nav-in">
      <a href="index.html" class="brand"><span class="brand-mark">🥬</span>싹싹김치<span class="brand-beta">BETA</span></a>
      <div class="nav-links">
        <div class="dd">
          <button class="navlink dd-btn" aria-haspopup="true" aria-expanded="false">자료실
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
          </button>
          <div class="dd-menu" aria-label="자료실 카테고리">
            <div class="dd-group">
              <div class="dd-label c-video"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2.5"/><path d="M7 4v16M17 4v16M3 9h4M3 15h4M17 9h4M17 15h4"/></svg>영상 도구</div>
              <a class="dd-item" href="video-downloader.html"><b>비디오 다운로더</b><span>1800+ 사이트 영상 저장</span></a>
              <a class="dd-item" href="player.html"><b>플레이어</b><span>가볍고 빠른 동영상 재생</span></a>
              <a class="dd-item" href="compressor.html"><b>비디오 압축기</b><span>카톡·디스코드 용량 맞춤</span></a>
              <a class="dd-item" href="thumbnail.html"><b>썸네일 추출기</b><span>유튜브 썸네일 원본 화질</span></a>
              <a class="dd-item" href="video-gif.html"><b>영상→GIF</b><span>움짤 만들기</span></a>
            </div>
            <div class="dd-group">
              <div class="dd-label c-doc"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H7a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7l-5-5Z"/><path d="M14 2v5h5"/></svg>문서 도구</div>
              <a class="dd-item" href="hangeul-viewer.html"><b>한글뷰어</b><span>HWP·PDF·오피스 한 창에서</span></a>
              <a class="dd-item" href="hwp-pdf.html"><b>한글→PDF 변환</b><span>설치 없이 브라우저에서</span></a>
              <a class="dd-item" href="pdf.html"><b>PDF 도구</b><span>합치기·분할·압축·이미지</span></a>
              <a class="dd-item" href="text-tools.html"><b>텍스트 도구</b><span>글자수·정렬·중복 제거</span></a>
            </div>
            <div class="dd-group">
              <div class="dd-label c-screen"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="13" rx="2"/><path d="M12 17v4M8 21h8"/></svg>화면 도구</div>
              <a class="dd-item" href="capture.html"><b>캡처</b><span>캡처·녹화·GIF·OCR</span></a>
              <a class="dd-item" href="image-tools.html"><b>이미지 도구</b><span>변환·리사이즈·압축</span></a>
              <a class="dd-item" href="heic.html"><b>HEIC 변환</b><span>아이폰 사진 JPG로</span></a>
              <a class="dd-item" href="pixel-test.html"><b>불량화소 체크</b><span>모니터 점 검사</span></a>
              <a class="dd-item" href="input-test.html"><b>키보드·마우스 테스트</b><span>입력기기 점검</span></a>
            </div>
            <div class="dd-group">
              <div class="dd-label c-life"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20.5S4.5 15.5 2.8 10.6C1.6 7.2 3.6 4.5 6.6 4.5c2.2 0 3.9 1.2 5.4 3.4 1.5-2.2 3.2-3.4 5.4-3.4 3 0 5 2.7 3.8 6.1C19.5 15.5 12 20.5 12 20.5Z"/></svg>생활 도구</div>
              <a class="dd-item" href="qr.html"><b>QR 생성기</b><span>링크·와이파이 QR</span></a>
              <a class="dd-item" href="password.html"><b>비밀번호 생성기</b><span>강력한 랜덤 암호</span></a>
              <a class="dd-item" href="dday.html"><b>디데이 계산기</b><span>날짜·기념일 계산</span></a>
              <a class="dd-item" href="salary.html"><b>실수령액 계산기</b><span>월급에서 얼마나 빠지나</span></a>
              <a class="dd-item" href="severance.html"><b>퇴직금 계산기</b><span>예상 퇴직금·연차수당</span></a>
            </div>
            <a class="dd-all" href="archive.html">자료실 한눈에 보기 →</a>
          </div>
        </div>

        <a class="navlink nav-hide-m" href="archive.html#install">설치 방법</a>
        <a class="navlink nav-hide-m" href="terms.html">이용약관</a>
        <button class="theme-btn" onclick="toggleTheme()" aria-label="테마 전환">
          <span class="theme-icon-sun"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.5M12 19.5V22M4.2 4.2l1.8 1.8M18 18l1.8 1.8M2 12h2.5M19.5 12H22M4.2 19.8l1.8-1.8M18 6l1.8-1.8"/></svg></span>
          <span class="theme-icon-moon"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8 8 0 1 1 9.5 4 6.3 6.3 0 0 0 20 14.5Z"/></svg></span>
        </button>
      </div>
    </div>
  </nav>
"""

FOOT = """
    <a class="back" href="archive.html">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 12H5m0 0 6-6m-6 6 6 6"/></svg>
      자료실로 돌아가기
    </a>
  </main>

  <footer>
    <div class="foot-brand"><span class="foot-mark">🥬</span>싹싹김치</div>
    <div class="foot-tag">무료 유틸리티를 만드는 브랜드</div>
    <div class="foot-beta">🚧 지금은 <b>베타</b>예요 — 사이트도 프로그램도 계속 다듬는 중입니다. 오류나 아쉬운 점은 언제든 알려주세요.</div>
    <div class="foot-links">
      <a class="foot-link" href="archive.html">자료실</a>
      <span>·</span>
      <a class="foot-link" href="terms.html">이용약관·면책</a>
      <span>·</span>
      <a class="foot-link" href="https://github.com/gyqls051-arch/ssakssak-downloader/issues" target="_blank" rel="noopener">문의 (GitHub Issues)</a>
    </div>
  </footer>
"""

CHEVRON = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 5 7 7-7 7"/></svg>'
BACKSVG = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--muted)" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9.2"/><path d="M12 8h.01M11 12h1v4h1"/></svg>'


def render(p):
    cat_cls, cat_name, cat_anchor = CATS[p['cat']]
    icon = CAT_ICONS[p['cat']]
    h = HEAD
    for k, v in [
        ('TITLE', p['title']), ('DESC', p['desc']), ('SLUG', p['slug']),
        ('OGT', p['og_title']), ('OGD', p['og_desc']), ('PNAME', p['name']),
        ('CATNAME', cat_name), ('CATANCHOR', cat_anchor),
        ('EXTRAHEAD', p.get('extra_head', '')),
        ('CSS', p.get('css', '')),
    ]:
        h = h.replace('@@'+k+'@@', v)
    notices = '\n'.join('        <li>%s</li>' % n for n in p['notice'])
    body = """
  <main class="wrap">

    <nav class="crumb" aria-label="현재 위치">
      <a href="archive.html">자료실</a>
      @@CHEV@@
      <a href="archive.html@@CATANCHOR@@">@@CATNAME@@</a>
      @@CHEV@@
      <span class="here">@@PNAME@@</span>
    </nav>

    <header class="prod-hero">
      <div class="prod-hero-main">
        <div class="prod-chips">
          <span class="cat-chip @@CATCLS@@">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">@@ICON@@</svg>
            @@CATNAME@@
          </span>
          <span class="live-chip">설치 없이 바로 사용</span>
        </div>
        <h1>@@H1@@</h1>
        <span class="pen" style="color:var(--green-ink)">@@PEN@@</span>
        <p class="desc">@@PDESC@@</p>
      </div>
      <img class="prod-hero-img" src="img/hero-@@SLUG@@.webp" width="1100" height="730" alt="@@PNAME@@ 화면 미리보기" fetchpriority="high">
    </header>

    <section class="tool">
@@BODY@@
    </section>

    <section class="notice">
      <div class="notice-head">
        @@BACKSVG@@
        <h2>이용 안내</h2>
      </div>
      <ul>
@@NOTICES@@
      </ul>
    </section>
"""
    for k, v in [
        ('CHEV', CHEVRON), ('CATANCHOR', cat_anchor), ('CATNAME', cat_name),
        ('PNAME', p['name']), ('CATCLS', cat_cls), ('ICON', icon),
        ('H1', p['h1']), ('PEN', p['pen']), ('PDESC', p['pdesc']),
        ('SLUG', p['slug']), ('BODY', p['body']), ('NOTICES', notices),
        ('BACKSVG', BACKSVG),
    ]:
        body = body.replace('@@'+k+'@@', v)
    return h + NAV + body + FOOT + p.get('script', '') + "\n</body>\n</html>\n"



def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import pages_a, pages_b, pages_c
    pages = pages_a.PAGES + pages_b.PAGES + pages_c.PAGES
    for p in pages:
        out = os.path.join(ROOT, p['slug'] + '.html')
        with io.open(out, 'w', encoding='utf-8', newline='\n') as f:
            f.write(render(p))
        print('wrote', p['slug'] + '.html')


if __name__ == '__main__':
    main()
