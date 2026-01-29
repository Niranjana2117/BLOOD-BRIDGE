"""
BLOOD – Blood Bank Application
Milestone 1: Local Development

A complete Flask web application for managing blood donations and requests.
Implements user registration, login, blood request creation, and donor-requestor matching.

Author: Development Team
Date: 2026
Version: 1.0.0
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
from ai_engine import (
    get_compatible_blood_groups, 
    filter_compatible_donors, 
    is_compatible,
    get_all_valid_blood_groups
)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'BLOOD_BANK_SECRET_KEY_2026_SECURE'

# ============================================================================
# IN-MEMORY DATA STORAGE
# ============================================================================

# Users storage: email -> {id, name, email, password, blood_group, role}
users = {}

# Blood requests: list of request dictionaries
requests_list = []

# Donation history: donor_email -> list of donations
donation_history = {}

# App metadata
APP_NAME = "BLOOD – Blood Bank Application"
APP_QUOTE = "Donate Blood, Save Lives"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def generate_unique_id(prefix):
    """
    Generate unique IDs for donors, requestors, and requests.
    
    Args:
        prefix (str): Prefix for the ID (e.g., 'donor_', 'requestor_', 'req_')
    
    Returns:
        str: Unique ID with prefix
    """
    return f"{prefix}{str(uuid.uuid4())[:8]}"


def get_current_user():
    """
    Get the currently logged-in user from session.
    
    Returns:
        dict: User dictionary or None if not logged in
    """
    if 'user_email' in session:
        return users.get(session['user_email'])
    return None


def is_user_logged_in():
    """Check if a user is currently logged in."""
    return 'user_email' in session


def get_donor_list():
    """Get list of all donors with their details."""
    return [user for user in users.values() if user['role'] == 'Donor']


def get_active_requests():
    """Get list of all active requests (status: Requested or Confirmed)."""
    return [req for req in requests_list if req['status'] in ['Requested', 'Confirmed']]


def get_user_requests(user_email, role):
    """
    Get requests specific to a user based on their role.
    
    Args:
        user_email (str): User's email
        role (str): User's role ('Donor' or 'Requestor')
    
    Returns:
        list: List of relevant requests
    """
    if role == 'Requestor':
        return [req for req in requests_list if req['requestor_email'] == user_email]
    elif role == 'Donor':
        return [req for req in requests_list if req['donor_email'] == user_email]
    return []


def record_donation(donor_email, request_id, blood_group, requestor_email):
    """
    Record a donation in the donation history.
    
    Args:
        donor_email (str): Email of the donor
        request_id (str): ID of the request
        blood_group (str): Blood group donated
        requestor_email (str): Email of the requestor
    """
    if donor_email not in donation_history:
        donation_history[donor_email] = []
    
    donation_record = {
        'request_id': request_id,
        'blood_group': blood_group,
        'requestor_email': requestor_email,
        'date_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    donation_history[donor_email].append(donation_record)


def get_compatible_donors_for_request(blood_group):
    """
    Get list of compatible donors for a given blood group using AI engine.
    
    Args:
        blood_group (str): Requested blood group
    
    Returns:
        list: List of compatible donors
    """
    all_donors = get_donor_list()
    compatible_donors = filter_compatible_donors(blood_group, all_donors)
    return compatible_donors


# ============================================================================
# ROUTES: HOME AND AUTHENTICATION
# ============================================================================

@app.route('/')
def index():
    """Home page of the application."""
    current_user = get_current_user()
    return render_template('index.html', 
                         app_name=APP_NAME, 
                         app_quote=APP_QUOTE,
                         current_user=current_user)


@app.route('/register-type')
def register_type():
    """Show registration type selection (Donor or Requestor)."""
    return render_template('register_type.html', 
                         app_name=APP_NAME, 
                         app_quote=APP_QUOTE)


@app.route('/register/<user_type>', methods=['GET', 'POST'])
def register(user_type):
    """
    Register a new user (Donor or Requestor).
    
    Args:
        user_type (str): 'donor' or 'requestor'
    """
    # Validate user type
    if user_type.lower() not in ['donor', 'requestor']:
        flash('Invalid user type!', 'danger')
        return redirect(url_for('register_type'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        blood_group = request.form.get('blood_group', '').strip().upper()
        
        # Validation
        if not name or not email or not password:
            flash('All fields are required!', 'warning')
            return redirect(url_for('register', user_type=user_type))
        
        if user_type.lower() == 'donor' and not blood_group:
            flash('Blood group is required for donors!', 'warning')
            return redirect(url_for('register', user_type=user_type))
        
        # Check if blood group is valid
        valid_blood_groups = get_all_valid_blood_groups()
        if user_type.lower() == 'donor' and blood_group not in valid_blood_groups:
            flash(f'Invalid blood group! Valid groups: {", ".join(valid_blood_groups)}', 'danger')
            return redirect(url_for('register', user_type=user_type))
        
        # Check if email already exists
        if email in users:
            flash('Email already registered!', 'danger')
            return redirect(url_for('register', user_type=user_type))
        
        # Create new user
        role = 'Donor' if user_type.lower() == 'donor' else 'Requestor'
        user_id = generate_unique_id(f"{role.lower()}_")
        
        users[email] = {
            'id': user_id,
            'name': name,
            'email': email,
            'password': generate_password_hash(password),
            'blood_group': blood_group if user_type.lower() == 'donor' else None,
            'role': role,
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        flash(f'Registration successful! Please log in.', 'success')
        return redirect(url_for('login_type'))
    
    valid_blood_groups = get_all_valid_blood_groups()
    return render_template('register.html', 
                         user_type=user_type,
                         app_name=APP_NAME,
                         app_quote=APP_QUOTE,
                         blood_groups=valid_blood_groups)


@app.route('/login-type')
def login_type():
    """Show login type selection (Donor or Requestor)."""
    return render_template('login_type.html', 
                         app_name=APP_NAME, 
                         app_quote=APP_QUOTE)


@app.route('/login/<user_type>', methods=['GET', 'POST'])
def login(user_type):
    """
    Login a user (Donor or Requestor).
    
    Args:
        user_type (str): 'donor' or 'requestor'
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        
        # Validate input
        if not email or not password:
            flash('Email and password required!', 'warning')
            return redirect(url_for('login', user_type=user_type))
        
        # Check if user exists
        if email not in users:
            flash('User not found!', 'danger')
            return redirect(url_for('login', user_type=user_type))
        
        user = users[email]
        
        # Verify password
        if not check_password_hash(user['password'], password):
            flash('Invalid password!', 'danger')
            return redirect(url_for('login', user_type=user_type))
        
        # Verify role matches
        expected_role = 'Donor' if user_type.lower() == 'donor' else 'Requestor'
        if user['role'] != expected_role:
            flash(f'This account is registered as a {user["role"]}, not a {expected_role}!', 'danger')
            return redirect(url_for('login', user_type=user_type))
        
        # Create session
        session['user_email'] = email
        session['user_role'] = user['role']
        
        flash(f'Welcome back, {user["name"]}!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('login.html', 
                         user_type=user_type,
                         app_name=APP_NAME,
                         app_quote=APP_QUOTE)


