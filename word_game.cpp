#include <bits/types/struct_timeval.h>
#include <cstddef>
#include <cstdio>
#include <iostream>
#include <string>
#include <sys/time.h>
#include <vector>
using namespace std;
const char space = '0';
const char barrier = '1';
const char anychar = '*';

int max_start_col = -1, max_end_row = -1, max_end_col = -1, max_start_row = -1;
int max_space_num = -1;

bool can_place_horizonal(vector<vector<char>> &board, string &word, int row,
                         int col, bool reverse) {
  int row_max_length = board.size();
  int col_max_length = board[row].size();
  int length = word.size();
  // 如果长度已经超过了
  if (!reverse && col + length > col_max_length)
    return false;

  if (reverse && col - length + 1 < 0)
    return false;

  for (int i = 0; i < length; i++) {
    char tmp = reverse ? board[row][col - i] : board[row][col + i];
    if (tmp == barrier)
      return false;
    else if (tmp == space || tmp == anychar) {

    } else {
      if (tmp != word[i])
        return false;
    }
  }

  // 检查相邻格子
  int neighbor_row1 = row;
  int neighbor_col1 = reverse ? col - length : col + length;
  int neighbor_row2 = row;
  int neighbor_col2 = reverse ? col + 1 : col - 1;

  if (neighbor_col1 >= 0 && neighbor_col1 < col_max_length &&
      board[neighbor_row1][neighbor_col1] != barrier)
    return false;
  if (neighbor_col2 >= 0 && neighbor_col2 < col_max_length &&
      board[neighbor_row2][neighbor_col2] != barrier)
    return false;

  return true;
}

bool can_place_vertical(vector<vector<char>> &board, string &word, int row,
                        int col, bool reverse) {
  int row_max_length = board.size();
  int col_max_length = board[row].size();
  int length = word.size();
  // 如果长度已经超过了
  if (!reverse && row + length > row_max_length)
    return false;

  if (reverse && row - length + 1 < 0)
    return false;

  for (int i = 0; i < length; i++) {
    char tmp = reverse ? board[row - i][col] : board[row + i][col];
    if (tmp == barrier)
      return false;
    else if (tmp == space || tmp == anychar) {

    } else {
      if (tmp != word[i])
        return false;
    }
  }

  // 检查相邻格子
  int neighbor_row1 = reverse ? row - length : row + length;
  int neighbor_col1 = col;
  int neighbor_row2 = reverse ? row + 1 : row - 1;
  int neighbor_col2 = col;

  if (neighbor_row1 >= 0 && neighbor_row1 < row_max_length &&
      board[neighbor_row1][neighbor_col1] != barrier)
    return false;
  if (neighbor_row2 >= 0 && neighbor_row2 < row_max_length &&
      board[neighbor_row2][neighbor_col2] != barrier)
    return false;
  return true;
}

// 更新最大的
void update_max(vector<vector<char>> &board, int start_row, int start_col,
                int end_row, int end_col) {
  int space_num = 0;
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
  for (int i = 0; i < board.size(); i++) {
    for (int j = 0; j < board[i].size(); j++) {
      if (!(i >= _start_row && i <= _end_row && j >= _start_col &&
            j <= _end_col) &&
          board[i][j] == space) {
        space_num++;
      }
    }
  }
  cout << "Available:" << endl;
  cout << "space num: " << space_num << endl;
  cout << start_row << " " << start_col << endl;
  cout << end_row << " " << end_col << endl;
  if (space_num > max_space_num) {
    max_space_num = space_num;
    max_start_row = start_row;
    max_start_col = start_col;
    max_end_row = end_row;
    max_end_col = end_col;
  }
}

void placeWordInCrossword(vector<vector<char>> &board, string word) {
  int max_row = board.size();
  int max_col = board[0].size();
  int word_length = word.size();
  for (int i = 0; i < board.size(); i++) {
    for (int j = 0; j < board[i].size(); j++) {
      if (can_place_vertical(board, word, i, j, false)) {
        update_max(board, i, j, i + word_length - 1, j);
      }
      if (can_place_vertical(board, word, i, j, true)) {
        update_max(board, i, j, i - word_length + 1, j);
      }
      if (can_place_horizonal(board, word, i, j, false)) {
        update_max(board, i, j, i, j + word_length - 1);
      }
      if (can_place_horizonal(board, word, i, j, true)) {
        update_max(board, i, j, i, j - word_length + 1);
      }
    }
  }
}

int main() {
  struct timeval start, end;
  double mtime;
  gettimeofday(&start, NULL);
  int m, n;
  cin >> m >> n;
  vector<vector<char>> board;
  for (int i = 0; i < m; i++) {
    board.push_back(vector<char>());
    for (int j = 0; j < n; j++) {
      char tmp;
      cin >> tmp;
      board[i].push_back(tmp);
    }
  }

  string word;
  cin >> word;

  placeWordInCrossword(board, word);
  if (max_space_num != -1) {
    cout << "Max:" << endl;
    cout << max_start_row << " " << max_start_col << endl;
    cout << max_end_row << " " << max_end_col << endl;
  } else {
    cout << "No" << endl;
  }
  gettimeofday(&end, NULL);
  mtime = ((end.tv_sec - start.tv_sec) * 1000.0 +
           (end.tv_usec - start.tv_usec) / 1000.0);
  cout << "运行时间：" << mtime << endl;
  return 0;
}
