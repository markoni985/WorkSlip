#https://stackoverflow.com/questions/51025893/flask-at-first-run-do-not-use-the-development-server-in-a-production-environmen
# libraries to be imported 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import glob
import os
import json
from flask import Flask, request, render_template
import os
from dotenv import load_dotenv
load_dotenv()

dbms = os.environ.get("DBMS")


fromaddrog = os.environ.get("fromaddr")
fromaddrog = fromaddrog.strip('[]"') 
toaddrog = os.environ.get("toaddr")
toaddrog = toaddrog.strip('[]"') 
addressog = os.environ.get("address")
addressog = addressog.strip('[]"') 
passwordog = os.environ.get("password")
passwordog = passwordog.strip('[]"')
techEmail = ""
busEmail =""

# Create a Flask app
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML file

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == "POST":
        # Collect fields by their IDs
        data = {
            "invoice_reference": request.form.get("refNumber"),
            "date": request.form.get("dateField"),
            "business_name": request.form.get("busName"),
            "business_phone": request.form.get("busPhone"),
            "business_address": request.form.get("busAddr"),
            "business_email": request.form.get("busEmail"),
            "service_nature": request.form.get("serviceNature"),
            "service_performed": request.form.get("servicePerformed"),
            "performed_by": request.form.get("performedBy"),
            "tech_Email": request.form.get("techEmail"),
            "cash_pay": request.form.get("cashPay") == "on",
            "charge_pay": request.form.get("chargePay") == "on",
            "check_pay": request.form.get("checkPay") == "on",
            "check_num": request.form.get('checkNum'),            
            "new_install": request.form.get("newInstall") == "on",
            "1st_visit": request.form.get("1stVis") == "on",
            "2nd_visit": request.form.get("2ndVis") == "on",
            "3rd_visit": request.form.get("3dVis") == "on",
            "COD": request.form.get("COD") == "on",
            "NCC": request.form.get("NCC") == "on",
            "invoiced": request.form.get("invoiced") == "on",
            "time_in": request.form.get("timeIn"),
            "time_out": request.form.get("timeOut"),
            "total_hours": request.form.get("totalHr"),
            "active_client": request.form.get("activeClient") == "on",
            "parts_cost": request.form.get("partsCost"),
            "labor_cost": request.form.get("laborCost"),
            "subtotal": request.form.get("subtotal"),
            "tax": request.form.get("tax"),
            "total": request.form.get("total"),
            "authorized_name": request.form.get("authorizedName"),
            "signature": request.form.get("signature"),
        }

        techEmail = request.form.get("techEmail")
        busEmail = request.form.get("busEmail")


        # Collect table rows dynamically
        items = []
        row_index = 1
        while request.form.get(f"qty{row_index}"):
            items.append({
                "quantity": request.form.get(f"qty{row_index}"),
                "part": request.form.get(f"part{row_index}"),
                "serial_number": request.form.get(f"sn{row_index}"),
                "price": request.form.get(f"price{row_index}"),
                "amount": request.form.get(f"amount{row_index}")
                
            })
            print("loop")
            row_index += 1

        data["items"] = items
        print(data)
        print (data["items"] )
        # Get form data (non-file fields)
        form_data = request.form.to_dict()
    
        # Get the uploaded PDF
        pdf_file = request.files.get("pdf")
        try:
            if pdf_file:
                pdf_file_name = pdf_file.filename
                print(f"Received PDF file: {pdf_file_name}")
                # Save the file
                save_path = os.path.join("uploads", pdf_file_name)
                pdf_file.save(save_path)
                # Generate JSON file name based on the PDF file name
                json_file_name = f"{pdf_file_name}.json"
                json_file_path = os.path.join("uploads", json_file_name)

                # Save the data to the JSON file
                with open(json_file_path, "w") as json_file:
                    json.dump(data, json_file, indent=4)
                sendEmail2(pdf_file_name, json_file_name)
                        # Return success response
            return {"status": "success", "message": "Email sent successfully!"}
               # Handle other form data
            print(form_data)

        
            # Process or save the data as needed
            return f"Collected data: {data}"

        except Exception as e:
            # Handle errors and return failure response
            print(f"Error: {e}")
            return {"status": "error", "message": "Failed to send email."}

           
    return render_template("index.html")




