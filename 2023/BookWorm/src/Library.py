
# class Library:
#     def adding_book(self, str_to_split):
#         if ',' in str_to_split:
#             book = str_to_split.split(", ")
#             author = book[0]
#             title = book[1]
#             # Author should be a string, but title could be an int --> 1984
#             if len(title) >= 3 and isinstance(author, str) and len(author) > 8:
#                 try:
#                     output_file = open('output.txt', 'a')
#                     output_file.write("\n" + author)
#                     output_file.write(", " + title)
#                 finally:
#                     output_file.close()
#                 return f"{title} written by {author} has been successfully added to library!"
#             else:
#                 return "Nope"
#         else:
#             return "Missing coma"
#
#     def delete_book(self, number_of_book_to_delete):
#         # TODO Checker méthode originelle!
#         #Check for input which must be an int
#         if int(number_of_book_to_delete):
#             try:
#                 output_file = open('output.txt', 'r+')
#                 #Check for valid number
#                 print("LEN OF FILE:", len(output_file.readlines()))
#                 print(output_file.readlines())
#                 if number_of_book_to_delete <= len(output_file.readlines()):
#                     print("Passing if check")
#                     print(output_file.readlines()[number_of_book_to_delete + 1])
#                     for line in output_file.readlines():
#                         print(line)
#                         if line != output_file[int(number_of_book_to_delete) + 1]:
#                             output_file.write(line)
#                     return f"{output_file.readlines()[int(number_of_book_to_delete) + 1]} has been successfully deleted!"
#
#                 else:
#                     print("LEN OF FILE 2:", len(output_file.readlines()))
#                     print(output_file.readlines())
#                     return "Number incorrect"
#
#             finally:
#                 output_file.close()
#         else:
#             return "NAN"
#
#
#
#     def update_book(self):
#
#         try:
#             output_file = open('output.txt', "r")
#
#             if IS_FILE_EMPTY:
#                 print(EMPTY_FILE_MESSAGE)
#                 answer = input("Do you want to add a new book?y/n\n")
#                 if answer.lower() == 'y':
#                     adding_book()
#
#             print(f"\nHere is the content of your library: \n {output_file.read()}")
#             book_to_update = input("\nWhich book do you want to update?: \n"
#                                    "To update the first book, enter 1...")
#
#         finally:
#             output_file.close()
#
#         try:
#             if book_to_update and int(book_to_update):
#
#                 try:
#                     output_file = open('output.txt', 'r')
#                     content_of_file = output_file.readlines()
#                     book_to_update = content_of_file[int(book_to_update) - 1]
#
#                 finally:
#                     output_file.close()
#
#                 try:
#                     output_file = open('output.txt', 'w')
#                     new_book_author = input("What is the author of the new book?:\n")
#                     new_book_title = input("What is the title of the new book?:\n")
#                     for line in content_of_file:
#                         if line != book_to_update:
#                             output_file.write(line)
#                         else:
#                             output_file.write(f"{new_book_author} , {new_book_title}")
#
#                 finally:
#                     output_file.close()
#
#         except:
#             print(f"'{book_to_update}' is not a correct number")
#             update_book()
#
#
#     def search_for_book(self, string_to_search):
#         possible_matches = []
#
#         try:
#             output_file = open('output.txt', 'r')
#             for line in output_file.readlines():
#                 if string_to_search in line:
#                     possible_matches.append(line)
#
#         finally:
#             output_file.close()
#         print(*possible_matches, sep='\n')

def delete_book(number_of_book_to_delete):
        # TODO Checker méthode originelle!
        #Check for input which must be an int
        if int(number_of_book_to_delete):
            #Check for valid number
            LEN_OF_FILE = len(open("output.txt", 'r+').readlines())
            FILE = open('output.txt', "r+").readlines()
            print(FILE)
            if number_of_book_to_delete <= LEN_OF_FILE:
                print(f"Book wannabe deleted: {FILE[number_of_book_to_delete - 1]}")
                for line in FILE:
                    print(f"BOOK -- > {line}")
                    if line == FILE[int(number_of_book_to_delete) - 1]:
                        print("Yup")
                        open('output.txt', "w").write(line.replace(line, ""))
                    else:
                        open('output.txt', "a").write(line)

                #return f"{FILE[int(number_of_book_to_delete) - 1]} has been successfully deleted!"

            else:
                return "Number incorrect"

        else:
            return "NAN"

delete_book(1)
