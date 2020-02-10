# import csv reader/writer
import pandas as pd

# import for time measuring
import time as ti

# import for statistics
import statistics

# define value of first year of data input
first_year = 2017
# define value of the minimum viable value (15 minutes)
min_value = 0.25
# define value of the amount of years
amt_of_year = 3


class Table:
    def __init__(self, name):
        self.name = name
        self.weekdays = []

    def add(self, e):
        self.weekdays.append(e)

    def find_pos(self, obj):

        index = 0

        # iterate over weekdays array
        for x in self.weekdays:

            # check if weekday in table matches to object weekday
            if x.weekday_num == obj.weekday:
                # set next day (needed to be able to add values over midnight)
                next_day = self.weekdays[(index % 6)+1]
                # if match is found, find correct time in weekday_object
                x.find_pos(obj, next_day)

            index += 1

    def calculate_statistics(self):

        for x in self.weekdays:
            for y in x.times:
                y.get_mode()
                y.get_median()
                y.get_mean()
                y.get_highest_value()
                y.get_lowest_value()
                y.get_standard_deviation()


class Weekday_Object:
    def __init__(self, weekday_num):
        self.weekday_num = weekday_num
        self.times = []

    def add(self, e):
        self.times.append(e)

    def find_pos(self, obj, next_day):

        # init counter at 1 to exclude the found time_objects
        index = 1

        # iterate over times array
        for x in self.times:

            # localize object duration
            dur = obj.duration

            # localize amt
            amt = int(dur / min_value)

            # localize position
            pos = obj.year % first_year

            # check if time_of_day matches to object time_of_day
            if x.time_of_day == obj.time_of_day:
                # if match is found, add value to certain position in time_object
                x.add_value_to_position(pos, 1)

                # add values to the rest of the time_objects from found time_object to the rest within duration
                self.add_value_by_duration(
                    index, (index+amt), pos, 1, next_day)

            # increment counter
            index += 1

    def add_value_by_duration(self, start, end, pos, value, next_day):

        index = start

        # add value to time object
        for x in range(start, end):
            if len(self.times) <= index:
                # recursive call to same function on the next_day object (range is end-index to exclude the duration that has been added to this day_object)
                next_day.add_value_by_duration(
                    0, (end-index), pos, value, next_day)
                break
            self.times[x].add_value_to_position(pos, value)
            index += 1


class Time_Object:
    def __init__(self, time_of_day):
        self.time_of_day = time_of_day

        # initalize list with zeros as value so add_value_to_position function works well
        self.numbers = [0]*amt_of_year

        # initalize list with zeros as values for space of statistics
        self.statistics = [0]*6

        # mode
        # median
        # mean
        # highest_value
        # lowest_value
        # standard_deviation

    def add_value_to_position(self, pos, value):

        # add value to position in numbers
        self.numbers[pos] += value

    def get_mode(self):

        # calculatem mode of values in numbers
        self.statistics[0] = statistics.mode(self.numbers)

    def get_median(self):

        # calculate median of values in numbers
        self.statistics[1] = statistics.median(self.numbers)

    def get_mean(self):

        # calculate mean of values in numbers
        self.statistics[2] = statistics.mean(self.numbers)

    def get_highest_value(self):

        # get highest value in numbers
        self.statistics[3] = max(self.numbers)

    def get_lowest_value(self):

        # get lowest value in numbers
        self.statistics[4] = min(self.numbers)

    def get_standard_deviation(self):

        # get standard deviation in numbers
        self.statistics[5] = statistics.stdev(self.numbers)


class Read_Object:
    def __init__(self, year, weekday, time_of_day, duration):
        self.year = year
        self.weekday = weekday
        self.time_of_day = time_of_day
        self.duration = duration

    # toString function
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


def init_table(ta):

    # start at day 3 (wednesday)
    day = 2

    # iterate over a week
    for x in range(0, 7):

        # use modulus to turn around to monday
        day = day % 7

        # get sunday
        if day == 0:
            day = 7

        # create weekday objects ranging with weekday_num 1-7 (mon-sun)
        we_obj = Weekday_Object(day)

        # increment day
        day += 1

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


def read_csv(file):

    # read csv file with pandas
    df = pd.read_csv(r'%s' % file)

    return df


def create_read_objects(read):

    arr = []

    for x in range(0, len(read.index)):
        # Create read_object
        ro = Read_Object(int(read.iloc[x][0]), int(
            read.iloc[x][1]), read.iloc[x][2], read.iloc[x][3])
        arr.append(ro)

    return arr


def feed_table(table, arr):

    for x in arr:
        table.find_pos(x)


def write_to_csv(table):

    # localize arrays
    week = []
    time = []
    mode = []
    median = []
    mean = []
    high = []
    low = []
    std = []

    # loop over the weekdays
    for x in table.weekdays:

        # extend current weekday to array
        week.extend([x.weekday_num] * (int(24 / 0.25)))

        # loop over times of the weekday
        for y in x.times:

            # save the times
            time.append(y.time_of_day)

            # save the mode values
            mode.append(y.statistics[0])

            # save the median values
            median.append(y.statistics[1])

            # save the mean values
            mean.append(y.statistics[2])

            # save the highest values
            high.append(y.statistics[3])

            # save the lowest values
            low.append(y.statistics[4])

            # save the lowest values
            std.append(y.statistics[5])

    # dictionary of lists
    dict = {'Weekday': week, 'Time': time, 'Mode': mode, 'Median': median, 'Mean': mean, 'High': high, 'Low': low, 'Std': std}

    # add dictinoary to dataFrame
    df = pd.DataFrame(dict)

    # saving the dataFrame (excluding indicies)
    df.to_csv('save.csv', header=True, index=False)


# START OF MAIN

start_time = ti.time()

# Create a table
ta1 = Table("Table")

# Init table with values
init_table(ta1)

# read csv file
read = read_csv('2017.csv')

# call create read objects with current csv as input
arr = create_read_objects(read)

# add all read_objects to table
feed_table(ta1, arr)

# read csv file
read = read_csv('2018.csv')

# call create read objects with current csv as input
arr = create_read_objects(read)

# add all read_objects to table
feed_table(ta1, arr)

# read csv file
read = read_csv('2019.csv')

# call create read objects with current csv as input
arr = create_read_objects(read)

# add all read_objects to table
feed_table(ta1, arr)

# calculate statistics on table values
ta1.calculate_statistics()

for x in ta1.weekdays:
    print('Weekday: %d' % x.weekday_num)
    for y in x.times:
        print('\tTime %.2f\t Value %s\t Stats %s' %
              (y.time_of_day, y.numbers, y.statistics))

print("--- Execution time of program %s seconds ---" % (ti.time()-start_time))

# write table to csv
write_to_csv(ta1)
