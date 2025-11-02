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
    <title>AAHAN POST UID CHECKER</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Rajdhani', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            overflow-x: hidden;
        }

        /* Animated Background */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.2) 0%, transparent 50%);
            animation: backgroundShift 10s ease-in-out infinite;
            z-index: -1;
        }

        @keyframes backgroundShift {
            0%, 100% { transform: scale(1) rotate(0deg); }
            50% { transform: scale(1.1) rotate(180deg); }
        }

        .neon-container {
            background: rgba(15, 12, 41, 0.85);
            border-radius: 25px;
            padding: 50px 40px;
            width: 100%;
            max-width: 600px;
            text-align: center;
            position: relative;
            backdrop-filter: blur(15px);
            border: 2px solid transparent;
            background-clip: padding-box;
            box-shadow: 
                0 0 25px rgba(0, 255, 255, 0.3),
                inset 0 0 25px rgba(0, 255, 255, 0.1);
            animation: neonGlow 3s ease-in-out infinite alternate;
        }

        @keyframes neonGlow {
            from {
                box-shadow: 
                    0 0 25px rgba(0, 255, 255, 0.3),
                    inset 0 0 25px rgba(0, 255, 255, 0.1),
                    0 0 50px rgba(255, 0, 255, 0.2);
            }
            to {
                box-shadow: 
                    0 0 35px rgba(0, 255, 255, 0.5),
                    inset 0 0 35px rgba(0, 255, 255, 0.2),
                    0 0 70px rgba(255, 0, 255, 0.4);
            }
        }

        /* Header with Neon Text */
        .header {
            margin-bottom: 40px;
            position: relative;
        }

        .neon-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, #00ffff, #ff00ff, #00ff00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 
                0 0 10px rgba(0, 255, 255, 0.5),
                0 0 20px rgba(0, 255, 255, 0.3),
                0 0 30px rgba(255, 0, 255, 0.3);
            margin-bottom: 10px;
            letter-spacing: 3px;
            animation: textGlow 2s ease-in-out infinite alternate;
        }

        @keyframes textGlow {
            from {
                text-shadow: 
                    0 0 10px rgba(0, 255, 255, 0.5),
                    0 0 20px rgba(0, 255, 255, 0.3),
                    0 0 30px rgba(255, 0, 255, 0.3);
            }
            to {
                text-shadow: 
                    0 0 15px rgba(0, 255, 255, 0.8),
                    0 0 25px rgba(0, 255, 255, 0.5),
                    0 0 35px rgba(255, 0, 255, 0.5),
                    0 0 45px rgba(0, 255, 255, 0.3);
            }
        }

        .subtitle {
            color: rgba(0, 255, 255, 0.8);
            font-size: 1.3rem;
            font-weight: 500;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        /* Input Section */
        .input-section {
            margin-bottom: 35px;
            position: relative;
        }

        .input-container {
            position: relative;
            margin-bottom: 25px;
        }

        .input-icon {
            position: absolute;
            left: 25px;
            top: 50%;
            transform: translateY(-50%);
            color: #00ffff;
            font-size: 1.4rem;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
            z-index: 2;
        }

        .neon-input {
            width: 100%;
            padding: 20px 25px 20px 65px;
            background: rgba(0, 0, 0, 0.6);
            border: 2px solid rgba(0, 255, 255, 0.3);
            border-radius: 15px;
            font-size: 16px;
            color: #00ffff;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }

        .neon-input:focus {
            outline: none;
            border-color: #00ffff;
            box-shadow: 
                0 0 20px rgba(0, 255, 255, 0.5),
                inset 0 0 20px rgba(0, 255, 255, 0.1);
            background: rgba(0, 0, 0, 0.8);
            transform: translateY(-2px);
        }

        .neon-input::placeholder {
            color: rgba(0, 255, 255, 0.5);
        }

        /* Neon Button */
        .neon-btn {
            width: 100%;
            padding: 20px;
            background: linear-gradient(135deg, #00ffff, #ff00ff);
            color: #0f0c29;
            border: none;
            border-radius: 15px;
            font-size: 1.2rem;
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            letter-spacing: 2px;
            text-transform: uppercase;
            box-shadow: 
                0 0 15px rgba(0, 255, 255, 0.5),
                0 0 30px rgba(255, 0, 255, 0.3);
        }

        .neon-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transition: 0.5s;
        }

        .neon-btn:hover::before {
            left: 100%;
        }

        .neon-btn:hover {
            transform: translateY(-3px);
            box-shadow: 
                0 0 25px rgba(0, 255, 255, 0.8),
                0 0 40px rgba(255, 0, 255, 0.5);
            background: linear-gradient(135deg, #ff00ff, #00ffff);
        }

        .neon-btn:active {
            transform: translateY(-1px);
        }

        .neon-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        /* Loading Animation */
        .loading {
            text-align: center;
            padding: 40px;
            color: #00ffff;
            display: none;
        }

        .neon-spinner {
            width: 60px;
            height: 60px;
            border: 3px solid rgba(0, 255, 255, 0.3);
            border-top: 3px solid #00ffff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Results Section */
        .result-section {
            margin-top: 30px;
            animation: fadeIn 0.5s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .success-card {
            background: rgba(0, 20, 20, 0.8);
            border: 2px solid #00ff00;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 
                0 0 25px rgba(0, 255, 0, 0.4),
                inset 0 0 25px rgba(0, 255, 0, 0.1);
            animation: successGlow 2s ease-in-out infinite alternate;
        }

        @keyframes successGlow {
            from {
                box-shadow: 
                    0 0 25px rgba(0, 255, 0, 0.4),
                    inset 0 0 25px rgba(0, 255, 0, 0.1);
            }
            to {
                box-shadow: 
                    0 0 35px rgba(0, 255, 0, 0.6),
                    inset 0 0 35px rgba(0, 255, 0, 0.2);
            }
        }

        .success-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 20px;
            color: #00ff00;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
        }

        .uid-display {
            background: rgba(0, 0, 0, 0.7);
            padding: 25px;
            border-radius: 15px;
            border: 2px dashed #00ff00;
            font-family: 'Courier New', monospace;
            font-size: 1.5rem;
            font-weight: 700;
            color: #00ff00;
            word-break: break-all;
            margin: 20px 0;
            box-shadow: inset 0 0 20px rgba(0, 255, 0, 0.2);
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        }

        .copy-btn {
            background: linear-gradient(135deg, #00ff00, #00cc00);
            color: #000;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            font-family: 'Orbitron', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 0 auto;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
            letter-spacing: 1px;
        }

        .copy-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.7);
            background: linear-gradient(135deg, #00cc00, #00ff00);
        }

        .error-card {
            background: rgba(20, 0, 0, 0.8);
            border: 2px solid #ff0000;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 
                0 0 25px rgba(255, 0, 0, 0.4),
                inset 0 0 25px rgba(255, 0, 0, 0.1);
            animation: errorGlow 2s ease-in-out infinite alternate;
        }

        @keyframes errorGlow {
            from {
                box-shadow: 
                    0 0 25px rgba(255, 0, 0, 0.4),
                    inset 0 0 25px rgba(255, 0, 0, 0.1);
            }
            to {
                box-shadow: 
                    0 0 35px rgba(255, 0, 0, 0.6),
                    inset 0 0 35px rgba(255, 0, 0, 0.2);
            }
        }

        .error-header {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            margin-bottom: 15px;
            color: #ff0000;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
        }

        /* Footer */
        .footer {
            margin-top: 40px;
            color: rgba(0, 255, 255, 0.6);
            font-size: 1rem;
            letter-spacing: 1px;
        }

        /* Floating Particles */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00ffff;
            border-radius: 50%;
            animation: float 6s infinite linear;
            box-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
        }

        @keyframes float {
            0% {
                transform: translateY(100vh) translateX(0) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) translateX(100px) rotate(360deg);
                opacity: 0;
            }
        }

        @media (max-width: 768px) {
            .neon-container {
                padding: 30px 20px;
                margin: 10px;
            }

            .neon-title {
                font-size: 2.5rem;
            }

            .subtitle {
                font-size: 1.1rem;
            }

            .neon-input, .neon-btn {
                padding: 18px 18px 18px 60px;
            }

            .uid-display {
                font-size: 1.2rem;
                padding: 20px;
            }
        }

        @media (max-width: 480px) {
            .neon-title {
                font-size: 2rem;
            }

            .neon-container {
                padding: 25px 15px;
            }
        }
    </style>
</head>
<body>
    <!-- Floating Particles -->
    <div class="particles" id="particles"></div>

    <div class="neon-container">
        <!-- Header -->
        <div class="header">
            <h1 class="neon-title">AAHAN POST UID CHECKER</h1>
            <div class="subtitle">PREMIUM FACEBOOK POST ID EXTRACTOR</div>
        </div>

        <!-- Input Section -->
        <div class="input-section">
            <div class="input-container">
                <i class="fas fa-link input-icon"></i>
                <input type="url" class="neon-input" id="postUrl" 
                       placeholder="Paste Facebook Posts URL Here..." 
                       required>
            </div>

            <button class="neon-btn" onclick="extractUID()" id="extractBtn">
                <i class="fas fa-bolt"></i>
                EXTRACT UID
            </button>
        </div>

        <!-- Loading -->
        <div class="loading" id="loading">
            <div class="neon-spinner"></div>
            <p>SCANNING FACEBOOK POST...</p>
        </div>

        <!-- Results -->
        <div class="result-section">
            <div class="success-card" id="successResult">
                <div class="success-header">
                    <i class="fas fa-check-circle"></i>
                    <span>UID EXTRACTED SUCCESSFULLY!</span>
                </div>
                <div class="uid-display" id="uidDisplay"></div>
                <button class="copy-btn" onclick="copyUID()">
                    <i class="fas fa-copy"></i>
                    COPY UID
                </button>
            </div>

            <div class="error-card" id="errorResult">
                <div class="error-header">
                    <i class="fas fa-exclamation-triangle"></i>
                    <span>EXTRACTION FAILED</span>
                </div>
                <p id="errorMessage"></p>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>POWERED BY AAHAN TECHNOLOGIES | NEON EDITION</p>
        </div>
    </div>

    <script>
        // Create floating particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 30;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + 'vw';
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (4 + Math.random() * 4) + 's';
                particle.style.background = i % 3 === 0 ? '#00ffff' : i % 3 === 1 ? '#ff00ff' : '#00ff00';
                particlesContainer.appendChild(particle);
            }
        }

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
            extractBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> EXTRACTING...';

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
                    showError(data.error || 'Failed to extract UID from this URL');
                }
            } catch (error) {
                showError('Network error: Please check your internet connection');
            } finally {
                loading.style.display = 'none';
                extractBtn.disabled = false;
                extractBtn.innerHTML = '<i class="fas fa-bolt"></i> EXTRACT UID';
            }
        }

        function isValidFacebookUrl(url) {
            return url.includes('facebook.com') || url.includes('fb.com');
        }

        function showSuccess(uid) {
            document.getElementById('uidDisplay').textContent = uid;
            document.getElementById('successResult').style.display = 'block';
            document.getElementById('errorResult').style.display = 'none';
            
            // Add celebration effect
            celebrateSuccess();
            
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
                copyBtn.innerHTML = '<i class="fas fa-check"></i> COPIED!';
                copyBtn.style.background = 'linear-gradient(135deg, #00cc00, #00ff00)';
                
                setTimeout(() => {
                    copyBtn.innerHTML = originalHTML;
                    copyBtn.style.background = 'linear-gradient(135deg, #00ff00, #00cc00)';
                }, 2000);
            });
        }

        // Celebration effect for successful extraction
        function celebrateSuccess() {
            const colors = ['#00ffff', '#ff00ff', '#00ff00'];
            for (let i = 0; i < 15; i++) {
                setTimeout(() => {
                    const particle = document.createElement('div');
                    particle.className = 'particle';
                    particle.style.background = colors[Math.floor(Math.random() * colors.length)];
                    particle.style.left = Math.random() * 100 + 'vw';
                    particle.style.animation = 'float 2s ease-out forwards';
                    document.getElementById('particles').appendChild(particle);
                    
                    setTimeout(() => {
                        particle.remove();
                    }, 2000);
                }, i * 100);
            }
        }

        // Enter key support
        document.getElementById('postUrl').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                extractUID();
            }
        });

        // Input focus effects
        document.getElementById('postUrl').addEventListener('focus', function() {
            this.style.transform = 'translateY(-2px)';
        });

        document.getElementById('postUrl').addEventListener('blur', function() {
            this.style.transform = 'translateY(0)';
        });

        // Initialize particles and auto-focus when page loads
        document.addEventListener('DOMContentLoaded', function() {
            createParticles();
            document.getElementById('postUrl').focus();
        });
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
    return jsonify({'status': 'healthy', 'service': 'AAHAN POST UID CHECKER'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 AAHAN POST UID CHECKER starting on port {port}")
    print(f"🌟 Neon Edition - Premium UID Extraction")
    app.run(host='0.0.0.0', port=port, debug=False)
