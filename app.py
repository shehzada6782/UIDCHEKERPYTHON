from flask import Flask, request, jsonify, render_template_string
import re
import os
import urllib.parse

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook UID Extractor</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }

        .glass-container {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 40px;
            width: 100%;
            max-width: 500px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .logo {
            font-size: 3rem;
            color: #fff;
            margin-bottom: 10px;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        h1 {
            color: white;
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 5px;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .subtitle {
            color: rgba(255, 255, 255, 0.8);
            font-size: 1rem;
            margin-bottom: 30px;
        }

        .input-group {
            position: relative;
            margin-bottom: 25px;
        }

        .input-icon {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: #764ba2;
            font-size: 1.2rem;
        }

        input {
            width: 100%;
            padding: 18px 20px 18px 50px;
            background: rgba(255, 255, 255, 0.9);
            border: 2px solid transparent;
            border-radius: 15px;
            font-size: 16px;
            color: #333;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }

        input:focus {
            outline: none;
            border-color: #764ba2;
            background: white;
            box-shadow: 0 8px 25px rgba(118, 75, 162, 0.3);
            transform: translateY(-2px);
        }

        input::placeholder {
            color: #999;
        }

        .btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 15px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }

        .btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            background: linear-gradient(135deg, #764ba2, #667eea);
        }

        .btn:active {
            transform: translateY(-1px);
        }

        .btn:disabled {
            opacity: 0.7;
            cursor: not-allowed;
            transform: none;
        }

        .result-container {
            margin-top: 25px;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .success-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #28a745;
        }

        .success-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 15px;
            color: #28a745;
            font-weight: 600;
        }

        .uid-display {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 20px;
            border-radius: 12px;
            border: 2px dashed #28a745;
            font-family: 'Courier New', monospace;
            font-size: 1.3rem;
            font-weight: 600;
            color: #333;
            word-break: break-all;
            margin: 15px 0;
            box-shadow: inset 0 2px 5px rgba(0, 0, 0, 0.1);
        }

        .copy-btn {
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 0 auto;
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        }

        .copy-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
        }

        .error-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #dc3545;
            color: #dc3545;
            text-align: center;
        }

        .error-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .loading {
            text-align: center;
            padding: 30px;
            color: white;
            display: none;
        }

        .spinner {
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-top: 3px solid white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .examples {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .examples h3 {
            color: white;
            margin-bottom: 15px;
            font-size: 1.1rem;
        }

        .example-list {
            text-align: left;
            color: rgba(255, 255, 255, 0.9);
            font-size: 0.9rem;
            line-height: 1.6;
        }

        .example-list li {
            margin-bottom: 8px;
            padding-left: 10px;
            font-family: monospace;
            background: rgba(0, 0, 0, 0.2);
            padding: 8px;
            border-radius: 5px;
        }

        .footer {
            margin-top: 30px;
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
        }

        @media (max-width: 768px) {
            .glass-container {
                padding: 30px 20px;
                margin: 10px;
            }

            h1 {
                font-size: 1.7rem;
            }

            .logo {
                font-size: 2.5rem;
            }

            input, .btn {
                padding: 16px 16px 16px 45px;
            }

            .uid-display {
                font-size: 1.1rem;
                padding: 15px;
            }
        }
    </style>
</head>
<body>
    <div class="glass-container">
        <!-- Header -->
        <div class="logo">
            <i class="fab fa-facebook"></i>
        </div>
        <h1>Facebook UID Extractor</h1>
        <div class="subtitle">Perfect UID Extraction for Posts URLs</div>

        <!-- Input Section -->
        <div class="input-group">
            <i class="fas fa-link input-icon"></i>
            <input type="url" id="postUrl" 
                   placeholder="Paste Facebook posts URL here..." 
                   required>
        </div>

        <button class="btn" onclick="extractUID()" id="extractBtn">
            <i class="fas fa-magic"></i>
            Extract UID
        </button>

        <!-- Loading -->
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Extracting UID...</p>
        </div>

        <!-- Results -->
        <div class="result-container">
            <div class="success-card" id="successResult">
                <div class="success-header">
                    <i class="fas fa-check-circle"></i>
                    <span>UID Extracted Successfully!</span>
                </div>
                <div class="uid-display" id="uidDisplay"></div>
                <button class="copy-btn" onclick="copyUID()">
                    <i class="fas fa-copy"></i>
                    Copy UID
                </button>
            </div>

            <div class="error-card" id="errorResult">
                <div class="error-header">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>Error</span>
                </div>
                <p id="errorMessage"></p>
            </div>
        </div>

        <!-- Examples -->
        <div class="examples">
            <h3><i class="fas fa-lightbulb"></i> Supported URL Formats</h3>
            <ul class="example-list">
                <li>https://www.facebook.com/61583283505209/posts/122095038687109450/</li>
                <li>https://facebook.com/username/posts/123456789012345/</li>
                <li>https://fb.com/pageid/posts/123456789012345/</li>
            </ul>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>Perfect UID Extraction for Posts URLs</p>
        </div>
    </div>

    <script>
        // Initially hide results
        document.getElementById('successResult').style.display = 'none';
        document.getElementById('errorResult').style.display = 'none';
        document.getElementById('loading').style.display = 'none';

        async function extractUID() {
            const postUrl = document.getElementById('postUrl').value.trim();
            const extractBtn = document.getElementById('extractBtn');
            const loading = document.getElementById('loading');
            const successResult = document.getElementById('successResult');
            const errorResult = document.getElementById('errorResult');

            // Hide previous results
            successResult.style.display = 'none';
            errorResult.style.display = 'none';
            loading.style.display = 'block';
            extractBtn.disabled = true;
            extractBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Extracting...';

            if (!postUrl) {
                showError('Please enter a Facebook URL');
                return;
            }

            if (!isValidFacebookUrl(postUrl)) {
                showError('Please enter a valid Facebook URL');
                return;
            }

            try {
                const response = await fetch('/extract-uid', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: postUrl })
                });

                const data = await response.json();

                if (data.success) {
                    showSuccess(data.uid);
                } else {
                    showError(data.error || 'Failed to extract UID');
                }
            } catch (error) {
                showError('Network error: Please check your connection');
            } finally {
                loading.style.display = 'none';
                extractBtn.disabled = false;
                extractBtn.innerHTML = '<i class="fas fa-magic"></i> Extract UID';
            }
        }

        function isValidFacebookUrl(url) {
            return url.includes('facebook.com') || url.includes('fb.com');
        }

        function showSuccess(uid) {
            document.getElementById('uidDisplay').textContent = uid;
            document.getElementById('successResult').style.display = 'block';
            document.getElementById('errorResult').style.display = 'none';
            
            // Smooth scroll to result
            document.getElementById('successResult').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }

        function showError(message) {
            document.getElementById('errorMessage').textContent = message;
            document.getElementById('successResult').style.display = 'none';
            document.getElementById('errorResult').style.display = 'block';
            
            // Smooth scroll to error
            document.getElementById('errorResult').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        }

        function copyUID() {
            const uid = document.getElementById('uidDisplay').textContent;
            navigator.clipboard.writeText(uid).then(() => {
                // Show temporary success
                const copyBtn = document.querySelector('.copy-btn');
                const originalHTML = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                copyBtn.style.background = 'linear-gradient(135deg, #20c997, #28a745)';
                
                setTimeout(() => {
                    copyBtn.innerHTML = originalHTML;
                    copyBtn.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
                }, 2000);
            });
        }

        // Enter key support
        document.getElementById('postUrl').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                extractUID();
            }
        });

        // Input focus effect
        document.getElementById('postUrl').addEventListener('focus', function() {
            this.style.transform = 'translateY(-2px)';
        });

        document.getElementById('postUrl').addEventListener('blur', function() {
            this.style.transform = 'translateY(0)';
        });

        // Auto-focus on input
        document.getElementById('postUrl').focus();
    </script>
