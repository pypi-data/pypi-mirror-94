import pandas as pd
from google.oauth2 import service_account
import pandas_gbq
from slackclient import SlackClient
#from dotenv import load_dotenv
from datetime import datetime, timedelta
import sys, os
import traceback
import os.path
import platform

#========================================================================

def check_slack_log(channel, job_name,current_date):
    '''
    find status message from channel and job name from dag
    '''
#`vinid-data-workspace-prod.BI_WORKSPACE.f_bot_slack_log`
    qr = f'''

        select * from
        (
        select *, row_number () over (partition by job_name, channel_name order by sent_datetime desc)  as rowno
        from `vinid-data-workspace-prod.BI_WORKSPACE.f_bot_slack_log`
        where 1=1
        and date(sent_datetime) = "{current_date}"
        and  channel_name = "{channel}"
        and job_name = "{job_name}"
        )
        where rowno=1
    '''
    status_mes = ''

    try:
        df = pd.read_gbq(qr, dialect='standard', project_id='vinid-datalake-prod')
        status_mes = df.status.values[0]
    except IndexError:
        status_mes = 'no_value'

    return status_mes


#========================================================================


def error_to_slack(text,slack_id_list,job_name,slack_token,channel_alert,channel):

    sc = SlackClient(slack_token)

    current_file_path = sys.argv[0]
    file1 = open(current_file_path,"r") 
    txt_code = file1.read()
    Code = file1.readlines()
    file1.close()
    for i in range(len(Code)):
        Code[i] = Code[i].replace("\n"," \n")
        Code[i] = Code[i].rstrip()
    for i in range(len(Code)):    
        try:        
            Code.remove('')
        except:
            print(f'line {i} ok')


    #concat list of slack id
    slack_id = ''
    for i in range(len(slack_id_list)) : 
        slack_id =  slack_id +  " <@" + slack_id_list[i] + ">"

    # prepare alert message
    message = [
                            {
                                "type": "context",
                                "elements": [
                                    {
                                        "type": "mrkdwn",
                                        "text": f':alert: {slack_id}*:toang_toang: :boom:{job_name}:boom:  failed because:* \n ```{text}```'
                                    }
                                ]
                            }

              ]    

    # post alert message and capture the message log
    error_message = sc.api_call(   "chat.postMessage",
                                channel=channel_alert,
                                blocks=message)

    df_message = pd.json_normalize(error_message)[['channel','ts','message.subtype','message.text','message.ts','message.username','message.bot_id','message.blocks']]

    df_message['error_description_text'] = f':alert: {slack_id}*:toang_toang: :boom:{job_name}:boom:  failed because:* \n ```{text}```'
    df_message['post_channel'] = channel
    df_message['processing_code'] = txt_code 
    df_message['compress_processing_code'] = ""
    df_message['compress_processing_code'].loc[0] = '\n'.join(Code)      
   
    df_message['date_time'] = datetime.now()
    df_message = df_message.rename(columns = { 'message.subtype': 'message_subtype', 'message.text': 'message_text','message.ts':'message_ts', 'message.username': 'message_username', 'message.bot_id': 'message_bot_id', 'message.blocks': 'message_blocks'}, inplace = False)
    
    print(df_message)

    dest_tbl = "BI_WORKSPACE.slack_bot_api_log"
    dest_proj = "vinid-data-workspace-prod"
    if_exists = "append"

    # send message log to big query
    df_message.to_gbq(destination_table=dest_tbl, project_id=dest_proj,if_exists=if_exists)


#========================================================================

def check_data_quality(table_name_list):
    qr = '''
     Select date(check_date) check_date,concat(a.project_name,".",a.table_schema,".",a.table_name) table_name, Final_Result from `vinid-data-workspace-prod.BI_WORKSPACE.etl_tracking_log` a
    left join
     (Select  project_name,table_schema,table_name, max(check_time) max_time from `vinid-data-workspace-prod.BI_WORKSPACE.etl_tracking_log` 
      where date(check_date) =  Date_sub(current_date,interval 1 day)
     group by project_name,table_schema,table_name
     ) b
     on a.project_name = b.project_name and a.table_schema = b.table_schema and a.table_name = b.table_name and a.check_time = b.max_time
     
  where date(check_date) =  Date_sub(current_date,interval 1 day)
  and b.project_name is not null
  and b.table_schema is not null
  and b.table_name is not null
  order by 1,2 
    '''
    df = pd.read_gbq(qr, dialect='standard', project_id='vinid-datalake-prod')

    #variables definition
    tbl_name_col = 'table_name'

    df_check = df[df[tbl_name_col].isin(table_name_list)]
    return df_check

