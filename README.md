# 🏦 Bank Account Manager – Streamlit Application

An interactive and fully-functional **Bank Account Management System** developed using **Python**, **Streamlit**, and **Pandas**. This app simulates a real-world banking interface, allowing users to manage multiple accounts, perform secure transactions, generate downloadable slips, and analyze financial summaries — all from a beautifully styled dashboard.

---

## 🎯 Project Objective

To create a **self-contained digital banking interface** with real-time transaction handling, account summaries, and detailed analytics — suitable for finance simulations, learning projects, or portfolio demonstration.

---

## ✨ Key Features

| Module | Description |
|--------|-------------|
| 👤 **Account Management** | Create Savings, Business, Checking, or Fixed Deposit accounts with custom holder names and initial balance. |
| 💳 **Transactions** | Perform real-time Credit/Debit operations with validation and auto-updated balances. |
| 📄 **Transaction Slips** | Generate downloadable text-based **bank slips** after every transaction. |
| 🧾 **History Tracker** | View complete transaction logs in tabular format and visual card layouts. |
| 📊 **Account Summary** | Summarize activity including total credits, debits, and net balance change. |
| 🏦 **Bank Summary Dashboard** | Aggregate data from all accounts with insights such as total accounts, total funds, account type distribution, etc. |
| 🖌️ **Beautiful UI/UX** | Clean, responsive layout with **custom Streamlit CSS styling** and animated banners for status messages. |
| 📥 **Download Option** | Users can save their transaction slips as `.txt` files, simulating printed receipts. |

---

## 🖼️ Screenshots

> Add your own screenshots or GIF demos here if available:
- Account Creation
- Transaction with success message
- Slip preview and download
- Bank-wide analytics

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|------------|
| UI Framework | [Streamlit](https://streamlit.io) |
| Styling | HTML + Custom CSS (injected via `st.markdown`) |
| Logic & Backend | Python 3, OOP (Classes, Session State) |
| Data | In-memory (using `st.session_state`), Pandas for tabular summaries |
| Export | `base64` for text file download |

---

## 🛠️ Getting Started

### 🔗 Clone this Repository

```bash
git clone https://github.com/your-username/bank-account-manager.git
cd bank-account-manager

---

### ✅ Tips:
- You can save this file as `README.md` at the root of your project.
- Add a `requirements.txt` file with:
  ```txt
  streamlit
  pandas
```
