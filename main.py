import pandas as pd
import os
import glob
import re
import numpy as np
import matplotlib.pyplot as plt
import squarify
from continents import get_continent_for_country


number_of_events_per_discipline = {
    'Badminton': 5,
    'Breakdancing': 2,
    'Boks': 13,
    'GimnastykaArtystyczna': 2,
    'GimnastykaSportowa': 14,
    'GimnastykaTrampolina': 2,
    'Golf': 2,
    'HokejNaTrawie': 2,
    'Jeździectwo': 6,
    'Judo': 15,
    'KajakarstwoGorskie': 6,
    'KajakarstwoRegatowe': 10,
    'KolarstwoBMX': 4,
    'KolarstwoGorskie': 2,
    'KolarstwoSzosowe': 4,
    'KolarstwoTorowe': 12,
    'Koszykowka': 2,
    'Koszykowka3x3': 2,
    'Lekkoatletyka': 48,
    'Lucznictwo': 5,
    'PieciobojNowoczesny': 2,
    'PilkaNozna': 2,
    'PilkaReczna': 2,
    'PilkaWodna': 2,
    'Plywanie': 37,
    'PlywanieSynchroniczne': 2,
    'PodnoszenieCiezarow': 10,
    'Rugby7': 2,
    'Siatkowka': 2,
    'SiatkowkaPlazowa': 2,
    'Skateboarding': 4,
    'SkokiDoWody': 8,
    'Strzelectwo': 15,
    'Surfing': 2,
    'Szermierka': 12,
    'Taekwondo': 8,
    'TenisStolowy': 5,
    'TenisZiemny': 5,
    'Triathlon': 3,
    'Wioslarstwo': 14,
    'WspinaczkaSportowa': 4,
    'Zapasy': 18,
    'Zeglarstwo': 10
}

def read_csv_files(path=os.getcwd()):
    return glob.glob(os.path.join(path, 'resources', '**', '*.xlsx'), recursive=True)

def read_csv_file_names(path=os.getcwd()):
    file_names = []
    for root, _, files in os.walk(os.path.join(path, 'resources')):
        for file in files:
            if file.endswith('.xlsx'):
                file_names.append(file)
    return file_names

def get_csv_file_number(path=os.getcwd()):
    return len(read_csv_file_names(path))

def show_finished_disciplines_and_events():
    pattern = re.compile(r'^(?P<Dyscyplina>[^#]+)#(?P<Konkurencja>[^.]+)\.xlsx$')
    discipline_dict = {}
    csv_file_names = read_csv_file_names()
    for filename in csv_file_names:
        match = pattern.match(filename)
        if match:
            dyscyplina = match.group('Dyscyplina')
            konkurencja = match.group('Konkurencja')
            if dyscyplina in discipline_dict:
                discipline_dict[dyscyplina].append(konkurencja)
            else:
                discipline_dict[dyscyplina] = [konkurencja]
    return discipline_dict

def show_current_points_table(top3=0):
    csv_files = read_csv_files()
    point_table_dict = {}
    for f in csv_files:
        temp_df = pd.read_excel(f)
        if top3 != 0:
            temp_df = temp_df[temp_df['Pozycja'].isin([1, 2, 3])]
        point_table_dict_grouped = temp_df.groupby(['Kraj', 'Pozycja'])['Punkty'].sum().reset_index()
        for _, row in point_table_dict_grouped.iterrows():
            country = row['Kraj']
            position = row['Pozycja']
            points = row['Punkty']
            if country not in point_table_dict:
                point_table_dict[country] = {'Liczba Punktów': 0}
                for i in range(1, 9):
                    point_table_dict[country][str(i)] = 0
            point_table_dict[country]['Liczba Punktów'] += points
            if position <= 8:
                point_table_dict[country][str(position)] += 1
    sorted_point_table_dict = dict(sorted(point_table_dict.items(), key=lambda value: (
        -value[1]['Liczba Punktów'],
        -value[1]['1'],
        -value[1]['2'],
        -value[1]['3'],
        -value[1]['4'],
        -value[1]['5'],
        -value[1]['6'],
        -value[1]['7'],
        -value[1]['8']
    )))

    return sorted_point_table_dict

def export_points_table_to_excel(p_table):
    rows = []
    for country, data in p_table.items():
        row = [country, data['Liczba Punktów']]
        row.extend([data[str(i)] for i in range(1, 9)])
        rows.append(row)
    columns = ['Kraj', 'Liczba Punktów'] + [str(i) for i in range(1, 9)]
    df = pd.DataFrame(rows, columns=columns)
    df.insert(0, 'Index', range(1, len(df) + 1))

    df.to_excel('results/StandingsAfter' + str(get_csv_file_number()) + 'Events.xlsx', index=False)
    # df.to_excel('results/JudoFull.xlsx', index=False)
    # df.to_excel('results/Lekkoatletyka8Aug.xlsx', index=False)


