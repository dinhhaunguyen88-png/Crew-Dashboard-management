"""
Vercel Serverless Function - Ultra Minimal Test
NO external project imports - just Flask
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body style="background:#1a1a2e;color:#fff;font-family:Arial;padding:40px;">
        <h1 style="color:#3b82f6;">Vercel Flask Test</h1>
        <p style="color:#22c55e;">Flask is working!</p>
        <p>If you see this, Flask runs correctly on Vercel.</p>
        <p><a href="/api/status" style="color:#3b82f6;">Check Status API</a></p>
    </body>
    </html>
    """

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'ok',
        'message': 'Flask is running on Vercel'
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

# Vercel handler
handler = app

if __name__ == '__main__':
    app.run(debug=True, port=5000)
