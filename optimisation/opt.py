import json
import random
import tqdm

def solve(filename):
    with open(filename) as f:
        json_data = json.load(f)
        data = {}
        for i, act in enumerate(json_data):
            data[i] = act
        money = 0
        fun_score = 0
        all_ratios = []
        all_ratio_w_time = []
        all_fun = []
        all_money = []
        chosen_act = []
        for activity in data:
            ratio = data[activity]['money']/ (data[activity]['fun'] if not abs(data[activity]['fun'] < 0.00005) else -1)
            if data[activity]['money']< 0 and data[activity]['fun']< 0:
                ratio *= -10
            all_ratios.append(ratio)
            all_ratio_w_time.append(ratio/data[activity]['hour_duration'])
            all_fun.append(data[activity]['fun'])
            all_money.append(data[activity]['money'])
        worst_cost = all_money.index(min(all_money))
        #print('worst cost', worst_cost)
        #print(all_ratios)
        #print(all_fun)
        for _ in tqdm.trange(len(all_ratios)):
            best_ratio_idx = all_ratios.index(max(all_ratios))
            best_money_idx = all_money.index(max(all_money))
            best_fun_idx = all_fun.index(max(all_fun))
            # test de condition money:   abs(10*money/worst_cost)
            chosen_idx = best_ratio_idx if random.random() > 0.2 and best_ratio_idx > 0 else best_money_idx if random.random() > abs(money/worst_cost) else best_fun_idx
            #print('chosen idx', chosen_idx)
            #print(data[chosen_idx])
            if best_ratio_idx not in chosen_act:
                if test_conflicts(data, chosen_act, chosen_idx):
                    if  money + all_money[chosen_idx]> 0:
                        if all_fun[chosen_idx] < 0:
                            continue
                        money += all_money[chosen_idx]
                        fun_score += all_fun[chosen_idx]
                        chosen_act.append(chosen_idx)
                        all_ratios.remove(all_ratios[chosen_idx])
                        all_fun.remove(all_fun[chosen_idx])
                        all_money.remove(all_money[chosen_idx])
        
        print('chosen!',chosen_act)
        print('final_money', money)
        print('final_fun:', fun_score)
        return chosen_act



def test_conflicts(data, chosenacts, current_act):
    day = data[current_act]['week_day']
    start = data[current_act]['start_hour']
    end = start + data[current_act]['hour_duration']
    for acti in chosenacts:
        if data[acti]['week_day'] != day:
            continue
        acti_start = data[acti]['start_hour']
        acti_end = acti_start + data[acti]['hour_duration']
        if start > acti_end or end < acti_start:
            continue
        else:
            return False
    return True

print('small version')
small_solved = solve('input/small.json')

print('medium version')
small_solved = solve('input/medium.json')

print('large version')
small_solved = solve('input/large.json')

print('Xlarge version')
small_solved = solve('input/xlarge.json')






import json
from enum import Enum
from typing import List

class WeekDay(Enum):
    Mon = "Mon"
    Tue = "Tue"
    Wed = "Wed"
    Thu = "Thu"
    Fri = "Fri"
    Sat = "Sat"
    Sun = "Sun"

class Activity:
    def __init__(self, week_day: WeekDay, start_hour: int, hour_duration: int, money: float, fun: float):
        self.week_day = week_day
        self.start_hour = start_hour
        self.hour_duration = hour_duration
        self.money = money
        self.fun = fun

    @staticmethod
    def deserialize(data: dict):
        return Activity(
            WeekDay(data["week_day"]),
            data["start_hour"],
            data["hour_duration"],
            data["money"],
            data["fun"]
        )

class Possibilities:
    def __init__(self, activities: List[Activity]):
        self.activities = activities

    @staticmethod
    def deserialize(data: dict):
        activities = [Activity.deserialize(item) for item in data["activities"]]
        return Possibilities(activities)
    
