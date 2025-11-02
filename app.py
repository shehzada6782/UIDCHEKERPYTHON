from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# HTML Template for the Web Interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Post UID Extractor</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .card { background: #f5f5f5; padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        input[type="url"] { width: 100%; padding: 10px; margin: 10px 0; }
        button { background: #1877f2; color: white; border: none; padding: 12px 25px; border-radius: 5px; cursor: pointer; }
        .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Facebook Post UID Extractor</h1>
            <p>Facebook post ka link daaliye aur UID prapt karein</p>
        </header>

        <div class="card">
            <div class="input-group">
                <label for="postUrl">Facebook Post URL:</label>
                <input type="url" id="postUrl" 
                       placeholder="https://www.facebook.com/share/p/..." 
                       required>
                <button id="extractBtn" onclick="extractUID()">UID Extract Karein</button>
            </div>

            <div id="result" class="result hidden"></div>
            <div id="loading" class="loading hidden">Processing...</div>
        </div>
    </div>

    <script>
        async function extractUID() {
            const postUrl = document.getElementById('postUrl').value.trim();
            const extractBtn = document.getElementById('extractBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');

            // Reset & show loading
            result.classList.add('hidden');
            loading.classList.remove('hidden');
            extractBtn.disabled = true;

            if (!postUrl) {
                showResult('Error: Please enter a Facebook URL', 'error');
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
                    showResult(`Success! Post UID: <strong>${data.post_id}</strong>`, 'success');
                } else {
                    showResult(`Error: ${data.error}`, 'error');
                }
            } catch (error) {
                showResult('Network error: Server se connect nahi ho paya', 'error');
            } finally {
                loading.classList.add('hidden');
                extractBtn.disabled = false;
            }
        }

        function showResult(message, type) {
            const result = document.getElementById('result');
            result.innerHTML = message;
            result.className = `result ${type}`;
            result.classList.remove('hidden');
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    """Serve the main page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/extract-uid', methods=['POST'])
def extract_uid_api():
    """API endpoint to extract UID from Facebook post URL"""
    try:
        data = request.get_json()
        post_url = data.get('post_url', '').strip()

        if not post_url:
            return jsonify({'success': False, 'error': 'Post URL is required'}), 400

        # Use facebook-scraper to get post info
        try:
            from facebook_scraper import get_posts
        except ImportError:
            return jsonify({
                'success': False, 
                'error': 'facebook-scraper library not installed. Add it to requirements.txt'
            }), 500

        # Extract post ID from the URL using facebook-scraper
        post_id = extract_post_id(post_url)

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
                'error': 'Could not extract Post ID. The post might not be public, the URL could be invalid, or Facebook is blocking the request.'
            }), 404

    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

def extract_post_id(post_url):
    """
    Extract post ID from Facebook URL using facebook-scraper
    """
    try:
        # Use facebook-scraper to get post information
        # The get_posts function can extract posts from URLs
        posts = list(get_posts(post_urls=[post_url], timeout=30))
        
        if posts and len(posts) > 0:
            post = posts[0]
            return post.get('post_id')
        
        return None
        
    except Exception as e:
        print(f"Error extracting post ID: {e}")
        return None

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
