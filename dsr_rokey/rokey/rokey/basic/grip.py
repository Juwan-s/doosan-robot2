# pick and place in 1 method. from pos1 to pos2 @20241104

import rclpy
import DR_init

# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 60, 60

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

ON, OFF = 1, 0


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("grip_simple", namespace=ROBOT_ID)

    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import (
            set_digital_output,
            get_digital_input,
            set_tool,
            set_tcp,
            movej,
            wait,
        )

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    def wait_digital_input(sig_num):
        while not get_digital_input(sig_num):
            wait(0.5)
            print("Wait for digital input")
            pass

    def release():
        set_digital_output(2, ON)
        set_digital_output(1, OFF)
        wait_digital_input(2)

    def grip():
        release()
        set_digital_output(1, ON)
        set_digital_output(2, OFF)
        wait_digital_input(1)

    set_tool("Tool Weight_2FG")
    set_tcp("2FG_TCP")

    # 초기 위치
    JReady = [0, 0, 90, 0, 90, 0]
    movej(JReady, vel=VELOCITY, acc=ACC)

    while rclpy.ok():
        grip()
        release()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
