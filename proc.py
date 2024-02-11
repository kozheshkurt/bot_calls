# Подключаем библиотеки
import re
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	

# класс обзвонщика
class Caller:
    def __init__(self, Id): # при создании присваиваем Id
        self.Id = Id
        
        self.contacts_ids = []
    
    def add_caller (self):
        pass


def authorize():
    CREDENTIALS_FILE = 'mypython-rbecs-calls-081fcae8bfff.json'  # Имя файла с закрытым ключом, вы должны подставить свое

    # Читаем ключи из файла
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 
    print ('Authorization success')
    return service


def get_sheetlist():
    # Получаем список листов, их Id и название
    spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
    sheetList = spreadsheet.get('sheets')
    print ('Sheets:')
    for sheet in sheetList:
        print('ID = ', sheet['properties']['sheetId'], ', title = ', sheet['properties']['title'])

    return sheetList

# Получаем список строк, каждая в формате [id, name, number, school, region, town, caller_name, result]
def get_all_rows(sheetTitle):
    # читаем данные из таблицы
    request = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                     ranges = [sheetTitle+"!A:H"], 
                                     valueRenderOption = 'FORMATTED_VALUE',  
                                     dateTimeRenderOption = 'FORMATTED_STRING')
    response = request.execute() 
    # читаем данные из листа
    sheet_values = response['valueRanges'][0]['values']
    return sheet_values


# Функция добавляет данные в низ таблицы (в первую незаполненную строку)
def add_one_into_bottom (sheetTitle, values): #values - список данных в строке ['A1','B1','C1']
    # Проверяем, сколько заполненных строк в столбце A (ID)
    request = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                        ranges = [sheetTitle+"!A:A"], 
                                        valueRenderOption = 'FORMATTED_VALUE',  
                                        dateTimeRenderOption = 'FORMATTED_STRING')
    response = request.execute()
    sheet_values = response['valueRanges'][0]['values']
    # Проверяем, есть ли уже ID в списке
    range = sheetTitle + "!A" + str(len(sheet_values) + 1) + ":H" + str(len(sheet_values) + 1) # Диапазон от A до H, номера строк с последней заполненной + 1
    # Заполняем данными строку в нужном диапазоне
    request = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": range, 
            "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
            "values": [values]}
        ]
    })
    response = request.execute()

    return response


def add_caller(caller_info):
    callers_sheetTitle = sheetList[1]['properties']['title']
    existing_callers = get_all_rows(callers_sheetTitle)
    if str(caller_info[0]) in [caller[0] for caller in existing_callers]:
        print('The user is already in the table. ', caller_info)
        return 'The user is already in the table'
    else:
        add_one_into_bottom (callers_sheetTitle, caller_info)
        #caller = Caller(caller_info[0])
        print('User added success: ', caller_info)
        return 'Added successfully'


def empty_contacts():
    contacts = get_all_rows('Contacts')
    free_contacts = []
    for contact in contacts:
        if (len(contact)<7) or (contact[6] == ''):
            free_contacts.append(contact)
    return free_contacts


def add_caller_to_contact(changed_contact, caller):
    contacts = get_all_rows('Contacts')
    for contact in contacts:
        if str(contact[0]) == str(changed_contact[0]):
            contact.append(caller)
    request = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": sheetTitle+"!A:I",
            "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
            "values": contacts
            }
        ]
    })
    response = request.execute()
    



spreadsheetId = '1YMX1iV-9VBS4gwn1ut6A-X3uP5COzVWa4O-MWY0aLX4'
service = authorize()
sheetList = get_sheetlist()
# Первый лист в списке листов    
sheetId = sheetList[0]['properties']['sheetId']
sheetTitle = sheetList[0]['properties']['title']




'''
# Заполняем таблицу данными 
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

'''
# Добавляем строку с тестовыми данными
values = ['_','Нове прізвище',"'0501111111",'Школа','Область',None,'Обзвонщик']
add_one_into_bottom (sheetTitle, values)

contacts = get_all_rows(sheetTitle, sheetId)
for contact in contacts:
    print(contact)
'''
