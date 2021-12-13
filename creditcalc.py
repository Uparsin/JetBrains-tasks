import math
import argparse

# constants
percent_100 = 100
months_in_year = 12

parser = argparse.ArgumentParser()


parser.add_argument("--type", choices=["diff", "annuity"], help="Incorrect parameters")
parser.add_argument("--payment", type=int)
parser.add_argument("--periods", type=int)
parser.add_argument("--principal", type=int)
parser.add_argument("--interest", type=float)

args = parser.parse_args()

if args.type == "diff":
    if args.interest is None:
        print("Incorrect parameters.")
    else:
        i = args.interest / (months_in_year * percent_100)
        overpayment = 0
        for counter in range(args.periods):
            pay = (args.principal / args.periods) + i * (args.principal - (args.principal * counter) / args.periods)
            overpayment += math.ceil(pay - (args.principal / args.periods))
            print(f"Month {counter + 1}: payment is {math.ceil(pay)}")
        print()
        print(f"Overpayment = {overpayment}")

elif args.type == "annuity":
    if args.interest is None:
        print("Incorrect parameters.")
    else:
        i = args.interest / (months_in_year * percent_100)
        if args.principal is None:
            loan_principal = args.payment / ((i * math.pow(1 + i, args.periods)) / (math.pow(1 + i, args.periods) - 1))
            print(loan_principal)
        else:
            if args.payment is None:
                A = math.ceil(args.principal * ((i * pow((1 + i), args.periods)) / (pow((1 + i), args.periods) - 1)))
                overpayment = args.principal - A * args.periods
                print(f"Your annuity payment = {A}!")
                print(f"Overpayment = {overpayment}")
            else:
                n = math.log(args.payment / (args.payment - i * args.principal), 1 + i)  # number of months
                n_round = math.ceil(n)
                years = int(n_round // months_in_year)
                months = int(n_round % months_in_year)
                overpayment = args.principal - n_round * args.payment
                print(f"It will take {years} years and {months} months to repay this loan!")
                print(f"Overpayment = {overpayment}")
else:
    print("Incorrect parameters.")
