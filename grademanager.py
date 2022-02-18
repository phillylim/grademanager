# Philly Lim, CSW8 (F21)

def print_main_menu(the_menu):
    '''
    Takes a dictionary type input and prints the options in the dictionary
    in a cohesive and properly formatted menu in increasing numerical order given
    that the dictionary keys are already defined in sequential order in the dictionary. 
    This is accompanied with a corresponding "frame", which is composed of 26 
    asterick (*) symbols that surrounds that dictionary options on the 
    top and the bottom to provide a visual aesthetic
    '''
    frame = '*' * 26
    print(frame)
    for key, item in the_menu.items(): # a "for loop" iterates through the dictionary's keys/items
        print('{} - {}'.format(key, item)) 
    print(frame) 

def check_option(option, menu):
    """
    Returns "invalid" if the provided `option`
    is not one of the keys in the given `menu`.
    Returns "valid" otherwise.
    """
    keys = menu.keys()
    if option not in keys:
        if type(option) == str:
            if not option.isdigit(): # Checks if it isn't a digit to output integer warning
                print('WARNING: `{}` is not an integer.'.format(option))
                print('Please enter an integer.')
                return 'invalid'
        print("WARNING: `{}` is an invalid option.".format(option)) #Otherwise print default message
        print('Please enter a valid option.')
        return 'invalid' 
    return 'valid'

def list_categories(db, showID = False):
    """
    The function takes two arguments: a dictionary
    and a Boolean flag that indicates whether to
    display the category IDs.
    The first argument is a dictionary, that stores a
    numeric ID as a key for each category;
    the corresponding value for the key is
    a list that contains a category item
    with 3 elements arranged as follows: 
    * `'name'` - the name of the category,
        e.g., "quiz", "participation";
    * `'percentage'` - the percentage of the total grade,
        e.g., 25, 5; 
    * `'grades'` - a list of grades.

    By default, displays the dictionary values as
    CATEGORY NAME : PERCENTAGE%
    If showID is True, the values are displayed as
    ID - CATEGORY NAME : PERCENTAGE%
    If a dictionary is empty, prints "There are no categories."
    If a dictionary has a single category,
    prints "There is only 1 category:"
    Otherwise, prints "There are X categories:"
    where X is the number of records in the dictionary.
    Returns the number of records.
    """
    records = len(db)
    if db == {}: # Checks for empty dictionary
        print('There are no categories.')
    elif records == 1:
        print('There is only 1 category:')
    else: # The only option left is that there are multiple categories
        print('There are {} categories:'.format(records))
    
    if showID:
        for key,item in db.items(): # iterate through dictionary
            name, percentage = item[0].upper(), item[1]
            print('{} - {} : {}%'.format(key, name, percentage)) # Print the corresponding ID
    else: # Otherwise, you don't print the ID
        for key,item in db.items(): 
            name, percentage = item[0].upper(), item[1]
            print('{} : {}%'.format(name, percentage))        
    return records # Returns the number of records

def add_category(db, cid, info_str):
    """
    Inserts into the `db` collection (dictionary)
    `cid` - the integer category ID (the key), and its
    corresponding value, which is a list obtained from the
    `info_str` that contains two elements: the category name 
    and the corresponding percentage of the total grade.
    If the list does not contain two elements, returns -2.
    Calls is_numeric():
    If the last input value (the percentage) in `info_str`
    is not numeric (int or float), does not update the
    dictionary and returns -1 instead.
    Otherwise, returns the integer ID of the category.
    Stores the percentage as a float (not as a string).
    """
    data = info_str.split()
    if len(data) != 2: # Checks if info has two elements only
        return -2
    if is_numeric(data[1]):
        db[cid] = [data[0], float(data[1])] # adds the category to the dictionary
        return cid
    return -1 # Otherwise return -1 if not correct type

def is_numeric(val):
    """
    Returns True if the string `val`
    contains a valid integer or a float.
    """
    if val.isdigit():
        return True
    elif '.' in val and val.count('.') == 1: # Checks for one period
        value = val.replace('.', '')
        return value.isdigit()
    return False

