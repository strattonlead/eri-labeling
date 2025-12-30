import streamlit as st
import pandas as pd
import os

def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error loading CSV: {e}")
            return None
    return None

def save_data(df, filename):
    try:
        df.to_csv(filename, index=False)
        st.success(f"Saved results to {filename}")
    except Exception as e:
        st.error(f"Error saving data: {e}")

def main():
    st.title("ERI Labeling Tool")

    st.sidebar.header("Configuration")
    labeler_name = st.sidebar.text_input("Labeler Name", value="Anonymous")

    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

    if "current_index" not in st.session_state:
        st.session_state.current_index = 0

    # Persistent storage file
    output_filename = "labeled_data.csv"

    if uploaded_file is not None:
        # Check if we have an existing labeled file to continue from, or load fresh
        # But if the user uploads a new file, we usually want that one.
        # To support "write results directly to the csv file", we should probably
        # use the uploaded file's content, but we can't overwrite the user's local file.
        # We will work with a local copy.

        # Logic: If 'labeled_data.csv' exists and matches the uploaded file schema/length, maybe use it?
        # For simplicity: We load the uploaded file. We check if 'labeled_data.csv' exists.
        # If it does, we can offer to load it instead or merge.
        # But let's keep it simple: Load uploaded file.

        if "df" not in st.session_state:
             st.session_state.df = load_data(uploaded_file)
             # Add columns if they don't exist
             if st.session_state.df is not None:
                 if "ERI_Score" not in st.session_state.df.columns:
                     st.session_state.df["ERI_Score"] = None
                 if "Labeler" not in st.session_state.df.columns:
                     st.session_state.df["Labeler"] = None

    if "df" in st.session_state and st.session_state.df is not None:
        df = st.session_state.df

        # Display Progress
        total_rows = len(df)
        current_idx = st.session_state.current_index

        st.write(f"**Labeling Row {current_idx + 1} of {total_rows}**")

        # Display current row data
        if 0 <= current_idx < total_rows:
            row_data = df.iloc[current_idx]
            st.table(row_data)

            # Labeling Interface
            with st.form("labeling_form"):
                score = st.slider("ERI Score (1-7)", min_value=1, max_value=7, value=4)
                submitted = st.form_submit_button("Save & Next")

                if submitted:
                    # Update DataFrame
                    df.at[current_idx, "ERI_Score"] = score
                    df.at[current_idx, "Labeler"] = labeler_name

                    # Save to disk
                    save_data(df, output_filename)

                    # Move to next
                    if current_idx < total_rows - 1:
                        st.session_state.current_index += 1
                        st.rerun()
                    else:
                        st.success("Labeling Complete!")

        else:
            st.info("No more rows to label.")
            if st.button("Restart"):
                st.session_state.current_index = 0
                st.rerun()

        # Navigation
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("Previous"):
                if st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
                    st.rerun()
        with col2:
             if st.button("Next (Skip)"):
                 if st.session_state.current_index < total_rows - 1:
                     st.session_state.current_index += 1
                     st.rerun()

        # Show Data
        st.subheader("Labeled Data Preview")
        st.dataframe(df)

        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Labeled CSV",
            data=csv,
            file_name="labeled_results.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
