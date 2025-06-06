from PyQt6.QtWidgets import QFileDialog
import csv
import statistics 

# 1. Get Racer Times
def get_racer_times(racer_name):
    filename, _ = QFileDialog.getSaveFileName(None, "Save CSV", "outputFiles", "CSV Files (*.csv);;All Files (*)")
    if filename:
    
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



# 2. Time Delta Analysis (Delta From Prev Lap)
def pre_lap_deltas(times):
    if not times:
        return
    
    for i, t in enumerate(times):
        if t is None:
            print(f"Lap {i+1}: No time")
            continue
        if i == 0:
            delta = 0
        else:
            delta = t - times[i - 1] if times[i - 1] is not None else 0
        sign = "+" if delta >= 0 else "-"
        print(f"Lap {i+1}: {t:.3f} ({sign}{abs(delta):.3f})")


# 3. Consistency Metrics
def consistency_metrics(times):
    valid_times = [t for t in times if t is not None]
    if len(valid_times) < 2:
        print("Not enough data to calculate consistency.")
        return
    
    variance = statistics.variance(valid_times)
    stddev = statistics.stdev(valid_times)
    
    print("\n--- Consistency Metrics ---")
    print(f"Variance: {variance:.3f}")
    print(f"Standard Deviation: {stddev:.3f}")



# 7. Time Delta Analysis (Deltas From Best Lap)
def best_lap_deltas(times):
    print("\n--- Deltas From Best Lap ---")
    best_time = min([t for t in times if t is not None])
    lap_times_with_best_time_deltas = []

    for i, time in enumerate(times):
        if time is not None:
            delta = time - best_time
            delta_str = f"{delta:+.3f}"  # Format the delta with + or - and two decimal places
            time_formated = f"{time:.3f}"
            print(f"Lap {i+1}: {time_formated} ({delta_str})")
            lap_times_with_best_time_deltas.append((time_formated, delta_str))

    return lap_times_with_best_time_deltas



"""
Percent Time within X% of Best Lap — how many laps fall 
within 1%, 2%, 5% of your best? Consistency in quality, not just variance.
"""
def percent_within_x_percent(lap_times, thresholds=(1, 2, 5)):
    best = min(lap_times)
    results = {}
    for x in thresholds:
        max_allowed = best * (1 + x / 100)
        count = sum(1 for t in lap_times if t <= max_allowed)
        percentage = 100 * count / len(lap_times)
        results[f"within_{x}_percent"] = round(percentage, 1)
    return results



"""
Pace Consistency Index — ratio of best lap to average lap or median 
lap to quantify “how close to your best you usually are.”
"""
def pace_consistency_index(lap_times):
    best = min(lap_times)
    mean = sum(lap_times) / len(lap_times)
    median = sorted(lap_times)[len(lap_times) // 2]

    pci_mean = best / mean
    pci_median = best / median

    return {
        "PCI_mean": round(pci_mean, 3),
        "PCI_median": round(pci_median, 3)
    }