import streamlit as st
from Bank import Bank


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Banking Management System",
    page_icon="🏦",
    layout="wide"
)


# =====================================================
# BANK OBJECT
# =====================================================

bank = Bank()


# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account_no" not in st.session_state:
    st.session_state.account_no = None


# =====================================================
# CSS
# =====================================================

st.markdown(
    """
    <style>

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
    }

    .subtitle {
        text-align: center;
        color: gray;
        font-size: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# LOGIN
# =====================================================

def login_page():

    st.markdown(
        '<div class="title">🏦 Banking Management System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Secure Digital Banking</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.subheader("🔐 Login")

        account_no = st.text_input(
            "Account Number",
            placeholder="Example: ABC123@"
        )

        pin = st.text_input(
            "4 Digit PIN",
            type="password",
            max_chars=4
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if not account_no or not pin:

                st.error(
                    "Please enter account number and PIN."
                )

            else:

                account = bank.login(
                    account_no,
                    pin
                )

                if account:

                    st.session_state.logged_in = True

                    st.session_state.account_no = (
                        account["accountNo"]
                    )

                    st.success(
                        "Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid account number or PIN."
                    )


# =====================================================
# CREATE ACCOUNT
# =====================================================

def create_account_page():

    st.subheader("📝 Create New Account")

    with st.form("create_account_form"):

        name = st.text_input(
            "Full Name"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=18
        )

        email = st.text_input(
            "Email"
        )

        pin = st.text_input(
            "4 Digit PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button(
            "Create Account",
            use_container_width=True
        )

        if submit:

            success, result = bank.create_account(
                name,
                age,
                email,
                pin
            )

            if success:

                st.success(
                    "Account created successfully!"
                )

                st.info(
                    f"Your Account Number is: "
                    f"**{result['accountNo']}**"
                )

                st.warning(
                    "Save your account number."
                )

            else:

                st.error(result)


# =====================================================
# DASHBOARD
# =====================================================

def dashboard():

    account_no = st.session_state.account_no

    account = bank.get_account(account_no)

    if account is None:

        st.session_state.logged_in = False
        st.session_state.account_no = None

        st.rerun()

        return

    # -------------------------------------------------
    # HEADER
    # -------------------------------------------------

    col1, col2 = st.columns([5, 1])

    with col1:

        st.title("🏦 Banking Dashboard")

        st.write(
            f"Welcome, **{account['name']}**"
        )

    with col2:

        if st.button(
            "Logout",
            use_container_width=True
        ):

            st.session_state.logged_in = False

            st.session_state.account_no = None

            st.rerun()

    st.divider()

    # -------------------------------------------------
    # ACCOUNT SUMMARY
    # -------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "💰 Balance",
            f"₹{float(account.get('balance', 0)):,.2f}"
        )

    with col2:

        st.metric(
            "💳 Account",
            account["accountNo"]
        )

    with col3:

        st.metric(
            "📊 Transactions",
            len(account.get("transactions", []))
        )

    # -------------------------------------------------
    # SIDEBAR
    # -------------------------------------------------

    option = st.sidebar.selectbox(
        "Banking Menu",
        [
            "🏠 Dashboard",
            "👤 Account Details",
            "💰 Deposit Money",
            "💸 Withdraw Money",
            "📝 Update Details",
            "📊 Transaction History",
            "🗑️ Delete Account"
        ]
    )

    # =================================================
    # DASHBOARD
    # =================================================

    if option == "🏠 Dashboard":

        st.header("Welcome to your account")

        col1, col2 = st.columns(2)

        with col1:

            st.info(
                """
                ### 💰 Deposit

                Add money to your account.

                Maximum:
                **₹10,000 per transaction**
                """
            )

        with col2:

            st.info(
                """
                ### 💸 Withdraw

                Withdraw money from your account.

                You cannot withdraw more than
                your available balance.
                """
            )

        st.divider()

        st.subheader("Account Overview")

        details = bank.get_details(account_no)

        st.table(details)

    # =================================================
    # ACCOUNT DETAILS
    # =================================================

    elif option == "👤 Account Details":

        st.header("👤 Account Details")

        details = bank.get_details(account_no)

        st.table(details)

    # =================================================
    # DEPOSIT
    # =================================================

    elif option == "💰 Deposit Money":

        st.header("💰 Deposit Money")

        current_balance = float(
            account.get("balance", 0)
        )

        st.metric(
            "Current Balance",
            f"₹{current_balance:,.2f}"
        )

        st.write(
            "Maximum deposit per transaction: **₹10,000**"
        )

        with st.form("deposit_form"):

            amount = st.number_input(
                "Enter Amount",
                min_value=1.0,
                max_value=10000.0,
                value=100.0,
                step=100.0
            )

            submit = st.form_submit_button(
                "💰 Deposit Money",
                use_container_width=True
            )

            if submit:

                success, message = bank.deposit(
                    account_no,
                    amount
                )

                if success:

                    st.success(message)

                    st.rerun()

                else:

                    st.error(message)

    # =================================================
    # WITHDRAW
    # =================================================

    elif option == "💸 Withdraw Money":

        st.header("💸 Withdraw Money")

        st.metric(
            "Available Balance",
            f"₹{float(account.get('balance', 0)):,.2f}"
        )

        with st.form("withdraw_form"):

            amount = st.number_input(
                "Enter Amount",
                min_value=1.0,
                value=100.0,
                step=100.0
            )

            submit = st.form_submit_button(
                "💸 Withdraw Money",
                use_container_width=True
            )

            if submit:

                success, message = bank.withdraw(
                    account_no,
                    amount
                )

                if success:

                    st.success(message)

                    st.rerun()

                else:

                    st.error(message)

    # =================================================
    # UPDATE DETAILS
    # =================================================

    elif option == "📝 Update Details":

        st.header("📝 Update Account Details")

        st.info(
            "Age and account number cannot be changed."
        )

        with st.form("update_form"):

            name = st.text_input(
                "Name",
                value=account["name"]
            )

            email = st.text_input(
                "Email",
                value=account["email"]
            )

            new_pin = st.text_input(
                "New 4 Digit PIN",
                type="password",
                max_chars=4
            )

            submit = st.form_submit_button(
                "Update Details",
                use_container_width=True
            )

            if submit:

                success, message = bank.update_account(
                    account_no,
                    name,
                    email,
                    new_pin
                )

                if success:

                    st.success(message)

                    st.rerun()

                else:

                    st.error(message)

    # =================================================
    # TRANSACTION HISTORY
    # =================================================

    elif option == "📊 Transaction History":

        st.header("📊 Transaction History")

        transactions = bank.get_transactions(
            account_no
        )

        if transactions:

            st.dataframe(
                transactions,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No transactions yet."
            )

    # =================================================
    # DELETE ACCOUNT
    # =================================================

    elif option == "🗑️ Delete Account":

        st.header("🗑️ Delete Account")

        st.error(
            "⚠️ This action cannot be undone."
        )

        confirm = st.checkbox(
            "I understand that my account will be permanently deleted."
        )

        if st.button(
            "Delete My Account",
            use_container_width=True
        ):

            if not confirm:

                st.warning(
                    "Please confirm account deletion."
                )

            else:

                success, message = bank.delete_account(
                    account_no
                )

                if success:

                    st.success(message)

                    st.session_state.logged_in = False

                    st.session_state.account_no = None

                    st.rerun()

                else:

                    st.error(message)


# =====================================================
# MAIN
# =====================================================

if st.session_state.logged_in:

    dashboard()

else:

    tab1, tab2 = st.tabs(
        [
            "🔐 Login",
            "📝 Create Account"
        ]
    )

    with tab1:
        login_page()

    with tab2:
        create_account_page()