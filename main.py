import pandas as pd
import os
import glob
import re


number_of_events_per_discipline={
    'Badminton':0,

}

def read_csv_files(path = os.getcwd()):
    return glob.glob(os.path.join(path+r'\resources','*.xlsx'))

def read_csv_file_names(path = os.getcwd()):
    return os.listdir(path+r'\resources')

def show_finished_disciplines_and_events():
    pattern = re.compile(r'^(?P<Dyscyplina>[^#]+)#(?P<Konkurencja>[^.]+)\.xlsx$')
    discipline_dict={}
    csv_file_names= read_csv_file_names()
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
    point_table_dict={}
    for f in csv_files:
        temp_df = pd.read_excel(f)
        if top3!=0:
            temp_df = temp_df[temp_df['Pozycja'].isin([1, 2, 3])]
            # TODO
        point_table_dict_grouped = temp_df.groupby('Kraj')['Punkty'].sum().to_dict()
        for country, points in point_table_dict_grouped.items():
            if country in point_table_dict:
                point_table_dict[country] += points
            else:
                point_table_dict[country] = points
    
    sorted_point_table_dict=dict(sorted(point_table_dict.items(), key=lambda value:value[1], reverse=True))
    return sorted_point_table_dict

def main():


    print(show_current_points_table(1))

if __name__ == '__main__':
    main()