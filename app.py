import pandas as pd
import matplotlib.pyplot as plt
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for

app = Flask(__name__)

old_data = []


def update_data(df, col="", val="", sign=""):
    
    if sign == '>':
        up_df = df[df[col] > val]  
    elif sign == '<':
        up_df = df[df[col] < val]
    elif sign == '=':
        up_df = df[df[col] == val]
    elif sign == '>=':
        up_df = df[df[col] >= val]
    elif sign == '<=':
        up_df = df[df[col] <= val]
    else:
        return(df)

    return(up_df)

def gen_report(df):
    print('Report:')

    # print("TEXT: \n" + 'Total number of people: ', len(df) + '\n' + 'Average age of people: ', df['age'].mean() + '\n' + 'Most common diseases:' + df['disease'].value_counts().head(3)) + '\n' + 'Most common ethinicities:' + df['ancestry'].value_counts().head(3)) + '\n' + 'Most common symptoms:' + df['symptom'].value_counts().head(3)) + '\n' + 'Gender distribution'), print(df['gender'].value_counts() + '\n' + 'Most common previous diseases'), print(df['prev_disease'].value_counts().head(3))
    # report = ("TEXT: \n" + 'Total number of people: ', str(len(df)) + '\n' + 'Average age of people: ', str(df['age'].mean()) + '\n' + 'Most common diseases:' + str(df['disease'].value_counts().head(3))) + '\n' + 'Most common ethinicities:' + str(df['ancestry'].value_counts().head(3)) + '\n' + str('Most common symptoms:' + df['symptom'].value_counts().head(3)) + '\n' + 'Gender distribution' + str(df['gender'].value_counts()) + '\n' + 'Most common previous diseases' + str(df['prev_disease'].value_counts().head(3))
    report = ''
    report.append(str('Total number of people: ', len(df)))
    report.append(str('Average age of people: ', df['age'].mean()))
    report.append(str('Most common diseases:'), print(df['disease'].value_counts().head(3)))
    report.append(str('Most common ethinicities:'), print(df['ancestry'].value_counts().head(3)))
    report.append(str('Most common symptoms:'), print(df['symptom'].value_counts().head(3)))
    report.append(str('Gender distribution'), print(df['gender'].value_counts()))
    report.append(str('Most common previous diseases'), print(df['prev_disease'].value_counts().head(3)))

    # print("PLOTS: ")
    # plt.subplot(2, 2, 1)


    # plt.title('Disease distribution')
    # df['disease'].value_counts().plot(kind='pie')
    # plt.show()

    # # plt.title('Age distribution')
    # # df['age'].value_counts().plot(kind='pie')
    # # plt.show()

    # plt.title('Gender distribution')
    # df['gender'].value_counts().plot(kind='bar')
    # plt.show()

    # plt.title('Ancestry distribution')
    # df['ancestry'].value_counts().plot(kind='bar')
    # plt.show()
    
    return(report)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():
    form_data = request.form.to_dict(flat=False)
    email = request.form['email']
    old_data.append(form_data)
    jsonStr = json.dumps(old_data)
    print(jsonStr)

    # Writing to sample.json
    with open("sample.json", "w") as outfile:
        outfile.write(jsonStr)

    return ("Success", 200)

@app.route("/analysis", methods=['GET'])
def analysis():
    report = gen_report(pd.read_json('sample.json'))
    return(report)




if __name__ == '__main__':
    app.run_server(debug=True)

    