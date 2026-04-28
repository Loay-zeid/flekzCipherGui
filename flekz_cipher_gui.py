
Copy

import tkinter as tk
from tkinter import messagebox, ttk
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
    shift_val  = k % 26
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
    left  = ciphertext[:mid]
    right = ciphertext[mid:]
    k = ascii_sum(key)
    shift_val  = k % 26
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
 
 
# ================= GUI APPLICATION =================
class FlekzApp:
    # ── Color palette ──────────────────────────────────────
    BG        = "#0d0f14"
    PANEL     = "#151820"
    BORDER    = "#1e2330"
    ACCENT    = "#00d4ff"
    ACCENT2   = "#7b61ff"
    GREEN     = "#00e5a0"
    RED       = "#ff4d6d"
    TEXT      = "#e8eaf0"
    MUTED     = "#6b7280"
    ENTRY_BG  = "#0a0c11"
 
    def __init__(self, root):
        self.root = root
        self.root.title("Flekz Cipher")
        self.root.geometry("680x620")
        self.root.resizable(False, False)
        self.root.configure(bg=self.BG)
 
        self._build_ui()
 
    # ── UI builder ─────────────────────────────────────────
    def _build_ui(self):
        # ── Header ─────────────────────────────────────────
        header = tk.Frame(self.root, bg=self.BG)
        header.pack(fill="x", padx=30, pady=(28, 0))
 
        tk.Label(
            header, text="⬡  FLEKZ CIPHER",
            font=("Consolas", 20, "bold"),
            fg=self.ACCENT, bg=self.BG
        ).pack(side="left")
 
        tk.Label(
            header, text="v1.0",
            font=("Consolas", 10),
            fg=self.MUTED, bg=self.BG
        ).pack(side="left", padx=(8, 0), pady=(8, 0))
 
        tk.Label(
            header,
            text="Encrypt & Decrypt with Flekz Algorithm",
            font=("Consolas", 10),
            fg=self.MUTED, bg=self.BG
        ).pack(side="right", pady=(8, 0))
 
        # Divider
        tk.Frame(self.root, bg=self.BORDER, height=1).pack(
            fill="x", padx=30, pady=(14, 20)
        )
 
        # ── Main card ──────────────────────────────────────
        card = tk.Frame(self.root, bg=self.PANEL, bd=0)
        card.pack(fill="both", padx=30, pady=0)
 
        inner = tk.Frame(card, bg=self.PANEL)
        inner.pack(fill="both", padx=20, pady=20)
 
        # ── Input text ─────────────────────────────────────
        self._section_label(inner, "INPUT TEXT")
        self.input_text = self._text_box(inner)
 
        # ── Key ────────────────────────────────────────────
        key_row = tk.Frame(inner, bg=self.PANEL)
        key_row.pack(fill="x", pady=(14, 0))
 
        self._section_label(key_row, "SECRET KEY", side="left")
 
        self.show_key_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            key_row, text="Show",
            variable=self.show_key_var,
            command=self._toggle_key_visibility,
            bg=self.PANEL, fg=self.MUTED,
            activebackground=self.PANEL,
            selectcolor=self.ENTRY_BG,
            font=("Consolas", 9), bd=0
        ).pack(side="right")
 
        self.key_entry = tk.Entry(
            inner,
            font=("Consolas", 12),
            bg=self.ENTRY_BG, fg=self.TEXT,
            insertbackground=self.ACCENT,
            relief="flat", bd=0,
            show="•"
        )
        self.key_entry.pack(fill="x", pady=(6, 0), ipady=8)
        self._add_border(inner, self.key_entry)
 
        # ── Key strength indicator ─────────────────────────
        self.strength_var = tk.StringVar(value="")
        self.strength_label = tk.Label(
            inner, textvariable=self.strength_var,
            font=("Consolas", 9), bg=self.PANEL, fg=self.MUTED,
            anchor="w"
        )
        self.strength_label.pack(fill="x", pady=(4, 0))
        self.key_entry.bind("<KeyRelease>", self._update_key_strength)
 
        # ── Mode selector ──────────────────────────────────
        mode_row = tk.Frame(inner, bg=self.PANEL)
        mode_row.pack(fill="x", pady=(16, 0))
 
        self.mode_var = tk.StringVar(value="encrypt")
 
        for text, val, color in [
            ("🔒  Encrypt", "encrypt", self.GREEN),
            ("🔓  Decrypt", "decrypt", self.ACCENT2),
        ]:
            rb = tk.Radiobutton(
                mode_row, text=text, variable=self.mode_var, value=val,
                font=("Consolas", 11, "bold"),
                fg=color, bg=self.PANEL,
                activebackground=self.PANEL,
                selectcolor=self.PANEL,
                bd=0, cursor="hand2"
            )
            rb.pack(side="left", padx=(0, 24))
 
        # ── Run button ─────────────────────────────────────
        self.run_btn = tk.Button(
            inner, text="▶  RUN",
            font=("Consolas", 12, "bold"),
            bg=self.ACCENT, fg=self.BG,
            activebackground="#00b8e0",
            activeforeground=self.BG,
            relief="flat", bd=0, cursor="hand2",
            padx=24, pady=8,
            command=self.run_action
        )
        self.run_btn.pack(pady=(18, 0))
        self.run_btn.bind("<Enter>", lambda e: self.run_btn.config(bg="#00b8e0"))
        self.run_btn.bind("<Leave>", lambda e: self.run_btn.config(bg=self.ACCENT))
 
        # Divider
        tk.Frame(inner, bg=self.BORDER, height=1).pack(fill="x", pady=(20, 0))
 
        # ── Output ─────────────────────────────────────────
        out_row = tk.Frame(inner, bg=self.PANEL)
        out_row.pack(fill="x", pady=(16, 6))
        self._section_label(out_row, "OUTPUT", side="left")
 
        self.copy_btn = tk.Button(
            out_row, text="⎘  Copy",
            font=("Consolas", 9),
            bg=self.BORDER, fg=self.MUTED,
            activebackground=self.BORDER,
            relief="flat", bd=0, cursor="hand2",
            padx=10, pady=3,
            command=self.copy_output
        )
        self.copy_btn.pack(side="right")
 
        self.output_text = self._text_box(inner, height=4, fg=self.ACCENT)
 
        # ── Status bar ─────────────────────────────────────
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Frame(self.root, bg=self.BORDER, height=28)
        status_bar.pack(fill="x", side="bottom")
        tk.Label(
            status_bar, textvariable=self.status_var,
            font=("Consolas", 9), fg=self.MUTED, bg=self.BORDER
        ).pack(side="left", padx=14)
 
        # ── Info row ───────────────────────────────────────
        self._build_info_bar()
 
    def _build_info_bar(self):
        info = tk.Frame(self.root, bg=self.BG)
        info.pack(fill="x", padx=30, pady=(12, 4))
 
        items = [
            ("SHIFT",   "key-based"),
            ("SWAP",    "block reversal"),
            ("HALVES",  "split & mirror"),
        ]
        for label, desc in items:
            pill = tk.Frame(info, bg=self.BORDER)
            pill.pack(side="left", padx=(0, 8))
            tk.Label(pill, text=f" {label} ", font=("Consolas", 8, "bold"),
                     fg=self.ACCENT2, bg=self.BORDER).pack(side="left")
            tk.Label(pill, text=f"{desc} ", font=("Consolas", 8),
                     fg=self.MUTED, bg=self.BORDER).pack(side="left")
 
    # ── Widget helpers ─────────────────────────────────────
    def _section_label(self, parent, text, side=None):
        lbl = tk.Label(
            parent, text=text,
            font=("Consolas", 9, "bold"),
            fg=self.MUTED, bg=self.PANEL if parent.cget("bg") == self.PANEL else parent.cget("bg"),
            anchor="w"
        )
        if side:
            lbl.pack(side=side)
        else:
            lbl.pack(fill="x", pady=(0, 6))
 
    def _text_box(self, parent, height=4, fg=None):
        box = tk.Text(
            parent,
            height=height,
            font=("Consolas", 12),
            bg=self.ENTRY_BG, fg=fg or self.TEXT,
            insertbackground=self.ACCENT,
            relief="flat", bd=0,
            wrap="word",
            padx=10, pady=8
        )
        box.pack(fill="x")
        self._add_border(parent, box)
        return box
 
    def _add_border(self, parent, widget):
        """Wrap widget with a 1px accent border frame."""
        # Re-pack the widget inside a border frame
        widget.pack_forget()
        border = tk.Frame(parent, bg=self.BORDER, padx=1, pady=1)
        border.pack(fill="x", pady=(0, 2))
        widget.pack(in_=border, fill="x")
 
    # ── Key strength ───────────────────────────────────────
    def _update_key_strength(self, event=None):
        key = self.key_entry.get()
        if not key:
            self.strength_var.set("")
            return
        score = (
            any(c.isdigit() for c in key) +
            any(c.isupper() for c in key) +
            any(c.islower() for c in key) +
            any(not c.isalnum() for c in key)
        )
        length_bonus = len(key) >= 8
        total = score + length_bonus
 
        if total <= 2:
            label, color = "Key strength: Weak ▪▪░░░", self.RED
        elif total <= 3:
            label, color = "Key strength: Fair ▪▪▪░░", "#f5a623"
        else:
            label, color = "Key strength: Strong ▪▪▪▪▪", self.GREEN
 
        self.strength_var.set(label)
        self.strength_label.config(fg=color)
 
    def _toggle_key_visibility(self):
        self.key_entry.config(show="" if self.show_key_var.get() else "•")
 
    # ── Actions ────────────────────────────────────────────
    def run_action(self):
        text = self.input_text.get("1.0", "end-1c").strip()
        key  = self.key_entry.get().strip()
 
        if not text:
            self._set_status("⚠  No input text provided.", self.RED)
            return
        if not key:
            self._set_status("⚠  Secret key is required.", self.RED)
            messagebox.showerror("Missing Key", "Please enter a secret key.")
            return
 
        mode = self.mode_var.get()
        try:
            if mode == "encrypt":
                result = flekz_encrypt(text, key)
                label  = "Encrypted"
                color  = self.GREEN
            else:
                result = flekz_decrypt(text, key)
                label  = "Decrypted"
                color  = self.ACCENT2
 
            self.output_text.config(state="normal", fg=color)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
            self._set_status(
                f"✔  {label} successfully  ·  {len(result)} chars  ·  key ascii-sum = {ascii_sum(key)}",
                color
            )
        except Exception as ex:
            self._set_status(f"✘  Error: {ex}", self.RED)
 
    def copy_output(self):
        result = self.output_text.get("1.0", "end-1c")
        if result:
            try:
                pyperclip.copy(result)
                self._set_status("✔  Copied to clipboard.", self.GREEN)
            except Exception:
                # fallback – use tkinter clipboard
                self.root.clipboard_clear()
                self.root.clipboard_append(result)
                self._set_status("✔  Copied to clipboard.", self.GREEN)
        else:
            self._set_status("⚠  Nothing to copy.", self.MUTED)
 
    def _set_status(self, msg, color=None):
        self.status_var.set(msg)
        # find the label in status bar and recolor it
        for w in self.root.winfo_children():
            if isinstance(w, tk.Frame) and w.cget("bg") == self.BORDER:
                for child in w.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(fg=color or self.MUTED)
 
 
# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = FlekzApp(root)
    root.mainloop()
