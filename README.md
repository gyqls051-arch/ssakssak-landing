# 싹싹김치 — 유틸리티 허브 (랜딩 사이트)

여러 프로그램을 담는 브랜드 허브 정적 사이트. **OFFCUT 본진과 격리**된 별도 Vercel(무료, gyqls051)
계정에 배포한다. 현재 라이브: **https://ssakssak-landing.vercel.app**

## 구성
- `index.html` — 허브 메인 (프로그램 카드 그리드 + 광고 배너 자리 2곳 + 이용 안내)
- `terms.html` — 이용약관 및 면책 고지 (전문)
- `banner.png` — (직접 추가) 상단 광고 배너 이미지. **권장 728×90** (레티나 2배 1456×180).
  - 없으면 "광고 배너 자리" 목업 박스가 대신 표시된다(위치는 항상 보임).

## 프로그램 카드 추가하는 법
`index.html` 의 `<section id="programs">` 안 `.grid` 에 카드 하나 복붙:
- 정식 출시: `class="card"` + `badge live` + 다운로드 `a.btn`
- 준비 중: `class="card soon"` + `badge soon` + `span.btn.dim`(곧 공개)
첫 카드(비디오 다운로더) 형태를 그대로 복사해서 제목/설명/링크만 바꾸면 됨.

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