#========================================================================

def write_slack_log(channel_name, job_name, status, reason, dest_proj, dest_tbl, if_exists = 'append'):
    # check os system: 
    os_system = platform.system()

    # check user_name: (nifi server treated as /root user)
    user = os.path.expanduser("~")

    current_time = datetime.now()#.strftime('%Y-%m-%dT%H:%I:%S')
    current_time_label = datetime.now().strftime('%Y.%m.%d')
    current_time = datetime.now()#.strftime('%Y-%m-%dT%H:%I:%S')
    default_schema = [{'name': 'channel_name', 'type':'STRING'}
                    , {'name': 'job_name', 'type':'STRING'}
                    , {'name': 'sent_datetime', 'type':'DATETIME'}
                    , {'name': 'status', 'type':'STRING'}
                    , {'name': 'reason', 'type':'STRING'}]

    log_dict = {'channel_name':channel_name,
                'job_name':job_name,
                'sent_datetime': current_time,
                'status': status,
                'reason' : reason }

    log_df = pd.DataFrame([log_dict])

    # condition for save log by os system
    # windows = not VM server, not autojob -> directly save to big query
    # linux & root user = possible VM server, save log to file csv
    if os_system == "Windows":
        log_df.to_gbq(destination_table=dest_tbl, project_id=dest_proj,if_exists=if_exists, table_schema=default_schema)
    if os_system == "Linux" and user ==  "/root":
        log_df.to_csv("/opt/nifi/nifi-operation/slack_bot_log/" + job_name + "_" + current_time_label +".csv",index = False)

    return log_df

#========================================================================

def pretty_format(x):
    '''
    Shorten number format to number + alphabet unit 
    '''
    y = ""
    if 1e3<=x<1e6:
        y = str(f"{round(x/1e3,2):,.2f}") + "K"
    elif 1e6<=x<1e9:
        y = str(f"{round(x/1e6,2):,.2f}") + "M"
    elif 1e9<=x:
        y = str(f"{round(x/1e9,2):,.2f}") + "B"
    else:
        y = str(f"{round(x,2):,.2f}") + ""
    return y

#========================================================================

