import re

REGEX_PATTERN_FOR_UPDATE = "\d[,][\sa-zA-Z]+.[a-zA-Z\s]+[,].[a-zA-Z\s]+"
# 1, Emile Zola, Nana OR 3, William Shakespeare, King Lear


class Library:
    def adding_book(self, str_to_split):
        if ',' in str_to_split:
            book = str_to_split.split(", ")
            author = book[0]
            title = book[1]
            # Author should be a string, but title could be an int --> 1984
            if len(title) >= 3 and isinstance(author, str) and len(author) > 8:
                try:
                    output_file = open('output.txt', 'a')
                    output_file.write("\n" + author + ", " + title)
                finally:
                    output_file.close()
                return f"{title} written by {author} has been successfully added to library!"
            else:
                return "Nope"
        else:
            return "Missing coma"

    def delete_book(self, number_of_book_to_delete):
        # Check for input which must be an int
        try:
            if int(number_of_book_to_delete) and number_of_book_to_delete > 0:
                # Check for valid number
                len_of_file = len(open("output.txt", 'r+').readlines())
                file = open('output.txt', "r+").readlines()

                if number_of_book_to_delete <= len_of_file:
                    for line in file:
                        if line == file[int(number_of_book_to_delete) - 1]:
                            open('output.txt', "w").write(line.replace(line, ""))
                        else:
                            open('output.txt', "a").write(line)

                    return f"{file[int(number_of_book_to_delete) - 1]} has been successfully deleted!"

            return "Number incorrect"

        except ValueError as Ve:
            return "NAN"


    def update_book(self, str_to_split):

        len_of_file = len(open("output.txt", 'r+').readlines())

        if len(re.findall(REGEX_PATTERN_FOR_UPDATE, str_to_split)) > 0:
            book = str_to_split.split(",")
            number_of_book_to_update = book[0]
            new_author = book[1]
            new_title = book[2]

            try:
                if int(number_of_book_to_update):
                    if int(number_of_book_to_update) <= len_of_file:

                        file = open('output.txt', 'r+').readlines()
                        book_to_update = file[int(number_of_book_to_update) - 1]
                        output_file = open('output.txt', 'w')

                        for line in file:

                            if line != book_to_update:
                                output_file.write(line)
                            else:
                                output_file.write(f"{new_author.strip()} , {new_title.strip()} \n")

                        return f"{book_to_update} has been changed to {new_author}, {new_title}"

                    else:
                        return "Too large"
            except ValueError:
                return "NAN"

        else:
            return "Bad format"