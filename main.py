# main.py
import tkinter as tk


def main():
    root = tk.Tk()
    root.title("My App")
    label = tk.Label(root, text="Hello, DMG!")
    label.pack(padx=20, pady=20)
    root.mainloop()


if __name__ == "__main__":
    main()
