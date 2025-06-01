import tkinter as tk
from tkinter import messagebox

# ===== Flekz Cipher Core Functions =====

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
        group = chars[i:i+group_size]
        chars[i:i+group_size] = group[::-1]
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

    # Process left half
    left = shift_text(left, shift_val)
    left = swap_blocks(left, swap_group)
    if do_reverse:
        left = reverse_text(left)

    # Process right half
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

    # Reverse transformations (right half)
    if do_reverse:
        right = reverse_text(right)
    right = swap_blocks(right, swap_group)
    right = shift_text(right, -shift_val)

    # Reverse transformations (left half)
    if do_reverse:
        left = reverse_text(left)
    left = swap_blocks(left, swap_group)
    left = shift_text(left, -shift_val)

    return left + right[::-1]

# ===== GUI Interface =====

def encrypt_action():
    text = input_text.get("1.0", "end-1c")
    key = key_entry.get()
    if not key:
        messagebox.showerror("Error", "Please enter a key.")
        return
    result = flekz_encrypt(text, key)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

def decrypt_action():
    text = input_text.get("1.0", "end-1c")
    key = key_entry.get()
    if not key:
        messagebox.showerror("Error", "Please enter a key.")
        return
    result = flekz_decrypt(text, key)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)

# ===== Tkinter GUI Setup =====

root = tk.Tk()
root.title("Flekz Cipher Encryptor/Decryptor")

tk.Label(root, text="Enter text:").pack()
input_text = tk.Text(root, height=5, width=50)
input_text.pack()

tk.Label(root, text="Enter key:").pack()
key_entry = tk.Entry(root, width=30)
key_entry.pack()

btn_frame = tk.Frame(root)
btn_frame.pack()

tk.Button(btn_frame, text="Encrypt", command=encrypt_action).pack(side=tk.LEFT, padx=5)
tk.Button(btn_frame, text="Decrypt", command=decrypt_action).pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Result:").pack()
output_text = tk.Text(root, height=5, width=50)
output_text.pack()

root.mainloop()
