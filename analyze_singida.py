import csv
from collections import Counter, defaultdict
import re
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

# Read the CSV file
data = []
with open('Singida.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append(row)

# 1. Count procedures and calculate demographics
procedure_count = len(data)

# Calculate gender distribution
male_count = sum(1 for row in data if row.get('Gender', '').strip() == 'Male')
female_count = sum(1 for row in data if row.get('Gender', '').strip() == 'Female')

# Calculate mean age
ages = []
for row in data:
    try:
        age = int(row.get('Age', 0))
        if age > 0:  # Only include valid ages
            ages.append(age)
    except:
        pass
mean_age = sum(ages) / len(ages) if ages else 0

# 2. Extract conditions
# In Singida.csv, there's a single "Conditions" column (not separated by eye)
# We'll count conditions generally, and also track by the operated eye
all_conditions = []
conditions_by_sex = defaultdict(list)
conditions_by_age = defaultdict(list)
conditions_male_re = []
conditions_male_le = []
conditions_female_re = []
conditions_female_le = []
conditions_age_19_40_re = []
conditions_age_19_40_le = []
conditions_age_41_60_re = []
conditions_age_41_60_le = []
conditions_age_61_80_re = []
conditions_age_61_80_le = []
conditions_age_81plus_re = []
conditions_age_81plus_le = []

# Age groups
def get_age_group(age_str):
    try:
        age = int(age_str)
        if age <= 18:
            return "0-18"
        elif age <= 40:
            return "19-40"
        elif age <= 60:
            return "41-60"
        elif age <= 80:
            return "61-80"
        else:
            return "81+"
    except:
        return "Unknown"

# Known procedure names to exclude from conditions
PROCEDURE_NAMES = {'SICS', 'EXCISION', 'INCISION & DRAINAGE', 'BTRP', 'ICCE', 
                   'IRIS REPOSITION', 'TPR', 'EVISCERATION', 'EPILATION', 
                   'FOREIGN BODY REMOVAL'}

for row in data:
    gender = row['Gender']
    age = row['Age']
    age_group = get_age_group(age)
    operated_eye = row.get('Operated Eye', '').strip().upper()
    
    # Extract conditions from the single Conditions column
    conditions_str = row.get('Conditions', '').strip()
    
    if conditions_str:
        # Split by comma (conditions are comma-separated like "Cataracts, Pterygium")
        for cond in re.split(r',', conditions_str):
            cond = cond.strip()
            # Filter out procedure names and empty strings
            if cond and cond.upper() not in PROCEDURE_NAMES:
                all_conditions.append(cond)
                conditions_by_sex[gender].append(cond)
                conditions_by_age[age_group].append(cond)
                
                # Assign to operated eye (since we don't have separate RE/LE condition columns)
                if operated_eye == 'RE':
                    if gender == 'Male':
                        conditions_male_re.append(cond)
                    elif gender == 'Female':
                        conditions_female_re.append(cond)
                    # Track by age group
                    if age_group == '19-40':
                        conditions_age_19_40_re.append(cond)
                    elif age_group == '41-60':
                        conditions_age_41_60_re.append(cond)
                    elif age_group == '61-80':
                        conditions_age_61_80_re.append(cond)
                    elif age_group == '81+':
                        conditions_age_81plus_re.append(cond)
                elif operated_eye == 'LE':
                    if gender == 'Male':
                        conditions_male_le.append(cond)
                    elif gender == 'Female':
                        conditions_female_le.append(cond)
                    # Track by age group
                    if age_group == '19-40':
                        conditions_age_19_40_le.append(cond)
                    elif age_group == '41-60':
                        conditions_age_41_60_le.append(cond)
                    elif age_group == '61-80':
                        conditions_age_61_80_le.append(cond)
                    elif age_group == '81+':
                        conditions_age_81plus_le.append(cond)

# Count frequencies
condition_freq_general = Counter(all_conditions)
condition_freq_by_sex = {sex: Counter(conditions) for sex, conditions in conditions_by_sex.items()}
condition_freq_by_age = {age_group: Counter(conditions) for age_group, conditions in conditions_by_age.items()}
condition_freq_male_re = Counter(conditions_male_re)
condition_freq_male_le = Counter(conditions_male_le)
condition_freq_female_re = Counter(conditions_female_re)
condition_freq_female_le = Counter(conditions_female_le)
condition_freq_age_19_40_re = Counter(conditions_age_19_40_re)
condition_freq_age_19_40_le = Counter(conditions_age_19_40_le)
condition_freq_age_41_60_re = Counter(conditions_age_41_60_re)
condition_freq_age_41_60_le = Counter(conditions_age_41_60_le)
condition_freq_age_61_80_re = Counter(conditions_age_61_80_re)
condition_freq_age_61_80_le = Counter(conditions_age_61_80_le)
condition_freq_age_81plus_re = Counter(conditions_age_81plus_re)
condition_freq_age_81plus_le = Counter(conditions_age_81plus_le)

# For the general table, we'll show conditions by operated eye
condition_freq_right_eye = Counter()
condition_freq_left_eye = Counter()

for row in data:
    operated_eye = row.get('Operated Eye', '').strip().upper()
    conditions_str = row.get('Conditions', '').strip()
    
    if conditions_str:
        for cond in re.split(r',', conditions_str):
            cond = cond.strip()
            if cond and cond.upper() not in PROCEDURE_NAMES:
                if operated_eye == 'RE':
                    condition_freq_right_eye[cond] += 1
                elif operated_eye == 'LE':
                    condition_freq_left_eye[cond] += 1

# Count procedures by eye
right_eye_procedures = []
left_eye_procedures = []
all_procedures = []

for row in data:
    procedure = row.get('Surgical Procedure Perfomed', '').strip()
    operated_eye = row.get('Operated Eye', '').strip().upper()
    
    if procedure and operated_eye:
        # Split by comma or plus sign
        procedures = re.split(r'[,+]', procedure)
        for proc in procedures:
            proc_clean = proc.strip().upper()
            # Filter out eye indicators and procedure modifiers
            if proc_clean and proc_clean not in ['RE', 'LE', 'PTERYGIUM', '']:
                all_procedures.append(proc_clean)
                if operated_eye == 'RE':
                    right_eye_procedures.append(proc_clean)
                elif operated_eye == 'LE':
                    left_eye_procedures.append(proc_clean)

procedure_freq_right = Counter(right_eye_procedures)
procedure_freq_left = Counter(left_eye_procedures)
procedure_freq_all = Counter(all_procedures)

# 3. Extract VA data for operated eye
va_data = []
patient_improvements = []

for row in data:
    operated_eye = row.get('Operated Eye', '').strip().upper()
    
    if operated_eye == 'RE':
        preop_va = row.get('PREOP VA - Right Eye\t', '').strip()
        day1_va = row.get('1 Day Post OP VA - Right Eye', '').strip()
        week2_va = row.get('2 Weeks Post OP VA - Right Eye', '').strip()
        month1_va = row.get('1 Month Post OP VA - Right Eye', '').strip()
    elif operated_eye == 'LE':
        preop_va = row.get('PREOP VA - Left Eye\t', '').strip()
        day1_va = row.get('1 Day Post OP VA - Left Eye', '').strip()
        week2_va = row.get('2 Weeks Post OP VA - Left Eye', '').strip()
        month1_va = row.get('1 Month Post OP VA - Left Eye', '').strip()
    else:
        continue  # Skip if we can't determine the eye
    
    # Only include if we have at least preop data
    if preop_va:
        va_data.append({
            'preop': preop_va,
            'day1': day1_va,
            'week2': week2_va,
            'month1': month1_va
        })
        
        # Store patient info for improvement tracking (use 1 month if available, else 2 weeks)
        final_va = month1_va if month1_va else week2_va
        if preop_va and final_va:
            # Handle BOM in column name
            patient_id_key = '\ufeffPatient Number' if '\ufeffPatient Number' in row else 'Patient Number'
            patient_improvements.append({
                'patient_id': row[patient_id_key],
                'name': row['Patient Name'],
                'preop_va': preop_va,
                'week2_va': week2_va,
                'month1_va': month1_va,
                'final_va': final_va
            })

# Count VA frequencies
preop_va_count = Counter([v['preop'] for v in va_data if v['preop']])
day1_va_count = Counter([v['day1'] for v in va_data if v['day1']])
week2_va_count = Counter([v['week2'] for v in va_data if v['week2']])
month1_va_count = Counter([v['month1'] for v in va_data if v['month1']])

# Define VA ordinal order (best to worst)
def get_va_order(va):
    """Return numeric order for VA values (lower = better vision)"""
    va_order = {
        '6/6': 1,
        '6/9': 2,
        '6/12': 3,
        '6/18': 4,
        '6/24': 5,
        '6/36': 6,
        '6/60': 7,
        'CF1M': 8,
        'CF2M': 9,
        'CF3M': 10,
        'CF4M': 11,
        'CF5M': 12,
        'CFN': 13,
        'HM': 14,
        'PL': 15,
        'NPL': 16
    }
    return va_order.get(va, 99)  # Unknown values go to end

# Get all unique VA values and sort by ordinal order
all_va_values = sorted(
    set(list(preop_va_count.keys()) + list(day1_va_count.keys()) + 
        list(week2_va_count.keys()) + list(month1_va_count.keys())),
    key=get_va_order
)

# Generate markdown report
markdown = f"""# Singida Eye Camp Report
## The Mo Dewji Foundation

---

## 1. Number of Procedures Done

**Total Procedures: {procedure_count}**

**Gender Distribution:**
- Male: {male_count} ({male_count/procedure_count*100:.2f}%)
- Female: {female_count} ({female_count/procedure_count*100:.2f}%)

**Mean Age: {mean_age:.1f} years**

---

## 2. Frequency Distribution of Conditions

### 2.1 General Frequency Distribution

**Note:** Condition counts are based on the operated eye for each patient. Since the Singida dataset has a single "Conditions" column (not separated by eye), conditions are assigned to the eye that was operated on. Some individuals had more than one diagnosis (e.g., "Cataracts, Pterygium"), and each condition is counted separately.

| Condition | Right Eye | Left Eye | Total |
|----------|-----------|----------|-------|
"""

# Get all unique conditions
all_unique_conditions = sorted(set(list(condition_freq_right_eye.keys()) + list(condition_freq_left_eye.keys())))

total_right = sum(condition_freq_right_eye.values())
total_left = sum(condition_freq_left_eye.values())
total_all = sum(condition_freq_general.values())

# Sort by total frequency (descending)
sorted_conditions = sorted(all_unique_conditions, key=lambda x: condition_freq_general.get(x, 0), reverse=True)

for condition in sorted_conditions:
    right_count = condition_freq_right_eye.get(condition, 0)
    left_count = condition_freq_left_eye.get(condition, 0)
    total_count = condition_freq_general.get(condition, 0)
    
    right_pct = (right_count / total_right * 100) if total_right > 0 else 0
    left_pct = (left_count / total_left * 100) if total_left > 0 else 0
    total_pct = (total_count / total_all * 100) if total_all > 0 else 0
    
    markdown += f"| {condition} | {right_count} ({right_pct:.2f}%) | {left_count} ({left_pct:.2f}%) | {total_count} ({total_pct:.2f}%) |\n"

# Add total row
markdown += f"| **Total** | **{total_right} (100.00%)** | **{total_left} (100.00%)** | **{total_all} (100.00%)** |\n"

# Generate PNG chart for top conditions
top_10_conditions = sorted_conditions[:10]
conditions_labels = [c.replace(' ', '\n') if len(c) > 15 else c for c in top_10_conditions]
conditions_values = [condition_freq_general.get(c, 0) for c in top_10_conditions]

plt.figure(figsize=(12, 6))
plt.bar(conditions_labels, conditions_values, color='#ff6b6b', edgecolor='#7C0000', linewidth=1.5)
plt.title('Top 10 Conditions by Total Frequency', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Condition', fontsize=11)
plt.ylabel('Frequency', fontsize=11)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('singida_chart_conditions_top10.png', dpi=300, bbox_inches='tight')
plt.close()

markdown += """

#### Chart: Top 10 Conditions Distribution

![Top 10 Conditions](singida_chart_conditions_top10.png)
"""

markdown += """

### 2.2 Procedure Counts

| Procedure | Right Eye | Left Eye | Total |
|-----------|-----------|----------|-------|
"""

# Get all unique procedures
all_unique_procedures = sorted(set(list(procedure_freq_right.keys()) + list(procedure_freq_left.keys())))

total_right_proc = sum(procedure_freq_right.values())
total_left_proc = sum(procedure_freq_left.values())
total_all_proc = sum(procedure_freq_all.values())

# Sort by total frequency (descending)
sorted_procedures = sorted(all_unique_procedures, key=lambda x: procedure_freq_all.get(x, 0), reverse=True)

for procedure in sorted_procedures:
    right_count = procedure_freq_right.get(procedure, 0)
    left_count = procedure_freq_left.get(procedure, 0)
    total_count = procedure_freq_all.get(procedure, 0)
    
    right_pct = (right_count / total_right_proc * 100) if total_right_proc > 0 else 0
    left_pct = (left_count / total_left_proc * 100) if total_left_proc > 0 else 0
    total_pct = (total_count / total_all_proc * 100) if total_all_proc > 0 else 0
    
    markdown += f"| {procedure} | {right_count} ({right_pct:.2f}%) | {left_count} ({left_pct:.2f}%) | {total_count} ({total_pct:.2f}%) |\n"

# Add total row
markdown += f"| **Total** | **{total_right_proc} (100.00%)** | **{total_left_proc} (100.00%)** | **{total_all_proc} (100.00%)** |\n"

# Generate PNG chart for procedures
proc_labels = [p.replace(' ', '\n') if len(p) > 15 else p for p in sorted_procedures]
proc_values = [procedure_freq_all.get(p, 0) for p in sorted_procedures]

plt.figure(figsize=(10, 6))
plt.bar(proc_labels, proc_values, color='#4ecdc4', edgecolor='#2a8a84', linewidth=1.5)
plt.title('Procedures by Total Count', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Procedure', fontsize=11)
plt.ylabel('Count', fontsize=11)
plt.xticks(rotation=45, ha='right', fontsize=9)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('singida_chart_procedures.png', dpi=300, bbox_inches='tight')
plt.close()

markdown += """

#### Chart: Procedures Distribution

![Procedures Distribution](singida_chart_procedures.png)
"""

markdown += """

---

## 3. Visual Acuity (VA) Analysis for Operated Eye

### 3.1 VA Distribution Across Time Points

| Visual Acuity | Pre-op | 1 Day Post-op | 2 Weeks Post-op | 1 Month Post-op | Change (Pre-op to 1 Month) |
|---------------|--------|---------------|-----------------|------------------|---------------------------|
"""

total_preop = sum(preop_va_count.values())
total_day1 = sum(day1_va_count.values())
total_week2 = sum(week2_va_count.values())
total_month1 = sum(month1_va_count.values())

for va in all_va_values:
    preop_count = preop_va_count.get(va, 0)
    day1_count = day1_va_count.get(va, 0)
    week2_count = week2_va_count.get(va, 0)
    month1_count = month1_va_count.get(va, 0)
    
    preop_pct = (preop_count / total_preop * 100) if total_preop > 0 else 0
    day1_pct = (day1_count / total_day1 * 100) if total_day1 > 0 else 0
    week2_pct = (week2_count / total_week2 * 100) if total_week2 > 0 else 0
    month1_pct = (month1_count / total_month1 * 100) if total_month1 > 0 else 0
    
    # Calculate change from preop to 1 month (prefer 1 month, fallback to 2 weeks)
    final_count = month1_count if month1_count > 0 else week2_count
    if preop_count > 0 and final_count > 0:
        change = ((final_count - preop_count) / preop_count * 100)
        change_str = f"{change:+.2f}%"
    elif preop_count == 0 and final_count > 0:
        change_str = "+∞%"
    elif preop_count > 0 and final_count == 0:
        change_str = "-100%"
    else:
        change_str = "N/A"
    
    markdown += f"| {va} | {preop_count} ({preop_pct:.2f}%) | {day1_count} ({day1_pct:.2f}%) | {week2_count} ({week2_pct:.2f}%) | {month1_count} ({month1_pct:.2f}%) | {change_str} |\n"

markdown += f"\n**Total Patients with Pre-op VA: {total_preop}**\n"
markdown += f"**Total Patients with 1 Day Post-op VA: {total_day1}**\n"
markdown += f"**Total Patients with 2 Weeks Post-op VA: {total_week2}**\n"
markdown += f"**Total Patients with 1 Month Post-op VA: {total_month1}**\n"

# Calculate improvements and find top 10
def get_va_score(va):
    """Convert VA to numeric score (lower = better vision)"""
    va_scores = {
        '6/6': 1, '6/9': 2, '6/12': 3, '6/18': 4, '6/24': 5, '6/36': 6, '6/60': 7,
        'CF1M': 8, 'CF2M': 9, 'CF3M': 10, 'CF4M': 11, 'CF5M': 12, 'CFN': 13,
        'HM': 14, 'PL': 15, 'NPL': 16
    }
    return va_scores.get(va, 99)

# Calculate improvement for each patient (use 1 month if available, else 2 weeks)
for patient in patient_improvements:
    preop_score = get_va_score(patient['preop_va'])
    final_score = get_va_score(patient['final_va'])
    improvement = preop_score - final_score  # Positive = improvement
    patient['improvement'] = improvement
    patient['achieved_6_6'] = (patient['final_va'] == '6/6')

# Sort: first by achieved 6/6, then by improvement (descending)
patient_improvements.sort(key=lambda x: (not x['achieved_6_6'], -x['improvement']))

# Get top 10
top_10_patients = patient_improvements[:10]

markdown += """

### 3.2 Top 10 Patients with Highest Improvement

| Patient ID | Patient Name | Pre-op VA | 2 Weeks Post-op VA | 1 Month Post-op VA |
|------------|--------------|-----------|---------------------|---------------------|
"""

for patient in top_10_patients:
    month1_display = patient['month1_va'] if patient['month1_va'] else 'N/A'
    markdown += f"| {patient['patient_id']} | {patient['name']} | {patient['preop_va']} | {patient['week2_va']} | {month1_display} |\n"

markdown += """

---

## 4. Conditions Analysis by Gender and Age

### 4.1 Frequency Distribution of Conditions by Gender

| Condition | Male - RE | Male - LE | Male - Total | Female - RE | Female - LE | Female - Total | Overall Total |
|-----------|-----------|-----------|--------------|-------------|-------------|----------------|---------------|
"""

# Get all unique conditions
all_conditions_for_gender = sorted(set(
    list(condition_freq_male_re.keys()) + 
    list(condition_freq_male_le.keys()) +
    list(condition_freq_female_re.keys()) +
    list(condition_freq_female_le.keys())
))

total_male_re = sum(condition_freq_male_re.values())
total_male_le = sum(condition_freq_male_le.values())
total_male = total_male_re + total_male_le
total_female_re = sum(condition_freq_female_re.values())
total_female_le = sum(condition_freq_female_le.values())
total_female = total_female_re + total_female_le
total_all_gender = total_male + total_female

# Sort by total frequency (descending)
sorted_conditions_gender = sorted(all_conditions_for_gender, 
                                  key=lambda x: (condition_freq_male_re.get(x, 0) + 
                                                condition_freq_male_le.get(x, 0) +
                                                condition_freq_female_re.get(x, 0) +
                                                condition_freq_female_le.get(x, 0)), 
                                  reverse=True)

for condition in sorted_conditions_gender:
    male_re_count = condition_freq_male_re.get(condition, 0)
    male_le_count = condition_freq_male_le.get(condition, 0)
    male_total = male_re_count + male_le_count
    female_re_count = condition_freq_female_re.get(condition, 0)
    female_le_count = condition_freq_female_le.get(condition, 0)
    female_total = female_re_count + female_le_count
    overall_total = male_total + female_total
    
    male_re_pct = (male_re_count / total_male_re * 100) if total_male_re > 0 else 0
    male_le_pct = (male_le_count / total_male_le * 100) if total_male_le > 0 else 0
    male_total_pct = (male_total / total_male * 100) if total_male > 0 else 0
    female_re_pct = (female_re_count / total_female_re * 100) if total_female_re > 0 else 0
    female_le_pct = (female_le_count / total_female_le * 100) if total_female_le > 0 else 0
    female_total_pct = (female_total / total_female * 100) if total_female > 0 else 0
    overall_pct = (overall_total / total_all_gender * 100) if total_all_gender > 0 else 0
    
    markdown += f"| {condition} | {male_re_count} ({male_re_pct:.2f}%) | {male_le_count} ({male_le_pct:.2f}%) | {male_total} ({male_total_pct:.2f}%) | {female_re_count} ({female_re_pct:.2f}%) | {female_le_count} ({female_le_pct:.2f}%) | {female_total} ({female_total_pct:.2f}%) | {overall_total} ({overall_pct:.2f}%) |\n"

# Add total row
markdown += f"| **Total** | **{total_male_re} (100.00%)** | **{total_male_le} (100.00%)** | **{total_male} (100.00%)** | **{total_female_re} (100.00%)** | **{total_female_le} (100.00%)** | **{total_female} (100.00%)** | **{total_all_gender} (100.00%)** |\n"

# Generate PNG chart for gender comparison
top_10_gender_conditions = sorted_conditions_gender[:10]
gender_labels = [c.replace(' ', '\n') if len(c) > 12 else c for c in top_10_gender_conditions]
male_values = [condition_freq_male_re.get(c, 0) + condition_freq_male_le.get(c, 0) for c in top_10_gender_conditions]
female_values = [condition_freq_female_re.get(c, 0) + condition_freq_female_le.get(c, 0) for c in top_10_gender_conditions]

x = range(len(gender_labels))
width = 0.35

plt.figure(figsize=(14, 6))
plt.bar([i - width/2 for i in x], male_values, width, label='Male', color='#95e1d3', edgecolor='#5a8a7f', linewidth=1.5)
plt.bar([i + width/2 for i in x], female_values, width, label='Female', color='#f38181', edgecolor='#c45a5a', linewidth=1.5)
plt.title('Top 10 Conditions: Male vs Female', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Condition', fontsize=11)
plt.ylabel('Frequency', fontsize=11)
plt.xticks(x, gender_labels, rotation=45, ha='right', fontsize=9)
plt.legend(fontsize=10)
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('singida_chart_gender_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

markdown += """

#### Chart: Top 10 Conditions by Gender Comparison

![Gender Comparison](singida_chart_gender_comparison.png)
"""

markdown += """

### 4.2 Frequency Distribution of Conditions by Age Groups

**Methodology:** Patients were categorized into four age groups based on their age at the time of the eye camp: 19-40 years (young adults), 41-60 years (middle-aged), 61-80 years (older adults), and 81+ years (elderly). Conditions were assigned to the operated eye for each patient, since the dataset has a single "Conditions" column. This allows for comparison of condition prevalence across different age demographics. The analysis includes all condition occurrences, meaning if a patient had multiple conditions (e.g., "Cataracts, Pterygium"), each condition was counted separately.

#### Chart: Top 10 Conditions by Age Group Comparison

"""

# Generate PNG chart for age group comparison
top_10_age_conditions = sorted_conditions_gender[:10]  # Use same top 10 as gender
age_labels = [c.replace(' ', '\n') if len(c) > 12 else c for c in top_10_age_conditions]

age_19_40_values = [condition_freq_age_19_40_re.get(c, 0) + condition_freq_age_19_40_le.get(c, 0) for c in top_10_age_conditions]
age_41_60_values = [condition_freq_age_41_60_re.get(c, 0) + condition_freq_age_41_60_le.get(c, 0) for c in top_10_age_conditions]
age_61_80_values = [condition_freq_age_61_80_re.get(c, 0) + condition_freq_age_61_80_le.get(c, 0) for c in top_10_age_conditions]
age_81plus_values = [condition_freq_age_81plus_re.get(c, 0) + condition_freq_age_81plus_le.get(c, 0) for c in top_10_age_conditions]

x = range(len(age_labels))
width = 0.2

plt.figure(figsize=(16, 7))
plt.bar([i - 1.5*width for i in x], age_19_40_values, width, label='19-40 years', color='#a8e6cf', edgecolor='#5a8a7f', linewidth=1.5)
plt.bar([i - 0.5*width for i in x], age_41_60_values, width, label='41-60 years', color='#ffd3b6', edgecolor='#cc9a7a', linewidth=1.5)
plt.bar([i + 0.5*width for i in x], age_61_80_values, width, label='61-80 years', color='#ffaaa5', edgecolor='#cc7a7a', linewidth=1.5)
plt.bar([i + 1.5*width for i in x], age_81plus_values, width, label='81+ years', color='#d4a5ff', edgecolor='#8a7acc', linewidth=1.5)
plt.title('Top 10 Conditions by Age Group Comparison', fontsize=14, fontweight='bold', pad=20)
plt.xlabel('Condition', fontsize=11)
plt.ylabel('Frequency', fontsize=11)
plt.xticks(x, age_labels, rotation=45, ha='right', fontsize=9)
plt.legend(fontsize=10, loc='upper right')
plt.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('singida_chart_age_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

markdown += """![Age Group Comparison](singida_chart_age_comparison.png)
"""

# Write to file
with open('singida_report.md', 'w', encoding='utf-8') as f:
    f.write(markdown)

print("Report generated successfully!")

