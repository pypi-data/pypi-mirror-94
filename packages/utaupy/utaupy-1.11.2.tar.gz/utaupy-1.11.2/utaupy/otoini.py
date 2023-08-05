#! /usr/bin/env python3
# coding: utf-8
"""
setParam用のINIファイルとデータを扱うモジュールです。
"""
import re
from collections import UserList

# from . import table


def main():
    """実行されたときの挙動"""
    print('耳ロボPとsetParamに卍感謝卍')


def load(path, mode='r', encoding='shift-jis'):
    """otoiniを読み取ってオブジェクト生成"""
    # otoiniファイルを読み取る
    path = path.strip('"')
    with open(path, mode=mode, encoding=encoding) as f:
        l = [re.split('[=,]', s.strip()) for s in f.readlines()]
    # # 入力ファイル末尾の空白行を除去
    # while l[-1] == ['']:
    #     del l[-1]

    # Otoクラスオブジェクトのリストを作る
    otoini = OtoIni()
    for v in l:
        oto = Oto()
        oto.from_otoini(v)
        otoini.append(oto)
    # OtoIniクラスオブジェクト化
    return otoini


class OtoIni(UserList):
    """oto.iniを想定したクラス"""

    def __dict__(self):
        d = {oto.alias: oto for oto in self}
        return d

    @property
    def values(self):
        """中身を確認する"""
        return self

    def replace_aliases(self, before, after):
        """エイリアスを置換する"""
        for oto in self:
            oto.alias = oto.alias.replace(before, after)
        return self

    def is_mono(self):
        """
        モノフォン形式のエイリアスになっているか判定する。
        返り値はbool。
        """
        return all(len(v.alias.split()) == 1 for v in self)

    def as_dict(self):
        """
        辞書に変換して返す。
        エイリアスが重複していると古いほうは消される。
        """
        d = {oto.alias: oto for oto in self}
        return d

    def kana2romaji(self, d_table):
        """
        エイリアスをローマ字にする
        replace:
          Trueのときエイリアスをローマ字に書き換え
          Falseのときエイリアスは平仮名のまま
        """
        for oto in self:
            try:
                oto.alias = ' '.join(d_table[oto.alias])
            except KeyError as e:
                print(f'[ERROR] KeyError in utaupy.otoini.OtoIni.kana2romaji: {e}')

    def monophonize(self):
        """
        音素ごとに分割する。
        otoini→label 変換の用途を想定
        音素の発声開始位置: 左ブランク=先行発声
        """
        # 新規OtoIniを作るために、otoを入れるリスト
        mono_otoini = OtoIni()
        for oto in self:
            phonemes = oto.alias.split()
            if len(phonemes) == 1:
                mono_otoini.append(oto)
            elif len(phonemes) in [2, 3]:
                name_wav = oto.filename
                # 1文字目(オーバーラップから先行発声まで)------------
                mono_oto = Oto()
                mono_oto.filename = name_wav
                mono_oto.alias = phonemes[0]
                mono_oto.offset = oto.offset + oto.overlap  # オーバーラップの位置に左ブランクを移動
                mono_oto.preutterance = 0
                mono_otoini.append(mono_oto)
                # 2文字目(先行発声から固定範囲まで)----------------
                mono_oto = Oto()
                mono_oto.filename = name_wav
                mono_oto.alias = phonemes[1]
                mono_oto.offset = oto.offset + oto.preutterance  # 先行発声の位置に左ブランクを移動
                mono_oto.preutterance = 0
                mono_otoini.append(mono_oto)
                if len(phonemes) == 3:
                    # 3文字目(固定範囲から右ブランクまで)----------------
                    mono_oto = Oto()
                    mono_oto.filename = name_wav
                    mono_oto.alias = phonemes[2]
                    mono_oto.offset = oto.offset + oto.consonant  # 固定範囲の位置に左ブランクを移動
                    mono_oto.preutterance = 0
                    mono_otoini.append(mono_oto)
            else:
                print('\n[ERROR in otoini.monophonize()]----------------')
                print('  エイリアスの音素数は 1, 2, 3 以外対応していません。')
                print('  phonemes: {}'.format(phonemes))
                print('  文字を連結して処理を続行します。')
                print('-----------------------------------------------\n')
                mono_otoini.append(oto)
        return mono_otoini


    def write(self, path, mode='w', encoding='shift-jis'):
        """OtoIniクラスオブジェクトをINIファイルに出力"""
        s = ''
        for oto in self:
            l = []
            l.append(oto.filename)
            l.append(oto.alias)
            l.append(oto.offset)
            l.append(oto.consonant)
            l.append(oto.cutoff)
            l.append(oto.preutterance)
            l.append(oto.overlap)
            # 数値部分を丸めてから文字列に変換
            l = l[:2] + [str(round(float(v), 4)) for v in l[2:]]
            s += '{}={},{},{},{},{},{}\n'.format(*l)  # 'l[0]=l[1],l[2],...'
        with open(path, mode=mode, encoding=encoding) as f:
            f.write(s)
        return s


