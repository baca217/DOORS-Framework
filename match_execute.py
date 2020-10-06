def execute_command(match):
    highest = ["", 0]
    for i in match:
        if i[1] > highest[1]:
            highest = i
    print("highest match ", highest)
