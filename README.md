# GP's AI Resume Analyzer 🚀

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3%2B-green)
![AI](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

**GP's AI Resume Analyzer** is a comprehensive, full-stack web application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). 

Powered by **Google's Gemini 2.0 Flash**, this tool analyzes resumes against specific job descriptions to provide actionable feedback, a visual match score, and smart editing tools to significantly increase hiring chances.

---

## ✨ Key Features

### 📊 Core Analysis
* **Smart Match Score:** Instantly visualize how well your resume fits the job with a dynamic, animated circular gauge.
* **Keyword Highlighter:** * <span style="color:green">**Green Badges**</span> highlight skills you successfully matched.
    * <span style="color:red">**Red Badges**</span> alert you to critical keywords missing from your profile.
* **Deep Analysis:** Get a structured breakdown of your "Key Strengths" and specific "Areas for Improvement."

### 🛠️ Bonus AI Tools
* **✨ Bullet Point Refiner:** Paste a weak resume bullet point (e.g., *"Worked on sales"*), and the AI will rewrite it into 3 powerful, STAR-method variations (Conservative, Aggressive, Concise).
* **🎯 Interview Prep:** Generates 5 technical and 3 behavioral interview questions tailored specifically to your resume and the target role.
* **✍️ Cover Letter Drafter:** Instantly writes a professional, persuasive cover letter connecting your unique experience to the job requirements.

### 📂 Utilities
* **📄 PDF Export:** Download the full analysis report, including interview questions and feedback, as a clean PDF file.
* **Multi-Format Support:** Accepts both `.pdf` and `.docx` files.

---

## 🏗️ Tech Stack

* **Backend:** Python, Flask
* **AI Engine:** Google Gemini API (`gemini-2.0-flash`)
* **Frontend:** HTML5, Tailwind CSS, JavaScript
* **Visualization:** Chart.js (Match Score Gauge)
* **PDF Generation:** html2pdf.js
* **File Processing:** `pdfplumber` (PDF extraction), `mammoth` (DOCX extraction)

---

## 🚀 Installation & Setup Guide

Follow these steps to run the project locally on your machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/ai-resume-analyzer.git](https://github.com/YOUR_USERNAME/ai-resume-analyzer.git)
cd ai-resume-analyzer
2. Create a Virtual Environment (Recommended)
It is best practice to isolate your project dependencies.

Windows:

Bash

python -m venv venv
venv\Scripts\activate
Mac/Linux:

Bash

python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash

pip install -r requirements.txt
4. Set Up Environment Variables
You need a Google Gemini API Key to run the AI.

Get a free API key from Google AI Studio.

Create a new file in the root folder named .env.

Open .env and add your key:

Plaintext

GEMINI_API_KEY=your_actual_api_key_here
(Note: The .env file is ignored by Git to keep your key secure.)

5. Run the Application
Bash

python app.py
Open your browser and go to http://127.0.0.1:5000 to start analyzing! 🎉

📂 Project Structure
Plaintext

ai-resume-analyzer/
├── app.py               # Main Flask application logic & AI integration
├── requirements.txt     # List of Python dependencies
├── .env                 # API Keys (Excluded from Git)
├── .gitignore           # Files to ignore (venv, .env, uploads)
├── uploads/             # Temporary storage for processing files
└── templates/
    └── index.html       # The frontend user interface (Tailwind + JS)
🤝 Contributing
Contributions are welcome! Here's how you can help:

Fork the project.

Create your feature branch (git checkout -b feature/AmazingFeature).

Commit your changes (git commit -m 'Add some AmazingFeature').

Push to the branch (git push origin feature/AmazingFeature).

Open a Pull Request.

📝 License
© 2025 Guruprasad | All Rights Reserved. This project is proprietary and not open-source for redistribution.

👋 Contact
For any questions or feedback, please reach out to Guruprasad Patil(patilguruprasad2004@gmail.com).