# Copyright 2025 Matej Mužila

import holidays
import locale
import datetime
import calendar
import itertools
from tabulate import tabulate
from pyfiglet import Figlet
import argparse

def isHoliday(*vargs):
    date = datetime.datetime(*vargs)
    if date.strftime("%Y-%l-%d") in holidays.CZ():
        return True

    if date.weekday() in [5,6]:
        return True
    return False

def get_months(year, font):
    for i in range(1,13):
        m = datetime.datetime(year, i, 1)
        month_name = m.strftime("%B").upper()

        l = [("", Figlet(font=font, justify="left", width=70).renderText(month_name).replace(" ", "@"))]

        out = filter(lambda x: x != 0, calendar.Calendar().itermonthdays(year, i))
        out = map(lambda x:  f"\u25a0 {x}" if isHoliday(year,i,x) else f"@ {x}", out)
        out = map(lambda x: (x, "@"*69), out)
        out = itertools.chain(l,out)
        yield out

def app():
    parser = argparse.ArgumentParser(
                    description='Print calendar for given year')
    parser.add_argument("year", type=int, nargs=1)
    parser.add_argument("--font", type=str, default="crazy")
    parser.add_argument("--locale", type=str, default="sk_SK")
    parser.add_argument("--font-month", type=str, default="mono9")
    args = parser.parse_args()

    year = args.year[0]
    locale.setlocale(locale.LC_TIME, args.locale)

    print("\n\n\n")
    print(Figlet(font=args.font, justify="center", width=80).renderText(str(year)))

    print(Figlet(font="train", justify="center", width=80).renderText(f" .._._._"))

    m_tabs = map(lambda x: tabulate(x, tablefmt="simple_grid", stralign="center"), get_months(year, font=args.font_month))
    m_tabs = map(lambda x: x.replace("@"," "), m_tabs)
    for i in m_tabs:
        print(i)

if __name__ == "__main__":
    app()
