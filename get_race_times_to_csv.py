import csv
import re

data = """
Lap	
1st place
26: Tumelo GT9
2nd place
25: JGrigs GT9
3rd place
27: Myles per hour...
4
20: EpicX18 GT9
5
24: Qberry GT9
6
21: Tdm GT9
7
6: Alex
8
12: Angel lopez-va...
9
1: Sam
1	24.552	24.84	24.288	24.459	23.702	24.118	31.707	29.207	28.583
2	23.575	26.294	23.848	23.888	23.686	24.556	29.679	27.028	26.967
3	22.403	23.295	22.926	22.623	23.164	23.951	31.487	27.788	28.148
4	23.252	23.829	23.272	23.368	23.512	24.302	28.573	31.428	30.054
5	22.405	23.643	23.114	23.087	23.688	24.045	26.938	26.816	28.092
6	22.556	23.054	23.077	24.201	23.08	23.514	30.582	25.849	26.495
7	22.492	22.908	22.74	22.646	22.849	23.461	93.064	25.72	27.706
8	22.414	22.725	22.667	22.654	22.689	23.626	26.971	28.111	28.795
9	22.397	26.162	24.873	25.23	25.714	26.593	29.842	34.734	29.987
10	23.042	23.424	23.445	23.231	24.235	24.944	26.406	25.743	26.955
11	23.239	24.823	24.994	25.676	24.893	23.91	25.56	29.412	29.582
12	23.642	22.931	22.902	22.721	22.999	23.426	27.895	27.085	28.848
13	22.005	22.622	22.871	22.708	24.056	24.458	28.236	29.161	29.51
14	22.361	23.394	22.549	23.561	23.037	23.482	28.935	29.995	28.585
15	22.1	22.501	22.525	26.509	23.032	24.312	26.004	28.218	28.713
16	22.523	22.738	22.944	22.933	22.849	23.105	26.98	31.235	30.375
17	23.825	23.031	22.473	22.871	22.87	25.164	26.639	29.335	29.416
18	23.265	22.678	22.835	22.643	22.621	23.364	25.127	26.333	29.687
19	23.362	22.462	23.178	22.671	22.819	24.033	 	26.944	27.778
20	22.409	24.302	22.701	23.544	24.327	23.391	 	26.253	29.648
21	22.024	23.776	22.623	23.424	23.312	23.489	 	 	 
22	22.274	22.639	23.013	22.756	23.249	23.316	 	 	 
23	22.649	22.447	22.674	22.609	22.738	23.125	 	 	 
24	22.344	22.419	22.807	22.474	22.729	 	 	 	 
25	22.359	 	 	 	 	 	 	 	 
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
with open('lap_times.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Lap'] + racers)
    writer.writerows(rows)

print("CSV saved as lap_times.csv")
