from flask import Blueprint, render_template, url_for, redirect, request

mod = Blueprint('account', __name__)

@mod.route('/', methods=['GET', 'POST'])
def signin():
  if request.method == 'GET':
    return render_template('signin.html')
  elif request.method == 'POST':
    # login process...    
    # ID & PW check and add session   
    return redirect(url_for('streamer.stream_cctv'))

@mod.route('/signout')
def signout():
  # session clear   
  return redirect(url_for('account.signin'))

