#include <cstdio>
#include <cstring>
#include <iostream>
using namespace std;

// 空格子
const char space = '0';
// 障碍格子
const char barrier = '1';
// 能与任意小写字母匹配的格子
const char anychar = '*';
// 题目中所给的数据最大范围
const int MAX_SIZE = 2005;

// 存储最优的放置方式
int max_start_col = -1, max_end_row = -1, max_end_col = -1, max_start_row = -1;
int max_space_num = -1;

// 将board声明为全局变量，因为全局变量可以分配的内存上限更大一些，我们题目要求的内存比较大，如果分配为局部变量可能会爆
char board[MAX_SIZE][MAX_SIZE] = {0};
char word[MAX_SIZE];
int m, n, word_length;

// 检查是否能够被水平放置，row是放置的行，col是放置的列，
// reverse为false的话是从左到右放，reverse为true的话是从右到左放
bool can_place_horizontal(int row, int col, bool reverse) {
  int row_max_length = m;
  int col_max_length = n;
  // 检查这个位置能否放下一个单词，如果放不下了则直接返回
  if (!reverse && col + word_length > col_max_length)
    return false;

  if (reverse && col - word_length + 1 < 0)
    return false;

  // 检查最左边和最右边相邻格子是不是障碍格子
  int neighbor_row1 = row;
  int neighbor_col1 = reverse ? col - word_length : col + word_length;
  int neighbor_row2 = row;
  int neighbor_col2 = reverse ? col + 1 : col - 1;

  if (neighbor_col1 >= 0 && neighbor_col1 < col_max_length &&
      board[neighbor_row1][neighbor_col1] != barrier)
    return false;
  if (neighbor_col2 >= 0 && neighbor_col2 < col_max_length &&
      board[neighbor_row2][neighbor_col2] != barrier)
    return false;

  // 检查要放置的这几个格子里的内容是否合法
  for (int i = 0; i < word_length; i++) {
    char tmp = reverse ? board[row][col - i] : board[row][col + i];
    if (tmp == barrier)
      // 如果要放置的格子里出现了障碍格子，直接返回，
      // 因为word不能放置在障碍格子里
      return false;
    else if (tmp == space || tmp == anychar) {
      // 如果要放置的格子里是空格或者*，那么就继续往下搜索
    } else {
      // 如果要放置的格子里是英文字母，那就与word对应的位进行比较
      if (tmp != word[i])
        return false; // 如果发现不匹配，则返回false
    }
  }
  // 检查通过，返回true
  return true;
}

// 检查是否能够被竖直放置，row是放置的行，col是放置的列，
// reverse为false的话是从上到下放，reverse为true的话是从下到上放
bool can_place_vertical(int row, int col, bool reverse) {
  int row_max_length = m;
  int col_max_length = n;
  // 检查这个位置能否放下一个单词，如果放不下了则直接返回
  if (!reverse && row + word_length > row_max_length)
    return false;

  if (reverse && row - word_length + 1 < 0)
    return false;

  // 检查最上边和最下边相邻格子是不是障碍格子
  int neighbor_row1 = reverse ? row - word_length : row + word_length;
  int neighbor_col1 = col;
  int neighbor_row2 = reverse ? row + 1 : row - 1;
  int neighbor_col2 = col;

  if (neighbor_row1 >= 0 && neighbor_row1 < row_max_length &&
      board[neighbor_row1][neighbor_col1] != barrier)
    return false;
  if (neighbor_row2 >= 0 && neighbor_row2 < row_max_length &&
      board[neighbor_row2][neighbor_col2] != barrier)
    return false;

  // 检查要放置的这几个格子里的内容是否合法
  for (int i = 0; i < word_length; i++) {
    char tmp = reverse ? board[row - i][col] : board[row + i][col];
    if (tmp == barrier)
      // 如果要放置的格子里出现了障碍格子，直接返回，
      // 因为word不能放置在障碍格子里
      return false;
    else if (tmp == space || tmp == anychar) {
      // 如果要放置的格子里是空格或者*，那么就继续往下搜索
    } else {
      // 如果要放置的格子里是英文字母，那就与word对应的位进行比较
      if (tmp != word[i])
        return false; // 如果发现不匹配，则返回false
    }
  }
  // 检查通过，返回true
  return true;
}

// 统计当前放置方案剩余的空格子数，然后更新最优的放置方式
void update_max(int start_row, int start_col, int end_row, int end_col) {
  int space_num = 0;
  // 为了方便后面用统一的for循环对从上到下和从下到上（从左到右和从右到左）
  // 两种方式进行空格子的统计，我们声明了_start_row, _start_col, _end_row,
  // _end_col，保证_start_row <= _end_row, _start_col <= _end_col
  int _start_row = start_row;
  int _start_col = start_col;
  int _end_row = end_row;
  int _end_col = end_col;
  if (start_row > end_row) {
    _start_row = end_row;
    _end_row = start_row;
  }
  if (start_col > end_col) {
    _start_col = end_col;
    _end_col = start_col;
  }

  // 使用for循环遍历整个棋盘
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      // 我们要排除该方案要填入的那几个格子，因为那几个格子被填入后，
      // 全部都会是英文字母，不会有空格子，所以需要排除
      if (!(i >= _start_row && i <= _end_row && j >= _start_col &&
            j <= _end_col) &&
          board[i][j] == space) {
        space_num++;
      }
    }
  }

  // 如果当前方案统计得出的空格子数比最优的方案还要多
  // 那么我们就更新最优方案，这里要用>而不用>=
  // 是为了遇到多个填入后剩余空格子相同的方案时，保存第一次遇到的方案
  // 从而保证如果一个word在board的相同格子的水平方向（竖直方向）上
  // 存在从左到右和从右到左（从上到下和从下到上）都合法的填入方式，
  // 优先选择从左到右（从上到下）的填入方式
  if (space_num > max_space_num) {
    max_space_num = space_num;
    max_start_row = start_row;
    max_start_col = start_col;
    max_end_row = end_row;
    max_end_col = end_col;
  }
}

void placeWordInCrossword(string word) {
  int word_length = word.size();
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      // 如果该格子是障碍格子，那肯定没法放置word，直接跳过
      if (board[i][j] == barrier)
        continue;
      // 为了能够保证规则7，下面的探索顺序也要注意一下
      // 探索是否可以水平从左到右放置
      if (can_place_horizontal(i, j, false)) {
        update_max(i, j, i, j + word_length - 1);
      }
      // 探索是否可以水平从右到左放置
      if (can_place_horizontal(i, j, true)) {
        update_max(i, j, i, j - word_length + 1);
      }
      // 探索是否可以竖直从上到下放置
      if (can_place_vertical(i, j, false)) {
        update_max(i, j, i + word_length - 1, j);
      }
      // 探索是否可以竖直从下到上放置
      if (can_place_vertical(i, j, true)) {
        update_max(i, j, i - word_length + 1, j);
      }
    }
  }
}

int main() {
  cin >> m >> n;
  for (int i = 0; i < m; i++) {
    for (int j = 0; j < n; j++) {
      cin >> board[i][j];
    }
  }
  cin >> word;
  word_length = strlen(word);
  placeWordInCrossword(word);
  if (max_space_num != -1) {
    // 如果有最优的放置方案，那么输出该方案
    cout << max_start_row << " " << max_start_col << endl;
    cout << max_end_row << " " << max_end_col << endl;
  } else {
    // 如果不存在放置方案，那么输出No
    cout << "No" << endl;
  }
  return 0;
}
