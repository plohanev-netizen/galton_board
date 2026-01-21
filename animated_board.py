import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# --- НАСТРОЙКИ ---
LEVELS = 10         
BALLS = 50              # Теперь работает корректно даже при 1, 2, 5 шариках
INITIAL_MODE = 'left'  
JAM_CHANCE = 0.03      
SPEED = 100            # Сделаем чуть медленнее для малых количеств, чтобы успеть рассмотреть

class GaltonBoard:
    def __init__(self, levels, mode='left', jam_chance=0.03):
        self.levels = levels
        self.jam_chance = jam_chance
        self.bins = [0] * (levels + 1)
        self.switches = []
        self.last_jams = [] 
        self.total_jams = 0      
        self.total_passes = 0    
        
        for i in range(1, levels + 1):
            if mode == 'left': row = [0] * i
            elif mode == 'right': row = [1] * i
            else: row = [random.randint(0, 1) for _ in range(i)]
            self.switches.append(row)

    def drop_ball(self):
        col = 0
        path = []
        self.last_jams = []
        
        for row in range(self.levels):
            current_x = col - row / 2.0
            path.append((current_x, -row))
            
            old_state = self.switches[row][col]
            self.total_passes += 1
            
            if random.random() < self.jam_chance:
                self.last_jams.append((row, col))
                self.total_jams += 1
            else:
                self.switches[row][col] = 1 - old_state
            
            if old_state == 1:
                col += 1
                
        final_x = col - self.levels / 2.0
        path.append((final_x, -self.levels))
        self.bins[col] += 1
        return path

board = GaltonBoard(LEVELS, INITIAL_MODE, JAM_CHANCE)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 11), gridspec_kw={'height_ratios': [2, 1]})

# Переменная для отслеживания реального номера шарика
current_ball_num = 0

def animate(i):
    global current_ball_num
    
    # Логика ускорения: если шариков много (больше 50), начинаем пропускать кадры
    # Если мало — показываем каждый
    step = 1
    if BALLS > 50:
        step = 1 if i < 20 else 10
    
    for _ in range(step):
        if current_ball_num < BALLS:
            path = board.drop_ball()
            current_ball_num += 1
        else:
            return # Все шарики выпущены

    ax1.clear()
    for r in range(LEVELS):
        for c in range(len(board.switches[r])):
            state = board.switches[r][c]
            x = c - r / 2.0
            y = -r
            is_jammed = (r, c) in board.last_jams
            color = '#F1C40F' if is_jammed else ('#3498DB' if state == 1 else '#E74C3C')
            lw = 5 if is_jammed else 3
            dx, dy = 0.3, 0.15
            if state == 1: 
                ax1.plot([x-dx, x+dx], [y+dy, y-dy], color=color, lw=lw) 
            else: 
                ax1.plot([x-dx, x+dx], [y-dy, y+dy], color=color, lw=lw)
            ax1.plot(x, y, 'ko', markersize=4)

    px, py = zip(*path)
    ax1.plot(px, py, color='#2ECC71', lw=2, alpha=0.5)
    ax1.plot(px[-1], py[-1], 'go', markersize=15)

    actual_rate = (board.total_jams / board.total_passes * 100) if board.total_passes > 0 else 0
    stats_info = (
        f"Шариков пропущено: {current_ball_num} из {BALLS}\n"
        f"Всего заклиниваний: {board.total_jams}\n"
        f"Реальный % сбоев: {actual_rate:.2f}%"
    )
    
    ax1.text(0.02, 0.95, stats_info, transform=ax1.transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax1.set_xlim(-LEVELS/2 - 1, LEVELS/2 + 1)
    ax1.set_ylim(-LEVELS - 1, 1)
    ax1.axis('off')

    ax2.clear()
    bars = ax2.bar(range(LEVELS + 1), board.bins, color='#95A5A6', edgecolor='black')
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{int(height)}', ha='center', va='bottom')
        
    ax2.set_ylim(0, max(board.bins) + 2)
    ax2.set_title("Распределение по корзинам")

# frames теперь считается динамически
ani = animation.FuncAnimation(fig, animate, frames=(BALLS//10 + 20) if BALLS > 50 else BALLS, 
                              interval=SPEED, repeat=False)

plt.tight_layout()
plt.show()