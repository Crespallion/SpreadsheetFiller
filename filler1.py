import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = "some_name" #true name of file is hidden

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)

spreadsheetId = "some_id" #true ID is hidden
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
access = driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': 's***@***.ru'}, #true email is hidden
    fields = 'id'
).execute()

NameList = open('namesm.txt').read().split('\n')
total = len(NameList)
MarkList0 = [0] * 500
MarkList = []
MarkExist = []

NameListOtchet = open('namesm.txt').read().split('\n')
MarksOtchet1 = []
MarksOtchet2 = []
MarksOtchet3 = []

iters = int(total/50)
f = open ("doc.html", 'r')
result = f.read()
if True:
	for i in range(total):
		st = result.rfind(NameList[i])
		st = result[st:st+800]
		st = st[st.rfind('attempt')+14:st.rfind('attempt')+20]
		if st != "":
			if st[0] == '>':
				st = st[1:]
			if st[-1] == '<':
				st = st[:-1]
			if st[0] == '\"':
				st = st[2:]
			MarkExist.append("1")
		else:
			MarkExist.append('')
		if st == '&slot' or st == '&slot=':
			st = '7,14'
		MarkList0[i] = st+' '
		MarkList.append(MarkList0[i])
		#print(NameList[i], MarkList0[i], MarkList[i])

if False:
	f = open ("doc1.html", 'r')
	result = f.read()
	for i in range(total):
    		st = result.rfind(NameList[i])
    		st = result[st:st+800]
    		st = st[st.rfind('attempt')+14:st.rfind('attempt')+20]
    		if st != "":
        		if st[0] == '>':
            			st = st[1:]
        		if st[-1] == '<':
            			st = st[:-1]
    		if (st[0] == '&'):
    			st = 'Shifted'
    		MarkList[i] = str(MarkList[i])+'|'+st

print(MarkList[358:388])

for i in range(len(NameListOtchet)):
	try:
		ii = NameList.index(NameListOtchet[i])
		if MarkExist[ii] == '1':
			MarksOtchet1.append('1')
			MarksOtchet2.append('1')
			MarksOtchet3.append(MarkList[ii])
		else:
			MarksOtchet1.append('')
			MarksOtchet2.append('')
			MarksOtchet3.append('')
	except:
		MarksOtchet1.append('')
		MarksOtchet2.append('')
		MarksOtchet3.append('')
		continue

results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "Лист номер один!B2:D3",
         "majorDimension": "ROWS",
         "values": [
                    ["Data", "Data", "Data"],
                    ['Data', "Data", "Data"]
                   ]}
    ]
}).execute()

def SetMark(lst):
    st = "Лист номер один!B1:G" + str(len(lst))
    results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": st,
                 "majorDimension": "COLUMNS",
                 "values": [lst, MarkList, 
                 MarksOtchet1, MarksOtchet2, MarksOtchet3, NameListOtchet]}
            ]
    }).execute()

SetMark(MarkList)

print(len(MarksOtchet3))