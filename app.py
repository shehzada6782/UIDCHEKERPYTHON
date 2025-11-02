from flask import Flask, request, jsonify, render_template_string
import requests
import re
import os

app = Flask(__name__)

# HTML Template as string (single file solution)
HTML_TEMPLATE = """
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
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            color: white;
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
        }

        .input-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }

        input[type="url"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e8ed;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
            margin-bottom: 15px;
        }

        input[type="url"]:focus {
            outline: none;
            border-color: #1877f2;
            box-shadow: 0 0 0 3px rgba(24, 119, 242, 0.1);
        }

        button {
            background: linear-gradient(135deg, #1877f2, #0d66d0);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(24, 119, 242, 0.4);
        }

        .result {
            margin-top: 20px;
        }

        .hidden {
            display: none !important;
        }

        .success-result, .error-result {
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }

        .success-result {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }

        .error-result {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }

        .result-item {
            margin: 15px 0;
        }

        .uid-display {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 10px 0;
        }

        .uid-display span {
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 18px;
            font-weight: bold;
            flex: 1;
            border: 2px dashed #28a745;
        }

        .copy-btn {
            background: #28a745;
            width: auto;
            padding: 10px 15px;
            font-size: 14px;
        }

        .loading {
            text-align: center;
            padding: 30px;
            color: #666;
        }

        .instructions {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        }

        .instructions h3 {
            color: #333;
            margin-bottom: 15px;
        }

        .instructions ol {
            margin-left: 20px;
            margin-bottom: 20px;
        }

        .instructions li {
            margin-bottom: 8px;
        }

        .note {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            padding: 15px;
            border-radius: 8px;
            color: #856404;
        }

        footer {
            text-align: center;
            margin-top: auto;
            padding-top: 30px;
            color: white;
            opacity: 0.8;
        }

        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            header h1 {
                font-size: 2rem;
            }
            .card {
                padding: 20px;
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
                           required>
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
                    <p>🔄 UID extract kiya ja raha hai...</p>
                </div>
            </div>

            <div class="instructions">
                <h3>ℹ️ Kaise Use Karein:</h3>
                <ol>
                    <li>Facebook post par jayein</li>
                    <li>Post ka complete URL copy karein</li>
                    <li>Yahan paste karein aur "UID Extract Karein" button dabayein</li>
                    <li>Apna Post UID prapt karein!</li>
                </ol>

                <div class="note">
                    <strong>Note:</strong> Ye tool sirf public posts ke liye kaam karta hai. Private posts ka UID extract nahi kar sakta.
                </div>
            </div>
        </main>

        <footer>
            <p>&copy; 2024 Facebook UID Extractor | Built with Python & Flask</p>
        </footer>
    </div>

    <script>
        async function extractUID() {
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
            
            // Disable button during processing
            extractBtn.disabled = true;
            extractBtn.textContent = '🔄 Processing...';

            if (!postUrl) {
                showError('Kripya Facebook post ka URL daalein');
                return;
            }

            if (!isValidFacebookUrl(postUrl)) {
                showError('Kripya valid Facebook URL daalein (facebook.com ya fb.com)');
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
                    showError(data.error || 'UID extract nahi ho paya');
                }
            } catch (error) {
                console.error('Error:', error);
                showError('Network error: Server se connect nahi ho paya');
            } finally {
                loading.classList.add('hidden');
                extractBtn.disabled = false;
                extractBtn.textContent = '🎯 UID Extract Karein';
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

            // Scroll to result
            result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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

            // Scroll to result
            result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        function copyToClipboard() {
            const postId = document.getElementById('postId').textContent;
            
            navigator.clipboard.writeText(postId).then(() => {
                // Show temporary success message on button
                const copyBtn = document.querySelector('.copy-btn');
                const originalText = copyBtn.textContent;
                
                copyBtn.textContent = '✅ Copied!';
                copyBtn.style.background = '#28a745';
                
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                    copyBtn.style.background = '';
                }, 2000);
            }).catch(err => {
                console.error('Copy failed:', err);
                alert('Copy karne mein error aaya. Manual copy karein.');
            });
        }

        // Enter key support
        document.getElementById('postUrl').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                extractUID();
            }
        });
    </script>
</body>
</html>
"""

def extract_facebook_post_id(post_url):
    """
    Extract Facebook Post ID from given URL using multiple methods
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(post_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        html_content = response.text
        post_id = None
        
        # Method 1: Look for share_fbid pattern
        share_fbid_match = re.search(r'"share_fbid":"(\d+)"', html_content)
        if share_fbid_match:
            post_id = share_fbid_match.group(1)
            return post_id
        
        # Method 2: Look for post ID in meta tags
        meta_og_url_match = re.search(r'<meta property="og:url" content="[^"]*/(\d+)/?', html_content)
        if meta_og_url_match:
            post_id = meta_og_url_match.group(1)
            return post_id
        
        # Method 3: Look for data in debug info
        debug_match = re.search(r'"debug_info":\{[^}]*"id":"([^"]+)"', html_content)
        if debug_match:
            try:
                import base64
                debug_info_encoded = debug_match.group(1)
                debug_info_decoded = base64.b64decode(debug_info_encoded).decode('utf-8')
                id_match = re.search(r'\d+', debug_info_decoded)
                if id_match:
                    post_id = id_match.group()
                    return post_id
            except:
                pass
        
        # Method 4: Try to extract from URL parameters
        if 'story_fbid=' in post_url:
            story_match = re.search(r'story_fbid=(\d+)', post_url)
            if story_match:
                return story_match.group(1)
        
        # Method 5: Look for post ID in the URL path
        url_path_match = re.search(r'/(\d+)(?:/?\?|/?$)', post_url)
        if url_path_match:
            return url_path_match.group(1)
        
        return None
        
    except requests.RequestException as e:
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        raise Exception(f"Extraction error: {str(e)}")

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/extract-uid', methods=['POST'])
def extract_uid():
    try:
        data = request.get_json()
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
                'error': 'Invalid Facebook URL'
            }), 400
        
        # Extract post ID
        post_id = extract_facebook_post_id(post_url)
        
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
                'error': 'Could not extract Post ID. Please make sure the URL is correct and the post is public.'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'OK', 
        'service': 'Facebook UID Extractor',
        'timestamp': '2024-11-02T09:01:51Z'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
