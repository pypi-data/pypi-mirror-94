
"""
Library of classes and functions for making personal finance decisions.
"""


__author__ = 'William.George'

# Standard Library
import collections
from decimal import Decimal
import decimal
from itertools import repeat
import os

# Package Imports
from typing import Union

from .FinanceObject import FinanceObjectMC

# Standard Library setup
decimal_context = decimal.getcontext()
decimal_context.prec = 8
D = Decimal

# __location__ setup for opening included csv files
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Annuity(FinanceObjectMC):
    """
    Investment, loan, or other instrument to which a fixed payment and interest rate
        are applied.

    interest_rate (should not be negative except through subclass) | apr
    initial_balance
    beginning_date
    current_date -> state
    current_balance -> state
    state: state object with current date, current balance, current apr
    """

    _mandatory_fields = ('beginning_date', 'balance', 'apr')
    _optional_fields = (('payment_amount', None),
                        ('compounding_periods_per_year', 12),
                        ('payments_per_year', 12),
                        ('duration', None)
    )

    def __init__(self, *args, **kwargs):
        self.payment_amount, self.compounding_periods_per_year, self.duration, \
            self.beginning_date, self.balance, self.apr = repeat(None, 6)

        values_to_decimal(kwargs)
        super().__init__(*args, **kwargs)


    def regular_annuity(self, **kwargs):
        kwargs = collections.ChainMap(kwargs, self.__dict__)
        m = kwargs['payment_amount']
        r = kwargs['apr']
        n = kwargs['compounding_periods_per_year']
        t = kwargs['duration']

        top = ((1 + (r / n)) ** (n * t)) - 1
        bottom = r / n
        A = m * (top / bottom)
        return A

    def future_value(self, **kwargs):
        kwargs = collections.ChainMap(kwargs, self.__dict__)
        PV = kwargs['balance']  # Present Value
        r = kwargs['apr']
        n = kwargs['compounding_periods_per_year']
        t = kwargs['duration']
        r = r / n
        t = n * t
        P = PV * ((1 + r) ** t)
        return P

    def future_balance(self, **kwargs):
        return self.future_value(**kwargs) + self.regular_annuity(**kwargs)

    def present_value(self, **kwargs):
        kwargs = collections.ChainMap(kwargs, self.__dict__)
        r = kwargs['apr']
        n = kwargs['compounding_periods_per_year']
        t = kwargs['duration']
        P = kwargs['payment_amount']
        r = r / n
        t = n * t

        PV = (1 - ((1 + r) ** -n)) / (r * P)
        return PV


class Loan(Annuity):
    """
    Loan (essentially Annuity with a negative Interest Rate) object.
    """
    _optional_fields = (('loan_type', 'fixed'),)

    def __init__(self, **kwargs):
        values_to_decimal(kwargs)
        super().__init__(**kwargs)

    def remaining_balance(self, **kwargs):
        return self.future_value(**kwargs) - self.regular_annuity(**kwargs)

    future_balance = remaining_balance

    def amortize_payment(self, **kwargs):
        kwargs = collections.ChainMap(kwargs, self.__dict__)
        PV = kwargs['balance']  # Present Value
        r = kwargs['apr']  # APR
        n = kwargs['compounding_periods_per_year']
        t = kwargs['duration']  # in years
        r = r / n  # rate per period
        t = n * t  # number of periods

        return r * PV / (1 - ((1 + r) ** (t * -1)))


class CashFlow:
    MONTHLY = D(365/12)
    ANNUAL = D(365)
    H_ANNUAL = D(2080)
    APS_H_ANNUAL = D(1196)
    BIWEEKLY = D(14)
    BIMONTHLY = MONTHLY/D(2)
    default_rate_period_in_days = MONTHLY
    default_period_in_days = MONTHLY

    def __init__(self, rate: Union[str, int, Decimal], rate_period_in_days=None, period_in_days=None):
        if rate_period_in_days is None:
            rate_period_in_days = self.default_rate_period_in_days
        if period_in_days is None:
            period_in_days = self.default_period_in_days
        self.rate = rate
        self.rate_period_in_days = rate_period_in_days
        self.period_in_days = period_in_days

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = D(value)

    @property
    def annual_rate(self):
        return self.rate / self.rate_period_in_days * self.ANNUAL

    @property
    def monthly_rate(self):
        return self.rate / self.rate_period_in_days * self.MONTHLY

    @property
    def hourly_rate(self):
        return self.annual_rate / self.H_ANNUAL

    def __eq__(self, other):
        return self.annual_rate == other.annual_rate


class Salary(CashFlow):
    default_rate_period_in_days = CashFlow.ANNUAL
    default_period_in_days = CashFlow.BIWEEKLY

    @classmethod
    def from_hourly(cls, hourly):
        return cls(rate=D(hourly) * CashFlow.H_ANNUAL)

    def __repr__(self):
        msg = 'Salary({0})'.format(str(self.annual_rate))
        return msg


CostTuple = collections.namedtuple('CostTuple', 'mothers, fathers')


class Parent:

    def __init__(self, name: str, salary: Decimal,
                 additional_monthly=D(0), additional_hourly=D(0), additional_annual=D(0),
                 weekly_custody=D('3.5'), annual_hours=CashFlow.H_ANNUAL):
        self.name, self.salary = name, salary

        self.additional_monthly, self.additional_hourly = additional_monthly, additional_hourly
        self.additional_annual, self.weekly_custody = additional_annual, weekly_custody
        self._annual_hours = annual_hours

    def reset_additional(self):
        self.additional_monthly = self.additional_hourly = self.additional_annual = D(0)

    @property
    def annual_hours(self):
        return self._annual_hours

    @annual_hours.setter
    def annual_hours(self, value):
        self.salary.H_ANNUAL = self._annual_hours = value

    @property
    def gross_monthly_income(self):
        adtl_monthly = self.additional_monthly
        adtl_hourly = self.additional_hourly * self.annual_hours / D(12)
        adtl_annual = self.additional_annual / D(12)
        adtl = adtl_annual + adtl_hourly + adtl_monthly
        return (self.salary.annual_rate / D(12)) + adtl

    @property
    def annual_custody(self):
        return self.weekly_custody * D(52)

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if not isinstance(value, Salary):
            value = Salary(value)
        self._salary = value

    def __repr__(self):
        args = self.name, str(self.salary.rate)
        return 'Parent({0})'.format(', '.join(args))


def values_to_decimal(d):
    for k, v in d.items():
        try:  # If it works, it's meant to work.
            d[k] = D(v)
            d[k] *= 1  # force rounding to context.prec
        except TypeError:
            print((k, d[k]))
        except (decimal.InvalidOperation, ValueError):
            pass
