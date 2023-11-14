import time

import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks the user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input(
            'To start, please enter a city name you wish to explore.\nEnter a city (Chicago, New york city, '
            'Washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('Invalid city. Please choose from the provided options.')

    while True:
        month = input(f'You have selected to explore data for {city.title()}.\nNow, enter a month to filter the data '
                      f'by. If you would like to view for all months available, enter All.\n\nEnter a month (all, '
                      f'january, february, ... , june): ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('Invalid month. Please choose from the provided options.')

    while True:
        day = input(
            f'You have selected to explore data for {city.title()}, with a month filter of {month.title()}.\nNow, '
            f'enter a day to filter the data '
            f'by. If you would like to view for all days of the week, enter All.\n\nEnter a day of the week '
            f'(all, monday, tuesday, ... sunday): ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day of the week. Please choose from the provided options.')

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # Convert the 'Start Time' column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week from 'Start Time' to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # Filter by day of the week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July']
    common_month = df['month'].mode()[0]
    print(f"The most common month: {common_month} ({months[common_month - 1]})")

    # Display the most common day of the week
    common_day = df['day_of_week'].mode()[0]
    print(f"The most common day of the week: {common_day}")

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    common_hour_12hr = pd.to_datetime(str(common_hour), format='%H').strftime('%I %p')
    print(f"The most common start hour: {common_hour} ({common_hour_12hr})")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trips."""
    print('\nCalculating The Most Popular Stations and Trips...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station: {common_start_station}")

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"The most commonly used end station: {common_end_station}")

    # Display most frequent combination of start station and end station trip
    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Trip'].mode()[0]
    print(f"The most frequent combination of start station and end station trip: {common_trip}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time_seconds = df['Trip Duration'].sum()
    total_minutes, total_seconds = divmod(total_travel_time_seconds, 60)
    total_hours, total_minutes = divmod(total_minutes, 60)

    mean_travel_time_seconds = df['Trip Duration'].mean()
    mean_minutes, mean_seconds = divmod(mean_travel_time_seconds, 60)
    mean_hours, mean_minutes = divmod(mean_minutes, 60)

    print(
        f"Total travel time: {int(total_hours)} hours, {int(total_minutes)} minutes, and {int(total_seconds)} seconds")
    print(f"Mean travel time: {int(mean_hours)} hours, {int(mean_minutes)} minutes, and {int(mean_seconds)} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types:")
    print(user_types)

    # Display counts of gender (if available in the data)
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of gender:")
        print(gender_counts)
    else:
        print("\nGender data not available for this city.")

    # Display earliest, most recent, and most common year of birth (if available in the data)
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"\nEarliest birth year: {earliest_birth_year}")
        print(f"Most recent birth year: {most_recent_birth_year}")
        print(f"Most common birth year: {common_birth_year}")
    else:
        print("\nBirth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    start_index = 0
    chunk_size = 5

    while True:
        display_option = input('Do you want to see 5 rows of data? Enter yes or no: ').lower()

        if display_option == 'yes':
            if start_index >= len(df):
                print("No more data to display.")
                break

            end_index = start_index + chunk_size
            chunk = df.iloc[start_index:end_index]

            # Set display options to show all columns without truncation
            pd.set_option('display.max_columns', None)

            # Displaying specified columns with formatted values
            print(chunk[['Start Time', 'End Time', 'Trip Duration', 'Start Station',
                         'End Station', 'User Type']])

            start_index = end_index
        elif display_option == 'no':
            # Reset display options
            pd.reset_option('display.max_columns')
            break
        else:
            print('Invalid input. Please enter yes or no.')


def main():
    print(__name__)
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
