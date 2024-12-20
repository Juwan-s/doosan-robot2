# pick and place in 1 method. from pos1 to pos2 @20241104

import rclpy
import DR_init

import numpy as np

# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 200, 200

DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

OFF, ON = 0, 1


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node("force_control", namespace=ROBOT_ID)

    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import (
            set_tool,
            set_tcp,
            movej,
            amovel,
            wait,
            DR_MV_RA_OVERRIDE,
            movel,
        )

        from DR_common2 import posx, posb

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    set_tool("Tool Weight_2FG")
    set_tcp("2FG_TCP")

    # 초기 위치
    JReady = [0, 0, 90, 0, 90, 0]
    movej(JReady, vel=VELOCITY, acc=ACC)
    initial_point = posx(0, 300, 300, 0, 180, 0)
    point1 = posx([259.0, 800.0, 651.5, 101.471, -180.0, 60.645])
    point2 = posx([259.0, -400.0, 651.5, 117.319, -180.0, 76.493])
    point3 = posx([459.0, -400.0, 651.5, 4.128, -180.0, -36.698])
    point4 = posx([659.0, -400.0, 651.5, 4.128, -180.0, -36.698])
    point5 = posx([859.0, -400.0, 651.5, 4.128, -180.0, -36.698])
    point6 = posx([259.0, -400.0, 651.5, 4.128, -180.0, -36.698])

    points = [point1, point2, point3, point4, point5, point6]
    movel(point1, vel=VELOCITY, acc=ACC)
    for i, P in enumerate(points):
        print(f"move to {i}")
        amovel(P, vel=VELOCITY, acc=ACC, ra=DR_MV_RA_OVERRIDE)
        wait(1.0)

    rclpy.shutdown()


if __name__ == "__main__":
    main()
