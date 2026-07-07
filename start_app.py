"""Launch the learning app on a local server. Open in phone browser or desktop."""
import http.server
import socket
import sys
import webbrowser
import os
import io

# Fix encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PORT = 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

print('=' * 50)
print('  📖 精读笔记 APP 已启动')
print('=' * 50)
print()
print('  📱 手机访问：')
# Try to get local IP
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    print(f'     http://{ip}:{PORT}/index.html')
except:
    ip = 'localhost'
    print(f'     http://localhost:{PORT}/index.html')
print()
print('  💻 电脑预览：')
print(f'     http://localhost:{PORT}/index.html')
print()
print('  📌 手机打开链接后，点浏览器菜单 → 添加到主屏幕')
print('  📌 按 Ctrl+C 停止服务器')
print()

webbrowser.open(f'http://localhost:{PORT}/index.html')
http.server.HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
