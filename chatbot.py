import os
from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import spacy
import sqlite3
import jwt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from werkzeug.utils import secure_filename

invoices=[]
expenses=[]
budgets=[]
reminders=[]

app = Flask(__name__)
SECRET_KEY="your_secret_key"

nlp=spacy.load("en_core_web_sm")
users={"admin":"password9999"}
roles={"admin":"admin"}

class DocumentClassifier:
  def __init__(self):
    self.vectorizer=CountVectorizer()
    self.clf=MultinomialNB()
    self.trained=False

  def train_model(self, documents, labels):
    X=self.vectorizer.fit_transform(documents)
    self.clf.fit(X,labels)
    self.trained=True

  def classify_document(self,document):
    if not self.trained:
      return "Model not trained"
    X_new = self.vectorizer.transform([document])
    return self.clf.predict(X_new)[0]

classifier=DocumentClassifier()



#Database setup
def init_db():
  conn=sqlite3.connect("documents.db")
  cursor=conn.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, content TEXT)''')
  conn.commit()
  return conn
conn=init_db()



#Document Extraction
@app.route("/upload",methods=["POST"])
def upload_document():
  file=request.files.get('file')
  if file:
    filename=secure_filename(file.filename)
    filepath=os.path.join("uploads",filename)
    file.save(os.path.join(filepath))

    try:
      if filename.endswith(('.png','.jpg','.jpeg','.tiff')):
        image=Image.open(filepath)
        extracted_text=pytesseract.image_to_string(image)
      else:
        return jsonify({"message":"Unsupported file format"}),400
    except Exception as e:
      return jsonify({"message":"Error during text extraction"}),500

    cursor=conn.cursor()
    cursor.execute("INSERT INTO documents (content) VALUES (?)",(extracted_text,))
    conn.commit()
    return jsonify({"message":"Document uploaded successfully"}),200
  else:
    return jsonify({"message":"No file provided"}),400



#Named Entity Recognition
@app.route('/ner',methods=["POST"])
def perform_NER():
  data=request.json
  text=data.get("text")
  entity_type=data.get("entity_type",None)

  if text:
    doc=nlp(text)
    if entity_type:
      entity_type=entity_type.upper()
      entities=[{"entity":ent.text,"label":ent.label_} for ent in doc.ents if ent.label_==entity_type]
    else:
      entities=[{"entity":ent.text,"label":ent.label_} for ent in doc.ents]
    return jsonify({"entities":entities})
  else:
    return jsonify({"message":"No text provided"}),400



#Document Classification
@app.route('/train_classifier',methods=['POST'])
def Train_Classifier():
  data=request.json
  documents=data.get("documents")
  labels=data.get("labels")

  if documents and labels and len(documents)==len(labels):
    classifier.train_model(documents, labels)
    return jsonify({"message":"Classifier trained successfully"})
  else:
    return jsonify({"message":"Invalid data format"}),400

@app.route('/classify',methods=['POST'])
def classify_document():
  data=request.json
  text=data.get("text")
  if text:
    prediction=classifier.classify_document(text)
    return jsonify({"document_type":prediction})
  else:
    return jsonify({"message":"No text provider"}),400



#Search functionality
@app.route('/search',methods=['GET'])
def search_documents():
  query=request.args.get('query')
  if query:
    cursor=conn.cursor()
    pattern=f"%{query}%"
    cursor.execute("SELECT * FROM documents WHERE content LIKE ?",(pattern,))
    results=cursor.fetchall()
    return jsonify({"results":results})
  else:
    return jsonify({"message":"No query provided"}),400



#User Verification and Role-Based Authentication
@app.route('/verify',methods=['POST'])
def verify_User():
  data=request.json
  username=data.get("username")
  password=data.get("password")

  if users.get(username)==password:
    token=jwt.encode({"username":username,"role":roles[username]},SECRET_KEY,algorithm="HS256")
    return jsonify({"token":token})
  else:
    return jsonify({"message":"Invalid credentials"}),401

@app.route('/dashboard',methods=['GET'])
def DashBoard():
  auth_header=request.headers.get("Authorization")
  if auth_header:
    token=auth_header.split(" ")[1]
    try:
      decoded=jwt.decode(token,SECRET_KEY,algorithms=["HS256"])
      return jsonify({"message":f"Welcome {decoded['username']} with role {decoded['role']}!"})
    except jwt.ExpiredSignatureError:
      return jsonify({"message":"Token has expired"}),400
    except jwt.InvalidTokenError:
      return jsonify({"message":"Invalid token"}),400
  else:
    return jsonify({"message":"Authorization token required"}),401



#Account balance enquiry
@app.route('/account_balance',methods=['GET'])
def account_balance_inquiry():
  #dummy account balance for demo purpose
  balances={
      "savings":4500,
      "checking":1200,
      "credit":500
  }
  return jsonify({"Account Balances":balances})



#Transaction history
@app.route('/transaction_history',methods=['GET'])
def transaction_history():
  transactions=[
      {"data":"2024-09-28","type":"debit","amount":50.00},
      {"data":"2024-09-30","type":"credit","amount":100.00},
      {"data":"2024-10-01","type":"credit","amount":150.00}
  ]

  date_filter=request.args.get("date")
  type_filter=request.args.get("type")
  amount_filter=request.args.get("amount")

  if date_filter:
    transactions=[t for t in transactions if t['date']==date_filter]
  if type_filter:
    transactions=[t for t in transactions if t['type']==type_filter]
  if amount_filter:
    transactions=[t for t in transactions if t['amount']==float(amount_filter)]

  return jsonify({"transactions":transactions})



#Invoice Management
@app.route('/invoices',methods=['POST'])
def create_invoice():
  data=request.json
  invoice={
      "id":len(invoices)+1,
      "description":data.get("description"),
      "amount":data.get("amount"),
      "status":"Pending"
  }
  invoices.append(invoice)
  return jsonify({"message":"Invoice created","invoice":invoice})

@app.route('/invoices',methods=['GET'])
def list_invoices():
    return jsonify({"invoices":invoices})

@app.route('/invoice_status/<int:invoice_id>',methods=['GET'])
def invoice_status(invoice_id):
    invoice=next((inv for inv in invoices if inv['id']==invoice_id),None)
    if invoice:
      return jsonify({"invoice_id":invoice_id,"status":invoice['status']})
    else:
      return jsonify({"message":"Invoice not found"}),400



#Expense tracking
@app.route('/track_expense',methods=['POST'])
def track_expenses():
  data=request.json
  expense={
      "category":data.get("category"),
      "amount":data.get("amount"),
      "description":data.get("description"),
      "date":data.get("date","2024-10-02") #taking today as default
  }
  expenses.append(expense)
  return jsonify({"message":"Expense tracked","expense":expense})

@app.route('/monthly_expenses',methods=['GET'])
def monthly_expenses():
  summary=sum(exp["amount"] for exp in expenses if "2024-10" in exp['date']) #summarizing expenses for this month
  return jsonify({"monthly expenses":summary,"details":expenses})



#Budgeting Assistance
@app.route('/set_budget',methods=['POST'])
def set_budget():
  data=request.json
  budget={
      "category":data.get("category"),
      "amount":data.get("amount")
  }
  budgets.append(budget)
  return jsonify({"message":"Budget set", "budget":budget})

@app.route('/budget_summary',methods=['GET'])
def budget_summary():
  category=request.args.get("category")
  if category:
    budget=next((b for b in budgets if b['category']==category),None)
    if budget:
      total_expense=sum(exp['amount'] for exp in expenses if exp['category']==category)
      return jsonify({
          "category":category,
          "budget":budget['amount'],
          "spent":total_expense,
          "remaining":budget['amount']-total_expense
      })
    else:
      return jsonify({"message":"No budget set for this category"}),404
  else:
    return jsonify({"budgets":budgets})



#Payment Reminders
@app.route('/payment_remainder',methods=['POST'])
def set_payment_reminder():
  data=request.json
  reminder={
      "description":data.get("description"),
      "due_date":data.get("due_date"),
      "amount":data.get("amount")
  }
  reminders.append(reminder)
  return jsonify({"message":"Payment reminder set","reminder":reminder})

@app.route('/payment_reminders',methods=['GET'])
def list_payment_reminders():
  return jsonify({"reminders":reminders})



#User Authentication and Role Management
@app.route('/role_management',methods=['POST'])
def role_management():
  data=request.json
  username=data.get("username")
  role=data.get("role")

  if username in users:
    roles[username]=role
    return jsonify({"message":f"Role of {username} updated to {role}"})
  else:
    return jsonify({"message":"User not found"}),404



#Generates HTTP link
if __name__=="__main__":
  app.run()


#This code is meant to run in production WSGI server ONLY





