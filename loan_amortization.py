import pandas as pd

def calculate_emi(principal, annual_interest_rate, tenure_years):
    monthly_interest_rate = annual_interest_rate / (12 * 100)
    total_payments = tenure_years * 12
    emi = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
    return emi, monthly_interest_rate, total_payments

def generate_amortization_schedule(principal, emi, monthly_interest_rate, total_payments, extra_payment=0, extra_payment_duration=0):
    remaining_balance = principal
    schedule = []
    
    for month in range(1, total_payments + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = emi - interest_payment
        total_principal_payment = principal_payment + extra_payment if month <= extra_payment_duration else principal_payment
        remaining_balance -= total_principal_payment
        
        schedule.append([
            month,
            round(emi + (extra_payment if month <= extra_payment_duration else 0), 2),
            round(interest_payment, 2),
            round(total_principal_payment, 2),
            round(remaining_balance, 2)
        ])
        
        if remaining_balance <= 0:
            break
    
    return pd.DataFrame(schedule, columns=["Month", "EMI", "Interest Payment", "Principal Payment", "Remaining Balance"])

def main():
    # Get loan details from the user
    principal = float(input("Enter the loan amount (principal): "))
    annual_interest_rate = float(input("Enter the annual interest rate (in %): "))
    tenure_years = int(input("Enter the loan tenure (in years): "))
    
    # Get extra payment details from the user
    extra_payment = float(input("Enter the extra payment amount per month (or 0 if none): "))
    extra_payment_duration = int(input("Enter the duration for extra payments in months (or 0 if none): "))

    emi, monthly_interest_rate, total_payments = calculate_emi(principal, annual_interest_rate, tenure_years)
    amortization_schedule = generate_amortization_schedule(principal, emi, monthly_interest_rate, total_payments, extra_payment, extra_payment_duration)
    
    print("\nMonthly EMI without extra payments:", round(emi, 2))
    print("Amortization Schedule with extra payments:")
    print(amortization_schedule)  # Print the entire amortization schedule

    # Save the schedule to an Excel file
    file_name = "amortization_schedule_with_extra_payments.xlsx"
    amortization_schedule.to_excel(file_name, index=False)
    print(f"\nFull amortization schedule saved to '{file_name}'")

if __name__ == "__main__":
    main()
