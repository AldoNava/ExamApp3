import json
# reading the data from the file
with open('questions.txt') as f:
    #data = f.read()
    questionList = json.load(f)


for x in questionList:
    for soc in x['discussion']:
        print(soc)

print(len(questionList))
from win32api import GetMonitorInfo, MonitorFromPoint

monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
work_area = monitor_info.get("Work")
print("The work area size is {}x{}.".format(work_area[2], work_area[3]))