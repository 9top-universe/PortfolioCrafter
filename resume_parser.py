import os
import re
import logging
from typing import Dict, List, Optional
import PyPDF2
from docx import Document

class ResumeParser:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def parse_resume(self, file_path: str) -> Optional[Dict]:
        """Parse resume and extract relevant information"""
        try:
            # Extract text based on file extension
            if file_path.lower().endswith('.pdf'):
                text = self._extract_pdf_text(file_path)
            elif file_path.lower().endswith(('.docx', '.doc')):
                text = self._extract_docx_text(file_path)
            else:
                self.logger.error(f"Unsupported file format: {file_path}")
                return None
            
            if not text:
                self.logger.error("No text extracted from file")
                return None
            
            # Parse extracted text
            parsed_data = self._parse_text(text)
            return parsed_data
            
        except Exception as e:
            self.logger.error(f"Error parsing resume: {str(e)}")
            return None
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            self.logger.error(f"Error extracting PDF text: {str(e)}")
        return text
    
    def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            self.logger.error(f"Error extracting DOCX text: {str(e)}")
        return text
    
    def _parse_text(self, text: str) -> Dict:
        """Parse extracted text and identify sections"""
        parsed_data = {
            'name': self._extract_name(text),
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'summary': self._extract_summary(text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'education': self._extract_education(text),
            'raw_text': text
        }
        
        return parsed_data
    
    def _extract_name(self, text: str) -> str:
        """Extract name from resume text"""
        lines = text.strip().split('\n')
        # Assume name is in the first few lines
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 2 and len(line) < 50:
                # Skip lines that look like emails, phones, or addresses
                if not re.search(r'[@\d]', line) and len(line.split()) <= 4:
                    return line.title()
        return "Portfolio Owner"
    
    def _extract_email(self, text: str) -> str:
        """Extract email from resume text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from resume text"""
        phone_pattern = r'(\+?1?[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
        phones = re.findall(phone_pattern, text)
        if phones:
            return ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
        return ""
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary or objective"""
        summary_keywords = ['summary', 'objective', 'profile', 'about']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in summary_keywords):
                # Get next few lines as summary
                summary_lines = []
                for j in range(i + 1, min(i + 5, len(lines))):
                    if lines[j].strip() and not any(section in lines[j].lower() 
                                                  for section in ['experience', 'education', 'skills']):
                        summary_lines.append(lines[j].strip())
                    else:
                        break
                return ' '.join(summary_lines)
        return ""
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        skills = []
        skills_keywords = ['skills', 'technologies', 'competencies', 'technical skills']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in skills_keywords):
                # Get next few lines as skills
                for j in range(i + 1, min(i + 10, len(lines))):
                    skill_line = lines[j].strip()
                    if skill_line and not any(section in skill_line.lower() 
                                           for section in ['experience', 'education', 'work']):
                        # Split by common delimiters
                        line_skills = re.split(r'[,•·\-\n]', skill_line)
                        for skill in line_skills:
                            skill = skill.strip()
                            if skill and len(skill) > 1:
                                skills.append(skill)
                    else:
                        break
                break
        
        return skills[:20]  # Limit to 20 skills
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience from resume text"""
        experience = []
        exp_keywords = ['experience', 'work history', 'employment', 'professional experience']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in exp_keywords):
                # Extract experience entries
                current_job = {}
                for j in range(i + 1, len(lines)):
                    exp_line = lines[j].strip()
                    if not exp_line:
                        continue
                    if any(section in exp_line.lower() 
                          for section in ['education', 'skills', 'projects']):
                        break
                    
                    # Simple job parsing
                    if current_job and ('company' not in current_job or 'position' not in current_job):
                        if len(exp_line.split()) <= 6:  # Likely a job title or company
                            if 'position' not in current_job:
                                current_job['position'] = exp_line
                            elif 'company' not in current_job:
                                current_job['company'] = exp_line
                    elif len(experience) < 5:  # Limit to 5 jobs
                        if current_job:
                            experience.append(current_job)
                        current_job = {'position': exp_line, 'description': ''}
                
                if current_job:
                    experience.append(current_job)
                break
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information from resume text"""
        education = []
        edu_keywords = ['education', 'academic', 'degree', 'university', 'college']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in edu_keywords):
                # Extract education entries
                for j in range(i + 1, min(i + 10, len(lines))):
                    edu_line = lines[j].strip()
                    if not edu_line:
                        continue
                    if any(section in edu_line.lower() 
                          for section in ['experience', 'skills', 'work']):
                        break
                    
                    if len(edu_line.split()) > 2:  # Likely an education entry
                        education.append({
                            'degree': edu_line,
                            'institution': '',
                            'year': ''
                        })
                break
        
        return education
