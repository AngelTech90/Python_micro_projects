
i = 0

def fill_list(list_len, new_list):

    i = 1

    while i != list_len:
    
        new_list.append(i)
    
        i = i + 1
        
    print(new_list)

# *Here we create a list for save our amount of grades in our classroom:
amount_grades = int(input('Give your amount of grades in your school: '))
list_grades = list()

# *Here we create and define our list for store our classrooms
amount_classrooms = int(input('Give the amount of your school classrooms: '))
list_classrooms = list()

# *Here we create our list for then fill with the names of our students
amount_students = int(input('Give me your amount of students: '))
list_students = list()


fill_list(amount_classrooms, list_classrooms)
fill_list(amount_grades, list_grades)
fill_list(amount_students, list_students)


#*This function is for asing with loops the grades name of our school
def asign_school_grades():
    
    i = 0
    
    grade = 0
    
    while i != amount_grades:
        
        grade = i + 1
        
        list_grades.insert(i, grade)
        
        i = i + 1
        
        print(i)
        
    

#*Here we are making that all our classrooms names be inside the alphabet words:
def asign_school_classrooms():
    
    i = 0
    
    classrooms = 'ABCDEFGHIJKMNLOPQRSUWYXZ'
    
    while i != amount_classrooms:
        
        while i != len(classrooms):
        
            list_classrooms.insert(i, classrooms[i])
            
            i = i + 1
            
            print(i)
    
    
#*Here we'll asign all our student name
def asign_school_students():
    
    i = 0
    
    while i != amount_students:
        
        first_name = str(input(f'Give me your student number {i + 1} name'))
        last_name = str(input(f'Give me your student number {i + 1} last name'))
        
        student_name = f'{first_name} {last_name}'
        
        list_students.insert(i, student_name)
        
        i = i + 1
        
        print(i)


# *This is the function for find our students in our lists:
def find_student(student):
    
    str(student)
    
    for students in list_students:
        
        if student == students:
            print(f'Your student is {student}')
        else:
            print(f"{student} is not registered in our student list")
            
            
asign_school_grades()
asign_school_classrooms()
asign_school_students()

find_student('Angel Molina')