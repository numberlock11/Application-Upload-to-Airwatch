import csv, requests, json
from pprint import pprint



# Map row to dictionary (dictionary comprehension)
def app(column_names, row):
    return {column_names[column]: data for column, data in enumerate(row) if column < len(column_names)}

# Map CSV file to list of dictionaries (list comprehension)
apps = [app(['ExternalId'], row) for row in csv.reader(open('/path/to/apps.csv', 'rbU'))]
row_count = sum(1 for each in apps)
x=0

# The upper limit is hardcoded based of max number in the csv
while x < row_count:
    cannot = []
    total = 0
    # Finding the bundle ID and the App name from the Apple API
    url = 'http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsLookup?id='+ apps[x+1]['ExternalId']
    print url
    headers1 = {'Content-Type': 'application/json'}
    response = requests.get (url,headers = headers1)
    jtext=response.text
    v=json.loads(jtext)
    # To verify if the App exists in the App store.
    count = v["resultCount"]
    print count
    bundle = v["results"][0]["bundleId"]
    appname = v["results"][0]["trackName"].encode('ascii','ignore')
    
    pprint(str(bundle))
    pprint(appname)
        
# Hardcoded the Auth token for the API call to upload in AirWatch
    headers = {'aw-tenant-code': '1LL4TMEQAAG6A7GAAIAA', 'Content-Type' : 'application/json'}
    
    bundlein = "'"+  bundle + "'"
    appnamein = "'" + appname + "'"
        
# Hardcoded LocationgroupId  and Pushmode (other option is "Auto")
    parameters = '{"ApplicationName":%s,"BundleId":%s,"ExternalId":%s,"Platform":2,"LocationGroupId":2459,"PushMode":"OnDemand"}' %(appnamein, bundlein, apps[x+1]['ExternalId'])

    print parameters
        
# Hardcoded the URL of the environment to upload and the Admin creds
    response = requests.post('https://####.awmdm.com/API/v1/mam/apps/public', headers = headers, data = parameters, auth =('####','####'))

    print response
    total = total+1
    x+=1
    print total
    print cannot
