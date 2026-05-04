"""
widgets.py — Custom widget reusable untuk Bank of Sains Data.
Responsif: PinPadDialog dan AlertFrame menerima Layout opsional untuk scaling.
"""

import tkinter as tk
from src.image_cache import ImageCache


class PlaceholderEntry(tk.Entry):
    def __init__(self, parent, placeholder: str = "",
                placeholder_color: str = "#777777",
                text_color: str = "black",
                is_password: bool = False, **kwargs):
        super().__init__(parent, **kwargs)
        self._placeholder = placeholder
        self._placeholder_color = placeholder_color
        self._text_color = text_color
        self._is_password = is_password
        self._showing_placeholder = False
        self._insert_placeholder()
        self.bind('<FocusIn>',  self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)

    def _insert_placeholder(self):
        if self._is_password:
            self.config(show='')
        self.insert(0, self._placeholder)
        self.config(fg=self._placeholder_color)
        self._showing_placeholder = True

    def _on_focus_in(self, _=None):
        if self._showing_placeholder:
            self.delete(0, tk.END)
            self.config(fg=self._text_color)
            if self._is_password:
                self.config(show='*')
            self._showing_placeholder = False

    def _on_focus_out(self, _=None):
        if not self.get():
            self._insert_placeholder()

    def get_value(self) -> str:
        return "" if self._showing_placeholder else self.get()


class PinPadDialog:

    def __init__(self, parent, on_submit, on_cancel=None, layout=None,
                image_path: str = "images/Frame 9.png",
                image_size: tuple = (211, 293)):
        self._on_submit = on_submit
        self._on_cancel = on_cancel
        self._L = layout

        if layout is not None:
            actual_size = layout.img(*image_size)
            def sx(v): return layout.px(v)
            def sy(v): return layout.py(v)
            def sf(v): return layout.font(v)
        else:
            actual_size = image_size
            def sx(v): return v
            def sy(v): return v
            def sf(v): return v

        self.frame = tk.Frame(parent)

        try:
            photo = ImageCache.get(image_path, actual_size)
            tk.Label(self.frame, image=photo).pack()
        except Exception:
            pass

        # PIN entry
        self.pin_var = tk.StringVar()
        self.pin_entry = tk.Entry(
            self.frame, font=('Helvetica', sf(16), 'bold'),
            width=6, border=0, bg="#d9d9d9", textvariable=self.pin_var
        )
        self.pin_entry.place(x=sx(68), y=sy(52))

        # Tutup (X)
        tk.Button(self.frame, text="X", font=('Helvetica', sf(10), 'bold'),
                  bg="#e4b672", fg="white", activebackground="#e4b672",
                  activeforeground="white", border=0,
                  command=self._cancel).place(x=sx(186), y=sy(13))

        # Numpad 1–9
        for label, bx, by in [("1",47,97),("2",97,97),("3",147,95),
                                ("4",47,140),("5",97,140),("6",147,140),
                                ("7",47,185),("8",97,185),("9",147,185)]:
            tk.Button(self.frame, text=label, font=('Helvetica', sf(13), 'bold'),
                      bg="#d9d9d9", border=0,
                      command=lambda d=label: self._append(d)
                      ).place(x=sx(bx), y=sy(by))

        tk.Button(self.frame, text="0", font=('Helvetica', sf(13), 'bold'),
                  bg="#d9d9d9", border=0,
                  command=lambda: self._append("0")).place(x=sx(97), y=sy(230))

        tk.Button(self.frame, text="⬅", font=('Helvetica', sf(16), 'bold'),
                  border=0, bg="#e4b672", fg="white",
                  activebackground="#e4b672", activeforeground="white",
                  command=self._clear).place(x=sx(29), y=sy(240))

        tk.Button(self.frame, text="✅", font=('Helvetica', sf(16), 'bold'),
                  border=0, bg="#FDCB7F", fg="white",
                  activebackground="#FDCB7F", activeforeground="white",
                  command=self._submit).place(x=sx(140), y=sy(240))

    def _append(self, digit: str):
        cur = self.pin_var.get()
        if len(cur) < 6:
            self.pin_var.set(cur + digit)

    def _clear(self):
        self.pin_var.set("")

    def _submit(self):
        self._on_submit(self.pin_var.get())

    def _cancel(self):
        self.frame.destroy()
        if self._on_cancel:
            self._on_cancel()

    def get_pin(self) -> str:
        return self.pin_var.get()

    def destroy(self):
        self.frame.destroy()


class AlertFrame:
    def __init__(self, parent, image_path: str, layout=None,
                size: tuple = (219, 227), position: tuple | None = None):
        self.frame = tk.Frame(parent)

        if layout is not None:
            actual_size = layout.img(*size)
            layout.center(self.frame, *size)
            close_x = layout.px(175)
            close_y = layout.py(7)
        else:
            actual_size = size
            px, py = position if position else (520, 270)
            self.frame.place(x=px, y=py)
            close_x, close_y = 175, 7

        try:
            photo = ImageCache.get(image_path, actual_size)
            tk.Label(self.frame, image=photo).pack()
        except Exception:
            pass

        tk.Button(self.frame, font=('Helvetica'), text="x",
                  fg="#ffffff", bg="#FDCB7F", border=0,
                  activebackground="#FDCB7F", activeforeground="#ffffff",
                  cursor="hand2", width=3,
                  command=self.frame.destroy).place(x=close_x, y=close_y)
