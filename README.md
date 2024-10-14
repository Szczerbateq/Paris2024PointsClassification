# Paris2024PointsClassification

The app requires resources directory with [day number]#[day and month] directories that contain .xlsx files for every discipline and event with TOP8 athletes. The data was collected manually, so it might contain some errors.

## Points Allocation
I distribute exactly 36 points for every event, spliting them between tied athletes. Every athlete that scored gold medal gets 8 points, the silver medalists get 7 points etc. and finally, the 8th athlete gets 1 point. Results are taken from olympics.com. Mind the fact, that different sports might have a different tie-breaking rules and i always refer to the official results .pdf file of each discipline. The points are always applied on the day of the final of certain event (or after all top8 places are set) even if e.g. teams from places 5-8 are already set.

## Data Preparation
Every event .xlsx file contains 5 columns:
- position
- name
- surname
- country
- points

If it was team or duet event, name and surname columns remain empty.

## Capabilities

### Partial data
The app allows to create separate .xlsx files for each:
- day
- country
- discipline

It also allows to return .xlsx file containing:
- index
- position
- name
- surname
- country
- points
- discipline
- event
- day
that can be used to extract interesting data using pivot tables.

### Points classification

Main goal of the script was to be able to follow changes in points classification during the Olympic Games in Paris and final Results.xlsx would look like this. Important thing to keep in mind here is the fact that not every 8th place is worth the same amount of points (this apply to all other positions too), so the amount of points is not directly taken from the placings, it is rather summed using data from each event .xlsx. Example results are below, they contain TOP10 countries in terms of

Index|Kraj|Liczba Punktów|1|2|3|4|5|6|7|8
-|-|-|-|-|-|-|-|-|-|-
1|USA|1179|40|44|42|19|30|16|15|20
2|Chiny|837,5|40|27|24|9|18|13|14|11
3|Francja|687,5|16|26|22|16|21|14|16|18
4|Wielka Brytania|679|14|22|29|19|23|8|13|8
5|Włochy|548|12|13|15|20|25|17|10|8
6|Australia|530|18|19|16|11|11|11|13|10
7|Japonia|515|20|12|13|8|23|12|16|11
8|Niemcy|480|12|13|8|12|22|22|13|15
9|Holandia|377,5|15|7|12|14|5|10|8|5
10|Kanada|332,5|9|7|11|11|9|9|9|13






