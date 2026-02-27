import http.server
import socketserver
import json
import os
import datetime

PORT = 8000
FORMS_DIR = "Forms"

class ContactFormHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/submit-form':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # Make sure the directory exists
                if not os.path.exists(FORMS_DIR):
                    os.makedirs(FORMS_DIR)

                # Format a unique filename with a timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"contact_submission_{timestamp}.txt"
                filepath = os.path.join(FORMS_DIR, filename)

                # Write the text file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("New Contact Form Submission\n")
                    f.write("---------------------------\n")
                    f.write(f"Date: {data.get('submittedAt', '')}\n\n")
                    f.write(f"Name: {data.get('firstName', '')} {data.get('lastName', '')}\n")
                    f.write(f"Email: {data.get('email', '')}\n")
                    f.write(f"Company: {data.get('company', '')}\n\n")
                    f.write("Message:\n")
                    f.write(f"{data.get('message', '')}\n")

                # Send success response to the browser
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))

            except Exception as e:
                # Send error response
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), ContactFormHandler) as httpd:
        print(f"Server started successfully!")
        print(f"1) Please open your browser to: http://localhost:{PORT}/index.html")
        print(f"2) Submissions will now be silently saved to the 'Forms' folder.")
        print(f"Press Ctrl+C to stop the server.")
        httpd.serve_forever()
