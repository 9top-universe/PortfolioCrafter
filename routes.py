import os
import uuid
import zipfile
from flask import render_template, request, redirect, url_for, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from app import app, db
from models import Portfolio
from resume_parser import ResumeParser
from portfolio_generator import PortfolioGenerator

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'resume' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['resume']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and file.filename and allowed_file(file.filename):
            # Generate unique filename
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Parse the resume
            parser = ResumeParser()
            parsed_data = parser.parse_resume(filepath)
            
            if not parsed_data:
                flash('Could not extract information from the resume. Please check the file format.', 'error')
                os.remove(filepath)
                return redirect(url_for('upload_page'))
            
            # Generate portfolio
            generator = PortfolioGenerator()
            portfolio_data = generator.generate_portfolio(parsed_data)
            
            # Save to database
            portfolio = Portfolio(
                original_filename=filename,
                generated_filename=f"portfolio_{uuid.uuid4()}.html",
                name=parsed_data.get('name', 'Unknown'),
                email=parsed_data.get('email', ''),
                phone=parsed_data.get('phone', '')
            )
            db.session.add(portfolio)
            db.session.commit()
            
            # Generate HTML file
            portfolio_html = render_template('portfolio_template.html', **portfolio_data)
            portfolio_path = os.path.join(app.config['GENERATED_FOLDER'], portfolio.generated_filename)
            
            with open(portfolio_path, 'w', encoding='utf-8') as f:
                f.write(portfolio_html)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return redirect(url_for('preview', portfolio_id=portfolio.id))
        else:
            flash('Invalid file type. Please upload PDF or DOCX files only.', 'error')
            return redirect(url_for('upload_page'))
            
    except Exception as e:
        app.logger.error(f"Error processing upload: {str(e)}")
        flash('An error occurred while processing your resume. Please try again.', 'error')
        return redirect(url_for('upload_page'))

@app.route('/preview/<int:portfolio_id>')
def preview(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    portfolio_path = os.path.join(app.config['GENERATED_FOLDER'], portfolio.generated_filename)
    
    if not os.path.exists(portfolio_path):
        flash('Portfolio file not found.', 'error')
        return redirect(url_for('index'))
    
    with open(portfolio_path, 'r', encoding='utf-8') as f:
        portfolio_content = f.read()
    
    return render_template('preview.html', portfolio=portfolio, portfolio_content=portfolio_content)

@app.route('/download/<int:portfolio_id>')
def download_portfolio(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    portfolio_path = os.path.join(app.config['GENERATED_FOLDER'], portfolio.generated_filename)
    
    if not os.path.exists(portfolio_path):
        flash('Portfolio file not found.', 'error')
        return redirect(url_for('index'))
    
    # Create ZIP file
    zip_filename = f"portfolio_{portfolio.name}_{portfolio.id}.zip"
    zip_path = os.path.join(app.config['GENERATED_FOLDER'], zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(portfolio_path, 'index.html')
        # Add enhanced CSS file
        css_content = """
/* Modern Portfolio Styles */
:root {
    --primary-color: #1a1a2e;
    --secondary-color: #16213e;
    --accent-color: #0f3460;
    --highlight-color: #e94560;
    --text-primary: #ffffff;
    --text-secondary: #b8bcc8;
    --text-accent: #e94560;
    --bg-primary: #0f0f23;
    --bg-secondary: #16213e;
    --bg-card: #1a1a2e;
    --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --gradient-accent: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    --shadow-soft: 0 10px 40px rgba(0, 0, 0, 0.1);
    --shadow-hover: 0 20px 60px rgba(0, 0, 0, 0.15);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.7;
    color: var(--text-primary);
    background: var(--bg-primary);
    overflow-x: hidden;
}

.navbar {
    position: fixed;
    top: 0;
    width: 100%;
    padding: 1rem 0;
    background: rgba(26, 26, 46, 0.95);
    backdrop-filter: blur(10px);
    z-index: 1000;
    transition: all 0.3s ease;
}

.hero-section {
    min-height: 100vh;
    display: flex;
    align-items: center;
    position: relative;
    background: var(--gradient-primary);
    padding: 80px 0 60px;
}

.hero-title {
    font-size: clamp(3rem, 8vw, 6rem);
    font-weight: 700;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.section { padding: 6rem 0; position: relative; }

.section-title {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-align: center;
    background: var(--gradient-accent);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.skill-category {
    background: var(--bg-card);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: var(--shadow-soft);
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 2rem;
}

.skill-tag {
    background: var(--gradient-accent);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    font-size: 0.9rem;
    font-weight: 500;
    margin: 0.25rem;
    display: inline-block;
}

.timeline-content {
    background: var(--bg-card);
    padding: 2rem;
    border-radius: 15px;
    box-shadow: var(--shadow-soft);
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 2rem;
}

.timeline-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.timeline-company {
    color: var(--text-accent);
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.contact-item {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1.5rem;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.95);
    text-decoration: none;
    margin: 0.5rem;
}

@media (max-width: 768px) {
    .hero-title { font-size: 2.5rem; }
    .section { padding: 4rem 0; }
}

@media print {
    body { color: #000; background: #fff; }
    .navbar { display: none; }
    .hero-section { min-height: auto; padding: 2rem 0; background: #333 !important; }
    .section { padding: 2rem 0; }
    .skill-category, .timeline-content { border: 1px solid #ddd; box-shadow: none; }
}
"""
        zipf.writestr('styles.css', css_content)
    
    return send_file(zip_path, as_attachment=True, download_name=zip_filename)

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('upload_page'))
