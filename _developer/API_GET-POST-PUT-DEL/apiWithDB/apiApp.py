from flask import Flask, jsonify, render_template, request, redirect, url_for
import requests
import metodoRequestDB as db
from time import sleep

app = Flask(__name__)

#requisita todos os valores
@app.route('/')
def requestGETdata():
    db.RequestDB('')
    rtData=db.RequestDB('').requestGET()    
    db.RequestDB('').closeDB()
    rtData=[rtData[i] for i in range(len(rtData))]
    return render_template('index.html', itemsDB=rtData)

#insere um valor no banco
@app.route('/api/register', methods=['POST'])
def requestPOSTdata():
    if request.method=='POST':
        db.RequestDB('')
        db.RequestDB('').requestPOST(request.form.get('nome'), request.form.get('email'))
        sleep(1)
        db.RequestDB('').closeDB()
    return redirect(url_for('requestGETdata'))

#efetua a alteração de um valor no banco
@app.route('/put/<id>', methods=['POST'])
def requestPUTdata(id):
    if request.method=='POST':
        db.RequestDB('').requestPUT(request.form.get('nome'), request.form.get('email'), id)
        db.RequestDB('').closeDB()
    return redirect(url_for("requestGETdata"))

#deleta o valor
@app.route('/del/<id>')
def requestDELETEdata(id):
    db.RequestDB('')
    db.RequestDB('').requestDELETE(id)
    db.RequestDB('').closeDB()
    return redirect(url_for("requestGETdata"))


if __name__=='__main__':
    app.run(debug=True)