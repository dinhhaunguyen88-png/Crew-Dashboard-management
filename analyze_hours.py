
import csv
import sys
import io

# Force UTF-8 for stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_time(time_str):
    """Convert HH:MM to decimal hours"""
    try:
        parts = time_str.split(':')
        if len(parts) == 2:
            return float(parts[0]) + float(parts[1]) / 60
        return 0.0
    except:
        return 0.0

def get_status(hours):
    """Return status based on 1000h limit"""
    if hours > 950:
        return "Critical"
    elif hours > 850:
        return "Warning"
    else:
        return "Normal"

def analyze():
    filename = "RolCrTotReport 28Feb26.csv"
    data = []

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except UnicodeDecodeError:
        with open(filename, 'r', encoding='latin1') as f:
            reader = csv.reader(f)
            rows = list(reader)

    # Skip first 5 lines of header
    # Check if Line 5 has data (ID should be digit)
    start_idx = 0
    for i, row in enumerate(rows):
        if len(row) > 0 and row[0].isdigit():
            start_idx = i
            break
            
    if start_idx == 0:
        # Fallback if detection fails, use hardcoded 5 based on peek
        start_idx = 5

    for row in rows[start_idx:]:
        if len(row) < 5: continue
        
        try:
            crew_id = row[0]
            name = row[1]
            h_28 = parse_time(row[3])
            h_12m = parse_time(row[4])
            
            data.append({
                'id': crew_id,
                'name': name,
                'hours_28': h_28,
                'hours_12m': h_12m,
                'raw_28': row[3],
                'raw_12m': row[4]
            })
        except Exception as e:
            continue

    # --- REPORT 1: Top 20 28-Day ---
    print("\n### Bảng 1: Top 20 High-Intensity Crew (Rolling 28 Days)")
    print("| Rank | ID | Name | Flight Hours (28-Day) |")
    print("|---|---|---|---|")
    
    sorted_28 = sorted(data, key=lambda x: x['hours_28'], reverse=True)[:20]
    for i, item in enumerate(sorted_28, 1):
        print(f"| {i} | {item['id']} | {item['name']} | {item['raw_28']} ({item['hours_28']:.2f}) |")

    # --- REPORT 2: Top 20 12-Month ---
    print("\n### Bảng 2: Top 20 High-Intensity Crew (Rolling 12 Months)")
    print("| Rank | ID | Name | Flight Hours (12-Month) | Status |")
    print("|---|---|---|---|---|")
    
    sorted_12m = sorted(data, key=lambda x: x['hours_12m'], reverse=True)[:20]
    for i, item in enumerate(sorted_12m, 1):
        status = get_status(item['hours_12m'])
        # Add emoji or formatting? User asked for table.
        # Markdown bold for critical
        status_display = f"**{status}**" if status == "Critical" else status
        print(f"| {i} | {item['id']} | {item['name']} | {item['raw_12m']} ({item['hours_12m']:.2f}) | {status_display} |")

    # --- SUMMARY ---
    critical_count = sum(1 for x in data if get_status(x['hours_12m']) == "Critical")
    warning_count = sum(1 for x in data if get_status(x['hours_12m']) == "Warning")
    
    print("\n### Tổng kết")
    print(f"- **Critical (>950h):** {critical_count} nhân viên")
    print(f"- **Warning (>850h):** {warning_count} nhân viên")

if __name__ == "__main__":
    analyze()
