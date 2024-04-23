import csv
import sys


def main():

    if len(sys.argv) == 3:
        csvf = sys.argv[1]
        seq = sys.argv[2]

        try:
            rows = []
            with open(csvf) as cf:
                rdr = csv.DictReader(cf)
                for row in rdr:
                    rows.append(row)

            with open(seq) as s:
                srdr = s.readlines()
        except FileNotFoundError:
            sys.exit("File not found")

        STR = {}
        for w in rdr.fieldnames[1:]:
            e = longest_match(srdr, w)
            STR[w] = e

        for row in rows:
            match = True
            for key in STR:
                if row[key] != STR[key]:
                    match = False
                    break
            if match:
                print(row["name"])
                return
        print("No match")

    else:
        sys.exit("Invalid input")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence[0])
    # print(sequence_length)
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
            if sequence[0][start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return str(longest_run)


main()
