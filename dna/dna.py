import csv
import sys
import json


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: file.csv file.txt")

    # TODO: Read database file into a variable
    database = {}
    data = True
    with open(sys.argv[1]) as file:
        while data:
            data = file.readline().strip("\n")
            if data != '':
                data1 = data.split(",", 1)
                name = data1[0]
                database[name] = data1[1].split(",", len(data1[1]))
                list = []
                if name != "name":
                    for i in database[name]:
                        list.append(int(i))
                        database[name] = list

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2]) as file:
        dna_S = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    str = []
    for value in database["name"]:
        str.append(longest_match(dna_S, value))

    # TODO: Check database for matching profiles
    for key, value in database.items():
        if database[key] == str:
            print(key)
            return
    else:
        print("No Match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
