import os


class FileManager:
    def load_file(self, file_path):
        if not os.path.exists(file_path):
            print("파일을 찾을 수 없습니다.")
            return []

        input = []
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    input.append(parts)
        return input


class Player:
    # constants
    WEEK_DAYS = 7

    def __init__(self, name):
        self.name = name
        self.point = 0
        self.grade = GradeFactory().make_grade_manager()
        self.attendance_num = [0] * self.WEEK_DAYS
        self.should_remain = False

    def set_attendanced(self, day):
        self.attendance_num[self.get_day_index(day)] += 1
        if self.is_essential(day):
            self.set_should_remain()
        point = self.get_points(day)
        self.add_point(point)

    def set_should_remain(self):
        self.should_remain = True

    def add_point(self, point):
        self.point += point
        self.grade.set_grade(self.point)

    def get_day_index(self, day):
        week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        return week.index(day)

    def get_player_info(self):
        return f"NAME : {self.name}, POINT : {self.point}, GRADE : {self.grade.get_string()}"

    def get_attendance_info(self, day):
        day = self.get_day_index(day)
        return self.attendance_num[day]

    def is_essential(self, day):
        essential_day = ["wednesday", "saturday", "sunday"]
        if day in essential_day:
            return True
        return False

    def get_points(self, day):
        if day == "wednesday":
            return 3
        elif day in ["saturday", "sunday"]:
            return 2
        return 1

    def should_remove(self):
        return self.grade.is_normal() and not self.should_remain

    def add_bonus_point(self):
        bonus_point = self.get_bonus_point()
        self.point += bonus_point

    def get_bonus_point(self):
        bonus_point = 0
        if self.need_wednesday_bonus():
            bonus_point += 10
        if self.need_weekend_bonus():
            bonus_point += 10
        return bonus_point

    def need_weekend_bonus(self):
        return self.get_attendance_info("saturday") + self.get_attendance_info("sunday") > 9

    def need_wednesday_bonus(self):
        return self.get_attendance_info("wednesday") > 9


class AttendanceManager:
    def __init__(self):
        self.players = {}

    def set_attendance(self, name, day):
        player = self.get_player(name)
        player.set_attendanced(day)

    def get_player(self, name):
        if name not in self.players:
            self.register_player(name)
        self.register_player(name)
        return self.players[name]

    def register_player(self, name):
        if name in self.players:
            return
        self.players[name] = Player(name)

    def manage_attendance(self, attendance_history):
        result = []
        for name, day in attendance_history:
            self.set_attendance(name, day)

        for player in self.players.values():
            player.add_bonus_point()
            result.append(player.get_player_info())

        result.append("\nRemoved player")
        result.append("==============")
        for player in self.players.values():
            if player.should_remove():
                result.append(player.name)
        print("\n".join(result))
        return "\n".join(result)  # for test


class GradeFactory:
    @staticmethod
    def make_grade_manager():
        return GradeManager()  # if rule is change, add factory


class GradeManager:
    def __init__(self):
        self.grade = 0

    def set_grade(self, point):
        if point >= 50:
            self.grade = 2
        elif point >= 30:
            self.grade = 1
        else:
            self.grade = 0

    def get_string(self):
        if self.grade == 0:
            return "NORMAL"
        elif self.grade == 1:
            return "SILVER"
        elif self.grade == 2:
            return "GOLD"

    def is_normal(self):
        return self.grade == 0


if __name__ == "__main__":
    if os.path.dirname(__file__) == '':
        CURRENT_DIR = os.getcwd()
    else:
        CURRENT_DIR = os.path.dirname(__file__)
    file_name = "attendance_weekday_500.txt"
    file_manager = FileManager()
    input = file_manager.load_file(os.path.join(CURRENT_DIR, file_name))

    attendance_manager = AttendanceManager()
    attendance_manager.manage_attendance(input)
