import rclpy
import DR_init
import tkinter as tk


# Configuration for a single robot
ROBOT_ID = "dsr01"
ROBOT_MODEL = "m0609"
VELOCITY, ACC = 60, 60
ON, OFF = 1, 0

# Initialize DR_init with robot parameters
DR_init.__dsr__id = ROBOT_ID
DR_init.__dsr__model = ROBOT_MODEL


def main(args=None):
    # Initialize the ROS node
    rclpy.init(args=args)
    node = rclpy.create_node("dsr_rokey_basic_py", namespace=ROBOT_ID)
    DR_init.__dsr__node = node

    # Import robot functions
    try:
        from DSR_ROBOT2 import (
            movej,
            movel,
            get_current_posx,
            parallel_axis,
            get_current_posj,
            get_digital_input,
            set_digital_output,
            wait,
            mwait,
            DR_BASE,
            DR_AXIS_Z,
        )
        from DR_common2 import posx, posj
    except ImportError as e:
        print(f"Error importing DSR_ROBOT2: {e}")
        return

    def create_label_entry(root, text, row, col):
        label = tk.Label(root, text=text)
        label.grid(row=row + 1, column=col - 1, padx=10, pady=5)
        entry = tk.Entry(root, width=10)
        entry.insert(0, str(1))
        entry.grid(row=row + 1, column=col)
        return entry

    def create_position_entries(root, labels, default_values, col, min_val=5, max_val=50):
        data_entries = []
        for i, (label_text, default_value) in enumerate(zip(labels, default_values)):
            label = tk.Label(root, text=label_text)
            label.grid(row=i + 1, column=col, padx=10, pady=5)

            if i <= 5:
                entry = tk.Entry(root, width=10)
                entry.insert(0, str(round(default_value, 3)))
                entry.grid(row=i + 1, column=col + 1, padx=10, pady=5)
                data_entries.append(entry)
            else:
                entry = tk.Scale(
                    root, from_=min_val, to=max_val, orient=tk.HORIZONTAL, length=200
                )
                entry.set(default_value)
                entry.grid(row=i + 1, column=col + 1, padx=10, pady=5, columnspan=3)
                data_entries.append(entry)

        return data_entries

    def create_increment_buttons(
        root, joint_data, axes_data, increment_j_value, increment_x_value
    ):
        for i in range(6):
            tk.Button(
                root,
                text="+",
                command=lambda i=i: increment_joint(
                    axes_data, joint_data, i, float(increment_j_value.get())
                ),
            ).grid(row=i + 1, column=2, padx=2, pady=5)
            tk.Button(
                root,
                text="-",
                command=lambda i=i: increment_joint(
                    axes_data, joint_data, i, -float(increment_j_value.get())
                ),
            ).grid(row=i + 1, column=3, padx=2, pady=5)
            tk.Button(
                root,
                text="+",
                command=lambda i=i: increment_linear(
                    axes_data, joint_data, i, float(increment_x_value.get())
                ),
            ).grid(row=i + 1, column=7, padx=2, pady=5)
            tk.Button(
                root,
                text="-",
                command=lambda i=i: increment_linear(
                    axes_data, joint_data, i, -float(increment_x_value.get())
                ),
            ).grid(row=i + 1, column=8, padx=2, pady=5)

    def create_control_buttons(root, joint_data, axes_data):
        tk.Button(
            root, text="movej", command=lambda: move_by_joint(axes_data, joint_data)
        ).grid(row=9, column=1, columnspan=1, pady=10)
        tk.Button(
            root, text="copy", command=lambda: copy_to_clipboard(root, joint_data, "posj")
        ).grid(row=9, column=2, columnspan=1, pady=10)

        print("make movel button")
        tk.Button(
            root, text="movel", command=lambda: move_by_line(axes_data, joint_data)
        ).grid(row=9, column=6, columnspan=1, pady=10)
        tk.Button(
            root, text="copy", command=lambda: copy_to_clipboard(root, axes_data, "posx")
        ).grid(row=9, column=7, columnspan=1, pady=10)

        print("make grip button")
        tk.Button(root, text="grip", command=lambda: grip()).grid(
            row=0, column=0, columnspan=4, pady=10
        )
        tk.Button(root, text="release", command=lambda: release()).grid(
            row=0, column=4, columnspan=4, pady=10
        )

        tk.Button(
            root,
            text="z-axis alignment",
            command=lambda: z_axis_alignment(axes_data, joint_data),
        ).grid(row=11, column=2, columnspan=4, pady=10)

    # Joint and Linear Movement Functions
    def move_by_joint(entries_x, entries_j):
        inputs = [float(entry.get()) for entry in entries_j]
        pos = inputs[:-2]
        is_success = movej(pos, vel=inputs[-2], acc=inputs[-1])
        mwait()
        update_entries(get_current_posx()[0], entries_x)
        update_entries(get_current_posj(), entries_j)

        print("current posx : ", get_current_posx())
        print("current posj : ", get_current_posj())
        print("is_success:", is_success)

    def move_by_line(entries_x, entries_j):
        inputs = [float(entry.get()) for entry in entries_x]
        pos = inputs[:-2]
        is_success = movel(pos, vel=inputs[-2], acc=inputs[-1], ref=DR_BASE)
        mwait()
        update_entries(get_current_posj(), entries_j)
        update_entries(get_current_posx()[0], entries_x)

        print("current posx : ", get_current_posx())
        print("current posj : ", get_current_posj())
        print("is_success:", is_success)

    # Utility to update entry fields
    def update_entries(values, entries):
        for i, val in enumerate(values):
            if val:
                entries[i].delete(0, tk.END)
                entries[i].insert(0, str(round(val, 3)))

    def copy_to_clipboard(root, entries, type_name):
        root.clipboard_clear()
        clipboard_text = (
            f"{type_name}(["
            + ", ".join([str(entry.get()) for entry in entries[:6]])
            + "])"
        )
        root.clipboard_append(clipboard_text)
        print(f"copy to clipboard: {clipboard_text}")
        root.update()

    def z_axis_alignment(axes_data, joint_data):
        vect = [0, 0, -1]
        parallel_axis(vect, DR_AXIS_Z, DR_BASE)
        mwait()
        print("move to z-axis alignment")
        update_entries(get_current_posj(), joint_data)
        update_entries(get_current_posx()[0], axes_data)
        # move_by_line(axes_data, joint_data)

    # Increment functions for joint and linear positions
    def increment_joint(entries_x, entries_j, idx, increment):
        temp = float(entries_j[idx].get())
        print("temp : ", temp, idx)
        entries_j[idx].delete(0, tk.END)
        entries_j[idx].insert(0, str(round(temp + increment, 3)))
        move_by_joint(entries_x, entries_j)

    def increment_linear(entries_x, entries_j, idx, increment):
        temp = float(entries_x[idx].get())
        print("temp : ", temp, idx)
        entries_x[idx].delete(0, tk.END)
        entries_x[idx].insert(0, str(round(temp + increment, 3)))
        move_by_line(entries_x, entries_j)

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

    # UI setup
    root = tk.Tk()
    root.title("Pos 설정")

    # Joint and Axis Position Data(row: 1~8, Joint and Axis Entries)
    print("create_position_entries")
    joint_data, axes_data = create_position_entries(
        root,
        labels=["J1", "J2", "J3", "J4", "J5", "J6", "Speed", "Acc"],
        default_values=get_current_posj() + [VELOCITY, ACC],
        col=0,
        max_val=50,
    ), create_position_entries(
        root,
        labels=["X", "Y", "Z", "Rx", "Ry", "Rz", "Speed", "Acc"],
        default_values=get_current_posx()[0] + [VELOCITY, ACC],
        col=5,
        max_val=100,
    )

    # Control Buttons(row: [0, 9, 11], grip, release, movej, movel, copy, z-axis alignment)
    print("control buttons")
    create_control_buttons(root, joint_data, axes_data)

    # Increment Input Fields(row: 9, Increment Entry)
    increment_j_value = create_label_entry(root, "Joint Increment", 9, 1)
    increment_x_value = create_label_entry(root, "Linear Increment", 9, 6)
    # Increment Buttons(row: 1~7, +- buttons)
    print("increment buttons")
    create_increment_buttons(
        root, joint_data, axes_data, increment_j_value, increment_x_value
    )

    # Run UI
    root.mainloop()


if __name__ == "__main__":
    main()
