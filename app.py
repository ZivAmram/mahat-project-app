from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo
import requests


app = Flask(__name__)


app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
client = pymongo.MongoClient('mongo', 27017)
db = client.user_login_system
db = client.coins

# Decorators
def login_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return redirect('/')
  
  return wrap

# Routes
from user import routes

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
  return render_template('dashboard.html')


@app.route('/market/')
@login_required
def market():
  url = "https://www.marketwatch.com/investing/cryptocurrency"
  
  # Headers to mimic the browser
  headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
  }
    
  # Get the page through get() method
  html_response = requests.get(url=url, headers = headers)
  btcusd = str(html_response.text).split('Bitcoin USD')[1].split('realtime">')[1].split('<')[0]
  btcusdper = float(str(html_response.text).split('Bitcoin USD')[1].split('percentchange')[1].split('</bg-quote>')[0].split('>')[1].replace('%', ''))
  ethusd = str(html_response.text).split('Ethereum USD')[1].split('realtime">')[1].split('<')[0]
  ethusdper = float(str(html_response.text).split('Ethereum USD')[1].split('percentchange')[1].split('</bg-quote>')[0].split('>')[1].replace('%', ''))
  # dogeusd = str(html_response.text).split('Dogecoin USD')[1].split('realtime">')[1].split('<')[0]
  # dogeusdper = float(str(html_response.text).split('Dogecoin USD')[1].split('percentchange')[1].split('</bg-quote>')[0].split('>')[1].replace('%', ''))
  xrpusd = str(html_response.text).split('XRP USD')[1].split('realtime">')[1].split('<')[0]
  xrpusdper = float(str(html_response.text).split('XRP USD')[1].split('percentchange')[1].split('</bg-quote>')[0].split('>')[1].replace('%', ''))
  ltcusd = str(html_response.text).split('Litecoin USD')[1].split('realtime">')[1].split('<')[0]
  ltcusdper = float(str(html_response.text).split('Litecoin USD')[1].split('percentchange')[1].split('</bg-quote>')[0].split('>')[1].replace('%', ''))
  bchusd = str(html_response.text).split('Bitcoin Cash USD')[1].split('realtime">')[1].split('<')[0]
  bchusdper = float(str(html_response.text).split('Bitcoin Cash USD')[1].split('percentchange')[1].split('</bg-quote>')[0].split('>')[1].replace('%', ''))

  # return render_template('market.html' , btc = btcusd , btcper = btcusdper , eth = ethusd , ethper = ethusdper , doge = dogeusd , dogeper = dogeusdper , xrp = xrpusd , xrpper = xrpusdper , ltc = ltcusd , ltcper = ltcusdper , bch = bchusd , bchper = bchusdper)
  return render_template('market.html' , btc = btcusd , btcper = btcusdper , eth = ethusd , ethper = ethusdper , xrp = xrpusd , xrpper = xrpusdper , ltc = ltcusd , ltcper = ltcusdper , bch = bchusd , bchper = bchusdper)
  