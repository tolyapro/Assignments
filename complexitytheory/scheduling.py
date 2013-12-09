"""

get_schedule_fast, _bruteforce, _dynamic(num_machines, jobs_weights)
return dict[machine_index] = [(job_index, job_weight), ...]

"""


def get_schedule_fast(num_machines, jobs_weights):
    results = {}
    weights = list(jobs_weights)
    l = [0] * num_machines

    while max(weights) > 0:
        argmax_weights = max(enumerate(weights), key= lambda x : x[1])[0]
        argmin_loads = min(enumerate(l), key= lambda x : x[1])[0]

        if argmin_loads in results.keys():
            results[argmin_loads].append((argmax_weights, weights[argmax_weights]))
        else:
            results[argmin_loads] = [(argmax_weights, weights[argmax_weights])]

        l[argmin_loads] += weights[argmax_weights]
        weights[argmax_weights] = -1

    return results 


def get_schedule_bruteforce(num_machines, jobs_weights):
    num_jobs = len(jobs_weights)
    schedules = []
    current_schedule = [0] * num_jobs

    def generate(pos=0): #recursive generation of all possible variants
        if pos == num_jobs:
            schedules.append(list(current_schedule))
        else:
            for i in range(num_machines):
                current_schedule[pos] = i
                generate(pos + 1)
    generate()

    all_schedules = []
    for schedule in schedules:
        tmp_schedulep_d = {}
        for i in range(len(schedule)):
            x = schedule[i]
            if x in tmp_schedulep_d.keys():
                tmp_schedulep_d[x].append((i, jobs_weights[i]))
            else:
                tmp_schedulep_d[x] = [(i, jobs_weights[i])]
        all_schedules.append(tmp_schedulep_d)

    return min(all_schedules, key=get_schedule_time)            

def get_schedule_dynamic(num_machines, jobs_weights):
    bound = get_schedule_time(get_schedule_fast(num_machines, jobs_weights))

    l = 0 # iterations
    first_step = []
    for i in range(num_machines):
        t = {}
        t[i] = [(l, jobs_weights[l])]
        first_step.append(t)

    new_step = list(first_step)

    while True:
        tmp_schedule = []

        for x in new_step:
            if get_schedule_time(x) <= bound:
                tmp_schedule.append(x)

        new_step = list(tmp_schedule)

        if l == len(jobs_weights) - 1:
            break

        l += 1

        tmp_schedule = []
        for x in range(len(new_step)):
            for i in range(0, num_machines):
                current = {}
                for key in new_step[x].keys():
                    current[key] = list(new_step[x][key])
                   
                if i in current.keys():
                    current[i].append((l, jobs_weights[l]))
                else:
                    current[i] = [(l, jobs_weights[l])]
                    
                current[i] = list(set(current[i]))
                tmp_schedule.append(current)

        new_step = list(tmp_schedule)

    return min(new_step, key=get_schedule_time)


def get_schedule_time(schedule):
    return max([sum(x for _,x in machine) for machine in schedule.values()])



