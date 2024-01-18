import mysql.connector

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="pass",
    database="student"
)

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Student (
        id INT AUTO_INCREMENT UNIQUE,
        name VARCHAR(255) DEFAULT '-',
        class INT DEFAULT 12,
        section VARCHAR(1) DEFAULT '-',
        scholar_number INT PRIMARY KEY,
        gender VARCHAR(1) DEFAULT '-',
        attendance INT DEFAULT 0,
        phy INT DEFAULT 0,
        chem INT DEFAULT 0,
        maths INT DEFAULT 0,
        eng INT DEFAULT 0,
        comp INT DEFAULT 0,
        total_marks INT,
        phone_number VARCHAR(15) DEFAULT '-',
        height VARCHAR(5) DEFAULT '-',
        weight VARCHAR(5) DEFAULT '-',
        fee INT DEFAULT 8000
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Teachers (
        id INT AUTO_INCREMENT UNIQUE,
        name VARCHAR(255) DEFAULT '-',
        attendance INT DEFAULT 50,
        salary INT DEFAULT 50000,
        PRIMARY KEY (id)
    )
""")

def insert_student_data():
    name = input("Name: ").capitalize()
    class_ = int(input("Class(*): "))
    section = input("Section: ").upper()
    scholar_number = int(input("Scholar Number(*): "))
    gender = input("Gender (M/F): ").upper()
    attendance = int(input("Attendance(/200*): "))
    phone_number = input("Phone Number: ") or 'xxxxxxxxxx'
    height = float(input("Height(cm*): "))
    weight = float(input("Weight(kg*): "))
    phy = int(input("Physics: "))
    chem = int(input("Chemistry: "))
    maths = int(input("Maths: "))
    eng = int(input("English: "))
    comp = int(input("Computer: "))
    total_marks = phy + chem + maths + eng + comp 
    fee = 7000

    insert_query = """
        INSERT INTO Student (name, class, section, scholar_number, gender, attendance, phy, chem, maths, eng, comp, total_marks, phone_number, height, weight, fee) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (name, class_, section, scholar_number, gender, attendance, phy, chem, maths, eng, comp, total_marks, phone_number, height, weight, fee)
    cursor.execute(insert_query, data)
    connection.commit()
    print("Data inserted successfully.")

def view_report_card():
    student_id = int(input("Enter Scholar No.(1000-1040): "))
    query = """
        SELECT name, class, section, attendance, phy, chem, maths, eng, comp, total_marks
        FROM Student
        WHERE scholar_number = %s
    """
    cursor.execute(query, (student_id,))
    result = cursor.fetchone()
    total = 100
    if result:
        c = (result[9] / (5 * total)) * 100
        classsec = f"{result[1]}{result[2]}"
        print("\n----------- REPORT CARD -----------")
        print(f"Name: {result[0]}")
        print(f"Class: {classsec}")
        print(f"Attendance: {result[3]}/200")
        print(f"Physics: {result[4]}/{total}")
        print(f"Chemistry: {result[5]}/{total}")
        print(f"Maths: {result[6]}/{total}")
        print(f"English: {result[7]}/{total}")
        print(f"Computer: {result[8]}/{total}")
        print(f"Total Marks: {result[9]}/{5 * total}")
        print(f"Percentage: {c}")
        print("----------------------------------")
    else:
        print("Student not found.")

def modify_entry():
    student_id = int(input("Enter Scholar Number: "))
    print("Choose a field to modify:")
    print("1. Name")
    print("2. Class")
    print("3. Section")
    print("4. Scholar Number")
    print("5. Gender")
    print("6. Attendance")
    print("7. Physics")
    print("8. Chemistry")
    print("9. Maths")
    print("10. English")
    print("11. Computer")
    print("12. Phone Number")
    print("13. Height")
    print("14. Weight")
    choice = int(input("Enter your choice: "))

    fields = [
        "name", "class", "section", "scholar_number", "gender", "attendance",
        "phy", "chem", "maths", "eng", "comp", "phone_number", "height", "weight"
    ]

    if 1 <= choice <= len(fields):
        field_name = fields[choice - 1]
        new_value = input(f"Enter new value for {field_name}: ")

        update_query = f"""
            UPDATE Student
            SET {field_name} = %s
            WHERE scholar_number = %s
        """
        cursor.execute(update_query, (new_value, student_id))
        connection.commit()
        print("Entry modified successfully.")
    else:
        print("Invalid choice.")

def view_full_table():
    query = "SELECT * FROM Student"
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        print("No records found.")
    else:
        print("\n----------- FULL STUDENT TABLE -----------")
        print("{:<5} {:<20} {:<5} {:<5} {:<8} {:<5} {:<12} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<15} {:<10} {:<10}".format(
            "ID", "Name", "Class", "Sec", "Schl No.", "Gender", "Attendence", "Phy", "Chem", "Maths", "Eng", "Comp", "Total", "Phone", "Height", "Weight"
        ))
        print("-" * 120)

        for row in results:
            print("{:<5} {:<20} {:<5} {:<5} {:<10} {:<5} {:<12} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<15} {:<10} {:<10}".format(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15]
            ))