def create_id(storage, offset=0):
    """
    Returns an integer ID that would be generated 
    for the next value inserted into the `db` based on
    an optional offset value
    """
    if len(storage) == 0:
        return offset
    return max(storage.keys()) + offset + 1

def add_categories(db, max_num, id_offset):
    """
    Prompts the user to enter a single-word category name
    and the corresponding percentage of the total grade.
    Calls `create_id()` to get the ID for the category.
    Calls `add_category()`, and keeps asking the user to
    input the correct value for that category, if
    its percentage is not a number (int or float).
    """
    def recursive_add(limit, warning=False, quit=False, call=1):
        '''
        A recursive adding function to add categories.
        It takes 'limit' as a required argument. 
        The 'limit' is the user's input on
        how many categories they desire adding to 
        the database. The optional values, 'warning' = False, 
        'quite' = False, and 'call' = 1, are meant to keep track
        throughout the recursive calls of previous inputs. 
        For instance, if warning is True, which happens if 
        adding the category returns -1 or -2, then the 
        proper warning message is displayed; if quit = 
        True then the user inputted either 'm' or 'M', 
        returning them to the menu; the call keeps tracks 
        of the number of recursive calls and is incremented 
        with each successful iteration of the recursive 
        add function -- if it goes over the alloted limit, 
        then the function block within the if statement will 
        not evaluate, and thus the function will stop.
        If the function gets a valid input, then it continues 
        by recursively calling itself and incrementing
        the call by 1. 
        '''
        if call != limit + 1 and quit != True: # Base cases: ends if it exceeds limit or user puts 'M'
            if warning: # Prints warning message and if there was an invalid input
                print('WARNING: invalid input for the name and percentage.')
                print(f'::: Enter the category {call} name (no spaces) followed by its percentage')
                print('::: or enter M to return back to the menu.')
            else:
                print(f'::: Enter the category {call} name (no spaces) followed by its percentage')
            usr_line = input("> ") 
            id_num = create_id(db, id_offset) # Calls function for ID creation
            val = add_category(db, id_num, usr_line) 
            if val != -2 and val != -1: 
                recursive_add(limit, call=(call + 1)) # Continue as normal if valid input, incrementing call
            else: # Otherwise display warning messages and check if user inputted 'M' to quit and retry
                recursive_add(limit, warning=True, quit=(usr_line == 'm' or usr_line == 'M'), call=call)

    print(f"You can add up to {max_num} categories.")
    print("::: How many categories will you add?")
    while True: # The instructions here were vague, so I did a loop just in case
        line = input("> ") 
        if is_numeric(line): # If int or float return the input
            num = int(line)
            break
        else:
            print(f'`{line}` is not a valid integer.')
            print('::: Enter a valid number of categories you plan to add') # New output message

    if num > max_num: 
        print(f'WARNING: Adding {num} categories would exceed the allowable max.')
        print(f'You can store up to {max_num} categories.')
        print(f'Current total of categories is {len(db)}.')
    else: # otherwise it calls the recursive adding function
        recursive_add(int(num))

def update_category(db):
    """
    Prompts the user to enter the category ID
    and then asks to enter the updated information:
    name and the corresponding percentage of the total grade.
    Calls list_categories() at the beginning of the function,
    and add_category() to update the info.
    """
    def print_error(line):
        '''
        Function to output the error message for this function for user input
        '''
        print(f'WARNING: `{line}` is not an ID of an existing category.')
        print('::: Enter the ID of the category you want to update')
        print('::: or enter M to return back to the menu.')

    print('Below is the info for the current categories.')
    records = list_categories(db, showID=True)

    if records != 0: # Doesn't execute if this code is equal to 0
        print('::: Enter the category ID that you want to update')
    while records > 0: # While loop to go through
        line = input("> ")
        if line == 'M' or line == 'm': # Stop if they have m or M
            break
        if not is_numeric(line):
            print_error(line) # If not a number go back and output error
            continue
        if int(line) in db.keys(): #T ype conversion error avoided
            print(f'Found a category with ID `{line}`:')
            print('::: Enter the updated info:') # output message if found key
            print('    category name followed by the percentage.')
            cid = int(line)
            line = input('> ')
            val = add_category(db, cid, line)
            if val == -2: # Error message 
                print('WARNING: insufficient information for the update.')
                print(f'Record with ID `{cid}` was not updated!')
            if val == -1: # Other error message if the other case was true
                print('WARNING: invalid input for the name and/or percentage.')
                print(f'Record with ID `{cid}` was not updated!')
            break
        print_error(line)

