# 싹싹김치 — 공홈 (브랜드 랜딩 + 자료실)

무료 유틸리티 브랜드 정적 사이트. **OFFCUT 본진과 격리**된 별도 Vercel(무료, gyqls051)
계정에 배포한다. 현재 라이브: **https://www.ssakkimchi.com** (구주소 ssakssak-landing.vercel.app)

> 📋 **현재 구조·디자인 규칙·새 프로그램 추가 절차는 `HANDOFF.md` 참고** (2026-07-12 리디자인 이후 그쪽이 최신)

**소스 리포**: https://github.com/gyqls051-arch/ssakssak-landing (공홈은 git 관리됨 — 수정 → 커밋·푸시 → `vercel deploy --prod`)

## 구성 (2026-10-11 기준)
- `index.html` — 홈 (루프 영상 히어로 + LINE-UP 20종 + HOW + 크로스프로모션)
- `archive.html` — 자료실 (5개 카테고리 그리드, UI-모킹 카드 썸네일)
- 다운로드형: `video-downloader.html` / `player.html` / `compressor.html` / `hangeul-viewer.html` / `capture.html`
- 브라우저 도구(서버 업로드 없음): `pdf.html` / `hwp-pdf.html` / `thumbnail.html` / `text-tools.html` / `image-tools.html`
- 유입용 웹도구 9종(2026-10 추가): `qr.html` `password.html` `dday.html` `salary.html` `severance.html` `heic.html` `pixel-test.html` `input-test.html` `video-gif.html`
  - 이 9개는 `tools/gen_pages.py` + `tools/pages_[abc].py` 로 생성 — 수정할 때 페이지 직접 고치거나, 스펙 고치고 `python tools/gen_pages.py` 재생성
  - 사용 라이브러리: `js/vendor/` (qrcode-generator·gif.js·heic2any — 전부 로컬 번들)
- `domino/` — 도미노 시뮬레이션 빌드 산출물 (원본: `domino-art-simulation` 리포)
- `terms.html` — 이용약관 및 면책 고지
- `ssak.css` / `ssak.js` — 공용 스타일·내비 드롭다운 / `img/` — WebP 일러스트 / `sitemap.xml`, `robots.txt` — SEO
- `promo.json` — **앱 배너 원격 설정** (이 파일만 고치면 전 앱 배너 문구·링크·색 교체)

## 프로그램 추가하는 법
`HANDOFF.md`의 "새 프로그램 추가 절차" 참고 — 전용 페이지 복제 + 자료실 행 + 드롭다운(7페이지) + 홈 LINE-UP + sitemap 갱신.

## 광고 배너 자리 (목업 2곳)
- 상단 슬롯: 현재 OFFCUT 광고(외부 광고주처럼). `banner.png` 넣으면 이미지로 표시.
- 하단 슬롯: 빈 목업("광고 배너 자리"). 제휴 광고 붙일 위치.
- 둘 다 `.adslot > .adbox` 구조. 728×90 권장.

## 링크 (이미 격리 계정으로 설정됨)
- 다운로드는 전부 `releases/latest/download/<버전 없는 고정 파일명>` 패턴 — 새 릴리즈 때 같은 고정 이름 자산만 올리면 사이트 수정 불필요.
  - 다운로더: `github.com/gyqls051-arch/ssakssak-downloader/releases/latest/download/SsakSsakKimchiDownloader.exe`
  - 플레이어: `github.com/gyqls051-arch/SsakSsak-Player/releases/latest/download/SsakSsak-Player-Setup.exe`
  - 캡처도구: `github.com/gyqls051-arch/ssakssak-capture/releases/latest/download/Setup_SsakKimchiCapture.exe` (+ `SsakKimchiCapture_portable.zip`)
- 문의: `github.com/gyqls051-arch/ssakssak-downloader/issues` (캡처는 `ssakssak-capture/issues`)
- 광고 클릭: `offcut.dev/?utm_source=ssakssak_hub&utm_medium=top_banner`
  - ⚠️ OFFCUT 은 **외부 광고주처럼만** 노출. 이 사이트가 OFFCUT 소유임을 드러내지 말 것.

## 재배포 (gyqls051 계정 전용)
이 폴더는 `.vercel/project.json` 으로 `gyqls051-archs-projects/ssakssak-landing` 에 연결돼 있음.
CLI 가 gyqls051-arch 로 로그인돼 있으면 (`vercel whoami` 로 확인, 2026-07-11 현재 그 상태) 그냥:
```
vercel deploy --prod --yes
```
⚠️ `vercel whoami` 가 본계정(rlagyqls051)이면 **반드시 gyqls051 토큰 + scope** 로 배포:
```
vercel deploy --prod --yes --scope gyqls051-archs-projects --token=<gyqls051 토큰>
```
(토큰: gyqls051 Vercel → Settings → Tokens → 짧은 만료로 생성, 배포 후 삭제)

## 주의 (격리)
- 앱 소스 레포와 분리된 폴더. 본계정/OFFCUT 계정·도메인과 엮지 말 것.
- 커스텀 도메인도 OFFCUT 과 무관하게.
