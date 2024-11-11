# pick and place in 1 method. from pos1 to pos2 @20241104

import DR_init

ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

import matplotlib
matplotlib.use('Agg') 

import rclpy

from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import matplotlib.pyplot as plt
import numpy as np
import cv2

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("dsr_rokey_posj_py", namespace=ROBOT_ID)

    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import get_tool_force, set_velx, set_accx, get_current_posj

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return
    

    class PosjStatePublisher(Node):

        def __init__(self):
            super().__init__('posj_publisher', namespace=ROBOT_ID)
            self.publisher_ = self.create_publisher(Float64MultiArray, 'Posj_State_Publisher', 10)
            timer_period = 0.5  # seconds
            self.timer = self.create_timer(timer_period, self.timer_callback)
            self.i = 0

            self.image_publisher_ = self.create_publisher(Image, 'force_graph_image', 10)
            self.bridge = CvBridge()
            self.force_data = [[] for _ in range(6)]
            self.max_data_points = 10  # 그래프에 표시할 최대 데이터 포인트 수
            

        def timer_callback(self):
            msg = Float64MultiArray()
            msg.data = get_current_posj()
            msg.data = [round(num, 2) for num in msg.data]
            self.publisher_.publish(msg)
                        
            #self.get_logger().info('Publishing: "%s"' % msg.data)
            #self.i += 1

            force = get_tool_force()
            for i, f in enumerate(force):
                self.force_data[i].append(f)
                if len(self.force_data[i]) > self.max_data_points:
                    self.force_data[i].pop(0)
            if len(self.force_data) > 1:
                self.publish_force_graph_image()
        
        def publish_force_graph_image(self):
            plt.figure(figsize=(8, 4))

            # 각 force 데이터 시리즈를 다른 색상으로 그래프에 추가, 마커 없이 선만 표시
            labels = [f'Force {i}' for i in range(6)]  # 각 force 데이터에 대한 레이블

            for i, data_series in enumerate(self.force_data):
                plt.plot(data_series, label=labels[i])

            plt.legend(loc="upper right")
            plt.xticks([])
            plt.yticks([])
            
            # 그래프를 OpenCV 이미지로 변환
            plt.draw()
            graph_image = np.frombuffer(plt.gcf().canvas.tostring_rgb(), dtype=np.uint8)
            graph_image = graph_image.reshape(plt.gcf().canvas.get_width_height()[::-1] + (3,))
            plt.close()

            # OpenCV 이미지를 ROS 이미지로 변환 후 발행
            ros_image = self.bridge.cv2_to_imgmsg(graph_image, encoding="rgb8")
            self.image_publisher_.publish(ros_image)


    set_velx(30, 20)
    set_accx(60, 40)

    while rclpy.ok():

        temp = PosjStatePublisher()

        rclpy.spin(temp)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
