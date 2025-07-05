# 🏦 Bank Account Manager – Streamlit Application

A feature-rich and visually appealing **Bank Account Management System** built using **Python**, **Streamlit**, and **Pandas**. This application mimics the core functionalities of real-world banking systems, allowing users to manage multiple account types, execute secure financial transactions, and monitor comprehensive financial summaries — all within an elegant, user-friendly interface.

---

## 🎯 Project Objective

To develop a **real-time digital banking simulation tool** with robust functionality for account handling, transaction tracking, and insightful analytics. Designed for educational use, portfolio enhancement, and demonstrating practical application of Streamlit and Python OOP principles.

---

## ✨ Key Features

| 🔧 Module | 💡 Description |
|----------|----------------|
| 👤 **Account Management** | Create and manage multiple accounts — Savings, Business, Checking, or Fixed Deposit — with user-defined names and initial balances. |
| 💳 **Secure Transactions** | Real-time credit and debit operations with live balance updates and transaction validation. |
| 📄 **Transaction Slips** | Automatically generate and download detailed, stylized bank slips in `.txt` format for each transaction. |
| 🧾 **Transaction History** | View a chronological log of all account activities in both **DataFrame** and **card format** with styling. |
| 📊 **Account Summary** | View per-account financial summaries, including net balance, total credits, total debits, and last transaction. |
| 🏦 **Bank Dashboard** | Analyze global data such as total funds, number of accounts, transaction volume, and account type distribution. |
| 🎨 **Elegant UI/UX** | Enhanced layout using **custom Streamlit CSS** for cards, banners, highlights, and responsive form elements. |
| 📥 **Slip Download Option** | Download transaction receipts in `.txt` format, simulating real-world banking workflows. |

---

## 🖼️ Screenshots

> (💡 Add screenshots or GIF previews here to showcase the app in action.)

- ✅ Create and manage accounts with ease  
- 💸 Perform transactions and see animated success/error banners  
- 🧾 View and download transaction receipts  
- 📊 Explore full financial summaries per account or entire bank

---

## 🔧 Tech Stack

| Layer         | Tools & Libraries                        |
|---------------|-------------------------------------------|
| UI Framework  | [Streamlit](https://streamlit.io)         |
| Styling       | Custom CSS via `st.markdown()`            |
| Backend Logic | Python 3, OOP (Classes, Methods, States)  |
| Data Handling | `pandas` for table rendering and summaries |
| State Mgmt    | `st.session_state` for in-memory storage  |
| File Export   | `base64` + `.txt` for downloadable slips  |

---

## 🧠 Learning Outcomes

- ✔️ Applied **Object-Oriented Programming (OOP)** for modeling bank accounts and transactions  
- ✔️ Leveraged **Streamlit session state** to manage dynamic UI interactions and persistent data  
- ✔️ Customized **CSS within Streamlit** to improve user interface and experience  
- ✔️ Built modular, scalable code with real-world usability in mind  
- ✔️ Developed downloadable content using Python I/O and `base64` encoding

---

## 🚀 How to Run the App

### 📦 Step 1: Clone the Repository

git clone https://github.com/your-username/bank-account-manager.git
cd bank-account-manager
🧪 Step 2: Install Dependencies

pip install -r requirements.txt
Or manually:


pip install streamlit pandas
⚙️ Step 3: Launch the App

streamlit run app.py
📁 Project Structure

📦 bank-account-manager
 ┣ 📄 app.py                # Main Streamlit Application
 ┣ 📄 README.md             # Project Documentation
 ┗ 📄 requirements.txt      # Python dependencies
🛠 Future Improvements
🔐 Add user login & authentication

📂 Connect to database for persistent storage (SQLite or MongoDB)

📈 Integrate visual charts (using Plotly/Altair)

📧 Email receipts or export PDF slips

🌐 Host online via Streamlit Cloud or Render

🧑‍💻 Developer
Vikas Sharma — Data Analyst & Python Developer

🌐 Portfolio

💼 LinkedIn

🐦 X / Twitter

👨‍💻 GitHub

⭐ Support This Project
If you found this project helpful or inspiring:

⭐ Star this repository

🍴 Fork and improve it

🗣️ Share with others

📜 License
This project is licensed under the MIT License.
Feel free to use, modify, and distribute with credit.

---

Would you like help creating the `requirements.txt`, `LICENSE`, or demo visuals (GIF/MP4)?
