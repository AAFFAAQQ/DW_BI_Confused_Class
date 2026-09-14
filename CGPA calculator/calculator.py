import streamlit as st

# =========================================
# GPA & CGPA CALCULATOR - Streamlit App
# (Marks-based version: user enters marks, we convert to grade + grade points)
# =========================================

st.set_page_config(page_title="GPA & CGPA Calculator", page_icon="🎓")
st.title("🎓 GPA & CGPA Calculator")


# ---- Helper function: convert marks (0-100) into (letter grade, grade points) ----
def marks_to_grade(marks):
    """
    Standard university grading scale.
    Change these ranges if your university uses a different scale.
    """
    if marks >= 85:
        return "A", 4.0
    elif marks >= 80:
        return "A-", 3.7
    elif marks >= 75:
        return "B+", 3.3
    elif marks >= 71:
        return "B", 3.0
    elif marks >= 68:
        return "B-", 2.7
    elif marks >= 64:
        return "C+", 2.3
    elif marks >= 61:
        return "C", 2.0
    elif marks >= 58:
        return "C-", 1.7
    elif marks >= 54:
        return "D+", 1.3
    elif marks >= 50:
        return "D", 1.0
    else:
        return "F", 0.0


# ---- STEP 1: Previous academic record ----
st.subheader("Previous Record")
has_previous = st.checkbox("I have a previous CGPA")

previous_points = 0.0
previous_credits = 0.0

if has_previous:
    previous_cgpa = st.number_input("Previous CGPA", min_value=0.0, max_value=4.0, step=0.01)
    previous_credits = st.number_input("Previous total credit hours", min_value=0.0, step=1.0)
    # Convert CGPA back into total quality points so it can be combined later
    previous_points = previous_cgpa * previous_credits

# ---- STEP 2: Current semester subjects ----
st.subheader("This Semester's Subjects")
num_subjects = st.number_input("How many subjects this semester?", min_value=1, step=1, value=1)

current_points = 0.0
current_credits = 0.0

# Store each subject's details so we can display grades after calculation
subjects_data = []

# Create input fields for each subject
for i in range(int(num_subjects)):
    col1, col2 = st.columns(2)
    with col1:
        marks = st.number_input(
            f"Marks (%) - Subject {i + 1}",
            min_value=0.0, max_value=100.0, step=1.0, key=f"marks_{i}"
        )
    with col2:
        credit = st.number_input(
            f"Credit hours - Subject {i + 1}",
            min_value=0.0, step=1.0, key=f"credit_{i}"
        )

    # Convert marks into letter grade + grade points
    letter_grade, grade_points = marks_to_grade(marks)

    current_points += grade_points * credit
    current_credits += credit

    subjects_data.append({
        "subject": f"Subject {i + 1}",
        "marks": marks,
        "credit": credit,
        "grade": letter_grade,
        "points": grade_points
    })

# ---- STEP 3 & 4: Calculate and display results ----
if st.button("Calculate"):
    if current_credits == 0:
        st.error("Total credit hours cannot be zero. Please enter valid credit hours.")
    else:
        # Show grade breakdown for each subject
        st.subheader("Grade Breakdown")
        for s in subjects_data:
            st.write(
                f"**{s['subject']}**: {s['marks']:.0f}% → Grade **{s['grade']}** "
                f"({s['points']} GP) × {s['credit']:.0f} credit hrs"
            )

        gpa = current_points / current_credits
        st.success(f"Your GPA for this semester is: **{gpa:.2f}**")

        total_points = previous_points + current_points
        total_credits = previous_credits + current_credits

        if total_credits > 0:
            cgpa = total_points / total_credits
            st.success(f"Your overall CGPA is: **{cgpa:.2f}**")
            st.info(f"Total credit hours completed: {total_credits:.1f}")