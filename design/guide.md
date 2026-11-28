# tempo 디자인 시스템

개발 도구 화면(상황판, 구성도, 터미널, 상태줄, 블로그, 노트)에 쓰는 어두운 테마다. 아날로그 계기판처럼 어두운 바탕에 신호 셋과 틀 색 하나를 둔다. 밝은 테마는 없다.

## 변형

| 변형 | 바탕 | 틀 색 | 어울리는 곳 |
|---|---|---|---|
| `tempo-ember` 먹 | 따뜻한 먹색 | 놋쇠 | 글을 오래 읽는 화면, 편집기·터미널 |
| `tempo-thread` 시간선 | 푸른 검정 | 호박 | 상황판·구성도처럼 신호를 보는 화면 |

두 변형은 원색 이름과 의미 토큰이 같다. 화면은 의미 토큰(`--bg` `--panel` `--ink` …)으로만 그리고, 변형은 `<html data-theme="tempo-ember">`나 `class="tempo-thread"`로 고른다.

## 색 쓰는 규칙

- 바탕은 세 단이다: 화면 `--bg`, 카드 `--panel`, 눌린 칸·대기 배지 `--soft`. 경계선은 `--line`
- 녹색 `--ok`(thread)는 지금 흐르는 것(동작 중·정상·실시간 그래프)에만 쓴다
- 틀 색 `--accent`(brass)는 탭 밑줄, 주 단추, 링크, 시계에 쓴다
- 경고 `--warn`(signal)과 틀 색은 색상이 가깝다. 상태는 색만으로 나타내지 않고 모양을 함께 쓴다: 정상 ●, 경고 ▲, 오류 ◆, 대기 ○
- 상태 배지 바탕은 `-bg` 짝(`--ok-bg` `--warn-bg` `--err-bg`)을 쓴다. 대기는 `--soft`
- 카드 왼쪽 띠로 흐름을 나타낸다: 흐르는 중은 `--ok`와 빛(`--tempo-glow`), 실패는 `--err`, 평상시는 `--line`
- 본문색(`paper` `dust` `brass` `thread` `signal` `branch`)은 바탕 세 단 어디서나 4.5:1 이상이다. 새 조합을 만들면 `generate.py --check`로 확인한다

## 서체

- 시스템 서체: `-apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", "Noto Sans KR", sans-serif`. 웹 글꼴을 내려받지 않는다
- 고정폭(`"SF Mono", ui-monospace, Menlo, "D2Coding", monospace`, `tabular-nums`)은 시각과 수치에만 쓴다. 라벨에는 쓰지 않는다
- 크기: 헤드라인 28/800, 구역 제목 20/800, 카드 제목 15/700, 본문 15/400 줄 간격 1.6, 보조 13/400
- 한국어는 `word-break: keep-all`로 낱말 단위로 줄을 바꾼다

## 모양

- 모서리: 카드 6px, 단추·입력 4px, 배지 999px
- 그림자를 쓰지 않는다. 층은 바탕 단과 경계선으로 나눈다. 빛(`--tempo-glow`)은 흐르는 녹색에만 쓴다
- 키보드 초점은 `outline: 2px solid var(--accent); outline-offset: 2px`
