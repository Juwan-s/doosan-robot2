# pick and place in 1 method. from pos1 to pos2 @20241104

import rclpy
import DR_init

# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 60, 60

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("dsr_example_demo_py", namespace=ROBOT_ID)

    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import (
            get_current_posx,
            set_tool,
            set_tcp,
            movej,
            movel,
            DR_FC_MOD_REL,
            DR_AXIS_Z,
            DR_BASE,
        )

        from DR_common2 import posx, posj

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    JReady = posj([0, 0, 90, 0, 90, 0])
    pos1 = posx([496.06, 93.46, 296.92, 20.75, 179.00, 19.09])
    pos2 = posx([548.70, -193.46, 96.92, 20.75, 179.00, 19.09])
    pos3 = posx([596.70, -7.46, 196.92, 20.75, 179.00, 19.09])

    set_tool("Tool Weight_2FG")
    set_tcp("2FG_TCP")

    if rclpy.ok():

        movej(JReady, vel=VELOCITY, acc=ACC)
        print("current position1 : ", get_current_posx())
        movel(pos1, vel=VELOCITY, acc=ACC)
        print("current position2 : ", get_current_posx())
        movel(pos2, vel=VELOCITY, acc=ACC)
        print("current position3 : ", get_current_posx())
        movel(pos3, vel=VELOCITY, acc=ACC)
        print("current position4 : ", get_current_posx())
        movej(JReady, vel=VELOCITY, acc=ACC)
        print("current position1 : ", get_current_posx())

    rclpy.shutdown()


if __name__ == "__main__":
    main()
