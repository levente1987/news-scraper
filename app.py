from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/pdf")
def proxy_pdf():
    pdf_url = request.args.get("url")
    if not pdf_url:
        return "Missing 'url' parameter", 400

    try:
        response = requests.get(pdf_url, verify=False, timeout=10)
        response.raise_for_status()
        return Response(
            response.content,
            content_type="application/pdf",
            headers={
                "Content-Disposition": "inline; filename=kozlony.pdf"
            }
        )
    except Exception as e:
        return f"Error downloading PDF: {str(e)}", 404
