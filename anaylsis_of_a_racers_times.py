# import csv

# def get_racer_times(filename, racer_name):
#     with open(filename, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         if racer_name not in reader.fieldnames:
#             print("Racer name not found")
#             return []
#         return [row[racer_name] for row in reader]

# # Usage
# times = get_racer_times('lap_times.csv', 'EpicX18 GT9')
# print(times)



# import csv

# def get_racer_times(filename, racer_name):
#     with open(filename, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         if racer_name not in reader.fieldnames:
#             print("Racer name not found")
#             return []
        
#         times = []
#         for row in reader:
#             time_str = row[racer_name]
#             if not time_str:
#                 times.append(None)
#             else:
#                 try:
#                     times.append(float(time_str.strip()))
#                 except ValueError:
#                     times.append(None)
#         return times


# def format_deltas(times):
#     if not times:
#         return
    
#     best = min(t for t in times if t is not None)
#     avg = sum(t for t in times if t is not None) / sum(1 for t in times if t is not None)
    
#     for i, t in enumerate(times):
#         if t is None:
#             print(f"Lap {i+1}: No time")
#             continue
#         if i == 0:
#             delta = 0
#         else:
#             delta = t - times[i - 1] if times[i - 1] is not None else 0
#         sign = "+" if delta >= 0 else "-"
#         print(f"Lap {i+1}: {t:.2f} ({sign}{abs(delta):.2f})")
    
#     print(f"\nBest Lap: {best:.2f}")
#     print(f"Average Lap: {avg:.2f}")


# times = get_racer_times('lap_times.csv', 'EpicX18 GT9')
# format_deltas(times)


"""
Time Delta Analysis (best vs. worst, and lap-to-lap comparisons)

Consistency Metrics (variance, standard deviation)

Time Loss Identification (look for laps where you lose significant time)

Performance Drop-off (start vs. end of sessions)

Lap Segmentation (breaking down the track into sectors)

Time Trends (tracking improvement or plateau)

Statistical Analysis (distribution of lap times, average vs best lap time comparison)



-----
1. Time Delta Analysis
Compare best vs. worst lap times.

Compare lap-to-lap times.

2. Consistency Metrics
Calculate variance and standard deviation.

3. Time Loss Identification
Identify laps where significant time loss occurred.

4. Performance Drop-off
Analyze the start vs. end of sessions.

5. Lap Segmentation
Break down lap times by sectors (assuming you have sector data).

6. Time Trends
Track improvement or plateaus.

7. Statistical Analysis
Analyze lap time distribution and comparison with the best lap.



------
Explanation:
get_racer_times: Extracts lap times from the CSV file for a specific racer.

format_deltas: Computes the time difference (delta) between each lap.

consistency_metrics: Calculates variance and standard deviation to measure consistency.

time_loss_identification: Highlights laps where there is significant time loss.

performance_dropoff: Measures performance drop-off by comparing the first and last lap times.

lap_segmentation: (Placeholder) Breaks down lap times by sectors if sector data is available.

time_trends: Analyzes if performance is improving or plateauing based on lap times.

statistical_analysis: Provides statistical analysis like average and best lap time.
"""

import csv
import statistics

# 1. Get Racer Times
def get_racer_times(filename, racer_name):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        if racer_name not in reader.fieldnames:
            print("Racer name not found")
            return []
        
        times = []
        for row in reader:
            time_str = row[racer_name]
            if not time_str:
                times.append(None)
            else:
                try:
                    times.append(float(time_str.strip()))
                except ValueError:
                    times.append(None)
        return times

