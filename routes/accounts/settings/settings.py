from flask import render_template, Blueprint, g, redirect, url_for, request, flash
from database.db_commands import update_user_settings


page = Blueprint('settings', __name__, url_prefix='/settings')


@page.route('/', methods=['GET', 'POST'])
def home():
    if not g.user:
        return redirect(url_for('login.login'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        account_type_display = request.form.get('account_type', '').strip()
        
        # Map display names to database values
        account_type_map = {
            'private account': 'private_user',
            'teacher': 'teacher',
            'student': 'student'
        }
        account_type = account_type_map.get(account_type_display)
        
        if not username or not email or not account_type:
            flash('Username, email, and account type are required.', 'error')
            return redirect(url_for('settings.home'))
        
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('settings.home'))
        
        success, message = update_user_settings(g.user['user_id'], username, email, account_type)
        flash(message, 'success' if success else 'error')
        if success:
            return redirect(url_for('settings.home'))
    
    # Map database values to display names for the template
    account_type_display_map = {
        'private_user': 'private account',
        'teacher': 'teacher',
        'student': 'student'
    }
    current_account_type = account_type_display_map.get(g.user.get('account_type', 'private_user'), 'private account')
    
    return render_template('settings/settings.jinja', current_account_type=current_account_type)   