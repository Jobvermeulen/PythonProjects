import csv

# Author Job Vermeulen
# Build V0.1
# Date 20/08/2019

# startUp class
class startUp:
    # initialize (csv_save_file == where is the csv file saved)
    def __init__(self, csv_save_file, csv_startTime_file, fieldNames):
        self.csv_save_file = csv_save_file
        self.csv_startTime_file = csv_startTime_file
        self.fieldNames = fieldNames
    
    # startProgram, what does the TickIn program needs to do
    # Switch, multiple options:
    # 0.create new TickIn (save point)
    # 1.create new TickIn with only starting time
    # 2.add stopping time to TickIn
    def startProgram(self):
       print("What do you want me to do?")
       print(" 0. create new TickIn \n 1. start new TickIn \n 2. stop TickIn")
       self.switch(int(input("What's it gonna be?")))

    def switch(self, value):
        tickIn = TickIn(self.csv_save_file, self.csv_startTime_file, self.fieldNames)
        switcher = {
            0: tickIn.newTickIn,
            1: tickIn.startTickIn,
            2: tickIn.addTickInStopTime
        }
        switcher.get(value, "nothing")()

class TickIn:
    def __init__(self, csv_save_file, csv_startTime_file, fieldNames):
        self.csv_save_file = csv_save_file
        self.csv_startTime_file = csv_startTime_file
        self.fieldNames = fieldNames

    # create new TickIn (save point)
    def newTickIn(self):
        print("\nLets create a new TickIn!")

        questions = Questions()

        questions.containsFollowing() 
        questions.printName() 
        questions.printDescription()
        questions.printStartTime()
        questions.printEndTime()
        questions.printDate()
        
        name = questions.tickInName()
        description = questions.tickInDescription()
        startTime = questions.tickInStartTime()
        endTime = questions.tickInEndTime()
        date = questions.tickInDate()

        try:
            self.save_to_csv(self.csv_save_file,'a',name,description,float(startTime),float(endTime),date)
            questions.success()
        except:
            questions.error()
        
    def startTickIn(self):
        print("\nLets start a new TickIn!")

        questions = Questions()

        questions.containsFollowing()
        questions.printName() 
        questions.printDescription()
        questions.printStartTime()
        questions.printDate()

        name = questions.tickInName()
        description = questions.tickInDescription()
        startTime = questions.tickInStartTime()
        endTime = 0
        date = questions.tickInDate()

        try:
            self.save_to_csv(self.csv_startTime_file,'a',name,description,float(startTime),float(endTime),date)
            questions.success()
        except:
            questions.error()

    # add stopping time to TickIn
    def addTickInStopTime(self):
        print("\nLets complete a TickIn!")

        questions = Questions()

        questions.containsFollowing()
        questions.printName() 
        questions.printEndTime()
        questions.printDate()
        
        name = questions.tickInName()
        endTime = questions.tickInEndTime()
        date = questions.tickInDate()

        try:
            self.addStopTime(name,date,endTime)
            questions.success()
        except:
            questions.error()

    # Save to the main csv file OR to the only start tickins csv file
    def save_to_csv(self, File, mode, name, description, startingTime, endTime, date):
        with open(File, mode=mode) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldNames)
            timediff = endTime - startingTime
            writer.writerow({'TickIn name': name, 'Description': description, 'Starting time': startingTime, 'End time': endTime, 'Time difference' : timediff,'Date': date})

    # Add the endtime to an excisting tickin
    # starttime(save file for only start tickins) -> TickIn(main save file)
    def addStopTime(self, name, date, endTime):
        with open(self.csv_startTime_file, 'r') as inp, open(self.csv_save_file, 'a') as out:
            writer = csv.DictWriter(out, fieldnames=self.fieldNames)
            for row in csv.reader(inp):
                if ((row[0] == name) and (row[5] == date)):
                    timediff = float(endTime) - float(row[2])
                    writer.writerow({'TickIn name': name, 'Description': row[1], 'Starting time' : row[2], 'End time' : endTime, 'Time difference' : timediff, 'Date' : date})
                    break

class Questions:
    def tickInName(self):
        name = input("What's the name of your TickIn? ")
        return name

    def tickInDescription(self):
        description = input("What's the description of your TickIn? ")
        return description

    def tickInStartTime(self):
        startTime = input("What's the starting time of your TickIn? \nTime needs in this format 00.00 ")
        return startTime

    def tickInEndTime(self):
        endTime = input("What's the end time of your TickIn? \nTime needs in this format 00.00 ")
        return endTime
    
    def tickInDate(self):
        date = input("On what date was your TickIn? ")
        return date
    
    def containsFollowing(self):
        print("This contains the following questions:")

    def printName(self):
        print("• What's the name of your TickIn?")

    def printDescription(self):
        print("• What's the description of your TickIn?")

    def printStartTime(self):
        print("• What's the starting time of your TickIn?")
    
    def printEndTime(self):
        print("• What's the end time of your TickIn?")

    def printDate(self):
        print("• On what date was your TickIn?\n")

    def success(self):
        print("(☞ﾟ∀ﾟ)☞  Your TickIn has been saved! \n")

    def error(self):
        print("There was an error while saving the file ¯\_(ツ)_/¯")

# main
def main():
    # the main save file
    csv_save_file = 'TickIn.csv'
    # the save file for only start tickins
    csv_startTime_file = 'startTime.csv'
    # Column names of the csv file
    fieldnames = ['TickIn name', 'Description', 'Starting time', 'End time', 'Time difference', 'Date']
    startup = startUp(csv_save_file, csv_startTime_file, fieldnames)
    startup.startProgram()

if __name__ == "__main__":
    main()