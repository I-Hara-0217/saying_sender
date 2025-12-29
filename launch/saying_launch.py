import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        # 送信機の起動
        launch_ros.actions.Node(
            package='saying_sender',
            executable='quotes_publisher',
            name='publisher_node'
        ),
        # 受信機の起動
        launch_ros.actions.Node(
            package='saying_sender',
            executable='quotes_subscriber',
            name='subscriber_node'
        ),
    ])
