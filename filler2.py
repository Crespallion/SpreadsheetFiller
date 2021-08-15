import requests
from PIL import Image
import base64
import io

# coding=<encoding name>
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = "some_file.json" #true name is hidden

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

spreadsheetId = "someID" #true ID is hidden

driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 's***@***.ru'},  #true email is hidden
    fields = 'id'
).execute()

MarkList = [1] * 550

f = open('lp.txt')
log = f.readline()[:-1] 
pas = f.readline()
f.close()

url = 'https://na-mars.ru/login/index.php'
with open("success.html","w",encoding="utf-8") as f:
	f.write('')

user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

session = requests.Session()
r = session.get(url, headers = {
    'User-Agent': user_agent_val
})

session.headers.update({'Referer':url})

session.headers.update({'User-Agent':user_agent_val})

_xsrf = session.cookies.get('_xsrf', domain="na-mars.ru")
logintoken = session.cookies.get('logintoken', domain="na-mars.ru")

buf = str(r.text)
part = buf[buf.find('logintoken'):buf[buf.find('logintoken'):].find('>')+buf.find('logintoken')]
logintoken = part[part.find("value")+7:-1]

print('===THE BEGIN===')

post_request = session.post(url, {
     'username': log,
     'password': pas,
     'logintoken': logintoken, 
})

post_request = session.get('https://na-mars.ru/course/view.php?id=23')
coursePage = post_request.text

print("Script loged in.\nLooking for homework...")
nameOfHomeWork = 'ДЗ от 18.01.2021'
nameOfHomeWork = input("Ввести название дз: ")
print("Дз называется:", nameOfHomeWork)

def getLink(page, name):
	start = page[:page.find(name)].rfind('href')+6
	end = start + page[start:].find('\"')
	return page[start:end]

pageOfHomeWork = session.get(getLink(coursePage, nameOfHomeWork)).text
pageOfAttempts = session.get(getLink(pageOfHomeWork, 'Попыток')).text

print("Homework is founded.\nLooking for attempts...")
listOfNames = open('namesm.txt').read().split('\n')
total = len(listOfNames)
num = 0
didNotPaste = []
for nameAndSurname in listOfNames:
	num += 1
	print(nameAndSurname, num, '/', total)
	start = pageOfAttempts.rfind(nameAndSurname)
	if (start == -1):
		print('Did not done.')
		didNotPaste.append(nameAndSurname)
		MarkList[listOfNames.index(nameAndSurname)] = ''
		continue
	start += pageOfAttempts[start:].find('href')+6
	end = start + pageOfAttempts[start:].find('\"')
	pageOfAttempt = session.get(pageOfAttempts[start:end]).text

	with open("success.html","a",encoding="utf-8") as f:
		f.write('<br><br><br>'+getLink(pageOfAttempt, nameAndSurname)+'<br>')

	numberOfPhotos = pageOfAttempt.count('forcedownload')
	koef = int(numberOfPhotos/3)+1
	for i in range(numberOfPhotos):
		try:
			linkToPhoto = getLink(pageOfAttempt, 'forcedownload')
			linkToPhoto = linkToPhoto[:linkToPhoto.find('?')]
			if (i % koef != 1):
				continue
			pageOfAttempt = pageOfAttempt[pageOfAttempt.find('forcedownload')+1:]
			contentOfPhoto = session.get(linkToPhoto).content
			img = Image.open(io.BytesIO(contentOfPhoto)).resize((250,250))
			buffered = io.BytesIO()
			img.save(buffered, format="JPEG", optimize = True, quality = 25)
			data_uri = base64.b64encode(buffered.getvalue()).decode('utf-8')
			img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
			with open("success.html","a",encoding="utf-8") as f:
				f.write(img_tag)
		except:
			print('ERROR GETTING PHOTO')
			didNotPaste.append(str('!'+nameAndSurname+'!'))
			MarkList[listOfNames.index(nameAndSurname)] = 'ОШИБКА ЧТЕНИЯ'
			break


print("Не сдавшие: ", didNotPaste)
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "Лист номер один!B2:D3",
         "majorDimension": "ROWS",
         "values": [
                    ["d", "d", "d"],
                    ['d', "d", "d"]
                   ]}
    ]
}).execute()

results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "Лист номер один!A1:B550",
         "majorDimension": "COLUMNS",
         "values": [listOfNames[:total-1], MarkList[:total-1]]}
    ]
}).execute()

print('===THE END===')