@app.route('/logout')
def logout():
    """Logout the current user."""
    if 'user_email' in session:
        user_name = users[session['user_email']]['name']
        session.clear()
        flash(f'You have been logged out. Goodbye!', 'info')
    return redirect(url_for('index'))


# ============================================================================
# ROUTES: DASHBOARD AND REQUEST MANAGEMENT
# ============================================================================

@app.route('/dashboard')
def dashboard():
    """
    User dashboard (role-based).
    - Requestor: View their blood requests
    - Donor: View available requests and their donation history
    """
    current_user = get_current_user()
    
    if not current_user:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login_type'))
    
    role = current_user['role']
    
    if role == 'Requestor':
        # Requestor dashboard: show their requests
        user_requests = [req for req in requests_list if req['requestor_email'] == current_user['email']]
        return render_template('dashboard.html',
                             app_name=APP_NAME,
                             app_quote=APP_QUOTE,
                             current_user=current_user,
                             role=role,
                             user_requests=user_requests,
                             compatible_donors=None)
    
    elif role == 'Donor':
        # Donor dashboard: show active requests and donation history
        active_requests = get_active_requests()
        donor_donations = donation_history.get(current_user['email'], [])
        
        # Enrich requests with compatible donor info
        for req in active_requests:
            compatible_donors = get_compatible_donors_for_request(req['blood_group'])
            req['compatible_donors'] = compatible_donors
        
        return render_template('dashboard.html',
                             app_name=APP_NAME,
                             app_quote=APP_QUOTE,
                             current_user=current_user,
                             role=role,
                             active_requests=active_requests,
                             donation_history=donor_donations)
    
    return redirect(url_for('index'))


