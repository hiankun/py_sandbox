import math

def avg(nums):
    #https://stackoverflow.com/a/4973701
    total = 0.
    for i, n in enumerate(nums, 1):
        total += n
    return total/i

#https://youtu.be/tmeKsb2Fras
with open('nums.txt') as f:
    nums = (x.partition('#')[0].strip() for x in f)
    nums = (float(x) for x in nums if x)
    nums = (x for x in nums if math.isfinite(x))
    nums = (max(0., x) for x in nums)
    print(f'avg: {avg(nums)}')
