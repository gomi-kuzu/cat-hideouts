# title: CatHideOuts Shell Game
# author: CatHideOuts
# desc: A three-shell game hosted by a pixel-art black cat
# site: https://gomi-kuzu.github.io/cat-hideouts/
# license: MIT
# version: 1.0

import pyxel
import math
import random

# ── 定数 ──
SCREEN_W = 200
SCREEN_H = 180
FPS = 30

# カップ位置
CUP_Y = 110
CUP_POSITIONS = [40, 100, 160]  # 3つのカップのX座標
CUP_W = 32
CUP_H = 28

# ゲーム状態
STATE_TITLE = 0
STATE_SHOW_COIN = 1       # コインを見せるフェーズ
STATE_HIDE_COIN = 2       # カップを被せる
STATE_SHUFFLE = 3         # シャッフル中
STATE_CHOOSE = 4          # プレイヤー選択
STATE_REVEAL = 5          # 結果発表
STATE_RESULT = 6          # 最終結果表示

# BGM情報
BGM_LABEL = "Tansaku01"

# 色
COL_BG = 1          # 濃紺
COL_BLACK = 0
COL_WHITE = 7
COL_GRAY = 5
COL_DARK_GRAY = 13
COL_PURPLE = 2
COL_CUP = 4         # 茶色
COL_CUP_DARK = 2    # 暗い紫（カップ影）
COL_GOLD = 10        # コイン色
COL_GOLD_DARK = 9    # コイン影
COL_CAT_EYE = 10     # 猫の目（黄色）
COL_ACCENT = 12      # アクセント青
COL_GREEN = 3        # 成功
COL_RED = 8          # 失敗
COL_PINK = 14        # ピンク


