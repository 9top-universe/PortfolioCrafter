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
        
        if file and allowed_file(file.filename):
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
        # Add CSS file
        css_content = """
/* Portfolio Styles */
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
.container { max-width: 1200px; margin: 0 auto; padding: 20px; }
.header { text-align: center; margin-bottom: 2rem; }
.section { margin-bottom: 2rem; }
.skills-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; }
.skill-item { background: #f8f9fa; padding: 0.5rem; border-radius: 0.25rem; text-align: center; }
@media print { body { font-size: 12px; } .container { padding: 10px; } }
"""
        zipf.writestr('styles.css', css_content)
    
    return send_file(zip_path, as_attachment=True, download_name=zip_filename)

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('upload_page'))
