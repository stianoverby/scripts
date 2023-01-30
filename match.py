"""
    DIVIDE PARTICIPANTS INTO ALLOWED/NOT ALLOWED AGE GROUPS
        Script developed to help an voluntary organization to filter what participants 
        are allowed to take part of an event. Allowed participants are those who are of
        the allowed age during the entire event.
"""

from datetime import datetime
import csv

date_format = "%d.%m.%Y"


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

        # Extract the headers
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
    participants = [{x: y for x, y in m if is_wanted_column((x, y))} for m in combined]

    # Filter out duplicates of participants
    unique_participants = []
    for idx, participant in enumerate(participants):
        if participant not in participants[idx + 1 :]:
            unique_participants.append(participant)

    return unique_participants


def is_wanted_column(tpl):
    wanted_column_headers = ["Fornavn", "Etternavn", "Fødselsdato", "Kjønn"]
    header, _ = tpl
    return header in wanted_column_headers


def convert_to_date(date):
    return datetime.strptime(date, date_format).date()


def after(d1, d2):
    if d2.month < d1.month:
        return True
    return d2.month == d1.month and d2.day < d1.day


def before(d1, d2):
    # The before function is not as strict, since if you have
    # your birthday the first day of the event you are allowed to go
    if d1.month < d2.month:
        return True
    return d1.month == d2.month and d1.day <= d2.day


def combine_rows_and_header(nested_lst, flat_lst):
    result = []
    for lst in nested_lst:
        new_lst = []
        for e1, e2 in zip(lst, flat_lst):
            new_lst.append((e2, e1))
        result.append(new_lst)
    return result


def partition_participants(participants, start_date, end_date):

    legal_ages = [16, 17]

    """ Predicate for filtering """

    def allowed_age(kid):
        birthday = datetime.strptime(kid["Fødselsdato"], "%d.%m.%Y")
        age_this_year = end_date.year - birthday.year

        # Becoming the minimum required age and has birthday before the start date of the event
        if age_this_year == min(legal_ages) and before(birthday, start_date):
            return True

        # Becoming an age in the allowed range that is not the minimum
        if 1 < len(legal_ages) and age_this_year in legal_ages[1:]:
            return True

        # Becoming older than the maximum legal age, but has birthday after the end of the event
        if age_this_year == max(legal_ages) + 1 and after(birthday, end_date):
            return True

        return False

    allowed = [p for p in participants if allowed_age(p)]
    not_allowed = [p for p in participants if not allowed_age(p)]

    return allowed, not_allowed


def process_participants(participants, event):

    event_name, sdate, edate = event

    start_date = datetime.strptime(sdate, date_format)
    end_date = datetime.strptime(edate, date_format)

    allowed_participants, not_allowed_participants = partition_participants(
        participants, start_date, end_date
    )

    allowed_participants = [list(dict.values()) for dict in allowed_participants]
    allowed_participants.sort()
    not_allowed_participants = [
        list(dict.values()) for dict in not_allowed_participants
    ]
    not_allowed_participants.sort()

    output = pretty_output_event(
        event_name, allowed_participants, not_allowed_participants
    )

    return output


def pretty_output_event(event_name, allowed_participants, not_allowed_participants):
    header_event = "\nEVENT => " + event_name.upper() + "\n"
    header_allowed = "   ALLOWED TO GO\n"
    header_not_allowed = "\n   TOO YOUNG OR OLD\n"
    header_bar = "=====================================================\n"

    output = header_event
    output += header_bar
    output += pretty_output_participants(header_allowed, allowed_participants)
    output += pretty_output_participants(header_not_allowed, not_allowed_participants)
    output += header_bar
    return output


def pretty_output_participants(title, participants):
    header_women = "   |Kvinner|\n"
    header_men = "\n   |Menn|\n"
    header_n_participants = (
        "\n   Participants in category : " + str(len(participants)) + "\n"
    )

    output = title
    output += header_women
    for participant in participants:
        if participant[3] == "Kvinne":
            output += "   " + str(participant) + "\n"

    output += header_men
    for participant in participants:
        if participant[3] == "Mann":
            output += "   " + str(participant) + "\n"
    output += header_n_participants
    return output


if __name__ == "__main__":
    participants = extract_participants("input.csv")
    events = read_events("events.txt")

    output = ""
    for event in events:
        output += process_participants(participants, event)

    with open("output.txt", "w") as file:
        file.write(output)
