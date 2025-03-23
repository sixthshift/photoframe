import os
import logging
import threading
import json
from flask import Flask, request, render_template, redirect, jsonify
from configparser import ConfigParser

# Create Flask app
app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static'))

# Global reference to the refresh function (will be set by main.py)
refresh_function = None
config_path = 'config.ini'

@app.route('/')
def home():
    """Render the management interface"""
    config = get_config()
    return render_template('management.html', config=config)

@app.route('/update-config', methods=['POST'])
def update_config():
    """Update the configuration file"""
    try:
        # Read current config first
        config = ConfigParser()
        config.read(config_path)
        
        # Initialize DEFAULT section if it doesn't exist
        if 'DEFAULT' not in config:
            config['DEFAULT'] = {}
            
        # Update config with form values
        for key, value in request.form.items():
            config['DEFAULT'][key] = value
            
        # Write updated config to file
        with open(config_path, 'w') as f:
            config.write(f)
            
        # Trigger a refresh if the function is available
        if refresh_function:
            threading.Thread(target=refresh_function).start()
            
        return jsonify({'status': 'success', 'message': 'Configuration updated successfully'})
    except Exception as e:
        logging.error(f"Error updating config: {e}")
        return jsonify({'status': 'error', 'message': f'Error: {str(e)}'})

@app.route('/refresh', methods=['POST'])
def refresh():
    """Trigger a manual refresh"""
    if refresh_function:
        threading.Thread(target=refresh_function).start()
        return jsonify({'status': 'success', 'message': 'Refresh triggered'})
    else:
        return jsonify({'status': 'error', 'message': 'Refresh function not available'})

@app.route('/logs')
def logs():
    """Get the latest logs"""
    try:
        log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'photoframe.log')
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                # Get the last 50 lines
                lines = f.readlines()[-50:]
                return jsonify({'status': 'success', 'logs': ''.join(lines)})
        return jsonify({'status': 'error', 'message': 'Log file not found'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error reading logs: {str(e)}'})

def get_config():
    """Get the current configuration"""
    config = ConfigParser()
    if os.path.exists(config_path):
        config.read(config_path)
        if 'DEFAULT' in config:
            return dict(config['DEFAULT'])
    return {'URL': '', 'INTERVAL': '3600'}

def start_server(refresh_callback=None, host='0.0.0.0', port=8080):
    """Start the management server"""
    global refresh_function
    refresh_function = refresh_callback
    
    # Run Flask in a separate thread
    threading.Thread(target=lambda: app.run(host=host, port=port, debug=False)).start()
    
    logging.info(f"Management server started at http://{host}:{port}") 