import sys
import calendar

'''
The code was a quick implementation of
    the introduction given in the video:
    https://youtu.be/yoHtaDfYj3k
'''
def year_parser(y):
    a = y // 100
    b = y % 100

    return a, b

year = int(sys.argv[1])

a, b = year_parser(year)
r = a % 4
s = list(range(7))[(-5-2*r)%7]
t = (b + b//4) % 7

doomsday = (s + t) % 7
weekday = calendar.day_name[doomsday-1]

print('The doomsday in {0} is {1}.'.format(year, weekday))
