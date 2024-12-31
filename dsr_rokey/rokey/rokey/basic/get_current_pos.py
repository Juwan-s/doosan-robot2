import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

import tkinter as tk
from tkinter import StringVar
import threading

from dsr_msgs2.srv import SetRobotMode


def copy_to_clipboard(root, text_box):
    text = text_box.get().strip()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # 클립보드 업데이트


def create_entries(root, default_value, row, col):
    entry_var = StringVar()
    entry_var.set(str(round(default_value, 3)))
    entry = tk.Entry(root, textvariable=entry_var, width=50)
    entry.grid(row=row, column=col, padx=10, pady=5)
    return entry_var


class ServiceClinetNode(Node):
    def __init__(self):
        super().__init__("service_client_node")

        self.cli = self.create_client(SetRobotMode, "/dsr01/system/set_robot_mode")
        while not self.cli.wait_for_service(timeout_sec=1.0):
            print("Waiting for service...")
            pass

    def send_request(self, mode=0):
        request = SetRobotMode.Request()
        request.robot_mode = mode
        future = self.cli.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


class PosTopicSubscriber(Node):
    def __init__(self, text_var1, text_var2):
        super().__init__("PosTopicSubscriber")

        # 메시지 저장 변수 초기화
        self.current_posx_msg = None
        self.joint_state_msg = None

        # Tkinter 텍스트 변수 (GUI 업데이트용)
        self.text_var1 = text_var1
        self.text_var2 = text_var2

        # 토픽 구독 설정
        self.create_subscription(
            Float64MultiArray, "/dsr01/msg/current_posx", self.current_posx_callback, 10
        )
        self.create_subscription(
            Float64MultiArray, "/dsr01/msg/joint_state", self.joint_state_callback, 10
        )

    def current_posx_callback(self, msg):
        self.current_posx_msg = msg
        data = [round(d, 3) for d in self.current_posx_msg.data]
        # 텍스트 박스 업데이트 (첫 번째 텍스트 박스)
        self.text_var1.set(f"posx({data})")

    def joint_state_callback(self, msg):
        self.joint_state_msg = msg
        data = [round(d, 3) for d in self.joint_state_msg.data]
        # 텍스트 박스 업데이트 (두 번째 텍스트 박스)
        self.text_var2.set(f"posj({data})")


def ros_thread(text_var1, text_var2):
    node = PosTopicSubscriber(text_var1, text_var2)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


def main():
    # Tkinter GUI 실행
    root = tk.Tk()
    tk.Label(root, text="current_posx:").grid(row=0, column=0)
    text_var1 = create_entries(root, 0.0, 0, 1)
    tk.Button(root, text="copy", command=lambda: copy_to_clipboard(root, text_var1)).grid(
        row=0, column=3, padx=2, pady=5
    )

    tk.Label(root, text="joint_state:").grid(row=1, column=0)
    text_var2 = create_entries(root, 0.0, 1, 1)
    tk.Button(root, text="copy", command=lambda: copy_to_clipboard(root, text_var2)).grid(
        row=1, column=3, padx=2, pady=5
    )

    # 서비스 실행
    print("Service Start")
    rclpy.init()
    client_node = ServiceClinetNode()
    response = client_node.send_request(0)
    client_node.get_logger().info(f"results: {response}")

    # ROS2 스레드 실행
    ros = threading.Thread(target=ros_thread, args=(text_var1, text_var2))
    ros.start()

    root.mainloop()


if __name__ == "__main__":
    main()
