#!/bin/bash
# SPDX-FileCopyrightText: 2025 Ibuki Hara
# SPDX-License-Identifier: BSD-3-Clause

ng () {
    res=1
}

res=0

# 文字化けや記録の遅れを防ぐ設定
export PYTHONUNBUFFERED=1
export RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED=1

source /opt/ros/jazzy/setup.bash
cd ~/ros2_ws
colcon build --packages-select saying_sender
source install/setup.bash

# 実行時間を 40秒 に延ばして、確実に回数を稼げるようにします
timeout 40s ros2 run saying_sender quotes_publisher > /tmp/saying_sender.log 2>&1 || true

# --- ここから追加：何が起きたか記録をすべて表示します ---
echo "--- 動作の全記録を表示します ---"
cat /tmp/saying_sender.log
echo "------------------------------"

# 送信の合図「Publish:」が何回出たか数えます
count=$(grep -c "Publish:" /tmp/saying_sender.log)
echo "確認された送信回数: $count"

# 3回以上あれば合格、なければ不合格
[ "$count" -ge 3 ] || ng "$LINENO"

[ "$res" = 0 ] && echo "検証結果：OK"
[ "$res" = 1 ] && echo "検証結果：不合格（送信回数が足りません）"

exit $res
