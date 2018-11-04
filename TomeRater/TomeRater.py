import re #optional: import to check email using regular expression (is_email)



init_info = True #optional: print extra init info (or not)

def is_email(email):
    if re.match(r"[^@]+@[^@]+\.[com|edu|org]+", email):
        return True
    else:
        return False



class TomeRater:
 
    def __init__(self):
        self.users = {}
        self.books = {}


    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)


    def add_user(self, name, email, user_books=None):
        if (is_email(email)): #extra error testing: check if email is correct (and within com/edu/org)
            if (email not in self.users): #extra error testing: check if email is unique
                self.users.update({email:User(name, email)})
                if (user_books):
                    for book in user_books:
                        self.add_book_to_user(book, email)
            else:
                print("Warning! User \"{name}\" with email \"{email}\" already exists!".format(name=name, email=email))
        else:
            print("Warning! User \"{name}\" has an invalid email: \"{email}\"!".format(name=name, email=email))


    def add_book_to_user(self, book, email, rating=None):
        if email in self.users:
            self.users[email].read_book(book, rating) 
            
            if rating!=None:
                book.add_rating(rating)
                if init_info: 
                    print("User with email \"{email}\" has read \"{book}\" (rating = {rating}).".format(email=email, book=book, rating=rating))
            else:
                if init_info:
                    print("User with email \"{email}\" has read \"{book}\" (no rating) ".format(email=email, book=book))

            if book in self.books:
                self.books.update({book:self.books[book]+1})
            else:
                self.books.update({book:1})
        else:
            print("Warning! No user with email {email}!\n".format(email=email))


            

    def print_catalog(self, extra_info=False): #optional: print with extra info
        print("Catalog:")
        for book in self.books:
            print("-", book)
            if extra_info:
                print("\tavarage rating: ", float("{0:.1f}".format(book.get_average_rating()))) #optional: round floats
                print("\ttotal reads: ", self.books[book]) 

    def print_users(self, extra_info=False): #optional: print with extra info
        print("Users:")
        for user in self.users:
            print("-", user)
            if extra_info:
                print("\tavarage rating: ", float("{0:.1f}".format(self.users[user].get_average_rating()))) #optional: round floats



    def most_positive_user(self):
        most_positive_rating = 0        
        most_positive_users = [] #optional: add ex aequo option
        for user in self.users:
            avarage_user_rating = self.users[user].get_average_rating()
            if avarage_user_rating > most_positive_rating:
                most_positive_rating = avarage_user_rating
                most_positive_users = [user]
            elif avarage_user_rating == most_positive_rating:
                most_positive_users.append(user)
        return most_positive_users

    def highest_rated_book(self):
        highest_rated_number = 0        
        highest_rated_books = [] #optional: add ex aequo option        
        for book in self.books:
            book_rating = book.get_average_rating()
            if book_rating > highest_rated_number:
                highest_rated_number = book_rating
                highest_rated_books = [book]
            elif book_rating == highest_rated_number:
                highest_rated_books.append(book)
        return highest_rated_books

    def most_read_book(self):
        most_read_number = 0
        most_read_books = [] #optional: add ex aequo option
        for book in self.books:
            book_reads = self.books[book]
            if self.books[book] > most_read_number: 
                most_read_number = book_reads
                most_read_books = [book]
            elif self.books[book] == most_read_number:
                most_read_books.append(book)
        return most_read_books

    def __repr__(self):
        return "TomeRater:\n- users: " + str(len(self.users)) + "\n- books: " + str(len(self.books))



class User(object):

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}
        if init_info:
            print("User \"{name}\" with email \"{email}\" has been added.".format(name=self.name, email=self.email))

    def get_email(self):
        return self.email

    def change_email(self, address):
        if (is_email(email)): #extra error testing: check if email is correct (and within com/edu/org)
            self.email = address 
            print("User {name} his/her email has been updated to {email}".format(name=self.name, email=self.email))
        else:
            print("Warning! Email cannot be changed - invalid new email: \"{email}\"!".format(email=email))


    def read_book(self, book, rating=None):
        self.books[book] = rating 

    def get_average_rating(self):
        sum_ratings = 0
        total_ratings = 0
        for value in self.books.values():
            if (value != None): #optional: added extra check because 'None' rating shouldn't influence the average
                sum_ratings += value
                total_ratings += 1 
        if total_ratings > 0: #optional: avoid /0
            return sum_ratings / total_ratings 
        else:
            return 0

    def __repr__(self):
        return "User {user}, email: {email}, books read: {books}".format(user=self.name, email=self.email, books=len(self.books))

    def __eq__(self, other_user):
        if (self.name==other_user.name and self.email==other_user.email):
            return True
        else:
            return False



class Book:

    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []
        if init_info:
            print("Book \"{title}\" with ISBN \"{isbn}\" has been instantiated.".format(title=title, isbn=isbn))

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("Book \"{name}\" its ISBN has been updated to \"{isbn}\".".format(name=self.title, isbn=str(self.isbn)))

    def add_rating(self, rating):
        if (rating!=None and rating>=0 and rating<=4):
            self.ratings.append(rating)
        elif (rating != None): #optional: added an extra check because 'None' rating isn't necessary invalid
            print("Warning! Invalid Rating (0-4) for \"{title}\"".format(title=self.title))

    def get_average_rating(self):
        sum_ratings = 0
        total_ratings = 0
        for rating in self.ratings:
            sum_ratings += rating
            total_ratings += 1
        if total_ratings>0: #optional: avoid /0
            return sum_ratings / total_ratings
        else:
            return 0

    def __eq__(self, other_book):
        if (self.title==other_book.title and self.isbn==other_book.isbn):
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "{title}".format(title=self.title)



class Fiction(Book):

    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)



class Non_Fiction(Book):

    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        first_letter_level = self.level[0] #optional: check if level starts with vowel or consonant (a/an)
        if first_letter_level in ["a", "e", "i", "o", "u"]:
            article = "an"
        else:
            article = "a"
        return "{title}, {article} {level} manual on {subject}".format(title=self.title, article=article, level=self.level, subject=self.subject)