</body>
</html>
'''

def extract_posts_uid(url):
    """
    Perfect UID extraction for Facebook posts URLs
    Format: https://www.facebook.com/61583283505209/posts/122095038687109450/?mibextid=...
    """
    try:
        # Clean the URL
        url = url.strip()
        
        # Method 1: Direct posts pattern extraction
        posts_patterns = [
            r'facebook\.com/\d+/posts/(\d+)',
            r'fb\.com/\d+/posts/(\d+)',
            r'/posts/(\d+)',
            r'facebook\.com/[^/]+/posts/(\d+)'
        ]
        
        for pattern in posts_patterns:
            match = re.search(pattern, url)
            if match:
                uid = match.group(1)
                # Validate it's a proper Facebook ID (numeric and reasonably long)
                if uid.isdigit() and len(uid) >= 15:
                    return uid
        
        # Method 2: URL path parsing
        parsed_url = urllib.parse.urlparse(url)
        path_parts = parsed_url.path.split('/')
        
        # Look for pattern: /number/posts/number/
        for i, part in enumerate(path_parts):
            if part == 'posts' and i + 1 < len(path_parts):
                uid = path_parts[i + 1]
                if uid.isdigit() and len(uid) >= 15:
                    return uid
        
        # Method 3: Last numeric part in path (fallback)
        for part in reversed(path_parts):
            if part.isdigit() and len(part) >= 15:
                return part
        
        return None
        
    except Exception as e:
        print(f"Error extracting UID: {e}")
        return None

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/extract-uid', methods=['POST'])
def extract_uid():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()

        if not url:
            return jsonify({'success': False, 'error': 'URL is required'})

        # Extract UID using specialized posts function
        uid = extract_posts_uid(url)

        if uid:
            return jsonify({
                'success': True,
                'uid': uid,
                'message': 'UID extracted successfully from posts URL'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not extract UID. Please make sure this is a valid Facebook posts URL in the format: https://www.facebook.com/PAGE_ID/posts/POST_ID/'
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'Facebook UID Extractor'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Facebook UID Extractor starting on port {port}")
    print(f"📱 Specialized for posts URLs: /PAGE_ID/posts/POST_ID/")
    app.run(host='0.0.0.0', port=port, debug=False)
