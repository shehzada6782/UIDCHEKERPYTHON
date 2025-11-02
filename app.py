from flask import Flask, request, jsonify, render_template_string
import requests
import re
import os
import time
import random

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
            backdrop-filter: blur(10px);
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
            text-transform: uppercase;
            letter-spacing: 0.5px;
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
            display: flex;
            align-items: center;
            gap: 10px;
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

        /* Responsive Design */
        @media (max-width: 768px) {
            body {
                padding: 15px;
            }
            
            header h1 {
                font-size: 2rem;
            }
            
            .card {
                padding: 25px 20px;
            }
            
            .uid-display {
                flex-direction: column;
                align-items: stretch;
            }
            
            .copy-btn {
                width: 100%;
            }
            
            input[type="url"] {
                font-size: 16px; /* Prevents zoom on iOS */
            }
        }

        @media (max-width: 480px) {
            header h1 {
                font-size: 1.8rem;
            }
            
            .card {
                padding: 20px 15px;
            }
            
            button {
                padding: 16px 25px;
                font-size: 16px;
            }
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
                           placeholder="https://www.facebook.com/username/posts/... ya https://fb.com/..." 
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
                    <strong>⚠️ Important Note:</strong> Ye tool sirf public Facebook posts ke liye kaam karta hai. 
                    Private posts, groups ke posts, ya restricted content ka UID extract nahi kar sakta. 
                    Agar error aaye to please post URL check karein aur phir try karein.
                </div>
            </div>
        </main>

        <footer>
            <p>&copy; 2024 Facebook UID Extractor | Built with Python & Flask | Deployed on Render</p>
        </footer>
    </div>

    <script>
        // Global variable to track current state
        let currentState = {
            isProcessing: false
        };

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
            extractBtn.style.opacity = '0.8';

            // Basic validation
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
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ post_url: postUrl })
                });

                const data = await response.json();

                if (data.success) {
                    showSuccess(data.post_id, data.full_url);
                } else {
                    showError(data.error || 'UID extract nahi ho paya. Post public hai?');
                }
            } catch (error) {
                console.error('Error:', error);
                showError('Network error: Server se connect nahi ho paya. Internet check karein.');
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

            // Scroll to result smoothly
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

            // Scroll to result smoothly
            result.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        function resetUI() {
            const extractBtn = document.getElementById('extractBtn');
            const loading = document.getElementById('loading');
            
            currentState.isProcessing = false;
            extractBtn.disabled = false;
            extractBtn.textContent = '🎯 UID Extract Karein';
            extractBtn.style.opacity = '1';
            loading.classList.add('hidden');
        }

        function copyToClipboard() {
            const postId = document.getElementById('postId').textContent;
            const copyBtn = document.querySelector('.copy-btn');
            
            navigator.clipboard.writeText(postId).then(() => {
                // Show success feedback
                const originalText = copyBtn.textContent;
                copyBtn.textContent = '✅ Copied!';
                copyBtn.style.background = '#218838';
                
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                    copyBtn.style.background = '';
                }, 2000);
            }).catch(err => {
                console.error('Copy failed:', err);
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = postId;
                document.body.appendChild(textArea);
                textArea.select();
                try {
                    document.execCommand('copy');
                    copyBtn.textContent = '✅ Copied!';
                    setTimeout(() => {
                        copyBtn.textContent = '📋 Copy';
                    }, 2000);
                } catch (fallbackErr) {
                    alert('Copy karne mein error aaya. Manual copy karein: ' + postId);
                }
                document.body.removeChild(textArea);
            });
        }

        // Enter key support
        document.getElementById('postUrl').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !currentState.isProcessing) {
                extractUID();
            }
        });

        // Input validation on paste and input
        document.getElementById('postUrl').addEventListener('input', function(e) {
            const url = e.target.value;
            if (url && !isValidFacebookUrl(url)) {
                e.target.style.borderColor = '#dc3545';
            } else {
                e.target.style.borderColor = '#e1e8ed';
            }
        });

        // Clear validation on focus
        document.getElementById('postUrl').addEventListener('focus', function(e) {
            e.target.style.borderColor = '#1877f2';
        });

        // Prevent form submission
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelector('form')?.addEventListener('submit', function(e) {
                e.preventDefault();
            });
        });
    </script>
