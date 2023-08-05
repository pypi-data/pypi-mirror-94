import collections
import csv
import decimal
import os


from .FinanceObject import FinanceObject
from .financeutils import Salary, Parent

CostTuple = collections.namedtuple('CostTuple', 'mothers, fathers')

# Standard Library setup
decimal_context = decimal.getcontext()
decimal_context.prec = 8
D = decimal.Decimal

# __location__ setup for opening included csv files
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class CSOBaseClass:
    last_ws_result = None  # subclass must override
    expense_line_numbers = []
    template_lines = []

    def __init__(self, mother, father, number_children,
                 childcare_costs: CostTuple = None, insurance_costs: CostTuple = None,
                 additional_costs: CostTuple = None):
        self.mother, self.father, self.number_children = mother, father, number_children

        self.childcare_costs = childcare_costs if childcare_costs else CostTuple(mothers=D(214) * D(52) / D(12), fathers=D(0))
        self.insurance_costs = insurance_costs if insurance_costs else CostTuple(mothers=D(390), fathers=D(0))
        self.additional_costs = additional_costs if additional_costs else CostTuple(mothers=D(0), fathers=D(0))

        self.worksheet_lines = {}
        self.worksheet_results = {}

    def execute_line(self, line_number):
        rslt_key = line_number
        line = self.worksheet_lines[line_number]
        rslt = line(self.worksheet_results)
        self.worksheet_results[rslt_key] = rslt
        return rslt

    def get_support_from_schedule(self, combined_gmi, number_children):
        combined_gmi = ((combined_gmi // 100) + (1 if combined_gmi % 100 else 0)) * 100
        max_value = max(self.basic_support_schedule.keys())
        combined_gmi = min(max_value, combined_gmi)
        return self.basic_support_schedule[combined_gmi][number_children-1]

    def normalize_costs(self):
        # ensure that costs are in `CostTuple`s and not anything else.
        for cost in [self.childcare_costs,
                     self.insurance_costs,
                     self.additional_costs]:
            cost = CostTuple(*cost)

    def run_worksheet(self):
        if not len(self.worksheet_lines):
            self.populate_worksheet_lines()
        for line_number, line in enumerate(self.worksheet_lines, 1):
            self.execute_line(line_number)

        self.normalize_costs()

        self.father.effective_salary = self.fathers_effective_salary
        self.mother.effective_salary = self.mothers_effective_salary
        return sorted(self.worksheet_results.items())

    run = run_worksheet


    @property
    def final_payment(self):
        try:
            return self.worksheet_results[self.last_ws_result]
        except (AttributeError, KeyError):
            raise AttributeError('final_payment unknown until worksheet is ran')

    @property
    def fathers_payment(self):
        return self.parent_payment(self.father)

    @property
    def fathers_effective_salary(self):
        return self.parent_effective_salary(self.father)

    @property
    def mothers_payment(self):
        return self.parent_payment(self.mother)

    @property
    def mothers_effective_salary(self):
        return self.parent_effective_salary(self.mother)

    @property
    def effective_salaries(self):
        return self.mother.effective_salary, self.father.effective_salary

    def parent_payment(self, parent):
        try:
            payee, payment = self.worksheet_results[self.last_ws_result]
        except IndexError:
            self.run_worksheet()
            return self.parent_payment(parent)
        return payment if parent is payee else -payment

    def parent_effective_salary(self, parent):
        parent_index = 0 if parent is self.mother else 1
        child_expense_line_numbers = self.expense_line_numbers
        child_expense_results = [self.worksheet_results[x] for x
                                 in child_expense_line_numbers]
        child_expenses = sum(x[parent_index] for x in child_expense_results)
        gmi = parent.gross_monthly_income
        payment = self.parent_payment(parent)
        return Salary(12 * (gmi - payment - child_expenses))

    @property
    def basic_support_schedule(self):

        try:
            return self._basic_support_schedule

        except AttributeError:
            self._basic_support_schedule = {}

            with open(os.path.join(__location__, 'nm-cs-support.txt')) as csvfile:
                reader = csv.reader(csvfile, delimiter=' ')

                for row, *children in reader:
                    children = tuple(map(self.clean_number, [child for child in children if child]))
                    self._basic_support_schedule[self.clean_number(row)] = tuple(map(D, children))

            return self._basic_support_schedule

    @staticmethod
    def clean_number(number):
        number = ''.join(number.split(','))
        try:
            number = D(number)
        except:
            print(repr(number))
            raise
        return number

    def reset_parents(self):
        self.mother.reset_additional()
        self.father.reset_additional()

    def transfer_from_father(self, monthly_amount):
        self.father.additional_monthly -= D(monthly_amount)
        self.mother.additional_monthly += D(monthly_amount)

    def render_output(self):
        output = self.run()
        lines = []
        for template, (num, items) in zip(self.template_lines, output):
            try:
                line = template.format(*items)
            except TypeError:
                line = template.format(items)
            lines.append(line)
        return '\n'.join(lines)


class ProportionalChildSupportObligation(CSOBaseClass):
    last_ws_result = 18
    expense_line_numbers = 12, 13, 14
    template_lines = (
        '1.  Gross Monthly Income:                   \n\t\t\t${0:7.2f}\t+${1:7.2f}\t=${2:7.2f}',
        '2.  Percentage of Combined Income:          \n\t\t\t {0:7.2%}\t+{1:7.2%}\t=100%',
        '3.  Number of Children:                     \n\t\t\t {0}',
        '4.  Basic Support from Schedule:            \n\t\t\t${0:7.2f}',
        '5.  Shared Responsibility Basic Obligation: \n\t\t\t${0:7.2f}\t+${1:7.2f}',
        '6.  Each Parent\'ts share:                  \n\t\t\t${0:7.2f}\t+${1:7.2f}',
        '7.  Number of 24 hour days with each parent:\n\t\t\t {0:7}\t+{1:7}\t=365',
        '8.  Percentage with each parent:            \n\t\t\t {0:7.2%}\t+{1:7.2%}\t=100%',
        '9.  Amount Retained:                        \n\t\t\t${0:7.2f}\t${1:7.2f}',
        '10. Each Parent\'s Obligation:              \n\t\t\t${0:7.2f}\t${1:7.2f}',
        '11. Amount Transferred:                     \n\t\t\t${1:7.2f} from {0.name}',
        '12. Children\'s Health & Dental Insurance Premiums: \n\t\t\t${0:7.2f}\t+${1:7.2f}',
        '13. Work-Related Child Care:                \n\t\t\t${0:7.2f}\t+${1:7.2f}',
        '14. Additional Expenses:                    \n\t\t\t${0:7.2f}\t+${1:7.2f}',
        '15. Total Additional Payments:              \n\t\t\t${0:7.2f}\t+${1:7.2f}',
        '16. Each Parent\'s Obligation:              \n\t\t\t${0:7.2f}\t+${1:7.2f}',
        '17. Amount Transferred:                     \n\t\t\t${1:7.2f} from {0.name}\t',
        '18. Payment:                                \n\t\t\t${1:7.2f} from {0.name}'
    )

    def populate_worksheet_lines(self):
        def line1(results):
            """
            Gross Monthly Income
            """
            mother, father = self.mother.gross_monthly_income, self.father.gross_monthly_income
            combined = mother + father
            rslt = mother, father, combined

            return rslt
        self.worksheet_lines[1] = line1

        def line2(results):
            """
            Percentage of Combined Income
            (each parent's income divided by combined income)
            """
            mother_gmi, father_gmi, combined_gmi = results[1]
            rslt = mother_gmi / combined_gmi, father_gmi / combined_gmi

            return rslt
        self.worksheet_lines[2] = line2

        def line3(results):
            """
            Number of Children
            """
            rslt = self.number_children
            return rslt
        self.worksheet_lines[3] = line3

        def line4(results):
            """
            Basic support from Schedule
            (use combined income from Line 1)
            """
            rslt = self.get_support_from_schedule(results[1][2], results[3])
            return rslt
        self.worksheet_lines[4] = line4

        def line5(results):
            """
            Shared Responsibility Basic Obligation
            (Line 4 x 1.5)
            """
            rslt = results[4] * D('1.5')
            return (rslt, ) * 2
        self.worksheet_lines[5] = line5

        def line6(results):
            """
            Each Parent's Share
            (Line 5 x each parent's Line 2)
            """
            mother_share, father_share = [
                srbo * pci
                for srbo, pci
                in zip(results[2], results[5])
            ]
            rslt = mother_share, father_share
            return rslt
        self.worksheet_lines[6] = line6

        def line7(results):
            """
            Number of 24-hr days with each parent
            (must total 365)
            (ignores setting for father and takes 365 - mother's annual custody)
            """
            mother, father = self.mother, self.father
            rslt = mother.annual_custody, 365-mother.annual_custody
            return rslt
        self.worksheet_lines[7] = line7

        def line8(results):
            """
            Percentage with each parent
            (Line 7 divided by 365)
            """
            rslt = [
                ac/D(365)
                for ac
                in results[7]
            ]
            return rslt
        self.worksheet_lines[8] = line8

        def line9(results):
            """
            Amount retained
            (Line 6 multiplied by Line 8 for each parent)
            """
            rslt = [
                l6_result * l8_result
                for l6_result, l8_result
                in zip(results[6], results[8])
            ]
            return rslt
        self.worksheet_lines[9] = line9

        def line10(results):
            """
            Each Parent's Obligation
            (Subtract Line 9 from Line 6)
            """
            rslt = [
                l6_result - l9_result
                for l6_result, l9_result
                in zip(results[6], results[9])
            ]
            return rslt
        self.worksheet_lines[10] = line10

        def line11(results):
            """
            Amount Transferred for basic Child Support
            (subtract smaller amount on Line 10 from larger amount on Line 10;
             Parent with larger amount on Line 10 pays other parent the difference)
            """
            l10_results = results[10]
            if l10_results[0] > l10_results[1]:  # TODO: implement mapping to/from parent index to eliminate this pattern
                payee = self.mother
            else:
                payee = self.father
            rslt = payee, max(l10_results) - min(l10_results)
            return rslt
        self.worksheet_lines[11] = line11

        def line12(results):
            """
            Children's Health and Dental Insurance Premiums
            """
            return self.insurance_costs
        self.worksheet_lines[12] = line12

        def line13(results):
            """
            Work-Related Child Care
            """
            return self.childcare_costs
        self.worksheet_lines[13] = line13

        def line14(results):
            """
            Additional Expenses
            """
            return self.additional_costs
        self.worksheet_lines[14] = line14

        def line15(results):
            """
            Total Additional Payments
            (add Lines 12, 13 and 14 for each parent and combined column)
            (combined column not tracked here because computers can do math good)
            """
            rslt = [
                sum(payments)
                for payments
                in zip(
                    results[12],
                    results[13],
                    results[14]
                )
            ]
            return rslt
        self.worksheet_lines[15] = line15

        def line16(results):
            """
            Each Parent's Obligation
            (combined Column Line 15 multiplied by each parent's Line 2)
            """
            combined_l15 = sum(results[15])

            rslt = [
                combined_l15 * l2_result
                for l2_result
                in results[2]
            ]
            return rslt
        self.worksheet_lines[16] = line16

        def line17(results):
            """
            Amount transferred for additional expenses
            (Subtract each parent's Line 15 from his/her Line 15.
             Parent with "minus" figure pays that amount to the other parent.)
            (Returns parent and the amount to transfer as a positive number)
            """
            rslt = [
                l15_result - l16_result
                for l15_result, l16_result
                in zip(
                    results[15],
                    results[16]
                )
            ]
            if rslt[0] < rslt[1]:
                payee = self.mother
            else:
                payee = self.father
            rslt = payee, max(rslt)
            return rslt
        self.worksheet_lines[17] = line17

        def line18(results):
            """
            Combine Lines 11 and 17
            (by addition if same parent pays on both lines;
             otherwise, by subtraction)
            """
            rslt = []

            l11_payee, l11_amt = results[11]
            l17_payee, l17_amt = results[17]
            if l11_payee is l17_payee:
                return l11_payee, l11_amt + l17_amt

            if l11_amt > l17_amt:
                return l11_payee, l11_amt - l17_amt
            else:
                return l17_payee, l17_amt - l11_amt

        self.worksheet_lines[18] = line18


class BasicChildSupportObligation(CSOBaseClass):
    last_ws_result = 11
    expense_line_numbers = 5, 6, 7
    template_lines = (
        '1.  Gross Monthly Income:                   \n\t\t\t${0:7.2f}\t+${1:7.2f}\t=${2:7.2f}',
        '2.  Percentage of Combined Income:          \n\t\t\t {0:7.2%}\t+{1:7.2%}\t=100%',
        '3.  Number of Children:                     \n\t\t\t {0}',
        '4.  Basic Support from Schedule:            \n\t\t\t${0:7.2f}\t+${1:7.2f}\t${2:7.2f}',
        '5. Children\'s Health & Dental Insurance Premiums: \n\t\t\t${0:7.2f}\t+${1:7.2f}\t${2:7.2f}',
        '6. Work-Related Child Care:                 \n\t\t\t${0:7.2f}\t+${1:7.2f}\t${2:7.2f}',
        '7. Additional Expenses:                     \n\t\t\t${0:7.2f}\t+${1:7.2f}\t${2:7.2f}',
        '8. Total Support:                           \n\t\t\t${0:7.2f}\t+${1:7.2f}\t${2:7.2f}',
        '9. Each Parent\'s Obligation:              \n\t\t\t${0:7.2f}\t+${1:7.2f}',
        '10. Enter amount for each parent from line 8:      \n\t\t\t${0:7.2f}\t+${1:7.2f}',
        '11. Payment:                                \n\t\t\t${1:7.2f} from {0.name}'
    )

    def populate_worksheet_lines(self):
        def line1(results):
            """
            Gross Monthly Income
            """
            mother, father = self.mother.gross_monthly_income, self.father.gross_monthly_income
            combined = mother + father
            rslt = mother, father, combined

            return rslt
        self.worksheet_lines[1] = line1

        def line2(results):
            """
            Percentage of Combined Income
            (each parent's income divided by combined income)
            """
            mother_gmi, father_gmi, combined_gmi = results[1]
            rslt = mother_gmi / combined_gmi, father_gmi / combined_gmi

            return rslt
        self.worksheet_lines[2] = line2

        def line3(results):
            """
            Number of Children
            """
            rslt = self.number_children
            return rslt
        self.worksheet_lines[3] = line3

        def line4(results):
            """
            Basic support from Schedule
            (use combined income from Line 1)
            """
            rslt = self.get_support_from_schedule(results[1][2], results[3])
            return [D(0), D(0), rslt]
        self.worksheet_lines[4] = line4

        def line5(results):
            """
            Children's Health and Dental Insurance Premiums
            """
            return self.insurance_costs + (sum(self.insurance_costs), )
        self.worksheet_lines[5] = line5

        def line6(results):
            """
            Work-Related Child Care
            """
            return self.childcare_costs + (sum(self.childcare_costs), )
        self.worksheet_lines[6] = line6

        def line7(results):
            """
            Additional Expenses
            """
            return self.additional_costs + (sum(self.additional_costs), )
        self.worksheet_lines[7] = line7

        def line8(results):
            """
            Total Support
            (Add Lines 4, 5, 6 and 7 for each parent and for combined column)
            (combined column not tracked here because computers can do math good)
            """
            # print(results[4], results[5], results[6], results[7])
            rslt = [
                sum(payments)
                for payments
                in zip(
                    results[4],
                    results[5],
                    results[6],
                    results[7]
                )
            ]
            return rslt
        self.worksheet_lines[8] = line8

        def line9(results):
            """
            Each Parent's Obligation
            (Combined Column Line 8 x each parent's Line 2)
            """
            combined_l15 = results[8][2]  # no idea why this variable is named this dumb shit

            rslt = [
                combined_l15 * l2_result
                for l2_result in
                results[2]
            ]
            return rslt
        self.worksheet_lines[9] = line9

        def line10(results):
            """
            Enter amount for each parent from Line 8
            (wtf, why?)
            """
            rslt = results[8]
            return rslt
        self.worksheet_lines[10] = line10

        def line11(results):
            """
            Each Parent's net obligation
            (Subtract Line 10 from Line 9 for each parent)
            """
            rslt = [
                l9_result - l10_result
                for l9_result, l10_result
                in zip(results[9], results[10])
            ]
            if rslt[0] > rslt[1]:
                payee = self.mother
            else:
                payee = self.father

            return payee, max(rslt)
        self.worksheet_lines[11] = line11


class DynamicChildSupportObligation:

    def __init__(self, mother: Parent, father: Parent, number_children,
                 childcare_costs: CostTuple = None, insurance_costs: CostTuple = None,
                 additional_costs: CostTuple = None):

        m_days = mother.weekly_custody
        f_days = father.weekly_custody
        assert int(m_days + f_days) == 7

        m_annual_days = m_days / 7 * 365
        f_annual_days = f_days / 7 * 365
        assert int(m_annual_days + f_annual_days) == 365
        if min(m_annual_days, f_annual_days) <= 128:
            self.cso_type = BasicChildSupportObligation
        else:
            self.cso_type = ProportionalChildSupportObligation

        self.cso = self.cso_type(mother, father, number_children, childcare_costs, insurance_costs,
                                 additional_costs)

    def __getattr__(self, name):
        return getattr(self.cso, name)


