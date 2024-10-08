import argparse
import collections

from lunar_python import Solar
from datetime import datetime



# Sample invocation
"""
This script calculates the BaZi (Eight Characters) for given dates.
It supports two modes of operation:

1. Single date mode:
   [Input] 
   python bazi_caller.py <year> <month> <day> <time>

   Example:
   python bazi_caller.py 2023 5 15 12

   This will calculate the BaZi for:
   Date: May 15, 2023
   Time: 12:00 PM

2. Batch mode:
   [Input]
   python bazi_caller.py -f <input_file>

   Example:
   python bazi_caller.py -f dates.txt

   Where dates.txt contains dates in the format "YYYY MM DD HH", one per line.

[Output]
For each date processed, the script will output:
1. The input date in Gregorian calendar (yellow color)
2. The Gans (Heavenly Stems) for year, month, day, and time (cyan color)
3. The Zhis (Earthly Branches) for year, month, day, and time (cyan color)

Example output:
输入日期(公历）: 2023-05-15-12
癸 乙 丁 戊
卯 巳 酉 午

The script uses the lunar_python library to perform the necessary calculations.
"""

# Modify the argument parser
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-f', '--file', help='Input file with dates (one per line)')
parser.add_argument('year', nargs='?', help='Year (for single date mode)')
parser.add_argument('month', nargs='?', help='Month (for single date mode)')
parser.add_argument('day', nargs='?', help='Day (for single date mode)')
parser.add_argument('time', nargs='?', help='Time (for single date mode)')

# Parse command-line arguments
options = parser.parse_args()

# Define named tuples for Gans and Zhis
Gans = collections.namedtuple("Gans", "year month day time")
Zhis = collections.namedtuple("Zhis", "year month day time")

def process_date(year, month, day, time):
    # Format the input date
    input_date = datetime(int(year), int(month), int(day), int(time))
    formatted_date = f"{year}-{int(month):02d}-{int(day):02d}-{int(time):02d}"

    # Create a Solar date object from input
    solar = Solar.fromYmdHms(int(year), int(month), int(day), int(time), 0, 0)
    # Convert Solar date to Lunar date
    lunar = solar.getLunar()

    # Get the Eight Characters (BaZi) from the lunar date
    ba = lunar.getEightChar() 

    # Extract Gans and Zhis from the Eight Characters
    gans = Gans(year=ba.getYearGan(), month=ba.getMonthGan(), day=ba.getDayGan(), time=ba.getTimeGan())
    zhis = Zhis(year=ba.getYearZhi(), month=ba.getMonthZhi(), day=ba.getDayZhi(), time=ba.getTimeZhi())

    # Print the results
    print('\033[1;33;40m' + f"输入日期(公历）: {formatted_date}")
    print('\033[1;36;40m' + ' '.join(list(gans)))
    print('\033[1;36;40m' + ' '.join(list(zhis)))
    print("-"*120)

# Check if we're in file mode or single date mode
if options.file:
    with open(options.file, 'r') as file:
        for line in file:
            year, month, day, time = line.strip().split()
            process_date(year, month, day, time)
else:
    if not all([options.year, options.month, options.day, options.time]):
        parser.error("For single date mode, all date components (year, month, day, time) are required.")
    process_date(options.year, options.month, options.day, options.time)