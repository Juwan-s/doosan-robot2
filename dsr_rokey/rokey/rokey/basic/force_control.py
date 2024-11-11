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
    node = rclpy.create_node("dsr_rokey_basic_py", namespace=ROBOT_ID)

    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import (
            release_compliance_ctrl,
            check_force_condition,
            task_compliance_ctrl,
            set_desired_force,
            get_desired_posx,
            set_velx,
            set_accx,
            set_tool,
            set_tcp,
            movej,
            movel,
            get_current_posx,
            DR_FC_MOD_REL,
            DR_AXIS_Z,
            DR_BASE,
        )

        from DR_common2 import posx, posj

    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    pos1_u = posx([496.06, 93.46, 96.92, 20.75, 179.00, 19.09])
    pos2_u = posx([548.70, 93.46, 96.92, 20.75, 179.00, 19.09])
    pos3_u = posx([596.70, 93.46, 96.92, 20.75, 179.00, 19.09])

    # 초기 위치
    JReady = [0, 0, 90, 0, 90, 0]

    set_velx(30, 20)
    set_accx(60, 40)

    while rclpy.ok():
        # set_tool("Tool Weight_2FG")
        # set_tcp("2FG_TCP")

        movej(JReady, v=30, a=30)

        movel(pos1_u, v=50, a=30)

        print('Move complete')
        a = get_current_posx()

        print()

        print(a)
        # # 초기 위치로 이동
        # movej(JReady, vel=VELOCITY, acc=ACC)

        # for i, pos in enumerate([pos1_u, pos2_u, pos3_u]):
        #     movel(pos, vel=VELOCITY, acc=ACC, ref=DR_BASE)
        #     task_compliance_ctrl(stx=[500, 500, 500, 100, 100, 100])
        #     set_desired_force(fd=[0, 0, -10, 0, 0, 0], dir=[0, 0, 1, 0, 0, 0], mod=DR_FC_MOD_REL)
        #     while not check_force_condition(DR_AXIS_Z, max=5):
        #         pass
        #     release_compliance_ctrl()
        #     print(f"current position{i}: {get_desired_posx()}")

        # movej(JReady, vel=VELOCITY, acc=ACC)

        # [[496.05999755859375], 0, 0, 0, 0, 0], 2

        rclpy.shutdown()


if __name__ == "__main__":
    main()