def getaddr():
    
    try:
        f=open("address.txt")
        print ("File opened.")
        var=f.readlines()
        print ("Lines read.")
        f.close()
        print ("File closed.")
        address = [line.rstrip('\n') for line in open("address.txt")]
        #address = [var.strip() for x in var] 
        print (address)
        return address

        
    except:
        address = [addressog]
        return address
        print ("Emailing default.")

def sendEmail(file_name):

        load_dotenv()
        
        filename = file_name
        # instance of MIMEMultipart 
        msg = MIMEMultipart() 

        # storing the senders email address 
        msg['From'] = fromaddrog 

        # storing the receivers email address
        rcv = getaddr()
        print("Recv")
        print(rcv)
        if busEmail and techEmail.strip() != "":
            rcv.append(busEmail)
        if techEmail and techEmail.strip() != "":
            rcv.append(techEmail)
        toaddr=rcv
        msg['To'] = ", ".join(rcv)
        #msg['To'] = toaddr
        print("Here are recipients")
        print(msg['To'])
        # storing the subject 
        msg['Subject'] = filename

        # string to store the body of the mail 
        body = "Here is Your Work Slip:"

        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 


        
        file_path = os.path.join(os.getcwd(), 'uploads', filename)
        attachment = open(file_path, "rb")

        


        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 

        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 

        # encode into base64 
        encoders.encode_base64(p) 

        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 

        # creates SMTP session 
        s = smtplib.SMTP('smtp.gmail.com', 587) 

        # start TLS for security 
        s.starttls() 

        # Authentication 
        s.login(fromaddrog, passwordog) 

        # Converts the Multipart msg into a string 
        text = msg.as_string() 

        print(toaddr)
        # sending the mail 
        s.sendmail(fromaddrog, toaddr, text)


def sendEmail2(file1_name, file2_name):
    #load_dotenv()
    techEmail = request.form.get("techEmail")
    busEmail = request.form.get("busEmail")
    #print("Email Collected")
    #print(techEmail)
    #print(busEmail)

    rcv = getaddr()  # Assuming this function gets the recipient addresses
    if busEmail.strip() != "":
        rcv.append(busEmail)
        #print("Appended")
    if techEmail.strip() != "":
        rcv.append(techEmail)
        #print("Appended")
    # Create email message instance
    msg = MIMEMultipart()
    msg['From'] = fromaddrog
    msg['To'] = ", ".join(rcv)
    msg['Subject'] = file1_name
    #print(msg['To'])

    # Email body
    body = "Here is Your Work Slip:"
    msg.attach(MIMEText(body, 'plain'))

    # Attach first file
    file1_path = os.path.join(os.getcwd(), 'uploads', file1_name)
    with open(file1_path, "rb") as attachment:
        part1 = MIMEBase('application', 'octet-stream')
        part1.set_payload(attachment.read())
        encoders.encode_base64(part1)
        part1.add_header('Content-Disposition', f"attachment; filename= {file1_name}")
        msg.attach(part1)

    # Attach second file
    file2_path = os.path.join(os.getcwd(), 'uploads', file2_name)
    with open(file2_path, "rb") as attachment:
        part2 = MIMEBase('application', 'octet-stream')
        part2.set_payload(attachment.read())
        encoders.encode_base64(part2)
        part2.add_header('Content-Disposition', f"attachment; filename= {file2_name}")
        msg.attach(part2)

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(fromaddrog, passwordog)
            server.sendmail(fromaddrog, rcv, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

