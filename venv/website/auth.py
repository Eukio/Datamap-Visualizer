from flask import Blueprint , render_template, request,redirect, flash, session
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
import collect 


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
 
    if request.method == 'POST' and 'login' in request.form:
       
        session['username'] = request.form.get('username')
        session['password'] = request.form.get('password')
        
        success = runCollect()
        if success == False:
            flash('Username or Password is incorrect', category='error')            
        else:
            return redirect('/home')
    return render_template('login.html', boolean=True)

def runCollect():
    return collect.main(session['username'], session['password'])





