# 🔐 Flekz Cipher (Encryption Tool)

## 📌 Overview

The **Flekz Cipher** is a custom encryption and decryption desktop application built using **Python** and **Tkinter**. It implements a unique symmetric cipher algorithm designed to transform text through multiple layers of operations including shifting, swapping, and reversing.

This project focuses on combining algorithmic thinking with user interface design, providing an interactive tool to securely encode and decode text using a secret key.

---

## 🚀 Key Features

- 🔐 Custom encryption & decryption algorithm  
- 🧠 Key-based dynamic transformations  
- 🔄 Text shifting (Caesar-like logic)  
- 🔁 Block swapping mechanism  
- 🔃 Conditional reversing logic  
- 💻 Interactive desktop GUI (Tkinter)  
- 📋 Copy to clipboard functionality  
- ⚡ Fast and responsive user experience  

---

## 🧠 How the Algorithm Works

The encryption process is based on multiple steps:

1. Convert the secret key into a numeric value using ASCII sum  
2. Split the text into two halves  
3. Reverse the second half  
4. Apply character shifting based on the key  
5. Swap characters in blocks (size depends on key)  
6. Optionally reverse text depending on key properties  
7. Merge both halves into final ciphertext  

The decryption process reverses all operations in the correct order.

---

## 🧰 Tech Stack

- Python  
- Tkinter (GUI)  
- Pyperclip (Clipboard handling)  

---

## ⚙️ Getting Started

```bash
# Clone the repository
git clone https://github.com/Loay-zeid/FlekzCipher.git

# Navigate to project folder
cd FlekzCipher

# Run the application
python main.py
```

---

## 🧭 How to Use the Application

### 1️⃣ Enter Text

- Type or paste the text you want to encrypt or decrypt  
- Supports letters, numbers, and symbols  

<p align="center">
  <img src="./input.png" width="900"/>
</p>

---

### 2️⃣ Enter Secret Key

- Provide a secret key used for encryption/decryption  
- The key determines shift, swapping, and reversing behavior  

<p align="center">
  <img src="./key.png" width="900"/>
</p>

---

### 3️⃣ Choose Mode

- Select **Encrypt** or **Decrypt**  
- Click the **Run** button  

<p align="center">
  <img src="./mode.png" width="900"/>
</p>

---

### 4️⃣ View Result

- Output will appear instantly  
- Use **Copy** button to copy result  

<p align="center">
  <img src="./result.png" width="900"/>
</p>

---

## 📚 What I Learned

- Designing a custom encryption algorithm  
- Working with string manipulation and transformations  
- Building desktop GUI applications using Tkinter  
- Handling user input and events  
- Improving UX in desktop applications  

---

## 📌 Future Improvements

- 🔑 Add stronger encryption variations  
- 💾 Save/load encrypted files  
- 🌐 Convert to web-based application  
- 🎨 Improve UI/UX design further  
- 🔐 Add password strength validation  

---
