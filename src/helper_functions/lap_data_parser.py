from bs4 import BeautifulSoup
from PyQt6.QtWidgets import QFileDialog


class LapDataParser:
    def __init__(self):
        pass

    def extract_name(self, cell):
        return cell.split(':', 1)[-1].strip() if ':' in cell else cell.strip()

    def process_raw_html(self, raw_data:str):
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

        header_row = rows[0]
        cleaned_header = [header_row[0]] + [self.extract_name(cell) for cell in header_row[1:]]
        rows[0] = cleaned_header
        return rows


