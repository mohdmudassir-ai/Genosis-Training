import streamlit as st
import requests


# ==========================================
# CONFIGURATION
# ==========================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Student Management System",
    page_icon=None,
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

    /* =====================================
       MAIN PAGE
       ===================================== */

    .stApp {
        background-color: #F4FAF9;
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }


    /* =====================================
       TOP HEADER
       ===================================== */

    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
        border-bottom: 1px solid #D8EEEA !important;
    }

    header[data-testid="stHeader"] button {
        color: #176B63 !important;
    }


    /* =====================================
       SIDEBAR
       ===================================== */

    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #D8EEEA !important;
    }

    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    .sidebar-title {
        font-size: 22px;
        font-weight: 700;
        color: #155E59 !important;
        margin-bottom: 25px;
    }

    section[data-testid="stSidebar"] label {
        color: #334155 !important;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] p {
        color: #64748B !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #D8EEEA !important;
    }


    /* =====================================
       PAGE TITLE
       ===================================== */

    .page-title {
        font-size: 36px;
        font-weight: 700;
        color: #155E59 !important;
        margin-bottom: 5px;
    }

    .page-subtitle {
        font-size: 15px;
        color: #64748B !important;
        margin-bottom: 32px;
    }


    /* =====================================
       SECTION TITLE
       ===================================== */

    .section-title {
        font-size: 27px;
        font-weight: 650;
        color: #155E59 !important;
        margin-bottom: 22px;
    }


    /* =====================================
       DASHBOARD CARDS
       ===================================== */

    .stat-card {
        background-color: #FFFFFF;
        border: 1px solid #D8EEEA;
        border-radius: 12px;
        padding: 24px;
        min-height: 105px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(21, 94, 89, 0.07);
    }

    .stat-label {
        font-size: 14px;
        font-weight: 600;
        color: #64748B !important;
        margin-bottom: 9px;
    }

    .stat-value {
        font-size: 31px;
        font-weight: 700;
        color: #0F766E !important;
        line-height: 1.2;
    }


    /* =====================================
       FORM BOX
       ===================================== */

    .form-box {
        background-color: #FFFFFF;
        border: 1px solid #D8EEEA;
        border-radius: 12px;
        padding: 28px;
        margin-bottom: 20px;
        box-shadow: 0 4px 14px rgba(21, 94, 89, 0.05);
    }


    /* =====================================
       INPUTS
       ===================================== */

    .stTextInput input,
    .stNumberInput input {
        background-color: #FFFFFF !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 7px !important;
        color: #334155 !important;
    }

    .stTextInput input:focus,
    .stNumberInput input:focus {
        border-color: #14B8A6 !important;
        box-shadow: 0 0 0 1px #14B8A6 !important;
    }

    .stTextInput label,
    .stNumberInput label {
        color: #334155 !important;
        font-weight: 600 !important;
    }


    /* =====================================
       BUTTONS
       ===================================== */

    .stButton > button {
        background-color: #0F766E !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 7px !important;
        font-weight: 600 !important;
        min-height: 42px;
        padding: 8px 20px;
    }

    .stButton > button:hover {
        background-color: #0D6861 !important;
        color: #FFFFFF !important;
    }


    /* =====================================
       FORM SUBMIT BUTTON
       ===================================== */

    .stFormSubmitButton > button {
        background-color: #0F766E !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 7px !important;
        font-weight: 600 !important;
        min-height: 42px;
        padding: 8px 20px;
    }

    .stFormSubmitButton > button:hover {
        background-color: #0D6861 !important;
        color: #FFFFFF !important;
    }


    /* =====================================
       TABLE
       ===================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #D8EEEA;
        border-radius: 9px;
        overflow: hidden;
        background-color: #FFFFFF;
    }


    /* =====================================
       ALERTS
       ===================================== */

    div[data-testid="stAlert"] {
        border-radius: 8px;
    }


    /* =====================================
       DARK MODE
       ===================================== */

    @media (prefers-color-scheme: dark) {

        .stApp {
            background-color: #182C2B !important;
        }

        header[data-testid="stHeader"] {
            background-color: #213C3A !important;
            border-bottom: 1px solid #355A56 !important;
        }

        header[data-testid="stHeader"] button {
            color: #CDEDEA !important;
        }

        section[data-testid="stSidebar"] {
            background-color: #213C3A !important;
            border-right: 1px solid #355A56 !important;
        }

        .sidebar-title {
            color: #D5F1EE !important;
        }

        section[data-testid="stSidebar"] label {
            color: #D5F1EE !important;
        }

        section[data-testid="stSidebar"] p {
            color: #A8C6C2 !important;
        }

        section[data-testid="stSidebar"] hr {
            border-color: #355A56 !important;
        }

        .page-title {
            color: #D5F1EE !important;
        }

        .page-subtitle {
            color: #A8C6C2 !important;
        }

        .section-title {
            color: #D5F1EE !important;
        }

        .stat-card {
            background-color: #213C3A !important;
            border: 1px solid #355A56 !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.16);
        }

        .stat-label {
            color: #A8C6C2 !important;
        }

        .stat-value {
            color: #5ED6C8 !important;
        }

        .form-box {
            background-color: #213C3A !important;
            border: 1px solid #355A56 !important;
        }

        .stTextInput input,
        .stNumberInput input {
            background-color: #294744 !important;
            border-color: #496965 !important;
            color: #E5F5F3 !important;
        }

        .stTextInput label,
        .stNumberInput label {
            color: #D5F1EE !important;
        }

        [data-testid="stDataFrame"] {
            background-color: #213C3A !important;
            border-color: #355A56 !important;
        }
    }

