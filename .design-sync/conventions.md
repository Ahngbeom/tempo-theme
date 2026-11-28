# Tempo 쓰는 법

Tempo는 **토큰과 CSS 부품 클래스로 된 테마**다. React 컴포넌트가 없어서 `window.Tempo`는 비어 있다. 화면은 직접 HTML/JSX로 짜고, 아래 부품 클래스를 쓰며, 그 밖의 색은 CSS 변수로만 칠한다. 아래 "Components"와 마운트 예시는 생성기가 붙인 일반 문구이니 무시한다.

## 설정

1. `tokens.css`, `components/bundle.css` 순서로 링크한다. `components/bundle.js`는 빈 스크립트다.
2. 변형을 고른다: `<html data-theme="tempo-ember">`(따뜻한 먹색 + 놋쇠) 또는 `data-theme="tempo-thread"`(푸른 검정 + 호박). 한 영역만 바꿀 때는 `class="tempo-thread"`를 쓴다.
   - 변형은 반드시 지정한다. 지정하지 않으면 `--ok-bg` `--warn-bg` `--err-bg` `--info-bg` `--tempo-glow`가 정의되지 않아서, 배지 바탕과 빛이 아무 경고 없이 사라진다. `components/bundle.css`만 링크했다면 변수가 하나도 정의되지 않는다.
3. 밝은 테마는 없다. `body`에 `background: var(--bg); color: var(--ink)`를 직접 준다.
4. `components/bundle.css`는 `table` `th` `td` `button` `a` `pre`와 `* { box-sizing: border-box }`도 테마 모양으로 칠한다. 새 클래스로 덮지 말고 그대로 쓴다.

## 토큰

| 쓰임 | 변수 |
|---|---|
| 바탕 세 단 | `--bg`(화면) `--panel`(카드) `--soft`(눌린 칸·대기 배지) |
| 경계선 | `--line` |
| 글자 | `--ink`(본문) `--muted`(보조) `--faint`(흐린 보조) |
| 틀 색 | `--accent`: 탭 밑줄, 주 단추, 링크, 시계 |
| 상태 | `--ok`(지금 흐르는 것만) `--warn` `--err` |
| 상태 배지 바탕 | `--ok-bg` `--warn-bg` `--err-bg` `--info-bg`, 대기는 `--soft` |
| 효과 | `--tempo-glow`(흐르는 녹색에만 쓰는 box-shadow), `--tempo-selection` |

원색 `--tempo-<이름>`(`void` `archive` `drawer` `seam` `paper` `dust` `ash` `brass` `thread` `signal` `branch`)은 의미 토큰 뒤에 있는 값이다. 화면에서는 의미 토큰만 쓴다. 16진수 색을 직접 쓰지 않는다.

## 부품 클래스

| 부품 | 마크업 |
|---|---|
| 카드 | `section.card` + `h3`. 왼쪽 띠: `.live`(흐르는 중, 녹색 빛) `.fork`(실패) |
| 상태 배지 | `span.st.ok` `.st.warn` `.st.err` `.st.idle`. 앞의 ● ▲ ◆ ○ 모양은 CSS가 그린다 |
| 단추 | `div.btns > button`, 주 단추 `button.pri`, 위험 `button.danger` |
| 큰 수치 | `div.big > b.mono + span` |
| 기록 시간선 | `ol.tl > li > time.mono + span.x`, 실패 줄은 `li.fork` |
| 갈래 시간선 | `figure.bt > svg`. 선은 `path.bt-main`(본선) `.bt-fork`(갈래) `.bt-cut`(잘린 갈래), 점은 `circle.bt-node`(갈래 점 `.bt-node.fork`), 잘린 끝은 45° 돌린 `rect.bt-end`, 지금 위치는 `circle.bt-halo` + `circle.bt-now`, 시각은 `text.t` |
| 계기 다이얼 | `div.dials > div.dial[style="--v:0~100"]`, 상태 `.warn` `.err`. 아래 예시의 SVG를 좌표까지 그대로 쓴다(바늘 축이 `60,62`에 맞춰져 있다) |
| 도장 배지 | `div.stamps > span.stamp > small.mono`(날짜), `.warn`(보류) `.err`(반려). 확정된 결정에만 쓴다 |
| 고정폭 | `.mono`: 시각과 수치에만 |

다이얼:

```html
<div class="dials"><div class="dial warn" style="--v:78">
  <svg viewBox="0 0 120 70" aria-hidden="true">
    <path class="dial-track" d="M12,62 A48,48 0 0 1 108,62" pathLength="100"/>
    <path class="dial-ticks" d="M12,62 A48,48 0 0 1 108,62" pathLength="100"/>
    <path class="dial-val" d="M12,62 A48,48 0 0 1 108,62" pathLength="100"/>
    <line class="dial-needle" x1="60" y1="62" x2="60" y2="22"/><circle class="dial-hub" cx="60" cy="62" r="4"/>
  </svg>
  <b class="mono">▲ 78%</b><span>주간 할당량</span>
</div></div>
```

## 어디를 읽나

- 색·서체·모양 규칙(상태는 모양과 함께: ● ▲ ◆ ○, 모서리 6/4/999px, 그림자 없음, 서체 크기): `guidelines/design/guide.md`
- 값: `tokens.json`, `tokens.css`. 배지 바탕까지 모든 변수와 부품 클래스: `components/bundle.css`

## 예시

```html
<html data-theme="tempo-thread">
<body style="margin:0;padding:24px;background:var(--bg);color:var(--ink);font:15px/1.6 -apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo',sans-serif;word-break:keep-all">
  <div style="position:relative;padding:16px 18px 16px 21px;background:var(--panel);border:1px solid var(--line);border-radius:6px">
    <span style="position:absolute;inset:0 auto 0 0;width:3px;border-radius:6px 0 0 6px;background:var(--ok);box-shadow:var(--tempo-glow)"></span>
    <h3 style="margin:0 0 10px;font-size:15px;font-weight:700">수집기</h3>
    <span style="display:inline-flex;gap:6px;padding:1px 9px;border-radius:999px;font-size:12.5px;font-weight:600;color:var(--ok);background:var(--ok-bg)">● 동작 중</span>
    <span style="font-family:'SF Mono',ui-monospace,Menlo,monospace;font-variant-numeric:tabular-nums;color:var(--muted)">14:02:31</span>
  </div>
</body>
</html>
```
