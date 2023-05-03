from flask import Flask, render_template, request, url_for, redirect
from funs import get_summ_pairs, store_res, create_connection
import random
import copy
import platform
import flask
import os

app = Flask(__name__)
# app = Flask(__name__,
#             static_url_path='',
#             static_folder='static',
#             template_folder='templates')


@app.route('/')
def index():
  return redirect(url_for('news_headline_subjectivity'))


@app.route('/surveys/news_headline_subjectivity', methods=['GET', 'POST'])
def news_headline_subjectivity():
  surveydb = 'survey_v2.db'
  conn = create_connection(surveydb)

  summ_pairs_before_shuffle = get_summ_pairs(conn)
  summ_pairs = copy.deepcopy(summ_pairs_before_shuffle)
  random.shuffle(summ_pairs)
  idx = [0, 1]
  opt = ['1', '2', 'c', 'D']
  name = '000'
  if request.method == 'GET':
    return render_template("main.html", lst=summ_pairs)
  if request.method == 'POST':
    name = request.form.get('name')
    res1 = request.form.get("1")
    res2 = request.form.get("2")
    res3 = request.form.get("3")
    res4 = request.form.get("4")
    res5 = request.form.get("5")
    res6 = request.form.get("6")
    res = [res1, res2, res3, res4, res5, res6]

    store_res(conn, summ_pairs, name, res)

    with conn:
      cur = conn.cursor()
      cur.execute("SELECT * FROM response")
      d = cur.fetchall()
    print('\n ----res table data-----\n', d)

    return redirect(
      url_for('news_headline_subjectivity',
              idx=idx,
              lst=summ_pairs,
              name=name,
              op=opt))
    #html template: https://codepen.io/emcmillan13/pen/yzgawM


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
# app.run(host='0.0.0.0', port=81, debug=True)
# https://stackoverflow.com/questions/66104059/passing-radio-button-value-on-page-refresh-in-flask
