import mysql.connector
import os

from Utilities import files


def getMySQLdb(authData):
    global g
    valid = False
    db = None
    while not valid:
        try:
            db = mySQLLogin(authData)
            valid = True
        except mysql.connector.errors.ProgrammingError as e:
            print("\nUser either doesn't exist, or the password is wrong\n{0}\n".format(e))
            g.setAuthData(user="None", password="None")
        except mysql.connector.errors.DatabaseError as e:
            print("\nNo database seems to exist as the host provided or the host doesn't exist\n{0}\n".format(e))
            g.setAuthData(host="None")
            print(e)
        authData = g.getAuthData()
    return db


def mySQLLogin(authData):
    db = mysql.connector.connect(
        host=authData["host"],
        user=authData["user"],
        password=authData["password"]
    )
    return db


def setupDatabase(authData, databaseName):
    db = getMySQLdb(authData)
    cursor = db.cursor()
    # cursor.execute("DROP DATABASE {0}".format(databaseName))
    cursor.execute("create database if not exists {0};".format(databaseName))
    cursor.execute("USE {0}".format(databaseName))

    cursor.execute("create table if not exists Users (id varchar(25) primary key not null, username varchar(25) not null)")
    cursor.execute("create table if not exists Items (id varchar(25) not null, userID varchar(25) not null, foreign key (userID) references Users(id))")
    return db


def mySQLCommandLine(db):
    cursor = db.cursor()
    print("Entered MySQL Command Line - leave as blank to exit")
    while True:
        inputted = input("MySQL: ")
        if inputted == "":
            break
        else:
            try:
                cursor.execute(inputted)
                for x in cursor:
                    print(x)
            except mysql.connector.errors.ProgrammingError as e:
                print(e)


def main():
    db = setupDatabase(g.getAuthData(), g.getDatabaseName())
    mySQLCommandLine(db)


class Globals:
    def __init__(self):
        # Global variables #
        self.usersDir = "User/"
        self.authPath = "auth.json"
        self.databaseName = "pyTest"
        self.authData = {}

        self.setup()

    def setup(self):
        # Todo check that usersDir has "/" on the last char
        if not os.path.isdir(self.getUsersDir()):
            print("Created {0}".format(self.usersDir))
            os.mkdir(self.usersDir)
        self.getAuthData()

    def getAuthData(self):
        if self.authData == {}:
            authData = files.openJSON(self.getUsersDir() + self.getAuthPath())
            if authData == {}:
                self.setAuthData()
            else:
                self.__setAuthData(authData)
        return self.authData

    def setAuthData(self, host="localhost", user="root", password=""):
        # Setting any variable to "None" (as a string because pycharm complains, and it looks ugly)
        # will induce a prompt to update it
        if host == "None":
            host = input("Please input the MySQL host: ")
        if user == "None":
            user = input("Please input the MySQL user for '{0}': ".format(host))
        if password == "None":
            password = input("Please input the MySQL password for '{0}': ".format(user))
        authData = {"host": host,
                    "user": user,
                    "password": password}
        if authData != self.authData:
            self.__setAuthData(authData)
        return authData

    def __setAuthData(self, authData):
        files.writeJSON(self.getUsersDir() + self.getAuthPath(), authData)
        self.authData = authData

    def getUsersDir(self):
        return self.usersDir

    def getDatabaseName(self):
        return self.databaseName

    def getAuthPath(self):
        return self.authPath


if __name__ == '__main__':
    g = Globals()
    main()
