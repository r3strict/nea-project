"""
NOTES:

# All of the 'countdown' variables or code that counts down in runtime are cosmetic when in use - they give a feel to the program that it's loading. 
# Code with comments on them are either WIPs that need to be fixed, or code that has been left for later development.
# There is a documentation at the very bottom which shows my development notes from 11/05/22.

"""

# Importing necessary modules
import re
import random
import time
from bisect import insort

# Setting our global variables
global total_points
global total_lives
global counter

total_points = 0
total_lives = 2
counter = 1


# Creates an instance of an account
class Account:
    # Holds all the accounts within a class dictionary
    allAccounts = {}

    def __init__(self, username, password):
        self.allAccounts[username] = self
        self.password = password


# Creates an instance of a song
class Song:
    # Holds all the songs within a class dictionary
    allSongs = {}

    def __init__(self, song_name, artist, creation_date):
        self.allSongs[song_name] = self
        self.song_name = song_name
        self.artist = artist
        self.creation_date = creation_date

    # Formats the song details into a specific order
    def print_details(self):
        x1 = ""
        for x in range(0, len(self.song_name)):
            # If a space is found then print the character right after it
            if self.song_name[x] == ' ':
                letter = self.song_name[x + 1]
                # Prints each first letter per word in a song separately from each song with one word in it
                x1 = x1 + ' ' + letter
        # Separates the first letter in each word of the song to make it readable      
        print('The first letter(s) of the song are: ', self.song_name[0], x1, sep='')
        print('The artist of the song is:', self.artist), time.sleep(0)
        print("The song's creation date is:", self.creation_date)


class Scores:
    # Holds all the scores within a class list
    allScores = []

    def __init__(self, name, points, lives):
        self.name = name
        self.points = points
        self.lives = lives
        insort(self.allScores, self)

    def __gt__(self, other):
        if self.points == other.points:
            return self.lives < other.lives
        else:
            return self.points < other.points


# Randomises the songs when printed
def get_random_song():
    return random.choice(list(Song.allSongs))


def load_accounts_and_songs_and_scores():
    # Loading all accounts in
    with open('accounts.txt') as file:
        for line in file:
            # Strips the line of any new lines
            line = line.rstrip()
            # Splits the line by a : and assigns it into the corresponding variables
            username, password = re.split('[:]', line)
            # Initialising the Account object
            Account(username, password)

    # Loading all songs in
    with open('songs.txt') as songs:
        for song_line in songs:
            # Strips the line of any new lines
            song_line = song_line.rstrip()
            # Splits the line by a : and assigns it into the corresponding variables
            song_name, artist, creation_date = re.split('[:]', song_line)
            # Initialising the Song object
            Song(song_name, artist, creation_date)

    # Loading all the scores in
    with open('leaderboards.txt') as scores:
        for score_line in scores:
            # Strips the line of any new lines
            score_line = score_line.rstrip()
            # Splits the line by a : and assigns it into the corresponding variables
            name, lives, points = re.split('[:]', score_line)
            # Initialising the Scores object
            Scores(name, lives, points)


def display_start_menu():
    print('Welcome to the Music Quiz Menu!')
    print('Please choose from one of the options available (1/2/3):'
          '\n'
          '\n1. Register'
          '\n2. Login'
          '\n3. Leaderboards'
          '\n4. Quit')

    # Loops the start menu until the user has correctly picked an option
    while True:
        try:
            menu_choice = int(input('\nPlease enter your desired option: '))
        except ValueError:
            print('Please enter an integer.')
            continue
        else:
            if menu_choice == 1:
                register()
                break
            elif menu_choice == 2:
                login()
                break
            elif menu_choice == 3:
                leaderboards()
                break
            elif menu_choice == 4:
                print('The program will now close!'), time.sleep(1)
                quit()
            else:
                print('Please choose from one of the options available.')


def register():
    print('\nWelcome to the registration page.')

    # Setting the user's new account with their sign in credentials
    while True:
        username = input('Please create a username: ')
        if username in Account.allAccounts.keys():
            print('The username is already taken. Please choose another username.\n')
        else:
            break

    password = input('Please create a password: ')

    # Saving the account to the 'accounts.txt' file
    with open('accounts.txt', 'a') as f:
        f.write(username + ':' + password + '\n')

    # Creating a new Account object with the given details
    Account(username, password)
    print('Your account has been created!\n')

    # Redirecting the user back to the Music Quiz Menu
    display_start_menu()


