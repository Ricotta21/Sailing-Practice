import pyxel
import math
import random

class Clock:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        self.sec = 0
        self.min = 0

    def update(self):
        self.sec = pyxel.frame_count // 30
        self.min = self.sec // 60

    def draw(self):
        pyxel.text(self.x, self.y, "Time: %02d:%02d" % (self.min, self.sec % 60), self.c)

class App:
    def __init__(self):
        pyxel.init(250, 250)
        pyxel.load("my_resource.pyxres")

        self.frag = 1
        self.icon_x = 115
        self.icon_y = 220
        self.icon_speed = 0.5
        self.is_space_pressed = False
        self.icon_angle = math.pi / 4  # 45度の角度
        self.clock = Clock(0, 0, 0)
        self.circles = self.initialize_circles()
        self.goal_crossed_count = 0  # ゴールラインを通過した回数をカウントする変数
        self.game_over = False  # ゲームオーバーフラグ

    def run(self):
        pyxel.run(self.update, self.draw)

    def update(self):
        if not self.game_over:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.is_space_pressed = True

            if self.is_space_pressed:
                # アイコンが円に触れているかを確認
                for circle in self.circles:
                    x, y, radius, _ = circle
                    if (
                        self.icon_x + 23 >= x - radius
                        and self.icon_x <= x + radius
                        and self.icon_y + 35 >= y - radius
                        and self.icon_y <= y + radius
                    ):
                        self.icon_speed = 1.1  # 円に触れていれば速度を増加
                        break
                    else:
                        self.icon_speed = 0.5  # 円に触れていなければ速度をリセット

                # アイコンの位置を更新（XおよびYの角度成分に基づいて）
                if pyxel.btnp(pyxel.KEY_SPACE):
                    self.frag += 1

                if self.frag % 2 == 0:
                    self.icon_x += self.icon_speed * math.cos(self.icon_angle)
                    self.icon_y -= self.icon_speed * math.sin(self.icon_angle)
                else:
                    self.icon_x -= self.icon_speed * math.cos(self.icon_angle)
                    self.icon_y -= self.icon_speed * math.sin(self.icon_angle)

                # 画面外にアイコンが出た場合、巻き戻す
                if self.icon_x < -23:
                    self.icon_x = pyxel.width
                elif self.icon_x > pyxel.width:
                    self.icon_x = -23

                if self.icon_y < -35:
                    if self.icon_x > 30 and self.icon_x < 230:
                        self.goal_crossed_count += 1  # ゴールラインを通過した
                        if self.goal_crossed_count == 3:
                            self.game_over = True
                    self.icon_y = 220
                    # 新しい円をランダムに生成
                    self.circles = self.initialize_circles()

                self.clock.update()

    def draw(self):
        pyxel.cls(12)

        # 円を描画
        for circle in self.circles:
            x, y, radius, color = circle
            pyxel.circ(x, y, radius, color)

        # アイコンを描画
        pyxel.blt(self.icon_x, self.icon_y, 0, 0, 0, 23, 35, 0)

        # ゴールとスタートラインを描画
        self.draw_lines()

        self.clock.draw()

        # ゲームオーバーを描画
        if self.game_over:
            pyxel.text(100, 100, "Thank you for enjoying sailing!!", 7)

    def initialize_circles(self):
        circles = []
        for _ in range(8):
            x = random.randint(0, pyxel.width - 1)
            y = random.choice(range(20, 210))
            radius = random.randint(8, 30)
            color = pyxel.COLOR_NAVY
            circles.append((x, y, radius, color))
        return circles

    def draw_lines(self):
        pyxel.text(20, 10, "GOAL.", 7)
        pyxel.text(20, 210, "START.", 7)
        pyxel.line(30, 20, 230, 20, 8)  # ゴールライン
        start_line_y = 210 + 10
        pyxel.line(30, start_line_y, 230, start_line_y, 8)  # スタートライン

        # 追加：ゴールラインとスタートライン上のポイントを描画
        pyxel.pset(30, 20, 8)  # ゴールライン上のポイント
        pyxel.pset(230, 20, 8)  # ゴールライン上のポイント
        pyxel.pset(30, start_line_y, 8)  # スタートライン上のポイント
        pyxel.pset(230, start_line_y, 8)  # スタートライン上のポイント

App().run()