class ShellGame:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="CatHideOuts Shell Game", fps=FPS)

        # ── サウンド定義（Pyxel内蔵音源）──
        self._init_sounds()

        # ── ゲーム状態 ──
        self.state = STATE_TITLE
        self.frame = 0
        self.coin_pos = 1           # コインがある位置（0,1,2）
        self.cup_positions = list(CUP_POSITIONS)  # 現在のカップX座標
        self.cups_lifted = [False, False, False]  # カップが持ち上がっているか

        # シャッフル
        self.shuffle_swaps = []     # (i, j) のスワップリスト
        self.shuffle_index = 0
        self.shuffle_frame = 0
        self.shuffle_speed = 15     # フレーム数/1回のスワップ
        self.shuffle_count = 0      # 総シャッフル回数

        # 選択
        self.cursor = 1
        self.selected = -1
        self.reveal_frame = 0

        # アニメーション
        self.cat_blink = 0
        self.cat_talk_frame = 0
        self.message = ""
        self.message_timer = 0

        # 得点
        self.score = 0
        self.round = 0
        self.max_rounds = 5

        # 難易度
        self.difficulty = 0  # 0: easy, 1: normal, 2: hard

        # BGM再生中フラグ
        self.bgm_playing = False

        # PCM音源のゲイン調整（デフォルト0.125は小さいので上げる）
        pyxel.channels[0].gain = 0.6

        pyxel.run(self.update, self.draw)

    # ═══════════════════════════════════════════
    #  サウンド初期化
    # ═══════════════════════════════════════════
    def _init_sounds(self):
        # Sound 0: カップ移動音（短いスライド音）
        pyxel.sounds[0].set(
            "c3e3", "pp", "32", "nn", 8
        )
        # Sound 1: コイン配置音
        pyxel.sounds[1].set(
            "e3g3c4", "ppp", "333", "nnn", 10
        )
        # Sound 2: 成功ジングル！
        pyxel.sounds[2].set(
            "c3e3g3c4e4g4c4", "ppppppp", "3333332", "nnnnnnn", 8
        )
        # Sound 3: 失敗音
        pyxel.sounds[3].set(
            "c3b2a2g2f2e2d2", "ttttttt", "3333333", "sssssss", 10
        )
        # Sound 4: カーソル移動音
        pyxel.sounds[4].set(
            "g4", "p", "2", "n", 5
        )
        # Sound 5: 決定音
        pyxel.sounds[5].set(
            "c4e4", "pp", "33", "nn", 5
        )
        # Sound 6: BGM（CatHideOuts 探索１ OGGファイル）
        pyxel.sounds[6].pcm("assets/002_tansaku01.ogg")
        # Sound 7: (未使用 - BGMはSound 6のみ)
        # Sound 8: タイトル画面ジングル
        pyxel.sounds[8].set(
            "c3r e3r g3r c4c4 r r",
            "pp pp pp pppp p p",
            "33 33 33 3332 3 3",
            "nn nn nn nnnn n n",
            12
        )
        # Sound 9: シャッフル開始音
        pyxel.sounds[9].set(
            "c3d3e3f3g3a3b3c4", "pppppppp", "22222222", "nnnnnnnn", 6
        )
        # Sound 10: カップ持ち上げ音
        pyxel.sounds[10].set(
            "g3c4e4", "ppp", "332", "nnn", 8
        )

        # Music 0: BGM（CatHideOuts 探索１）
        pyxel.musics[0].set([6], [], [], [])

    # ═══════════════════════════════════════════
    #  リセット
    # ═══════════════════════════════════════════
    def reset_round(self):
        self.coin_pos = random.randint(0, 2)
        self.cup_positions = list(CUP_POSITIONS)  # cup_positions[i] = カップIDiの現在X座標
        self.cups_lifted = [False, False, False]
        self.shuffle_swaps = []
        self.shuffle_index = 0
        self.shuffle_frame = 0
        self.cursor = 1         # リセット直後はslot1が物理中央（CUP_POSITIONS[1]=100）
        self.selected = -1
        if self.round < 2:
            self.shuffle_count = 3 + self.round
            self.shuffle_speed = 18
        elif self.round < 4:
            self.shuffle_count = 5 + self.round
            self.shuffle_speed = 12
        else:
            self.shuffle_count = 8 + self.round
            self.shuffle_speed = 8

        # シャッフルリスト生成
        self._generate_shuffles()

    def _generate_shuffles(self):
        self.shuffle_swaps = []
        prev = -1
        for _ in range(self.shuffle_count):
            pair = random.choice([(0, 1), (1, 2), (0, 2)])
            # 同じスワップが連続しないように
            while pair == prev:
                pair = random.choice([(0, 1), (1, 2), (0, 2)])
            self.shuffle_swaps.append(pair)
            prev = pair

    def reset_game(self):
        self.score = 0
        self.round = 0
        self.reset_round()

    # ═══════════════════════════════════════════
    #  UPDATE
    # ═══════════════════════════════════════════
    def update(self):
        self.frame += 1

        # 猫の瞬き
        if self.frame % 120 == 0:
            self.cat_blink = 6

        if self.cat_blink > 0:
            self.cat_blink -= 1

        # メッセージタイマー
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ""

        if self.state == STATE_TITLE:
            self._update_title()
        elif self.state == STATE_SHOW_COIN:
            self._update_show_coin()
        elif self.state == STATE_HIDE_COIN:
            self._update_hide_coin()
        elif self.state == STATE_SHUFFLE:
            self._update_shuffle()
        elif self.state == STATE_CHOOSE:
            self._update_choose()
        elif self.state == STATE_REVEAL:
            self._update_reveal()
        elif self.state == STATE_RESULT:
            self._update_result()

    def _update_title(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.play(3, 8)
            self.reset_game()
            self.state = STATE_SHOW_COIN
            self.frame = 0
            # BGM開始
            pyxel.playm(0, loop=True)
            self.bgm_playing = True

    def _update_show_coin(self):
        # コインを見せてから自動で次へ
        if self.frame == 30:
            pyxel.play(2, 1)
            self.message = "ここにコインを入れるにゃ！"
            self.message_timer = 60
            self.cat_talk_frame = 60
        if self.frame > 90:
            self.state = STATE_HIDE_COIN
            self.frame = 0

    def _update_hide_coin(self):
        # カップを被せるアニメーション
        if self.frame > 30:
            self.message = "よく見ているにゃ..."
            self.message_timer = 60
            self.cat_talk_frame = 60
            pyxel.play(2, 9)
            self.state = STATE_SHUFFLE
            self.frame = 0
            self.shuffle_index = 0
            self.shuffle_frame = 0

    def _update_shuffle(self):
        self.shuffle_frame += 1

        if self.shuffle_index < len(self.shuffle_swaps):
            i, j = self.shuffle_swaps[self.shuffle_index]
            progress = self.shuffle_frame / self.shuffle_speed

            if progress >= 1.0:
                # スワップ完了
                self.cup_positions[i], self.cup_positions[j] = self.cup_positions[j], self.cup_positions[i]
                self.shuffle_index += 1
                self.shuffle_frame = 0
                pyxel.play(2, 0)
            else:
                # スワップアニメーション中: 円弧を描いて移動
                pass  # draw側で処理
        else:
            # シャッフル完了
            self.state = STATE_CHOOSE
            self.frame = 0
            self.message = "どのカップかにゃ？"
            self.message_timer = 120
            self.cat_talk_frame = 120

    def _update_choose(self):
        # 物理的なX座標順にソートしたスロット一覧（左→右）
        sorted_slots = sorted(range(3), key=lambda i: self.cup_positions[i])
        cur_rank = sorted_slots.index(self.cursor)

        if pyxel.btnp(pyxel.KEY_LEFT):
            self.cursor = sorted_slots[(cur_rank - 1) % 3]
            pyxel.play(2, 4)
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.cursor = sorted_slots[(cur_rank + 1) % 3]
            pyxel.play(2, 4)
        elif pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.selected = self.cursor
            pyxel.play(2, 5)
            self.state = STATE_REVEAL
            self.frame = 0
            self.reveal_frame = 0

        # マウス対応
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx = pyxel.mouse_x
            my = pyxel.mouse_y
            for idx in range(3):
                cx = self.cup_positions[idx]
                if cx - CUP_W // 2 <= mx <= cx + CUP_W // 2 and CUP_Y - CUP_H <= my <= CUP_Y + 10:
                    self.selected = idx
                    pyxel.play(2, 5)
                    self.state = STATE_REVEAL
                    self.frame = 0
                    self.reveal_frame = 0
                    break

    def _update_reveal(self):
        self.reveal_frame += 1

        if self.reveal_frame == 10:
            pyxel.play(2, 10)

        if self.reveal_frame == 40:
            # coin_pos = コインが入っているカップのID
            # cup_positions[coin_pos] = そのカップの現在X座標
            coin_cup_index = self.coin_pos

            if self.selected == coin_cup_index:
                self.score += 1
                self.message = "正解にゃ！すごいにゃ！"
                self.cat_talk_frame = 90
                pyxel.stop()
                self.bgm_playing = False
                pyxel.play(0, 2)
            else:
                self.message = "残念にゃ～..."
                self.cat_talk_frame = 90
                pyxel.stop()
                self.bgm_playing = False
                pyxel.play(0, 3)

            self.message_timer = 120
            self.state = STATE_RESULT
            self.frame = 0

    def _update_result(self):
        if self.frame > 60:
            if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.round += 1
                if self.round >= self.max_rounds:
                    # ゲーム終了 → タイトルへ
                    self.state = STATE_TITLE
                    self.frame = 0
                    if self.bgm_playing:
                        pyxel.stop()
                        self.bgm_playing = False
                else:
                    self.reset_round()
                    self.state = STATE_SHOW_COIN
                    self.frame = 0
                    if not self.bgm_playing:
                        pyxel.playm(0, loop=True)
                        self.bgm_playing = True

    # ═══════════════════════════════════════════
    #  DRAW
    # ═══════════════════════════════════════════
    def draw(self):
        pyxel.cls(COL_BG)

        if self.state == STATE_TITLE:
            self._draw_title()
        else:
            self._draw_game()

    # ─── タイトル画面 ───
    def _draw_title(self):
        # 背景装飾
        for i in range(20):
            x = (i * 37 + self.frame) % (SCREEN_W + 20) - 10
            y = (i * 23 + self.frame // 2) % (SCREEN_H + 20) - 10
            pyxel.pset(x, y, COL_DARK_GRAY)

        # タイトル
        pyxel.text(52, 20, "CatHideOuts", COL_ACCENT)
        pyxel.text(42, 32, "Shell Game", pyxel.frame_count % 16)

        # 黒猫（大きめ）
        self._draw_cat_large(100, 65)

        # カップのイラスト
        for i, x in enumerate([55, 100, 145]):
            offset = int(math.sin(self.frame * 0.05 + i) * 3)
            self._draw_cup(x, 115 + offset, False)

        # 説明
        pyxel.text(28, 138, "3つのカップからコインを", COL_WHITE)
        pyxel.text(46, 148, "見つけるゲームだにゃ！", COL_WHITE)

        # ボタン
        blink = self.frame % 40 < 30
        if blink:
            pyxel.text(32, 164, "CLICK or ENTER to START", COL_ACCENT)

        # 前回スコア表示
        if self.round > 0:
            pyxel.text(55, 4, f"Last: {self.score}/{self.max_rounds}", COL_GOLD)

    # ─── ゲーム画面 ───
    def _draw_game(self):
        # ステージ（テーブル）
        pyxel.rect(0, CUP_Y + 12, SCREEN_W, SCREEN_H - CUP_Y - 12, COL_PURPLE)
        pyxel.rect(0, CUP_Y + 10, SCREEN_W, 4, 4)

        # スコア・ラウンド表示
        pyxel.text(4, 4, f"Round {self.round + 1}/{self.max_rounds}", COL_WHITE)
        pyxel.text(150, 4, f"Score: {self.score}", COL_GOLD)

        # 黒猫
        self._draw_cat(100, 18)

        # coin_pos = コインが入っているカップのID
        # cup_positions[coin_pos] = そのカップの現在X座標
        coin_cup_index = self.coin_pos

        # コイン表示条件
        show_coin = False
        if self.state == STATE_SHOW_COIN:
            show_coin = True
        elif self.state == STATE_REVEAL and self.reveal_frame > 15:
            show_coin = True
        elif self.state == STATE_RESULT:
            show_coin = True

        if show_coin:
            coin_x = self.cup_positions[coin_cup_index]
            self._draw_coin(coin_x, CUP_Y + 2)

        # カップ描画
        for idx in range(3):
            cup_x = self.cup_positions[idx]
            lifted = False

            # シャッフル中のアニメーション
            if self.state == STATE_SHUFFLE and self.shuffle_index < len(self.shuffle_swaps):
                i, j = self.shuffle_swaps[self.shuffle_index]
                progress = self.shuffle_frame / self.shuffle_speed
                if idx == i or idx == j:
                    other = j if idx == i else i
                    start_x = self.cup_positions[idx]
                    end_x = self.cup_positions[other]

                    # 円弧を描くアニメーション
                    t = progress
                    arc_x = start_x + (end_x - start_x) * t
                    arc_y_offset = -math.sin(t * math.pi) * 25  # 上に弧を描く
                    self._draw_cup(arc_x, CUP_Y + arc_y_offset, False)
                    continue

            # リヴィール時の持ち上げアニメーション
            if (self.state == STATE_REVEAL or self.state == STATE_RESULT):
                if idx == self.selected:
                    lift = min(self.reveal_frame * 1.5, 35) if self.state == STATE_REVEAL else 35
                    self._draw_cup(cup_x, CUP_Y - lift, False)
                    continue

            # カップをまだ見せない状態
            if self.state == STATE_SHOW_COIN:
                if idx == coin_cup_index:
                    # コインの上にカップを被せるアニメーション
                    if self.frame < 60:
                        # カップは上にある
                        self._draw_cup(cup_x, CUP_Y - 30, False)
                    else:
                        self._draw_cup(cup_x, CUP_Y, False)
                    continue

            self._draw_cup(cup_x, CUP_Y, False)

        # カーソル表示
        if self.state == STATE_CHOOSE:
            cursor_x = self.cup_positions[self.cursor]
            arrow_y = CUP_Y - CUP_H - 12 + int(math.sin(self.frame * 0.15) * 3)
            # 矢印
            pyxel.tri(
                cursor_x, arrow_y + 8,
                cursor_x - 5, arrow_y,
                cursor_x + 5, arrow_y,
                COL_GOLD
            )

        # メッセージ
        if self.message:
            self._draw_message_box(self.message)

        # BGM名表示（画面右下に2倍サイズ）
        if self.bgm_playing:
            bgm_text = f"BGM: {BGM_LABEL}"
            tw = len(bgm_text) * 4 * 2  # 2倍幅
            tx = SCREEN_W - tw - 4
            self._draw_text_2x(tx, SCREEN_H - 16, bgm_text, COL_DARK_GRAY)

        # 結果画面の追加表示
        if self.state == STATE_RESULT and self.frame > 30:
            # 正解・不正解のアイコン
            coin_cup_idx = coin_cup_index
            if self.selected == coin_cup_idx:
                # ○ マーク
                pyxel.circb(self.cup_positions[self.selected], CUP_Y - 50, 12, COL_GREEN)
                # 紙吹雪
                for i in range(15):
                    px = random.randint(0, SCREEN_W)
                    py = random.randint(0, CUP_Y - 10)
                    col = random.choice([COL_GOLD, COL_ACCENT, COL_GREEN, COL_PINK, COL_WHITE])
                    pyxel.pset(px, py, col)
            else:
                # × マーク
                cx = self.cup_positions[self.selected]
                pyxel.line(cx - 8, CUP_Y - 58, cx + 8, CUP_Y - 42, COL_RED)
                pyxel.line(cx - 8, CUP_Y - 42, cx + 8, CUP_Y - 58, COL_RED)

            blink = self.frame % 40 < 30
            if blink:
                if self.round + 1 >= self.max_rounds:
                    pyxel.text(38, SCREEN_H - 22, "CLICK or ENTER for TITLE", COL_ACCENT)
                else:
                    pyxel.text(42, SCREEN_H - 22, "CLICK or ENTER for NEXT", COL_ACCENT)

    # ─── 描画ヘルパー ───

    def _draw_cup(self, x, y, lifted):
        """カップを描画（x, yはカップ底中央）"""
        # カップの影
        pyxel.elli(x - 14, y + 4, 28, 8, COL_BLACK)

        # カップ本体（台形風）
        # 下部
        pyxel.rect(x - 13, y - 8, 26, 10, COL_CUP)
        # 中部
        pyxel.rect(x - 11, y - 18, 22, 12, COL_CUP)
        # 上部
        pyxel.rect(x - 9, y - 24, 18, 8, COL_CUP)
        # つまみ
        pyxel.rect(x - 3, y - 28, 6, 5, COL_CUP)
        pyxel.rect(x - 2, y - 30, 4, 3, COL_GOLD)

        # ハイライト
        pyxel.line(x - 10, y - 22, x - 10, y - 4, COL_CUP_DARK)
        pyxel.line(x + 10, y - 22, x + 10, y - 4, 9)

        # 下の縁
        pyxel.rect(x - 14, y + 2, 28, 3, COL_CUP_DARK)

    def _draw_coin(self, x, y):
        """コインを描画"""
        pyxel.circ(x, y, 5, COL_GOLD)
        pyxel.circb(x, y, 5, COL_GOLD_DARK)
        pyxel.text(x - 2, y - 2, "$", COL_GOLD_DARK)

    def _draw_cat(self, x, y):
        """黒猫（小）を描画 - ゲームマスター"""
        # 体
        pyxel.rect(x - 8, y + 6, 16, 12, COL_BLACK)
        # 頭
        pyxel.circ(x, y + 2, 8, COL_BLACK)
        # 耳（左）
        pyxel.tri(x - 8, y - 2, x - 6, y - 8, x - 3, y - 1, COL_BLACK)
        pyxel.tri(x - 7, y - 2, x - 6, y - 7, x - 4, y - 1, COL_PINK)
        # 耳（右）
        pyxel.tri(x + 8, y - 2, x + 6, y - 8, x + 3, y - 1, COL_BLACK)
        pyxel.tri(x + 7, y - 2, x + 6, y - 7, x + 4, y - 1, COL_PINK)

        # 目
        if self.cat_blink > 0:
            pyxel.line(x - 4, y + 1, x - 2, y + 1, COL_CAT_EYE)
            pyxel.line(x + 2, y + 1, x + 4, y + 1, COL_CAT_EYE)
        else:
            pyxel.rect(x - 5, y, 3, 3, COL_CAT_EYE)
            pyxel.rect(x + 2, y, 3, 3, COL_CAT_EYE)
            # 瞳
            pyxel.pset(x - 4, y + 1, COL_BLACK)
            pyxel.pset(x + 3, y + 1, COL_BLACK)

        # 鼻
        pyxel.pset(x, y + 4, COL_PINK)

        # 口（話している時）
        if self.cat_talk_frame > 0:
            self.cat_talk_frame -= 1
            if self.frame % 8 < 4:
                pyxel.rect(x - 1, y + 5, 3, 2, COL_RED)
            else:
                pyxel.line(x - 1, y + 5, x + 1, y + 5, COL_DARK_GRAY)
        else:
            pyxel.line(x - 1, y + 5, x + 1, y + 5, COL_DARK_GRAY)

        # しっぽ
        tail_wave = math.sin(self.frame * 0.1) * 3
        pyxel.line(x + 8, y + 14, x + 14, y + 10 + tail_wave, COL_BLACK)
        pyxel.line(x + 14, y + 10 + tail_wave, x + 16, y + 8 + tail_wave, COL_BLACK)

    def _draw_cat_large(self, x, y):
        """黒猫（大）を描画 - タイトル画面用"""
        # 体
        pyxel.rect(x - 12, y + 10, 24, 18, COL_BLACK)
        # 頭
        pyxel.circ(x, y + 4, 12, COL_BLACK)
        # 耳（左）
        pyxel.tri(x - 12, y - 3, x - 9, y - 12, x - 5, y - 1, COL_BLACK)
        pyxel.tri(x - 11, y - 3, x - 9, y - 10, x - 6, y - 1, COL_PINK)
        # 耳（右）
        pyxel.tri(x + 12, y - 3, x + 9, y - 12, x + 5, y - 1, COL_BLACK)
        pyxel.tri(x + 11, y - 3, x + 9, y - 10, x + 6, y - 1, COL_PINK)

        # 目
        if self.cat_blink > 0:
            pyxel.line(x - 6, y + 2, x - 3, y + 2, COL_CAT_EYE)
            pyxel.line(x + 3, y + 2, x + 6, y + 2, COL_CAT_EYE)
        else:
            pyxel.rect(x - 7, y, 5, 5, COL_CAT_EYE)
            pyxel.rect(x + 3, y, 5, 5, COL_CAT_EYE)
            # 瞳
            pyxel.rect(x - 6, y + 1, 2, 3, COL_BLACK)
            pyxel.rect(x + 4, y + 1, 2, 3, COL_BLACK)
            # ハイライト
            pyxel.pset(x - 5, y + 1, COL_WHITE)
            pyxel.pset(x + 5, y + 1, COL_WHITE)

        # 鼻
        pyxel.tri(x - 1, y + 6, x + 1, y + 6, x, y + 7, COL_PINK)

        # 口
        if self.cat_talk_frame > 0:
            if self.frame % 8 < 4:
                pyxel.rect(x - 2, y + 8, 4, 3, COL_RED)
            else:
                pyxel.line(x - 2, y + 8, x, y + 9, COL_DARK_GRAY)
                pyxel.line(x, y + 9, x + 2, y + 8, COL_DARK_GRAY)
        else:
            pyxel.line(x - 2, y + 8, x, y + 9, COL_DARK_GRAY)
            pyxel.line(x, y + 9, x + 2, y + 8, COL_DARK_GRAY)

        # ヒゲ
        pyxel.line(x - 14, y + 5, x - 7, y + 6, COL_WHITE)
        pyxel.line(x - 13, y + 8, x - 7, y + 7, COL_WHITE)
        pyxel.line(x + 14, y + 5, x + 7, y + 6, COL_WHITE)
        pyxel.line(x + 13, y + 8, x + 7, y + 7, COL_WHITE)

        # 前足
        pyxel.rect(x - 10, y + 24, 6, 6, COL_BLACK)
        pyxel.rect(x + 4, y + 24, 6, 6, COL_BLACK)
        # 肉球
        pyxel.pset(x - 8, y + 28, COL_PINK)
        pyxel.pset(x + 6, y + 28, COL_PINK)

        # しっぽ
        tail_wave = math.sin(self.frame * 0.08) * 5
        pyxel.line(x + 12, y + 22, x + 20, y + 16 + tail_wave, COL_BLACK)
        pyxel.line(x + 20, y + 16 + tail_wave, x + 24, y + 12 + tail_wave, COL_BLACK)

    def _draw_text_2x(self, x, y, text, col):
        """2倍スケールでテキストを描画（スクラッチ領域方式）"""
        char_w = 4
        char_h = 6
        tw = len(text) * char_w
        # (0,0)のピクセルを退避
        saved = [[pyxel.pget(px, py) for px in range(tw)] for py in range(char_h)]
        # 背景色を敷いてテキスト描画
        bg = (col + 1) % 16
        pyxel.rect(0, 0, tw, char_h, bg)
        pyxel.text(0, 0, text, col)
        # ピクセルを読み取って2倍で描画
        for py in range(char_h):
            for px in range(tw):
                if pyxel.pget(px, py) == col:
                    pyxel.rect(x + px * 2, y + py * 2, 2, 2, col)
        # 退避したピクセルを復元
        for py in range(char_h):
            for px in range(tw):
                pyxel.pset(px, py, saved[py][px])

    def _draw_message_box(self, text):
        """吹き出しメッセージ"""
        tw = len(text) * 4  # 概算幅
        bx = SCREEN_W // 2 - tw // 2 - 6
        by = 50
        bw = tw + 12
        bh = 14

        # 吹き出し背景
        pyxel.rect(bx, by, bw, bh, COL_WHITE)
        pyxel.rectb(bx, by, bw, bh, COL_BLACK)

        # 吹き出しの三角（猫から）
        pyxel.tri(
            SCREEN_W // 2 - 3, by + bh,
            SCREEN_W // 2 + 3, by + bh,
            SCREEN_W // 2, by + bh + 5,
            COL_WHITE
        )
        pyxel.line(SCREEN_W // 2 - 3, by + bh, SCREEN_W // 2, by + bh + 5, COL_BLACK)
        pyxel.line(SCREEN_W // 2 + 3, by + bh, SCREEN_W // 2, by + bh + 5, COL_BLACK)

        # テキスト
        pyxel.text(bx + 6, by + 4, text, COL_BLACK)


ShellGame()
