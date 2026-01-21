import matplotlib.pyplot as plt
import random

# --- НАСТРОЙКИ ---
LEVELS = 10         
INITIAL_MODE = 'left'  
JAM_CHANCE = 0.03      

class GaltonBoard:
    def __init__(self, levels, mode='left', jam_chance=0.03):
        self.levels = levels
        self.mode = mode
        self.jam_chance = jam_chance
        self.reset()

    def reset(self):
        self.bins = [0] * (self.levels + 1)
        self.switches = []
        self.total_jams = 0
        self.total_passes = 0
        self.balls_completed = 0
        
        # Состояние текущего шарика: None (нет на поле), или [row, col]
        self.current_ball = None 
        self.last_jams = []
        
        for i in range(1, self.levels + 1):
            if self.mode == 'left': row = [0] * i
            elif self.mode == 'right': row = [1] * i
            else: row = [random.randint(0, 1) for _ in range(i)]
            self.switches.append(row)

    def step(self):
        """Один шаг шарика вниз"""
        self.last_jams = []
        
        # 1. Если шарика нет, создаем его над первым переключателем
        if self.current_ball is None:
            self.current_ball = [0, 0] # [row, col]
            return

        row, col = self.current_ball
        
        # 2. Если шарик на уровне переключателей (0...LEVELS-1)
        if row < self.levels:
            old_state = self.switches[row][col]
            self.total_passes += 1
            
            # Логика переключения
            jammed = False
            if random.random() < self.jam_chance:
                self.last_jams.append((row, col))
                self.total_jams += 1
                jammed = True
            else:
                self.switches[row][col] = 1 - old_state
            
            # Определяем, куда упадет (в ту же колонку или col+1)
            next_col = col + 1 if old_state == 1 else col
            self.current_ball = [row + 1, next_col]
            
            # Если шарик достиг дна (уровень == LEVELS)
            if self.current_ball[0] == self.levels:
                final_col = self.current_ball[1]
                self.bins[final_col] += 1
                self.balls_completed += 1
        else:
            # 3. Если шарик уже в корзине, убираем его, чтобы следующим нажатием создать новый
            self.current_ball = None
            self.step()

# Инициализация
board = GaltonBoard(LEVELS, INITIAL_MODE, JAM_CHANCE)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 11), gridspec_kw={'height_ratios': [2, 1]})

def update_plot():
    ax1.clear()
    ax2.clear()
    
    # Отрисовка переключателей
    for r in range(LEVELS):
        for c in range(len(board.switches[r])):
            state = board.switches[r][c]
            x, y = c - r / 2.0, -r
            is_jammed = (r, c) in board.last_jams
            color = '#F1C40F' if is_jammed else ('#3498DB' if state == 1 else '#E74C3C')
            lw = 5 if is_jammed else 3
            dx, dy = 0.3, 0.15
            if state == 1: 
                ax1.plot([x-dx, x+dx], [y+dy, y-dy], color=color, lw=lw) 
            else: 
                ax1.plot([x-dx, x+dx], [y-dy, y+dy], color=color, lw=lw)
            ax1.plot(x, y, 'ko', markersize=4)

    # Отрисовка текущего положения шарика
    if board.current_ball is not None:
        r, c = board.current_ball
        bx, by = c - r / 2.0, -r
        ax1.plot(bx, by, 'go', markersize=15, zorder=5)

    # Статистика
    actual_rate = (board.total_jams / board.total_passes * 100) if board.total_passes > 0 else 0
    stats = (f"Завершено шариков: {board.balls_completed}\n"
             f"Всего заклиниваний: {board.total_jams}\n"
             f"Текущий сбой: {actual_rate:.2f}%")
    ax1.text(0.02, 0.95, stats, transform=ax1.transAxes, fontsize=11, 
             bbox=dict(facecolor='white', alpha=0.8))
    
    ax1.set_title("Нажимайте ПРОБЕЛ для шага вниз | 'R' - сброс", fontsize=12)
    ax1.set_xlim(-LEVELS/2 - 1, LEVELS/2 + 1)
    ax1.set_ylim(-LEVELS - 1, 1)
    ax1.axis('off')

    # Гистограмма
    ax2.bar(range(LEVELS + 1), board.bins, color='#95A5A6', edgecolor='black')
    ax2.set_ylim(0, max(board.bins) + 3)
    ax2.set_xticks(range(LEVELS + 1))
    ax2.set_title("Распределение в корзинах")
    
    plt.draw()

def on_key(event):
    if event.key == ' ':
        board.step()
        update_plot()
    elif event.key == 'r' or event.key == 'к':
        board.reset()
        update_plot()

fig.canvas.mpl_connect('key_press_event', on_key)
update_plot()
plt.tight_layout()
plt.show()