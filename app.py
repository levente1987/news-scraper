from flask import Flask, request, Response
import requests
import urllib.parse
import os

app = Flask(__name__)

@app.route("/pdf")
def proxy_pdf():
    encoded_url = request.args.get("url")
    if not encoded_url:
        return "Missing 'url' parameter", 400

    pdf_url = urllib.parse.unquote(encoded_url)

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; RenderPDFProxy/1.0; +https://render.com/)"
        }
        response = requests.get(pdf_url, headers=headers, timeout=10)
        response.raise_for_status()
        return Response(
            response.content,
            content_type="application/pdf",
            headers={"Content-Disposition": "inline; filename=kozlony.pdf"}
        )
    except Exception as e:
        return f"Error downloading PDF: {str(e)}", 404

# ✅ THIS is the critical fix for Render to detect the port:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
