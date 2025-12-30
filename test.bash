#!/bin/bash -xv
# SPDX-FileCopyrightText: 2025 Ibuki Hara
# SPDX-License-Identifier: BSD-3-Clause

ng () {
    echo ${1}行目が違うよ
    res=1
}

res=0

source /opt/ros/jazzy/setup.bash
cd $HOME/ros2_ws

### BUILD TEST ###
colcon build --packages-select saying_sender || ng "$LINENO"
source $HOME/ros2_ws/install/setup.bash

### EXECUTION TEST ###
timeout 10s ros2 run saying_sender quotes_publisher > /tmp/saying_sender.log 2>&1 || true

### OUTPUT CHECK ###
count=$(grep -c "Publish:" /tmp/saying_sender.log)
[ "$count" -ge 1 ] || ng "$LINENO"

[ "$res" = 0 ] && echo OK

exit $res
