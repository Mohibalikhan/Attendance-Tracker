import streamlit as st
import pandas as pd
import datetime
from database import mark_attendance, get_attendance, reset_attendance  # ✅ Import functions
from io import BytesIO

# ✅ Load Student Data from Excel
@st.cache_data
def load_students():
    return pd.read_excel("students.xlsx", dtype={"Roll No": str})

students_df = load_students()

st.title("📌 Attendance Tracker App")

# ✅ Select multiple students by roll number
selected_roll_numbers = st.multiselect("Select Roll Numbers", students_df["Roll No"].astype(str))

# ✅ Display selected students
if selected_roll_numbers:
    selected_students = students_df[students_df["Roll No"].astype(str).isin(selected_roll_numbers)]
    selected_text = ", ".join([f"<span style='color:green;'>{row['Name']} (Roll No: {row['Roll No']})</span>" for _, row in selected_students.iterrows()])
    st.markdown(f"#### ✅ Selected Students: {selected_text}", unsafe_allow_html=True)

# ✅ Select Date
date = st.date_input("Select Date", datetime.date.today())

# ✅ Get current attendance records
data = get_attendance()
attendance_df = pd.DataFrame(data, columns=["Roll No", "Name", "Date", "Status"])
attendance_df["Roll No"] = attendance_df["Roll No"].astype(str)

# ✅ Mark Attendance
if st.button("Mark Attendance"):
    already_marked = []
    newly_marked_present = []
    newly_marked_absent = []

    # ✅ Mark "Present" for selected students
    for roll_number in selected_roll_numbers:
        student_name = students_df.loc[students_df["Roll No"].astype(str) == roll_number, "Name"].values[0]

        if not attendance_df[(attendance_df["Roll No"] == roll_number) & (attendance_df["Date"] == str(date))].empty:
            already_marked.append(f"{student_name} (Roll No: {roll_number})")
        else:
            mark_attendance(student_name, str(date), "Present")
            newly_marked_present.append(f"{student_name} (Roll No: {roll_number})")

    # ✅ Mark "Absent" for unselected students
    absent_students = students_df[~students_df["Roll No"].astype(str).isin(selected_roll_numbers)]
    for _, row in absent_students.iterrows():
        roll_number = str(row["Roll No"])
        student_name = row["Name"]

        if attendance_df[(attendance_df["Roll No"] == roll_number) & (attendance_df["Date"] == str(date))].empty:
            mark_attendance(student_name, str(date), "Absent")
            newly_marked_absent.append(f"{student_name} (Roll No: {roll_number})")

    # ✅ Show Messages
    if newly_marked_present:
        st.success(f"✅ Attendance marked as 'Present' for {len(newly_marked_present)} student(s): " + ", ".join(newly_marked_present))
    
    if newly_marked_absent:
        st.info(f"ℹ️ Attendance marked as 'Absent' for {len(newly_marked_absent)} student(s): " + ", ".join(newly_marked_absent))
    
    if already_marked:
        st.warning(f"⚠️ These students already have attendance for {date}: " + ", ".join(already_marked))

# ✅ Display Attendance Records
st.subheader("📋 Attendance Records")
data = get_attendance()
df = pd.DataFrame(data, columns=["Roll No", "Name", "Date", "Status"])
df["Roll No"] = df["Roll No"].astype(str)

# ✅ Highlight selected rows in the table
def highlight_selected(s):
    return ['background-color: lightgreen' if str(s["Roll No"]) in selected_roll_numbers else '' for _ in s]

if not df.empty:
    styled_df = df.style.apply(highlight_selected, axis=1)
    st.dataframe(styled_df)

# ✅ Download Attendance as Excel File
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="Attendance", index=False)
    output.seek(0)
    return output

if not df.empty:
    excel_data = convert_df_to_excel(df)
    st.download_button(
        label="📥 Download Attendance as Excel",
        data=excel_data,
        file_name="subject_attendance.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ✅ Reset Attendance Button
if st.button("Reset Attendance Data ❌"):
    reset_attendance()
    st.warning("⚠️ All attendance records have been deleted!")
    st.rerun()  # ✅ Refresh the app after reset
