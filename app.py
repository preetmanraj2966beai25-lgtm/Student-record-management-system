import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Student Record Management System", page_icon="📚", layout="wide"
)

# Initialize Session State for Data Storage
if "students" not in st.session_state:
  st.session_state.students = pd.DataFrame(
      columns=["ID", "Name", "Age", "Grade", "Email"]
  )
  # Pre-populate with sample records
  st.session_state.students.loc[0] = [
      "S001",
      "Alice Smith",
      20,
      "A",
      "alice@example.com",
  ]
  st.session_state.students.loc[1] = [
      "S002",
      "Bob Jones",
      22,
      "B",
      "bob@example.com",
  ]

st.title("📚 Student Record Management System (CRUD)")
st.markdown("Manage student profiles easily using Streamlit and Pandas.")

# Sidebar Navigation
menu = ["View & Search", "Add Student", "Update Student", "Delete Student"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# ==========================================
# 1. READ (View & Search Records)
# ==========================================
if choice == "View & Search":
  st.subheader("📋 All Student Records")

  if st.session_state.students.empty:
    st.info("No student records available.")
  else:
    # Search Filter
    search_query = st.text_input("🔍 Search by Name or ID", "")

    if search_query:
      filtered_df = st.session_state.students[
          st.session_state.students["Name"].str.contains(
              search_query, case=False, na=False
          )
          | st.session_state.students["ID"].str.contains(
              search_query, case=False, na=False
          )
      ]
      st.write(f"Showing results for: **{search_query}**")
      st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    else:
      st.dataframe(
          st.session_state.students, use_container_width=True, hide_index=True
      )

    st.metric(
        label="Total Students", value=len(st.session_state.students)
    )

# ==========================================
# 2. CREATE (Add New Student)
# ==========================================
elif choice == "Add Student":
  st.subheader("➕ Add a New Student Record")

  with st.form("add_student_form"):
    col1, col2 = st.columns(2)
    with col1:
      student_id = st.text_input("Student ID (e.g., S003)")
      name = st.text_input("Full Name")
      age = st.number_input("Age", min_value=5, max_value=100, value=18)
    with col2:
      grade = st.selectbox("Grade", ["A", "B", "C", "D", "F"])
      email = st.text_input("Email Address")

    submit_button = st.form_submit_button("Save Student")

    if submit_button:
      if not student_id or not name:
        st.warning("⚠️ Student ID and Full Name are required fields!")
      elif student_id in st.session_state.students["ID"].values:
        st.error(f"❌ Student ID '{student_id}' already exists!")
      else:
        new_row = pd.DataFrame(
            [[student_id, name, age, grade, email]],
            columns=["ID", "Name", "Age", "Grade", "Email"],
        )
        st.session_state.students = pd.concat(
            [st.session_state.students, new_row], ignore_index=True
        )
        st.success(f"✅ Student '{name}' added successfully!")

# ==========================================
# 3. UPDATE (Modify Student Record)
# ==========================================
elif choice == "Update Student":
  st.subheader("✏️ Update Student Information")

  if st.session_state.students.empty:
    st.info("No student records available to update.")
  else:
    student_ids = st.session_state.students["ID"].tolist()
    selected_id = st.selectbox(
        "Select Student ID to Modify", student_ids
    )

    # Fetch current values
    student_data = st.session_state.students.loc[
        st.session_state.students["ID"] == selected_id
    ].iloc[0]

    with st.form("update_student_form"):
      new_name = st.text_input("Full Name", value=student_data["Name"])
      new_age = st.number_input(
          "Age", min_value=5, max_value=100, value=int(student_data["Age"])
      )

      grades_list = ["A", "B", "C", "D", "F"]
      current_grade_index = (
          grades_list.index(student_data["Grade"])
          if student_data["Grade"] in grades_list
          else 0
      )
      new_grade = st.selectbox(
          "Grade", grades_list, index=current_grade_index
      )
      new_email = st.text_input("Email Address", value=student_data["Email"])

      update_button = st.form_submit_button("Update Record")

      if update_button:
        st.session_state.students.loc[
            st.session_state.students["ID"] == selected_id,
            ["Name", "Age", "Grade", "Email"],
        ] = [new_name, new_age, new_grade, new_email]
        st.success(f"✅ Student ID '{selected_id}' updated successfully!")

# ==========================================
# 4. DELETE (Remove Student Record)
# ==========================================
elif choice == "Delete Student":
  st.subheader("🗑️ Delete Student Record")

  if st.session_state.students.empty:
    st.info("No student records available to delete.")
  else:
    student_ids = st.session_state.students["ID"].tolist()
    selected_id = st.selectbox("Select Student ID to Delete", student_ids)

    # Show details of record to be deleted
    student_row = st.session_state.students.loc[
        st.session_state.students["ID"] == selected_id
    ]
    st.write("Record to be deleted:")
    st.dataframe(student_row, use_container_width=True, hide_index=True)

    if st.button("Delete Permanently", type="primary"):
      st.session_state.students = st.session_state.students[
          st.session_state.students["ID"] != selected_id
      ].reset_index(drop=True)
      st.success(f"✅ Student ID '{selected_id}' has been deleted.")
      st.rerun()