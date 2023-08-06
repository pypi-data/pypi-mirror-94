import pyodbc
import os
import pandas as pd
import re
from datetime import datetime
from datetime import timedelta


def get_occupancy(start, server, database, user, password, end=None):

    date_check = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')

    if date_check.year >= datetime.now().year - 1:
        database = database
    else:
        database = database + '_' + str(date_check.year)

    # QUERY DATABASE
    amcnxn = pyodbc.connect(r'driver={SQL Server};'
                            r'server='+ server + ';'
                            r'database=' + database + ';'
                            r'UID=' + user + ';'
                            r'PWD=' + password)

    if end is None:
        lot_occupancy = pd.read_sql(r"SELECT [Counts].SiteName as [Lot Name]"
                                    r",[Counts].Date as [Date]"
                                    r",[Counts].Description as [Description]"
                                    r",[Counts].Occupied as [Occupied Spaces]"
                                    r",[Counts].Available as [Available Spaces]"
                                    r",[Counts].Total as [Total Spaces]"
                                    r",'Amano-McGann' as [Data Source]"
                                    r"FROM " + database + ".dbo.COUNT_DIFFERENTIALS as [Counts]"
                                    r"WHERE [Counts].Date >= '" + start + "'"
                                    r"ORDER BY [Counts].Date DESC",
                                    amcnxn)
    else:
        lot_occupancy = pd.read_sql(r"SELECT [Counts].SiteName as [Lot Name]"
                                    r",[Counts].Date as [Date]"
                                    r",[Counts].Description as [Description]"
                                    r",[Counts].Occupied as [Occupied Spaces]"
                                    r",[Counts].Available as [Available Spaces]"
                                    r",[Counts].Total as [Total Spaces]"
                                    r",'Amano-McGann' as [Data Source]"
                                    r"FROM " + database + ".dbo.COUNT_DIFFERENTIALS as [Counts]"
                                    r"WHERE [Counts].Date >= '" + start + "' AND [Counts].Date <= '" + end + "'"
                                    r"ORDER BY [Counts].Date DESC",
                                    amcnxn)

    # Segment Reserved Areas in Ramps
    lot_occupancy.loc[(lot_occupancy['Description'].str.contains('reserved', flags=re.IGNORECASE, regex=True)) |
                      (lot_occupancy['Description'].str.contains('month area', flags=re.IGNORECASE, regex=True)),
                      'Lot Name'] = lot_occupancy['Lot Name'] + ' (Reserved)'

    # Add Column to Note Transient vs. Contract vs. Full Garage
    lot_occupancy['Parker Type'] = lot_occupancy['Description'].str.lower()
    lot_occupancy.loc[lot_occupancy['Parker Type'].str.contains('monthly'), 'Parker Type'] = 'Contract'
    lot_occupancy.loc[lot_occupancy['Parker Type'].str.contains('transient'), 'Parker Type'] = 'Transient'
    lot_occupancy.loc[(lot_occupancy['Parker Type'] != 'Contract') & (lot_occupancy['Parker Type'] != 'Transient'),
                      'Parker Type'] = 'Total'

    # Get Available Counts
    available = lot_occupancy.loc[lot_occupancy['Parker Type'] == 'Total']
    available['Parker Type'] = 'Available'
    available = available[['Date', 'Lot Name', 'Parker Type', 'Data Source', 'Available Spaces']]

    available.rename(columns={'Available Spaces': 'Count'}, inplace=True)

    # Melt Original Dataframe to Match Available Counts Dataframe
    lot_occupancy = pd.melt(lot_occupancy,
                            id_vars=['Date', 'Lot Name', 'Parker Type', 'Data Source'],
                            value_vars=['Occupied Spaces'])
    lot_occupancy = lot_occupancy.drop(columns='variable')

    lot_occupancy.rename(columns={'value': 'Count'}, inplace=True)

    # Concatenate Occupancy and Available Count Dataframes
    lot_occupancy = pd.concat([lot_occupancy, available], ignore_index=True, sort=True)

    # Format Date
    lot_occupancy['Date'] = pd.to_datetime(lot_occupancy['Date']).dt.strftime('%Y-%m-%d %H:00:00')
    lot_occupancy['Date'] = pd.to_datetime(lot_occupancy['Date'])

    # Add Comparison Date
    # This Year
    this_start = datetime(datetime.now().year, 1, 1, 0, 0, 0)
    this_end = datetime(datetime.now().year, 12, 31, 23, 59, 59)

    # Last Year
    if datetime.now().year - 1 % 4 == 0:
        last_start = this_start - timedelta(days=363)
        last_end = this_end - timedelta(days=363)
    else:
        last_start = this_start - timedelta(days=364)
        last_end = this_end - timedelta(days=364)

    # YEAR FILTERS AND COMPARISON DATES
    # Initially Set Year Filter Column to Number of Years Ago
    lot_occupancy['Year'] = this_start.year - lot_occupancy['Date'].dt.year

    # Determine Number of Unique Years in Dataset
    years_ago = lot_occupancy['Year'].unique()

    # Set Comparison Dates
    lot_occupancy['Comparison Date'] = lot_occupancy['Date']

    for number in years_ago:
        if number > 0:
            # Check is Current Year is Leap Year and Set Dates Accordingly
            if datetime.now().year - 1 % 4 == 0:
                lot_occupancy.loc[lot_occupancy['Year'] == number, 'Comparison Date'] = lot_occupancy[
                                                                                            'Date'] + timedelta(
                    days=364 - int(number))
            else:
                lot_occupancy.loc[lot_occupancy['Year'] == number, 'Comparison Date'] = lot_occupancy[
                                                                                            'Date'] + timedelta(
                    days=365 - int(number))

    lot_occupancy['Comparison Date'] = pd.to_datetime(lot_occupancy['Comparison Date'], '%Y-%m-%d %H:%M:%S')

    # Convert Year Column to text value of given year
    lot_occupancy['Year'] = lot_occupancy['Date'].dt.strftime('%Y')

    # Add Parking Ramp/Lot Coordinates
    lot_occupancy['Coordinates'] = None

    # Reorder Columns for Import
    # Reorder Columns for Import
    lot_occupancy = lot_occupancy[['Date',
                                   'Comparison Date',
                                   'Count',
                                   'Lot Name',
                                   'Parker Type',
                                   'Year',
                                   'Data Source']]

    return lot_occupancy


