# pick and place in 1 method. from pos1 to pos2 @20241104

import DR_init

ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL



import rclpy

from rclpy.node import Node
from std_msgs.msg import Float64MultiArray

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

        def timer_callback(self):
            msg = Float64MultiArray()
            msg.data = get_current_posj()
            msg.data = [round(num, 2) for num in msg.data]
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: "%s"' % msg.data)
            self.i += 1


    set_velx(30, 20)
    set_accx(60, 40)

    while rclpy.ok():

        temp = PosjStatePublisher()

        rclpy.spin(temp)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
