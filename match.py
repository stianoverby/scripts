from datetime import datetime
import csv

date_format = '%d.%m.%Y'

def read_events(filename):
    # Create an empty list to store the data
    data = []

    # Open the file and read in the lines
    with open(filename, "r") as file:
        for line in file:
            # Split the line into separate fields
            fields = line.strip().split(", ")
            # Append the fields to the list
            data.append(fields)

    return data

def extract_participants(filename):
    
    with open(filename) as file:
        csvreader = csv.reader(file)

        #Extract the headers
        header = []
        iterator = csvreader
        header = next(iterator)

        # Extract the rows. Skip the first blank row.
        rows = []
        next(iterator)
        for row in iterator:
            rows.append(row)

    # Combine the correct row elements with their header
    combined = combine_rows_and_header(rows, header)

    # Extract only the columnst with the wanted headers
    participants = [{x : y for x,y in m if is_wanted_column((x,y))} for m in combined]
    
    # Filter out duplicates of participants
    unique_participants = []
    for idx, participant in enumerate(participants):
        if participant not in participants[idx+1 : ]:
            unique_participants.append(participant)
    
    return unique_participants

def is_wanted_column(tpl):
    wanted_column_headers = ["Fornavn", "Etternavn", "Fødselsdato", "Kjønn"]
    header, _ = tpl
    return header in wanted_column_headers

''' Date helper functions '''
def convert_to_date(date):
    return datetime.strptime(date, date_format).date()

def after(d1, d2):
    return d2.month <= d1.month and d2.day < d1.day

def before(d1, d2):
    return d1.month <= d2.month and d1.day <= d2.day 

''' Functions for moving around lists '''
def combine_rows_and_header(nested_lst, flat_lst):
    result = []
    for lst in nested_lst:
        new_lst = []
        for e1, e2 in zip(lst, flat_lst):
            new_lst.append((e2, e1))
        result.append(new_lst)
    return result

def filter_on_age(kids, legal_age, start_date, end_date, negate_predicate = False):
    
    # Filter function
    def allowed_age(kid):
        birthday = datetime.strptime(kid['Fødselsdato'], "%d.%m.%Y")
        age_this_year = end_date.year - birthday.year

        # Becoming the minimum required age and has birthday before the start date of the event
        if age_this_year == min(legal_age) and before(birthday, start_date):
            return True
        
        # Becoming an age in the allowed range that is not the minimum
        if 1 < len(legal_age) and age_this_year in legal_age[1:]:
            return True 

        # Becoming older than the maximum legal age, but has birthday after the end of the event
        if age_this_year == max(legal_age) + 1 and after(birthday, end_date):
            return True 

        return False

    if negate_predicate:
        return list(filter(lambda x: not allowed_age(x), kids))

    return list(filter(allowed_age, kids))

def process_participants(participants, event, legal_age):
    
    event_name, sdate, edate = event

    start_date = datetime.strptime(sdate, date_format)
    end_date = datetime.strptime(edate, date_format)

    legal_participants = filter_on_age(participants, legal_age, start_date, end_date)
    possible_participants = ([list(dict.values()) for dict in legal_participants])
    possible_participants.sort()
    
    illegal_participants = filter_on_age(participants, legal_age, start_date, end_date, negate_predicate=True)
    not_possible_participants = ([list(dict.values()) for dict in illegal_participants])
    not_possible_participants.sort()

    output = ""
    output += "\nEVENT => " + event_name.upper() + "\n"
    output += "=====================================================\n"
    output += pretty_str("   ALLOWED TO GO\n", possible_participants)
    output += pretty_str("\n   TOO YOUNG OR OLD\n", not_possible_participants)
    output += "=====================================================\n"

    return output

def pretty_str(title, participants):
    output = title
    output += "   |Kvinner|\n"
    for participant in participants:
        if participant[3] == "Kvinne":
            output += "   " + str(participant) + "\n"

    output += "\n   |Menn|\n"
    for participant in participants:
        if participant[3] == "Mann":
            output += "   " + str(participant) + "\n"
    output += "\n   Participants in category : " + str(len(participants)) + "\n"
    return output

if __name__ == "__main__":
    participants = extract_participants("input.csv")
    events = read_events("events.txt")
    legal_age = [16, 17]

    output = ""
    for event in events:
        output += process_participants(participants, event, legal_age)
    
    with open("output.txt", "w") as file:
        file.write(output)