def get_entries(start, user, password):

    # SET RELATIVE DATES
    # This Year
    this_start = datetime(datetime.now().year, 1, 1, 0, 0, 0)
    this_end = datetime(datetime.now().year, 12, 31, 23, 59, 59)

    # Last Year
    if datetime.now().year - 1 % 4 == 0:
        last_start = this_start - timedelta(days=363)
        last_end = this_end - timedelta(days=363)
    else:
        last_start = this_start - timedelta(days=364)
        last_end = this_end - timedelta(days=364)

    # DATABASE CONNECTION
    amcnxn = pyodbc.connect(r'driver={SQL Server};'
                            r'server=MGRVDB1;'
                            r'database=McGANN;'
                            r'UID=' + os.environ['AMANO_USERNAME'] +
                            r';PWD=' + os.environ['AMANO_PASSWORD'])

    # ENTRIES QUERIES
    amano_contract = pd.read_sql("SELECT 'AM-' + CAST([Contracts].ID AS VARCHAR(16)) AS [Entry ID], [Contracts].CARD_NUM as [Card or Ticket Number], [Lots].LotDesc as [Lot Name], 'Contractor' as [Parker Type], [Access].GROUP_NAME as [Access Group], [Readers].DESCRIPTION as [Lane], [Contracts].ACTIVITY_TIME as [Activity Time], 'Amano McGann' as [Data Source], 'Total' as [Total] FROM McGANN.dbo.CONTRACT_ACTIVITY as [Contracts] LEFT OUTER JOIN McGANN.dbo.SiteLots as [Lots] on ([Contracts].LOT_NUMBER = [Lots].Lot_Number) LEFT OUTER JOIN McGANN.dbo.READERS as [Readers] on ([Contracts].READER = [Readers].READER_NUM) LEFT OUTER JOIN McGANN.dbo.ACCESS_GROUP_NAMES as [Access] on ([Contracts].ACCESS_GROUP = [Access].GROUP_NUM) WHERE [Contracts].ACTIVITY_TIME >= '" + start + "' AND [Contracts].ACTIVITY_TIME <= '2029-01-01 00:00:00' AND [Contracts].DIRECTION = 1 ORDER BY [Contracts].ACTIVITY_TIME DESC", amcnxn)
    amano_entries  = pd.read_sql("SELECT 'AM-' + CAST([Entries].ID AS VARCHAR(16)) as [Entry ID], [Entries].TICKET as [Card or Ticket Number], CASE WHEN [Lots].LotDesc IS NULL AND [Devices].NAME LIKE '%Library%' THEN 'Grand Rapids - Library' WHEN [Lots].LotDesc IS NULL AND [Devices].NAME LIKE '%Area 2 Spitter%' THEN 'Area 2' ELSE [Lots].LotDesc END as [Lot Name], 'Transient' as [Access Group], [Devices].NAME as [Lane], [Entries].ENTRY_TIME as [Activity Time], 'Amano McGann' as [Data Source], 'Transient' as [Parker Type], 'Total' as [Total] FROM McGANN.dbo.RV_ENTRIES as [Entries] LEFT OUTER JOIN McGANN.dbo.RV_CONFIG_DEVICES as [Devices] on ([Entries].DEVICE_KEY = [Devices].DEVICE_KEY) LEFT OUTER JOIN McGANN.dbo.SiteLots as [Lots] on ([Devices].LOT = [Lots].Lot_Number) WHERE [Entries].ENTRY_TIME >= '" + start + "' ORDER BY [Entries].ENTRY_TIME DESC", amcnxn)

    # AMANO ENTRIES TRANSFORMS
    # Combine Transient and Contractor
    amano_entries = pd.concat([amano_entries, amano_contract],
                              ignore_index=True, sort=False)

    # Format ID Numbers as Text
    amano_entries['Card or Ticket Number'] = amano_entries['Card or Ticket Number'].astype('Int64').astype('str')

    # Format and Add Dates
    amano_entries['Activity Time']      = pd.to_datetime(amano_entries['Activity Time'])

    amano_entries['Activity Time Hour'] = pd.to_datetime(amano_entries['Activity Time'].dt.strftime('%Y-%m-%d %H:00:00'))

    # YEAR FILTERS AND COMPARISON DATES
    # Initially Set Year Filter Column to Number of Years Ago
    amano_entries['Year'] = this_start.year - amano_entries['Activity Time'].dt.year

    # Determine Number of Unique Years in Dataset
    years_ago = amano_entries['Year'].unique()

    # Set Comparison Dates
    amano_entries['Comparison Date'] = amano_entries['Activity Time Hour']

    for number in years_ago:
        if number > 0:
            # Check is Current Year is Leap Year and Set Dates Accordingly
            if datetime.now().year - 1 % 4 == 0:
                amano_entries.loc[amano_entries['Year'] == number, 'Comparison Date'] = amano_entries['Activity Time Hour'] + timedelta(days=364 - int(number))
            else:
                amano_entries.loc[amano_entries['Year'] == number, 'Comparison Date'] = amano_entries['Activity Time Hour'] + timedelta(days=365 - int(number))

    # Convert Year Column to Filter by This, Last, and Previous Years
    amano_entries['Year'] = amano_entries['Activity Time'].dt.strftime('%Y')

    # Add Parking Ramp/Lot Coordinates
    amano_entries['Coordinates'] = None

    # Reorder Columns for Import
    amano_entries = amano_entries[['Entry ID',
                                   'Card or Ticket Number',
                                   'Lot Name',
                                   'Access Group',
                                   'Lane',
                                   'Comparison Date',
                                   'Activity Time Hour',
                                   'Activity Time',
                                   'Data Source',
                                   'Parker Type',
                                   'Year',
                                   'Coordinates']]

    return amano_entries


