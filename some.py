import datetime
m2 = '01:59 PM'
in_time = datetime.datetime.strptime(m2, "%I:%M %p")
out_time = datetime.datetime.strftime(in_time, "%H:%M")

print(out_time)