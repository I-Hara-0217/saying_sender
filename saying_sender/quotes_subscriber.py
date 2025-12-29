#!/usr/bin/python3
# SPDX-FileCopyrightText: 2025 Ibuki Hara
# SPDX-License-Identifier: BSD-3-Clause

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class QuotesSubscriber(Node):
    def __init__(self):
        super().__init__('quotes_subscriber')
        self.subscription = self.create_subscription(
            String,
            'quote_topic',
            self.listener_callback,
            10)
