import os
import pandas as pd

def addItem(item, price, stockFileLocation):
    if os.path.isfile(stockFileLocation):
        df = pd.DataFrame({'Item': item, 'Price': price}, index=[1])
        existingStock = pd.read_csv(stockFileLocation)
        newStock = existingStock.append(df, ignore_index=True)
        newStock.to_csv(stockFileLocation, index=False)
    else:
        print(f'No file was found at the given location {stockFileLocation}\nCreating new file at same location.')
        df = pd.DataFrame({'Item': item, 'Price': price}, index=[1])
        df.to_csv(stockFileLocation, index=False)
        print(f'{item} added to stock with price {price}.')
    

def isFloat(number):
    try:
        float(number)
        return True
    except:
        return False

while True:
    continueData = input('Would you like to add item to your stock? (y/n): ')
    if continueData == 'y':
        
        itemName = input('Enter Item name: ')
        itemPrice = input('Enter Item price: ')
        stockFileLocation = input('Enter Stock File location')

        if itemName == '':
            print('Item name cannot be blank\nPlease retry\n')
        elif not isFloat(itemPrice):
            print('Item Price connot be computed.\nPlease retry\n')
        else:
            addItem(itemName, itemPrice, stockFileLocation)



    elif continueData == 'n':
        break
    else:
        print('Invalid input, please retry.\n')
