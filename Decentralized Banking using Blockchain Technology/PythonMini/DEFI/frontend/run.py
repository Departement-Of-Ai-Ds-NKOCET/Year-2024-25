#5FLCQoP3HyGgpvLQ8MEEOS2f3AncAq
#sepolia
#0x4543457E297B1d8f901102796d63596Fc07A0bcC
#0x8EbC37451D9f82647d68540908dba6Ed89cC81Eb

#0xd9a6e4718919bce695fc0cd984b7f28b08d044d3 0x86e70A4059487DB4176Fc0a4E036e6Bc6beAea7b 0x4F4fF82b3A446c623841b059c733Ac0eba6FF065

#from flask_wtf import FlaskForm,Form

import os
from flask import Flask, jsonify, render_template, request
from flask_wtf import FlaskForm,Form
from wtforms import SelectField
from brownie import accounts, Contract , network
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = "5FLCQoP3HyGgpvLQ8MEEOS2f3AncAq"
network.connect('sepolia')
usdcAddress = Contract('0x4543457E297B1d8f901102796d63596Fc07A0bcC')
defi_contract = Contract('0x8EbC37451D9f82647d68540908dba6Ed89cC81Eb')

account = accounts.add(os.getenv("PRIVATE_KEY"))
accounts.add(os.getenv("PRIVATE_KEY1"))
accounts.add(os.getenv("PRIVATE_KEY2"))

class Form(FlaskForm):
    Faccounts = SelectField('Account' , choices = ['0xd9a6e4718919bce695fc0cd984b7f28b08d044d3',
                                                    '0x86e70A4059487DB4176Fc0a4E036e6Bc6beAea7b',
                                                    '0x4F4fF82b3A446c623841b059c733Ac0eba6FF065'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deposit')
def deposit():
    form = Form()
    AvailableBal = SC_getAccountbal() / 10 ** 18
    DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
    return render_template('deposit.html', form = form, AvailableBal = AvailableBal, DepositedAmount = DepositedAmount)

@app.route('/depositButton', methods =['GET', 'POST'])
def depositButton():
    form = Form()
    if request.method == 'POST':
        depositAmount = request.form.get("depositValue", type = int) * (10 ** 18)
        SC_depositBal(depositAmount)
        DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
        AvailableBal = usdcAddress.balanceOf(account) /(10 ** 18)
    return render_template('deposit.html',form = form,  AvailableBal = AvailableBal, DepositedAmount = DepositedAmount)

@app.route('/withdrawButton', methods =['GET', 'POST'])
def withdrawButton():
    form = Form()
    if request.method == 'POST':
        withdrawAmount = request.form.get("withdrawValue", type = int) * (10 ** 18)
        SC_withdrawBal(withdrawAmount)
        DepositedAmount = defi_contract.depositBalance(account) / (10 ** 18)
        AvailableBal = usdcAddress.balanceOf(account) /(10 ** 18)
    return render_template('deposit.html',form = form,  AvailableBal = AvailableBal, DepositedAmount = DepositedAmount)

def SC_withdrawBal(withdrawAmount):
    defi_contract.withdraw(withdrawAmount, {"from": account})

def SC_getAccountbal():
    balance = usdcAddress.balanceOf(account)
    return balance

def SC_depositBal(depositAmount):
    usdcAddress.approve(defi_contract, depositAmount, {"from": account})
    defi_contract.depositToken(depositAmount, {"from": account})

@app.route('/refresh/<currentAccount>')
def refresh(currentAccount):
    global account
    account = accounts.at(currentAccount)
    currentBal = usdcAddress.balanceOf(account) /(10 ** 18)
    stakedBalance = defi_contract.depositBalance(account) / (10 ** 18)
    return jsonify({'response' : currentAccount ,'stakedBalance' : stakedBalance , 'currentBal': currentBal})

@app.route('/FundMe', methods =["GET", "POST"])
def FundMe():
    if request.method == "POST":
        FromAddress = request.form.get("fromAddress")
        FromAddress = accounts.at(FromAddress, force=True)
        ToAddress = request.form.get("toAddress")
        Amount = request.form.get("Amount", type = int)
        usdcAddress.transfer(ToAddress, Amount * 10 ** 18, {"from": FromAddress})
    return render_template('FundMe.html')

if __name__ == "__main__":
    
    app.run()
    network.disconnect()
