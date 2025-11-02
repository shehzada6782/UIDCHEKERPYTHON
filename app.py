from flask import Flask, request, jsonify, render_template_string
import requests
import re
import os
import urllib.parse

app = Flask(__name__)

# HTML Template with complete CSS and JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Post UID Extractor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
        }

        .input-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #555;
            font-size: 1.1rem;
        }

        input[type="url"] {
            width: 100%;
            padding: 15px 20px;
            border: 2px solid #e1e8ed;
            border-radius: 12px;
            font-size: 16px;
            transition: all 0.3s ease;
            margin-bottom: 20px;
            font-family: inherit;
        }

        input[type="url"]:focus {
            outline: none;
            border-color: #1877f2;
            box-shadow: 0 0 0 3px rgba(24, 119, 242, 0.2);
            transform: translateY(-2px);
        }

        button {
            background: linear-gradient(135deg, #1877f2, #0d66d0);
            color: white;
            border: none;
            padding: 18px 30px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            font-family: inherit;
        }

        button:hover:not(:disabled) {
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(24, 119, 242, 0.4);
        }

        button:disabled {
            opacity: 0.7;
            cursor: not-allowed;
            transform: none;
        }

        .result {
            margin-top: 25px;
        }

        .hidden {
            display: none !important;
        }

        .success-result, .error-result {
            padding: 25px;
            border-radius: 12px;
            margin-top: 20px;
            animation: slideDown 0.3s ease;
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .success-result {
            background: linear-gradient(135deg, #d4edda, #c3e6cb);
            border: 2px solid #28a745;
            color: #155724;
        }

        .error-result {
            background: linear-gradient(135deg, #f8d7da, #f5c6cb);
            border: 2px solid #dc3545;
            color: #721c24;
        }

        .result-item {
            margin: 20px 0;
        }

        .uid-display {
            display: flex;
            align-items: center;
            gap: 15px;
            margin: 15px 0;
            flex-wrap: wrap;
        }

        .uid-display span {
            background: #f8f9fa;
            padding: 15px 20px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 20px;
            font-weight: bold;
            flex: 1;
            border: 2px dashed #28a745;
            min-width: 200px;
        }

        .copy-btn {
            background: #28a745;
            width: auto;
            padding: 12px 25px;
            font-size: 16px;
            border-radius: 8px;
        }

        .copy-btn:hover {
            background: #218838;
            transform: translateY(-2px);
        }

        .full-url {
            color: #1877f2;
            text-decoration: none;
            word-break: break-all;
            display: block;
            margin-top: 8px;
            font-weight: 500;
        }

        .full-url:hover {
            text-decoration: underline;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .loading-spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #1877f2;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .instructions {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }

        .instructions h3 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.4rem;
        }

        .instructions ol {
            margin-left: 25px;
            margin-bottom: 25px;
            font-size: 1.05rem;
        }

        .instructions li {
            margin-bottom: 12px;
            line-height: 1.7;
        }

        .note {
            background: #fff3cd;
            border: 2px solid #ffeaa7;
            padding: 20px;
            border-radius: 10px;
            color: #856404;
            font-size: 1.05rem;
        }

        footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 30px;
            color: white;
            opacity: 0.9;
            font-size: 1rem;
        }

        @media (max-width: 768px) {
            body { padding: 15px; }
            header h1 { font-size: 2rem; }
            .card { padding: 25px 20px; }
            .uid-display { flex-direction: column; }
            .copy-btn { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📱 Facebook Post UID Extractor</h1>
            <p>Facebook post ka link daaliye aur UID instantly prapt kijiye</p>
        </header>

        <main>
            <div class="card">
                <div class="input-group">
                    <label for="postUrl">Facebook Post URL:</label>
                    <input type="url" id="postUrl" 
                           placeholder="https://www.facebook.com/share/p/1C8EEGCHWy/?mibextid=wwXIfr" 
                           required autocomplete="off">
                    <button id="extractBtn" onclick="extractUID()">
                        🎯 UID Extract Karein
                    </button>
                </div>

                <div id="result" class="result hidden">
                    <div id="successResult" class="success-result hidden">
                        <h3>✅ UID Successfully Extracted!</h3>
                        <div class="result-item">
                            <label>Post UID:</label>
                            <div class="uid-display">
                                <span id="postId"></span>
                                <button onclick="copyToClipboard()" class="copy-btn">
                                    📋 Copy
                                </button>
                            </div>
                        </div>
                        <div class="result-item">
                            <label>Full URL:</label>
                            <a id="fullUrl" target="_blank" class="full-url"></a>
                        </div>
                    </div>

                    <div id="errorResult" class="error-result hidden">
                        <h3>❌ Error</h3>
                        <p id="errorMessage"></p>
                    </div>
                </div>

                <div class="loading hidden" id="loading">
                    <div class="loading-spinner"></div>
                    <p>🔄 Facebook post ka data fetch kiya ja raha hai...</p>
                </div>
            </div>

            <div class="instructions">
                <h3>ℹ️ Kaise Use Karein:</h3>
                <ol>
                    <li><strong>Facebook post par jayein</strong> - Jis post ka UID chahiye</li>
                    <li><strong>Post ka complete URL copy karein</strong> - Address bar se</li>
                    <li><strong>Yahan paste karein</strong> - Upar wale box mein</li>
                    <li><strong>"UID Extract Karein" button dabayein</strong> - Aur result ka intezar karein</li>
                    <li><strong>Apna Post UID prapt karein!</strong> - Copy button se copy kar lein</li>
                </ol>

                <div class="note">
                    <strong>⚠️ Important Note:</strong> Ye tool aapke diye gaye URL se directly UID extract karta hai. 
                    Koi external libraries use nahi hoti, isliye 100% work karega! 
                    Example: "https://www.facebook.com/share/p/1C8EEGCHWy/" ka UID hai "1C8EEGCHWy"
                </div>
            </div>
        </main>

        <footer>
            <p>&copy; 2024 Facebook UID Extractor | Built with Python & Flask | Deployed on Render</p>
        </footer>
    </div>

    <script>
        let currentState = { isProcessing: false };

        async function extractUID() {
            if (currentState.isProcessing) return;
            
            const postUrl = document.getElementById('postUrl').value.trim();
            const extractBtn = document.getElementById('extractBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const successResult = document.getElementById('successResult');
            const errorResult = document.getElementById('errorResult');

            // Reset previous results
            successResult.classList.add('hidden');
            errorResult.classList.add('hidden');
            result.classList.add('hidden');
            loading.classList.remove('hidden');
            
            // Update state and UI
            currentState.isProcessing = true;
            extractBtn.disabled = true;
            extractBtn.textContent = '🔄 Processing...';

            if (!postUrl) {
                showError('Kripya Facebook post ka URL daalein');
                resetUI();
                return;
            }

            if (!isValidFacebookUrl(postUrl)) {
                showError('Kripya valid Facebook URL daalein (facebook.com ya fb.com)');
                resetUI();
                return;
            }

            try {
                const response = await fetch('/extract-uid', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ post_url: postUrl })
                });

                const data = await response.json();

                if (data.success) {
                    showSuccess(data.post_id, data.full_url);
                } else {
                    showError(data.error || 'UID extract nahi ho paya');
                }
            } catch (error) {
                console.error('Error:', error);
                showError('Network error: Server se connect nahi ho paya');
            } finally {
                resetUI();
            }
        }

        function isValidFacebookUrl(url) {
            const facebookPattern = /^(https?:\/\/)?(www\.)?(facebook|fb)\.com\/.+/i;
            return facebookPattern.test(url);
        }

        function showSuccess(postId, fullUrl) {
            const successResult = document.getElementById('successResult');
            const errorResult = document.getElementById('errorResult');
            const result = document.getElementById('result');
            const postIdElement = document.getElementById('postId');
            const fullUrlElement = document.getElementById('fullUrl');

            postIdElement.textContent = postId;
            fullUrlElement.href = fullUrl;
            fullUrlElement.textContent = fullUrl;

            errorResult.classList.add('hidden');
            successResult.classList.remove('hidden');
            result.classList.remove('hidden');

            result.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        function showError(message) {
            const successResult = document.getElementById('successResult');
            const errorResult = document.getElementById('errorResult');
            const result = document.getElementById('result');
            const errorMessage = document.getElementById('errorMessage');

            errorMessage.textContent = message;
            
            successResult.classList.add('hidden');
            errorResult.classList.remove('hidden');
            result.classList.remove('hidden');

            result.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        function resetUI() {
            const extractBtn = document.getElementById('extractBtn');
            const loading = document.getElementById('loading');
            
            currentState.isProcessing = false;
            extractBtn.disabled = false;
            extractBtn.textContent = '🎯 UID Extract Karein';
            loading.classList.add('hidden');
        }

        function copyToClipboard() {
            const postId = document.getElementById('postId').textContent;
            const copyBtn = document.querySelector('.copy-btn');
            
            navigator.clipboard.writeText(postId).then(() => {
                const originalText = copyBtn.textContent;
                copyBtn.textContent = '✅ Copied!';
                copyBtn.style.background = '#218838';
                
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                    copyBtn.style.background = '';
                }, 2000);
            }).catch(err => {
                const textArea = document.createElement('textarea');
                textArea.value = postId;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                copyBtn.textContent = '✅ Copied!';
                setTimeout(() => {
                    copyBtn.textContent = '📋 Copy';
                }, 2000);
            });
        }

        // Enter key support
        document.getElementById('postUrl').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !currentState.isProcessing) {
                extractUID();
            }
        });
    </script>
