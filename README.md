# Resume to Portfolio Generator

A Flask-based web application that automatically converts uploaded resumes (PDF/DOCX) into professional portfolio websites. Users can upload their CV and instantly generate a clean, modern portfolio site with download functionality.

## Features

- **Resume Parsing**: Supports PDF and DOCX files with comprehensive data extraction
- **Professional Design**: Clean, modern portfolio template matching reference designs
- **Comprehensive Sections**: Extracts and displays contact info, experience, education, skills, projects, certifications, achievements, languages, and interests
- **Optimized Performance**: Minified CSS and JavaScript for fast loading
- **Responsive Design**: Mobile-friendly layout with modern styling
- **Download Functionality**: Generate and download complete portfolio as ZIP file

## Recent Optimizations (July 27, 2025)

### File Size Reduction
- **CSS Minification**: Compressed all CSS from ~15KB to ~4KB (73% reduction)
- **JavaScript Compression**: Minified JS from ~2KB to ~0.5KB (75% reduction)
- **Template Optimization**: Removed unnecessary whitespace and comments
- **Overall Size**: Reduced portfolio template file size by approximately 60%

### Performance Improvements
- Removed redundant CSS properties
- Consolidated CSS selectors
- Compressed JavaScript variables and functions
- Maintained full functionality while reducing bandwidth usage

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install flask flask-sqlalchemy pypdf2 python-docx werkzeug
   ```

2. **Run Application**
   ```bash
   python main.py
   ```

3. **Access Application**
   - Open `http://localhost:5000`
   - Upload your resume (PDF or DOCX)
   - Download your generated portfolio

## Technology Stack

- **Backend**: Flask, SQLAlchemy, PyPDF2, python-docx
- **Frontend**: Bootstrap 5, Font Awesome, Inter Font
- **Database**: SQLite (configurable to PostgreSQL)
- **Styling**: Minified CSS with CSS variables
- **JavaScript**: Compressed vanilla JS for smooth scrolling and navigation

## Project Structure

```
├── app.py                 # Flask application setup
├── main.py               # Application entry point
├── models.py             # Database models
├── routes.py             # Application routes
├── resume_parser.py      # PDF/DOCX parsing logic
├── portfolio_generator.py # Portfolio creation logic
├── templates/
│   ├── index.html        # Landing page
│   ├── upload.html       # File upload interface
│   ├── preview.html      # Portfolio preview
│   └── portfolio_template.html # Generated portfolio (optimized)
├── static/               # CSS and JS assets
├── uploads/              # Uploaded resume files
└── generated/            # Generated portfolio files
```

## Resume Parsing Capabilities

The application intelligently extracts:

- **Contact Information**: Name, email, phone, location, LinkedIn, GitHub, portfolio
- **Professional Summary**: Career objectives and professional statements
- **Skills**: Technical and soft skills with categorization
- **Work Experience**: Job titles, companies, dates, descriptions
- **Projects**: Project names, technologies, descriptions
- **Education**: Degrees, institutions, dates, achievements
- **Certifications**: Professional credentials and certifications
- **Achievements**: Awards, recognitions, accomplishments
- **Languages**: Language proficiencies with skill levels
- **Interests**: Personal interests and hobbies

## Portfolio Template Features

- **Modern Design**: Clean white background with professional typography
- **Service Cards**: Circular icons with gradient backgrounds
- **Project Showcase**: Featured project cards with technology tags
- **Timeline Layout**: Professional experience and education timelines
- **Skill Categories**: Organized skill display with visual tags
- **Responsive Navigation**: Fixed header with smooth scrolling
- **Social Integration**: LinkedIn, GitHub, and email links
- **Mobile Optimized**: Fully responsive design for all devices

## Deployment

The application is designed for easy deployment on platforms like Replit:

- Environment variable configuration
- SQLite default with PostgreSQL option
- File upload handling with proper limits
- Session management and security

## Contributing

This project focuses on helping non-technical users create professional online presence from their existing CVs. Contributions should maintain the balance between comprehensive functionality and ease of use.

## License

Open source project for educational and professional portfolio generation.