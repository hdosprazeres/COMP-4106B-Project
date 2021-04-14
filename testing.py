import subprocess

# in snake.py change sleep_time = 0
# in snake.py at end of game_loop add close()

for _ in range(100):
    for x in range(5):
        print("py", "snake.py", x)
        subprocess.run(["py", "snake.py", str(x)])
        print("\n")
