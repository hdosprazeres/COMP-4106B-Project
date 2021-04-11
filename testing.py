import subprocess

# in snake.py change sleep_time = 0
# in snake.py at end of game_loop add close()

# for _ in range(100):
for _ in range(2):
    p1 = subprocess.run(["py", "snake.py", "1"])
    p2 = subprocess.run(["py", "snake.py", "2"])
    p3 = subprocess.run(["py", "snake.py", "3"])
    p4 = subprocess.run(["py", "snake.py", "4"])
