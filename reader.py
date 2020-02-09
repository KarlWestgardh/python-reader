# define value of first year of data input
first_year = 2017
# define value of the minimum viable value (15 minutes)
min_value = 0.25


class Table:
    def __init__(self, name):
        self.name = name
        self.weekdays = []

    def add(self, e):
        self.weekdays.append(e)

    def find_pos(self, obj):
        # iterate over weekdays array
        for x in range(0, len(self.weekdays)):

            # check if weekday in table matches to object weekday
            if self.weekdays[x].weekday_num == obj.weekday:
                # if match is found, find correct time in weekday_object
                self.weekdays[x].find_pos(obj)
            else:
                # invalidate no matches found
                print("is not ok")


class Weekday_Object:
    def __init__(self, weekday_num):
        self.weekday_num = weekday_num
        self.times = []

    def add(self, e):
        self.times.append(e)

    def find_pos(self, obj):
        # iterate over times array
        for x in range(0, len(self.times)):

            # localize duration of object
            dur = obj.duration

            # localize position
            pos = obj.year % first_year

            # check if time_of_day matches to object time_of_day
            if self.times[x].time_of_day == obj.time_of_day:
                # if match is found, add value to certain position in time_object
                self.times[x].numbers.add_value_to_position(
                    pos, 1)

                # also add value to next positions until duration is exhausted
                for y in range(x, (dur / min_value)):
                    self.times[x].numbers.add_value_to_position(
                        pos, 1)
                    x += 1
            else:
                # invalidate no matches found
                print("is not ok")


class Time_Object:
    def __init__(self, time_of_day):
        self.time_of_day = time_of_day
        self.numbers = []

    def add_value_to_position(self, pos, value):
        self.numbers[pos] += value


class Read_Object:
    def __init__(self, year, weekday, time_of_day, duration):
        self.year = year
        self.weekday = weekday
        self.time_of_day = time_of_day
        self.duration = duration


def init_table(ta):
    # iterate over a week
    for x in range(0, 7):
        # create weekday objects ranging with weekday_num 1-7 (mon-sun)
        we_obj = Weekday_Object(x+1)

        # initalize time array in weekday_object
        init_weekday_object(we_obj)

        # if successful, add weekday object to list of weekdays in table
        ta.add(we_obj)


def init_weekday_object(we_obj):
    # define decimal value of 24-hour
    dec = 0.00

    # iterate over a 24-hour day with minimum time value (top)
    for x in range(0, (int(24 / min_value))):

        # create time object ranging with time_of_day value 0-23,75 (hour in decimal)
        ti_obj = Time_Object(dec)

        # add time_object to weekday_object
        we_obj.add(ti_obj)

        # increment decimal value with min_value
        dec += min_value

# Main running


# Create a table
ta1 = Table("Table")

# Init table with values
init_table(ta1)

for x in ta1.weekdays:
    print('Weekday %d' %x.weekday_num)
    for y in x.times:
        print('\tTime %.2f' %y.time_of_day)
