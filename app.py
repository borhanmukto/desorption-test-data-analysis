import streamlit as st
import pandas as pd
import io
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# ==================== HELPER FUNCTIONS ====================
def find_columns(df):
    """Return (timestamp_col, response_col) with smart fallbacks."""
    cols = list(df.columns)
    
    # Locate Timestamp column
    ts_col = "Timestamp" if "Timestamp" in cols else cols[0]
    
    # Locate Response/Value column
    if "Response_raw" in cols:
        resp_col = "Response_raw"
    elif "Response" in cols:
        resp_col = "Response"
    else:
        # Fallback: use 2nd column if available, else 1st
        resp_col = cols[1] if len(cols) > 1 else cols[0]
        
    return ts_col, resp_col

def numeric_from_response(series):
    """Extract the numeric part from strings like '821.7       g' -> 821.7 (float)."""
    # Convert to string, remove commas, strip whitespace
    s = series.astype(str).str.replace(",", "", regex=False).str.strip()
    # Extract number (handles integers and decimals, positive/negative)
    num = s.str.extract(r'([+-]?\d+(?:\.\d+)?)')[0]
    return pd.to_numeric(num, errors="coerce")

# ==================== STREAMLIT UI ====================
st.set_page_config(page_title="Desorption Test Data Analysis Tool", page_icon="📊")

# Centered Title
st.markdown("<h1 style='text-align: center;'>📊 Desorption Test Data Analysis Tool</h1>", unsafe_allow_html=True)

# Centered Developer Credit & LinkedIn Link
st.markdown("<div style='text-align: center; color: grey; font-size: small; margin-top: -10px; margin-bottom: 20px;'>Developed by Borhan Uddin Rabbani || <a href='https://www.linkedin.com/in/borhan-uddin-rabbani/' target='_blank'>Connect on LinkedIn</a></div>", unsafe_allow_html=True)

# Centered Instruction Text (UPDATED TEXT)
st.markdown("<p style='text-align: center;'>Upload your CSV file to clean, average, and consolidate data.</p>", unsafe_allow_html=True)

# --- SIDEBAR CONFIGURATION ---
st.sidebar.header("Configuration")

# 1. User Input: Time Interval
time_to_average_sec = st.sidebar.number_input(
    "Average Interval (seconds)", 
    min_value=1, 
    value=60, 
    step=1,
    help="The time window to group and average data points."
)

# 2. User Input: File Upload (UPDATED TO CSV)
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

resample_freq = f"{time_to_average_sec}s"

# --- MAIN LOGIC ---

if uploaded_file is not None:
    st.info(f"File uploaded: `{uploaded_file.name}`. Click 'Process Data' to start.")
    
    if st.button("Process Data", type="primary"):
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        try:
            status_text.text("Reading CSV file... (This may take a moment for large files)")
            
            # UPDATED: Read CSV instead of Excel
            # We assume standard comma separation. If your CSVs use semicolons, add sep=';'
            df = pd.read_csv(uploaded_file)
            
            all_processed_data = []
            
            # Since CSV has no sheets, we treat the whole file as one block
            # Identify columns
            ts_col, resp_col = find_columns(df)
            
            # --- FILTERING GARBAGE DATA ---
            garbage_keywords = "Balance|OHAUS|User|Project|Weighing|Gross|Net|Tare|/"
            mask_garbage = df[resp_col].astype(str).str.contains(garbage_keywords, case=False, na=False, regex=True)
            df = df[~mask_garbage].copy()
            
            # Convert Timestamp and Values
            df["Timestamp"] = pd.to_datetime(df[ts_col], errors="coerce")
            df["Value"] = numeric_from_response(df[resp_col])
            
            # Drop invalid rows
            df = df.dropna(subset=["Timestamp", "Value"]).copy()
            
            if df.empty:
                st.warning("The CSV file resulted in no valid data after cleaning.")
            else:
                # Resample Logic
                df = df.set_index("Timestamp").sort_index()
                avg_data = df["Value"].resample(resample_freq).mean().to_frame(name="Value_avg")
                
                # Fill nulls with neighbor mean
                s = avg_data["Value_avg"]
                neighbor_mean = (s.ffill() + s.bfill()) / 2.0
                avg_data["Value_avg_filled"] = s.where(~s.isna(), neighbor_mean)
                
                # Final formatting
                out_sheet = avg_data.reset_index()
                # Use filename as source since there are no sheet names
                out_sheet["Source_Sheet"] = uploaded_file.name 
                all_processed_data.append(out_sheet)
                
                # Update progress to 100%
                progress_bar.progress(1.0)
                status_text.text("Processing complete.")

            # --- FINAL OUTPUT GENERATION ---
            if all_processed_data:
                final_df = pd.concat(all_processed_data, ignore_index=True)
                
                if "Timestamp" in final_df.columns:
                    final_df = final_df.sort_values("Timestamp")
                
                # Preview Data
                st.write("### Preview of Processed Data")
                st.dataframe(final_df.head(50))
                st.caption(f"Total Rows: {len(final_df)}")
                
                # Convert to Excel in memory
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    final_df.to_excel(writer, sheet_name='Combined_Data', index=False)
                
                output.seek(0)
                
                # Download Button
                st.success("Processing Complete!")
                st.download_button(
                    label="Download Processed Excel",
                    data=output,
                    file_name=f"averaged_{time_to_average_sec}_second_data.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error("No valid data was processed. Please check the input file format.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a CSV file in the sidebar to begin.")