def quiz_loss():
    global total_lives
    global total_points
    global counter

    print("\nYou've lost the quiz!")

    while True:
        try:
            quizlost = int(input(
                '\n1) Main menu'
                '\n2) Quit'
                '\n\nPick an option: '))

            # Returns back to the options if an invalid integer or option is entered
        except ValueError:
            print('\nPlease enter an integer.')
            continue

        else:
            if quizlost == 1:
                print('Redirecting to the main menu.', end=''), time.sleep(0.5)
                print('.', end=''), time.sleep(0.5)
                print('.\n'), time.sleep(0.5)

                # Resets the lives, points and counter variables back to the default values
                while total_lives < 2:
                    total_lives += 1
                if total_lives == 2:
                    pass

                while total_points > 0:
                    total_points -= 1
                if total_points == 0:
                    pass

                while counter != 1:
                    counter += 1
                    if counter == 1:
                        pass

                # Returns back to the main menu
                display_start_menu()
                break


            # Quits the program
            elif quizlost == 2:
                print('Quitting.', end=''), time.sleep(0.5)
                print('.', end=''), time.sleep(0.5)
                print('.'), time.sleep(0.5)
                quit()

            else:
                print('Please enter one of the 2 options.')


def extralife():
    global total_lives
    global total_points

    print('\nHave you lost a life?')

    while True:
        try:
            # Asks the user if they lost a life or not
            life_given = int(input("If so, please say '1' to obtain a life. Otherwise, say '2' to move on: "))

        except ValueError:
            # Returns back to the question if the user typed in an incorrect option
            print('\nPlease enter a correct option.')
            continue

        else:
            if life_given == 1:
                # If the user already has maximum lives and they try to cheat, the program quits itself
                if total_lives >= 2:
                    print('\nStop trying to cheat!')
                    print('The game will not save your progress.')
                    print('\nQuitting.', end=''), time.sleep(1)
                    print('.', end=''), time.sleep(1)
                    print('.'), time.sleep(1)
                    quit()
                else:
                    while total_lives < 2:
                        total_lives += 1
                    if total_lives == 2:
                        print('\nYour life has been given!\n'), time.sleep(1)
                        break

            # Skips the whole process and just moves on if the user declined the offer  
            elif life_given == 2:
                print('No lives given. Moving on to the next question...\n\n')
                break


def leaderboards():

    if len(Scores.allScores) > 4:
        leaderboard_size = 5
    else:
        leaderboard_size = len(Scores.allScores)

    for n in range(0, leaderboard_size):
        currentScore = Scores.allScores[n]
        print("\n", n+1, ")", currentScore.name + " :", currentScore.points, "points :", currentScore.lives, "lives")


def quiz_win():
    global total_lives
    global total_points
    global counter

    print('\nYou won the quiz!\n')

    def lbs2():
        username = input('Please enter your username: ')
        points = str(total_points)
        lives = str(total_lives)

        if username in Account.allAccounts.keys():
            with open('leaderboards.txt', 'a') as f:
                f.write(username + ':' + points + ':' + lives + '\n')
                print('\nYour score has been saved!')
                pass

        else:
            print('\nPlease re-enter your username.\n'), time.sleep(0.75)
            lbs2()

    lbs2()

    while True:
        try:
            # Asks the user to pick an option
            win = int(input(
                '\n'
                '1) Main menu\n'
                '2) Quit\n'
                '3) Leaderboards\n'
                '\nPlease pick an option: '))

        except ValueError:
            print('Please enter an integer.')
            continue

        else:
            if win == 2:
                print('Quitting.', end=''), time.sleep(0.5)
                print('.', end=''), time.sleep(0.5)
                print('.', end=''), time.sleep(0.5)
                quit()

            elif win == 1:
                print('Redirecting to the main menu.', end=''), time.sleep(0.5)
                print(' .', end=''), time.sleep(0.5)
                print(' .\n'), time.sleep(0.5)

                # Resets the lives, points and counter variables back to the default values
                while total_lives != 2:
                    total_lives += 1
                if total_lives == 2:
                    pass

                while total_points > 0:
                    total_points -= 1
                if total_points == 0:
                    pass

                while counter != 1:
                    counter += 1
                if counter == 1:
                    pass

                # Returns back to the main menu
                display_start_menu()
                break

            elif win == 3:
                leaderboards()
                break

            else:
                print('Please enter one of 3 options.'), time.sleep(0.75)