</body>
</html>
'''

def get_enhanced_headers():
    """Return realistic browser headers to avoid blocking"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    return {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/avif,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0',
        'DNT': '1'
    }

def extract_facebook_post_id(post_url):
    """
    Enhanced Facebook Post ID extraction with multiple fallback methods
    """
    try:
        print(f"Attempting to extract from: {post_url}")
        
        # Clean and validate URL
        if not post_url.startswith(('http://', 'https://')):
            post_url = 'https://' + post_url
        
        headers = get_enhanced_headers()
        
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(2, 4))
        
        response = requests.get(
            post_url, 
            headers=headers, 
            timeout=15,
            allow_redirects=True
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code != 200:
            return None, f"Facebook returned status code: {response.status_code}"
        
        html_content = response.text
        post_id = None
        
        # Method 1: Direct URL pattern extraction
        url_patterns = [
            r'facebook\.com/(\d+)(?:\?|/|$)',
            r'story_fbid=(\d+)',
            r'posts/(\d+)',
            r'permalink/(\d+)',
            r'/(\d+)/?(?:\?|$)'
        ]
        
        for pattern in url_patterns:
            match = re.search(pattern, post_url)
            if match:
                post_id = match.group(1)
                print(f"Found via URL pattern {pattern}: {post_id}")
                return post_id, "Success"
        
        # Method 2: Share FBID pattern in HTML
        share_fbid_match = re.search(r'"share_fbid":"(\d+)"', html_content)
        if share_fbid_match:
            post_id = share_fbid_match.group(1)
            print(f"Found via share_fbid: {post_id}")
            return post_id, "Success"
        
        # Method 3: Look for post ID in meta tags
        meta_patterns = [
            r'<meta[^>]*property="og:url"[^>]*content="[^"]*/(\d+)/?',
            r'data-post-id="(\d+)"',
            r'fb://photo/(\d+)',
            r'"post_id":"(\d+)"'
        ]
        
        for pattern in meta_patterns:
            match = re.search(pattern, html_content, re.IGNORECASE)
            if match:
                post_id = match.group(1)
                print(f"Found via meta pattern {pattern}: {post_id}")
                return post_id, "Success"
        
        # Method 4: Look for data in debug info (base64 encoded)
        debug_match = re.search(r'"debug_info":"([^"]+)"', html_content)
        if debug_match:
            try:
                import base64
                debug_info_encoded = debug_match.group(1)
                debug_info_decoded = base64.b64decode(debug_info_encoded).decode('utf-8', errors='ignore')
                id_match = re.search(r'\d{10,}', debug_info_decoded)
                if id_match:
                    post_id = id_match.group()
                    print(f"Found via debug info: {post_id}")
                    return post_id, "Success"
            except Exception as e:
                print(f"Debug info decoding failed: {e}")
        
        # Method 5: Look for reaction count data
        reaction_match = re.search(r'reaction_count.*?(\d{15,})', html_content)
        if reaction_match:
            post_id = reaction_match.group(1)
            print(f"Found via reaction count: {post_id}")
            return post_id, "Success"
            
        return None, "Could not find Post ID in the page content"
        
    except requests.exceptions.Timeout:
        return None, "Request timeout: Facebook took too long to respond"
    except requests.exceptions.ConnectionError:
        return None, "Connection error: Cannot connect to Facebook"
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

@app.route('/')
def home():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/extract-uid', methods=['POST'])
def extract_uid():
    """API endpoint to extract Facebook Post ID"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON data'
            }), 400
        
        post_url = data.get('post_url', '').strip()
        
        if not post_url:
            return jsonify({
                'success': False,
                'error': 'Post URL is required'
            }), 400
        
        # Validate Facebook URL
        if not re.match(r'^(https?://)?(www\.)?(facebook|fb)\.com/.+', post_url, re.IGNORECASE):
            return jsonify({
                'success': False,
                'error': 'Invalid Facebook URL. Please use facebook.com or fb.com links only.'
            }), 400
        
        # Extract post ID
        post_id, message = extract_facebook_post_id(post_url)
        
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
                'error': f'{message}. Please ensure: 1) Post is public, 2) URL is correct, 3) Try again later.'
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
        'timestamp': '2024-11-02T09:01:51Z',
        'version': '2.0'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    print(f"🚀 Starting Facebook UID Extractor on port {port}")
    print(f"📧 Debug mode: {debug_mode}")
    print(f"🌐 Access at: http://localhost:{port}")
    
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=debug_mode,
        threaded=True
    )
