from flask import Flask, render_template, jsonify
from ollama import chat
from read import get_unread_emails  
app = Flask(__name__)
def summarize_text(text):
    response = chat(
        model='mistral',
        messages=[{
            'role': 'user',
            'content': (
                f'Summarize the following email body in a professional manner in lessthan 50 words,do not start with "Email Summary:":\n{text} '
            )
        }]
    )
    return response['message']['content']
@app.route("/")
def home():
    try:
        emails = get_unread_emails().get("unread_emails", [])
        if not emails:
            return render_template("index.html", message="No unread emails found.")
        
        summarized_emails=[]
        for email in emails:
            sender=email["sender"]
            subject=email["subject"]
            summary=summarize_text(subject)
            summarized_emails.append({
                "sender": sender,
                "subject": subject,
                "summary": summary
            })

        return render_template("index.html", summarized_emails=summarized_emails)
    except Exception as e:
        return render_template("index.html", error=str(e))

if __name__ == "__main__":
    app.run(debug=True)
