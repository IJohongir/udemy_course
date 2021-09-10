from datetime import datetime

date_time_str = '18/09/19'
one =' 00:00:00'
date_time_str = date_time_str+one
date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')


print ("The type of the date is now",  type(date_time_obj))
print ("The date is", date_time_obj)