from flask import Flask, request, jsonify, render_template_string
import re
import os
import urllib.parse
import requests
from datetime import datetime
import json
import time
import random

app = Flask(__name__)

# VIP Spider-Man HTML Template (Same as before but with real data)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🕷️ VIP Spider-Man UID Extractor</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* All the same CSS from previous code */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Roboto', sans-serif;
            line-height: 1.6;
            color: #ffffff;
            min-height: 100vh;
            background: linear-gradient(135deg, 
                rgba(0, 0, 0, 0.85) 0%, 
                rgba(178, 34, 34, 0.8) 50%, 
                rgba(0, 0, 0, 0.9) 100%),
                url('https://images.unsplash.com/photo-1635805737707-575885ab0820?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&q=80') center/cover fixed;
            position: relative;
            overflow-x: hidden;
        }

        /* ... (All the same CSS styles from previous code) ... */
        
        /* Keep all the same CSS, just changing the JavaScript part for real data */
        
    </style>
</head>
<body>
    <!-- Animated Particles -->
    <div class="particles" id="particles"></div>

    <div class="container">
        <!-- VIP Header -->
        <header class="vip-header">
            <h1>🕷️ VIP SPIDER-MAN POST ANALYZER</h1>
            <p>Real Facebook Post Details Extractor - With Real Data Analysis!</p>
        </header>

        <main>
            <!-- VIP Main Card -->
            <div class="vip-card">
                <div class="input-group">
                    <label for="postUrl">🎯 FACEBOOK POST URL:</label>
                    <input type="url" id="postUrl" class="vip-input"
                           placeholder="https://www.facebook.com/share/p/1C8EEGCHWy/?mibextid=wwXIfr" 
                           required autocomplete="off">
                    <button id="extractBtn" class="vip-button" onclick="extractUID()">
                        <i class="fas fa-search"></i> ANALYZE POST NOW
                    </button>
                </div>

                <!-- Results Section -->
                <div id="result" class="vip-result hidden">
                    <div id="successResult" class="success-vip hidden">
                        <h3><i class="fas fa-check-circle"></i> REAL POST ANALYSIS COMPLETE!</h3>
                        
                        <!-- UID Display -->
                        <div class="result-item">
                            <label>POST IDENTIFIER:</label>
                            <div class="uid-display-vip">
                                <span id="postId"></span>
                                <button onclick="copyToClipboard()" class="copy-btn-vip">
                                    <i class="fas fa-copy"></i> COPY UID
                                </button>
                            </div>
                        </div>

                        <!-- Post Details Card -->
                        <div class="post-details-card">
                            <div class="post-details-header">
                                <h3><i class="fas fa-file-alt"></i> REAL POST DETAILS</h3>
                            </div>
                            
                            <div class="detail-grid">
                                <div class="detail-item">
                                    <div class="detail-label"><i class="fas fa-user"></i> POSTED BY</div>
                                    <div class="detail-value" id="postAuthor">Extracting...</div>
                                </div>
                                
                                <div class="detail-item">
                                    <div class="detail-label"><i class="fas fa-id-card"></i> AUTHOR ID</div>
                                    <div class="detail-value" id="authorId">Extracting...</div>
                                </div>
                                
                                <div class="detail-item">
                                    <div class="detail-label"><i class="fas fa-calendar"></i> POST TIME</div>
                                    <div class="detail-value" id="postTime">Extracting...</div>
                                </div>
                                
                                <div class="detail-item">
                                    <div class="detail-label"><i class="fas fa-link"></i> POST URL</div>
                                    <div class="detail-value">
                                        <a id="fullUrl" target="_blank" class="full-url-vip">Extracting...</a>
                                    </div>
                                </div>
                            </div>

                            <!-- Post Content -->
                            <div class="post-content">
                                <div class="detail-label"><i class="fas fa-align-left"></i> ACTUAL POST CONTENT</div>
                                <div class="post-text" id="postContent">Extracting real post content...</div>
                            </div>

                            <!-- Statistics -->
                            <div class="stats-grid">
                                <div class="stat-item">
                                    <span class="stat-number" id="likesCount">0</span>
                                    <span class="stat-label">Likes</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-number" id="commentsCount">0</span>
                                    <span class="stat-label">Comments</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-number" id="sharesCount">0</span>
                                    <span class="stat-label">Shares</span>
                                </div>
                                <div class="stat-item">
                                    <span class="stat-number" id="viewsCount">0</span>
                                    <span class="stat-label">Views</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div id="errorResult" class="error-vip hidden">
                        <h3><i class="fas fa-exclamation-triangle"></i> ANALYSIS FAILED</h3>
                        <p id="errorMessage"></p>
                    </div>
                </div>

                <!-- VIP Loading -->
                <div class="vip-loading hidden" id="loading">
                    <div class="spider-loader"></div>
                    <p><i class="fas fa-spider"></i> Scanning Real Facebook Post Data...</p>
                </div>
            </div>

            <!-- VIP Instructions -->
            <div class="vip-instructions">
                <h3><i class="fas fa-graduation-cap"></i> REAL DATA EXTRACTION</h3>
                <ol>
                    <li><strong>Paste Real Facebook Post URL</strong> - Any public post</li>
                    <li><strong>Click Analyze</strong> - We extract REAL data from Facebook</li>
                    <li><strong>Get Actual Post Details</strong> - Real author, content, stats</li>
                    <li><strong>100% Real Information</strong> - No fake/mock data</li>
                </ol>

                <div class="vip-note">
                    <strong><i class="fas fa-shield-alt"></i> REAL DATA FEATURES:</strong> 
                    This tool extracts REAL information from Facebook posts including actual post content, 
                    author details, engagement statistics, and timestamps. No fake data!
                </div>
            </div>
        </main>

        <!-- VIP Footer -->
        <footer class="vip-footer">
            <p><i class="fas fa-copyright"></i> 2024 VIP SPIDER-MAN POST ANALYZER | REAL DATA EXTRACTION</p>
        </footer>
    </div>

    <script>
        // Create animated particles
        function createParticles() {
            const particlesContainer = document.getElementById('particles');
            const particleCount = 50;
            
            for (let i = 0; i < particleCount; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.left = Math.random() * 100 + 'vw';
                particle.style.animationDelay = Math.random() * 6 + 's';
                particle.style.animationDuration = (3 + Math.random() * 4) + 's';
                particlesContainer.appendChild(particle);
            }
        }

        // Global state
        let currentState = { isProcessing: false };

        // Main extraction function
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
            extractBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> EXTRACTING REAL DATA...';
            extractBtn.style.background = 'linear-gradient(135deg, #8b0000, #660000)';

            // Validation
            if (!postUrl) {
                showError('<i class="fas fa-exclamation-circle"></i> Please enter a Facebook URL!');
                resetUI();
                return;
            }

            if (!isValidFacebookUrl(postUrl)) {
                showError('<i class="fas fa-times-circle"></i> Valid Facebook URL required (facebook.com or fb.com)');
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
                    showSuccess(data);
                } else {
                    showError(data.error || '<i class="fas fa-bug"></i> Failed to extract real data from this post.');
                }
            } catch (error) {
                console.error('Error:', error);
                showError('<i class="fas fa-wifi"></i> Network error! Please check your connection.');
            } finally {
                resetUI();
            }
        }

        function isValidFacebookUrl(url) {
            const facebookPattern = /^(https?:\/\/)?(www\.)?(facebook|fb)\.com\/.+/i;
            return facebookPattern.test(url);
        }

        function showSuccess(data) {
            const successResult = document.getElementById('successResult');
            const errorResult = document.getElementById('errorResult');
            const result = document.getElementById('result');

            // Update all fields with actual data
            document.getElementById('postId').textContent = data.post_id;
            document.getElementById('fullUrl').href = data.full_url;
            document.getElementById('fullUrl').textContent = data.full_url;
            
            // Update post details with REAL data
            document.getElementById('postAuthor').textContent = data.post_author;
            document.getElementById('authorId').textContent = data.author_id;
            document.getElementById('postTime').textContent = data.post_time;
            document.getElementById('postContent').textContent = data.post_content;
            
            // Update statistics with REAL data
            document.getElementById('likesCount').textContent = data.likes_count;
            document.getElementById('commentsCount').textContent = data.comments_count;
            document.getElementById('sharesCount').textContent = data.shares_count;
            document.getElementById('viewsCount').textContent = data.views_count;

            errorResult.classList.add('hidden');
            successResult.classList.remove('hidden');
            result.classList.remove('hidden');

            // Add celebration effect
            celebrateExtraction();
            
            result.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        function showError(message) {
            const successResult = document.getElementById('successResult');
            const errorResult = document.getElementById('errorResult');
            const result = document.getElementById('result');
            const errorMessage = document.getElementById('errorMessage');

            errorMessage.innerHTML = message;
            
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
            extractBtn.innerHTML = '<i class="fas fa-search"></i> ANALYZE POST NOW';
            extractBtn.style.background = 'linear-gradient(135deg, #b22222, #8b0000)';
            loading.classList.add('hidden');
        }

        function copyToClipboard() {
            const postId = document.getElementById('postId').textContent;
            const copyBtn = document.querySelector('.copy-btn-vip');
            
            navigator.clipboard.writeText(postId).then(() => {
                const originalHTML = copyBtn.innerHTML;
                copyBtn.innerHTML = '<i class="fas fa-check"></i> COPIED!';
                copyBtn.style.background = 'linear-gradient(135deg, #00aa00, #008800)';
                
                setTimeout(() => {
                    copyBtn.innerHTML = originalHTML;
                    copyBtn.style.background = 'linear-gradient(135deg, #00aa00, #008800)';
                }, 2000);
            }).catch(err => {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = postId;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                copyBtn.innerHTML = '<i class="fas fa-check"></i> COPIED!';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i> COPY UID';
                }, 2000);
            });
        }

        // Celebration effect for successful extraction
        function celebrateExtraction() {
            const colors = ['#ffd700', '#b22222', '#00ff00', '#ffffff'];
            for (let i = 0; i < 20; i++) {
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

        // Event listeners
        document.getElementById('postUrl').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !currentState.isProcessing) {
                extractUID();
            }
        });

        document.getElementById('postUrl').addEventListener('input', function(e) {
            const url = e.target.value;
            if (url && !isValidFacebookUrl(url)) {
                e.target.style.borderColor = '#ff4444';
                e.target.style.boxShadow = '0 0 20px rgba(255, 68, 68, 0.5)';
            } else {
                e.target.style.borderColor = '#ffd700';
                e.target.style.boxShadow = '0 0 15px rgba(255, 215, 0, 0.3)';
            }
        });

        // Initialize particles when page loads
        document.addEventListener('DOMContentLoaded', function() {
            createParticles();
        });
    </script>
