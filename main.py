#%%
import json
import websocket
import ssl
import time

import FN

QUERY_HEADSET_ID                    =   1
CONNECT_HEADSET_ID                  =   2
REQUEST_ACCESS_ID                   =   3
AUTHORIZE_ID                        =   4
CREATE_SESSION_ID                   =   5
SUB_REQUEST_ID                      =   6
SETUP_PROFILE_ID                    =   7
QUERY_PROFILE_ID                    =   8
TRAINING_ID                         =   9
DISCONNECT_HEADSET_ID               =   10
CREATE_RECORD_REQUEST_ID            =   11
STOP_RECORD_REQUEST_ID              =   12
EXPORT_RECORD_ID                    =   13
INJECT_MARKER_REQUEST_ID            =   14
SENSITIVITY_REQUEST_ID              =   15
MENTAL_COMMAND_ACTIVE_ACTION_ID     =   16
MENTAL_COMMAND_BRAIN_MAP_ID         =   17
MENTAL_COMMAND_TRAINING_THRESHOLD   =   18
SET_MENTAL_COMMAND_ACTIVE_ACTION_ID =   19


#%%
url = "wss://localhost:6868"
user = {
    "license" : "",
    "client_id" : "Your client_id",
    "client_secret" : "Your client_secret",
    "debit" : 100
}

############################ Request access for app ############################
def request_access(user, ws):
    # print('request access --------------------------------')
    request_access_request = {
        "id": REQUEST_ACCESS_ID,
        "jsonrpc": "2.0", 
        "method": "requestAccess",
        "params": {
            "clientId": user['client_id'], 
            "clientSecret": user['client_secret']
        },
    }

    ws.send(json.dumps(request_access_request, indent=4))
    print('#######################################\n')
    print(ws.recv())

############################ Query headset request ############################
def query_headset(ws):
    # print('query headset --------------------------------')
    query_headset_request = {
        "jsonrpc": "2.0", 
        "id": QUERY_HEADSET_ID,
        "method": "queryHeadsets",
        "params": {}
    }

    ws.send(json.dumps(query_headset_request, indent=4))
    print('#######################################\n')

    result = ws.recv()
    result_dic = json.loads(result)

    print(result_dic)

    return result_dic['result']

############################ Connect headset request ############################
def connect_headset(ws, headset_id):
    # print("Checking headset connectivity...")

    connect_headset_request = {
        "jsonrpc": "2.0", 
        "id": CONNECT_HEADSET_ID,
        "method": "controlDevice",
        "params": {
            "command": "connect",
            "headset": headset_id
        }
    }
    
    ws.send(json.dumps(connect_headset_request, indent=4))
    print('#######################################\n')

    result = ws.recv()
    result_dic = json.loads(result)

    print(result_dic)

############################ Authorize request ############################
def authorize(ws, user):
    # print('authorize --------------------------------')
    authorize_request = {
        "jsonrpc": "2.0",
        "method": "authorize", 
        "params": { 
            "clientId": user['client_id'], 
            "clientSecret": user['client_secret'], 
            "license": user['license'],
            "debit": user['debit']
        },
        "id": AUTHORIZE_ID
    }


    ws.send(json.dumps(authorize_request))
    print('#######################################\n')

    result = ws.recv()
    result_dic = json.loads(result)

    print(result_dic)

    return result_dic['result']['cortexToken']

############################ Create session request ############################
def create_session(ws, auth, headset_id):
    # print('create session --------------------------------')
    create_session_request = { 
        "jsonrpc": "2.0",
        "id": CREATE_SESSION_ID,
        "method": "createSession",
        "params": {
            "cortexToken": auth,
            "headset": headset_id,
            "status": "active"
        }
    }
    
    ws.send(json.dumps(create_session_request))
    print('#######################################\n')

    result = ws.recv()
    result_dic = json.loads(result)

    print(result_dic)

    return result_dic['result']['id']
        
#%%
def main():
    record_time = input("Enter the time(seconds) to record : ")

    stream = ['met'] # Using met function
    ws = websocket.create_connection(url, sslopt={"cert_reqs": ssl.CERT_NONE})

    request_access(user, ws)
    headset_id = query_headset(ws)
    connect_headset(ws, headset_id[0]['id'])
    auth = authorize(ws, user)
    session_id = create_session(ws, auth, headset_id[0]['id'])

    sub_request_json = {
        "jsonrpc": "2.0", 
        "method": "subscribe", 
        "params": { 
            "cortexToken": auth,
            "session": session_id,
            "streams": stream
        }, 
        "id": SUB_REQUEST_ID
    }

    ws.send(json.dumps(sub_request_json))

    # Time Recording
    total_time = 0
    record_time = int(record_time)

    # It has no value when first request
    First_Request = True

    while(True):
        time_start = time.time() # Start Recording Time

        # Receive Data From Emotiv
        new_data = ws.recv() 
        met_data = json.loads(new_data)

        print('#######################################\n')

        
        if(First_Request == False):
            # Get Met Data
            VAL = met_data['met'][10]
            ENG = met_data['met'][1]
            FOC = met_data['met'][12]
            EXC = met_data['met'][3]
            MED = met_data['met'][8]
            FRU = met_data['met'][6]

            # Show Emotiv State
            FN.Show_Emotiv_State(VAL, ENG, FOC, EXC, MED, FRU)


            time_end = time.time() # Finish Recording Time
            time_cost = int(time_end - time_start)  # Time Spent
            total_time = total_time + time_cost # Total Time

            print("Spent %d second" % time_cost)

            if(total_time > record_time):
                print("\nFinish testing : Spent %d second totally" % total_time)

                break
            
        First_Request = False



if __name__ == '__main__':
    main()

#%%