</body>
</html>
'''

def extract_uid_from_url(post_url):
    """
    Extract UID from Facebook share URL format without using any external libraries
    Example: https://www.facebook.com/share/p/1C8EEGCHWy/?mibextid=wwXIfr
    """
    try:
        # Parse the URL to get path
        parsed_url = urllib.parse.urlparse(post_url)
        path_parts = parsed_url.path.split('/')
        
        # Look for the pattern: /share/p/UID/
        if 'share' in path_parts and 'p' in path_parts:
            share_index = path_parts.index('share')
            if share_index + 2 < len(path_parts):
                uid = path_parts[share_index + 2]
                if uid and uid != '':  # Make sure UID is not empty
                    return uid
        
        # Alternative method: regex pattern for share URLs
        share_patterns = [
            r'/share/p/([^/?]+)',
            r'facebook\.com/share/p/([^/?]+)',
            r'/p/([^/?]+)'
        ]
        
        for pattern in share_patterns:
            match = re.search(pattern, post_url)
            if match:
                uid = match.group(1)
                if uid and uid != '':
                    return uid
        
        # Final fallback: get the last non-empty part of the path
        for part in reversed(path_parts):
            if part and part not in ['', 'share', 'p']:
                return part
                
        return None
        
    except Exception as e:
        print(f"Error extracting UID: {e}")
        return None

@app.route('/')
def home():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/extract-uid', methods=['POST'])
def extract_uid():
    """API endpoint to extract UID from Facebook post URL"""
    try:
        data = request.get_json()
        post_url = data.get('post_url', '').strip()

        if not post_url:
            return jsonify({'success': False, 'error': 'Post URL is required'}), 400

        # Validate Facebook URL
        if not re.match(r'^(https?://)?(www\.)?(facebook|fb)\.com/.+', post_url, re.IGNORECASE):
            return jsonify({
                'success': False, 
                'error': 'Invalid Facebook URL. Please use facebook.com or fb.com links only.'
            }), 400

        # Extract UID from URL
        post_id = extract_uid_from_url(post_url)

        if post_id:
            return jsonify({
                'success': True,
                'post_id': post_id,
                'full_url': f'https://facebook.com/{post_id}',
                'message': 'UID successfully extracted!'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not extract UID from the URL. Please make sure the URL is in the correct format: https://www.facebook.com/share/p/UID/'
            }), 404
            
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'OK', 
        'service': 'Facebook UID Extractor',
        'version': '3.0 - Simple & Working'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Facebook UID Extractor on port {port}")
    print(f"🌐 Access at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