</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown(
    '<div class="sidebar-title">Student Management</div>',
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Add Student",
        "View Students",
        "Update Student",
        "Delete Student"
    ]
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Student Management System"
)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="page-title">Student Management System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Manage student records using FastAPI and Supabase'
    '</div>',
    unsafe_allow_html=True
)


# ==========================================
# DASHBOARD
# ==========================================

if menu == "Dashboard":

    st.markdown(
        '<div class="section-title">Dashboard</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    try:

        response = requests.get(
            f"{API_URL}/students"
        )

        if response.status_code == 200:

            students = response.json()["data"]

            total_students = len(students)

            if total_students > 0:

                total_marks = sum(
                    student["marks"]
                    for student in students
                )

                average_marks = (
                    total_marks / total_students
                )

                highest_marks = max(
                    student["marks"]
                    for student in students
                )

            else:

                average_marks = 0
                highest_marks = 0


            with col1:

                st.markdown(
                    f'<div class="stat-card">'
                    f'<div class="stat-label">Total Students</div>'
                    f'<div class="stat-value">{total_students}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )


            with col2:

                st.markdown(
                    f'<div class="stat-card">'
                    f'<div class="stat-label">Average Marks</div>'
                    f'<div class="stat-value">'
                    f'{average_marks:.2f}'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )


            with col3:

                st.markdown(
                    f'<div class="stat-card">'
                    f'<div class="stat-label">Highest Marks</div>'
                    f'<div class="stat-value">'
                    f'{highest_marks}'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        else:

            st.error(
                "Could not connect to backend."
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Backend is not running. Start FastAPI first."
        )


# ==========================================
# ADD STUDENT
# ==========================================

elif menu == "Add Student":

    st.markdown(
        '<div class="section-title">Add Student</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="form-box">',
        unsafe_allow_html=True
    )

    with st.form("add_student_form"):

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Student Name",
                placeholder="Enter student name"
            )

        with col2:

            course = st.text_input(
                "Course",
                placeholder="Enter course"
            )

        marks = st.number_input(
            "Marks",
            min_value=0,
            max_value=100,
            value=0
        )

        submit = st.form_submit_button(
            "Add Student"
        )

        if submit:

            if name.strip() == "":

                st.warning(
                    "Please enter student name."
                )

            elif course.strip() == "":

                st.warning(
                    "Please enter course."
                )

            else:

                try:

                    response = requests.post(
                        f"{API_URL}/students",
                        params={
                            "name": name,
                            "course": course,
                            "marks": marks
                        }
                    )

                    if response.status_code == 200:

                        st.success(
                            "Student added successfully!"
                        )

                    else:

                        st.error(
                            f"Failed to add student. "
                            f"Status: {response.status_code}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Backend is not running."
                    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ==========================================
# VIEW STUDENTS
# ==========================================

elif menu == "View Students":

    st.markdown(
        '<div class="section-title">All Students</div>',
        unsafe_allow_html=True
    )

    if st.button("Refresh Students"):

        st.rerun()

    try:

        response = requests.get(
            f"{API_URL}/students"
        )

        if response.status_code == 200:

            students = response.json()["data"]

            if len(students) == 0:

                st.info(
                    "No students found."
                )

            else:

                st.write(
                    f"Total Students: **{len(students)}**"
                )

                st.dataframe(
                    students,
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.error(
                "Failed to retrieve students."
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Backend is not running."
        )


# ==========================================
# UPDATE STUDENT
# ==========================================

elif menu == "Update Student":

    st.markdown(
        '<div class="section-title">Update Student</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Enter the Student ID and new information."
    )

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "New Name",
            placeholder="Enter new name"
        )

    with col2:

        course = st.text_input(
            "New Course",
            placeholder="Enter new course"
        )

    marks = st.number_input(
        "New Marks",
        min_value=0,
        max_value=100,
        value=0
    )

    if st.button("Update Student"):

        if name.strip() == "":

            st.warning(
                "Please enter a name."
            )

        elif course.strip() == "":

            st.warning(
                "Please enter a course."
            )

        else:

            try:

                response = requests.put(
                    f"{API_URL}/students/{student_id}",
                    params={
                        "name": name,
                        "course": course,
                        "marks": marks
                    }
                )

                if response.status_code == 200:

                    st.success(
                        "Student updated successfully!"
                    )

                else:

                    st.error(
                        f"Failed to update student. "
                        f"Status: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Backend is not running."
                )


# ==========================================
# DELETE STUDENT
# ==========================================

elif menu == "Delete Student":

    st.markdown(
        '<div class="section-title">Delete Student</div>',
        unsafe_allow_html=True
    )

    st.warning(
        "Deleting a student cannot be undone."
    )

    student_id = st.number_input(
        "Student ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Student"):

        try:

            response = requests.delete(
                f"{API_URL}/students/{student_id}"
            )

            if response.status_code == 200:

                st.success(
                    "Student deleted successfully!"
                )

            else:

                st.error(
                    f"Failed to delete student. "
                    f"Status: {response.status_code}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Backend is not running."
            )