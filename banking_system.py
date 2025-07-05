import streamlit as st
import datetime
import pandas as pd
import base64

# Initialize session state with robust defaults
def init_session_state():
    defaults = {
        'accounts': {},
        'current_account': None,
        'transactions': {},
        'slip_history': {},
        'last_slip': None,
        'last_transaction': None,
        'transaction_success': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Account class with enhanced features
class Account:
    def __init__(self, bal, acc, name, acc_type):
        self.balance = bal
        self.account_no = acc
        self.account_holder = name
        self.account_type = acc_type
        self.opening_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
    def debit(self, amount, description):
        if amount > self.balance:
            return (False, "Insufficient balance! Transaction failed.")
        self.balance -= amount
        transaction_id = f"TXN{len(st.session_state.transactions.get(self.account_no, [])) + 1:04d}"
        transaction = {
            "id": transaction_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Debit",
            "amount": amount,
            "description": description,
            "balance": self.balance
        }
        self.add_transaction(transaction)
        return (True, transaction)
    
    def credit(self, amount, description):
        self.balance += amount
        transaction_id = f"TXN{len(st.session_state.transactions.get(self.account_no, [])) + 1:04d}"
        transaction = {
            "id": transaction_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Credit",
            "amount": amount,
            "description": description,
            "balance": self.balance
        }
        self.add_transaction(transaction)
        return (True, transaction)
    
    def get_balance(self):
        return self.balance
    
    def add_transaction(self, transaction):
        if self.account_no not in st.session_state.transactions:
            st.session_state.transactions[self.account_no] = []
        st.session_state.transactions[self.account_no].append(transaction)
    
    def generate_slip(self, transaction, slip_type):
        slip_id = f"SLIP{len(st.session_state.slip_history.get(self.account_no, [])) + 1:04d}"
        slip = {
            "id": slip_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": slip_type,
            "account_no": self.account_no,
            "account_holder": self.account_holder,
            "transaction_id": transaction["id"],
            "amount": transaction["amount"],
            "description": transaction["description"],
            "balance": transaction["balance"]
        }
        if self.account_no not in st.session_state.slip_history:
            st.session_state.slip_history[self.account_no] = []
        st.session_state.slip_history[self.account_no].append(slip)
        return slip

# Function to generate a transaction slip as a downloadable text file
def generate_slip_file(slip):
    slip_content = f"""
╔═════════════════════════════════════════════════╗
║              BANK TRANSACTION SLIP              ║
╠═════════════════════════════════════════════════╣
║ Slip ID:        {slip['id']:<30} ║
║ Date:           {slip['date']:<30} ║
║ Type:           {slip['type']:<30} ║
╠═════════════════════════════════════════════════╣
║ Account No:     {slip['account_no']:<30} ║
║ Account Holder: {slip['account_holder'][:30]:<30} ║
║ Transaction ID: {slip['transaction_id']:<30} ║
╠═════════════════════════════════════════════════╣
║ Amount:         ₹{slip['amount']:<29.2f} ║
║ Description:    {slip['description'][:30]:<30} ║
║ Balance:        ₹{slip['balance']:<29.2f} ║
╚═════════════════════════════════════════════════╝
"""
    return slip_content

# Main function for the Streamlit app
def main():
    st.set_page_config(
        page_title="Bank Account Manager",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS for styling
    st.markdown("""
    <style>
        :root {
            --primary: #1a237e;
            --primary-light: #534bae;
            --secondary: #283593;
            --accent: #3949ab;
            --success: #43a047;
            --danger: #e53935;
            --warning: #ffb300;
            --info: #039be5;
            --light: #f5f5f5;
            --dark: #212121;
            --card-bg: #ffffff;
        }
        
        .main {
            background-color: #f0f2f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .stButton>button {
            background-color: var(--accent);
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #d1d5db;
            padding: 10px 12px;
        }
        
        .header {
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
        }
        
        .account-card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 25px;
            border-left: 4px solid var(--accent);
        }
        
        .transaction-card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 15px;
        }
        
        .debit {
            border-left: 4px solid var(--danger);
        }
        
        .credit {
            border-left: 4px solid var(--success);
        }
        
        .slip-container {
            background: linear-gradient(135deg, #f0f7ff, #e3f2fd);
            border-radius: 12px;
            padding: 25px;
            margin-top: 25px;
            border: 1px solid #bbdefb;
        }
        
        .success-banner {
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            color: #155724;
            padding: 18px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 5px solid var(--success);
        }
        
        .error-banner {
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            color: #721c24;
            padding: 18px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 5px solid var(--danger);
        }
        
        .balance-display {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            padding: 20px;
            border-radius: 12px;
            margin: 20px 0;
            text-align: center;
        }
        
        .metric-card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
            margin-bottom: 20px;
        }
        
        .form-container {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 25px;
        }
        
        h1, h2, h3 {
            color: var(--primary);
        }
    </style>
    """, unsafe_allow_html=True)
    
    init_session_state()
    
    st.markdown('<div class="header"><h1 style="color:white; margin:0;">🏦 Bank Account Manager</h1></div>', unsafe_allow_html=True)
    
    # Navigation
    menu = ["Create Account", "Account Operations", "Transaction History", "Account Summary", "Bank Summary"]
    choice = st.sidebar.selectbox("Navigation", menu)
    
    # Create Account Page
    if choice == "Create Account":
        st.subheader("Create New Account")
        
        with st.form("create_account_form"):
            col1, col2 = st.columns(2)
            with col1:
                acc_no = st.text_input("Account Number*", placeholder="Enter account number")
                acc_holder = st.text_input("Account Holder Name*", placeholder="Full name")
            with col2:
                acc_type = st.selectbox("Account Type*", ["Savings", "Checking", "Business", "Fixed Deposit"])
                balance = st.number_input("Initial Balance (₹)*", min_value=0.0, step=100.0, format="%.2f")
            
            submitted = st.form_submit_button("Create Account")
            
            if submitted:
                if not acc_no or not acc_holder:
                    st.error("Account number and holder name are required!")
                elif acc_no in st.session_state.accounts:
                    st.error("Account number already exists!")
                else:
                    account = Account(balance, acc_no, acc_holder, acc_type)
                    st.session_state.accounts[acc_no] = account
                    st.session_state.current_account = acc_no
                    st.success(f"Account {acc_no} created successfully with initial balance of ₹{balance:.2f}")
    
    # Account Operations Page
    elif choice == "Account Operations":
        st.subheader("Account Operations")
        
        if not st.session_state.accounts:
            st.warning("No accounts found. Please create an account first.")
            return
        
        # Account selection
        account_options = [f"{acc_no} - {st.session_state.accounts[acc_no].account_holder}" 
                          for acc_no in st.session_state.accounts]
        
        # Get current index safely
        current_index = 0
        if st.session_state.current_account:
            keys = list(st.session_state.accounts.keys())
            if st.session_state.current_account in keys:
                current_index = keys.index(st.session_state.current_account)
        
        selected_account = st.selectbox("Select Account", account_options, index=current_index)
        acc_no = selected_account.split(" - ")[0]
        st.session_state.current_account = acc_no
        account = st.session_state.accounts[acc_no]
        
        # Display account info
        st.markdown("### Account Information")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="account-card">
                <p><strong>Account Holder:</strong> {account.account_holder}</p>
                <p><strong>Account Type:</strong> {account.account_type}</p>
                <p><strong>Account Number:</strong> {account.account_no}</p>
                <p><strong>Opening Date:</strong> {account.opening_date}</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            balance = account.get_balance()
            st.markdown(f"""
            <div class="account-card">
                <h3 style="text-align:center; color:#1a237e; margin-top:10px;">Current Balance</h3>
                <h2 style="text-align:center; color:#283593;">₹{balance:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Transaction form
        st.markdown("### Perform Transaction")
        with st.form("transaction_form"):
            amount = st.number_input("Amount (₹)", min_value=0.01, step=100.0, format="%.2f")
            description = st.text_input("Description", placeholder="Enter transaction description")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                debit_btn = st.form_submit_button("Debit")
            with col2:
                credit_btn = st.form_submit_button("Credit")
            with col3:
                balance_btn = st.form_submit_button("Check Balance")
            
            if debit_btn:
                if amount <= 0:
                    st.session_state.last_transaction = "Amount must be greater than zero"
                    st.session_state.transaction_success = False
                else:
                    success, transaction = account.debit(amount, description)
                    if success:
                        slip_type = "Debit Slip"
                        slip = account.generate_slip(transaction, slip_type)
                        st.session_state.last_slip = slip
                        st.session_state.last_transaction = f"₹{amount:.2f} debited successfully"
                        st.session_state.transaction_success = True
                    else:
                        st.session_state.last_transaction = "Transaction failed: Insufficient balance"
                        st.session_state.transaction_success = False
            
            if credit_btn:
                if amount <= 0:
                    st.session_state.last_transaction = "Amount must be greater than zero"
                    st.session_state.transaction_success = False
                else:
                    success, transaction = account.credit(amount, description)
                    if success:
                        slip_type = "Credit Slip"
                        slip = account.generate_slip(transaction, slip_type)
                        st.session_state.last_slip = slip
                        st.session_state.last_transaction = f"₹{amount:.2f} credited successfully"
                        st.session_state.transaction_success = True
            
            if balance_btn:
                st.session_state.last_transaction = f"Current Balance: ₹{account.get_balance():,.2f}"
                st.session_state.transaction_success = True
        
        # Display transaction result
        if 'last_transaction' in st.session_state and st.session_state.last_transaction:
            if st.session_state.transaction_success:
                st.markdown(f'<div class="success-banner">{st.session_state.last_transaction}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-banner">{st.session_state.last_transaction}</div>', unsafe_allow_html=True)
        
        # Display transaction slip
        if 'last_slip' in st.session_state and st.session_state.last_slip:
            slip = st.session_state.last_slip
            st.markdown("### Transaction Slip")
            st.markdown(f"""
            <div class="slip-container">
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <p><strong>Slip ID:</strong> {slip['id']}</p>
                        <p><strong>Date:</strong> {slip['date']}</p>
                    </div>
                    <div>
                        <p style="font-size:1.2rem; font-weight:bold; color:{"#e53935" if slip['type'] == 'Debit Slip' else '#43a047'}">
                            {slip['type']}
                        </p>
                    </div>
                </div>
                <hr style="margin:15px 0; border-top:1px solid #ddd;">
                <div style="display:flex; justify-content:space-between;">
                    <div>
                        <p><strong>Account No:</strong> {slip['account_no']}</p>
                        <p><strong>Account Holder:</strong> {slip['account_holder']}</p>
                    </div>
                    <div>
                        <p><strong>Transaction ID:</strong> {slip['transaction_id']}</p>
                    </div>
                </div>
                <hr style="margin:15px 0; border-top:1px solid #ddd;">
                <div style="display:flex; justify-content:space-between; margin-top:20px;">
                    <div>
                        <p><strong>Amount:</strong></p>
                        <h3 style="color:{"#e53935" if slip['type'] == 'Debit Slip' else '#43a047'}; margin:5px 0;">
                            ₹{slip['amount']:.2f}
                        </h3>
                    </div>
                    <div>
                        <p><strong>Balance:</strong></p>
                        <h3 style="color:#1a237e; margin:5px 0;">₹{slip['balance']:.2f}</h3>
                    </div>
                </div>
                <p style="margin-top:15px;"><strong>Description:</strong> {slip['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate and download slip button
            slip_content = generate_slip_file(slip)
            st.download_button(
                label="Download Transaction Slip",
                data=slip_content,
                file_name=f"bank_slip_{slip['id']}.txt",
                mime="text/plain"
            )
    
    # Transaction History Page
    elif choice == "Transaction History":
        st.subheader("Transaction History")
        
        if not st.session_state.accounts:
            st.warning("No accounts found. Please create an account first.")
            return
        
        # Account selection
        account_options = [f"{acc_no} - {st.session_state.accounts[acc_no].account_holder}" 
                          for acc_no in st.session_state.accounts]
        
        # Get current index safely
        current_index = 0
        if st.session_state.current_account:
            keys = list(st.session_state.accounts.keys())
            if st.session_state.current_account in keys:
                current_index = keys.index(st.session_state.current_account)
        
        selected_account = st.selectbox("Select Account", account_options, index=current_index)
        acc_no = selected_account.split(" - ")[0]
        account = st.session_state.accounts[acc_no]
        
        # Display transaction history
        if acc_no in st.session_state.transactions and st.session_state.transactions[acc_no]:
            st.markdown(f"### Transaction History for {account.account_holder}")
            
            # Display as DataFrame
            df = pd.DataFrame(st.session_state.transactions[acc_no])
            df = df[['date', 'type', 'amount', 'description', 'balance']]
            st.dataframe(
                df.style
                .format({'amount': '₹{:.2f}', 'balance': '₹{:.2f}'})
                .applymap(lambda x: 'color: #e53935' if x == 'Debit' else 'color: #43a047', subset=['type']),
                height=400
            )
        else:
            st.info("No transactions found for this account.")
    
    # Account Summary Page
    elif choice == "Account Summary":
        st.subheader("Account Summary")
        
        if not st.session_state.accounts:
            st.warning("No accounts found. Please create an account first.")
            return
        
        # Account selection
        account_options = [f"{acc_no} - {st.session_state.accounts[acc_no].account_holder}" 
                          for acc_no in st.session_state.accounts]
        
        # Get current index safely
        current_index = 0
        if st.session_state.current_account:
            keys = list(st.session_state.accounts.keys())
            if st.session_state.current_account in keys:
                current_index = keys.index(st.session_state.current_account)
        
        selected_account = st.selectbox("Select Account", account_options, index=current_index)
        acc_no = selected_account.split(" - ")[0]
        account = st.session_state.accounts[acc_no]
        
        # Display account summary
        st.markdown(f"### Account Summary: {account.account_holder}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="account-card">
                <h3>Account Details</h3>
                <p><strong>Account Holder:</strong> {account.account_holder}</p>
                <p><strong>Account Type:</strong> {account.account_type}</p>
                <p><strong>Account Number:</strong> {account.account_no}</p>
                <p><strong>Opening Date:</strong> {account.opening_date}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display balance
            balance = account.get_balance()
            st.markdown(f"""
            <div class="account-card">
                <h3>Balance Information</h3>
                <h2 style="text-align:center; color:#283593;">₹{balance:,.2f}</h2>
                <p style="text-align:center;">Current Available Balance</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Transaction summary
            total_credit = 0
            total_debit = 0
            transaction_count = 0
            
            if acc_no in st.session_state.transactions:
                transactions = st.session_state.transactions[acc_no]
                transaction_count = len(transactions)
                for txn in transactions:
                    if txn['type'] == 'Credit':
                        total_credit += txn['amount']
                    else:
                        total_debit += txn['amount']
            
            st.markdown(f"""
            <div class="account-card">
                <h3>Transaction Summary</h3>
                <p><strong>Total Transactions:</strong> {transaction_count}</p>
                <p><strong>Total Credits:</strong> <span style="color:#43a047;">₹{total_credit:,.2f}</span></p>
                <p><strong>Total Debits:</strong> <span style="color:#e53935;">₹{total_debit:,.2f}</span></p>
                <p><strong>Net Change:</strong> <span style="color:#1a237e;">₹{total_credit - total_debit:,.2f}</span></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Bank Summary Page
    elif choice == "Bank Summary":
        st.subheader("Bank Summary")
        
        if not st.session_state.accounts:
            st.warning("No accounts found. Please create an account first.")
            return
        
        # Bank statistics
        total_accounts = len(st.session_state.accounts)
        total_balance = sum(acc.get_balance() for acc in st.session_state.accounts.values())
        
        # Display bank summary
        st.markdown("### Bank Overview")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Accounts</h3>
                <h1>{total_accounts}</h1>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Balance</h3>
                <h1>₹{total_balance:,.2f}</h1>
            </div>
            """, unsafe_allow_html=True)
        
        # List all accounts
        st.markdown("### All Accounts")
        accounts_data = []
        for acc in st.session_state.accounts.values():
            accounts_data.append({
                "Account No": acc.account_no,
                "Account Holder": acc.account_holder,
                "Type": acc.account_type,
                "Balance": acc.get_balance(),
                "Opening Date": acc.opening_date
            })
        
        st.dataframe(
            pd.DataFrame(accounts_data).style.format({'Balance': '₹{:.2f}'}),
            height=400
        )

if __name__ == "__main__":
    main()