from datetime import timedelta
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
filters = ['month','day','both','none']
months = ['January','February','March','April','May','June']
days = ['Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday','Friday']
filter = "Null"
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in CITY_DATA:
        try:
            city = input("Would you like to see data for Chicago, New York, or Washington?\n").lower()
        except Exception as e:
            print("An Error occured: ",e)
            print("Please check your input and try again!\n")
        else:
            if city not in CITY_DATA:
                print("Invalid Input {}! We expect that you enter one of the 3 provided cities\n".format(city.title()))
            else:
                print("Looks like you want to hear about {}! If this is not true, restart the program now!".format(city.title()))
    
    # get user filter for the data 
    global filter
    filter = "Null"
    while filter not in filters: 
        try:
            filter = input('\nWould you like to filter data by month, day, both, or not at all? Type "none" for no time filter\n').lower()
        except Exception as e:
            print("An Error occured: ",e)
            print("Please check your input and try again!\n")
        else:
            if filter not in filters:
                print('Invalid Filter {}! We expect that you enter one of the provided filters or "none" for no time filter\n'.format(filter))
            elif filter != 'none':
                print('We will make sure to filter by {}!\n'.format(filter))
    month = 'all'
    day = 'all'
    if filter != 'none':
        # get user input for month (all, january, february, ... , june)
        if filter == 'month' or filter == 'both':
            while month not in months:
                try:
                    month = input("\nWhich month? " + ', '.join(months) + "?\n").title()
                except:
                    print("An Error occured: ",e)
                    print("Please check your input and try again!\n")    
                else:
                    if month not in months:
                        print('Invalid Input {}! We expect that you enter one of the provided months\n'.format(month))

        # get user input for day of week (all, monday, tuesday, ... sunday)
        if filter == 'day' or filter == 'both':
            while day not in days:
                try:
                    day = input("\nWhich day? " + ', '.join(days) + "?\n").title()
                except:
                    print("An Error occured: ",e)
                    print("Please check your input and try again!\n")    
                else:
                    if day not in days:
                        print('Invalid Input {}! We expect that you enter one of the provided Days\n'.format(day))

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("\nJust one moment... Loading the data!\n")
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # Calculating statistics for the most common month from January to June
    popular_month = df['month'].mode()[0]
    popular_month_count = df[df['month']== popular_month].count()[0]

    # display the most common month
    print("What was the most common month for travelling?")
    print('Common Month:',popular_month, ' Count:', popular_month_count, ' Filter:',filter,'\n')    

    # Calculating statistics for the most common Day Of Week
    popular_day_of_week = df['day_of_week'].mode()[0]
    popular_day_of_week_count = df[df['day_of_week']== popular_day_of_week].count()[0]

    # display the most common day of week
    print("What was the most common day for travelling?")
    print('Day of the Week:', popular_day_of_week, ' Count:', popular_day_of_week_count, ' Filter:',filter,'\n')
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    
    # Calculating statistics for the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    popular_hour_count = df[df['hour']== popular_hour].count()[0]
    
    # display the most common start hour
    print("What was the most popular hour of the day to start a trip?")
    print('Most Frequent Hour:', popular_hour, ' Count:', popular_hour_count, ' Filter:',filter)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_count = df[df['Start Station']== popular_start_station].count()[0]
    print("What was the most commonly used start station?")
    print('Start Station:', popular_start_station, ' Count:', popular_start_station_count, ' Filter:',filter)
    
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_count = df[df['End Station']== popular_end_station].count()[0]
    print("\nWhat was the most commonly used end station?")
    print('End Station:', popular_end_station, ' Count:', popular_end_station_count, ' Filter:',filter)

    # display most frequent combination of start station and end station trip
    df['Combined Stations']= df['Start Station'] +','+ df['End Station']
    popular_combined_station = df['Combined Stations'].mode()[0]
    popular_combined_station_count = df[df['Combined Stations']== popular_combined_station].count()[0]
    popular_combined_station = str(popular_combined_station).split(',')    
    print("\nWhat was the most frequent combination of start station and end station trip?")
    print('Start Station:', popular_combined_station[0],' End Station:',popular_combined_station[1], ' Count:', popular_combined_station_count, ' Filter:',filter)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("What was the total time duration for travelling?")
    total_duration = df['Trip Duration'].sum()
    print("{} seconds".format(total_duration))
    total_duration = timedelta(seconds=float(total_duration))
    print("timedelta({})".format(total_duration))


    # display mean travel time
    print("\nWhat was the average time duration for travelling?")
    total_duration = df['Trip Duration'].mean()
    print("{} seconds".format(total_duration))
    total_duration = timedelta(seconds=float(total_duration))
    print("timedelta({})".format(total_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("What is the breakdown of users?")
    print(df['User Type'].value_counts())

    # Display counts of gender
    print("\nWhat is the breakdown of gender?")
    try:
        res = df['Gender'].value_counts()
    except:
        print("No gender data to be shown!")
        res = 'none'
    finally:
        print(res)

    # Display earliest, most recent, and most common year of birth
    print("\nWhat is the oldest, youngest, most common year of birth, respectively?")
    try:
        years = (df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0])
    except:
        print("No year of birth data to be shown!")
        years = 'none'
    finally:
        print(years)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip(city):
    """Displays 5 lines of raw data."""
    # set a counter for count how many data we showed
    count = 1
    # open the city file to explore
    with open(CITY_DATA[city]) as f:
        # get column names from the first line in the data
        columns = f.readline().strip().split(',')
        columns = np.array(columns)
        # iterate each row in the data and display its values
        for line in f:
            data = line.strip().split(',')
            data = np.array(data)
            # store row values in pandas Series
            raw_data = pd.Series(data = data, index = columns)
            raw_data.sort_index(inplace=True)
            # display the row values 
            for index in raw_data.index:
               print("'{}': '{}'".format(index,raw_data.loc[index]))
            print('-'*40)
            count +=1
            if count > 5 :
                # prompt the user if they want to see 5 lines of raw data
                start_trip = input("Would you like to view indvidual trip data? Type 'yes' or 'no'\n")
                if start_trip.lower() != 'yes':
                    break
                # reset the counter to start new individual_trip if user type 'yes'
                count = 1

def main():
    while True:
        # print(load_data('washington','all','all').shape[0]) # Solved and gives 300000
        # Hint: you just needed to use All NOT all, my code was filtered  correctly from first
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        individual_trip(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