def send_message(slack_token, slack_id_list, channel, job, channel_alert, check_list_tbl, sent_message, is_manual, force_manual):
    '''
    (slack_token,channel,is_manual,force_manual)

    slack_token: BOT token which is used to post the message to channel.

    slack_id: Slack ID of users

    channel: Channel where the message will be posted.
    
    job: Mame of the automation bot.
    
    channel_alert: Channel where the error will be posted for alert if error occurs.
    
    check_list: list of table to be checked, defined by the user, input blank array [] if there is none.
    
    is_manual: (value = 0: used in normal daily state assume that the data quality check working OK) (value = 1: used to bypass the data check function when assume that the data quality check NOT working OK). 

    force_manual: (value = 0: run the function normally) (value = 1: force the function to send message despite any state (to bypass the 'success' state on check log table)).
    '''
    try:
        sc = SlackClient(slack_token)
        #channel_name = 'test_slack'
        #channel_name = 'metrics-vinpay'
        channel_name = channel
        channel_airflow = channel_alert
        current_date = datetime.now().strftime('%Y-%m-%d')
        job_name = job
        print(current_date)


        status_fail = 'failed'
        status_success = 'success'


        slack_check_mes = check_slack_log(channel_name, job_name,current_date)

        def error_mes(job_name, df_check, slack_id_list):
            txt = ''
            slack_id = ''
            for i in range(len(slack_id_list)) : 
                slack_id =  slack_id +  " <@" + slack_id_list[i] + ">"

            error_des = ''
            for i in range(len(df_check)) :
                if df_check.iloc[i, 1] == "NOT UPDATE":
                    txt =  txt + f'\n`{df_check.iloc[i, 0]}` \n Data is not updated to *{current_date}* yet. Kindly check with team DE.'
                elif df_check.iloc[i, 1] == "FAIL_N":
                    txt =  txt + f'\n`{df_check.iloc[i, 0]}` \n The number of today records seems *ABNORMALLY DROPS*. Kindly check with team DE to verify.' 
                else:
                    txt =  txt + f'\n`{df_check.iloc[i, 0]}` \n {df_check.iloc[i, 1]} '      

                #compound_text = f'{compound_text} ' + txt
            print(df_check)
            message = [   
                            {
                                "type": "context",
                                "elements": [
                                    {
                                        "type": "mrkdwn",
                                        "text": f':alert: {slack_id}*:toang_toang: :boom:{job_name}:boom:  failed because:*  {txt}'
                                    }
                                ]
                            }

                    ]


            return message

        def sending_execution(channel,message):
            current_file_path = sys.argv[0]
            file1 = open(current_file_path,"r") 
            txt_code = file1.read()
            Code = file1.readlines()
            file1.close()
            for i in range(len(Code)):
                Code[i] = Code[i].replace("\n"," \n")
                Code[i] = Code[i].rstrip()
            for i in range(len(Code)):    
                try:        
                    Code.remove('')
                except:
                    print(f'line {i} ok')

            error_message = sc.api_call(
                                            "chat.postMessage",
                                            channel=channel,
                                            blocks=message           
                                            )
            df_message = pd.json_normalize(error_message)[['channel','ts','message.subtype','message.text','message.ts','message.username','message.bot_id','message.blocks']]
         #   print("Check place: " + str(pd.json_normalize(pd.json_normalize(message)['elements'][0])['text'][0]))
            df_message['error_description_text'] = ""
            df_message['post_channel'] = channel
            df_message['processing_code'] = txt_code  
            df_message['compress_processing_code'] = ""            
            df_message['compress_processing_code'].loc[0] = '\n'.join(Code)       
         #   df_message['compress_processing_code'].loc[0] = Code                        
            df_message['date_time'] = datetime.now()
            df_message = df_message.rename(columns = {'message.subtype': 'message_subtype', 'message.text': 'message_text','message.ts':'message_ts', 'message.username': 'message_username', 'message.bot_id': 'message_bot_id', 'message.blocks': 'message_blocks'}, inplace = False)

            print(df_message)

            dest_tbl = "BI_WORKSPACE.slack_bot_api_log"
            dest_proj = "vinid-data-workspace-prod"
            if_exists = "append"

            df_message.to_gbq(destination_table=dest_tbl, project_id=dest_proj,if_exists=if_exists)

        if force_manual == 1:
            message = sent_message
            sending_execution(channel=channel_name, message=message)
            print('Done')

            ### write success log
            write_slack_log(channel_name=channel_name, job_name=job_name, status=status_success, reason=status_success, dest_proj='vinid-data-workspace-prod', dest_tbl='BI_WORKSPACE.f_bot_slack_log', if_exists = 'append')
        else:
            if slack_check_mes == 'success':
                print('enough for today')
            else:
                print('pass slack check')
                    # Check table status
                tbl_list = check_list_tbl
                df_check = check_data_quality(table_name_list = tbl_list)                 
                if is_manual == 1:
                    df_check.Final_Result = 'OK'
                
                    ##check time update for table
                if df_check[(df_check.Final_Result == 'NOT UPDATE') | (df_check.Final_Result == 'FAIL_N')].empty == False:
                    df_check = df_check[(df_check.Final_Result == 'NOT UPDATE') | (df_check.Final_Result == 'FAIL_N')][['table_name','Final_Result']]
                    reason_mes = error_mes(job_name, df_check , slack_id_list)
                    write_slack_log(channel_name=channel_name, job_name=job_name, status=status_fail, reason = reason_mes, dest_proj='vinid-data-workspace-prod', dest_tbl='BI_WORKSPACE.f_bot_slack_log', if_exists = 'append')
                    sending_execution(channel=channel_airflow, message=reason_mes)

                else:
                    print('pass job check table')
                    ###send final message to slack
                    message = sent_message
                    sending_execution(channel=channel_name, message=message)
                    print('Done')

                    ### write success log
                    write_slack_log(channel_name=channel_name, job_name=job_name, status=status_success, reason=status_success, dest_proj='vinid-data-workspace-prod', dest_tbl='BI_WORKSPACE.f_bot_slack_log', if_exists = 'append')

    except: 
        exc_type, exc_value, exc_traceback = sys.exc_info()
        error = traceback.format_exc()
        if(error.find("SQL") == -1):
            error_to_slack(error,slack_id_list,job_name,slack_token,channel_alert,channel)
        else:
            error_to_slack(exc_value,slack_id_list,job_name,slack_token,channel_alert,channel)

#========================================================================        
