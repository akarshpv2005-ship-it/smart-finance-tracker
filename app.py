import streamlit as st


st.set_page_config(
    page_title="Monthly EMI & Savings Predictor",
    page_icon="💰",
    layout="centered",
)

CURRENCY = "₹"


def calculate_emi(principal, annual_rate, months):
    monthly_rate = annual_rate / 1200
    if monthly_rate == 0:
        return principal / months
    rate_factor = (1 + monthly_rate) ** months
    return principal * monthly_rate * rate_factor / (rate_factor - 1)


st.title("💰 Salary & EMI Predictor")
st.write(
    "Enter your monthly salary and loan details to estimate your EMI "
    "and how much money may be left for savings."
)

with st.form("emi_prediction"):
    st.subheader("Your monthly finances")
    salary = st.number_input(
        "Monthly take-home salary",
        min_value=0.0,
        value=50000.0,
        step=1000.0,
        help="Enter the salary amount you receive each month.",
    )
    expenses = st.number_input(
        "Other monthly expenses (excluding this loan EMI)",
        min_value=0.0,
        value=15000.0,
        step=500.0,
        help="Include rent, bills, food, and other spending. Do not include this loan's EMI.",
    )

    st.subheader("Loan details")
    loan_amount = st.number_input(
        "Loan amount",
        min_value=1.0,
        value=500000.0,
        step=10000.0,
    )
    annual_rate = st.number_input(
        "Annual interest rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
    )
    years = st.number_input(
        "Loan term (years)",
        min_value=1,
        max_value=50,
        value=5,
        step=1,
    )
    submitted = st.form_submit_button("Predict my EMI and savings", type="primary")

if submitted:
    months = int(years * 12)
    emi = calculate_emi(loan_amount, annual_rate, months)
    total_repayment = emi * months
    total_interest = total_repayment - loan_amount
    monthly_balance = salary - expenses - emi

    st.divider()
    st.subheader("Your prediction")
    first, second = st.columns(2)
    first.metric("Estimated monthly EMI", f"{CURRENCY}{emi:,.2f}")
    second.metric("Estimated money left each month", f"{CURRENCY}{monthly_balance:,.2f}")

    third, fourth = st.columns(2)
    third.metric("Total loan repayment", f"{CURRENCY}{total_repayment:,.2f}")
    fourth.metric("Total interest over loan term", f"{CURRENCY}{total_interest:,.2f}")

    if monthly_balance > 0:
        st.success(
            f"After the listed expenses and estimated EMI, about "
            f"{CURRENCY}{monthly_balance:,.2f} may remain each month. "
            "This is your potential monthly savings before any expenses not entered above."
        )
    elif monthly_balance == 0:
        st.warning("Your salary would be fully used by the listed expenses and estimated EMI.")
    else:
        st.error(
            f"The estimated EMI and listed expenses exceed your salary by "
            f"{CURRENCY}{abs(monthly_balance):,.2f} per month."
        )

    st.caption(
        "This is an estimate using a standard fixed-rate EMI formula. "
        "Actual lender terms, fees, taxes, and variable rates may change the amount."
    )