def export_daily_points_to_excel(daily_points_dict):
    rows = []
    for country, daily_points in daily_points_dict.items():
        total_points = sum(daily_points.values())
        row = [country, total_points]
        for day in sorted(daily_points.keys(), key=int):
            row.append(daily_points[day])
        rows.append(row)

    rows.sort(key=lambda x: x[1], reverse=True)

    all_days = sorted({day for daily_points in daily_points_dict.values() for day in daily_points.keys()}, key=int)
    columns = ['Kraj', 'Total Points'] + [f'Day {day}' for day in all_days]

    df = pd.DataFrame(rows, columns=columns)

    output_file = 'results/DailyPointsTable.xlsx'
    df.to_excel(output_file, index=False)

def calculate_completion_percentage():
    pattern = re.compile(r'^(?P<Dyscyplina>[^#]+)#(?P<Konkurencja>[^.]+)\.xlsx$')
    discipline_dict = show_finished_disciplines_and_events()
    completion_percentage = {}
    for discipline, events in discipline_dict.items():
        if discipline in number_of_events_per_discipline:
            total_events = number_of_events_per_discipline[discipline]
            completed_events = len(events)
            completion_percentage[discipline] = (completed_events / total_events) * 100
    return completion_percentage

def calculate_points_table(discipline_names=None, start=1, end=8):
    point_table_dict = {}
    csv_files = read_csv_files()

    if discipline_names:
        pattern = re.compile(rf'^.*\\({"|".join(map(re.escape, discipline_names))})#(?P<Konkurencja>[^.]+)\.xlsx$')
    else:
        pattern = re.compile(r'^(?P<Dyscyplina>[^#]+)#(?P<Konkurencja>[^.]+)\.xlsx$')

    for file_path in csv_files:
        filename = os.path.relpath(file_path, start=os.getcwd())
        if pattern.match(filename):
            df = pd.read_excel(file_path)
            df = df[df['Pozycja'].between(start, end)]
            for _, row in df.iterrows():
                country = row['Kraj']
                position = row['Pozycja']
                points = row['Punkty']
                if country not in point_table_dict:
                    point_table_dict[country] = {'Liczba Punktów': 0}
                    for i in range(1, 9):
                        point_table_dict[country][str(i)] = 0
                point_table_dict[country]['Liczba Punktów'] += points
                if position <= 8:
                    point_table_dict[country][str(position)] += 1

    sorted_point_table_dict = dict(sorted(point_table_dict.items(), key=lambda value: (
        -value[1]['Liczba Punktów'],
        -value[1]['1'],
        -value[1]['2'],
        -value[1]['3'],
        -value[1]['4'],
        -value[1]['5'],
        -value[1]['6'],
        -value[1]['7'],
        -value[1]['8']
    )))
    return sorted_point_table_dict

def create_daily_points_dict():
    csv_files = read_csv_files()
    daily_points_dict = {}
    pattern = re.compile(r'resources\\(\d+)#[^\\]+\\(?P<discipline>[^#]+)#(?P<event>[^.]+)\.xlsx$')
    
    all_days = set()
    for file_path in csv_files:
        match = pattern.search(file_path)
        if match:
            day = match.group(1)
            all_days.add(day)
    all_days = sorted(all_days, key=int)

    for file_path in csv_files:
        match = pattern.search(file_path)
        if match:
            day = match.group(1)
            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                country = row['Kraj']
                if country not in daily_points_dict:
                    daily_points_dict[country] = {day: 0 for day in all_days}
                points = row['Punkty']
                daily_points_dict[country][day] += points

    for country in daily_points_dict:
        for day in all_days:
            if day not in daily_points_dict[country]:
                daily_points_dict[country][day] = 0

    for country in daily_points_dict:
        daily_points_dict[country]['Kontynent'] = get_continent_for_country(country)

    return daily_points_dict

def daily_points_dict_to_dataframe(daily_points_dict):
    rows = []

    for country, details in daily_points_dict.items():
        continent = details.get('Kontynent', 'Nieznany kontynent')
        daily_points = {k: details.get(k, 0) for k in details if k != 'Kontynent'}
        total_points = sum(daily_points.values())
        row = [country, continent, total_points]
        for day in sorted(daily_points.keys(), key=lambda x: int(x) if x.isdigit() else 0):
            row.append(daily_points[day])
        rows.append(row)

    rows.sort(key=lambda x: x[2], reverse=True)

    all_days = sorted(
        {day for details in daily_points_dict.values() for day in details.keys() if day.isdigit()},
        key=int
    )
    columns = ['Kraj', 'Kontynent', 'Punkty'] + [f'Dzien {day}' for day in all_days]

    df = pd.DataFrame(rows, columns=columns)

    return df

