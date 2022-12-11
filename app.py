import pandas as pd
import matplotlib.pyplot as plt
# import flask
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)



def update_data(df, col, val, sign):
    
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
        print('Invalid sign')
        return None

    return(up_df)

def gen_report(df):
    print('Report:')

    print("TEXT: ")
    print('Total number of people: ', len(df))
    # print('Average age of people: ', df['age'].mean())
    print('Most common diseases:'), print(df['disease'].value_counts().head(3))
    print('Most common ethinicities:'), print(df['ancestry'].value_counts().head(3))
    # print('Most common symptoms:'), print(df['symptom'].value_counts().head(3))
    print('Gender distribution'), print(df['gender'].value_counts())
    # print('Most common previous diseases'), print(df['prev_disease'].value_counts().head(3))

    print("PLOTS: ")
    plt.subplot(2, 2, 1)


    plt.title('Disease distribution')
    df['disease'].value_counts().plot(kind='pie')
    plt.show()

    # plt.title('Age distribution')
    # df['age'].value_counts().plot(kind='pie')
    # plt.show()

    plt.title('Gender distribution')
    df['gender'].value_counts().plot(kind='bar')
    plt.show()

    plt.title('Ancestry distribution')
    df['ancestry'].value_counts().plot(kind='bar')
    plt.show()
    

@app.route("/")
def hello_world():
    return render_template('index.html')

if __name__ == '__main__':
    app.run_server(debug=True)

    