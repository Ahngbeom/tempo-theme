# Tempo 쓰는 법

Tempo는 **토큰만 있는 테마**다. React 컴포넌트가 없어서 `window.Tempo`는 비어 있다. 화면은 직접 HTML/JSX로 짜고, 색은 아래 CSS 변수로만 칠한다. 아래 "Components"와 마운트 예시는 생성기가 붙인 일반 문구이니 무시한다.

## 설정

1. `tokens.css`, `components/bundle.css` 순서로 링크한다. `components/bundle.js`는 빈 스크립트다.
2. 변형을 고른다: `<html data-theme="tempo-ember">`(따뜻한 먹색 + 놋쇠) 또는 `data-theme="tempo-thread"`(푸른 검정 + 호박). 한 영역만 바꿀 때는 `class="tempo-thread"`를 쓴다.
   - 변형은 반드시 지정한다. 지정하지 않으면 `--ok-bg` `--warn-bg` `--err-bg` `--info-bg` `--tempo-glow`가 정의되지 않아서, 배지 바탕과 빛이 아무 경고 없이 사라진다. `components/bundle.css`만 링크했다면 변수가 하나도 정의되지 않는다.
3. 밝은 테마는 없다. `body`에 `background: var(--bg); color: var(--ink)`를 직접 준다.

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

## 어디를 읽나

- 색·서체·모양 규칙(상태는 모양과 함께: ● ▲ ◆ ○, 모서리 6/4/999px, 그림자 없음, 서체 크기): `guidelines/design/guide.md`
- 값: `tokens.json`, `tokens.css`. 배지 바탕까지 모든 변수: `components/bundle.css`

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