def delete_category(db):
    """
    Calls list_categories() at the beginning of the function.
    Prompts the user to enter the category ID
    and then verifies the information and selection by printing 
    that record from the `db`.
    Deletes the category and its info, once the user confirms.
    """
    def confirmation(line):
        '''
        Function to reduce nested if statements within delete_category() and
        increase readability
        Confirms if the user wants to delete an inputted value
        '''
        print('::: Are you sure? Type Y or N')
        confirm = input("> ") # Gets input
        if confirm == 'Y' or confirm == 'y':
            del db[int(line)] # Delete if 'y'
            print('Deleted')
        else: # in any other case, cancel
            print("Looks like you aren't 100% sure.\nCancelling the deletion.")

    def print_error(line):
        '''
        Function to output the error message for this function based on user input
        '''
        print(f'WARNING: `{line}` is not an ID of an existing category.')
        print('::: Enter the ID of the category you want to delete')
        print('::: or enter M to return back to the menu.')

    print('Below is the info for the current categories.')
    records = list_categories(db, showID=True)
    if records != 0: # doesn't display if no categories
        print('::: Enter the category ID that you want to delete')
    while records > 0: # Loops through until it breaks
        line = input("> ")
        if line == 'M' or line == 'm':
            break # Input of 'm' ends the loop
        if not is_numeric(line):
            print_error(line)
            continue # Checks if not a number and goes back
        if int(line) in db.keys(): # If it finds it within keys
            print(f'Found a category with ID `{line}`:')
            print(db[int(line)])
            confirmation(line) # Call confirmation function
            break
        print_error(line) # Otherwise it will print error

def add_grades(db):
    """
    Calls list_categories() at the beginning of the function.
    Prompts the user to enter the category ID
    and then asks to enter the grades for that category. 
    Convert the grades string to the list of float values.
    Calls add_category_grades() to insert the record.
    Does not add the grades if not all provided grades
    contain numeric scores.
    """
    def print_error(line):
        '''
        Displays a corresponding error message for reusability
        in this function. Takes user input to output a message
        '''
        print(f'`{line}` is not an ID of an existing category.')
        print('::: Enter the ID of the category to add grades to')
        print('::: or enter M to return back to the menu.')
    records, found_key = list_categories(db, showID=True), False

    if records != 0: # If the number of records is 0 it won't print
        print('::: Enter the category ID for which you want to add grades')
    while records > 0:
        line = input("> ")
        if line == 'M' or line == 'm':
            break
        if found_key:
            val = add_category_grades(db, cid, line) # Attempt to add
            if val != -1:
                print(f'Success! Grades for the {db[cid][0].upper()} category were added.')
            else: # The instructions did not specify a warning message here
                print('WARNING: Invalid input for grades!')
                print(f'Category grades with ID `{cid}` was not added!')
            break
        if not is_numeric(line): 
            print_error(line) # Checks to avoid conversion error 
            continue
        if int(line) in db.keys(): # Checks if within the keys
            print(f'You selected a {db[int(line)][0].upper()} category.')
            print('::: Enter space-separated grades')
            print('::: or enter M to return back to the menu.')
            found_key = True # found_key is set to True for when it loops back
            cid = int(line)
        else:
            print_error(line)

