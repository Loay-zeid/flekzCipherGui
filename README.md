# Flekz Cipher 🔐

Flekz Cipher is a custom-made **symmetric encryption algorithm** based on the visual idea of an hourglass (sand clock).

It splits the plaintext into two halves and applies transformations (like shifting, swapping, reversing) in opposite directions to simulate sand flowing through an hourglass.

## 🧠 Concept

- Text is split into **two halves**.
- Each half is **transformed separately** using a key:
  - 🔁 `Shift`: Characters are shifted using Caesar-style shifting.
  - 🔄 `Swap`: Characters are swapped in chunks (e.g., every 2 or 3).
  - ↩️ `Reverse`: Halves are optionally reversed.
- Transformations are determined by the **sum of ASCII values of the key**.

Decryption simply reverses the operations.

## 🖥️ GUI Interface

This project includes a simple **Tkinter-based Python GUI** for:

- Encrypting text using Flekz Cipher
- Decrypting back the ciphertext
- Using your own custom key

## 📁 Files

Download the project  : 

- `flekz_cipher_gui.py` – The main GUI application (Python)


## 🚀 How to Run

Make sure you have Python 3.7+ installed, then run:

```bash
python flekz_cipher_gui.py
