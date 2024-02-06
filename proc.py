# Подключаем библиотеки
import re
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	


# Функция добавляет данные в низ таблицы (в первые незаполненные строки)
def add_into_bottom (sheetTitle, values): #values - список списков (строк) [['A1','B1'],['A2','B2'],['A3','B3']]
    # Проверяем, сколько заполненных строк в столбце A (ID)
    
    request = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                        ranges = [sheetTitle+"!A:A"], 
                                        valueRenderOption = 'FORMATTED_VALUE',  
                                        dateTimeRenderOption = 'FORMATTED_STRING')
    response = request.execute() 
    sheet_values = response['valueRanges'][0]['values']

    range = sheetTitle + "!A" + str(len(sheet_values) + 1) + ":H" + str(len(sheet_values) + 1 + len(values)) # Диапазон от A до H, номера строк с последней заполненной+1 
    
    # Заполняем данными строки в нужном диапазоне
    request = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": range, 
            "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
            "values": values}
        ]
    })
    response = request.execute()

    return response


CREDENTIALS_FILE = 'mypython-rbecs-calls-081fcae8bfff.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

spreadsheetId = '1YMX1iV-9VBS4gwn1ut6A-X3uP5COzVWa4O-MWY0aLX4'


# Получаем список листов, их Id и название
spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
sheetList = spreadsheet.get('sheets')
for sheet in sheetList:
    print('ID = ', sheet['properties']['sheetId'], ', title = ', sheet['properties']['title'])

# Первый лист в списке листов    
sheetId = sheetList[0]['properties']['sheetId']
sheetTitle = sheetList[0]['properties']['title']

print('Current sheet Id = ', sheetId, '\n')

# Заполняем таблицу данными 
'''
request = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
    "data": [
        {"range": sheetTitle+"!B2:D5",
         "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
         "values": [
                    ["Ячейка B2", "Ячейка C2", "Ячейка D2"], # Заполняем первую строку
                    ['25', "=6*6", "=SIN(3.14/2)"]  # Заполняем вторую строку
                   ]}
    ]
})
response = request.execute()
'''
# Добавляем строку с тестовыми данными
values = [['Нове прізвище',"'0501111111",'Школа','Область','Місто','Обзвонщик', 'все ок']]
add_into_bottom (sheetTitle, values)


# Читаем данные из таблицы
request = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                     ranges = [sheetTitle+"!A:H"], 
                                     valueRenderOption = 'FORMATTED_VALUE',  
                                     dateTimeRenderOption = 'FORMATTED_STRING')
response = request.execute() 
sheet_values = response['valueRanges'][0]['values']
for row in sheet_values:
    print(row)


'''
callers = []
contacts = []

# добавляет обзвонщика в список обзвонщиков
def add_caller (name):
    callers.append(name)
'''