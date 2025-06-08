from flask import Flask, request, render_template
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import numpy as np
from io import StringIO
app = Flask(__name__)

FLAG = 'grifflesCTF{8A+GmF[!G1k5BYg(}'
ACCURACY_THRESHOLD = 0.80  # 80% accuracy required to get the flag

def validate(file):
    # Check if the file has the right format (header should be "ID")
    if not file or len(file) < 2:  # At least a header and one row
        return False, "File is empty or too small."

    # Load the KNN model
    with open("./fraud_classifier.pkl", 'rb') as f:
        KNN = pickle.load(f)

    csv_content = "\n".join(file)
    df = pd.read_csv(StringIO(csv_content))

    df_clean = df.drop("Id", axis=1).iloc[:, 0:5]

    # Make sure the user didn't just copy the same row for the whole doc
    row_sim = cosine_similarity(df_clean)
    # Remove diagonal elements of this matrix because the cosine similarity of a vector with itself is 1
    row_sim = row_sim[~np.eye(row_sim.shape[0],dtype=bool)].reshape(row_sim.shape[0],-1)

    if row_sim.mean() >= 0.95 or df_clean.shape[0] != 2000:
        # Rows are too similar, reject the data
        return False, "🚨🚨 ALERT: DATA POISONING DETECTED!! CALLING FINANCE DEPARTMENT 🚨🚨"
    
    preds = KNN.predict(df_clean)
    fraudulent_transactions = (preds == 1).sum()
    total_transactions = len(preds)
    percentage_fraudulent = (fraudulent_transactions / total_transactions)

    if percentage_fraudulent > 0.2:
        return True, "🚨🚨 ALERT: TOO MANY FRAUDULENT TRANSACTIONS !! CALLING FINANCE DEPARTMENT 🚨🚨"
    else:
        return True, f"NO SUSPICIOUS BEHAVIOUR DETECTED.✅✅ PRINTING FLAG... {FLAG}"

@app.route("/", methods=['GET', 'POST'])
def page():
    if request.method == 'GET':
        return render_template("upload.html")
    elif request.method == 'POST':
        f = request.files['document']
        content = f.read()
        if len(content) > 500000: return render_template("upload.html", box="error", message="bruh")

        try:
            content = content.decode().split("\n")
        except UnicodeDecodeError:
            # they sent us rubbish!!!!!!
            # bruh moment
            return render_template('upload.html', box="error", message="Please send a valid csv file.")
        
        acc, msg = validate(content)
        return render_template("upload.html", box="ok" if acc else "error", message=msg)  


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)