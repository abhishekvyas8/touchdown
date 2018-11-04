##################
# For testing
amount = 0
##################

from authorizenet import apicontractsv1
from authorizenet.apicontrollers import*
from decimal import*
from firebase import firebase
from authorizenet import apicontractsv1
from authorizenet.apicontrollers import createTransactionController
import os
import sys
import imp

f = firebase.FirebaseApplication('https://brobet-221407.firebaseio.com', None)
'''
user1 = f.get('/Bets/vyas6SC', 'User1')
print(user1)

user2 = f.get('/Bets/vyas6SC', 'User2')
print(user2)

team1 = f.get('/Bets/vyas6SC','Team1')
print(team1)

team2 = f.get('/Bets/vyas6SC', 'Team2')
print(team2)
'''
user1 = f.get('Bets/vyas6UK', 'User1')
user2 = f.get('Bets/vyas6UK', 'User2')
ratio1 = int(f.get('Bets/vyas6UK', 'Ratio1'))
ratio2 = int(f.get('Bets/vyas6UK', 'Ratio2'))
winner = f.get('Bets/vyas6UK', 'Winner').lower()
initialAmount = int(f.get('Bets/vyas6UK', 'Amount'))


if(user1 != winner):
    loser = user1.lower()
else:
    loser = user2.lower()

# Compare the final scores to determine winner
CONSTANTS = imp.load_source('modulename', 'constants.py')

amount = initialAmount * (ratio1 + ratio2) / ratio1

#winner -> merchant
 

# Card details extracted to make payment
cardNumber = f.get('/Users/'+loser+'/Card','Number')
expirationYear = f.get('/Users/'+loser+'/Card', 'Expiry Year')
expirationMonth = f.get('/Users/'+loser+'/Card', 'Expiry Month')
expirationDate = expirationYear + '-' + expirationMonth
cardCode = f.get('/Users/'+loser+'/Card', 'CVV')

def charge_credit_card():
    #try:
        # Create a merchantAuthenticationType object with authentication details
        # retrieved from the constants file
        merchantAuth = apicontractsv1.merchantAuthenticationType()
        merchantAuth.name = CONSTANTS.apiLoginId
        merchantAuth.transactionKey = CONSTANTS.transactionKey

        # Create the payment data for a credit card
        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = "4111111111111111"
        creditCard.expirationDate = "2020-12"
        creditCard.cardCode = cardCode

        # Add the payment data to a paymentType object
        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        # Create order information
        order = apicontractsv1.orderType()
        order.invoiceNumber = "110011"
        order.description = "Lost a Bet" 
    
        # Set the customer's Bill To address
        fullname1 = f.get('/Users/'+loser, 'name')

        customerAddress = apicontractsv1.customerAddressType()
        customerAddress.firstName = "John"
        customerAddress.lastName = "Doe"
        customerAddress.company = "Souveniropolis"
        customerAddress.address1 = "14 Main Street"
        customerAddress.city1 = "Pecan Springs"
        customerAddress.state1 = "TX"
        customerAddress.zip1 = "44628"
        customerAddress.country1 = "USA"


        # Add values for transaction settings
        duplicateWindowSetting = apicontractsv1.settingType()
        duplicateWindowSetting.settingName = "duplicateWindow"
        duplicateWindowSetting.settingValue = "600"
        settings = apicontractsv1.ArrayOfSetting()
        settings.setting.append(duplicateWindowSetting)

        customerData = apicontractsv1.customerDataType()
        customerData.type = "individual"
        customerData.id = "99999456657"
        customerData.email = "vyas6@purdue.edu"

        # Create a transactionRequestType object and add the previous objects to it.
        #charged
        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authCaptureTransaction"
        transactionrequest.amount = amount
        transactionrequest.payment = payment
        transactionrequest.order = order
        transactionrequest.billTo = customerAddress
        transactionrequest.customer = customerData
        transactionrequest.transactionSettings = settings

        # Assemble the complete transaction request
        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = merchantAuth
        #createtransactionrequest.refId = "MerchantID-0001"
        createtransactionrequest.transactionRequest = transactionrequest
        # Create the controller
        createtransactioncontroller = createTransactionController(
            createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()

        if response is not None:
            # Check to see if the API request was successfully received and acted upon
            if response.messages.resultCode == "Ok":
                # Since the API request was successful, look for a transaction response
                # and parse it to display the results of authorizing the card
                if hasattr(response.transactionResponse, 'messages') is True:
                    print(
                        'Successfully created transaction with Transaction ID: %s'
                        % response.transactionResponse.transId)
                    print('Transaction Response Code: %s' %
                        response.transactionResponse.responseCode)
                    print('Message Code: %s' %
                        response.transactionResponse.messages.message[0].code)
                    print('Description: %s' % response.transactionResponse.
                        messages.message[0].description)
                else:
                    print('Failed Transaction.')
                    if hasattr(response.transactionResponse, 'errors') is True:
                        print('Error Code:  %s' % str(response.transactionResponse.
                                                    errors.error[0].errorCode))
                        print(
                            'Error message: %s' %
                            response.transactionResponse.errors.error[0].errorText)
            # Or, print errors if the API request wasn't successful
            else:
                print('Failed Transaction.')
                if hasattr(response, 'transactionResponse') is True and hasattr(
                        response.transactionResponse, 'errors') is True:
                    print('Error Code: %s' % str(
                        response.transactionResponse.errors.error[0].errorCode))
                    print('Error message: %s' %
                        response.transactionResponse.errors.error[0].errorText)
                else:
                    print('Error Code: %s' %
                        response.messages.message[0]['code'].text)
                    print('Error message: %s' %
                        response.messages.message[0]['text'].text)
        else:
            print('Null Response.')

        return response

    #except:
    #    print("missing info")

def authorize_credit_card():
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = CONSTANTS.apiLoginId
    merchantAuth.transactionKey =CONSTANTS.transactionKey

    creditCard = apicontractsv1.creditCardType()
    creditCard.cardNumber = cardNumber
    creditCard.expirationDate = expirationDate

    payment = apicontractsv1.paymentType()
    payment.creditCard = creditCard

    transactionrequest = apicontractsv1.transactionRequestType()
    transactionrequest.transactionType ="authCaptureTransaction"
    transactionrequest.amount = Decimal (amount)
    transactionrequest.payment = payment


    createtransactionrequest = apicontractsv1.createTransactionRequest()
    createtransactionrequest.merchantAuthentication = merchantAuth
    createtransactionrequest.refId ="MerchantID-0001"

    createtransactionrequest.transactionRequest = transactionrequest
    createtransactioncontroller = createTransactionController(createtransactionrequest)
    createtransactioncontroller.execute()

    response = createtransactioncontroller.getresponse()

    if (response.messages.resultCode=="Ok"):
        print("Transaction ID : %s" % response.transactionResponse.transId)
    else:
        print("response code: %s" % response.messages.resultCode)

if (os.path.basename(__file__) == os.path.basename(sys.argv[0])):
    authorize_credit_card()
    charge_credit_card()  