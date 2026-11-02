#!/usr/bin/env python3
"""
VKU MLOps AI Vision Cockpit - Interactive Web Dashboard
Zero-dependency Single-Page Web Application & Backend-For-Frontend (BFF)
Built for Graduation Thesis Defense & Live Demonstration
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from http.server import HTTPServer, BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor

PORT = 8888
FASTAPI_URL = "http://localhost:8080"
PROMETHEUS_URL = "http://localhost:9090"
GRAFANA_URL = "http://localhost:3000"
MLFLOW_URL = "http://localhost:5000"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def check_endpoint_health(url, timeout=1.0):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MLOps-Cockpit/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status in (200, 302)
    except Exception:
        return False

def get_system_stats():
    mem_total_mb = 0
    mem_avail_mb = 0
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    mem_total_mb = int(line.split()[1]) // 1024
                elif line.startswith("MemAvailable:"):
                    mem_avail_mb = int(line.split()[1]) // 1024
        mem_used_mb = mem_total_mb - mem_avail_mb
    except Exception:
        mem_used_mb, mem_total_mb = 0, 0

    return {
        "mem_used_mb": mem_used_mb,
        "mem_total_mb": mem_total_mb,
        "mem_percent": round((mem_used_mb / mem_total_mb * 100), 1) if mem_total_mb else 0,
        "kernel": os.uname().release if hasattr(os, "uname") else "Linux",
        "hostname": os.uname().nodename if hasattr(os, "uname") else "localhost"
    }

def run_quick_benchmark(total_requests=50, concurrency=10):
    start_time = time.time()
    latencies = []
    success_count = 0
    fail_count = 0

    def single_probe():
        t0 = time.time()
        try:
            req = urllib.request.Request(f"{FASTAPI_URL}/health")
            with urllib.request.urlopen(req, timeout=3.0) as resp:
                if resp.status == 200:
                    dt = (time.time() - t0) * 1000.0
                    return True, dt
                return False, 0
        except Exception:
            return False, 0

    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [executor.submit(single_probe) for _ in range(total_requests)]
        for f in futures:
            ok, lat = f.result()
            if ok:
                success_count += 1
                latencies.append(lat)
            else:
                fail_count += 1

    total_duration = time.time() - start_time
    latencies.sort()

    p50 = latencies[int(len(latencies) * 0.50)] if latencies else 0
    p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0
    p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0
    rps = round(total_requests / total_duration, 1) if total_duration > 0 else 0

    return {
        "total_requests": total_requests,
        "concurrency": concurrency,
        "duration_sec": round(total_duration, 3),
        "rps": rps,
        "success_rate": round((success_count / total_requests) * 100, 1),
        "min_ms": round(latencies[0], 2) if latencies else 0,
        "p50_ms": round(p50, 2),
        "p95_ms": round(p95, 2),
        "p99_ms": round(p99, 2),
        "max_ms": round(latencies[-1], 2) if latencies else 0
    }

HTML_DASHBOARD = r"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VKU MLOps AI Vision Cockpit — Live Inference Studio</title>
  <style>
    :root {
      --bg-dark: #080d1a;
      --panel-bg: rgba(16, 24, 48, 0.75);
      --panel-border: rgba(56, 189, 248, 0.2);
      --accent-cyan: #00F0FF;
      --accent-blue: #38BDF8;
      --accent-purple: #818CF8;
      --accent-emerald: #10B981;
      --accent-amber: #F59E0B;
      --accent-rose: #F43F5E;
      --text-main: #F1F5F9;
      --text-muted: #94A3B8;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      --font-sans: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 15% 20%, rgba(0, 240, 255, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(99, 102, 241, 0.1) 0%, transparent 45%),
        linear-gradient(180deg, #070b14 0%, #0d1527 100%);
      color: var(--text-main);
      font-family: var(--font-sans);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      overflow-x: hidden;
    }

    /* Header Nav */
    header {
      background: rgba(11, 19, 43, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--panel-border);
      padding: 14px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 50;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .vku-logo-badge {
      background: linear-gradient(135deg, #BA141A 0%, #E11D48 100%);
      color: white;
      font-weight: 800;
      font-size: 14px;
      letter-spacing: 1px;
      padding: 6px 10px;
      border-radius: 8px;
      box-shadow: 0 0 15px rgba(186, 20, 26, 0.4);
    }

    .brand-title {
      font-size: 18px;
      font-weight: 800;
      letter-spacing: 0.5px;
      background: linear-gradient(90deg, #FFFFFF, var(--accent-cyan));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .brand-sub {
      font-size: 11px;
      color: var(--text-muted);
      letter-spacing: 0.3px;
    }

    .status-cluster {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .pill-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(148, 163, 184, 0.2);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 11.5px;
      font-weight: 600;
    }

    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #64748B;
    }
    .dot.green { background: var(--accent-emerald); box-shadow: 0 0 8px var(--accent-emerald); }
    .dot.blue { background: var(--accent-cyan); box-shadow: 0 0 8px var(--accent-cyan); }
    .dot.amber { background: var(--accent-amber); box-shadow: 0 0 8px var(--accent-amber); }

    /* Top Telemetry Cards */
    .telemetry-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      padding: 20px 28px 10px 28px;
    }

    .metric-card {
      background: var(--panel-bg);
      backdrop-filter: blur(12px);
      border: 1px solid var(--panel-border);
      border-radius: 12px;
      padding: 14px 18px;
      transition: transform 0.2s, border-color 0.2s;
      position: relative;
      overflow: hidden;
    }

    .metric-card:hover {
      transform: translateY(-2px);
      border-color: var(--accent-cyan);
    }

    .metric-card::before {
      content: '';
      position: absolute;
      top: 0; left: 0; width: 4px; height: 100%;
      background: var(--accent-cyan);
    }
    .metric-card.purple::before { background: var(--accent-purple); }
    .metric-card.emerald::before { background: var(--accent-emerald); }
    .metric-card.amber::before { background: var(--accent-amber); }

    .metric-title {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 6px;
    }

    .metric-val {
      font-size: 20px;
      font-weight: 800;
      color: #FFFFFF;
      font-family: var(--font-mono);
      display: flex;
      align-items: baseline;
      gap: 6px;
    }

    .metric-sub {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    /* Main Studio Container */
    main {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      padding: 10px 28px 20px 28px;
      flex: 1;
    }

    .panel {
      background: var(--panel-bg);
      backdrop-filter: blur(14px);
      border: 1px solid var(--panel-border);
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }

    .panel-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--panel-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(15, 23, 42, 0.5);
    }

    .panel-title {
      font-size: 14px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
      color: #FFFFFF;
    }

    .panel-body {
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      flex: 1;
    }

    /* Sample Selector Bar */
    .sample-bar {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .sample-btn {
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid rgba(148, 163, 184, 0.25);
      color: var(--text-main);
      padding: 7px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .sample-btn:hover {
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
      transform: translateY(-1px);
    }

    .sample-btn.active {
      background: rgba(0, 240, 255, 0.2);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
      box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
    }

    /* Dropzone & Preview */
    .dropzone {
      border: 2px dashed rgba(56, 189, 248, 0.3);
      border-radius: 12px;
      padding: 24px;
      text-align: center;
      background: rgba(15, 23, 42, 0.4);
      cursor: pointer;
      transition: all 0.2s;
      position: relative;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 280px;
      overflow: hidden;
    }

    .dropzone:hover, .dropzone.dragover {
      border-color: var(--accent-cyan);
      background: rgba(0, 240, 255, 0.05);
    }

    .preview-container {
      position: relative;
      max-width: 100%;
      max-height: 380px;
      display: none;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    }

    .preview-img {
      max-width: 100%;
      max-height: 360px;
      object-fit: contain;
      display: block;
      border-radius: 8px;
    }

    .scanline {
      position: absolute;
      top: 0; left: 0; right: 0; height: 3px;
      background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
      box-shadow: 0 0 12px var(--accent-cyan);
      display: none;
      animation: scan 1.8s linear infinite;
    }

    @keyframes scan {
      0% { top: 0%; opacity: 0; }
      20% { opacity: 1; }
      80% { opacity: 1; }
      100% { top: 100%; opacity: 0; }
    }

    /* Action Buttons */
    .action-row {
      display: flex;
      gap: 12px;
    }

    .btn-primary {
      flex: 2;
      background: linear-gradient(135deg, #0284C7 0%, #00F0FF 100%);
      color: #041020;
      border: none;
      padding: 12px 20px;
      border-radius: 10px;
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 0.5px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all 0.2s;
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.35);
    }

    .btn-primary:hover {
      box-shadow: 0 0 28px rgba(0, 240, 255, 0.6);
      transform: translateY(-1px);
    }

    .btn-primary:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      box-shadow: none;
    }

    .btn-secondary {
      flex: 1;
      background: rgba(30, 41, 59, 0.8);
      border: 1px solid rgba(148, 163, 184, 0.3);
      color: var(--text-main);
      padding: 12px 16px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .btn-secondary:hover {
      background: rgba(56, 189, 248, 0.15);
      border-color: var(--accent-cyan);
    }

    /* Output Console */
    .output-stats-bar {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .stat-chip {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(148, 163, 184, 0.2);
      border-radius: 6px;
      padding: 6px 10px;
      font-size: 11.5px;
      font-family: var(--font-mono);
    }
    .stat-chip span { color: var(--accent-cyan); font-weight: 700; }

    .text-console {
      flex: 1;
      min-height: 280px;
      background: rgba(5, 10, 24, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.2);
      border-radius: 10px;
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 13px;
      line-height: 1.6;
      color: #E2E8F0;
      white-space: pre-wrap;
      overflow-y: auto;
      max-height: 380px;
      position: relative;
    }

    .console-placeholder {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      color: var(--text-muted);
      gap: 8px;
    }

    /* Toast Notification */
    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: rgba(16, 185, 129, 0.95);
      color: white;
      padding: 10px 18px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
      display: none;
      z-index: 100;
      animation: fadeIn 0.2s ease;
    }

    /* Ecosystem Quick Bar */
    .ecosystem-bar {
      padding: 12px 28px 20px 28px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      border-top: 1px solid rgba(148, 163, 184, 0.1);
      background: rgba(11, 19, 43, 0.4);
    }

    .link-group {
      display: flex;
      gap: 10px;
    }

    .eco-btn {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(148, 163, 184, 0.2);
      color: var(--text-muted);
      text-decoration: none;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .eco-btn:hover {
      color: white;
      border-color: var(--accent-cyan);
      background: rgba(56, 189, 248, 0.1);
    }
  </style>
</head>
<body>

  <!-- Top Header Navigation -->
  <header>
    <div class="brand">
      <div class="vku-logo-badge">VKU MLOPS</div>
      <div>
        <div class="brand-title">DUAL-NODE AI VISION COCKPIT</div>
        <div class="brand-sub">Rootless Containerization • Zero-Trust Network • Real-time Tesseract OCR Engine</div>
      </div>
    </div>

    <div class="status-cluster">
      <div class="pill-badge" id="pillFastapi"><span class="dot green"></span>FastAPI: :8080</div>
      <div class="pill-badge" id="pillRootless"><span class="dot blue"></span>Rootless: UID 10001</div>
      <div class="pill-badge" id="pillZeroTrust"><span class="dot green"></span>Zero-Trust: Port 5432 Closed</div>
      <div class="pill-badge" id="pillPrometheus"><span class="dot green"></span>Prometheus: :9090</div>
    </div>
  </header>

  <!-- Telemetry Row -->
  <section class="telemetry-row">
    <div class="metric-card">
      <div class="metric-title">Mô hình AI Suy luận</div>
      <div class="metric-val" id="dispModel">Tesseract LSTM</div>
      <div class="metric-sub" id="dispModelVer">Version: v3.0.0-tesseract-ocr</div>
    </div>
    <div class="metric-card purple">
      <div class="metric-title">An ninh Phân vùng Container</div>
      <div class="metric-val" id="dispSecurity">Rootless Safe</div>
      <div class="metric-sub">User namespaces • Slirp4netns active</div>
    </div>
    <div class="metric-card emerald">
      <div class="metric-title">Độ trễ Suy luận (Roundtrip)</div>
      <div class="metric-val"><span id="dispLatency">--</span> <small style="font-size:12px;font-weight:500;">ms</small></div>
      <div class="metric-sub" id="dispResolution">Chờ yêu cầu đầu vào...</div>
    </div>
    <div class="metric-card amber">
      <div class="metric-title">Tài nguyên Host Arch Linux</div>
      <div class="metric-val"><span id="dispRam">--</span> <small style="font-size:12px;font-weight:500;">RAM</small></div>
      <div class="metric-sub" id="dispHostInfo">Arch Linux Rolling Kernel</div>
    </div>
  </section>

  <!-- Main Work Studio -->
  <main>
    <!-- Left Column: Input Studio -->
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">
          <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
          ẢNH ĐẦU VÀO & CHỌN MẪU THỬ NGHIỆM
        </div>
        <span style="font-size:11px;color:var(--text-muted);">Hỗ trợ PNG, JPG, WEBP</span>
      </div>

      <div class="panel-body">
        <!-- 1-Click Sample Bar -->
        <div class="sample-bar">
          <span style="font-size:12px;font-weight:700;color:var(--text-muted);display:flex;align-items:center;">⚡ Chọn Mẫu:</span>
          <button class="sample-btn" onclick="loadSample('sample_receipt.png', this)">🧾 Hóa Đơn Bán Lẻ (Receipt)</button>
          <button class="sample-btn" onclick="loadSample('sample_syslog.png', this)">💻 Nhật Ký An Ninh (Syslog)</button>
          <button class="sample-btn" onclick="loadSample('sample_ocr.png', this)">📄 API Swagger Spec</button>
        </div>

        <!-- Dropzone / Image Preview Area -->
        <div class="dropzone" id="dropzone" onclick="document.getElementById('fileInput').click()">
          <input type="file" id="fileInput" accept="image/*" style="display:none" onchange="handleFileSelect(event)">
          
          <div id="dropzonePrompt">
            <svg width="48" height="48" fill="none" stroke="rgba(56, 189, 248, 0.6)" stroke-width="1.5" viewBox="0 0 24 24" style="margin-bottom:12px;"><path d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
            <div style="font-weight:700;font-size:14px;color:#FFFFFF;">Kéo & Thả ảnh tài liệu vào đây</div>
            <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">hoặc bấm để chọn ảnh từ máy tính</div>
          </div>

          <div class="preview-container" id="previewContainer">
            <img id="previewImg" class="preview-img" alt="Preview">
            <div class="scanline" id="scanline"></div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="action-row">
          <button class="btn-primary" id="btnScan" onclick="triggerScan()">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
            QUÉT AI NHẬN DIỆN CHỮ NGAY
          </button>
          <button class="btn-secondary" onclick="reloadModel()" title="Kiểm chứng tính năng cập nhật mô hình không downtime">
            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
            Hot Reload Model
          </button>
        </div>
      </div>
    </div>

    <!-- Right Column: Extracted Intelligence -->
    <div class="panel">
      <div class="panel-header">
        <div class="panel-title">
          <svg width="18" height="18" fill="none" stroke="var(--accent-cyan)" stroke-width="2" viewBox="0 0 24 24"><path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          KẾT QUẢ BÓC TÁCH VĂN BẢN (EXTRACTED OCR TEXT)
        </div>
        <div style="display:flex;gap:8px;">
          <button class="sample-btn" onclick="copyResultText()" id="btnCopy">📋 Copy Text</button>
          <button class="sample-btn" onclick="downloadResultText()">💾 Tải .TXT</button>
        </div>
      </div>

      <div class="panel-body">
        <div class="output-stats-bar">
          <div class="stat-chip">Trạng Thái: <span id="chipStatus">READY</span></div>
          <div class="stat-chip">Tổng Số Từ: <span id="chipWords">0 từ</span></div>
          <div class="stat-chip">Tổng Ký Tự: <span id="chipChars">0 ký tự</span></div>
          <div class="stat-chip">Engine: <span id="chipEngine">Tesseract LSTM</span></div>
        </div>

        <div class="text-console" id="textConsole">
          <div class="console-placeholder" id="consolePlaceholder">
            <svg width="40" height="40" fill="none" stroke="rgba(148, 163, 184, 0.4)" stroke-width="1.5" viewBox="0 0 24 24"><path d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path></svg>
            <div>Chưa có dữ liệu. Vui lòng chọn ảnh mẫu hoặc kéo thả ảnh để AI quét.</div>
          </div>
        </div>
      </div>
    </div>
  </main>

  <!-- Bottom Ecosystem Bar -->
  <footer class="ecosystem-bar">
    <div class="link-group">
      <span style="font-size:12px;font-weight:700;color:var(--text-muted);display:flex;align-items:center;">🌐 MLOps Stack:</span>
      <a href="http://localhost:3000" target="_blank" class="eco-btn">📊 Grafana Telemetry (:3000)</a>
      <a href="http://localhost:9090" target="_blank" class="eco-btn">📈 Prometheus (:9090)</a>
      <a href="http://localhost:5000" target="_blank" class="eco-btn">🧪 MLflow UI (:5000)</a>
      <a href="http://localhost:8080/docs" target="_blank" class="eco-btn">📑 Swagger API (:8080)</a>
    </div>

    <div style="font-size:12px;color:var(--text-muted);font-weight:600;">
      🛡️ VKU Thesis 2026 • Dual-Node MLOps Isolation Architecture
    </div>
  </footer>

  <!-- Toast Notification -->
  <div class="toast" id="toastBox">Đã sao chép văn bản vào bộ nhớ tạm!</div>

  <script>
    let currentImageFile = null;

    // Load initial system stats
    async function refreshStatus() {
      try {
        const res = await fetch('/api/status');
        const data = await res.json();
        
        if (data.fastapi) {
          document.getElementById('pillFastapi').innerHTML = '<span class="dot green"></span>FastAPI: ONLINE';
          if (data.model_version) document.getElementById('dispModelVer').innerText = 'Version: ' + data.model_version;
        } else {
          document.getElementById('pillFastapi').innerHTML = '<span class="dot amber"></span>FastAPI: OFFLINE';
        }

        if (data.system) {
          document.getElementById('dispRam').innerText = data.system.mem_used_mb + ' / ' + data.system.mem_total_mb + ' MB';
          document.getElementById('dispHostInfo').innerText = data.system.hostname + ' • ' + data.system.kernel;
        }
      } catch (e) {
        console.error('Status refresh error:', e);
      }
    }
    refreshStatus();
    setInterval(refreshStatus, 8000);

    // Sample Loader
    async function loadSample(filename, btnElement) {
      document.querySelectorAll('.sample-btn').forEach(b => b.classList.remove('active'));
      if (btnElement) btnElement.classList.add('active');

      try {
        const res = await fetch('/api/sample-image/' + filename);
        const blob = await res.blob();
        currentImageFile = new File([blob], filename, { type: blob.type || 'image/png' });
        
        displayPreview(URL.createObjectURL(blob));
        showToast('Đã nạp ảnh mẫu: ' + filename);
      } catch (e) {
        alert('Lỗi tải ảnh mẫu: ' + e);
      }
    }

    function handleFileSelect(e) {
      const file = e.target.files[0];
      if (!file) return;
      currentImageFile = file;
      document.querySelectorAll('.sample-btn').forEach(b => b.classList.remove('active'));
      displayPreview(URL.createObjectURL(file));
    }

    function displayPreview(src) {
      const prompt = document.getElementById('dropzonePrompt');
      const container = document.getElementById('previewContainer');
      const img = document.getElementById('previewImg');
      prompt.style.display = 'none';
      container.style.display = 'block';
      img.src = src;
    }

    // Drag and drop handling
    const dropzone = document.getElementById('dropzone');
    dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.classList.remove('dragover');
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        currentImageFile = e.dataTransfer.files[0];
        displayPreview(URL.createObjectURL(currentImageFile));
      }
    });

    // Run OCR Inference
    async function triggerScan() {
      if (!currentImageFile) {
        alert('Vui lòng chọn 1 ảnh mẫu hoặc tải ảnh lên trước khi quét!');
        return;
      }

      const btn = document.getElementById('btnScan');
      const scanline = document.getElementById('scanline');
      const consoleBox = document.getElementById('textConsole');
      const placeholder = document.getElementById('consolePlaceholder');

      btn.disabled = true;
      btn.innerText = '⚡ AI Đang Phân Tích...';
      scanline.style.display = 'block';
      if (placeholder) placeholder.style.display = 'none';

      const formData = new FormData();
      formData.append('file', currentImageFile);

      const t0 = performance.now();
      try {
        const res = await fetch('/api/scan', {
          method: 'POST',
          body: formData
        });
        const duration = Math.round(performance.now() - t0);
        const data = await res.json();

        if (data.status === 'success') {
          consoleBox.innerText = data.extracted_text;
          document.getElementById('dispLatency').innerText = duration;
          document.getElementById('dispResolution').innerText = 'Kích thước: ' + (data.image_resolution || 'Chuẩn');
          document.getElementById('chipStatus').innerText = 'THÀNH CÔNG (' + duration + ' ms)';
          document.getElementById('chipWords').innerText = data.word_count + ' từ';
          document.getElementById('chipChars').innerText = data.char_count + ' ký tự';
          showToast('Quét thành công trong ' + duration + ' ms!');
        } else {
          consoleBox.innerText = 'LỖI: ' + JSON.stringify(data, null, 2);
          document.getElementById('chipStatus').innerText = 'LỖI XỬ LÝ';
        }
      } catch (err) {
        consoleBox.innerText = 'Lỗi kết nối tới vi dịch vụ AI: ' + err;
        document.getElementById('chipStatus').innerText = 'KẾT NỐI THẤT BẠI';
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg> QUÉT AI NHẬN DIỆN CHỮ NGAY';
        scanline.style.display = 'none';
      }
    }

    // Model Hot Reload
    async function reloadModel() {
      try {
        const res = await fetch('/api/reload-model', { method: 'POST' });
        const data = await res.json();
        if (data.active_version) {
          document.getElementById('dispModelVer').innerText = 'Version: ' + data.active_version;
          showToast('Hot Reload thành công! Model Active: ' + data.active_version);
        }
      } catch (e) {
        alert('Lỗi reload model: ' + e);
      }
    }

    // Copy to clipboard
    function copyResultText() {
      const text = document.getElementById('textConsole').innerText;
      if (!text || text.includes('Chưa có dữ liệu')) return;
      navigator.clipboard.writeText(text).then(() => {
        showToast('Đã sao chép văn bản vào clipboard!');
      });
    }

    // Download .txt
    function downloadResultText() {
      const text = document.getElementById('textConsole').innerText;
      if (!text || text.includes('Chưa có dữ liệu')) return;
      const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'ocr_extracted_text_' + Date.now() + '.txt';
      a.click();
    }

    function showToast(msg) {
      const box = document.getElementById('toastBox');
      box.innerText = msg;
      box.style.display = 'block';
      setTimeout(() => { box.style.display = 'none'; }, 2600);
    }

    // Auto-select receipt sample on startup
    window.addEventListener('DOMContentLoaded', () => {
      const firstBtn = document.querySelector('.sample-btn');
      if (firstBtn) firstBtn.click();
    });
  </script>
</body>
</html>
"""

class CockpitHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silent logs for cleaner terminal
        pass

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        url_path = self.path.split("?")[0]

        if url_path in ("/", "/index.html", "/demo"):
            content = HTML_DASHBOARD.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        elif url_path == "/api/status":
            fastapi_ok = False
            model_ver = "v3.0.0-tesseract-ocr"
            try:
                req = urllib.request.Request(f"{FASTAPI_URL}/health")
                with urllib.request.urlopen(req, timeout=1.0) as resp:
                    if resp.status == 200:
                        fastapi_ok = True
                        hdata = json.loads(resp.read().decode())
                        model_ver = hdata.get("model_version", model_ver)
            except Exception:
                fastapi_ok = False

            data = {
                "fastapi": fastapi_ok,
                "model_version": model_ver,
                "prometheus": check_endpoint_health(PROMETHEUS_URL),
                "grafana": check_endpoint_health(GRAFANA_URL),
                "mlflow": check_endpoint_health(MLFLOW_URL),
                "system": get_system_stats()
            }
            self.send_json(data)
            return

        elif url_path.startswith("/api/sample-image/"):
            filename = os.path.basename(url_path)
            file_path = os.path.join(ASSETS_DIR, filename)
            if os.path.exists(file_path):
                ext = os.path.splitext(filename)[1].lower()
                mime = "image/png" if ext == ".png" else "image/jpeg"
                with open(file_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", mime)
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
                return
            else:
                self.send_error(404, "Sample image not found")
                return

        self.send_error(404, "Not Found")

    def do_POST(self):
        url_path = self.path.split("?")[0]

        if url_path == "/api/scan":
            content_type = self.headers.get("Content-Type", "")
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            target_url = f"{FASTAPI_URL}/v1/ocr/scan"
            req = urllib.request.Request(target_url, data=post_data, headers={"Content-Type": content_type})
            
            try:
                with urllib.request.urlopen(req, timeout=10.0) as resp:
                    resp_data = resp.read()
                    self.send_response(resp.status)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Content-Length", str(len(resp_data)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(resp_data)
            except urllib.error.HTTPError as he:
                err_data = he.read()
                self.send_response(he.code)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(err_data)))
                self.end_headers()
                self.wfile.write(err_data)
            except Exception as e:
                self.send_json({"status": "error", "message": str(e)}, status=500)
            return

        elif url_path == "/api/reload-model":
            target_url = f"{FASTAPI_URL}/v1/models/reload"
            req = urllib.request.Request(target_url, data=b"", headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=3.0) as resp:
                    resp_data = resp.read()
                    self.send_response(resp.status)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Content-Length", str(len(resp_data)))
                    self.end_headers()
                    self.wfile.write(resp_data)
            except Exception as e:
                self.send_json({"status": "error", "message": str(e)}, status=500)
            return

        elif url_path == "/api/benchmark-quick":
            res = run_quick_benchmark(total_requests=50, concurrency=10)
            self.send_json(res)
            return

        self.send_error(404, "Not Found")

def run_server():
    server_address = ("0.0.0.0", PORT)
    httpd = HTTPServer(server_address, CockpitHandler)
    print("\033[1;36m" + "="*70 + "\033[0m")
    print(f"\033[1;32m[✔] VKU MLOps AI Vision Cockpit is RUNNING at:\033[0m")
    print(f"    👉 \033[1;33mhttp://localhost:{PORT}\033[0m (hoặc http://127.0.0.1:{PORT})")
    print("\033[1;36m" + "="*70 + "\033[0m")
    print("[*] Đang lắng nghe yêu cầu từ trình duyệt. Bấm Ctrl+C để dừng.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Đang tắt AI Cockpit...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
