import tkinter as tk

def check_frame_packing(frame):
    is_packed = frame.winfo_ismapped()
    print(is_packed)
    return is_packed

def pack_frame():
    frame2.pack()
    check_frame_packing(frame2)

def unpack_frame():
    frame2.pack_forget()
    check_frame_packing(frame2)

root = tk.Tk()

frame1 = tk.Frame(root, width=200, height=100, bg="red")
frame1.pack()

frame2 = tk.Frame(root, width=200, height=100, bg="blue")

pack_button = tk.Button(root, text="Pack Frame2", command=pack_frame)
pack_button.pack()

unpack_button = tk.Button(root, text="Unpack Frame2", command=unpack_frame)
unpack_button.pack()

# Initial check before any packing/unpacking
print("Initial - Frame2 is packed:", check_frame_packing(frame2))

root.mainloop()
