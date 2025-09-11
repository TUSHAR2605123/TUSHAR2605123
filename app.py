import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import hashlib
import pandas as pd
import os
from datetime import datetime

# ------------------------- DATABASE CONNECTION -------------------------
def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql@pranav1",  # Replace with your actual password
        database="smartlearn"
    )

# ------------------------- PASSWORD HASHING -------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------------- HOME PAGE -------------------------
def home():
    st.set_page_config(page_title="Smart Learn Home", layout="wide")
    
    st.markdown("""
        <style>
            .main-title {
                text-align: center;
                font-size: 40px;
                font-weight: bold;
                color: white;
                margin-bottom: 0px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title"> 👩‍🎓 Welcome to Smart Learn 📘</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.image("C:\\Users\\Shree\\Downloads\\Smart Learn Logo Design.png", width=600 )
        st.markdown("###### Developed by @pranav_awasare")
    with col2:
        st.write("🌟 This is a platform for students to learn and share knowledge.")
        st.write("🔑 You can **login**, 📝 **register**, 👤 **update your profile**, 📋 **view student lists**, ✍️ **write blogs**, and more.")
        st.write("📌 Use the sidebar to navigate through the application.")
        st.write("🚀 Feel free to explore the features and functionalities of Smart Learn.")
        st.write("📚 **Features:**")
        st.write("- User Authentication (Login/Register)")
        st.write("- Profile Management (View/Update Profile)")
        st.write("- Student List (View All Students)")
        st.write("- Blog Writing (Create/Edit/Delete Blogs)")
        st.write("- Search Functionality (Search Blogs/Students)")
        st.write("📞 For any assistance, please contact support.")
        st.write("🙏 Thank you for using Smart Learn! 🎉")


# ------------------------- LOGIN FORM -------------------------
def login_form():
    st.set_page_config(page_title="Smart Learn Login", layout="wide")

    
    st.markdown("""
        <style>
            .main-title {
                text-align: center;
                font-size: 40px;
                font-weight: bold;
                color: white;
                margin-bottom: 0px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">Smart Learn 📘</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔑 Learn Login")
        email=st.text_input("Email")
    with col1:
        password = st.text_input("Password", type='password')

    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter both email and password.")
            return

        connection = create_db_connection()
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        cursor.execute("SELECT * FROM users WHERE email=%s AND password_hash=%s", (email, hashed_password))
        user = cursor.fetchone()
        connection.close()

        if user:
            st.success("✅ Logged in successfully!")
            st.session_state.logged_in = True
            st.session_state.user_email = email
        else:
            st.error("❌ Invalid email or password")

# ------------------------- REGISTER FORM -------------------------
def register_form():
    st.set_page_config(page_title="Smart Learn Registration", layout="wide")
    st.markdown("""
        <style>
            .main-title {
                text-align: center;
                font-size: 40px;
                font-weight: bold;
                color: white;
                margin-bottom: 0px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title">Smart Learn 📘</h1>', unsafe_allow_html=True)
    st.markdown("### 📝 Registration")

    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name")
        email = st.text_input("Email")
    with col2:
        last_name = st.text_input("Last Name")
        mobile = st.text_input("Mobile Number")

    address = st.text_input("Address")

    col3, col4 = st.columns(2)
    with col3:
        degree = st.text_input("Degree")
        college = st.text_input("College")
    with col4:
        passyear = st.text_input("Passout Year")
        university = st.text_input("University")

    col5, col6 = st.columns(2)
    with col5:
        password = st.text_input("Password", type='password')
    with col6:
        confirm_password = st.text_input("Confirm Password", type='password')

    if st.button("Register"):
        if not (first_name and last_name and email and password and confirm_password):
            st.warning("Please fill all required fields.")
            return

        if password != confirm_password:
            st.error("Passwords do not match!")
            return

        connection = create_db_connection()
        cursor = connection.cursor()

        # Check for existing user
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            st.warning("User already exists with this email.")
            connection.close()
            return

        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, mobile_number, address, degree, college, passout_year, university, password_hash)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, mobile, address, degree, college, passyear, university, hashed_password))

        connection.commit()
        cursor.close()
        connection.close()

        st.success("✅ Registered successfully! You can now login.")



# Student List Show from database
def student_list():
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT first_name, last_name, email, mobile_number FROM users")
    students = cursor.fetchall()
    cursor.close()
    connection.close()

    if students:
        df = pd.DataFrame(students, columns=["First Name", "Last Name", "Email", "Mobile Number"],index=range(1, len(students)+1))
        st.write("### 👥 Student List")
        st.dataframe(df)
    else:
        st.write("No students found.")

def profile():
    if "logged_in" in st.session_state and st.session_state.logged_in:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT first_name, last_name, email, mobile_number, address, degree, college, passout_year, university FROM users WHERE email=%s", (st.session_state.user_email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            st.markdown("### 👤 My Profile")
            st.write("Welcome! Here are your profile details:")
            st.write(f"**First Name:** {user[0]}")
            st.write(f"**Last Name:** {user[1]}")
            st.write(f"**Email:** {user[2]}")
            st.write(f"**Mobile Number:** {user[3]}")
            st.write(f"**Address:** {user[4]}")
            st.write(f"**Degree:** {user[5]}")
            st.write(f"**College:** {user[6]}")
            st.write(f"**Passout Year:** {user[7]}")
            st.write(f"**University:** {user[8]}")
            if st.button("Edit Profile"):
                st.session_state["edit_mode"] = True
        else:
            st.error("User not found.")
    else:
        st.warning("### 🚪 Please login to view your profile.")

def edit_profile():
    if "logged_in" in st.session_state and st.session_state.logged_in:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT first_name, last_name, email, mobile_number, address, degree, college, passout_year, university FROM users WHERE email=%s", (st.session_state.user_email,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user:
            st.markdown("### ✏️ Edit Profile")
            first_name = st.text_input("First Name", value=user[0])
            last_name = st.text_input("Last Name", value=user[1])
            email = st.text_input("Email", value=user[2])
            mobile = st.text_input("Mobile Number", value=user[3])
            address = st.text_area("Address", value=user[4])
            degree = st.text_input("Degree", value=user[5])
            college = st.text_input("College", value=user[6])
            passyear = st.text_input("Passout Year", value=user[7])
            university = st.text_input("University", value=user[8])

            if st.button("Save Changes"):
                cursor = connection.cursor()
                cursor.execute("""
                    UPDATE users SET first_name=%s, last_name=%s, email=%s, mobile_number=%s, address=%s, degree=%s, college=%s, passout_year=%s, university=%s
                    WHERE email=%s
                """, (first_name, last_name, email, mobile, address, degree, college, passyear, university, st.session_state.user_email))
                connection.commit()
                cursor.close()
                connection.close()

                st.success("Profile updated successfully!")
                st.session_state["edit_mode"] = False
        else:
            st.error("User not found.")
    else:
        st.warning("### 🚪 Please login to edit your profile.")

# File to save posts
DATA_FILE = "student_wall.csv"

def load_posts():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["username", "content", "image", "time"])


def student_wall():
    st.title("📰 Student Wall Feed")

    # ✅ Always load posts first
    posts = load_posts()
    connection = create_db_connection()
    cursor = connection.cursor()
    query = "SELECT first_name FROM users WHERE email=%s"
    cursor.execute(query, (st.session_state.user_email,))
    username = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    # welcome Username on SSocial Wall
    st.markdown(f"### 👋 Welcome {username} to the Student Wall!")
    content = st.text_area("What's on your mind?")
    image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if st.button("Post"):
        if username.strip() != "" and content.strip() != "":
            img_path = ""
            if image:
                os.makedirs("uploads", exist_ok=True)
                img_path = f"uploads/{image.name}"
                with open(img_path, "wb") as f:
                    f.write(image.getbuffer())

            new_post = pd.DataFrame(
                [[username, content, img_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]],
                columns=["username", "content", "image", "time"]
            )

            
            posts = pd.concat([new_post, posts], ignore_index=True)
            posts.to_csv(DATA_FILE, index=False)

            st.success("✅ Post shared successfully!")
            st.rerun()  

        else:
            st.warning("⚠️ Please enter both name and content.")

    st.markdown("---")

    # Show posts
    if not posts.empty:
        for _, row in posts.iterrows():
            with st.container():
                st.markdown(f"**👤 {row['username']}**  •  *{row['time']}*")
                st.write(row["content"])
                if isinstance(row["image"], str) and os.path.exists(row["image"]):
                        st.image(row["image"], use_container_width=True)
                st.markdown("---")

        # ✅ Delete button
        if st.button("Delete All Posts"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
                st.success("🗑️ All posts deleted successfully!")
                st.rerun() 
    else:
        st.info("No posts yet. Be the first to share something! 🚀")


# Save Data in Blog Table
def save_blog(user_email, title, content):
    connection = create_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO blogs (user_email, title, content) VALUES (%s, %s, %s)", (user_email, title, content))
    connection.commit()
    cursor.close()
    connection.close()

def my_modules():
    st.markdown("### 🔖 My Modules")
    st.write("This is the My Modules section. More features coming soon!")

def logout():
    st.set_page_config(page_title="📝Smart Learn Logout", layout="wide")
    st.markdown("""
        <style>
            .main-title {
                text-align: center;
                font-size: 40px;
                font-weight: bold;
                color: white;
                margin-bottom: 0px;
            }
            .logo-container {
                display: flex;
                justify-content: center;
                margin-bottom: 10px;
            }
            .logo-container img {
                width: 90px;
                height: 90px;
                border-radius: 0%;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
                }
                }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">Smart Learn 📘</h1>', unsafe_allow_html=True)


    st.markdown("### 🚪 Logout")
    st.write("Welcome ! Please confirm you want to logout.")
    if st.button("Logout"):
        st.success("Logged out successfully!")
        st.session_state.clear()  

# ------------------------- MAIN APP -------------------------
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


    with st.sidebar:
        select = option_menu(
            menu_title=" MENU",
            options=[
                "Home",
                "Login",
                "Registration",
                "Student List",
                "Profile",
                "Student Wall",
                "Write Blog",
                "My Modules",
                "Logout"
            ]
        )

    if select == "Home":
        home()
    elif select== "Login":
        login_form()
    elif select == "Registration":
        register_form()
    elif select == "Student List":
        # call only when active session current login session
        if "logged_in" in st.session_state and st.session_state.logged_in:
            student_list()
        else:
            st.warning("### 🚪 Please login to view the student list.") 
    elif select == "Profile":
        profile()
        
    elif select == "Student Wall":
        if "logged_in" in st.session_state and st.session_state.logged_in:
            student_wall()
            load_posts()
        else:
            st.warning("### 🚪 Please login to view the student wall.")
    elif select == "Write Blog":
        
        if "logged_in" in st.session_state and st.session_state.logged_in:
            connection = create_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT first_name FROM users WHERE email=%s", (st.session_state.user_email,))
            user = cursor.fetchone()
            if user:
                st.markdown(f"Welcome {user[0]} to the Blog Section")
                st.markdown("### ✍ Write Your Blog")
                blog_content = st.text_area("Blog Content")
                if st.button("Submit Blog"):
                    if blog_content:
                        save_blog(st.session_state.user_email, blog_title, blog_content)
                        st.success("Blog submitted successfully!")
                    else:
                        st.warning("Please enter blog content.")
            elif user is None:
                st.warning("User not found.")
            cursor.close()
            connection.close()
        else:
            st.warning("### 🚪 Please login to write a blog.")

    if select == "My Modules":
        if "logged_in" in st.session_state and st.session_state.logged_in:
           
            with st.sidebar.expander("🔖 My Modules"):
                sub_modules = option_menu(
                    menu_title=" ",
                    options=[
                        "Shortlist Candidate",
                        "SmartLearn GPT",
                        "Module 3"
                    ]
                )
                #if sub module is shortlisted candidate then it only for admin
                if sub_modules == "Shortlist Candidate":
                    connection = create_db_connection()
                    cursor = connection.cursor()
                    #if email was admin@gmail.com then only allow
                    query = "SELECT email FROM users WHERE email=%s"
                    cursor.execute(query, (st.session_state.user_email,))
                    user = cursor.fetchone()
                    if user and user[0] == "admin@gmail.com":
                        st.success("### ✅ You have access to this feature.")
                    else:
                        st.warning("### 🚪 This feature is only available for admin users.")
            my_modules()
        else:
            st.warning("### 🚪 Please login to view your modules.")

    elif select == "Logout":
        logout()

if __name__ == "__main__":
    main()
