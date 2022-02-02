import pandas as pd
import os
import datetime

# Variabel declaration

shopData = {}
billData = {'customerDetails': [], 'billItems': []}
pageWidth = 165


if not os.path.isfile('users.csv'):
    df = pd.DataFrame(columns=['Username', 'Password', 'shopName', 'shopAddress', 'shopContact'])
    df.to_csv('users.csv', index=False)



# Function declaration

def isFloat(number):
    try:
        float(number)
        return True
    except:
        return False



def login():
    '''Takes username and password as input and authenticate the user'''


    print('\nPlease provide login details')

    username = input('Enter Username: ')
    password = input('Enter Password: ')

    userDetails = pd.read_csv('users.csv')

    if username in userDetails['Username'].tolist():
        if password in (userDetails.loc[userDetails['Username'] == username])['Password'].tolist():

            currentUserDetails = userDetails.loc[userDetails['Username'] == username]

            shopData['LogedIn'] = True
            shopData['shopName'] = currentUserDetails['shopName'].tolist()[0]
            shopData['shopAddress'] = currentUserDetails['shopAddress'].tolist()[0]
            shopData['shopContact'] = currentUserDetails['shopContact'].tolist()[0]
            shopData['shopUsername'] = currentUserDetails['Username'].tolist()[0]
            shopData['shopPassword'] = currentUserDetails['Password'].tolist()[0]

            print('Login Successful')


        else:
            print('Invalid Credentials\nPlease retry')
            user()
    else:
        print('Invalid Credentials\nPlease retry')
        user()



def signUp():
    '''Regesters a new user'''

    print('\nWelcome to bill generator\nPlease provide following details to register: ')

    shopName = input('Enter shop name: ')
    shopAddress = input('Enter shop Address: ')
    shopContact = input('Enter contact: ')
    username = input('Enter Username: ')
    password = input('Enter Password: ')

    for detail in [shopName, shopAddress, shopContact, username, password]:
        if detail == '':
            print('All Details not provided, please retry')
            print('-'*50)
            signUp()

    data = {'Username':username, 'Password': password, 'shopName':shopName, 'shopAddress':shopAddress, 'shopContact':shopContact}
    toAddDataFrame = pd.DataFrame(data, index=[1])
    oldDataFrame = pd.read_csv('users.csv')

    newDataFrame = oldDataFrame.append(toAddDataFrame, ignore_index= False)
    newDataFrame.to_csv('users.csv', index = False)

    print('Details Saved, please login')
    login()



def user():
    '''Check for existing user and forward to login page or to signup page'''

    existingUser = input('Are you an existing user (y/n): ')

    if existingUser.lower() == 'y':
        login()

    elif existingUser.lower() == 'n':
        signUp()


    else:
        print('Invalid input\nPlease retry\n')
        user()


def generateBill():
    stockFileLocation = input("Please provide stock file location (.csv file): ")
    if not os.path.isfile(stockFileLocation):
        print('File not found. Check the input and retry.\n')
        generateBill() 
    else:
        customerName = input('Enter customer name: ')
        customerContact = input('Enter customer contact: ')
        billData['customerDetails'] = [customerName, customerContact]
        stock = pd.read_csv(stockFileLocation)
        while True:
            itemName = input('ItemName: ')

            if itemName in stock['Item'].tolist():
                itemPrice = (stock.loc[stock['Item'] == itemName])['Price'].tolist()[0]
            else:
                print(f'{itemName}, not found in stock file.\nPlease retry.')
                continue

            itemQuantity = input('Quantity: ')

            if isFloat(itemQuantity):
                billData['billItems'].append([itemName, itemPrice, float(itemQuantity), itemPrice*float(itemQuantity)])
            else:
                print('Quantity can not be processed')
                continue

            continueAddItem = input('Enter \'y\' to add more item: ')

            if continueAddItem.lower() == 'y':
                continue
            else:
                print(printBill())
                break


def printBill():
    print('-'*pageWidth)
    print(' '*((pageWidth-len(shopData['shopName']))//2) + shopData['shopName'] + ' '*((pageWidth-len(shopData['shopName']))//2))
    print(' '*((pageWidth-len(shopData['shopAddress']))//2) + shopData['shopAddress'] + ' '*((pageWidth-len(shopData['shopAddress']))//2))
    print(' '*((pageWidth-len(shopData['shopContact']))//2) + shopData['shopContact'] + ' '*((pageWidth-len(shopData['shopContact']))//2))
    print('-'*pageWidth)
    print('Customer Name: ' + billData['customerDetails'][0] + ' '*(pageWidth - (len('Customer Name: ' + billData['customerDetails'][0]) + len('Date/Time: ' + datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S')))) + 'Date/Time: ' + datetime.datetime.now().strftime('%d-%m-%y %H:%M:%S'))
    print('Customer contact: '+ billData['customerDetails'][1])
    print('-'*pageWidth)


def main():
    user()
    createBill = input('Do you want to create a bill?(y/any key to exit)')
    if createBill.lower() == 'y':
        generateBill()
    else:
        pass

main()
