from flask import Blueprint, flash, render_template, request, redirect, send_file
import pandas as pd
import os
import json
from tabulate import tabulate
from werkzeug.utils import secure_filename

CSV_FILEPATH = CSV_FILEPATH = os.path.join(os.path.dirname(__file__), 'data', 'Data.csv')
DATAMAP_DIRNAME = os.path.join(os.path.dirname(__file__), 'datamaps')
JSON_DATAMAP_FILEPATH = os.path.join(os.path.dirname(__file__),'datamaps', '2STG_ACAH.json')
columnList = []
views = Blueprint('views', __name__)

@views.route('/home', methods = ['GET','POST'])
def home():
    if request.method == 'POST' and 'export_csv' in request.form:
      return send_file(CSV_FILEPATH, as_attachment=True, download_name='Data.csv', mimetype='text/csv')
    if request.method == 'POST' and 'file' in request.files:
        return uploadFile(request.files.get('file'))
    return render_template('home.html', boolean = True, columnList=columnList)

def uploadFile(file):
    global json_input_filepath
    if file.filename.endswith('.json'):
        json_input_filepath = os.path.join(os.path.dirname(__file__), 'data', secure_filename(file.filename))
        file.save(json_input_filepath)
        flash(f'{file.filename} uploaded successfully!', 'success')
        createData(json_input_filepath)
    else:
        flash('Please upload a valid JSON file.', 'error')
    return redirect('/home')

class Column:
    def __init__(self, columnName, htmlTable):
        self.columnName = columnName
        self.htmlTable = htmlTable

def createData(json_input_filepath):
    
    columnList.clear()
    with open(JSON_DATAMAP_FILEPATH) as json_data:
        data = json.load(json_data)
    datamap_df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index': 'Key', 0: 'Value'})
    input_json = pd.read_json(json_input_filepath)
    csv_df = pd.DataFrame()
    for col in input_json.columns:
        temp_df = pd.DataFrame(input_json[col]).dropna(how='all')
        temp_df = temp_df.reset_index().rename(columns={'index': 'Key', col: 'Value'})        
        temp_df = pd.DataFrame(pd.merge(temp_df, datamap_df, on='Key', how='inner'))
        temp_df = temp_df.drop(columns=['Value_x'])
        html_table = tabulate(temp_df, showindex=False, tablefmt='html')
        csv_df= pd.concat([csv_df, temp_df], axis=1)
        csv_df.to_csv(CSV_FILEPATH, header =
                       False, index = False, encoding="utf-16")  
        columnList.append(Column(col, html_table)) 


    
#across datamaps, with hardcoded inputs
def createCSVAcrossMultipleDatamaps(): 

    # Read the CSV file and create a DataFrame, name the column 'Key'
    output_df = pd.read_csv(CSV_FILEPATH, header=None, encoding="utf-16").T
    output_df.columns = ['Key']
    output_df = output_df.map(lambda x: x.strip() if isinstance(x, str) else x)
    print(output_df)
    key_df = output_df.copy()

    for name in os.listdir(DATAMAP_DIRNAME):
        if name.endswith('.json'):
            path = os.path.join(os.getcwd(), DATAMAP_DIRNAME, name)
            with open(path) as json_data:
                data = json.load(json_data)
            df = pd.DataFrame.from_dict(data, orient='index').reset_index().rename(columns={'index': 'Key', 0: name})

            #Merge on the key column
            temp_df = pd.DataFrame(pd.merge(key_df, df, on='Key', how='inner')[name])
            temp_df = temp_df.rename(columns={name: name})
            output_df = pd.concat([output_df, temp_df], axis=1)
            
    #save the new DataFrame to a CSV file

    output_df = output_df.T
    output_df.index.values[0] = ''
    print(output_df)
    output_df.to_csv(CSV_FILEPATH, header = False, index = False, encoding="utf-16")  