import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs.
    city = ""
    while city not in ['chicago', 'new york', 'washington']:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()

    month = ""
    day = ""
    is_filter = input('Would you like to filter the data by month, day, or not at all?\n').lower()
    if is_filter == 'month':
        # Get user input for month (all, january, february, ... , june).
        while month not in ['January', 'February', 'March', 'April', 'May', 'June']:
            month = input('Which month - January, February, March, April, May, or June?\n').capitalize()
    elif is_filter == 'day':
        # Get user input for day of week (all, monday, tuesday, ... sunday).
        while day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            day = input('Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').capitalize()

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
    df = pd.read_csv(CITY_DATA[city]) # Read in the csv file.

    df['Start Time'] = pd.to_datetime(df['Start Time']) # Convert date to datetime.

    filtered_df = df # When no filter is applied.

    if month != "":
        filtered_df = df[(df['Start Time'].dt.month_name() == month)] # Filter by month.
    
    if day != "":
        filtered_df = df[(df['Start Time'].dt.day_name() == day)] # Filter by day.

    return df, filtered_df

def display_data(df):
    """Prompt the user if they want to see 5 lines of raw data,
    Display that data if the answer is 'yes',
    Continue iterating these prompts and displaying the next 5 lines of raw data at each iteration,
    Stop the program when the user says 'no' or there is no more raw data to display."""
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?")
    start_loc = 0
    while view_data == "yes":
        try:
            print(df.iloc[start_loc:start_loc+4])
            start_loc += 5
            view_data = input("Do you wish to continue?: ").lower()
        except:
            print("You've reached the end of the table")




def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month.
    df['month'] = df['Start Time'].dt.month_name()
    common_month = df['month'].mode()[0]
    print(f'The most common month is: {common_month}')

    # Display the most common day of week.
    df['day'] = df['Start Time'].dt.day_name()
    common_day = df['day'].mode()[0]
    print(f'The most common day is: {common_day}')

    # Display the most common start hour.
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f'The most common start hour is: {common_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(filtered_df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station.
    common_start = filtered_df['Start Station'].mode()[0]
    print(f'The most common start station is: {common_start}')


    # Display most commonly used end station.
    common_end = filtered_df['End Station'].mode()[0]
    print(f'The most common end station is: {common_end}')


    # Display most frequent combination of start station and end station trip.
    filtered_df = filtered_df.copy()
    filtered_df['stations'] = filtered_df['Start Station'] + ' TO ' + filtered_df['End Station']
    common_station = filtered_df['stations'].mode()[0]
    print(f'The most common combination of start station and end station trip is: {common_station}')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(filtered_df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    filtered_df = filtered_df.copy()

    # Display total travel time.
    filtered_df['travel time'] = pd.to_datetime(filtered_df['End Time']) - pd.to_datetime(filtered_df['Start Time'])
    total_time = filtered_df['travel time'].sum()
    print(f'Total travel time is {total_time}')

    # Display mean travel time.
    mean_time = filtered_df['travel time'].mean()
    print(f'Mean travel time is {mean_time}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(filtered_df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    filtered_df = filtered_df.copy()

    # Display counts of user types.
    user_types = filtered_df['User Type'].value_counts()
    print(user_types)


    # Display counts of gender.
    try:
        gender_types = filtered_df['Gender'].value_counts()
        print(gender_types)
    except:
        print('No gender information')

    # Display earliest, most recent, and most common year of birth.
    try:
        earliest_dob = filtered_df['Birth Year'].min()
        recent_dob = filtered_df['Birth Year'].max()
        common_dob = filtered_df['Birth Year'].mode()[0]
        print(f'Earliest year of birth is {earliest_dob}')
        print(f'Most recent year of birth is {recent_dob}')
        print(f'Most common year of birth is {common_dob}')
    except:
        print('No birth year information')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df, filtered_df = load_data(city, month, day)

        time_stats(df)
        display_data(df)
        station_stats(filtered_df)
        trip_duration_stats(filtered_df)
        user_stats(filtered_df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
