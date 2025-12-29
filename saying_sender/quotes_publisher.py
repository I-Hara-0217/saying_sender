#!/usr/bin/python3
# SPDX-FileCopyrightText: 2025 Ibuki Hara
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import random
import os

class QuotesPublisher(Node):
    def __init__(self):
        super().__init__('quotes_publisher')
        self.publisher_ = self.create_publisher(String, 'quote_topic', 10)
        self.timer = self.create_timer(5.0, self.timer_callback)

    def timer_callback(self):
        msg = String()

        # 99分の1の確率で「当たり」のメッセージを出す
        # 確率 P = 1/99
        if random.randint(1, 99) == 99:
            msg.data = "【大当たり】今日はとても良いことがありそうです！"
        else:
            # words.txt のファイルパスを指定
            file_path = os.path.expanduser('~/ros2_ws/src/robosys2025_2/words.txt')
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        # ファイルの中から一行をランダムにチョイス
                        msg.data = random.choice(lines).strip()
                    else:
                        msg.data = "words.txt が空です。"
            except FileNotFoundError:
                msg.data = "words.txt が見つかりません。"

        # データをパブリッシュ（送信）
        self.publisher_.publish(msg)
        # ログに出力
        self.get_logger().info(f'Publish: "{msg.data}"')

    def main(args=None):
    # ROS 2 の通信機能を初期化
    rclpy.init(args=args)
    # QuotesPublisher のインスタンスを作成
    node = QuotesPublisher()
    try:
        # ノードをスピン（実行状態を維持）させてタイマーを動かす
        rclpy.spin(node)
    except KeyboardInterrupt:
        # Ctrl+C で停止した際の処理
        pass

    # ノードを破棄して終了処理を行う
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
