#!/usr/bin/python3
# SPDX-FileCopyrightText: 2025 Ibuki Hara
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
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
        if random.randint(1, 99) == 99:
            msg.data = "【大当たり】今日はとても良いことがありそうです！"
        else:
            file_path = os.path.expanduser('~/ros2_ws/src/saying_sender/words.txt')
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        msg.data = random.choice(lines).strip()
                    else:
                        msg.data = "words.txt is empty"
            except FileNotFoundError:
                msg.data = "words.txt not found"

        self.publisher_.publish(msg)
        self.get_logger().info(f'Publish: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = QuotesPublisher()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