@app.route('/request', methods=['GET', 'POST'])
def create_request():
    """
    Create a new blood request (Requestor only).
    """
    current_user = get_current_user()
    
    if not current_user:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login_type'))
    
    if current_user['role'] != 'Requestor':
        flash('Only requestors can create requests!', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        blood_group = request.form.get('blood_group', '').strip().upper()
        units = request.form.get('units', '0')
        
        # Validation
        valid_blood_groups = get_all_valid_blood_groups()
        if blood_group not in valid_blood_groups:
            flash(f'Invalid blood group! Valid groups: {", ".join(valid_blood_groups)}', 'danger')
            return redirect(url_for('create_request'))
        
        try:
            units = int(units)
            if units <= 0:
                raise ValueError
        except ValueError:
            flash('Units must be a positive number!', 'warning')
            return redirect(url_for('create_request'))
        
        # Create new request
        request_id = generate_unique_id('req_')
        
        new_request = {
            'id': request_id,
            'blood_group': blood_group,
            'units': units,
            'requestor_email': current_user['email'],
            'requestor_name': current_user['name'],
            'donor_email': None,
            'donor_name': None,
            'status': 'Requested',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'compatibility_info': get_compatible_blood_groups(blood_group)
        }
        
        requests_list.append(new_request)
        
        flash(f'Blood request created successfully! Request ID: {request_id}', 'success')
        return redirect(url_for('dashboard'))
    
    valid_blood_groups = get_all_valid_blood_groups()
    return render_template('request.html',
                         app_name=APP_NAME,
                         app_quote=APP_QUOTE,
                         current_user=current_user,
                         blood_groups=valid_blood_groups)


@app.route('/donors')
def view_donors():
    """
    View all donors and their details.
    Shows AI-recommended compatible donors based on current context.
    """
    current_user = get_current_user()
    
    if not current_user:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login_type'))
    
    all_donors = get_donor_list()
    
    # Get compatible donors info
    compatible_donors_info = {}
    for donor in all_donors:
        compatible_donors_info[donor['email']] = {
            'blood_group': donor['blood_group'],
            'is_active': True
        }
    
    return render_template('donors.html',
                         app_name=APP_NAME,
                         app_quote=APP_QUOTE,
                         current_user=current_user,
                         all_donors=all_donors,
                         compatible_donors_info=compatible_donors_info)


@app.route('/donor/<donor_email>')
def donor_profile(donor_email):
    """
    View a specific donor's profile and donation history.
    """
    current_user = get_current_user()
    
    if not current_user:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login_type'))
    
    # Get donor info
    if donor_email not in users:
        flash('Donor not found!', 'danger')
        return redirect(url_for('view_donors'))
    
    donor = users[donor_email]
    
    if donor['role'] != 'Donor':
        flash('This user is not a donor!', 'danger')
        return redirect(url_for('view_donors'))
    
    # Get donor's donation history
    donor_donations = donation_history.get(donor_email, [])
    
    # Get compatible blood groups for this donor
    compatible_requests = [
        req for req in get_active_requests()
        if is_compatible(donor['blood_group'], req['blood_group'])
    ]
    
    return render_template('donor_profile.html',
                         app_name=APP_NAME,
                         app_quote=APP_QUOTE,
                         current_user=current_user,
                         donor=donor,
                         donation_history=donor_donations,
                         compatible_requests=compatible_requests)


# ============================================================================
# ROUTES: DONATION ACCEPTANCE AND CONFIRMATION
# ============================================================================

@app.route('/donate-blood/<request_id>', methods=['GET', 'POST'])
def donate_blood(request_id):
    """
    Accept a blood request (Donor accepts to donate).
    
    Args:
        request_id (str): ID of the request to accept
    """
    current_user = get_current_user()
    
    if not current_user:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login_type'))
    
    if current_user['role'] != 'Donor':
        flash('Only donors can accept requests!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Find the request
    blood_request = None
    for req in requests_list:
        if req['id'] == request_id:
            blood_request = req
            break
    
    if not blood_request:
        flash('Request not found!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check if request is still available
    if blood_request['status'] != 'Requested':
        flash('This request is no longer available!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check compatibility using AI engine
    if not is_compatible(current_user['blood_group'], blood_request['blood_group']):
        flash(f'Your blood group ({current_user["blood_group"]}) is not compatible with the requested blood group ({blood_request["blood_group"]})!', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Accept the request
        blood_request['donor_email'] = current_user['email']
        blood_request['donor_name'] = current_user['name']
        blood_request['status'] = 'Accepted'
        blood_request['accepted_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Record in donation history
        record_donation(
            current_user['email'],
            request_id,
            blood_request['blood_group'],
            blood_request['requestor_email']
        )
        
        flash(f'You have successfully accepted the request! Donation recorded in your history.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('confirmation.html',
                         app_name=APP_NAME,
                         app_quote=APP_QUOTE,
                         current_user=current_user,
                         blood_request=blood_request,
                         action='donate')


@app.route('/confirm/<request_id>', methods=['GET', 'POST'])
def confirm_request(request_id):
    """
    Confirm that a request has been fulfilled (Requestor confirms donation received).
    Updates request status from Accepted to Confirmed.
    
    Args:
        request_id (str): ID of the request to confirm
    """
    current_user = get_current_user()
    
    if not current_user:
        flash('Please log in first!', 'warning')
        return redirect(url_for('login_type'))
    
    # Find the request
    blood_request = None
    for req in requests_list:
        if req['id'] == request_id:
            blood_request = req
            break
    
    if not blood_request:
        flash('Request not found!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Verify ownership
    if blood_request['requestor_email'] != current_user['email']:
        flash('You can only confirm your own requests!', 'danger')
        return redirect(url_for('dashboard'))
    
    # Check status
    if blood_request['status'] != 'Accepted':
        flash('This request is not in the correct status for confirmation!', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Confirm the donation
        blood_request['status'] = 'Confirmed'
        blood_request['confirmed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        flash(f'Donation confirmed! Thank you for saving a life.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('confirmation.html',
                         app_name=APP_NAME,
                         app_quote=APP_QUOTE,
                         current_user=current_user,
                         blood_request=blood_request,
                         action='confirm')


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors."""
    return render_template('index.html',
                         app_name=APP_NAME,
                         app_quote=APP_QUOTE,
                         error="Page not found"), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Handle 500 errors."""
    return render_template('index.html',
                         app_name=APP_NAME,
                         app_quote=APP_QUOTE,
                         error="Internal server error"), 500


# ============================================================================
# TEMPLATE CONTEXT PROCESSOR
# ============================================================================

@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    return {
        'app_name': APP_NAME,
        'app_quote': APP_QUOTE,
        'current_user': get_current_user()
    }


# ============================================================================
# MAIN APPLICATION ENTRY POINT
# ============================================================================

if __name__ == '__main__':
    """
    Run the Flask application in debug mode.
    Access at http://127.0.0.1:5000
    """
    print(f"\n{'=' * 70}")
    print(f"  {APP_NAME}")
    print(f"  {APP_QUOTE}")
    print(f"{'=' * 70}")
    print(f"\nStarting Flask application in DEBUG mode...")
    print(f"Access the application at: http://127.0.0.1:5000")
    print(f"\nPress Ctrl+C to stop the server.\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000)
