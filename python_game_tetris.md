# 테트리스 게임 개발 과정 (VSCode + Copilot)

### VSCode에서 Copilot을 활용해 파이썬으로 테트리스 게임을 단계별로 개발한 과정을 정리했습니다.

## 1. 초기 설정 및 기본 게임 구현
- **상황**: VSCode에서 새 파일 `tetris.py`를 열고 Copilot 활성화.
- **입력**: "pygame으로 테트리스 게임 창과 그리드를 만들자."
- **Copilot 제안**: `pygame` 초기화, 창 설정, 그리드 생성 코드.
- **구현**:
  - 창 크기: 300x600px.
  - 10x20 그리드 리스트로 정의.
  - 블록을 화면에 그리기 위한 `draw_grid()` 함수 작성.

```python
import pygame
pygame.init()
WIDTH, HEIGHT = 300, 600
GRID_WIDTH, GRID_HEIGHT = 10, 20
BLOCK_SIZE = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
```

---

## 2. 블록 이동 및 회전 기능 추가
- **입력**: "블록을 좌우로 이동하고 회전시키는 기능 추가."
- **Copilot 제안**: `Tetromino` 클래스와 이동/회전 로직.
- **구현**:
  - `Tetromino` 클래스: 블록 위치와 모양 관리.
  - 방향키로 좌우 이동(`move`) 및 회전(`rotate`) 구현.
  - `valid_move()`로 충돌 여부 확인.

```python
class Tetromino:
    def __init__(self):
        self.x = GRID_WIDTH // 2 - 1
        self.y = 0
        self.shape = [[1, 1], [1, 1]]  # 예: 사각형 블록

    def move(self, dx, dy):
        if valid_move(self, dx, dy):
            self.x += dx
            self.y += dy

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        if not valid_move(self, 0, 0):
            self.shape = [list(row) for row in zip(*self.shape)][::-1]  # 복구
```

---

## 3. 블록 하강 및 고정
- **입력**: "블록이 자동으로 떨어지고 바닥에 닿으면 고정되게."
- **Copilot 제안**: 주기적 하강 로직과 `merge_tetromino()` 함수.
- **구현**:
  - `fall_time`과 `fall_speed`로 하강 속도 조절.
  - 바닥 충돌 시 그리드에 고정 후 새 블록 생성.

```python
fall_time = 0
fall_speed = 500  # 밀리초
clock = pygame.time.Clock()

while True:
    fall_time += clock.get_rawtime()
    clock.tick()
    if fall_time >= fall_speed:
        current_piece.move(0, 1)
        fall_time = 0
```

---

## 4. 줄 지우기 및 점수 시스템
- **입력**: "가득 찬 줄을 지우고 점수를 추가해."
- **Copilot 제안**: `clear_lines()`와 점수 증가 로직.
- **구현**:
  - 가득 찬 줄 제거 및 위 줄 하강.
  - 줄당 100점 추가, 화면에 표시.

```python
score = 0

def clear_lines():
    global grid, score
    lines_cleared = 0
    for i in range(GRID_HEIGHT):
        if all(grid[i]):
            del grid[i]
            grid.insert(0, [0] * GRID_WIDTH)
            lines_cleared += 1
    score += lines_cleared * 100
```

---

## 5. 게임 오버 및 재시작
- **입력**: "게임 오버 조건과 재시작 기능 넣어."
- **Copilot 제안**: 블록 생성 시 공간 확인, `S` 키 재시작.
- **구현**:
  - 새 블록 생성 불가 시 게임 오버 화면 표시.
  - `S` 키로 재시작.

```python
def check_game_over():
    return not valid_move(Tetromino(), 0, 0)

if check_game_over():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 36)
    text = font.render("Game Over - Press S to Restart", True, (255, 255, 255))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
```

---

## 6. 시작 및 일시정지 기능
- **입력**: "게임 시작과 일시정지 기능 추가."
- **Copilot 제안**: `paused` 변수와 `P` 키 토글.
- **구현**:
  - `S` 키로 시작, `P` 키로 일시정지/재개.
  - 오른쪽 UI로 상태 표시.

```python
paused = False
running = False

for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_s:
            running = True
        if event.key == pygame.K_p and running:
            paused = not paused
```

---

## 7. 즉시 하강 기능
- **입력**: "스페이스바로 블록을 바로 떨어뜨리자."
- **Copilot 제안**: `drop_to_bottom()` 메서드.
- **구현**:
  - 스페이스바로 블록을 바닥까지 이동 후 고정.

```python
def drop_to_bottom(piece):
    while valid_move(piece, 0, 1):
        piece.move(0, 1)
    merge_tetromino(piece)

if event.key == pygame.K_SPACE:
    drop_to_bottom(current_piece)
```

---

## 8. 오른쪽 영역 보호 및 창 크기 확장
- **입력**: "오른쪽 UI 영역을 보호하고 창을 키워."
- **Copilot 제안**: 경계 조건 추가, `WIDTH` 확장.
- **구현**:
  - 블록 이동을 `GRID_WIDTH`로 제한.
  - 창 크기를 500x600으로 확장, UI 조정.

```python
WIDTH = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def valid_move(piece, dx, dy):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = piece.x + x + dx
                if new_x < 0 or new_x >= GRID_WIDTH:
                    return False
    return True
```

---

## 9. 블록 반전 기능 추가
- **입력**: "블록을 좌우로 반전시키는 기능 넣어."
- **Copilot 제안**: `flip` 메서드와 `R` 키 로직.
- **구현**:
  - `R` 키로 좌우 반전, 충돌 시 복구.

```python
def flip(self):
    self.shape = [row[::-1] for row in self.shape]
    if not valid_move(self, 0, 0):
        self.shape = [row[::-1] for row in self.shape]

if event.key == pygame.K_r:
    current_piece.flip()
```

---

## 10. 음악 코드 주석 처리
- **입력**: "음악은 나중에 추가하려고, 관련 코드 주석 처리해."
- **Copilot 제안**: `pygame.mixer` 코드 주석화.
- **구현**:
  - 음악 관련 코드 주석 처리.

```python
# pygame.mixer.init()
# pygame.mixer.music.load("tetris_music.mp3")
# pygame.mixer.music.play(-1)
```

---

## 최종 결과물
- **파일명**: `tetris_final.py`
- **특징**:
  - 기본 기능: 이동, 회전, 하강, 줄 지우기.
  - 추가 기능: 점수, 게임 오버, 시작/일시정지, 즉시 하강, 블록 반전.
  - 창 크기: 500x600px, 오른쪽 UI 포함.
  - 음악: 주석 처리 상태.

---

## 실행 방법
1. VSCode에서 `tetris_final.py` 저장.
2. 터미널에서 실행:
   ```bash
   python tetris_final.py
   ```

Copilot의 도움을 받아 단계별로 발전시킨 테트리스 게임입니다. 추가 요청이 있다면 언제든 말씀해주세요!
```

---

### 사용 방법
1. 위 내용을 복사합니다.
2. VSCode에서 새 파일을 만들고 `tetris_development.md`로 저장합니다.
3. 파일을 열어 확인하거나, Markdown 뷰어 확장(예: Markdown Preview)을 사용해 미리보기를 볼 수 있습니다.

이 형식은 깃허브나 문서화에도 적합하며, 코드 블록과 설명이 잘 구분되어 있습니다. 추가 수정이 필요하면 말씀해주세요!