def delete_student_record():
    scholar_number = int(input("Enter Scholar Number to delete: "))
    delete_query = "DELETE FROM Student WHERE scholar_number = %s"
    cursor.execute(delete_query, (scholar_number,))
    connection.commit()
    print("Student record deleted successfully.")

def search_student():
    search_field = input("Enter the field to search (name/id/class/gender/): ")
    search_value = input(f"Enter the {search_field} to search: ")
    search_query = f"SELECT id, name, class, section, gender FROM Student WHERE {search_field} = %s"
    cursor.execute(search_query, (search_value,))
    results = cursor.fetchall()

    if not results:
        print("No records found.")
    else:
        print("\n----------- SEARCH RESULTS -----------")
        for row in results:
            print(row)

def average_marks():
    average_query = "SELECT AVG(phy), AVG(chem), AVG(maths), AVG(eng), AVG(comp) FROM Student"
    cursor.execute(average_query)
    averages = cursor.fetchone()

    print("\n----------- AVERAGE MARKS -----------")
    print(f"Physics: {averages[0]}")
    print(f"Chemistry: {averages[1]}")
    print(f"Maths: {averages[2]}")
    print(f"English: {averages[3]}")
    print(f"Computer: {averages[4]}")

def show_teachers_table():
    query = "SELECT * FROM Teachers"
    cursor.execute(query)
    results = cursor.fetchall()

    if not results:
        print("No records found in Teachers table.")
    else:
        print("\n----------- TEACHERS TABLE -----------")
        print("{:<5} {:<20} {:<12} {:<5}".format("ID", "Name", "Attendance", "Salary"))
        print("-" * 40)

        for row in results:
            print("{:<5} {:<20} {:<10} {:<5}".format(row[0], row[1], row[2], row[3]))

def teacher_attendance_tracker():
    teacher_name = input("Enter teacher's name: ").capitalize()

    query = "SELECT attendance, salary FROM Teachers WHERE name = %s"
    cursor.execute(query, (teacher_name,))
    result = cursor.fetchone()

    if result:
        print("\n----------- TEACHER ATTENDANCE TRACKER -----------")
        print(f"Teacher: {teacher_name}")
        print(f"Attendance: {result[0]}")
        print(f"Salary: {result[1]}")
    else:
        print(f"No information found for teacher: {teacher_name}")

def delete_teacher_by_name():
    teacher_name = input("Enter teacher's name to delete: ").capitalize()
    delete_query = "DELETE FROM Teachers WHERE name = %s"
    cursor.execute(delete_query, (teacher_name,))
    connection.commit()
    print(f"Teacher '{teacher_name}' deleted successfully.")

def admin_portal_menu():
    while True:
        print("\nADMIN PORTAL MENU:")
        print("1. Teachers Attendance Tracker")
        print("2. Finances")
        print("3. Show Teachers Table")
        print("4. Delete a Teacher")
        print("5. Exit")

        admin_choice = input("Select an option (1/2/3/4): ")

        if admin_choice == '1':
            teacher_attendance_tracker()
        elif admin_choice == '2':
            earning_query = "SELECT IFNULL(SUM(fee), 0) FROM Student"
            cursor.execute(earning_query)
            total_earning = cursor.fetchone()[0]

            spending_query = "SELECT IFNULL(SUM(salary), 0) FROM Teachers"
            cursor.execute(spending_query)
            total_spending = cursor.fetchone()[0]

            net_balance = total_earning - total_spending

            print("\n----------- FINANCIAL SUMMARY -----------")
            print(f"Earnings from Student Fees: {total_earning}")
            print(f"Spending on Teachers' Salaries: {total_spending}")
            print(f"Net Profit/Loss: {net_balance}")

        elif admin_choice == '3':
            show_teachers_table()
        elif admin_choice == '4':
            delete_teacher_by_name()
        elif admin_choice == '5':
            print("Exiting the Admin Portal.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def student_portal_menu():
    while True:
        print("\nSTUDENT PORTAL MENU:")
        print("1. Insert Student Data")
        print("2. View Report Card")
        print("3. Modify Entry")
        print("4. View Full Student Table")
        print("5. Delete A Student")

        student_choice = input("Select an option (1/2/3/4/5): ")

        if student_choice == '1':
            insert_student_data()
        elif student_choice == '2':
            view_report_card()
        elif student_choice == '3':
            modify_entry()
        elif student_choice == '4':
            view_full_table()
        elif student_choice == '5':
            delete_student_record()
        elif student_choice == '6':
            print("Exiting the Student Portal.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def main_menu():
    while True:
        print("\nMAIN MENU:")
        print("1. Admin Portal")
        print("2. Student Portal")
        print("3. Exit")

        main_choice = input("Select an option (1/2/3): ")

        if main_choice == '1':
            admin_portal_menu()
        elif main_choice == '2':
            student_portal_menu()
        elif main_choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

main_menu()

cursor.close()
connection.close()