def get_exits(start, server, database, user, password):

    # SET RELATIVE DATES
    # This Year
    this_start = datetime(datetime.now().year, 1, 1, 0, 0, 0)
    this_end = datetime(datetime.now().year, 12, 31, 23, 59, 59)

    # Last Year
    if datetime.now().year - 1 % 4 == 0:
        last_start = this_start - timedelta(days=363)
        last_end = this_end - timedelta(days=363)
    else:
        last_start = this_start - timedelta(days=364)
        last_end = this_end - timedelta(days=364)

    # DATABASE CONNECTION
    amcnxn = pyodbc.connect(r'driver={SQL Server};'
                            r'server=' + server + r';'
                            r'database=' + database + r';'
                            r'UID=' + user +
                            r';PWD=' + password)

    # ENTRIES QUERIES
    amano_contract = pd.read_sql("SELECT 'AM-' + CAST([Contracts].ID AS VARCHAR(16)) AS [Exit ID], [Contracts].CARD_NUM as [Card or Ticket Number], [Lots].LotDesc as [Lot Name], [Access].GROUP_NAME as [Access Group], [Readers].DESCRIPTION as [Lane], [Contracts].ACTIVITY_TIME as [Exit Time], 'Amano McGann' as [Data Source],  'Contractor' as [Parker Type] FROM McGANN.dbo.CONTRACT_ACTIVITY as [Contracts] LEFT OUTER JOIN McGANN.dbo.SiteLots as [Lots] on ([Contracts].LOT_NUMBER = [Lots].Lot_Number) LEFT OUTER JOIN McGANN.dbo.READERS as [Readers] on ([Contracts].READER = [Readers].READER_NUM) LEFT OUTER JOIN McGANN.dbo.ACCESS_GROUP_NAMES as [Access] on ([Contracts].ACCESS_GROUP = [Access].GROUP_NUM) WHERE [Contracts].ACTIVITY_TIME >= '" + start + "' AND [Contracts].ACTIVITY_TIME <= '2029-01-01 00:00:00' AND ([Contracts].DIRECTION = 2) ORDER BY [Contracts].ACTIVITY_TIME DESC", amcnxn)
    amano_exits  = pd.read_sql("SELECT 'AM-' + CAST([Exits].ID AS VARCHAR(16)) as [Exit ID], [Exits].TICKET as [Card or Ticket Number], CASE WHEN [Lots].LotDesc IS NULL AND [Devices].NAME LIKE '%Library%' THEN 'Grand Rapids - Library' WHEN [Lots].LotDesc IS NULL AND [Devices].NAME LIKE '%Area 2 Spitter%' THEN 'Area 2' ELSE [Lots].LotDesc END as [Lot Name], 'Transient' as [Access Group], [Devices].NAME as [Lane], [Exits].EXIT_TIME as [Exit Time], 'Amano McGann' as [Data Source], 'Transient' as [Parker Type] FROM McGANN.dbo.RV_EXITS as [Exits] LEFT OUTER JOIN McGANN.dbo.RV_CONFIG_DEVICES as [Devices] on ([Exits].DEVICE_KEY = [Devices].DEVICE_KEY) LEFT OUTER JOIN McGANN.dbo.SiteLots as [Lots] on ([Devices].LOT = [Lots].Lot_Number) WHERE [Exits].ENTRY_TIME >= '" + start + "' AND [Exits].EXIT_TIME <= '" + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S') + "' ORDER BY [Exits].ENTRY_TIME DESC", amcnxn)

    # AMANO ENTRIES TRANSFORMS
    # Combine Transient and Contractor
    amano_exits = pd.concat([amano_exits, amano_contract],
                              ignore_index=True, sort=False)

    # Format ID Numbers as Text
    amano_exits['Card or Ticket Number'] = amano_exits['Card or Ticket Number'].astype('Int64').astype('str')

    # Format and Add Dates
    amano_exits['Exit Time']      = pd.to_datetime(amano_exits['Exit Time'])

    amano_exits['Exit Time Hour'] = pd.to_datetime(amano_exits['Exit Time'].dt.strftime('%Y-%m-%d %H:00:00'))

    # YEAR FILTERS AND COMPARISON DATES
    # Initially Set Year Filter Column to Number of Years Ago
    amano_exits['Year'] = this_start.year - amano_exits['Exit Time'].dt.year

    # Determine Number of Unique Years in Dataset
    years_ago = amano_exits['Year'].unique()

    # Set Comparison Dates
    amano_exits['Comparison Date'] = amano_exits['Exit Time Hour']

    for number in years_ago:
        if number > 0:
            # Check is Current Year is Leap Year and Set Dates Accordingly
            if datetime.now().year - 1 % 4 == 0:
                amano_exits.loc[amano_exits['Year'] == number, 'Comparison Date'] = amano_exits['Exit Time Hour'] + timedelta(days=364 - int(number))
            else:
                amano_exits.loc[amano_exits['Year'] == number, 'Comparison Date'] = amano_exits['Exit Time Hour'] + timedelta(days=365 - int(number))

    # Convert Year Column to Filter by This, Last, and Previous Years
    amano_exits['Year'] = amano_exits['Exit Time'].dt.strftime('%Y')

    # Add Parking Ramp/Lot Coordinates
    amano_exits['Coordinates'] = None

    # Reorder Columns for Import
    amano_exits = amano_exits[['Exit ID',
                               'Card or Ticket Number',
                               'Lot Name',
                               'Access Group',
                               'Lane',
                               'Comparison Date',
                               'Exit Time Hour',
                               'Exit Time',
                               'Data Source',
                               'Parker Type',
                               'Year',
                               'Coordinates']]

    return amano_exits


def get_sessions(start, server, database, user, password, end=None):

    # SET RELATIVE DATES
    # This Year
    this_start = datetime(datetime.now().year, 1, 1, 0, 0, 0)
    this_end = datetime(datetime.now().year, 12, 31, 23, 59, 59)

    # Last Year
    if datetime.now().year - 1 % 4 == 0:
        last_start = this_start - timedelta(days=363)
        last_end = this_end - timedelta(days=363)
    else:
        last_start = this_start - timedelta(days=364)
        last_end = this_end - timedelta(days=364)

    date_check = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')

    if date_check.year >= datetime.now().year - 1:
        database = database
    else:
        database = database + '_' + str(date_check.year)

    # DATABASE CONNECTION
    amcnxn = pyodbc.connect(r'driver={SQL Server};'
                            r'server=' + server + r';'
                            r'database=' + database + r';'
                            r'UID=' + user +
                            r';PWD=' + password)

    # ENTRIES QUERIES
    if end is None:
        amano_sessions = pd.read_sql(r"SELECT 'AM-' + CAST([Exits].ID AS VARCHAR(16)) as [Session ID]"
                                     r", [Exits].TICKET as [Card or Ticket Number]"
                                     r", CASE WHEN [Lots].LotDesc IS NULL AND [Devices].NAME LIKE '%Library%' THEN 'Grand Rapids - Library' "
                                     r"WHEN [Lots].LotDesc IS NULL AND [Devices].NAME LIKE '%Area 2 Spitter%' THEN 'Area 2' "
                                     r"ELSE [Lots].LotDesc END as [Lot Name]"
                                     r", 'Transient' as [Access Group]"
                                     r", [Devices].NAME as [Lane]"
                                     r", [Exits].ENTRY_TIME as [Session Start]"
                                     r", [Exits].EXIT_TIME as [Session End]"
                                     r",([Exits].CARD_AMOUNT + [Exits].CHECK_NUMBER + [Exits].CHECK_AMOUNT + [Exits].MISC_AMOUNT) as [Revenue]"
                                     r", DATEDIFF(minute, [Exits].ENTRY_TIME, [Exits].EXIT_TIME) as [Duration]"
                                     r", 'Amano McGann' as [Data Source]"
                                     r", 'Transient' as [Parker Type] "
                                     r"FROM " + database + ".dbo.RV_EXITS as [Exits] "
                                     r"LEFT OUTER JOIN McGANN.dbo.RV_CONFIG_DEVICES as [Devices] on ([Exits].DEVICE_KEY = [Devices].DEVICE_KEY) "
                                     r"LEFT OUTER JOIN McGANN.dbo.SiteLots as [Lots] on ([Devices].LOT = [Lots].Lot_Number) "
                                     r"WHERE [Exits].ENTRY_TIME >= '" + start + "'"
                                     r" AND [Exits].CARD_NUMBER != 0 "
                                     r"ORDER BY [Exits].ENTRY_TIME DESC",
                                    amcnxn)
    else:
        amano_sessions = pd.read_sql(r"SELECT 'AM-' + CAST([Exits].ID AS VARCHAR(16)) as [Session ID]"
                                     r", [Exits].TICKET as [Card or Ticket Number]"
                                     r", CASE WHEN [Lots].LotDesc IS NULL AND [Devices].NAME LIKE '%Library%' THEN 'Grand Rapids - Library' "
                                     r"WHEN [Lots].LotDesc IS NULL AND [Devices].NAME LIKE '%Area 2 Spitter%' THEN 'Area 2' "
                                     r"ELSE [Lots].LotDesc END as [Lot Name]"
                                     r", 'Transient' as [Access Group]"
                                     r", [Devices].NAME as [Lane]"
                                     r", [Exits].ENTRY_TIME as [Session Start]"
                                     r", [Exits].EXIT_TIME as [Session End]"
                                     r",([Exits].CARD_AMOUNT + [Exits].CHECK_NUMBER + [Exits].CHECK_AMOUNT + [Exits].MISC_AMOUNT) as [Revenue]"
                                     r", DATEDIFF(minute, [Exits].ENTRY_TIME, [Exits].EXIT_TIME) as [Duration]"
                                     r", 'Amano McGann' as [Data Source]"
                                     r", 'Transient' as [Parker Type] "
                                     r"FROM " + database + ".dbo.RV_EXITS as [Exits] "
                                     r"LEFT OUTER JOIN McGANN.dbo.RV_CONFIG_DEVICES as [Devices] on ([Exits].DEVICE_KEY = [Devices].DEVICE_KEY) "
                                     r"LEFT OUTER JOIN McGANN.dbo.SiteLots as [Lots] on ([Devices].LOT = [Lots].Lot_Number) "
                                     r"WHERE [Exits].ENTRY_TIME >= '" + start + "' AND [Exits].ENTRY_TIME <='" + end + "'"
                                     r" AND [Exits].CARD_NUMBER != 0 "
                                     r"ORDER BY [Exits].ENTRY_TIME DESC",
                                    amcnxn)


    # Format ID Numbers as Text
    amano_sessions['Card or Ticket Number'] = amano_sessions['Card or Ticket Number'].astype('Int64').astype('str')

    # Format and Add Dates
    amano_sessions['Session Start']      = pd.to_datetime(amano_sessions['Session Start'])

    amano_sessions['Session Start Hour'] = pd.to_datetime(amano_sessions['Session Start'].dt.strftime('%Y-%m-%d %H:00:00'))

    # YEAR FILTERS AND COMPARISON DATES
    # Initially Set Year Filter Column to Number of Years Ago
    amano_sessions['Year'] = this_start.year - amano_sessions['Session Start'].dt.year

    # Determine Number of Unique Years in Dataset
    years_ago = amano_sessions['Year'].unique()

    # Set Comparison Dates
    amano_sessions['Comparison Date'] = amano_sessions['Session Start Hour']

    for number in years_ago:
        if number > 0:
            # Check is Current Year is Leap Year and Set Dates Accordingly
            if datetime.now().year - 1 % 4 == 0:
                amano_sessions.loc[amano_sessions['Year'] == number, 'Comparison Date'] = amano_sessions['Session Start Hour'] + timedelta(days=364 - int(number))
            else:
                amano_sessions.loc[amano_sessions['Year'] == number, 'Comparison Date'] = amano_sessions['Session Start Hour'] + timedelta(days=365 - int(number))

    # Convert Year Column to Filter by This, Last, and Previous Years
    amano_sessions['Year'] = amano_sessions['Session Start'].dt.strftime('%Y')

    # Add Parking Ramp/Lot Coordinates
    amano_sessions['Coordinates'] = None

    # Reorder Columns for Import
    amano_sessions = amano_sessions[['Session ID',
                                     'Card or Ticket Number',
                                     'Lot Name',
                                     'Access Group',
                                     'Lane',
                                     'Revenue',
                                     'Duration',
                                     'Comparison Date',
                                     'Session Start Hour',
                                     'Session Start',
                                     'Session End',
                                     'Data Source',
                                     'Parker Type',
                                     'Year',
                                     'Coordinates']]

    return amano_sessions


def get_contract_sessions(start, server, database, user, password):

    # DATABASE CONNECTION
    amcnxn = pyodbc.connect(r'driver={SQL Server};'
                            r'server=' + server + r';'
                            r'database=' + database + r';'
                            r'UID=' + user +
                            r';PWD=' + password)

    # QUERY
    amano_contract = pd.read_sql("SELECT TOP (1000) 'AM-' + CAST([Exits].ID AS VARCHAR(16)) as [Session ID], [Exits].TICKET as [Card or Ticket Number], CASE WHEN [Lots].LotDesc IS NULL AND [Devices].NAME LIKE '%Library%' THEN 'Grand Rapids - Library' WHEN [Lots].LotDesc IS NULL AND [Devices].NAME LIKE '%Area 2 Spitter%' THEN 'Area 2' ELSE [Lots].LotDesc END as [Lot Name], 'Transient' as [Access Group], [Devices].NAME as [Lane], [Exits].ENTRY_TIME as [Session Start], [Exits].EXIT_TIME as [Session End],([Exits].CARD_AMOUNT + [Exits].CHECK_NUMBER + [Exits].CHECK_AMOUNT + [Exits].MISC_AMOUNT) as [Revenue], DATEDIFF(minute, [Exits].ENTRY_TIME, [Exits].EXIT_TIME) as [Duration], 'Amano McGann' as [Data Source], 'Transient' as [Parker Type] FROM McGANN.dbo.RV_EXITS as [Exits] LEFT OUTER JOIN McGANN.dbo.RV_CONFIG_DEVICES as [Devices] on ([Exits].DEVICE_KEY = [Devices].DEVICE_KEY) LEFT OUTER JOIN McGANN.dbo.SiteLots as [Lots] on ([Devices].LOT = [Lots].Lot_Number) WHERE [Exits].ENTRY_TIME >= '2018-01-01 00:00:00' AND [Exits].EXIT_TIME <= '" + start + "' AND [Exits].CARD_NUMBER != 0 ORDER BY [Exits].ENTRY_TIME DESC",
                                 amcnxn)

    # AMANO CONTRACTOR ENTRY AND EXIT FORMATTING FOR COMPLETED SESSIONS

    cards = list(amano_contract['Card or Ticket Number'].unique())

    for card in cards:
        current_card = amano_contract.loc[amano_contract['Card or Ticket Number'] == card]
        if current_card['Activity Time'].loc[current_card.index.min()] == 'Entry':
            current_card.drop(index=current_card.index.min())

        # Separate Exits and Entries
        card_exits = current_card.loc[current_card['Activity Type'] == 'Exit']
        card_entries = current_card.loc[current_card['Activity Type'] == 'Entry']

        # Check that Lengths Match and Join Dataframes
        if len(card_entries) == len(card_exits):
            card_entries.reset_index().join(card_exits['Activity Time'].reset_index(), rsuffix='_exit')


def get_reserved_occupancy(start, server, database, user, password):
    # DATABASE CONNECTION
    amcnxn = pyodbc.connect(r'driver={SQL Server};'
                            r'server=' + server + r';'
                            r'database=' + database + r';'
                            r'UID=' + user +
                            r';PWD=' + password)

    # QUERY
    amano_contract = pd.read_sql(
        "SELECT"
        "[Cards].CARD_NUM as [Card Number]"
        ",[Contract].CARD_NUM as [Contract Number]"
        ",[Contract].ACTIVITY_TIME as [Activity Time]"
        ",[Cards].IO_STATUS as [Status]"
        ",[Lots].LotDesc as [Lot Name]"
        ",[Access].GROUP_NAME as [Access Group]"
        "FROM McGANN.dbo.CARDS as [Cards]"
        "LEFT OUTER JOIN McGANN.dbo.CONTRACT_ACTIVITY as [Contract] on ([Cards].CARD_NUM = [Contract].CARD_NUM)"
        "LEFT OUTER JOIN McGANN.dbo.ACCESS_GROUP_NAMES as [Access] on ([Contract].ACCESS_GROUP = [Access].GROUP_NUM)"
        "LEFT OUTER JOIN McGANN.dbo.SiteLots as [Lots] on ([Contract].LOT_NUMBER = [Lots].Lot_Number) "
        "WHERE ([Lots].LotDesc = 'DeVos Place'"
        "OR [Lots].LotDesc = 'Louis Campau'"
        "OR [Lots].LotDesc = 'Monroe Center'"
        "OR [Lots].LotDesc = 'Ottawa Fulton'"
        "OR [Lots].LotDesc = 'Pearl Ionia'"
        "OR [Lots].LotDesc = 'Western Commerce')"
        "AND ([Access].GROUP_NAME LIKE '%24/7%' OR [Access].GROUP_NAME LIKE '%RESERVE%')"
        "ORDER BY [Contract].ACTIVITY_TIME DESC",
        amcnxn)

    # RECODE STATUS FOR OCCUPANCY CALCULATION
    amano_contract['Type'] = None

    amano_contract.loc[amano_contract['Status'] == 1, 'Type'] = 'Entry'
    amano_contract.loc[amano_contract['Status'] == 2, 'Type'] = 'Exit'
    amano_contract.loc[amano_contract['Status'] == 0, 'Type'] = 'Neutral'

    # CALCULATE OCCUPANCY
    amano_contract = amano_contract.groupby(by='Card Number').agg({'Activity Time': max,
                                                                   'Lot Name': 'first',
                                                                   'Type': 'first'})

    # ADD COLUMN TO CALCULATE TOTALS
    amano_contract['Count'] = 1

    # CALCULATE TOTAL CARDS
    available = amano_contract.loc[amano_contract['Type'] == 'Exit'].groupby(by='Lot Name').agg({'Count': sum}) \
    .reset_index()
    available['Parker Type'] = 'Available'

    # CALCULATE UNKNOWN/NEUTRAL
    unknown = amano_contract.loc[amano_contract['Type'] == 'Neutral'].groupby(by='Lot Name').agg({'Count': sum}) \
    .reset_index()
    unknown['Parker Type'] = 'Available'

    # CALCULATE CURRENT OCCUPANCY
    occupied = amano_contract.loc[amano_contract['Type'] == 'Entry'].groupby(by='Lot Name').agg({'Count': sum}) \
    .reset_index()
    occupied['Parker Type'] = 'Contract'

    # COMBINE DATA
    contract_occupancy = pd.concat([available, unknown, occupied], sort=True)

    # ADD MISSING COLUMNS
    # DATE
    contract_occupancy['Date'] = datetime.now().strftime('%Y-%m-%d %H:00:00')

    # DATA SOURCE
    contract_occupancy['Data Source'] = 'Amano-McGann'

    # LOT NAME
    contract_occupancy['Lot Name'] = contract_occupancy['Lot Name'] + ' (Reserved)'

    # COMPARISON DATES AND YEAR FILTER
    contract_occupancy['Comparison Date'] = contract_occupancy['Date']

    contract_occupancy['Year'] = pd.to_datetime(contract_occupancy['Date'], format='%Y-%m-%d %H:%M:%S')
    contract_occupancy['Year'] = contract_occupancy['Year'].dt.strftime('%Y')

    return contract_occupancy

