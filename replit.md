# Resume to Portfolio Generator

## Overview

This is a Flask-based web application that automatically converts uploaded resumes (PDF/DOCX) into professional portfolio websites. The system parses resume content, extracts relevant information, and generates a complete portfolio website that users can download as a ZIP file.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

**July 26, 2025**: Major portfolio template enhancement
- Completely redesigned portfolio template with modern dark theme
- Added animated background with floating gradients
- Implemented fixed navigation with smooth scrolling
- Created responsive timeline layout for experience and education
- Enhanced skill cards with gradient backgrounds and hover effects
- Added scroll-triggered animations and intersection observers
- Improved mobile responsiveness and print styles
- Updated downloadable CSS to match new design

**July 26, 2025**: Comprehensive resume parsing and section enhancement
- Enhanced resume parser to extract all key resume sections:
  * Contact information (name, email, phone, location, LinkedIn, GitHub, portfolio)
  * Professional summary and career objectives
  * Skills categorization and technical competencies
  * Work experience with detailed formatting
  * Projects with technologies and descriptions
  * Education background and academic credentials
  * Certifications and professional credentials
  * Achievements, awards, and recognitions
  * Language proficiencies with skill levels
  * Personal interests and hobbies
- Updated portfolio template to display all sections conditionally
- Improved parsing algorithms for better data extraction
- Enhanced portfolio generator to process and organize all new data types
- Made website generation much more comprehensive and detailed

**July 26, 2025**: Complete portfolio design overhaul
- Redesigned portfolio template to match modern clean style from user reference images
- Switched from dark theme to clean white background with professional typography
- Implemented service cards with circular icons for "What I Do" section
- Created project showcase cards with featured badges and technology tags
- Added professional navigation with highlighted active states
- Designed clean timeline layouts for experience and education
- Integrated modern color scheme with blue accent colors
- Enhanced responsive design for mobile and tablet devices
- Added smooth scrolling navigation and interactive elements

## System Architecture

The application follows a traditional Flask MVC architecture with clear separation of concerns:

- **Flask Web Framework**: Handles HTTP requests, routing, and templating
- **SQLAlchemy ORM**: Manages database operations with SQLite as the default database
- **File Processing**: Dedicated modules for resume parsing and portfolio generation
- **Template Engine**: Jinja2 templates for dynamic HTML generation
- **Static Assets**: Bootstrap-based responsive UI with custom CSS/JS

## Key Components

### Backend Components

1. **Flask Application (`app.py`)**
   - Main application factory and configuration
   - Database initialization with SQLAlchemy
   - File upload configuration (16MB limit)
   - Session management with secret key

2. **Database Models (`models.py`)**
   - Portfolio model: Stores metadata about generated portfolios
   - Tracks original filename, generated filename, user details, and creation timestamp

3. **Resume Parser (`resume_parser.py`)**
   - Extracts text from PDF files using PyPDF2
   - Extracts text from DOCX files using python-docx
   - Parses extracted text to identify resume sections (name, email, skills, experience, etc.)

4. **Portfolio Generator (`portfolio_generator.py`)**
   - Transforms parsed resume data into portfolio structure
   - Generates default content when information is missing
   - Applies professional styling and formatting

5. **Routes (`routes.py`)**
   - `/`: Homepage with feature overview
   - `/upload`: Resume upload interface
   - `/upload` (POST): Processes uploaded files
   - File download endpoints for generated portfolios

### Frontend Components

1. **Templates**
   - `index.html`: Landing page with features showcase
   - `upload.html`: File upload interface with drag-and-drop
   - `preview.html`: Portfolio preview and download page
   - `portfolio_template.html`: Generated portfolio template

2. **Static Assets**
   - Custom CSS for upload interface and styling
   - JavaScript for file upload handling and user interactions
   - Bootstrap integration for responsive design

## Data Flow

1. **Upload Process**:
   - User uploads resume file via web interface
   - File is validated and saved with unique filename
   - Resume parser extracts text content
   - Portfolio generator creates structured data
   - Portfolio HTML is generated from template
   - Database record is created
   - User is redirected to preview page

2. **Download Process**:
   - Generated portfolio files are packaged into ZIP
   - ZIP file is served for download
   - Temporary files are cleaned up

## External Dependencies

### Python Packages
- **Flask**: Web framework and routing
- **Flask-SQLAlchemy**: Database ORM
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX file processing
- **Werkzeug**: File handling and security utilities

### Frontend Libraries
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Icon library
- **Custom CSS/JS**: Enhanced user experience

### File Storage
- Local filesystem for uploaded resumes
- Generated portfolio files stored temporarily
- SQLite database for metadata persistence

## Deployment Strategy

### Development Configuration
- SQLite database for simplicity
- Debug mode enabled
- Local file storage
- Session secret from environment variable

### Production Considerations
- Database URL configurable via `DATABASE_URL` environment variable
- Session secret should be set via `SESSION_SECRET` environment variable
- File upload limits configured (16MB)
- Proxy fix middleware for deployment behind reverse proxy

### File Management
- Upload folder: `uploads/`
- Generated files folder: `generated/`
- Automatic directory creation on startup
- Unique filename generation to prevent conflicts

The application is designed to be easily deployable on platforms like Replit, with environment variable configuration and reasonable defaults for development.