def add_category_grades(db, cid, grades_str):
    """
    Inserts into the `db` collection (a dictionary)
    a list of grades for the provided category ID.
    The list is obtained from the grades_str.
    Calls is_numeric() to check each grade in 
    grades_str: if all provided grades were not numeric, 
    does not update the dictionary and returns -1.
    Stores the grades as a list of floats (not as strings).
    Calls show_grades_category() if the user adds grades to a category
    that already has grades added to it. 
    If a category with the provided ID already has grades
    in it, then the new grades are appended to the existing
    grades and updated information is displayed.
    Returns the number of grades that were added.
    """
    # Uses List Comprehensions - Optional material in Zybooks 7.8
    has_grades = False
    sorted_input = [float(number) for number in grades_str.split() if is_numeric(number)]
    if len(sorted_input) != len(grades_str.split()): # Not all values numeric
        return -1
    if len(db[cid]) == 3: # If it already has grades then call function
        show_grades_category(db, cid)
        has_grades = True
    if not has_grades:
        db[cid].append(sorted_input) # add grades if it doesn't have it
    if has_grades: # If it already had grades, print again to show updated grades
        db[cid][2].extend(sorted_input)
        show_grades_category(db, cid)
    return len(sorted_input)
    
def show_grades(db):
    """
    Calls list_categories() at the beginning of the function.
    If the dictionary is empty, return from the function.
    Otherwise, prompts the user to enter the category ID or 
    enter "A" to show grades of all categories that store them
    If the provided ID is not valid, prompt the user to enter 
    a valid ID or go back to the menu using ‘M’ or ‘m’ as input.
    Calls show_grades_category() with appropriate arguments 
    to show the grades.
    """
    record = list_categories(db, showID=True) # Display categories
    if record != 0: # Doesn't print if equal to 0
        print('::: Enter the category ID for which you want to see the grades')
        print('::: or enter A to list all of them.')
    while record > 0: # Otherwise loop through options
        line = input("> ")
        if line == 'M' or line == 'm':
            break # Standard break if the user inputs 'm'
        if line == 'A' or line == 'a':
            list_all_grades(db)
            break # list all grades function
        if is_numeric(line):
            if int(line) in db.keys():
                show_grades_category(db, int(line))
                break # Otherwise check for key and show that specific cat.
        print(f'WARNING: `{line}` is not an ID of an existing category.')
        print('::: Enter a valid category ID to see the grades')
        print('::: or enter M to return back to the menu.')

def show_grades_category(db, cid, all=False):
    """
    Displays the grades the user added into the db collection (dictionary), 
    for the provided category ID `cid`.
    If there are no grades, display "No grades were provided for category ID `cid`."
    and return 0.
    Otherwise, print the capitalized category name followed by a word "grades",
    and then a list of grades. Print the grades list without any beautification. 
    E.g.: QUIZ grades [100, 100, 95, 5, 80, 0]
    Return the number of grades in the grades list.
    I added an extra optional parameter to not output a message
    if the grades are empty since the instructions specified this.
    """
    if len(db[cid]) != 3:
        if not all: # change so it wont print under all grades call
            print(f'No grades were provided for category ID `{cid}`.')
        return 0 
    print(f'{db[cid][0].upper()} grades {db[cid][2]}') # outputs it out
    return db[cid][2] #returns the 2 element (grades)

def list_all_grades(db):
    '''
    Function that takes a collection, and
    prints all the grades. This is a function to
    reduce redundancy. It does not print if
    a given category does not have any grades.
    '''
    for key in db.keys():
        show_grades_category(db, key, all=True)
    
def sum_percentages(db):
    """
    Given a collection (dictionary),
    where each value is a list whose
    second element is a percentage of
    a category, returns the sum of the
    percentages.
    """
    return sum([item[1] for item in db.values()])

def get_avg_grade(grade_list):
    """
    Given a list of grades,
    returns the average value of the
    grades. Returns 0 if the list is
    empty.
    """
    if len(grade_list) == 0:
        return 0
    return sum(grade_list) / len(grade_list)

