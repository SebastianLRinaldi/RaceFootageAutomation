import csv
import re
from PyQt6.QtWidgets import QFileDialog

class LapDataParser:
    def __init__(self):
        pass


    def process_and_save_csv(self, raw_data:str):


        from bs4 import BeautifulSoup
        import csv

        soup = BeautifulSoup(raw_data, "html.parser")
        rows = []

        for tr in soup.find_all("tr"):
            row = []
            for td in tr.find_all("td"):
                # Extract all <p> inside <td> as separate lines, join with newline or space
                texts = [p.get_text(strip=True) for p in td.find_all("p")]
                cell_text = "\n".join(texts) if texts else td.get_text(strip=True)
                row.append(cell_text)
            rows.append(row)

        with open("output.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

