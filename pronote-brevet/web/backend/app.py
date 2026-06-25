from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pronotepy
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Servir les fichiers statiques (HTML, CSS, JS)
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API pour récupérer la moyenne générale depuis Pronote
@app.route('/api/pronote/moyenne', methods=['POST'])
def get_pronote_moyenne():
    data = request.json
    url = data.get('url')
    username = data.get('username')
    password = data.get('password')
    
    if not url or not username or not password:
        return jsonify({'error': 'URL, username et password requis'}), 400
    
    try:
        client = pronotepy.Client(url, username, password)
        
        # Récupérer la moyenne générale de la période en cours
        for period in client.periods:
            if period.name == "Trimestre 1" or period.name == "Trimestre 2" or period.name == "Trimestre 3":
                # La moyenne générale est dans period.average
                moyenne_generale = period.average.student.value
                if moyenne_generale:
                    return jsonify({
                        'success': True,
                        'moyenne_cc': round(moyenne_generale, 2),
                        'periode': period.name
                    })
        
        # Si pas trouvé, essayer de calculer depuis les notes
        notes = []
        for period in client.periods:
            for grade in period.grades:
                if grade.student.value:
                    notes.append(grade.student.value)
        
        if notes:
            moyenne = sum(notes) / len(notes)
            return jsonify({
                'success': True,
                'moyenne_cc': round(moyenne, 2),
                'periode': 'Calculée'
            })
        
        return jsonify({'error': 'Impossible de récupérer la moyenne générale'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
