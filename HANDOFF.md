# 싹싹김치 공홈 — 핸드오프 (2026-07-12)

> 2026-07-11~12 전면 리디자인 + 도메인 연결 + SEO 세팅 완료 시점의 인수인계 문서.
> ⚠️ 내부 문서. `.vercelignore`로 배포 제외됨 — 공개 사이트에 올라가면 안 됨.

## 현재 상태 요약

- **라이브**: https://www.ssakkimchi.com (기본) · apex `ssakkimchi.com` → www 308 리다이렉트 · 구주소 `ssakssak-landing.vercel.app` 도 서빙 중(canonical이 www로 정리해줌)
- **도메인**: ssakkimchi.com, Vercel에서 구매 (gyqls051 계정, 연 $11.25)
- **호스팅**: Vercel `gyqls051-archs-projects/ssakssak-landing`, **무료(Hobby) 플랜 유지 결정** — 자체 홍보만 하는 동안 무료, 애드센스 등 수익화 시 Pro($20/월) 전환하기로 함
- **배포**: 이 PC CLI가 `gyqls051-arch`로 로그인돼 있음 → `vercel deploy --prod --yes` 한 줄이면 끝
- **다운로드**: 전부 GitHub Releases 영구링크 (`releases/latest/download/<고정 파일명>`) — Vercel 트래픽 소모 없음

## 페이지 구조 (7페이지)

| 파일 | 역할 |
|---|---|
| `index.html` | 홈 — 디더링 셰이더 히어로(클릭 시 무늬 순환) + ABOUT + LINE-UP + HOW. CSS/셰이더JS 자체 내장 |
| `archive.html` | 자료실 — 카테고리(영상/문서/화면)별 프로그램 목록 + "다음 무료 도구 준비 중" 슬롯 + 설치 방법(#install) |
| `video-downloader.html` | 다운로더 소개·다운로드 (영상, v1.7, 무설치) |
| `player.html` | 플레이어 소개·다운로드 (영상, v0.2.0, 설치형) |
| `hangeul-viewer.html` | 한글뷰어 소개·다운로드 (문서, 설치형) |
| `capture.html` | 캡처 소개·다운로드 (화면, v1.0.4, 설치형+포터블ZIP) |
| `terms.html` | 이용약관 17조 (오픈소스 고지 포함). CSS 자체 내장 |

공용 파일: `ssak.css`(자료실+프로그램 4페이지 공용 스타일), `ssak.js`(내비 드롭다운 — 호버 열림 + 350ms 닫힘 유예), `og-image.png`(1200×630 SNS 공유 이미지), `robots.txt`, `sitemap.xml`
잔재: `style.css` — **아무 페이지도 참조 안 함, 삭제 가능**

## 내비게이션 구조 (사용자 확정 사항)

- 상단 "자료실 ▾" = **드롭다운**으로 카테고리→프로그램 페이지 직행 (전 7페이지 공통, 마크업은 각 페이지 `.dd-menu`에 복제돼 있음)
- 자료실 페이지는 보조 디렉터리(드롭다운의 "자료실 한눈에 보기")

## 디자인 규칙 (사용자 피드백으로 확정 — 위반 금지)

1. **주황 큰 면적 금지** — 그라디언트 대형 카드 X, 주황은 버튼/포인트만 ("눈아파" 피드백)
2. **이모지를 UI 아이콘으로 금지** — SVG(Lucide 스타일 stroke)만. 🥬는 브랜드 마스코트 자리만 허용
3. **아이콘 의미 중복 금지** — 다운로드 화살표는 다운로드 버튼 전용. 프로그램 타일: 다운로더=필름, 플레이어=재생, 뷰어=문서, 캡처=카메라
4. 톤: 밝고 여백 많게(WonderKids 레퍼런스) + 나눔펜스크립트 손글씨 위트 + Pretendard 본문
5. 다크모드: localStorage `ssak-theme`, 전 페이지 지원

## SEO 상태

- ✅ 완료: 키워드 타이틀(유튜브 다운로더/HWP 뷰어/화면 캡처/동영상 플레이어), canonical, OG+트위터 카드, JSON-LD(SoftwareApplication+BreadcrumbList, 홈 WebSite, 자료실 CollectionPage), sitemap.xml(7페이지), robots.txt, og-image.png
- ✅ 소유확인 메타태그 심음: 구글(`HlAU0...`) + 네이버(`4ee92...`) — index.html
- ⏳ **사용자 액션 남음**: 서치콘솔/서치어드바이저에서 확인 버튼 → 사이트맵 제출(`https://www.ssakkimchi.com/sitemap.xml`) → 색인/수집 요청
- 전략 메모: "유튜브 다운로더"는 초경쟁 — 롱테일(무설치 등)과 "HWP 뷰어 무료"·"스크롤 캡처" 같은 저경쟁 키워드가 먼저 잡힘. 네이버는 사이트보다 네이버 블로그 포스팅이 효과 빠름

## 새 프로그램 추가 절차 (자료실 계속 확장 예정)

1. 기존 프로그램 페이지(예: `capture.html`) 복제 → 내용 교체 (breadcrumb·JSON-LD·canonical 포함)
2. `archive.html` — 해당 카테고리에 `.prog` 행 추가 (+카테고리 개수 갱신, 필요시 새 카테고리 섹션)
3. **7개 페이지 전부**의 드롭다운 `.dd-menu`에 항목 추가
4. `index.html` — LINE-UP 행 추가 (+히어로 스탯 "도구 N종")
5. `sitemap.xml` — URL 추가
6. 다운로드는 GitHub Releases 고정 파일명 패턴 유지

### 다음 프로그램 후보 (2026-07-12 리서치)
1. **동영상 용량 줄이기/변환기** — 플레이어의 트랜스코드 프리셋(카톡300MB/디스코드) 스핀오프, 개발비 최소 (단기 추천)
2. **PDF 도구** (합치기·분할·압축) — "PDF 합치기" 대형 키워드, 경쟁자가 광고번들/업로드형뿐 → 100% 오프라인 각 (메인 승부수)
3. HEIC/WebP 변환기, AI 자막 생성기(로컬 Whisper), 파일명 일괄 변경
- 피할 것: 압축(반디집), 뷰어(꿀뷰), PC최적화(스캠 이미지)

## 격리 원칙 (절대 준수)

- GitHub 리포 4개 전부 `gyqls051-arch` (public 유지 필수 — private 전환 시 다운로드 전부 깨짐)
- Vercel·도메인 = gyqls051 계정. **본계정(rlagyqls051)/OFFCUT과 절대 연결 금지**
- OFFCUT 광고는 "외부 광고주처럼만" — 소유 관계 노출 금지 (배너: 사이드레일 2 + 하단 1)
- 릴리스 시 exe 파일명 변경 금지 (영구링크 깨짐). 페이지의 버전 텍스트(v1.7 등)는 하드코딩 — 수동 갱신

## git

- 로컬 전용 리포(GitHub 리모트 없음), 브랜치 `main`
- 주요 커밋: `6b624e7` 전면 리디자인 → 소유확인 태그 → 도메인 URL 교체 → (본 커밋) 핸드오프
