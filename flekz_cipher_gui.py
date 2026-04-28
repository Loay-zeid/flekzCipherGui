import tkinter as tk
from tkinter import messagebox
import pyperclip

# ================= FLEKZ CIPHER CORE =================

def ascii_sum(key):
    return sum(ord(char) for char in key)

def shift_text(text, shift):
    shifted = ''
    for c in text:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            shifted += chr((ord(c) - base + shift) % 26 + base)
        else:
            shifted += c
    return shifted

def swap_blocks(text, group_size):
    chars = list(text)
    for i in range(0, len(chars) - group_size + 1, group_size):
        group = chars[i:i + group_size]
        chars[i:i + group_size] = group[::-1]
    return ''.join(chars)

def reverse_text(text):
    return text[::-1]

def flekz_encrypt(plaintext, key):
    if len(plaintext) % 2 != 0:
        plaintext += "_"

    mid = len(plaintext) // 2
    left = plaintext[:mid]
    right = plaintext[mid:][::-1]

    k = ascii_sum(key)
    shift_val = k % 26
    swap_group = 2 if k % 3 == 0 else 3
    do_reverse = k % 2 == 1

    left = shift_text(left, shift_val)
    left = swap_blocks(left, swap_group)
    if do_reverse:
        left = reverse_text(left)

    right = shift_text(right, shift_val)
    right = swap_blocks(right, swap_group)
    if do_reverse:
        right = reverse_text(right)

    return left + right

def flekz_decrypt(ciphertext, key):
    mid = len(ciphertext) // 2
    left = ciphertext[:mid]
    right = ciphertext[mid:]

    k = ascii_sum(key)
    shift_val = k % 26
    swap_group = 2 if k % 3 == 0 else 3
    do_reverse = k % 2 == 1

    if do_reverse:
        right = reverse_text(right)
    right = swap_blocks(right, swap_group)
    right = shift_text(right, -shift_val)

    if do_reverse:
        left = reverse_text(left)
    left = swap_blocks(left, swap_group)
    left = shift_text(left, -shift_val)

    return left + right[::-1]

# ================= GUI =================

class FlekzApp:
    BG = "#0d0f14"
    PANEL = "#151820"
    BORDER = "#1e2330"
    ACCENT = "#00d4ff"
    TEXT = "#e8eaf0"
    ENTRY_BG = "#0a0c11"

    def __init__(self, root):
        self.root = root
        self.root.title("Flekz Cipher")
        self.root.geometry("650x550")
        self.root.configure(bg=self.BG)

        self.build_ui()

    def build_ui(self):
        container = tk.Frame(self.root, bg=self.PANEL)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # INPUT
        tk.Label(container, text="Input Text", fg=self.TEXT, bg=self.PANEL).pack(anchor="w")

        self.input_text = tk.Text(
            container,
            height=5,
            bg=self.ENTRY_BG,
            fg=self.TEXT,
            insertbackground=self.ACCENT
        )
        self.input_text.pack(fill="x", pady=5)

        # KEY (مع border صحيح)
        tk.Label(container, text="Secret Key", fg=self.TEXT, bg=self.PANEL).pack(anchor="w")

        key_border = tk.Frame(container, bg=self.BORDER, padx=1, pady=1)
        key_border.pack(fill="x", pady=5)

        self.key_entry = tk.Entry(
            key_border,
            bg=self.ENTRY_BG,
            fg=self.TEXT,
            insertbackground=self.ACCENT,
            relief="flat"
        )
        self.key_entry.pack(fill="x", ipady=6)

        # BUTTONS
        btn_frame = tk.Frame(container, bg=self.PANEL)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Encrypt", command=self.encrypt).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Decrypt", command=self.decrypt).pack(side="left", padx=5)

        # OUTPUT
        tk.Label(container, text="Output", fg=self.TEXT, bg=self.PANEL).pack(anchor="w")

        self.output_text = tk.Text(
            container,
            height=5,
            bg=self.ENTRY_BG,
            fg=self.ACCENT,
            insertbackground=self.ACCENT
        )
        self.output_text.pack(fill="x", pady=5)

        # COPY
        tk.Button(container, text="Copy", command=self.copy).pack(pady=5)

    def encrypt(self):
        text = self.input_text.get("1.0", "end-1c")
        key = self.key_entry.get()

        if not key:
            messagebox.showerror("Error", "Enter a key")
            return

        result = flekz_encrypt(text, key)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

    def decrypt(self):
        text = self.input_text.get("1.0", "end-1c")
        key = self.key_entry.get()

        if not key:
            messagebox.showerror("Error", "Enter a key")
            return

        result = flekz_decrypt(text, key)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

    def copy(self):
        result = self.output_text.get("1.0", "end-1c")
        if result:
            pyperclip.copy(result)

# ================= RUN =================

if __name__ == "__main__":
    root = tk.Tk()
    app = FlekzApp(root)
    root.mainloop()
