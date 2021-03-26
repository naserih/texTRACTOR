import os
import io
from flask import Flask, flash,abort, jsonify, render_template, request, send_file, url_for, send_from_directory
import env
import csv
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# from skimage.io import imsave, imread
# import _tkinter
# from scipy import ndimage


output_path = env.OUTPUTDATA
db = env.PATIENTS_DATABASE
SERVER_IP = env.SERVER_IP
SERVER_PORT = env.SERVER_PORT
notes_url = 'http://%s:%s/notes'%(SERVER_IP,SERVER_PORT)
KEYS = env.VALID_KEYS



def load_scores(directory):
    scores = {}
    if not os.path.exists(directory):
        os.makedirs(directory)
    elif 'pain_scores.csv' in os.listdir(directory):
        with open('%s/pain_scores.csv'%(directory), 'r') as csvfile:
                csvreader = csv.reader(csvfile, delimiter=',')
                for row in csvreader:
                    scores[row[0]] = row[1]
    return scores


app = Flask(__name__)


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# patient_metadata = {}



@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.cache_control.max_age = 3
    return response



@app.route("/notes/<patient_file>/")
def get_patient_file(patient_file):
    try:
        # print('FILE NAME >>>>>>', app.config["FILE_PATH"])
        # return send_from_directory(app.config["FILE_PATH"], filename=patient_file, as_attachment=True)
        return send_from_directory(app.config["FILE_PATH"], filename=patient_file, as_attachment=False)

        # return send_file(app.config["FILE_PATH"], attachment_filename=patient_file)

    except:
        abort(404, description="Resource not found %s"%app.config["FILE_PATH"])


@app.route('/_load_patients')
def load_patients():
    access_key = request.args.get('key', 0, type=str)
    if access_key in KEYS: 
        directory = '%s/%s_%s/%s'%(output_path, access_key,KEYS[access_key][0],KEYS[access_key][1])
        stored_scores = load_scores(directory)
        patient_file_path = db[KEYS[access_key][1]]
        patients_data = os.listdir(patient_file_path)
        if len(patients_data) == 0:
            patients_data = ['DONE']
    else:
        patients_data = []

    # print ('stored_scores > ', stored_scores)
    # print ('patients_data > ', patients_data)
    return jsonify(patients_data = patients_data, 
                    stored_scores = stored_scores)

@app.route('/_load_patient_file')
def load_patient_data():
    access_key = request.args.get('key', 0, type=str)
    fileId = request.args.get('fileId', 0, type=str)

    patient_file_path = db[KEYS[access_key][1]]
    # print(db)
    # print(patient_file_path)
    app.config["FILE_PATH"] = patient_file_path
    app.config["FILE_NAME"] = fileId
    app.config["FILE_URL"] = '%s/%s'%(notes_url,fileId) 
    # print('>>>', app.config["FILE_URL"])
    return jsonify(patient_file = app.config["FILE_URL"])



@app.route('/_post_scores', methods=['POST', 'GET'])
def post_scores():
    if request.method == 'POST':
        scores = request.json['scores']
        access_key = request.json['key']
        score_array = []
        for key in scores:
            score_array.append([scores[key]['file_name'], scores[key]['score']])
            # print (scores[key]['file_name'], scores[key]['score'])

        directory = '%s/%s_%s/%s'%(output_path, access_key,KEYS[access_key][0],KEYS[access_key][1])    
        with open('%s/pain_scores.csv'%(directory), 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerows(score_array)
        return jsonify(status='stored!')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/help")
def help():
    return render_template("help.html")

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host=SERVER_IP, port=SERVER_PORT)
    