def grade_stats(db):
    """
    Calls list_categories() at the beginning of the function.
    Calls show_grades_category() to display the grades.
    Calls sum_percentages() to get the total percentages;
    shows a warning if they do not add up to 100.
    Calls get_avg_grade() to compute the average score for
    each category.
    Returns the computed course grade or, if there are no
    categories, returns 0.
    """
    print('Below is the info for the current categories.')
    records = list_categories(db)

    print('\nProvided grades:')
    list_all_grades(db) # Diplays all grades
    print()

    total_percentage = sum_percentages(db)
    if total_percentage != 100: # Error message if doesn't add up
        print("WARNING: Percentages don't add up to 100%.")
        print(f"Current category percentages comprise {total_percentage} of the total.")

    print('\nGrade calculation:')
    total = 0.00
    for key in db.keys(): # loops through keys
        cat_name, percent = db[key][0], db[key][1] / 100
        if len(db[key]) == 3: # Does this to prevent index error
            avg = get_avg_grade(db[key][2])
        else:
            avg = 0 # In the case that grades haven't been added yet
        weighted_percent = percent * avg
        print('{} = {:.2f} * {:.2f} = {:.2f}'.format(cat_name, avg, percent, weighted_percent))
        total += weighted_percent
    print('Total grade = {:.2f}'.format(total))
    return total

def save_data(db):
    """
    Calls list_categories() at the beginning of the function.
    If there are no categories, notify the user and return 0.
    By default, save the `db` to a CSV file.
    Asks the user whether to read from the default filename
    or ask for the filename to open.
    Calls save_dict_to_csv() to create the file.
    """
    records = list_categories(db)
    if records == 0: # Doesn't make a file if no cat.
        print('Skipping the creation of an empty file.')
        return 0
    
    print('::: Save to the default file (grade_data.csv)? Type Y or N')
    line = input("> ")
    if line == 'Y' or line == 'y':
        print('Saving the database in grade_data.csv')
        filename = 'grade_data.csv'
    else:
        while True: # parses through for valid custom CSV
            print('::: Enter the name of the csv file to load.')
            filename = input("> ") # Checks for a valid .csv file input
            if not check_file_extension(filename):
                print(f'WARNING: {filename} does not end with `.csv`')
                print('::: Enter the name of an existing csv file.')
            else:
                break
    save_dict_to_csv(db, filename)
    print('Database contents:') # Prints them out
    print(load_dict_from_csv(filename))

def save_dict_to_csv(db, filename):
    """
    Takes in a collection (dictionary) and 
    outputs the contents of the collection 
    to a csv file. Each row of the csv follows
    the format of (cat is short for category):
    catKey,catName,catPercent,catGrades,...
    The catGrades are separated comma by comma
    after the category percentage. If there aren't
    grades, then it adds an empty list at the end
    of the percentage
    """
    import csv
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for key in db.keys():
            grades = [] # temporary array to add for grades
            # To prevent index out of bounds error if grades not added
            if len(db[key]) == 3: 
                grades = db[key][2]
            writer.writerow([key, db[key][0], db[key][1]] + grades)

def load_dict_from_csv(filename):
    '''
    Given a string containing the filename,
    Opens the file and stores its contents
    into the dictionary, which is returned
    from this function.
    The function assumes that the first element
    on each row will be an integer ID, stored
    as a key in the dictionary, and the values
    that are on the rest of the line are stored
    in a list as follows:
    [row[1], float(row[2]), [float(i) for i in row[3:]]]
    The function returns an empty dictionary
    if the CSV file is empty.

    From the zybooks labs, this helps
    to convert a file CSV in the format of:
    Category ID,Category Name,Percentage,Grades...
    to a dictionary withe format of:
    {ID: [Name, Percentage, [Grades]]}
    Returns a collection (dictionary) back
    '''
    import csv
    with open(filename, 'r') as file:
        storage = {}
        lines = csv.reader(file, delimiter=',') # splits by comma
        for line in lines: # Iterates through lines and stores each value 
            storage[int(line[0])] = [line[1], float(line[2]), [float(x) for x in line[3:]]]
    return storage # returns the resulting dictionary