def question5():
    global total_lives
    global total_points
    global counter

    # Runs the quiz_loss() subroutine if you fail to answer the question twice (losing the game)
    if total_lives < 1:
        quiz_loss()

    # Uses the counter variable to make sure the extralife() will not run more than once per question
    if counter != 1:
        pass
    else:
        extralife()

    # Prints the random song details
    random_song = get_random_song()
    Song.allSongs[random_song].print_details()

    question_5 = input('\nWhat is the name of the song?: ').casefold()

    if total_lives == 1 and question_5 == random_song.casefold():
        # Gives the player 1 point for scoring the song correctly the second time
        print('\nCorrect! ')
        total_points += 1
        print('You have', total_lives, 'life(s) and', total_points, 'point(s).')
        quiz_win()

    elif total_lives == 2 and question_5 == random_song.casefold():
        # Gives the player 3 points for scoring the song correctly first time
        print('\nCorrect! ')
        total_points += 3
        print('You have', total_lives, 'life(s) and', total_points, 'point(s).')
        quiz_win()

    elif question_5 != random_song.casefold():

        # Removes a life if the player got a question wrong the first time
        counter -= 2
        total_lives -= 1
        print('\nIncorrect answer.\n')
        question5()


def question4():
    global total_lives
    global total_points
    global counter

    # Runs the quiz_loss() subroutine if you fail to answer the question twice (losing the game)
    if total_lives < 1:
        quiz_loss()

    # Uses the counter variable to make sure the extralife() will not run more than once per question
    if counter != 1:
        pass
    else:
        extralife()

    # Prints the random song details
    random_song = get_random_song()
    Song.allSongs[random_song].print_details()

    question_4 = input('\nWhat is the name of the song?: ').casefold()

    if total_lives == 1 and question_4 == random_song.casefold():
        # Gives the player 1 point for scoring the song correctly the second time
        print('\nCorrect! ')
        while counter != 1:
            counter += 1
            if counter == 1:
                break

        total_points += 1

        print('You have', total_lives, 'life(s) and', total_points, 'point(s).')
        question5()

    elif total_lives == 2 and question_4 == random_song.casefold():
        # Gives the player 3 points for scoring the song correctly first time
        print('\nCorrect! ')
        while counter != 1:
            counter += 1
            if counter == 1:
                break
        total_points += 3
        print('You have', total_lives, 'life(s) and', total_points, 'point(s).')
        question5()

    elif question_4 != random_song.casefold():
        # Removes a life if the player got a question wrong the first time
        counter -= 2
        total_lives -= 1
        print('\nIncorrect answer.\n')
        question4()


def question3():
    global total_lives
    global total_points
    global counter

    # Runs the quiz_loss() subroutine if you fail to answer the question twice (losing the game)
    if total_lives < 1:
        quiz_loss()

    # Uses the counter variable to make sure the extralife() will not run more than once per question
    if counter != 1:
        pass
    else:
        extralife()

    # Prints the random song details
    random_song = get_random_song()
    Song.allSongs[random_song].print_details()

    question_3 = input('\nWhat is the name of the song?: ').casefold()

    if total_lives == 1 and question_3 == random_song.casefold():
        # Gives the player 1 point for scoring the song correctly the second time
        print('\nCorrect! ')
        while counter != 1:
            counter += 1
            if counter == 1:
                break

        total_points += 1
        print('You have', total_lives, 'life(s) and', total_points, 'point(s).')
        question4()

    elif total_lives == 2 and question_3 == random_song.casefold():
        # Gives the player 3 points for scoring the song correctly first time
        print('\nCorrect! ')
        while counter != 1:
            counter += 1
            if counter == 1:
                break

        total_points += 3

        print('You have', total_lives, 'life(s) and', total_points, 'point(s).')
        question4()

    elif question_3 != random_song.casefold():
        counter -= 2
        total_lives -= 1
        # Removes a life if the player got a question wrong the first time
        print('\nIncorrect answer.\n')
        question3()


