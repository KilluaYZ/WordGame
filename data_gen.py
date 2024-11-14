# 生成题目的数据

from enum import Enum
import random 
import sys
import math 

VERTICAL = 'v'
VERTICAL_REVERSE = 'vr'
HORIZONTAL = 'h'
HORIZONTAL_REVERSE = 'hr'
SPACE = "0"
BARRIER = "1"
ANY = "*"
class Line:
    def __init__(self, row: int, col: int, type: str, length:int, is_correct = False):
        self.row = row
        self.col = col 
        self.type = type 
        self.length = length 
        self.content: list[str] = []
        self.content_conflict: list[bool] = [False for _ in range(self.length)]
        self.is_correct = is_correct
        self.fill_ratio = 0
        self.has_star = False

class BoardBuilder:
    def __init__(self, max_row: int, max_col: int, word: str):
        self.max_row = max_row
        self.max_col = max_col
        self.word = word
        self.line_list: list[Line] = []
        self.line_list_correct: list[Line] = []
        self.board = [[BARRIER for _ in range(self.max_col)] for _ in range(self.max_row)]
    
    def _check_if_line_exists(self, _line:Line) -> bool:
        for line in self.line_list:
            if line.row == _line.row and line.col == _line.col and line.type == _line.type:
                return True
        return False 
    
    def _random_gen_line(self):
        line_row = random.randint(0, self.max_row - 1)
        line_col = random.randint(0, self.max_col - 1)
        line_type = random.choice(['v', 'vr', 'h', 'hr'])
        max_length = -1
        if line_type == HORIZONTAL:
            max_length = self.max_col - line_col
        elif line_type == HORIZONTAL_REVERSE:
            max_length = line_col + 1
        elif line_type == VERTICAL:
            max_length = self.max_row - line_row 
        elif line_type == VERTICAL_REVERSE:
            max_length = line_row + 1
        line_length = random.randint(1, max_length)
        return Line(line_row, line_col, line_type, line_length)
    
    def _alloc_line(self, _line: Line) -> bool:
        if(self._validate_line(_line)):
            self.line_list.append(_line)
            if _line.is_correct:
                self.line_list_correct.append(_line)
            return True 
        return False
    
    def _check_if_covered(self, _line: Line) -> bool:
        for line in self.line_list:
            # 使用比较严格的限制条件
            if line.type == HORIZONTAL and (_line.type == HORIZONTAL or _line.type == HORIZONTAL_REVERSE) and line.row == _line.row and _line.col >= line.col and _line.col < line.col + line.length:
                return True
            if line.type == HORIZONTAL_REVERSE and (_line.type == HORIZONTAL or _line.type == HORIZONTAL_REVERSE)  and line.row == _line.row and _line.col <= line.col and _line.col > line.col - line.length:
                return True
            if line.type == VERTICAL and (_line.type == VERTICAL or _line.type == VERTICAL_REVERSE)  and line.col == _line.col and _line.row >= line.row and _line.row < line.row + line.length:
                return True
            if line.type == VERTICAL_REVERSE and (_line.type == VERTICAL or _line.type == VERTICAL_REVERSE)  and line.col == _line.col and _line.row <= line.row and _line.row > line.row - line.length:
                return True
        return False
    
    def _validate_line(self, _line: Line) -> bool:
        # 检查是不是很小
        if _line.length < 2:
            return False
        
        # 进行检查是否会导致越界
        if(_line.row >= self.max_row or _line.row < 0 or _line.col >= self.max_col):
            return False
        if(_line.type == VERTICAL and _line.row + _line.length - 1 >= self.max_row):
            return False
        if(_line.type == VERTICAL_REVERSE and _line.row - _line.length + 1 < 0):
            return False
        if(_line.type == HORIZONTAL and _line.col + _line.length - 1 >= self.max_col):
            return False
        if(_line.type == HORIZONTAL_REVERSE and _line.col - _line.length + 1 < 0):
            return False
        
        # 检查该格子上是否已经分配过type一样的line
        if(self._check_if_line_exists(_line)):
            return False 
        
        # 检查该格子的起点是否被已分配的line覆盖
        if(self._check_if_covered(_line)):
            return False
        
        # 满足约束条件，返回True
        return True 
    
    def _get_random_alpha(self) -> str:
        return random.choice('abcdefghijklmnopqrstuvwxyz')
    
    def _get_random_alpha_exclude(self, excludes: list[str]):
        alpha_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                      'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                      'w', 'x', 'y', 'z',]
        excluded_alpha_list = list(set(alpha_list) - set(excludes))
        return random.choice(excluded_alpha_list)
    
    # 为_line填入字母，让这些line一定不会被匹配
    def _fill_line_with_error_ans(self, _line: Line):
        # 如果这个空的长度和目标单词的长度不等
        # 那么一定不会填入到这个空里面，所以我们只需要随机地往里面加入一些字母就好
        for i in range(_line.length):
            if(random.random() > 0.7):
                _line.content.append(self._get_random_alpha())
            else:
                _line.content.append(SPACE)
        has_diff = False
        content_length = min(len(_line.content), len(self.word))
        for i in range(content_length):
            if (_line.content[i] != SPACE 
                    and _line.content[i] != self.word[i]
                    and _line.content[content_length - i - 1] != SPACE 
                    and _line.content[content_length - i - 1] != self.word[i]
                    ):
                has_diff = True
                break 
        if not has_diff:
            # 如果没有不一致的地方，那么我们需要手动调整
            edit_idx = random.randint(0, content_length - 1)
            _line.content[edit_idx] = self._get_random_alpha_exclude([self.word[edit_idx]])
            _line.content[content_length - edit_idx - 1] = self._get_random_alpha_exclude([self.word[edit_idx]])
    
    def _fill_line_with_correct_ans(self, _line: Line):
        # 先全部填入0
        _line.content = [SPACE for _ in range(_line.length)]
        fill_num = int(math.ceil(_line.fill_ratio * _line.length))
        not_conflict_num = _line.content_conflict.count(False)
        fill_num = min(fill_num, not_conflict_num)
        choose_idx = []
        while len(choose_idx) < fill_num:
            idx = random.randint(0, _line.length - 1)
            if idx not in choose_idx and not _line.content_conflict[idx]:
                choose_idx.append(idx)
        for idx in choose_idx:
            _line.content[idx] = self.word[idx]
        if _line.has_star:
            for i in range(_line.length):
                if _line.content[i] == SPACE:
                    _line.content[i] = ANY
                    break
    
    def _update_map_with_c_line(self, _map:dict, _c_idx: int):
        _c_line = self.line_list_correct[_c_idx]
        for i in range(_c_line.length):
            _col = _c_line.col
            _row = _c_line.row
            
            if _c_line.type == HORIZONTAL:
                _col = _col + i
            elif _c_line.type == HORIZONTAL_REVERSE:
                _col = _col - i 
            elif _c_line.type == VERTICAL:
                _row = _row + i
            elif _c_line.type == VERTICAL_REVERSE:
                _row = _row - i 
                
            if (_row, _col) not in _map:
                _map[(_row, _col)] = []
            _map[(_row, _col)].append({
                "line_idx": _c_idx,
                "content_idx": i,
            })
    
    def _update_c_line_conflict_with_map(self, _map: dict):
        for key, val in _map.items():
            _row, _col = key 
            is_conflict = False 
            for i in range(len(val)):
                for j in range(len(val)):
                    i_line_idx = val[i]["line_idx"]
                    i_content_idx = val[i]["content_idx"]
                    j_line_idx = val[j]["line_idx"]
                    j_content_idx = val[j]["content_idx"]
                    if i < j and i_content_idx != j_content_idx:
                        is_conflict = True
            # 如果发现冲突，那么就把所有line的这个位置的flag都置为True
            if is_conflict:
                for i in range(len(val)):
                    i_line_idx = val[i]["line_idx"]
                    i_content_idx = val[i]["content_idx"]
                    self.line_list_correct[i_line_idx].content_conflict[i_content_idx] = True
    
    def _analyse_lines_conflict(self):
        _map = {}
        for _idx in range(len(self.line_list_correct)):
            self._update_map_with_c_line(_map, _idx)
        self._update_c_line_conflict_with_map(_map)
    
    def _fill_lines_with_correct_ans(self):
        # 先分析line的冲突情况
        self._analyse_lines_conflict()
        # 获取到冲突情况之后再进行填充
        for _c_line in self.line_list_correct:
            self._fill_line_with_correct_ans(_c_line)
        
    
    def _random_gen_line_correct(self, ratio: float, has_star = False) -> Line:
        # 生成正确的答案
        alloc_success = False 
        for _ in range(100):
            _line = self._random_gen_line()
            if _line.length < len(self.word):
                continue
            _line.is_correct = True
            _line.fill_ratio = ratio
            _line.length = len(self.word)
            _line.has_star = has_star
            _line.content_conflict = [False for _ in range(_line.length)]
            # self._fill_line_with_correct_ans(_line, ratio)
            if(self._alloc_line(_line)):
                alloc_success = True
                break
        if not alloc_success:
            raise RuntimeError("failed to generate right ans")
    
    def random_gen_lines(self):
        # 决定要生成多少个Line
        # max_num = int(math.ceil(self.max_row * self.max_col / 6))
        max_num = 10000
        min_num = int(max_num / 2)
        line_num = random.randint(min_num, max_num)
        
        # 分配line的大小和范围
        for i in range(line_num):
            if(not self._alloc_line(self._random_gen_line())):
                i = i - 1

        # 填入line的内容，这时候要保证填入的所有line都不是正确的答案
        for i in range(len(self.line_list)):
            self._fill_line_with_error_ans(self.line_list[i])
        
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.1)
        self._random_gen_line_correct(.2)
        self._random_gen_line_correct(.2)
        self._random_gen_line_correct(.2)
        self._random_gen_line_correct(.2)
        self._random_gen_line_correct(.2)
        self._random_gen_line_correct(.2)
        self._random_gen_line_correct(.2)
        self._random_gen_line_correct(.2)
        self._random_gen_line_correct(.3)
        self._random_gen_line_correct(.3)
        self._random_gen_line_correct(.3)
        self._random_gen_line_correct(.3)
        self._random_gen_line_correct(.3)
        self._random_gen_line_correct(.3)
        self._random_gen_line_correct(.3)
        self._random_gen_line_correct(.3)
        self._random_gen_line_correct(.3)
        self._random_gen_line_correct(.3)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.4)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.5)
        self._random_gen_line_correct(.8)
        self._fill_lines_with_correct_ans()
        
    def _write_line(self, _line: Line):
        if _line.type == HORIZONTAL:
            for i in range(_line.length):
                self.board[_line.row][_line.col + i] = _line.content[i]
        elif _line.type == HORIZONTAL_REVERSE:
            for i in range(_line.length):
                self.board[_line.row][_line.col - i] = _line.content[i]
        elif _line.type == VERTICAL:
            for i in range(_line.length):
                self.board[_line.row + i][_line.col] = _line.content[i]
        elif _line.type == VERTICAL_REVERSE:
            for i in range(_line.length):
                self.board[_line.row - i][_line.col] = _line.content[i]
        print(f"line_row = {_line.row} line_col = {_line.col} line_length = {_line.length} line_type = {_line.type}", file=sys.stderr)

    def _set_board(self, _row:int, _col:int, val: str):
        if _row >=0 and _row < self.max_row and _col >=0 and _col < self.max_col:
            self.board[_row][_col] = val

    def _add_barrier_on_both_sides_of_line(self, _line: Line):
        _row1, _row2, _col1, _col2 = _line.row, _line.row, _line.col, _line.col
        if _line.type == HORIZONTAL:
            _col1 = _col1 - 1
            _col2 = _col2 + _line.length
        elif _line.type == HORIZONTAL_REVERSE:
            _col1 = _col1 + 1 
            _col2 = _col2 - _line.length
        elif _line.type == VERTICAL:
            _row1 = _row1 - 1
            _row2 = _row2 + _line.length
        elif _line.type == VERTICAL_REVERSE:
            _row1 = _row1 + 1
            _row2 = _row2 - _line.length
        
        self._set_board(_row1, _col1, BARRIER)
        self._set_board(_row2, _col2, BARRIER)
        

    def gen_board(self):
        # 需要先随机地生成一些可以填的空格
        self.random_gen_lines()

        # 将line_list中的所有line的值都放到board中
        for line in self.line_list:
            if line.length != len(self.word) and not line.is_correct:
                self._write_line(line)
        for line in self.line_list:
            if line.length == len(self.word) and not line.is_correct:
                self._write_line(line)
        for line in self.line_list_correct:
            self._write_line(line)
        for line in self.line_list_correct:
            self._add_barrier_on_both_sides_of_line(line)
        
    def print(self):
        for _row in self.board:
            for _col in _row:
                print(f"{_col} ", end="")
            print("")

if __name__ == "__main__":
    row = 1200
    col = 1200
    # word = "supercalifragilisticexpialidocious"
    word = "pneumonoultramicroscopicsilicovolcanoconiosis"
    # word = "pneumonoultramicroscopicsilicovolcanoconiosispneumonoultramicroscopicsilicovolcanoconiosis"
    # word = "antidisestablishmentarianism"
    # word = "information"
    # word = "iloverucandschoolofinfomationverymuch"
    bb = BoardBuilder(row, col, word)
    bb.gen_board()
    print(f"{row} {col}")
    bb.print()
    print(word)