def load_data(db):
    """
    Loads the collection database into a csv file
    It defaults to grade_data.csv, but it can 
    be outputted to a custom csv file name.
    """
    import csv
    import os
    filename = "grade_data.csv"
    print(f"::: Load the default file ({filename})? Type Y or N")
    line = input('> ') 
    if not (line == 'y' or line == 'Y'):
        print('::: Enter the name of the csv file to load.')
    while not (line == 'y' or line == 'Y'):
        filename = input('> ') # Parses for a valid file name
        if not check_file_extension(filename): 
            print(f'WARNING: {filename} does not end with `.csv`')
            print('::: Enter the name of an existing csv file.')
        else:
            break # End loop once a valid name is provided
    print(f"Reading the database from {filename}")
    new_db = load_dict_from_csv(filename) # Load
    print("Resulting database:\n", new_db)
    db.update(new_db) # Updates database with new one
    return db

def check_file_extension(filename):
    '''
    Checks if the corresponding filename has .csv
    extension or not. Returns True if so, False
    otherwise
    '''
    parts = filename.split('.')
    if len(parts) < 2: # Edge case in where they don't give enough characters
        return False # Eg. ('a.') or ('.') or ('.c') - Not valid!
    if filename.count('.') == 1 and 'csv' == parts[1]:
        return True # True if last part is csv
    return False

def plot_statistics(db):
    '''
    Extra credit option to plot statistics of the grades
    '''
    # Covered in additional material Ch. 15
    import matplotlib.pyplot as plt
    import csv
    print('::: Database contents:\n')
    list_categories(db)
    print('\n::: Plotting database...')
    cat_grades = [[x[0],x[2]] for x in db.values() if len(x) == 3]
    # Covered in additional material Ch. 12.1
    try: # This is to prevent the program from breaking
        plt.xlabel('Anonymous Students') # Labels x-axis
        for cat_grade in cat_grades: # Goes over each category
            plt.ylabel(f'Scores') # Labels y axis
            number_of_grades = range(1, len(cat_grade) + 1)
            plt.bar(number_of_grades, cat_grade) # Plots scores
            plt.show() # Displays the graph to the user
    except: # Prints this if matplot isn't properly installed
        print('This requires the installation of matplot!')
        print('Error! You may have not installed matplot!')
        print('Please try installing it on your system to graph data!')

if __name__ == "__main__":
    # Defines the menu for output to the user
    the_menu = {
        '1' : 'List categories', '2' : 'Add a category', '3' : 'Update a category', 
        '4' : 'Delete a category', '5' : 'Add grades', '6' : 'Show grades', '7' : 'Grade statistics', 
        '8' : 'Save the data', '9' : 'Upload data from file', '*': 'Graph Data', 'Q' : 'Quit this program'
    } 
    main_db = {} # stores the grading categories and info
    max_cat = 10 # the max total num of categories a user can provide
    cat_id_offset = 100 # the starting value for the category ID

    opt = None

    while True:
        print_main_menu(the_menu)
        print("::: Enter an option")
        opt = input("> ")

        if opt == 'q' or opt == 'Q':
            print("Goodbye")
            break # Ends loop if character is 'q' or 'Q'
        else:
            if check_option(opt, the_menu) == "invalid": # Checks if the user input is an invalid key
                continue # If so, it continues to the start of the loop
            print("You selected option {} to > {}.".format(opt, the_menu[opt]))
        if opt == '1':
            list_categories(main_db)
        elif opt == '2':
            add_categories(main_db, max_cat, cat_id_offset)
        elif opt == '3':
            update_category(main_db)
        elif opt == '4':
            delete_category(main_db)
        elif opt == '5':
            add_grades(main_db)
        elif opt == '6':
            show_grades(main_db)
        elif opt == '7':
            grade_stats(main_db)
        elif opt == '8':
            save_data(main_db)
        elif opt == '9':
            load_data(main_db)
        elif opt == '*': # Extra credit function I implemented
            plot_statistics(main_db)
        opt = input("::: Press Enter to continue...")

    print("See you next time!")

    

