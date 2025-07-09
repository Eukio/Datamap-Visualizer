import os
import sys
import json
import time
import pandas as pd
from flask import Blueprint, flash, render_template, request, redirect, send_file, session
from werkzeug.utils import secure_filename
from tabulate import tabulate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
if getattr(sys, 'frozen', False):
    base_dir = sys._MEIPASS
    DATAMAP_DIRNAME = os.path.join(base_dir,'website','datamaps')
else:
    base_dir = os.path.dirname(__file__)
    DATAMAP_DIRNAME = os.path.join(base_dir,'datamaps')

DATA_INPUT_DIRNAME = os.path.join(base_dir, 'data')
CSV_FILEPATH = os.path.join(base_dir, 'data', 'Data.csv')

columnList = []
timeDelayList =['None','30','60','90','120','240']
runTimer = False

import auth

home = Blueprint('home', __name__)

@home.route('/home', methods = ['GET','POST'])
def home_view():
    global runTimer
    if request.method == 'POST': 
        if 'export_csv' in request.form:
            return send_file(CSV_FILEPATH, as_attachment=True, download_name='Data.csv', mimetype='text/csv')
        if 'file' in request.files:
            session['datamap'] =  request.form.get('file_selection')
            uploadFile()           
        if 'switch_user' in request.form:
            resetUser()
            return redirect('/login')
        if request.form.get('delay_selection') == str(timeDelayList[0]):
            runTimer = False
        elif 'refresh_Timer_button' in request.form:
            runTimer = True
            timerRefresh(int(request.form.get('delay_selection')))
        if 'refresh_button' in request.form:
            refreshDisplay()
    return render_template('home.html', boolean = True, columnList=columnList, datamapList=os.listdir(DATAMAP_DIRNAME),timeDelayList=timeDelayList)

def timerRefresh(time_delay):
    print(f"Timer start {time_delay} sec")
    while runTimer:
        time.sleep(time_delay)
        print("Refresh")
        refreshDisplay()
        if runTimer == False:
            break
    
def refreshDisplay():
  auth.runCollect() 
  if 'json_filepath' in session:
    createData(session['json_filepath'], datamap=session['datamap'])
  else:
      print('no datamap to refresh')

def resetUser():
    session.pop("file",None)
    session.pop("datamap",None)
    columnList.clear()
    session.pop("username",None)
    session.pop("password",None)
    clearDirectory(DATAMAP_DIRNAME)
    clearDirectory(DATA_INPUT_DIRNAME)
          
def clearDirectory(directory):
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

def uploadFile():
    if request.files.get('file').filename.endswith('json'):
        flash("File uploaded successfully", category='success')
        os.makedirs(DATA_INPUT_DIRNAME, exist_ok=True)
        session['json_filepath'] = os.path.join(DATA_INPUT_DIRNAME, secure_filename(request.files.get('file').filename))
        request.files.get('file').save(session['json_filepath'])
        createData(session['json_filepath'], session['datamap'])
    else:
        flash('Please upload a valid JSON file.', category='error')

class Column:
    def __init__(self, columnName, htmlTable):
        self.columnName = columnName
        self.htmlTable = htmlTable

def createData(json_input_filepath, datamap):
    columnList.clear()

    datamap_path = os.path.join(DATAMAP_DIRNAME, datamap)
    with open(datamap_path) as f:
        datamap_df = pd.DataFrame.from_dict(json.load(f), orient='index').reset_index()
    datamap_df.columns = ['Key', 'Value']

    with open(json_input_filepath) as f:
        raw_data = json.load(f)
    max_len = max(map(len, raw_data.values()))
    for k in raw_data:
        raw_data[k] += [None] * (max_len - len(raw_data[k]))
    input_df = pd.DataFrame(raw_data)

    csv_df = pd.DataFrame()
    for col in input_df.columns:
        temp_df = pd.DataFrame(input_df[col].dropna()).reset_index(drop=True).rename(columns={col: 'Key'})
        merged = pd.merge(temp_df, datamap_df, on='Key', how='inner')
        html_table = tabulate(merged, showindex=False, tablefmt='html')
        csv_df= pd.concat([csv_df, merged], axis=1)

        columnList.append(Column(col, html_table))

    csv_df.to_csv(CSV_FILEPATH, header=False, index=False, encoding="utf-16")
