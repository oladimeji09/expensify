#@auto-fold regex /./
import json,requests as r,sys,time, pandas as pd,env
## NOTE: documentation https://integrations.expensify.com/Integration-Server/doc/#report-exporter

dates = env.date_between(100,1)
start_date = dates[0].date()
end_date  = dates[1].date()

s3_folder  = 'schema' #s3 folder & schema name
table_name = 'expensify'
baseURl = "https://integrations.expensify.com/Integration-Server/ExpensifyIntegrations"

def query():
    with open('query.json') as f:
        settings = json.load(f)
    return settings

def request(stack):
    """Returns a report ID to be downloaded"""
    param = {"requestJobDescription": json.dumps(stack),
                        "template": open('template.ftl').read()}
    resp = r.post(baseURl, params=param)
    if resp.status_code == 200:
        return resp.text
    else:
        raise Exception("Query failed to run by returning code of {}, with error {}. {}".format(resp.status_code, resp.content, stack))

def extract(start_date,end_date):
    """Loop through dates and download the reports into a single DF"""
    df = pd.DataFrame()
    while start_date < end_date:
        stack = query()
        stack['inputSettings']['filters'].update({'startDate': str(start_date)})
        stack['inputSettings']['filters'].update({'endDate': str(start_date + pd.Timedelta(days=90))})
        reportID = request(stack)
        param = {"requestJobDescription": json.dumps({
                "type":"download",
                "credentials":stack['credentials'],
                "fileName": reportID
                })}
        resp = r.get(baseURl, params=param)
        clean_data  = json.loads(resp.text)
        df = df.append(pd.DataFrame(clean_data))
        time.sleep(5)
        start_date += pd.Timedelta(days=90)
        print("Retrieving data between "+str(start_date)+"-"+str(start_date + pd.Timedelta(days=90)))
    return df

def transform(start_date,end_date):
    """Transform data into the shape needed"""
    df = extract(start_date,end_date)
    cols = df.columns
    df[cols] = df.replace('[^a-zA-Z]', ' ')
    df['category'] = df['category'].str.replace('[^a-zA-Z]', ' ')
    df = df.reindex(sorted(df.columns), axis=1)
    df['created'] = df['created'].astype('datetime64[ns]')
    df['load_date'] = pd.to_datetime('today').strftime("%Y-%m-%d %H:%M")
    df.to_csv(env.file_path+table_name+'.csv', sep=',' ,index=False,  encoding='utf-8', line_terminator =None)
