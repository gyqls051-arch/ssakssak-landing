# -*- coding: utf-8 -*-
# 손작성 페이지의 내비 드롭다운을 gen_pages.NAV와 동기화한다 — python tools/sync_nav.py
#
# 내비를 바꿀 때는 tools/gen_pages.py의 NAV 문자열만 수정한 뒤:
#   python tools/gen_pages.py   (생성 페이지 재생성)
#   python tools/sync_nav.py    (손작성 페이지 내비 블록 교체)
#
# <nav class="nav"> ~ 첫 </nav> 사이를 통째로 NAV로 바꾼다.
# breadcrumb의 <nav class="crumb">는 건드리지 않는다. domino/index.html 처럼
# 내비가 없는 페이지는 자동으로 건너뛴다.
#
# 겸사: ssak.css / ssak.js 참조의 ?v= 쿼리를 현재 파일 내용 해시로 스탬프한다.
# 에셋이 바뀌면 쿼리도 달라져 브라우저 캐시가 자동으로 무효화된다.
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_pages

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAV = gen_pages.NAV.rstrip('\n')
PAT = re.compile(r'^  <nav class="nav">.*?^  </nav>', re.M | re.S)

# 페이지 고유 내비 차이 — canonical NAV 교체 후 적용 (내비 밖에는 해당 문자열이 없어야 함)
TWEAKS = {
    'archive.html': [
        ('<button class="navlink dd-btn" aria-haspopup="true" aria-expanded="false">자료실',
         '<button class="navlink active dd-btn" aria-haspopup="true" aria-expanded="false">자료실'),
        ('href="archive.html#install"', 'href="#install"'),
    ],
    'terms.html': [
        ('<a class="navlink nav-hide-m" href="terms.html">이용약관</a>',
         '<a class="navlink active" href="terms.html" aria-current="page">이용약관</a>'),
    ],
}


ASSET_PAT = re.compile(r'(["\'])(ssak\.(?:css|js))(?:\?v=[^"\']*)?\1')
CSSV, JSV = gen_pages._asset_v('ssak.css'), gen_pages._asset_v('ssak.js')


def stamp_assets(s):
    def repl(m):
        v = CSSV if m.group(2).endswith('.css') else JSV
        return '%s%s?v=%s%s' % (m.group(1), m.group(2), v, m.group(1))
    return ASSET_PAT.sub(repl, s)


def sync_file(path):
    s0 = io.open(path, encoding='utf-8').read()
    s = stamp_assets(s0)
    if '<nav class="nav">' not in s:
        if s != s0:
            io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
            return 'assets stamped (no nav)'
        return 'skip (no nav)'
    nav = NAV
    for a, b in TWEAKS.get(os.path.basename(path), []):
        if a not in nav:
            return 'WARN tweak anchor missing: %r' % a
        nav = nav.replace(a, b)
    new, n = PAT.subn(lambda _m: nav, s, count=1)
    if n != 1:
        return 'WARN matched %d' % n
    if new == s0:
        return 'already'
    io.open(path, 'w', encoding='utf-8', newline='\n').write(new)
    return 'synced'


def main():
    changed = 0
    for name in sorted(os.listdir(ROOT)):
        if not name.endswith('.html'):
            continue
        r = sync_file(os.path.join(ROOT, name))
        print('%-26s %s' % (name, r))
        if r == 'synced':
            changed += 1
    print('done - %d file(s) synced' % changed)


if __name__ == '__main__':
    main()
