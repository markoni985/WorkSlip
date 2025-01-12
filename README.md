# Work Slip Generator

This project is a web application for generating and managing work slips. It allows users to fill out a form with various details, create a PDF of the work slip, and submit the form data to a server.

## Features

- Fill out a form with details such as invoice reference number, service nature, payment method, etc.
- Generate a PDF of the work slip.
- Submit the form data along with the generated PDF to a server.
- Display a loading spinner while the PDF is generated and the form is submitted.

## Technologies Used

- HTML
- CSS
- JavaScript
- Flask (Python)
- jsPDF (for PDF generation)
- HTML2Canvas (for capturing HTML content)
- Signature Pad (for capturing signatures)

## Setup and Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/your-username/work-slip-generator.git
   cd work-slip-generator

   
2. **Set up the Python environment:**
   
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. **Install the required Python packages:**
     pip install Flask

4. **Place your logo image in the static directory:**
    Ensure that the logo.png file is located in the static directory.
   work-slip-generator/
    ├── app.py
    ├── templates/
    │   ├── index.html
    ├── static/
        ├── logo.png
5. **Run the Flask application:**
   Create .env file containing:
  fromaddr = "senders email address" //used to login to Gmail account
  address = "recipient's email address"
  password = "Your Gmail password for this app"

6. **Run the Flask application:**
     python workslip.py

7. **Open the application in your browser:**
   Navigate to http://127.0.0.1:5000/ in your web browser.

   Usage
      Fill out the form:
      
      Enter the required details such as invoice reference number, service nature, payment method, etc.
      
      Generate the PDF:
      
      Click the "Submit" button to generate the PDF of the work slip.
      
      Submit the form:
      
      The form data along with the generated PDF will be submitted to the server. A loading spinner will be displayed while        the PDF is being generated and the form is being submitted.
      
      Contributing
      Contributions are welcome! Please feel free to submit a Pull Request.
      
      License
      This project is licensed under the MIT License. See the LICENSE file for more details.



   

   
