# pick and place in 1 method. from pos1 to pos2 @20241104

import rclpy
import DR_init

import numpy as np

# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 60, 60

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
            movel,
            DR_BASE,
            movesx,
            DR_MVS_VEL_CONST,
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

    JReady = [0, 0, 90, 0, 90, 0]
    
    movej(JReady, vel=VELOCITY, acc=ACC)

    points1 = [277.145, 7.384, 34.081, 109.384, 179.97, 109.228]
    points2 = [707.81, 7.384, 34.081, 109.384, 179.97, 109.228]
    period = points2[0] - points1[0]

    x = np.arange(0, 2 * np.pi, 0.1)
    y = np.sin(x)

    x *= period / (2 * np.pi)
    y *= period / (2 * np.pi)

    x += points1[0]
    y += points1[1]

    sine_list = []
    for i in range(len(x)):
        pos = [x[i], y[i]] + points1[2:] 
        sine_list.append(posx(pos))

    print(len(sine_list))
    
    movesx(sine_list, vel=[100, 30], acc=[100, 60], ref=DR_BASE, vel_opt=DR_MVS_VEL_CONST)
    print("Done")
    movej(JReady, vel=VELOCITY, acc=ACC)
    rclpy.shutdown()


if __name__ == "__main__":
    main()