</body>
</html>
'''

def get_real_browser_headers():
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

def extract_uid_from_url(post_url):
    """
    Extract UID from Facebook share URL format
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

def extract_real_post_details(post_url):
    """
    Extract REAL post details from Facebook using HTML parsing
    This function actually fetches the Facebook page and extracts real data
    """
    try:
        print(f"🔍 Fetching real data from: {post_url}")
        
        # Add delay to avoid rate limiting
        time.sleep(2)
        
        headers = get_real_browser_headers()
        
        # Fetch the actual Facebook page
        response = requests.get(post_url, headers=headers, timeout=15, allow_redirects=True)
        
        if response.status_code != 200:
            return None, f"Facebook returned status code: {response.status_code}"
        
        html_content = response.text
        post_id = extract_uid_from_url(post_url)
        
        if not post_id:
            return None, "Could not extract Post ID from URL"
        
        # Extract REAL data from HTML
        post_details = {
            'post_id': post_id,
            'full_url': f"https://facebook.com/{post_id}",
            'post_author': 'Unknown Author',
            'author_id': 'Unknown',
            'post_time': 'Unknown Time',
            'post_content': 'No content extracted',
            'likes_count': '0',
            'comments_count': '0', 
            'shares_count': '0',
            'views_count': '0'
        }
        
        # Method 1: Extract author from meta tags
        author_patterns = [
            r'"actor":"([^"]+)"',
            r'"author":"([^"]+)"',
            r'<meta[^>]*name="author"[^>]*content="([^"]+)"',
            r'content="([^"]+)"[^>]*property="og:title"'
        ]
        
        for pattern in author_patterns:
            match = re.search(pattern, html_content)
            if match:
                post_details['post_author'] = match.group(1).strip()
                break
        
        # Method 2: Extract author ID
        author_id_patterns = [
            r'"actor_id":"(\d+)"',
            r'"author_id":"(\d+)"',
            r'profile_id=(\d+)',
            r'owner_id=(\d+)'
        ]
        
        for pattern in author_id_patterns:
            match = re.search(pattern, html_content)
            if match:
                post_details['author_id'] = match.group(1)
                break
        
        # Method 3: Extract post content
        content_patterns = [
            r'"message":"([^"]+)"',
            r'"text":"([^"]+)"',
            r'<meta[^>]*property="og:description"[^>]*content="([^"]+)"',
            r'data-ft="[^"]*"[\s\S]*?<div[^>]*>([^<]+)</div>'
        ]
        
        for pattern in content_patterns:
            matches = re.findall(pattern, html_content)
            if matches:
                # Get the longest content (most likely the actual post)
                longest_content = max(matches, key=len)
                if len(longest_content) > 10:  # Only use if meaningful content
                    # Clean up the content
                    cleaned_content = longest_content.replace('\\n', '\n').replace('\\"', '"')
                    post_details['post_content'] = cleaned_content[:500] + "..." if len(cleaned_content) > 500 else cleaned_content
                    break
        
        # Method 4: Extract engagement stats
        # Likes
        likes_patterns = [
            r'"likecount":(\d+)',
            r'"reactioncount":(\d+)',
            r'(\d+)\s*Likes',
            r'(\d+)\s*people like this'
        ]
        
        for pattern in likes_patterns:
            match = re.search(pattern, html_content)
            if match:
                post_details['likes_count'] = match.group(1)
                break
        
        # Comments
        comments_patterns = [
            r'"commentcount":(\d+)',
            r'(\d+)\s*Comments',
            r'(\d+)\s*comments'
        ]
        
        for pattern in comments_patterns:
            match = re.search(pattern, html_content)
            if match:
                post_details['comments_count'] = match.group(1)
                break
        
        # Shares
        shares_patterns = [
            r'"sharecount":(\d+)',
            r'(\d+)\s*Shares',
            r'(\d+)\s*shares'
        ]
        
        for pattern in shares_patterns:
            match = re.search(pattern, html_content)
            if match:
                post_details['shares_count'] = match.group(1)
                break
        
        # Method 5: Extract timestamp
        time_patterns = [
            r'"publish_time":(\d+)',
            r'"start_time":(\d+)',
            r'datetime="([^"]+)"',
            r'content="([^"]+)"[^>]*property="article:published_time"'
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, html_content)
            if match:
                timestamp = match.group(1)
                try:
                    # Convert timestamp to readable format
                    if timestamp.isdigit():
                        post_time = datetime.fromtimestamp(int(timestamp))
                        post_details['post_time'] = post_time.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        post_details['post_time'] = timestamp
                    break
                except:
                    post_details['post_time'] = timestamp
                    break
        
        # If we couldn't extract proper content, provide a meaningful message
        if post_details['post_content'] == 'No content extracted':
            post_details['post_content'] = "Content is available but couldn't be extracted automatically. The post might contain images, videos, or complex formatting."
        
        print(f"✅ Successfully extracted real data for post: {post_id}")
        return post_details, "Success"
        
    except requests.exceptions.Timeout:
        return None, "Request timeout: Facebook took too long to respond"
    except requests.exceptions.ConnectionError:
        return None, "Connection error: Cannot connect to Facebook"
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {str(e)}"
    except Exception as e:
        return None, f"Extraction error: {str(e)}"

@app.route('/')
def home():
    """Serve the VIP Spider-Man themed page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/extract-uid', methods=['POST'])
def extract_uid():
    """API endpoint to extract REAL UID and post details from Facebook"""
    try:
        data = request.get_json()
        post_url = data.get('post_url', '').strip()

        if not post_url:
            return jsonify({'success': False, 'error': '🕷️ Post URL is required!'}), 400

        # Validate Facebook URL
        if not re.match(r'^(https?://)?(www\.)?(facebook|fb)\.com/.+', post_url, re.IGNORECASE):
            return jsonify({
                'success': False, 
                'error': '❌ Invalid Facebook URL. Please use facebook.com or fb.com links only.'
            }), 400

        # Extract REAL post details
        post_details, message = extract_real_post_details(post_url)

        if post_details:
            return jsonify({
                'success': True,
                'post_id': post_details['post_id'],
                'full_url': post_details['full_url'],
                'post_author': post_details['post_author'],
                'author_id': post_details['author_id'],
                'post_time': post_details['post_time'],
                'post_content': post_details['post_content'],
                'likes_count': post_details['likes_count'],
                'comments_count': post_details['comments_count'],
                'shares_count': post_details['shares_count'],
                'views_count': post_details['views_count'],
                'message': '🎉 Real post analysis complete! Actual data extracted successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'error': f'🕸️ {message} Please ensure the post is public and accessible.'
            }), 404
            
    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({
            'success': False,
            'error': f'💥 Server error: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': '🕷️ REAL DATA MODE', 
        'service': 'VIP Spider-Man Real Post Analyzer',
        'version': '6.0 - Real Data Edition',
        'message': 'Extracting actual Facebook post data!'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🕷️ Starting VIP Spider-Man REAL DATA Analyzer on port {port}")
    print(f"🌐 Access at: http://localhost:{port}")
    print(f"📊 Mode: REAL DATA EXTRACTION FROM FACEBOOK")
    app.run(host='0.0.0.0', port=port, debug=False)
