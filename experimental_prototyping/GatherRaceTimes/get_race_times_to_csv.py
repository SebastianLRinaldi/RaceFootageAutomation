import csv
import re

data = """
Lap	
1st place
29: EpicX18 GT9
2nd place
26: timmehhh ...
3rd place
23: JGrigs GT9
4
28: Tumelo GT9
5
27: Qberry GT9
6
21: Cookie.Monster...
7
20: JBreezy GT9
8
24: The King of bl...
9
25: Green Shell Sn...
10
10: jerry ...
1	23.715	22.961	23.391	23.471	23.593	23.213	24.228	23.708	24.855	24.314
2	22.728	22.504	22.885	23.243	23.366	22.693	23.477	23.165	24.404	23.886
3	22.784	23.76	23.003	24.285	23.156	22.777	22.984	23.055	24.47	23.874
4	22.75	22.954	22.894	22.664	23.2	22.755	22.949	23.183	26.468	24.275
5	23.901	22.595	23.082	22.628	22.955	23.383	22.886	24.168	24.13	23.397
6	23.076	22.648	22.879	24.249	23.156	22.892	22.897	23.171	23.827	23.537
7	22.719	22.646	22.823	22.652	23.067	22.61	22.753	23.165	24.129	23.466
8	22.742	22.62	22.624	22.609	22.85	22.817	22.855	23.29	26.226	23.718
9	23.345	22.553	22.84	22.324	22.884	23.031	22.716	23.952	25.393	23.528
10	22.614	22.653	22.991	22.304	22.961	22.794	22.744	23.124	24.809	23.562
11	22.423	22.528	22.738	22.433	22.7	22.717	22.504	23.649	25.04	24.665
12	23.725	22.667	22.282	22.756	22.86	22.545	23.002	23.83	25.978	24.356
13	22.988	22.344	22.44	22.576	23.015	22.555	22.792	23.621	23.474	24.118
14	22.766	22.677	22.621	22.461	22.857	22.571	22.957	23.29	23.745	23.463
15	22.386	22.359	22.59	22.685	23.084	22.567	23.802	24.424	23.766	23.808
16	22.592	22.225	22.519	22.621	22.658	22.533	22.917	23.34	23.497	23.351
17	22.322	22.463	22.239	22.33	22.573	22.514	23.146	23.265	23.15	24.039
18	22.796	22.368	22.663	22.293	22.875	22.601	22.922	23.006	23.797	23.26
19	22.49	22.444	22.815	22.692	22.662	22.535	23.537	23.25	23.59	33.827
20	22.315	22.528	22.549	22.568	22.534	22.761	23.029	22.904	23.139	24.735
21	22.473	22.764	22.705	22.46	22.611	22.598	23.124	22.955	23.529	23.203
22	22.187	22.83	22.606	22.626	22.433	22.625	22.881	22.974	 	 
23	22.221	22.5	22.594	22.416	23.745	22.451	23.85	23.285	 	 	 	 	 	 	 	 	 
"""  # Paste your raw data here

# Step 1: Clean and split lines
lines = [line.strip() for line in data.strip().splitlines() if line.strip()]

# Step 2: Extract racer names in order
racers = []
i = 0
while i < len(lines):
    if re.match(r'^\d+:', lines[i]):  # Line like "14: Crown GT9"
        _, name = lines[i].split(':', 1)
        racers.append(name.strip())
    elif re.match(r'^\d+\t', lines[i]):  # Start of lap data
        break
    i += 1

# Step 3: Extract lap data
lap_lines = lines[i:]
laps = [line.split('\t') for line in lap_lines]

# Step 4: Normalize lap rows
rows = []
for lap in laps:
    lap_num = lap[0]
    times = lap[1:]
    # Pad or truncate to match racer count
    times += [''] * (len(racers) - len(times))
    row = [lap_num] + times[:len(racers)]
    rows.append(row)

# Step 5: Write CSV
with open('lap_times1.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Lap'] + racers)
    writer.writerows(rows)

print("CSV saved as lap_times1.csv")
