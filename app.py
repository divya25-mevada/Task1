from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Sample user data (in production, use a proper database)
users = {
    'john.doe@email.com': {
        'password': 'password123',
        'name': 'John Doe',
        'accounts': {
            'checking': {'number': '***1234', 'balance': 12485.50},
            'savings': {'number': '***5678', 'balance': 45230.75},
            'business': {'number': '***9012', 'balance': 8750.25},
            'credit': {'number': '***1234', 'balance': 2150.00, 'limit': 10000.00}
        }
    }
}

# Sample transaction data
sample_transactions = [
    {
        'id': 1,
        'date': '2023-12-15',
        'description': 'Grocery Store',
        'type': 'payment',
        'account': 'checking',
        'amount': -85.50,
        'balance': 12485.50,
        'status': 'completed'
    },
    {
        'id': 2,
        'date': '2023-12-14',
        'description': 'Salary Deposit',
        'type': 'deposit',
        'account': 'checking',
        'amount': 4200.00,
        'balance': 12571.00,
        'status': 'completed'
    },
    {
        'id': 3,
        'date': '2023-12-13',
        'description': 'Electric Bill',
        'type': 'payment',
        'account': 'checking',
        'amount': -125.00,
        'balance': 8371.00,
        'status': 'completed'
    },
    {
        'id': 4,
        'date': '2023-12-12',
        'description': 'ATM Withdrawal',
        'type': 'withdrawal',
        'account': 'checking',
        'amount': -200.00,
        'balance': 8496.00,
        'status': 'completed'
    },
    {
        'id': 5,
        'date': '2023-12-11',
        'description': 'Transfer to Savings',
        'type': 'transfer',
        'account': 'checking',
        'amount': -1000.00,
        'balance': 8696.00,
        'status': 'completed'
    },
    {
        'id': 6,
        'date': '2023-12-10',
        'description': 'Gas Station',
        'type': 'payment',
        'account': 'checking',
        'amount': -45.75,
        'balance': 9696.00,
        'status': 'completed'
    },
    {
        'id': 7,
        'date': '2023-12-09',
        'description': 'Online Purchase',
        'type': 'payment',
        'account': 'checking',
        'amount': -299.99,
        'balance': 9741.75,
        'status': 'pending'
    }
]

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users and users[email]['password'] == password:
            session['loggedin'] = True
            session['email'] = email
            session['name'] = users[email]['name']
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect email/password!')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        user_data = users[session['email']]
        return render_template('dashboard.html', user=user_data)
    return redirect(url_for('login'))

@app.route('/transactions')
def transactions():
    if 'loggedin' in session:
        return render_template('transactions.html', transactions=sample_transactions)
    return redirect(url_for('login'))

@app.route('/accounts')
def accounts():
    if 'loggedin' in session:
        user_data = users[session['email']]
        return render_template('accounts.html', user=user_data)
    return redirect(url_for('login'))

@app.route('/transfers')
def transfers():
    if 'loggedin' in session:
        user_data = users[session['email']]
        return render_template('transfers.html', user=user_data)
    return redirect(url_for('login'))

@app.route('/bills')
def bills():
    if 'loggedin' in session:
        return render_template('bills.html')
    return redirect(url_for('login'))

@app.route('/cards')
def cards():
    if 'loggedin' in session:
        return render_template('cards.html')
    return redirect(url_for('login'))

@app.route('/loans')
def loans():
    if 'loggedin' in session:
        return render_template('loans.html')
    return redirect(url_for('login'))

@app.route('/investments')
def investments():
    if 'loggedin' in session:
        return render_template('investments.html')
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        user_data = users[session['email']]
        return render_template('profile.html', user=user_data)
    return redirect(url_for('login'))

@app.route('/settings')
def settings():
    if 'loggedin' in session:
        return render_template('settings.html')
    return redirect(url_for('login'))

@app.route('/api/transactions')
def api_transactions():
    if 'loggedin' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # Get filter parameters
    account_filter = request.args.get('account', '')
    type_filter = request.args.get('type', '')
    from_date = request.args.get('from_date', '')
    to_date = request.args.get('to_date', '')
    amount_range = request.args.get('amount_range', '')
    
    filtered_transactions = sample_transactions.copy()
    
    # Apply filters
    if account_filter:
        filtered_transactions = [t for t in filtered_transactions if t['account'] == account_filter]
    
    if type_filter:
        filtered_transactions = [t for t in filtered_transactions if t['type'] == type_filter]
    
    if from_date:
        filtered_transactions = [t for t in filtered_transactions if t['date'] >= from_date]
    
    if to_date:
        filtered_transactions = [t for t in filtered_transactions if t['date'] <= to_date]
    
    if amount_range:
        if amount_range == '0-100':
            filtered_transactions = [t for t in filtered_transactions if abs(t['amount']) <= 100]
        elif amount_range == '100-500':
            filtered_transactions = [t for t in filtered_transactions if 100 < abs(t['amount']) <= 500]
        elif amount_range == '500-1000':
            filtered_transactions = [t for t in filtered_transactions if 500 < abs(t['amount']) <= 1000]
        elif amount_range == '1000+':
            filtered_transactions = [t for t in filtered_transactions if abs(t['amount']) > 1000]
    
    return jsonify(filtered_transactions)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('name', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)