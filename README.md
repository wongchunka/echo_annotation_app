# Echo Annotation App

A web application for annotating ultrasound (echo) reports. This application allows users to upload CSV files containing ultrasound report data and annotate various cardiac conditions.

## Features

- **Upload CSV Files**: Upload CSV files containing ultrasound report data
- **View Reports**: Browse all reports in a paginated table view
- **Annotate Reports**: Annotate each report for various cardiac conditions
- **Track Progress**: Automatically track annotation progress with timestamps

## Required CSV Format

The CSV file should contain the following columns:
- `Patient_Name`: Name of the patient
- `Echo_Path`: Path to the echo file
- `Echo_Diagnosis`: Diagnosis text from the echo report
- `Ecg_Path`: Path to the ECG file
- Annotation fields (can be 0, 1, or other values):
  - `LVH`
  - `LV dilated`
  - `LV impaired`
  - `RV dilated`
  - `RV impaired`
  - `AS mod severe`
  - `AR mod severe`
  - `MS mod severe`
  - `MR mod severe`
  - `TR mod severe`
  - `Pericardial effusion`

A new column `last_update` will be automatically added to track when each record was last annotated.

## Installation

1. Clone this repository:
```
git clone <repository-url>
cd echo_annotation_app
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python main.py
```

4. Open your browser and navigate to `http://localhost:8000`

## Workflow

1. **Upload Page**: Upload your CSV file containing ultrasound report data
2. **Table Page**: View all reports, check annotation status, and select reports to annotate
3. **Annotation Page**: View echo and ECG paths, echo diagnosis, and annotate cardiac conditions
   - Choose "Yes" (stored as 1 in CSV)
   - Choose "No" (stored as 0 in CSV)
   - Choose "Unknown" (original value preserved in CSV)

## Notes

- All annotations directly modify the source CSV file
- The last_update column is automatically updated with timestamps when annotations are saved
