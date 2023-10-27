# The original function code:
def manage_permissions_route():
    error = None

    if request.method == 'POST':
        users.check_csrf()
        action = request.form.get('action')
        request_id = request.form.get('request_id')
        github_handle = request.form.get('github_handle')
        role = request.form.get('role')

        if action == 'approve':
            permissions.update_request_status(request_id, 'approved')
            permissions.add_permitted_user(github_handle, role)
        elif action == 'reject':
            permissions.update_request_status(request_id, 'rejected')
        else:
            try:
                permissions.add_permitted_user(github_handle, role)
            except Exception as e:
                error = f"Error occurred: {str(e)}"

    requests = permissions.get_pending_permission_requests()
    permitted_users = permissions.get_all_permitted_users()
    csrf_token = users.get_or_create_csrf_token()

    return render_template('manage_permissions.html', requests=requests, permitted_users=permitted_users, error=error, csrf_token=csrf_token)

# The refactored function code:
# In this version, input data validation is more concise and easier to read, 
# and the handling of the action is placed in a try-except block to catch exceptions. 

def manage_permissions_route():
    # Initialize error as None
    error = None

    # Handle negative cases first
    if request.method != 'POST':
        return render_template('manage_permissions.html')

    # Use clear and descriptive names
    csrf_token = users.check_csrf()
    
    # Validate input data
    action = request.form.get('action')
    request_id = request.form.get('request_id')
    github_handle = request.form.get('github_handle')
    role = request.form.get('role')

    if not (action and request_id and github_handle and role and csrf_token):
        error = "Invalid request"
        return render_template('manage_permissions.html', error=error)

    # Handle the action
    try:
        if action == 'approve':
            permissions.update_request_status(request_id, 'approved')
            permissions.add_permitted_user(github_handle, role)
        elif action == 'reject':
            permissions.update_request_status(request_id, 'rejected')
        else:
            permissions.add_permitted_user(github_handle, role)
    except Exception as e:
        error = f"Error occurred: {str(e)}"

    requests = permissions.get_pending_permission_requests()
    permitted_users = permissions.get_all_permitted_users()
    csrf_token = users.get_or_create_csrf_token()

    return render_template('manage_permissions.html', requests=requests, permitted_users=permitted_users, error=error, csrf_token=csrf_token)
