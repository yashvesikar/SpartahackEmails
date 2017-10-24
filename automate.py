import csv
import pprint as pp

contacts = open("contacts.csv", "r")
budget = open("budget.csv", "r")

def cleanData(contacts,budget):
    data  = {}

    budget_reader = csv.reader(budget)
    contacts_reader = csv.reader(contacts)

    company_data = [] # List of tuples containing company name and previous years attendence
    sponsor_data = {} ## {company name: [(person name, email)]} structured sponsor info


    #Generates company data
    for company in budget_reader:
        company_data.append((company[0].lower(),company[9]))
    # Generates sponsor info
    total = 0
    for row in contacts_reader:
        row[0] = row[0].lower()
        if row[0] not in sponsor_data:
            sponsor_data[row[0]] = [(row[1].lower(),row[3])]
        elif row[0] in sponsor_data:
            sponsor_data[row[0]].append((row[1].lower(),row[3]))
    # Generates final data dictionary
    # Data structure : {(company name, last years response): [(person name, email)]}
    for company in company_data:
        if company[0] in sponsor_data:
            data[company] = sponsor_data[company[0]]

    for sponsor, contacts in data.items():
        people = set()
        keep = []
        for contact in contacts:
            # Checks for duplicate emails
            if contact[1] in people:
                continue
                # print("CONTACT: ",contact,"PEOPLE: ", keep)
            else:
                people.add(contact[1])
                keep.append(contact)

            # if contact[0] == '' or contact[0] == ' ':  #Checks for empty name
                # print("empty name: ",contact)
            data[sponsor] = keep
    # print(len(data))
    pp.pprint(data)
    return data

def filterData(myCompanies,alldata):
    filteredData = {}
    for sponsor, contacts in alldata.items():
        if sponsor[0] in myCompanies:
            filteredData[sponsor] = contacts
            print(sponsor[0])
    print(len(filteredData))
    return(filteredData)
    # for company in myCompanies:

    #     if company in

def fillTemplate(data,name):
    yourName = name
    never_resp = 0
    not_inter = 0
    comm_fell_through = 0

    responsefile = open("responses.txt",'w')

    for sponsor, contacts in data.items():
        # companyName =
        # contactName =
        if sponsor[1] == "Never responded":
            never_resp +=1
            response = """Hello,

My name is {yourName} and I'm on the Sponsorship team for SpartaHack IV, Michigan State University’s annual student-run hackathon. Last January, we welcomed over 600 student developers from around the country for the second-annual SpartaHack — a weekend where students of all skill levels and disciplines learned new technologies, got creative with tech, and connected with peers and company sponsors.

Since last January, our team has been hard at work on new designs, technologies, and ideas to make our 2018 event even better. We will bring together 500 students from MSU and beyond for another 36-hour coding marathon on the weekend of January 19-21, 2018.

We would love to partner with {company} this year to make SpartaHack IV an even bigger success. In the attached documents you will find more information about SpartaHack, including attendee statistics from last year and our updated sponsorship packages.

Please let us know whether you are interested in supporting SpartaHack IV. If you would prefer to set up a phone call, let me know when you are available in the next week. We look forward to working with you!

Thank you,
{yourName}
SpartaHack IV
""".format(yourName=yourName,company=sponsor[0])
            # print(response, sponsor[1].upper())
        elif sponsor[1] == "Not interested":
            not_inter+=1
            response = """Hello,

Last January, {company} helped our team put on an incredible hackathon for over 600 student developers. Because of your involvement, these students had an unparalleled opportunity to connect, learn, experiment, design, and ultimately drive the creation of a technical project from start to finish. Together, {company} and SpartaHack can make this happen again.

My name is {yourName} and I'm on the Sponsorship team for SpartaHack IV, Michigan
State University’s annual student-run hackathon. Since last January, our team has been hard at work on new designs, technologies, and ideas to make our 2018 event even better. We will bring together 500 students from around the country for another 36-hour coding marathon on the weekend of January 19-21, 2018.

{specific}, and we would love to work with you again this year. In the attached documents, you will find more information about SpartaHack, including attendee statistics from last year and our updated sponsorship packages.

Please let us know whether you are interested in returning for SpartaHack IV. If you would prefer to set up a phone call, let me know when you are available in the next week. I look forward to working with you!

Thank you,
{yourName}
""".format(yourName=yourName, company=sponsor[0],specific="***ENTER SOME SPECIFIC INFO HERE***")
        elif sponsor[1] == "Communication fell through":
            comm_fell_through+=1
            response = """Hello,

My name is {yourName} and I'm on the Sponsorship team for SpartaHack IV, Michigan State University’s annual student-run hackathon. Last January, we welcomed over 600 student developers from around the country for the second-annual SpartaHack — a weekend where students of all skill levels and disciplines learned new technologies, got creative with tech, and connected with peers and company sponsors.

Since last January, our team has been hard at work on new designs, technologies, and ideas to make our 2018 event even better. We will bring together 500 students from MSU and beyond for another 36-hour coding marathon on the weekend of January 19-21, 2018.

{specific} We would love to partner with {company} this year to make SpartaHack IV an even bigger success. In the attached documents you will find more information about SpartaHack, including attendee statistics from last year and our updated sponsorship packages.

Please let us know whether you are interested in supporting SpartaHack IV. If you would prefer to set up a phone call, let me know when you are available in the next week. We look forward to working with you!

Thank you,
{yourName}
SpartaHack IV
""".format(yourName=yourName,company=sponsor[0],specific="***INFO SPECIFIC TO WHY COMMUNICATION FELL THROUGH***")
        else:
            response = "Whoops! Make a pull request or write the email yourself!"
        # print("DEBUG CONTACTS: ", contacts)
        sponsor_info = ""
        for contact in contacts:
            sponsor_info += "Name: "+contact[0]+" Email: "+contact[1]+"\n"
        # print("*****DEBUG SPONSOR INFO*****", sponsor_info)
        responsefile.write("Company: "+sponsor[0].upper()+"\n\n")
        responsefile.write("Contacts: "+"\n"+sponsor_info+"\n\n")
        responsefile.write(response+"\n")
        responsefile.write("*"*120+"\n\n")
    responsefile.close()
    print("Never responded: ", never_resp, "Not interested: ", not_inter, "Communication Fell Through: ", comm_fell_through)
    print("Total: ", never_resp+not_inter+comm_fell_through)
def main():
    print("If you haven't already, make a textfile with your list of companies copied and pasted in from the budget on Google Drive")
    print("Save the file as companies.txt in the same folder")
    ready = input("Are you ready? y/n: ").lower()
    if ready == "y" or ready == "yes":
        myCompanies = []
        try:
            companiesFile = open("companies.txt",'r')
            for company in companiesFile:
                myCompanies.append(company.lower().strip("\n"))
            # print(len(myCompanies))
        except Exception as ex:
            print(ex.message)

        allData = cleanData(contacts,budget)
        filteredData = filterData(myCompanies,allData)
        myName = input("Please enter your name as it should be seen in the email: ")
        fillTemplate(filteredData,myName)
    else:
        print("Did you type yes?")



if __name__ == '__main__':
    # sys.exit(main(sys.argv)) # used to give a better look to exists
    main()
