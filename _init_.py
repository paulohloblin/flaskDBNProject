from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('click_db')
    return conn


connection = get_db_connection()

cur = connection.cursor()

queries = [item[0] for item in cur.execute("SELECT DISTINCT Запит FROM click_log").fetchall()]
doc_list = []
query = ['']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results_updated', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       qr = query[0] = request.form['search_q']
       connection = get_db_connection()
       cur = connection.cursor()
       doc_list = [item[0] for item in cur.execute(f'SELECT Документ FROM click_log WHERE  Запит = ?', (qr,)).fetchall()]
       print(qr)
       print(doc_list)
       return render_template('results.html', queries=queries, doc_list=doc_list, qr=qr)


@app.route('/ctr_res')
def res():
    if request.method == "GET":
       qr = query[0]
       sel_doc = request.args['inputState']
       connection = get_db_connection()
       cur = connection.cursor()
       ctr = cur.execute(f'SELECT "a" FROM click_log WHERE Документ = ? AND Запит = ?', (sel_doc, qr)).fetchall()[0][0]
       sat = cur.execute(f'SELECT "s" FROM click_log_s WHERE Документ = ? AND Запит = ?', (sel_doc, qr)).fetchall()[0][0]
       relev = ctr*sat
       return jsonify(ctr="{0:.1f}".format(ctr*100),sat="{0:.1f}".format(sat*100),relev="{0:.1f}".format(relev*100))


@app.route('/existing_prods')
def existing_prods():
    return render_template('existing_prods.html')


@app.route('/model_info')
def model_info():
    return render_template('model_info.html')


@app.route('/results')
def results():
    return render_template('results.html', queries=queries, doc_list=doc_list, qr=query[0])


def getApp():
    return app


if __name__ == '__main__':
    app.run()
