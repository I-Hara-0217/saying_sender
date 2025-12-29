#!/bin/bash
# SPDX-FileCopyrightText: 2025 Ibuki Hara
# SPDX-License-Identifier: BSD-3-Clause

ng () {
    res=1
}

res=0

source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws
colcon build --packages-select saying_sender
source install/setup.bash

timeout 15s ros2 run saying_sender quotes_publisher > /tmp/saying_sender.log || true

count=$(grep -c "Publish:" /tmp/saying_sender.log)

[ "$count" -ge 3 ] || ng "$LINENO"

[ "$res" = 0 ] && echo OK

exit $res
