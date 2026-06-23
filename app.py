import streamlit as st
import sqlite3
import pandas as pd

# -------------------------
# DATABASE SETUP
# -------------------------
conn = sqlite3.connect("placement.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    department TEXT,
    cgpa REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS companies(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    hr_email TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT,
    title TEXT,
    package REAL,
    location TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS applications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT,
    job_title TEXT
)
""")

conn.commit()

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("College Placement Portal")

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Dashboard",
        "Student Registration",
        "Company Registration",
        "Post Job",
        "View Jobs",
        "Apply Job",
        "Reports"
    ]
)

# -------------------------
# DASHBOARD
# -------------------------
if menu == "Dashboard":

    st.title("🎓 College Placement Portal")

    students = pd.read_sql_query(
        "SELECT * FROM students", conn)

    companies = pd.read_sql_query(
        "SELECT * FROM companies", conn)

    jobs = pd.read_sql_query(
        "SELECT * FROM jobs", conn)

    applications = pd.read_sql_query(
        "SELECT * FROM applications", conn)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Students", len(students))
    c2.metric("Companies", len(companies))
    c3.metric("Jobs", len(jobs))
    c4.metric("Applications", len(applications))

# -------------------------
# STUDENT REGISTRATION
# -------------------------
elif menu == "Student Registration":

    st.header("Student Registration")

    with st.form("student_form"):

        name = st.text_input("Name")
        email = st.text_input("Email")
        dept = st.text_input("Department")
        cgpa = st.number_input(
            "CGPA",
            min_value=0.0,
            max_value=10.0
        )

        submit = st.form_submit_button("Register")

        if submit:

            cursor.execute("""
            INSERT INTO students
            (name,email,department,cgpa)
            VALUES(?,?,?,?)
            """,
            (name, email, dept, cgpa))

            conn.commit()

            st.success("Student Registered Successfully")

# -------------------------
# COMPANY REGISTRATION
# -------------------------
elif menu == "Company Registration":

    st.header("Company Registration")

    with st.form("company_form"):

        company = st.text_input("Company Name")
        hr = st.text_input("HR Email")

        submit = st.form_submit_button("Register")

        if submit:

            cursor.execute("""
            INSERT INTO companies
            (company_name,hr_email)
            VALUES(?,?)
            """,
            (company, hr))

            conn.commit()

            st.success("Company Registered")

# -------------------------
# JOB POSTING
# -------------------------
elif menu == "Post Job":

    st.header("Post New Job")

    companies = pd.read_sql_query(
        "SELECT company_name FROM companies",
        conn
    )

    if companies.empty:
        st.warning("Register a company first.")
    else:

        company = st.selectbox(
            "Company",
            companies["company_name"]
        )

        title = st.text_input("Job Title")

        package = st.number_input(
            "Package (LPA)",
            min_value=0.0
        )

        location = st.text_input("Location")

        if st.button("Post Job"):

            cursor.execute("""
            INSERT INTO jobs
            (company_name,title,package,location)
            VALUES(?,?,?,?)
            """,
            (company, title, package, location))

            conn.commit()

            st.success("Job Posted Successfully")

# -------------------------
# VIEW JOBS
# -------------------------
elif menu == "View Jobs":

    st.header("Available Jobs")

    jobs = pd.read_sql_query(
        "SELECT * FROM jobs",
        conn
    )

    if jobs.empty:
        st.info("No jobs available.")
    else:
        st.dataframe(jobs)

# -------------------------
# APPLY JOB
# -------------------------
elif menu == "Apply Job":

    st.header("Apply for Job")

    students = pd.read_sql_query(
        "SELECT name FROM students",
        conn
    )

    jobs = pd.read_sql_query(
        "SELECT title FROM jobs",
        conn
    )

    if students.empty or jobs.empty:

        st.warning(
            "Need students and jobs before applying."
        )

    else:

        student = st.selectbox(
            "Student",
            students["name"]
        )

        job = st.selectbox(
            "Job",
            jobs["title"]
        )

        if st.button("Apply"):

            cursor.execute("""
            INSERT INTO applications
            (student_name,job_title)
            VALUES(?,?)
            """,
            (student, job))

            conn.commit()

            st.success("Application Submitted")

# -------------------------
# REPORTS
# -------------------------
elif menu == "Reports":

    st.header("Placement Reports")

    students = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    companies = pd.read_sql_query(
        "SELECT * FROM companies",
        conn
    )

    jobs = pd.read_sql_query(
        "SELECT * FROM jobs",
        conn
    )

    applications = pd.read_sql_query(
        "SELECT * FROM applications",
        conn
    )

    st.subheader("Students")
    st.dataframe(students)

    st.subheader("Companies")
    st.dataframe(companies)

    st.subheader("Jobs")
    st.dataframe(jobs)

    st.subheader("Applications")
    st.dataframe(applications)