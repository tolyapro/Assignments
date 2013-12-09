"""

generate_random_test() - creates test with random amount of machines and jobs and 
returns (fast_time, bruteforce_time, fast_weight/bruteforce_weight)

stat(N) - generates N random tests and prints average time ratio and average weight ratio

"""


import time
import random
from scheduling import *


def test(num_machines, jobs_weights):
    schedule = get_schedule_fast(num_machines, jobs_weights)
    return (schedule, get_schedule_time(schedule))


def test_dynamic(num_machines, jobs_weights):
    schedule = get_schedule_dynamic(num_machines, jobs_weights)
    return (schedule, get_schedule_time(schedule))

    
def test_time(num_machines, jobs_weights):
    start_fast = time.time()
    schedule_fast = get_schedule_fast(num_machines, jobs_weights)
    end_fast = time.time()
    schedule_bruteforce = get_schedule_bruteforce(num_machines, jobs_weights)
    end_bruteforce = time.time()
    return (end_fast - start_fast, end_bruteforce - end_fast, float(get_schedule_time(schedule_fast))/get_schedule_time(schedule_bruteforce))


def generate_random_test():
    num_machines = random.randint(2, 4)
    num_jobs = random.randint(num_machines * 2, 10)
    jobs_weights = [0] * num_jobs

    for i in range(num_jobs):
        jobs_weights[i] = random.randint(5, 20)

    #print jobs_weights
    #print num_machines

    return test_time(num_machines, jobs_weights)


def stat(N = 25):
    fast_time = .0
    bruteforce_time = .0
    ratio = .0
    for i in range(N):
        #print i
        result = generate_random_test()
        fast_time += result[0]
        bruteforce_time += result[1]
        ratio += result[2]

    print (bruteforce_time / N) / (fast_time / N) , ratio / N