class Oto:
    """oto.ini中の1モーラ"""

    def __init__(self):
        keys = ('FileName', 'Alias', 'Offset',
                'Consonant', 'Cutoff', 'Preutterance', 'Overlap')
        tpl = (None, None, 0, 0, 0, 0, 0, 0)
        self.__d = dict(zip(keys, tpl))

    def __str__(self):
        return f'\'{self.alias}\'\t<utaupy.otoini.Oto object at {id(self)}>'

    def from_otoini(self, l):
        """1音分のリストをもらってクラスオブジェクトにする"""
        keys = ('FileName', 'Alias', 'Offset',
                'Consonant', 'Cutoff', 'Preutterance', 'Overlap')
        # 数値部分をfloatにする
        l = l[:2] + [float(v) for v in l[2:]]
        self.__d = dict(zip(keys, l))
        return self

    # ここからノートの全値の処理----------------------
    @property
    def values(self):
        """中身を確認する"""
        return self.__d

    @values.setter
    def values(self, d):
        """中身を上書きする"""
        self.__d = d
    # ここまでノートの全値の処理----------------------

    # ここからノートの各値の処理----------------------
    @property
    def filename(self):
        """wavファイル名を確認する"""
        return self.__d['FileName']

    @filename.setter
    def filename(self, x):
        """wavファイル名を上書きする"""
        self.__d['FileName'] = x

    @property
    def alias(self):
        """エイリアスを確認する"""
        return self.__d['Alias']

    @alias.setter
    def alias(self, x):
        """エイリアスを上書きする"""
        self.__d['Alias'] = x

    @property
    def offset(self):
        """左ブランクを確認する"""
        return self.__d['Offset']

    @offset.setter
    def offset(self, x):
        """左ブランクを上書きする"""
        self.__d['Offset'] = x

    # @property
    # def offset2(self):
    #     """左ブランクの値を取得する"""
    #     return self.__d['Offset']
    #
    # @offset2.setter
    # def offset2(self, x):
    #     """
    #     左ブランクの値を上書きする
    #     左ブランクが変化した分だけほかのパラメータの数値を調整するため、
    #     ほかの値の絶対時刻を変化させず、左ブランクだけを移動できる。
    #     """
    #     original_offset = self.__d['Offset']
    #     self.__d['Offset'] = x
    #     dt = self.__d['Offset'] - original_offset
    #     self.__d['Overlap'] += dt
    #     self.__d['Preutterance'] += dt
    #     self.__d['Consonant'] += dt
    #     self.cutoff2 += dt

    @property
    def consonant(self):
        """固定範囲を確認する"""
        return self.__d['Consonant']

    @consonant.setter
    def consonant(self, x):
        """固定範囲を上書きする"""
        self.__d['Consonant'] = x

    @property
    def cutoff(self):
        """
        右ブランク

        正の値のときは、絶対時刻ではなくファイル末尾からの時間
        負の値のときは、その絶対値が左ブランクからの相対位置
        """
        return self.__d['Cutoff']

    @cutoff.setter
    def cutoff(self, x):
        self.__d['Cutoff'] = x

    @property
    def cutoff2(self):
        """
        右ブランクを絶対時刻で取得する
        """
        cutoff = self.__d['Cutoff']
        if cutoff > 0:
            raise ValueError(f'Cutoff(右ブランク) must be negative : {str(self)}')
        return self.__d['Offset'] - cutoff

    @cutoff2.setter
    def cutoff2(self, x):
        """
        右ブランクを絶対時刻で受け取り、負の値で上書きする
        """
        if x < 0:
            raise ValueError(f'Argument "x" must be positive : {x}')
        self.__d['Cutoff'] = self.__d['Offset'] - x

    @property
    def preutterance(self):
        """先行発声を取得する"""
        return self.__d['Preutterance']

    @preutterance.setter
    def preutterance(self, x):
        """先行発声を上書きする"""
        self.__d['Preutterance'] = x

    @property
    def overlap(self):
        """オーバーラップを取得する"""
        return self.__d['Overlap']

    @overlap.setter
    def overlap(self, x):
        """オーバーラップを上書きする"""
        self.__d['Overlap'] = x
    # ここまでノートの各値の処理----------------------


if __name__ == '__main__':
    main()

if __name__ == '__init__':
    pass