def question2():
    global total_lives
    global total_points
    global counter

    # Runs the quiz_loss() subroutine if you fail to answer the question twice (losing the game)
    if total_lives < 1:
        quiz_loss()

    # Uses the counter variable to make sure the extralife() will not run more than once per question
    if counter != 1:
        pass
    else:
        extralife()

    # Prints the random song details
    random_song = get_random_song()
    Song.allSongs[random_song].print_details()

    question_2 = input('\nWhat is the name of the song?: ').casefold()

    if total_lives == 1 and question_2 == random_song.casefold():
        # Gives the player 1 point for scoring the song correctly the second time
        print('\nCorrect! ')
        while counter != 1:
            counter += 1
            if counter == 1:
                break

        total_points += 1
        print('You have', total_lives, 'life(s) and', total_points, 'point(s).')
        question3()

    elif total_lives == 2 and question_2 == random_song.casefold():
        # Gives the player 3 points for scoring the song correctly first time
        print('Correct! ')
        while counter != 1:
            counter += 1
            if counter == 1:
                break

        total_points += 3

        print('You have', total_lives, 'life(s) and', total_points, 'point(s).')
        question3()

    elif question_2 != random_song.casefold():
        counter -= 2
        # Removes a life if the player got a question wrong the first time
        total_lives -= 1
        print('\nIncorrect answer.\n')
        question2()


def question1():
    global total_lives
    global total_points

    # Runs the quiz_loss() subroutine if you fail to answer the question twice (losing the game)
    if total_lives < 1:
        quiz_loss()

    # Prints the random song details
    random_song = get_random_song()
    Song.allSongs[random_song].print_details()

    question_1 = input('\nWhat is the name of the song?: ').casefold()

    if total_lives == 1 and question_1 == random_song.casefold():
        # Gives the player 1 point for scoring the song correctly the second time
        print('\nCorrect! ')
        total_points += 1
        print('You have 1 life(s) and', total_points, 'point(s).')
        question2()

    elif total_lives == 2 and question_1 == random_song.casefold():
        # Gives the player 3 points for scoring the song correctly first time
        print('Correct! ')
        total_points += 3
        print('You have', total_lives, 'life(s) and', total_points, 'point(s).')
        question2()

    elif question_1 != random_song.casefold():
        # Removes a life if the player got a question wrong the first time
        print('\nIncorrect answer.\n')
        total_lives -= 1
        question1()


def quiz():
    # Prints the rules
    print("\n\nWelcome to the music quiz! Let's get some rules down.\n")
    print('The quiz will consist of a list of songs, artist and release date of the song.'
          '\nYou will get 3 points for getting the song right the first time and then 1 point if you get it wrong once, then correct.')
    print(
        'However, only the first letter of each word within the song will be given to you.\n\nGood luck!\n'), time.sleep(
        3)
    question1()


def login():
    print('\nWelcome to the login page.')

    # Ask the user to enter their credentials
    username = input('Please enter your username: ')
    password = input('Please enter your password: ')

    try:
        authenticatedUser = (Account.allAccounts[username].password == password)
    except KeyError:
        authenticatedUser = False
    finally:
        if authenticatedUser:
            print('\nWelcome ', username, '!')
            quiz()

        else:
            print('The account credentials are incorrect. You will be returned to the menu.\n')
            display_start_menu()


load_accounts_and_songs_and_scores()
display_start_menu()

# big thanks to roman for helping me with the code at home :)


"""
Documenting this as I want to note this for future reference and show development

11/05/22 - I got the case sensitive-ness to disappear; I used '.casefold()' to allow any sort of capitalisation on the input of songs, regardless whether it is all capitals, etc.
           My next plan is to then get the leaderboard working; I need to make it so that it prints the top 5 scores from top to bottom, then print the current user's score separately from that too.
           I currently still do not know how to use classes fluently or even know how they fully work yet but I will soon. (Andy)

12/05/22 - I finally got the 'def print_details(self)' to finally work!! I had to find some for loop online that prints the first letter of every word in a song. I had to mess around and add a '' variable
           because for some reason if I did just 'pass' in the elif statement (refer back to the class Song to understand all this) then it would mess up and not print properly in my case. (Andy)
           
13/05/22 - Turns out the documentation above was false for songs with 2 or more words. So I asked the Python Discord server and someone told me to use " sep='' ". It worked in the end, and now can print any amount
           of words without restriction. (Andy)
           
next/date/here - (documentation)
           
13/05/2022 - Ryan edited this

"""
