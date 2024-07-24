import pandas as pd
import os
import glob
import re




def main():
    pattern = re.compile(r'^(?P<Dyscyplina>[^#]+)#(?P<Konkurencja>[^.]+)\.xlsx$')
    path = os.getcwd()
    csv_files = glob.glob(os.path.join(path+r'\resources','*.xlsx'))
    csv_file_names=os.listdir(path+r'\resources')
    discipline_dict={}
    point_table_dict={}
    

    for filename in csv_file_names:
        match = pattern.match(filename)
        if match:
            dyscyplina = match.group('Dyscyplina')
            konkurencja = match.group('Konkurencja')
            
            if dyscyplina in discipline_dict:
                discipline_dict[dyscyplina].append(konkurencja)
            else:
                discipline_dict[dyscyplina] = [konkurencja]

    for f in csv_files:
        temp_df = pd.read_excel(f)
        point_table_dict_grouped = temp_df.groupby('Kraj')['Punkty'].sum().to_dict()
        for country, points in point_table_dict_grouped.items():
            if country in point_table_dict:
                point_table_dict[country] += points
            else:
                point_table_dict[country] = points
    
    sorted_point_table_dict=dict(sorted(point_table_dict.items(), key=lambda value:value[1], reverse=True))
    print(sorted_point_table_dict)
    print(discipline_dict)

if __name__ == '__main__':
    main()