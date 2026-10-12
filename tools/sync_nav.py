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
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_pages

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAV = gen_pages.NAV.rstrip('\n')
PAT = re.compile(r'^  <nav class="nav">.*?^  </nav>', re.M | re.S)

# 페이지 고유 내비 차이 — canonical NAV 교체 후 적용 (내비 밖에는 해당 문자열이 없어야 함)
TWEAKS = {
    'archive.html': [
        ('<button class="navlink dd-btn"', '<button class="navlink active dd-btn"'),
        ('href="archive.html#install"', 'href="#install"'),
    ],
    'terms.html': [
        ('<a class="navlink nav-hide-m" href="terms.html">이용약관</a>',
         '<a class="navlink active" href="terms.html" aria-current="page">이용약관</a>'),
    ],
}


def sync_file(path):
    s = io.open(path, encoding='utf-8').read()
    if '<nav class="nav">' not in s:
        return 'skip (no nav)'
    nav = NAV
    for a, b in TWEAKS.get(os.path.basename(path), []):
        if a not in nav:
            return 'WARN tweak anchor missing: %r' % a
        nav = nav.replace(a, b)
    new, n = PAT.subn(lambda _m: nav, s, count=1)
    if n != 1:
        return 'WARN matched %d' % n
    if new == s:
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
