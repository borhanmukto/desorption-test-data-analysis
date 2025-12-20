📊 Desorption Test Data Analysis Tool
=====================================

This application is a post-processing tool designed to clean, consolidate, and average raw data collected from Ohaus scales (or similar devices). It takes raw Excel files—often containing multiple sheets and "garbage" text (like "Tare", "Gross", etc.)—and outputs a clean, time-averaged dataset ready for analysis.

📋 Prerequisites
----------------

Before running this application, ensure you have **Python (version 3.8 or higher)** installed.

*   Download from [python.org](https://www.python.org/downloads/).
    
*   _Note: During installation, it is highly recommended to check the box "Add Python to PATH"._
    

⚙️ Installation
---------------

1.  **Create the Project Folder**
    
    *   Create a new folder on your computer (e.g., DataAnalyzer).
        
    *   Save the Python script provided in this package inside that folder as **analyzer.py**.
        
2.  Bash`pip install streamlit pandas openpyxl xlsxwriter`⚠️ If the command above fails (Command not found)If you see an error saying 'pip' is not recognized, it means Python was not added to your system PATH. Use this command instead:Bash`py -m pip install streamlit pandas openpyxl xlsxwriter`
    
    *   Open your Command Prompt (Windows) or Terminal (Mac/Linux).
        
    *   Navigate to your folder (e.g., cd Desktop/DataAnalyzer).
        
    *   Run the following command:
        

🚀 How to Run
-------------

1.  Open your Command Prompt/Terminal.
    
2.  Navigate to the folder where you saved analyzer.py.
    
3.  Bash`streamlit run analyzer.py`⚠️ If the command above failsIf your computer does not recognize streamlit, use the Python launcher directly:Bash`py -m streamlit run analyzer.py`
    
4.  A new tab should automatically open in your default web browser.
    

📖 User Guide
-------------

### 1\. Configuration (Sidebar)

*   **Average Interval (seconds):** The time window for grouping data.
    
    *   _Example:_ If set to 60, the app will take all readings within every minute and calculate a single average value. This smoothes out noise.
        
*   **Upload Excel File:** Drag and drop your raw .xlsx or .xls file here.
    

### 2\. Processing Logic

Once you click **"Process Data"**, the tool automatically performs the following:

1.  **Merges Sheets:** It reads every sheet in your Excel file.
    
2.  **Cleans Garbage:** It removes lines containing keywords like "Balance", "Net", "Tare", "Gross", or headers that interrupt the data stream.
    
3.  **Standardizes Numbers:** It extracts pure numbers from text fields (e.g., converts "821.7 g" to 821.7).
    
4.  **Resamples:** It averages the data based on your chosen time interval.
    
5.  **Fills Gaps:** If a small gap in data exists, it fills it using the average of the surrounding neighbors.
    

### 3\. Output

*   **Preview:** You will see a table of the first 50 rows of processed data.
    
*   **Download:** Click the **"Download Processed Excel"** button to save the final clean file.
    

⚠️ Troubleshooting
------------------

**"No valid data was processed":**

*   Check your input file. The tool looks for columns named Timestamp and Response (or Response\_raw). If your headers are different, the tool tries to guess (using the 1st and 2nd columns), but standard headers work best.
    

**"File is open" error:**

*   Ensure the Excel file you are trying to upload is **closed** on your computer before uploading it.
    

### Developed with Python & Streamlit
