
import streamlit as st
import pandas as pd
import os
from io import BytesIO
import datetime

# Set page configuration
st.set_page_config(page_title="Data Transformer", layout='wide')

# Add title and description with custom styling
st.markdown("""
    <style>
        .title {
            font-size: 50px;
            font-weight: bold;
            font-family:serif;
            color: rgb(182, 6, 123);
            text-align: center;
            padding: 20px;
            border-radius: 10px;
        }
        .description {
            font-size: 18px;
            text-align: center;
            color: #555555;
            margin-bottom: 30px;
            font-style:italic;
        }
        .file-metadata {
            font-size: 25px;
            color:rgb(89, 1, 92);
            margin-bottom: 20px;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease;
        }
        .button:hover {
            background-color: #45a049;
        }
        .warning {
            color: #ff9800;
        }
        .success {
            color: #4caf50;
        }
        .error {
            color:rgb(60, 0, 68);
        }
        .section {
            margin-top: 20px;
        }
        .section-title {
            font-size: 22px;
            color: #3f51b5;
        }
    </style>
    <div class="title">📊 Data Transformer 🚀</div>
    <div class="description">Transform and clean your data effortlessly with built-in data visualization and export options! 🌟</div>
""", unsafe_allow_html=True)

# File uploader with multiple file selection
uploaded_files = st.file_uploader("📤 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Display file metadata and suggestions for cleaning
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        file_size = file.size / 1024  # File size in KB
        upload_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Read file depending on extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        # Display file information and preview
        st.markdown(f"### **File Name:** {file.name} 📄")
        st.markdown(f"**File Size:** {file_size:.2f} KB 💾")
        st.markdown(f"**Uploaded on:** {upload_time} ⏰")
        st.markdown(f"**File Type:** {file_ext.upper()} 📝")

        st.markdown("### **Preview of Data** 🔍")
        st.dataframe(df.head())

        # Auto suggestions for cleaning based on data quality
        with st.expander(f"⚠️ **Data Quality Suggestions for {file.name}**", expanded=True):
            st.markdown(f"### ⚠️ **Data Quality Suggestions for {file.name}**")
            if df.isnull().sum().sum() > 0:
                st.warning("⚠️ This file contains missing values!")
            if df.duplicated().any():
                st.warning("⚠️ This file contains duplicate rows!")
            
            st.write("**Suggested Actions:** 📝")
            st.write("- Remove duplicates.")
            st.write("- Fill or drop missing values.")

        # Data cleaning options section in expandable format
        with st.expander(f"🧹 **Data Cleaning Options for {file.name}**", expanded=True):
            st.markdown(f"### 🧹 **Data Cleaning Options for {file.name}**")
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🧼 Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicated rows removed.")

            with col2:
                if st.button(f"💧 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values have been filled.")

        # Column selection for further analysis
        with st.expander(f"🔧 **Select Columns to Convert for {file.name}**", expanded=True):
            st.markdown(f"### 🔧 **Select Columns to Convert for {file.name}**")
            columns = st.multiselect("🖋️ Choose Columns", df.columns, default=df.columns)
            df = df[columns]
            st.write("You have selected the following columns: ✅")
            st.write(df.columns)

        # Visualization options
        with st.expander(f"📈 **Data Visualization for {file.name}**", expanded=False):
            st.markdown(f"### 📈 **Data Visualization for {file.name}**")
            if st.checkbox(f"Show Bar Chart for {file.name}"):
                # Ensure the dataframe contains numeric columns before plotting
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:  # Check if there are numeric columns to plot
                    st.bar_chart(df[numeric_cols].iloc[:, :2])  # Plot the first two numeric columns
                else:
                    st.warning("⚠️ No numeric columns available for visualization.")

        # File conversion options
        with st.expander(f"🔄 **Convert {file.name} to Another Format**", expanded=True):
            st.markdown(f"### 🔄 **Convert {file.name} to Another Format**")
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"🚀 Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)
                st.download_button(
                    label=f"Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                    use_container_width=True
                )

        # Compare two uploaded files (if applicable)
        if len(uploaded_files) > 1:
            st.markdown("### **🔍 File Comparison (If Multiple Files Uploaded)**")
            compare_file = st.selectbox("Select another file to compare:", uploaded_files)
            if compare_file:
                compare_ext = os.path.splitext(compare_file.name)[-1].lower()
                if compare_ext == ".csv":
                    compare_df = pd.read_csv(compare_file)
                elif compare_ext == ".xlsx":
                    compare_df = pd.read_excel(compare_file)

                if df.equals(compare_df):
                    st.success(f"✅ The files **{file.name}** and **{compare_file.name}** are identical.")
                else:
                    st.error(f"❌ The files **{file.name}** and **{compare_file.name}** are different.")

    st.success("🎉 All files processed successfully.")
