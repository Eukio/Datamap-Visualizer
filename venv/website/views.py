from flask import Blueprint, flash, render_template, request, redirect, send_file
import pandas as pd
import os
import json
from werkzeug.utils import secure_filename
CSV_FILEPATH = CSV_FILEPATH = os.path.join(os.path.dirname(__file__), 'data', 'Data.csv')
DATAMAP_DIRNAME = os.path.join(os.path.dirname(__file__),'static', 'datamaps')

views = Blueprint('views', __name__)

@views.route('/', methods = ['GET','POST'])
def home():
    print(request.method, request.form)
    if request.method == 'POST' and 'export_csv' in request.form:
      createData()
      return send_file(CSV_FILEPATH, as_attachment=True, download_name='Data.csv', mimetype='text/csv')
    if request.method == 'POST' and 'file' in request.files:
        return uploadFile(request.files.get('file'))
    return render_template('home.html', boolean = True)

def uploadFile(file):
    if file.filename.endswith('.json'):
        file.save(os.path.join(DATAMAP_DIRNAME, secure_filename(file.filename)))
        flash(f'{file.filename} uploaded successfully!', 'success')
    return redirect('/')
      
def createData():

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