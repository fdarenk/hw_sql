import sqlite3, re


def main_menu():
    action_type = input('You are in Main Menu.\n'
                        'There are the following options:\n'
                        '1. See all projects of a freelancer, ordered by the deadline date\n'
                        '2. See all projects of an employee (ordered by the payment)\n'
                        '3. Register a freelancer\n'
                        '4. Register a project\n'
                        '5. Register an employer\n'
                        '6. Write about acceptance of a project by a freelancer\n'
                        '7. TRY THE JOIN FUNCTION and get the data for correlation between birthdate and salary\n'
                        'Enter the number of the desired option: ')
    if action_type == '1':
        fl_projects()
    if action_type == '2':
        em_projects()
    if action_type == '3':
        create_freelancer()
    if action_type == '4':
        create_project()
    if action_type == '5':
        create_employer()
    if action_type == '6':
        acceptance()
    if try_join == '7':
        try_join()

def try_join():
    con = sqlite3.connect("Fedorenko_DB-HW2.db")
    cur = con.cursor()
    data_res = cur.execute("SELECT freelancers.birthdate, projects.payment "
                          "FROM freelancers, acceptances "
                          "INNER JOIN projects ON acceptances.p_id = projects.p_id")
    data = data_res.fetchall()
    print(data)
    con.commit()

def acceptance():
    print('You are write about acceptance of a project by a freelancer. Please, specify the freelancer and the project')
    fl_id = detect_person()
    p_id = detect_project()
    con = sqlite3.connect("Fedorenko_DB-HW2.db")
    cur = con.cursor()
    write = cur.execute("INSERT INTO acceptances (fl_id, p_id) VALUES (?, ?)",
                        (fl_id, p_id))
    con.commit()

def fl_projects():
    con = sqlite3.connect("Fedorenko_DB-HW2.db")
    cur = con.cursor()
    fl_id = detect_person(name)
    projects_select = cur.execute("SELECT projects.p_name, employers.e_name, projects.payment, projects.deadline, projects.challenge "
                          "FROM acceptances, projects, employers "
                          "WHERE acceptances.fl_id = ? AND projects.e_id = employers.e_id "
                                  "ORDER BY projects.deadline ASC", (fl_id,))
    projects = projects_select.fetchall()
    for project in projects:
        print(''.join(['Project \"'project[0], '\" provided by ', project[1], ', payed with ', project[2], ', with deadline at ', project[3], '. The challenge in the project is: ', project[4]]))
    con.commit()

def em_projects():
    con = sqlite3.connect("Fedorenko_DB-HW2.db")
    cur = con.cursor()
    employer_name = input('Enter, please, the employer\'s name: ')
    projects_select = cur.execute("SELECT projects.p_name, projects.payment, projects.deadline, projects.challenge "
                          "FROM projects, employers "
                          "WHERE projects.e_name = ? AND projects.e_id = employers.e_id AND "
                                  "ORDER BY projects.payment DESC", (fl_id,))
    projects = projects_select.fetchall()
    for project in projects:
        print(''.join(['Project \"'project[0], ', payed with ', project[1], ', with deadline at ', project[2], '. The challenge in the project is: ', project[3]]))
    con.commit()

def create_freelancer():
    print('You are creating a note about a freelancer. Please, fill the following info.')
    f_name = input('Enter the freelancer\'s full name: ')
    birthdate = input('Enter the freelancer\'s birthdate (YYYY.MM.DD): ')
    birthplace = input('Enter the freelancer\'s birthplace: ')
    con = sqlite3.connect("Fedorenko_DB-HW2.db")
    cur = con.cursor()
    write = cur.execute("INSERT INTO staff (f_name, birthdate, birthplace) VALUES (?, ?, ?)", (f_name, birthdate, birthplace))
    con.commit()

def create_project():
    con = sqlite3.connect("Fedorenko_DB-HW2.db")
    cur = con.cursor()
    print('You are creating a note about a project. Please, fill the following info.')
    p_name = input('Enter the project\'s name: ')
    e_name = input('Enter the project\'s employer\'s name: ')
    create_employer(e_name)
    payment = input('Enter the project\'s payment: ')
    deadline = input('Enter the project\'s deadline (YYYY.MM.DD): ')
    challenge = input('Enter the project\'s challenge: ')
    write = cur.execute("INSERT INTO staff (p_name, e_name, payment, deadline, challenge) VALUES (?, ?, ?, ?, ?)",
                        (p_name, e_name, payment, deadline, challenge))
    con.commit()

def create_employer(name):
    con = sqlite3.connect("Fedorenko_DB-HW2.db")
    cur = con.cursor()
    employers_res = cur.execute("SELECT e_name FROM employers ")
    employers = employers_res.fetchall()
    if name not in employers:
        write = cur.execute("INSERT INTO employers (e_name,) VALUES (?,)", (name,))
    con.commit()

def detect_person():
    con = sqlite3.connect("Fedorenko_DB-HW2.db")
    cur = con.cursor()
    name = input('Please, enter the name of the person: ')
    persons_res = cur.execute("SELECT f_id, f_name, birthdate, birthplace"
                         "FROM freelancers "
                         "WHERE p_name=?", (name,))
    persons = p_id.fetchall()
    if len(persons) == 0:
        print('There is no freelancer with such a name.')
    elif len(persons) == 1:
        return persons[0][0]
    else:
        i = 1
        print('Please, find the freelancer in the list below')
        for line in persons:
            print(''.join(['(', str(i) , ') Name: ', line[1], '; Birthdate: ', line[2], '; Birthplace: ', line[3]]))
            i += 1
        return persons[int(input("Enter the number of the person you meant: "))-1][0]
    con.commit()

def detect_project():
    con = sqlite3.connect("Fedorenko_DB-HW2.db")
    cur = con.cursor()
    name = input('Please, enter the name of the project: ')
    projects_res = cur.execute("SELECT projects.p_name, employers.e_name, projects.payment, projects.deadline, projects.challenge"
                         "FROM projects, employers "
                         "WHERE projects.p_name=? AND projects.e_id = employers.e_id", (name,))
    projects = p_id.fetchall()
    if len(persons) == 0:
        print('There is no project with such a name.')
    elif len(persons) == 1:
        return persons[0][0]
    else:
        i = 1
        print('Please, find the project in the list below')
        for line in persons:
            print(''.join(['(', str(i) , ') Name: ', line[1], '; Employer: ', line[2], '; Payment: ', line[3], '; Deadline: ', line[4], '; Challenge: ', line[5]]))
            i += 1
        return persons[int(input("Enter the number of the project you meant: "))-1][0]
    con.commit()

if __name__ == '__main__':
    main_menu()