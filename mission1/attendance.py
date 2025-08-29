import os

MAX_PLAYER_NUM = 100

players = {}
total_player_num = 0

attendanced = [[0] * 7 for _ in range(MAX_PLAYER_NUM)]
points = [0] * MAX_PLAYER_NUM
grade = ["NORMAL"] * MAX_PLAYER_NUM
names = [''] * MAX_PLAYER_NUM
should_remain_player = [False] * MAX_PLAYER_NUM


def set_attendance(player, day):
    player_index = get_player_index(player)
    index = get_day_index(day)
    should_remain_player[player_index] |= is_essential(day)
    attendanced[player_index][index] += 1
    points[player_index] += get_points(day)


def get_player_index(player):
    if player not in players:
        register_player(player)
    return players[player]


def register_player(player):
    global total_player_num
    total_player_num += 1
    players[player] = total_player_num
    names[total_player_num] = player


def get_day_index(wk):
    week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    return week.index(wk)


def get_points(wk):
    if wk == "wednesday":
        return 3
    elif wk in ["saturday", "sunday"]:
        return 2
    return 1


def is_essential(day):
    essential_day = ["wednesday", "saturday", "sunday"]
    if day in essential_day:
        return True
    return False


def manage_attendance(attendance_history):
    result = []
    for player, name in attendance_history:
        set_attendance(player, name)

    for player in range(1, total_player_num + 1):
        add_bonus_point(player)
        set_grade(player)
        result.append(f"NAME : {names[player]}, POINT : {points[player]}, GRADE : {grade[player]}")

    result.append("\nRemoved player")
    result.append("==============")
    for player in range(1, total_player_num + 1):
        if should_remove(player):
            result.append(names[player])
    print("\n".join(result))
    return "\n".join(result)  # for test


def should_remove(player):
    return grade[player] not in (1, 2) and should_remain_player[player] is False


def set_grade(player):
    if points[player] >= 50:
        grade[player] = "GOLD"
    elif points[player] >= 30:
        grade[player] = "SILVER"


def add_bonus_point(player):
    if need_wednesday_bonus(player):
        points[player] += 10
    if need_weekend_bonus(player):
        points[player] += 10


def need_weekend_bonus(player):
    saturday = get_day_index("saturday")
    sunday = get_day_index("sunday")
    return attendanced[player][saturday] + attendanced[player][sunday] > 9


def need_wednesday_bonus(i):
    return attendanced[i][get_day_index("wednesday")] > 9


def load_file(file_path):
    if not os.path.exists(file_path):
        print("파일을 찾을 수 없습니다.")
        return []

    attendance_history = []
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                attendance_history.append(parts)
    return attendance_history


if __name__ == "__main__":
    if os.path.dirname(__file__) == '':
        CURRENT_DIR = os.getcwd()
    else:
        CURRENT_DIR = os.path.dirname(__file__)
    file_name = "attendance_weekday_500.txt"
    input = load_file(os.path.join(CURRENT_DIR, file_name))
    manage_attendance(input)
