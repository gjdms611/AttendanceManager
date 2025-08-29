import unittest
import sys
import os

if os.path.dirname(__file__) == '':
    CURRENT_DIR = os.getcwd()
else:
    CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(ROOT_DIR)
from attendance import *


class TestAttendanceManager(unittest.TestCase):
    def setUp(self):
        self.attendance = AttendanceManager()

    def test_manage_attendance(self):
        input = [
            ('test1', 'tuesday'),
            ('test1', 'tuesday'),
            ('test1', 'tuesday'),
            ('test1', 'tuesday'),
            ('test1', 'tuesday')
        ]
        result = self.attendance.manage_attendance(input)
        expected = '''NAME : test1, POINT : 5, GRADE : NORMAL

Removed player
==============
test1'''

        self.assertEqual(result, expected)


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("test_player")

    def test_get_day_index(self):
        self.assertEqual(self.player.get_day_index("monday"), 0)
        self.assertEqual(self.player.get_day_index("tuesday"), 1)
        self.assertEqual(self.player.get_day_index("wednesday"), 2)
        self.assertEqual(self.player.get_day_index("thursday"), 3)
        self.assertEqual(self.player.get_day_index("friday"), 4)
        self.assertEqual(self.player.get_day_index("saturday"), 5)
        self.assertEqual(self.player.get_day_index("sunday"), 6)

    def test_should_remove(self):
        self.assertTrue(self.player.should_remove())
        self.player.add_point(30)
        self.assertFalse(self.player.should_remove())
        self.player.add_point(20)
        self.assertFalse(self.player.should_remove())
        self.player.point = 0
        self.player.grade.set_grade(0)
        self.player.set_should_remain()
        self.assertFalse(self.player.should_remove())
        self.player.add_point(30)
        self.assertFalse(self.player.should_remove())

    def test_get_player_info(self):
        result = self.player.get_player_info()
        expected = "NAME : test_player, POINT : 0, GRADE : NORMAL"
        self.assertEqual(result, expected)

        self.player.add_point(30)
        result = self.player.get_player_info()
        expected = "NAME : test_player, POINT : 30, GRADE : SILVER"
        self.assertEqual(result, expected)

        self.player.add_point(20)
        result = self.player.get_player_info()
        expected = "NAME : test_player, POINT : 50, GRADE : GOLD"
        self.assertEqual(result, expected)

    def test_set_attendanced(self):
        week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        for day in week:
            self.player.should_remain = False
            self.assertEqual(self.player.get_attendance_info(day), 0)
            self.player.set_attendanced(day)
            self.assertEqual(self.player.should_remain, self.player.is_essential(day))
            self.assertEqual(self.player.get_attendance_info(day), 1)

    def test_get_bonus_point(self):
        self.assertEqual(self.player.get_bonus_point(), 0)
        self.player.attendance_num[self.player.get_day_index("wednesday")] = 9
        self.assertEqual(self.player.get_bonus_point(), 0)
        self.player.attendance_num[self.player.get_day_index("wednesday")] = 10
        self.assertEqual(self.player.get_bonus_point(), 10)
        self.player.attendance_num[self.player.get_day_index("wednesday")] = 11
        self.assertEqual(self.player.get_bonus_point(), 10)
        self.player.attendance_num[self.player.get_day_index("saturday")] = 9
        self.assertEqual(self.player.get_bonus_point(), 10)
        self.player.attendance_num[self.player.get_day_index("saturday")] = 10
        self.assertEqual(self.player.get_bonus_point(), 20)
        self.player.attendance_num[self.player.get_day_index("saturday")] = 11
        self.assertEqual(self.player.get_bonus_point(), 20)

        self.player.attendance_num[self.player.get_day_index("saturday")] = 0
        self.player.attendance_num[self.player.get_day_index("sunday")] = 9
        self.assertEqual(self.player.get_bonus_point(), 10)
        self.player.attendance_num[self.player.get_day_index("sunday")] = 10
        self.assertEqual(self.player.get_bonus_point(), 20)
        self.player.attendance_num[self.player.get_day_index("sunday")] = 11
        self.assertEqual(self.player.get_bonus_point(), 20)

        self.player.attendance_num[self.player.get_day_index("saturday")] = 5
        self.player.attendance_num[self.player.get_day_index("sunday")] = 5
        self.assertEqual(self.player.get_bonus_point(), 20)


class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.test_path = os.path.join(CURRENT_DIR, "test_files")
        os.makedirs(self.test_path, exist_ok=True)

    @staticmethod
    def clear_test_files(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
        pass

    def test_load_file(self):
        file_manager = FileManager()
        result = file_manager.load_file("non_exist.txt")
        self.assertEqual(result, [])

        expected = [
            ["Umar", "monday"],
            ["Daisy", "tuesday"],
            ["Alice", "tuesday"],
            ["Xena", "saturday"],
            ["Ian", "tuesday"],
            ["Hannah", "monday"],
            ["Hannah", "thursday"],
            ["Ethan", "wednesday"],
            ["Xena", "wednesday"],
            ["Daisy", "tuesday"],
            ["Vera", "saturday"],
            ["Xena", "sunday"]
        ]
        file_path = os.path.join(self.test_path, "existing_file.txt")
        with open(file_path, "w") as f:
            f.write("\n".join((f"{a} {b}" for a, b in expected)))

        result = file_manager.load_file(file_path)
        self.assertEqual(result, expected)

class TestGradeManager(unittest.TestCase):
    def setUp(self):
        self.grade_manager = GradeManager()

    def test_get_grade_normal(self):
        self.grade_manager.set_grade(0)
        self.assertEqual(self.grade_manager.get_string(), "NORMAL")

        self.grade_manager.point = 29
        self.assertEqual(self.grade_manager.get_string(), "NORMAL")

    def test_get_grade_silver(self):
        self.grade_manager.set_grade(30)
        self.assertEqual(self.grade_manager.get_string(), "SILVER")

        self.grade_manager.set_grade(31)
        self.assertEqual(self.grade_manager.get_string(), "SILVER")

        self.grade_manager.set_grade(49)
        self.assertEqual(self.grade_manager.get_string(), "SILVER")

    def test_get_grade_gold(self):
        self.grade_manager.set_grade(50)
        self.assertEqual(self.grade_manager.get_string(), "GOLD")

        self.grade_manager.set_grade(51)
        self.assertEqual(self.grade_manager.get_string(), "GOLD")


if __name__ == '__main__':
    unittest.main()
