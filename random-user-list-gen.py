from faker import Faker
import random

fake = Faker('en_IN')

# Generate a list of scholar numbers
scholar_numbers = list(range(1001, 1041))
random.shuffle(scholar_numbers)

# Function to generate random student data
def generate_random_student():
    scholar_number = scholar_numbers.pop(0)
    name = fake.name()
    class_ = random.randint(10, 12)
    section = random.choice(['A', 'B', 'C'])
    gender = random.choice(['M', 'F'])
    attendance = random.randint(150, 200)
    phy = random.randint(75, 95)
    chem = random.randint(75, 95)
    maths = random.randint(75, 95)
    eng = random.randint(75, 95)
    comp = random.randint(75, 95)
    total_marks = phy + chem + maths + eng + comp
    phone_number = '+91' + ''.join(random.choice('0123456789') for _ in range(10))
    height = round(random.uniform(150, 180), 1)
    weight = round(random.uniform(40, 80), 1)

    return (
        f'{name}', class_, f'{section}', scholar_number, f'{gender}', attendance,
        phy, chem, maths, eng, comp, total_marks, f'{phone_number}', height, weight
    )

# Generate data for 40 students
students_data = [generate_random_student() for _ in range(40)]

# Create a single SQL INSERT statement for all students
insert_statement = """
INSERT INTO Student (name, class, section, scholar_number, gender, attendance, phy, chem, maths, eng, comp, total_marks, phone_number, height, weight)
VALUES
    {};
""".format(',\n    '.join(str(data) for data in students_data))

# Print the SQL statement
print(insert_statement)