def get_tree_chart_from_dict(points_per_day_dict):
    df = daily_points_dict_to_dataframe(points_per_day_dict)

    color_mapping = {
        'Europa': 'blue',
        'Afryka': 'black',
        'Azja': 'yellow',
        'Australia': 'green',
        'Ameryka': 'red',
        'Nieznany kontynent': 'gray',
        'Neutralni': 'gray'
    }

    colors = [color_mapping.get(continent, 'gray') for continent in df['Kontynent']]

    plt.figure(figsize=(12, 8))

    squarify.plot(sizes=df['Punkty'], label=df['Kraj'], color=colors, alpha=.8, pad=True)

    for i, rect in enumerate(squarify.squarify(df['Punkty'], x=0, y=0, dx=1, dy=1)):
        x, y, w, h = rect['x'], rect['y'], rect['dx'], rect['dy']
        font_size = min(12, max(8, df['Punkty'].iloc[i] / max(df['Punkty']) * 12))
        if df['Punkty'].iloc[i] >= 10:
            plt.text(x + w / 2, y + h / 2, df['Kraj'].iloc[i],
                     fontsize=font_size, ha='center', va='center', color='white')
    
    plt.axis('off')
    plt.show()

def get_athletes_by_country(country, path=os.getcwd()):
    pattern = re.compile(r'\\(?P<day>\d+)#[^\\]+\\(?P<discipline>[^#]+)#(?P<competition>[^.]+)\.xlsx$')
    
    athletes_data = []
    
    csv_files = glob.glob(os.path.join(path, 'resources', '**', '*.xlsx'), recursive=True)
    
    for file_path in csv_files:
        match = pattern.search(file_path)
        if match:
            day = match.group('day')
            discipline = match.group('discipline')
            competition = match.group('competition')
            
            df = pd.read_excel(file_path)
            
            country_df = df[df['Kraj'] == country].copy()
            
            country_df['Dzień'] = day
            country_df['Dyscyplina'] = discipline
            country_df['Konkurencja'] = competition
            
            athletes_data.append(country_df[['Pozycja', 'Imię', 'Nazwisko', 'Punkty', 'Dyscyplina', 'Konkurencja', 'Dzień']])
    
    if athletes_data:
        final_df = pd.concat(athletes_data, ignore_index=True)
        
        final_df.sort_values(by=['Pozycja', 'Punkty'], ascending=[True, False], inplace=True)
    else:
        final_df = pd.DataFrame(columns=['Pozycja', 'Imię', 'Nazwisko', 'Punkty', 'Dyscyplina', 'Konkurencja', 'Dzień'])
    
    final_df.index = np.arange(1, len(final_df)+1)
    return final_df

def get_full_results(path=os.getcwd()):
    pattern = re.compile(r'\\(?P<day>\d+)#[^\\]+\\(?P<discipline>[^#]+)#(?P<competition>[^.]+)\.xlsx$')
    
    athletes_data = []
    
    csv_files = glob.glob(os.path.join(path, 'resources', '**', '*.xlsx'), recursive=True)
    
    for file_path in csv_files:
        match = pattern.search(file_path)
        if match:
            day = int(match.group('day'))
            discipline = match.group('discipline')
            competition = match.group('competition')
            
            df = pd.read_excel(file_path)
            
            df['Dzień'] = day
            df['Dyscyplina'] = discipline
            df['Konkurencja'] = competition
            df['Kraj'] = df['Kraj']
            
            athletes_data.append(df[['Pozycja', 'Imię', 'Nazwisko', 'Punkty', 'Dyscyplina', 'Konkurencja', 'Dzień', 'Kraj']])
    
    if athletes_data:
        final_df = pd.concat(athletes_data, ignore_index=True)
        final_df.sort_values(by=['Dzień','Konkurencja','Pozycja'], ascending=[True, True, True], inplace=True)
    else:
        final_df = pd.DataFrame(columns=['Pozycja', 'Imię', 'Nazwisko', 'Punkty', 'Dyscyplina', 'Konkurencja', 'Dzień', 'Kraj'])
    
    final_df.index = np.arange(1, len(final_df)+1)
    return final_df

def main():

    # df = get_athletes_by_country('Węgry')
    # print(df)
    # df.to_excel('results/PolscyPunktujący.xlsx')

    df=get_full_results()
    print(df)
    df.to_excel('results/FullPoints.xlsx')

    completion_percentage = calculate_completion_percentage()
    print(completion_percentage)
    points_table = calculate_points_table()
    print(points_table)
    export_points_table_to_excel(points_table)
    print(get_csv_file_number())

    # daily_points = create_daily_points_dict()
    # print(daily_points)
    # export_daily_points_to_excel(daily_points)



    # completion_percentage = calculate_completion_percentage()
    # print(completion_percentage)
    # points_table = calculate_points_table(['Lekkoatletyka'])
    # print(points_table)
    # export_points_table_to_excel(points_table)
    # print(get_csv_file_number())

    # get_tree_chart_from_dict(daily_points)

if __name__ == '__main__':
    main()
