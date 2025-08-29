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


class TestAttendance(unittest.TestCase):
    def test_equal_result(self):
        file_name = "attendance_weekday_500.txt"
        input = load_file(os.path.join(ROOT_DIR, file_name))
        result = manage_attendance(input)
        expected = '''NAME : Umar, POINT : 48, GRADE : SILVER
NAME : Daisy, POINT : 45, GRADE : SILVER
NAME : Alice, POINT : 61, GRADE : GOLD
NAME : Xena, POINT : 91, GRADE : GOLD
NAME : Ian, POINT : 23, GRADE : NORMAL
NAME : Hannah, POINT : 127, GRADE : GOLD
NAME : Ethan, POINT : 44, GRADE : SILVER
NAME : Vera, POINT : 22, GRADE : NORMAL
NAME : Rachel, POINT : 54, GRADE : GOLD
NAME : Charlie, POINT : 58, GRADE : GOLD
NAME : Steve, POINT : 38, GRADE : SILVER
NAME : Nina, POINT : 79, GRADE : GOLD
NAME : Bob, POINT : 8, GRADE : NORMAL
NAME : George, POINT : 42, GRADE : SILVER
NAME : Quinn, POINT : 6, GRADE : NORMAL
NAME : Tina, POINT : 24, GRADE : NORMAL
NAME : Will, POINT : 36, GRADE : SILVER
NAME : Oscar, POINT : 13, GRADE : NORMAL
NAME : Zane, POINT : 1, GRADE : NORMAL

Removed player
==============
Bob
Zane'''
        self.assertEqual(result, expected)  # add assertion here


if __name__ == '__main__':
    unittest.main()
