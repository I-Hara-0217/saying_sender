#!/bin/bash
# SPDX-FileCopyrightText: 2025 Ibuki Hara
# SPDX-License-Identifier: BSD-3-Clause

# 何か問題が起きたらその場で止まるようにします
set -e

res=0
# 記録が途切れないようにする設定
export PYTHONUNBUFFERED=1
export RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED=1

# OS側の基本的な道具を読み込みます
source /opt/ros/jazzy/setup.bash

# 作業場へ移動して組み立て
cd $HOME/ros2_ws
colcon build --packages-select saying_sender

# 【ここが重要】組み立てたばかりの部品の住所を、絶対パスで確実に読み込ませます
source $HOME/ros2_ws/install/setup.bash

# 実行して記録を取る（少し長めに40秒待ちます）
set +e
timeout 40s ros2 run saying_sender quotes_publisher > /tmp/saying_sender.log 2>&1 || true

# 記録を画面に出して確認
echo "--- 動作の全記録を表示します ---"
cat /tmp/saying_sender.log
echo "------------------------------"

# 送信の合図（Publish:）を数える
count=$(grep -c "Publish:" /tmp/saying_sender.log)
echo "確認された送信回数: $count"

# 判定（3回以上あれば合格）
if [ "$count" -ge 3 ]; then
    echo "検証結果：合格"
    res=0
else
    echo "検証結果：不合格（送信回数が足りない、または部品が見つかりません）"
    res=1
fi

exit $res
