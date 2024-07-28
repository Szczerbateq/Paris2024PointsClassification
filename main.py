import pandas as pd
import os
import glob
import re

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
    return glob.glob(os.path.join(path+r'\resources', '*.xlsx'))

def read_csv_file_names(path=os.getcwd()):
    return os.listdir(path+r'\resources')

def get_csv_file_number(path=os.getcwd()):
    return len(os.listdir(path+r'\resources'))

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

    df.to_excel('results\StandingsAfter'+str(get_csv_file_number())+'Events.xlsx', index=False)


def main():

    result_table=show_current_points_table()
    print(result_table)
    export_points_table_to_excel(result_table)
    print(get_csv_file_number())

if __name__ == '__main__':
    main()  