# tempo-theme

개발 환경 전체(대시보드, 터미널, 셸 프롬프트, Claude Code 상태줄, 블로그, Obsidian)에서 같이 쓰는 어두운 테마다. 색의 원본은 `tokens.json` 하나이고, 도구별 파일은 `generate.py`가 `dist/`에 만든다.

아날로그 계기판처럼 어두운 바탕에 신호 셋(녹색·노랑·적주황)과 틀 색 하나를 둔다. 같은 색을 웹·터미널·앱에서 똑같이 읽도록 대비를 생성 단계에서 검사한다.

## 변형

| 변형 | 바탕 | 틀(탭·주 단추·링크·시계) | 어울리는 곳 |
|---|---|---|---|
| `ember` 템포 · 먹 | 따뜻한 먹색 `#0f0c09` | 놋쇠 `#d79a45` | 글을 오래 읽는 화면, 편집기·터미널 |
| `thread` 템포 · 시간선 | 푸른 검정 `#050b0b` | 호박 `#e8a33d` | 상황판·구성도처럼 신호를 보는 화면 |

두 변형은 같은 원색 이름(`void` `archive` `drawer` `seam` `paper` `dust` `ash` `brass` `thread` `signal` `branch`)과 터미널 16색을 가진다. 견본은 `specimen/index.html`을 브라우저로 열면 된다.

## 색 쓰는 규칙

색·서체·모양 규칙은 [`design/guide.md`](design/guide.md)에 있다. 같은 문서가 Claude Design 디자인 시스템의 안내문이 된다.

## 도구별 파일

| 도구 | 파일 | 쓰는 법 |
|---|---|---|
| 웹(CSS) | `dist/css/tempo.css` | `<html data-theme="tempo-ember">` 또는 `class="tempo-thread"`. `--bg` `--panel` `--ink` `--muted` `--accent` `--ok` `--warn` `--err`과 `-bg` 짝을 정의한다. 원색은 `--tempo-<이름>` |
| iTerm2 | `dist/iterm2/Tempo Ember.itermcolors` | Settings > Profiles > Colors > Color Presets > Import |
| Ghostty | `dist/ghostty/tempo-ember` | `~/.config/ghostty/themes/`에 복사하고 설정에 `theme = tempo-ember` |
| herdr | `dist/herdr/tempo-ember.toml` | 내용을 `~/.config/herdr/config.toml`에 붙이고 `herdr server reload-config`. 또는 `[theme] name = "terminal"`로 두면 터미널 16색을 그대로 따른다 |
| 256색 도구 | `dist/ansi256/tempo-ember.json` | 원색·16색마다 가장 가까운 xterm 256색 번호. shell-prompt·claude-statusline 테마가 쓴다 |
| Swift (AppKit) | `dist/swift/TempoTheme.swift` | `TempoTheme.ember.brass` 같은 `NSColor` . 어두운 바탕을 직접 그리는 앱에만 쓴다 |
| Obsidian | `dist/obsidian/tempo-ember.css` | 보관함의 `.obsidian/snippets/`에 복사하고 설정 > 모양 > CSS 스니펫에서 켠다. 어두운 모드에서만 적용된다 |
| Claude Design | `dist/claude-design/`, `/design-sync` | 아래 "Claude Design" 참고 |

바탕을 시스템이 칠하는 곳에는 적용하지 않는다. 예를 들어 cc-menutor의 메뉴바와 드롭다운은 라이트·다크·투명 바탕 위에 그려지고, 밝은 메뉴바(#ECECEC)에서 `thread`·`signal`의 대비가 1.2~1.4:1로 떨어진다. cc-menutor는 두 바탕 모두에서 3.5:1을 지키는 자체 색을 그대로 쓴다.

다른 저장소는 필요한 파일을 복사해 가고, 파일 머리나 커밋 메시지에 이 저장소의 커밋을 적는다.

## Claude Design

Claude Design에 올리는 길은 둘이고, 올라가는 내용이 다르다.

| 길 | 올라가는 것 | 어디로 |
|---|---|---|
| `/design-sync` | `dist/css/tempo-kit.css`(토큰 + `design/components.css` 부품 클래스), `design/guide.md`(안내문), `.design-sync/conventions.md`(README 머리) | Design System artifact `Tempo`. 대상은 `.design-sync/artifact.json` |
| `dist/claude-design/` 묶음 | 아래 표의 파일. 카드 포함 | claude.ai/design 프로젝트에 손으로 올린다 |

`design/cards/` 미리보기 카드는 `dist/claude-design/` 묶음에만 들어간다. `/design-sync`로는 부품 클래스만 올라가고 카드는 올라가지 않는다.

### `/design-sync`

1. `tokens.json`이나 `design/guide.md`를 고치고 `python3 generate.py`로 다시 만든다
2. 이 저장소에서 Claude Code의 `/design-sync`를 실행한다. 설정은 `.design-sync/config.json`에 있다

토큰 이름이나 부품 클래스를 바꾸면 `.design-sync/conventions.md`의 토큰 표·부품 표도 같이 고친다.

### `dist/claude-design/` 묶음

| 파일 | 원본 |
|---|---|
| `README.md` | `design/guide.md` 그대로 |
| `tokens.css` | `dist/css/tempo.css`와 같다 |
| `preview/*.html` | `design/cards/*.html` 조각을 두 변형으로 나란히 펼친 카드. 첫 줄 `@dsCard` 표시로 디자인 시스템 창의 묶음(Colors·Type·Components·Timeline·Terminal)이 정해진다 |

1. 카드를 더하거나 고치려면 `design/cards/`에 조각을 쓴다. 첫 줄은 `<!-- @dsCard group="묶음" -->`, 본문에서 `{{label}}` `{{swatches}}` `{{ansi}}` `{{semantic}}`을 쓸 수 있다. 부품 모양은 `design/components.css`
2. `python3 generate.py`로 다시 만든다
3. `dist/claude-design/`의 파일을 claude.ai/design 프로젝트에 올린다

Claude Design에서 색을 직접 고치지 않는다. 고친 색은 다른 도구 파일과 어긋난다.

## 색 바꾸기

1. `tokens.json`을 고친다. `dist/`와 `specimen/index.html`은 손으로 고치지 않는다
2. `python3 generate.py`로 다시 만든다
3. `python3 -m unittest discover -s tests`로 확인한다. 대비가 모자라면 어느 색이 몇 대 1인지 알려 준다

Python 3.11 이상, 표준 라이브러리만 쓴다.
