import rclpy
import DR_init

import tkinter as tk
from tkinter import messagebox


# for single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 10, 10

DR_init.dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL

pos = None

global pos1_u, pos2_u, entries1


def main(args=None):
    global pos
    rclpy.init(args=args)
    node = rclpy.create_node("dsr_jog", namespace=ROBOT_ID)

    DR_init.__dsr__node = node

    try:
        from DSR_ROBOT2 import movej, get_current_posj
    except ImportError as e:
        print(f"Error importing DSR_ROBOT2 : {e}")
        return

    def move_by_joint(entries_j):
        inputs = [float(entry.get()) for entry in entries_j]
        pos = [d for d in inputs[:-2]]
        movej(pos, vel=float(inputs[-2]), acc=float(inputs[-1]))

    print("create UI")
    root = tk.Tk()
    root.title("Pos 설정")

    joint_data = []
    default_values = get_current_posj() + [VELOCITY, ACC]
    default_values = [round(d, 3) for d in default_values]
    labels_text = ["J1", "J2", "J3", "J4", "J5", "J6", "Speed", "Acc"]

    for i, (label_text, default_value) in enumerate(zip(labels_text, default_values)):
        label = tk.Label(root, text=label_text.center(max(map(len, labels_text))))
        label.grid(row=i, column=0, padx=10, pady=5)

        entry = tk.Entry(root, width=10)
        entry.insert(0, str(default_value))  # 기본값 설정
        entry.grid(row=i, column=1, padx=10, pady=5)
        joint_data.append(entry)

    # 버튼
    joint = tk.Button(root, text="movej", command=lambda: move_by_joint(joint_data))
    joint.grid(row=8, column=0, columnspan=4, pady=10)

    root.mainloop()


if __name__ == "main":
    # UI 생성
    main()
