from flask import Flask, request, jsonify, render_template_string
import re
import os
import urllib.parse
import requests
from datetime import datetime
import json

app = Flask(__name__)

# VIP Spider-Man HTML Template with Premium Design
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

        /* Spider Web Background Effect */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: 
                radial-gradient(circle at 20% 80%, rgba(178, 34, 34, 0.1) 25px, transparent 26px),
                radial-gradient(circle at 40% 40%, rgba(178, 34, 34, 0.1) 15px, transparent 16px),
                radial-gradient(circle at 80% 20%, rgba(178, 34, 34, 0.1) 20px, transparent 21px);
            pointer-events: none;
            z-index: -1;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 2;
        }

        /* VIP Header with Spider-Man Theme */
        .vip-header {
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: linear-gradient(135deg, 
                rgba(178, 34, 34, 0.9) 0%, 
                rgba(0, 0, 0, 0.9) 50%, 
                rgba(178, 34, 34, 0.9) 100%);
            border-radius: 20px;
            border: 3px solid #ffd700;
            box-shadow: 0 0 30px rgba(178, 34, 34, 0.6),
                        inset 0 0 20px rgba(255, 215, 0, 0.3);
            position: relative;
            overflow: hidden;
        }

        .vip-header::before {
            content: '🕷️';
            position: absolute;
            top: 10px;
            left: 20px;
            font-size: 2rem;
            animation: spiderFloat 3s ease-in-out infinite;
        }

        .vip-header::after {
            content: '🕷️';
            position: absolute;
            bottom: 10px;
            right: 20px;
            font-size: 2rem;
            animation: spiderFloat 3s ease-in-out infinite 1.5s;
        }

        @keyframes spiderFloat {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(10deg); }
        }

        .vip-header h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 3.2rem;
            margin-bottom: 15px;
            background: linear-gradient(45deg, #ffd700, #ffffff, #ffd700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 20px rgba(255, 215, 0, 0.5);
            letter-spacing: 2px;
        }

        .vip-header p {
            font-size: 1.3rem;
            opacity: 0.9;
            color: #ffd700;
            font-weight: 500;
        }

        /* VIP Card Design */
        .vip-card {
            background: linear-gradient(135deg, 
                rgba(0, 0, 0, 0.85) 0%, 
                rgba(178, 34, 34, 0.7) 100%);
            border-radius: 25px;
            padding: 40px;
            margin-bottom: 30px;
            border: 2px solid #ffd700;
            box-shadow: 0 0 40px rgba(178, 34, 34, 0.5),
                        inset 0 0 30px rgba(255, 215, 0, 0.2);
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }

        .vip-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: conic-gradient(
                transparent, 
                rgba(255, 215, 0, 0.3), 
                transparent 30%
            );
            animation: rotate 6s linear infinite;
            z-index: 1;
        }

        .vip-card > * {
            position: relative;
            z-index: 2;
        }

        @keyframes rotate {
            100% { transform: rotate(360deg); }
        }

        .input-group {
            margin-bottom: 30px;
        }

        .input-group label {
            display: block;
            margin-bottom: 15px;
            font-weight: 600;
            color: #ffd700;
            font-size: 1.3rem;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .vip-input {
            width: 100%;
            padding: 20px 25px;
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #ffd700;
            border-radius: 15px;
            font-size: 18px;
            color: #ffffff;
            transition: all 0.3s ease;
            margin-bottom: 25px;
            font-family: 'Roboto', sans-serif;
            box-shadow: 0 0 15px rgba(255, 215, 0, 0.3);
        }

        .vip-input:focus {
            outline: none;
            border-color: #b22222;
            box-shadow: 0 0 25px rgba(178, 34, 34, 0.6);
            transform: translateY(-3px);
        }

        .vip-input::placeholder {
            color: #888;
        }

        .vip-button {
            background: linear-gradient(135deg, #b22222, #8b0000);
            color: #ffd700;
            border: none;
            padding: 22px 35px;
            border-radius: 15px;
            font-size: 1.4rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            border: 2px solid #ffd700;
            box-shadow: 0 0 20px rgba(178, 34, 34, 0.5);
            position: relative;
            overflow: hidden;
        }

        .vip-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: 0.5s;
        }

        .vip-button:hover::before {
            left: 100%;
        }

        .vip-button:hover:not(:disabled) {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(178, 34, 34, 0.8);
            background: linear-gradient(135deg, #8b0000, #b22222);
        }

        .vip-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        /* VIP Result Sections */
        .vip-result {
            margin-top: 30px;
        }

        .hidden {
            display: none !important;
        }

        .success-vip, .error-vip {
            padding: 30px;
            border-radius: 20px;
            margin-top: 25px;
            animation: slideDown 0.5s ease;
            border: 2px solid;
            backdrop-filter: blur(10px);
        }

        @keyframes slideDown {
            from { 
                opacity: 0; 
                transform: translateY(-20px) scale(0.9); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0) scale(1); 
            }
        }

        .success-vip {
            background: linear-gradient(135deg, rgba(0, 100, 0, 0.8), rgba(0, 0, 0, 0.9));
            border-color: #00ff00;
            box-shadow: 0 0 30px rgba(0, 255, 0, 0.4);
            color: #00ff00;
        }

        .error-vip {
            background: linear-gradient(135deg, rgba(139, 0, 0, 0.8), rgba(0, 0, 0, 0.9));
            border-color: #ff4444;
            box-shadow: 0 0 30px rgba(255, 68, 68, 0.4);
            color: #ff4444;
        }

        /* Post Details Card */
        .post-details-card {
            background: linear-gradient(135deg, rgba(30, 30, 30, 0.9), rgba(0, 0, 0, 0.95));
            border-radius: 20px;
            padding: 30px;
            margin: 25px 0;
            border: 2px solid #ffd700;
            box-shadow: 0 0 25px rgba(255, 215, 0, 0.3);
        }

        .post-details-header {
            text-align: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #ffd700;
        }

        .post-details-header h3 {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            color: #ffd700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .detail-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 25px;
        }

        .detail-item {
            background: rgba(0, 0, 0, 0.6);
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #333;
            transition: all 0.3s ease;
        }

        .detail-item:hover {
            transform: translateY(-5px);
            border-color: #ffd700;
            box-shadow: 0 5px 15px rgba(255, 215, 0, 0.2);
        }

        .detail-label {
            font-weight: 600;
            color: #ffd700;
            margin-bottom: 8px;
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .detail-value {
            color: #ffffff;
            font-size: 1.1rem;
            word-break: break-all;
        }

        .post-content {
            background: rgba(0, 0, 0, 0.7);
            padding: 25px;
            border-radius: 15px;
            border-left: 4px solid #b22222;
            margin: 20px 0;
        }

        .post-content .detail-label {
            color: #b22222;
            font-size: 1.2rem;
        }

        .post-text {
            color: #ffffff;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-top: 10px;
            white-space: pre-wrap;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .stat-item {
            text-align: center;
            padding: 15px;
            background: rgba(178, 34, 34, 0.2);
            border-radius: 10px;
            border: 1px solid #b22222;
        }

        .stat-number {
            font-size: 1.5rem;
            font-weight: bold;
            color: #ffd700;
            display: block;
        }

        .stat-label {
            font-size: 0.9rem;
            color: #ffffff;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .result-item {
            margin: 25px 0;
        }

        .result-item label {
            display: block;
            margin-bottom: 12px;
            font-weight: 600;
            color: #ffd700;
            font-size: 1.2rem;
            font-family: 'Orbitron', sans-serif;
        }

        .uid-display-vip {
            display: flex;
            align-items: center;
            gap: 20px;
            margin: 20px 0;
            flex-wrap: wrap;
        }

        .uid-display-vip span {
            background: rgba(0, 0, 0, 0.8);
            padding: 20px 25px;
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            font-size: 22px;
            font-weight: bold;
            flex: 1;
            border: 2px dashed #00ff00;
            color: #00ff00;
            min-width: 250px;
            text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
            box-shadow: inset 0 0 15px rgba(0, 255, 0, 0.2);
        }

        .copy-btn-vip {
            background: linear-gradient(135deg, #00aa00, #008800);
            color: #ffffff;
            border: 2px solid #00ff00;
            padding: 15px 30px;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
        }

        .copy-btn-vip:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 20px rgba(0, 255, 0, 0.5);
            background: linear-gradient(135deg, #008800, #00aa00);
        }

        .full-url-vip {
            color: #ffd700;
            text-decoration: none;
            word-break: break-all;
            display: block;
            margin-top: 10px;
            font-weight: 500;
            font-size: 1.1rem;
            transition: color 0.3s ease;
        }

        .full-url-vip:hover {
            color: #ffffff;
            text-decoration: underline;
        }

        /* VIP Loading Animation */
        .vip-loading {
            text-align: center;
            padding: 50px;
            color: #ffd700;
        }

        .spider-loader {
            width: 80px;
            height: 80px;
            border: 4px solid #ffd700;
            border-top: 4px solid transparent;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 25px;
            position: relative;
        }

        .spider-loader::before {
            content: '🕷️';
            position: absolute;
            top: -10px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 1.5rem;
            animation: bounce 0.5s ease-in-out infinite alternate;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes bounce {
            from { transform: translateX(-50%) translateY(0px); }
            to { transform: translateX(-50%) translateY(-10px); }
        }

        /* VIP Instructions */
        .vip-instructions {
            background: linear-gradient(135deg, 
                rgba(0, 0, 0, 0.85) 0%, 
                rgba(178, 34, 34, 0.7) 100%);
            border-radius: 25px;
            padding: 35px;
            border: 2px solid #ffd700;
            box-shadow: 0 0 30px rgba(178, 34, 34, 0.5);
            backdrop-filter: blur(10px);
        }

        .vip-instructions h3 {
            color: #ffd700;
            margin-bottom: 25px;
            font-size: 1.8rem;
            font-family: 'Orbitron', sans-serif;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .vip-instructions ol {
            margin-left: 30px;
            margin-bottom: 30px;
            font-size: 1.1rem;
        }

        .vip-instructions li {
            margin-bottom: 15px;
            line-height: 1.7;
            color: #ffffff;
            padding-left: 10px;
        }

        .vip-instructions strong {
            color: #ffd700;
        }

        .vip-note {
            background: linear-gradient(135deg, 
                rgba(255, 215, 0, 0.1), 
                rgba(178, 34, 34, 0.1));
            border: 2px solid #ffd700;
            padding: 25px;
            border-radius: 15px;
            color: #ffd700;
            font-size: 1.1rem;
            text-align: center;
        }

        /* VIP Footer */
        .vip-footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            color: #ffd700;
            opacity: 0.9;
            font-size: 1rem;
            border-top: 1px solid rgba(255, 215, 0, 0.3);
            font-family: 'Orbitron', sans-serif;
            letter-spacing: 1px;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            body { padding: 15px; }
            
            .vip-header h1 { 
                font-size: 2.2rem; 
                letter-spacing: 1px;
            }
            
            .vip-card { 
                padding: 25px 20px; 
            }
            
            .uid-display-vip { 
                flex-direction: column; 
                align-items: stretch;
            }
            
            .copy-btn-vip { 
                width: 100%; 
            }
            
            .vip-input {
                font-size: 16px;
                padding: 18px 20px;
            }
            
            .vip-button {
                padding: 20px 25px;
                font-size: 1.2rem;
            }

            .detail-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 480px) {
            .vip-header h1 { 
                font-size: 1.8rem; 
            }
            
            .vip-card { 
                padding: 20px 15px; 
                border-radius: 20px;
            }
            
            .vip-button {
                padding: 18px 20px;
                font-size: 1.1rem;
                letter-spacing: 1px;
            }
            
            .uid-display-vip span {
                font-size: 18px;
                padding: 15px 20px;
                min-width: auto;
            }
        }

        /* Particle Effects */
        .particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
        }

        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #ffd700;
            border-radius: 50%;
            animation: float 6s infinite linear;
        }

        @keyframes float {
            0% {
                transform: translateY(100vh) translateX(0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) translateX(100px);
                opacity: 0;
            }
        }
    </style>
</head>
<body>
    <!-- Animated Particles -->
    <div class="particles" id="particles"></div>

    <div class="container">
        <!-- VIP Header -->
        <header class="vip-header">
            <h1>🕷️ VIP SPIDER-MAN POST ANALYZER</h1>
            <p>Premium Facebook Post Details Extractor - With Great Power Comes Great Analysis!</p>
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
                        <h3><i class="fas fa-check-circle"></i> POST ANALYSIS COMPLETE!</h3>
                        
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
                                <h3><i class="fas fa-file-alt"></i> POST DETAILS ANALYSIS</h3>
                            </div>
                            
                            <div class="detail-grid">
                                <div class="detail-item">
                                    <div class="detail-label"><i class="fas fa-user"></i> POSTED BY</div>
                                    <div class="detail-value" id="postAuthor">Loading...</div>
                                </div>
                                
                                <div class="detail-item">
                                    <div class="detail-label"><i class="fas fa-id-card"></i> AUTHOR ID</div>
                                    <div class="detail-value" id="authorId">Loading...</div>
                                </div>
                                
                                <div class="detail-item">
                                    <div class="detail-label"><i class="fas fa-calendar"></i> POST TIME</div>
                                    <div class="detail-value" id="postTime">Loading...</div>
                                </div>
                                
                                <div class="detail-item">
                                    <div class="detail-label"><i class="fas fa-link"></i> POST URL</div>
                                    <div class="detail-value">
                                        <a id="fullUrl" target="_blank" class="full-url-vip">Loading...</a>
                                    </div>
                                </div>
                            </div>

                            <!-- Post Content -->
                            <div class="post-content">
                                <div class="detail-label"><i class="fas fa-align-left"></i> POST CONTENT</div>
                                <div class="post-text" id="postContent">Loading post content...</div>
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
                    <p><i class="fas fa-spider"></i> Scanning Facebook Post... Spider-Man is analyzing!</p>
                </div>
            </div>

            <!-- VIP Instructions -->
            <div class="vip-instructions">
                <h3><i class="fas fa-graduation-cap"></i> HOW TO USE THIS VIP ANALYZER</h3>
                <ol>
                    <li><strong>Find the Target Post</strong> - Locate any public Facebook post</li>
                    <li><strong>Copy the Web Address</strong> - Get complete URL from address bar</li>
                    <li><strong>Paste in VIP Analyzer</strong> - Drop link in our premium input field</li>
                    <li><strong>Activate Deep Analysis</strong> - Hit the ANALYZE button with style!</li>
                    <li><strong>Get Complete Intelligence</strong> - Receive full post details and UID</li>
                </ol>

                <div class="vip-note">
                    <strong><i class="fas fa-shield-alt"></i> SPIDER-SENSE FEATURES:</strong> 
                    This premium analyzer extracts UID, author details, post content, engagement stats, 
                    and complete post intelligence from any public Facebook post!
                </div>
            </div>
        </main>

        <!-- VIP Footer -->
        <footer class="vip-footer">
            <p><i class="fas fa-copyright"></i> 2024 VIP SPIDER-MAN POST ANALYZER | WITH GREAT POWER COMES GREAT ANALYSIS!</p>
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
            extractBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> SPIDER-MAN ANALYZING...';
            extractBtn.style.background = 'linear-gradient(135deg, #8b0000, #660000)';

            // Validation
            if (!postUrl) {
                showError('<i class="fas fa-exclamation-circle"></i> Please enter a Facebook URL, hero!');
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
                    showError(data.error || '<i class="fas fa-bug"></i> Analysis failed! Is this a valid public post?');
                }
            } catch (error) {
                console.error('Error:', error);
                showError('<i class="fas fa-wifi"></i> Network issue! Check your connection, hero.');
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
            
            // Update post details
            document.getElementById('postAuthor').textContent = data.post_author || 'Unknown Author';
            document.getElementById('authorId').textContent = data.author_id || 'N/A';
            document.getElementById('postTime').textContent = data.post_time || 'Unknown Time';
            document.getElementById('postContent').textContent = data.post_content || 'No content available';
            
            // Update statistics
            document.getElementById('likesCount').textContent = data.likes_count || '0';
            document.getElementById('commentsCount').textContent = data.comments_count || '0';
            document.getElementById('sharesCount').textContent = data.shares_count || '0';
            document.getElementById('viewsCount').textContent = data.views_count || '0';

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

def get_post_details(post_url):
    """
    Simulate getting post details - In real implementation, you'd use Facebook API
    This is a mock function that returns sample data
    """
    try:
        # Extract UID first
        post_id = extract_uid_from_url(post_url)
        
        if not post_id:
            return None
        
        # Mock data - in real implementation, you'd fetch from Facebook API
        # Note: Getting real post details requires Facebook API access token
        mock_details = {
            'post_id': post_id,
            'post_author': 'Spider-Man Fan Page',
            'author_id': '100085432123456',
            'post_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'post_content': '🕷️ Just swinging through the city and found this amazing view! With great power comes great responsibility. #SpiderMan #Marvel #Superhero',
            'likes_count': '1.2K',
            'comments_count': '247',
            'shares_count': '89',
            'views_count': '15.7K',
            'post_url': post_url
        }
        
        return mock_details
        
    except Exception as e:
        print(f"Error getting post details: {e}")
        return None

@app.route('/')
def home():
    """Serve the VIP Spider-Man themed page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/extract-uid', methods=['POST'])
def extract_uid():
    """API endpoint to extract UID and post details from Facebook post URL"""
    try:
        data = request.get_json()
        post_url = data.get('post_url', '').strip()

        if not post_url:
            return jsonify({'success': False, 'error': '🕷️ Post URL is required, hero!'}), 400

        # Validate Facebook URL
        if not re.match(r'^(https?://)?(www\.)?(facebook|fb)\.com/.+', post_url, re.IGNORECASE):
            return jsonify({
                'success': False, 
                'error': '❌ Invalid Facebook URL. Please use facebook.com or fb.com links only.'
            }), 400

        # Extract post details
        post_details = get_post_details(post_url)

        if post_details:
            return jsonify({
                'success': True,
                'post_id': post_details['post_id'],
                'full_url': f"https://facebook.com/{post_details['post_id']}",
                'post_author': post_details['post_author'],
                'author_id': post_details['author_id'],
                'post_time': post_details['post_time'],
                'post_content': post_details['post_content'],
                'likes_count': post_details['likes_count'],
                'comments_count': post_details['comments_count'],
                'shares_count': post_details['shares_count'],
                'views_count': post_details['views_count'],
                'message': '🎉 Post analysis complete! Spider-Man has gathered all intelligence!'
            })
        else:
            return jsonify({
                'success': False,
                'error': '🕸️ Could not analyze post. Make sure URL format is correct and post is public.'
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
        'status': '🕷️ AMAZING', 
        'service': 'VIP Spider-Man Post Analyzer',
        'version': '5.0 - Full Details Edition',
        'message': 'With great power comes great post analysis!'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🕷️ Starting VIP Spider-Man Post Analyzer on port {port}")
    print(f"🌐 Access at: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