# 2. Time Delta Analysis
# 2. Time Delta Analysis
def format_deltas(times):
    if not times:
        return
    
    best = min(t for t in times if t is not None)
    avg = sum(t for t in times if t is not None) / sum(1 for t in times if t is not None)
    
    print("\n--- Time Delta Analysis ---")
    
    gain = 0
    reduction = 0
    
    for i, t in enumerate(times):
        if t is None:
            print(f"Lap {i+1}: No time")
            continue
        if i == 0:
            delta = 0
        else:
            delta = t - times[i - 1] if times[i - 1] is not None else 0
        sign = "+" if delta >= 0 else "-"
        print(f"Lap {i+1}: {t:.2f} ({sign}{abs(delta):.2f})")
        
        # Track gain or reduction
        if delta > 0:
            gain += delta  # Accumulating constant gain
        elif delta < 0:
            reduction += abs(delta)  # Accumulating constant reduction
    
    print(f"\nBest Lap: {best:.2f}")
    print(f"Average Lap: {avg:.2f}")
    
    # Analyze constant gain or reduction
    if gain > reduction:
        print(f"Constant Gain: {gain:.2f} seconds")
    elif reduction > gain:
        print(f"Constant Reduction: {reduction:.2f} seconds")
    else:
        print("No clear trend in gain or reduction.")


# 3. Consistency Metrics
def consistency_metrics(times):
    valid_times = [t for t in times if t is not None]
    if len(valid_times) < 2:
        print("Not enough data to calculate consistency.")
        return
    
    variance = statistics.variance(valid_times)
    stddev = statistics.stdev(valid_times)
    
    print("\n--- Consistency Metrics ---")
    print(f"Variance: {variance:.2f}")
    print(f"Standard Deviation: {stddev:.2f}")

# 4. Time Loss Identification
def time_loss_identification(times):
    print("\n--- Time Loss Identification ---")
    thresholds = [0.2, 0.3, 0.4, 0.5]  # List of thresholds
    for i in range(1, len(times)):
        if times[i] and times[i-1]:
            delta = times[i] - times[i-1]
            for threshold in thresholds:
                if abs(delta) > threshold:  # Check if the time difference exceeds the threshold
                    if delta > 0:
                        print(f"Lap {i+1}: Time gained ({delta:.2f}s) compared to previous lap with threshold {threshold}s.")
                    else:
                        print(f"Lap {i+1}: Time lost ({-delta:.2f}s) compared to previous lap with threshold {threshold}s.")

# 5. Performance Drop-off
def performance_dropoff(times):
    start_time = times[0] if times[0] is not None else None
    end_time = times[-1] if times[-1] is not None else None
    if start_time and end_time:
        dropoff = end_time - start_time
        print("\n--- Performance Drop-off ---")
        print(f"Start Time: {start_time:.2f}")
        print(f"End Time: {end_time:.2f}")
        print(f"Performance Drop-off: {dropoff:.2f}")

# 6. Lap Segmentation (Assuming sectors are provided)
def lap_segmentation(sector_times):
    print("\n--- Lap Segmentation ---")
    for lap_num, sectors in enumerate(sector_times, 1):
        total_time = sum(sectors)
        print(f"Lap {lap_num}: Total Time: {total_time:.2f} | Sectors: {sectors}")

# 7. Time Trends
def time_trends(times):
    print("\n--- Time Trends ---")
    best_time = min([t for t in times if t is not None])

    for i, time in enumerate(times):
        if time is not None:
            delta = time - best_time
            delta_str = f"{delta:+.2f}"  # Format the delta with + or - and two decimal places
            print(f"Lap {i+1}: {time:.2f} ({delta_str})")



# 8. Statistical Analysis
def statistical_analysis(times):
    valid_times = [t for t in times if t is not None]
    if len(valid_times) < 2:
        print("Not enough data for statistical analysis.")
        return
    
    avg_time = sum(valid_times) / len(valid_times)
    best_time = min(valid_times)
    
    print("\n--- Statistical Analysis ---")
    print(f"Average Lap Time: {avg_time:.2f}")
    print(f"Best Lap Time: {best_time:.2f}")
    print(f"Distribution of Lap Times: {valid_times}")

# 9. Main function to call all analyses
def analyze_lap_times(filename, racer_name):
    times = get_racer_times(filename, racer_name)
    
    if times:
        format_deltas(times)
        consistency_metrics(times)
        time_loss_identification(times)
        performance_dropoff(times)
        # If you had sector data, you could use lap_segmentation here
        time_trends(times)
        statistical_analysis(times)

# Running the analysis
analyze_lap_times('lap_times.csv', 'Tumelo GT9')
