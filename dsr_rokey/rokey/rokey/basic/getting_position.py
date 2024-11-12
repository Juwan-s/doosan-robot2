# pick and place in 1 method. from pos1 to pos2 @20241104

import rclpy

# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 100, 100


import DR_init

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("move_periodic", namespace=ROBOT_ID)

    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import (
            set_tool,
            set_tcp,
            movej,
            DR_TOOL,
            amove_periodic,
        )

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    JReady = [0, 0, 90, 0, 90, 0]

    while rclpy.ok():
        set_tool("Tool Weight_RG2")
        set_tcp("RG2_TCP")

        movej(JReady, vel=VELOCITY, acc=ACC)
        amove_periodic(amp=[0, 0, 0, 0, 0, 30], period=1.0, atime=0.02, repeat=3, ref=DR_TOOL)

        rclpy.shutdown()


if __name__ == "__main__":
    main()
