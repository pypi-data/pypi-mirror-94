#! /usr/bin/env python3
# coding: utf-8
"""
日本語とアルファベットの対応表を扱うモジュールです。
"""


def main():
    """呼び出されても特に何もしない"""
    print('平仮名とアルファベットの対応表を扱うモジュールです。')


def load(path, encoding='utf-8'):
    """テーブルを読み取ってインスタンス生成"""
    # ファイル読み取り
    try:
        with open(path, mode='r', encoding=encoding) as f:
            l = [v.strip().split() for v in f.readlines()]
    except UnicodeDecodeError:
        try:
            with open(path, mode='r', encoding='sjis') as f:
                l = [v.strip().split() for v in f.readlines()]
        except UnicodeDecodeError:
            with open(path, mode='r', encoding='utf-8') as f:
                l = [v.strip().split() for v in f.readlines()]
    # 辞書にする
    d = {}
    for v in l:
        d[v[0]] = v[1:]
    return d


if __name__ == '__main__':
    main()

if __name__ == '__init__':
    print('utaupy.table imported')
