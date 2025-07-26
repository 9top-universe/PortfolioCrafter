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
            'location': self._extract_location(text),
            'linkedin': self._extract_linkedin(text),
            'github': self._extract_github(text),
            'portfolio_url': self._extract_portfolio_url(text),
            'summary': self._extract_summary(text),
            'skills': self._extract_skills(text),
            'experience': self._extract_experience(text),
            'projects': self._extract_projects(text),
            'education': self._extract_education(text),
            'certifications': self._extract_certifications(text),
            'achievements': self._extract_achievements(text),
            'languages': self._extract_languages(text),
            'interests': self._extract_interests(text),
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
    
    def _extract_location(self, text: str) -> str:
        """Extract location from resume text"""
        location_patterns = [
            r'([A-Za-z\s]+,\s*[A-Z]{2})',  # City, State
            r'([A-Za-z\s]+,\s*[A-Za-z\s]+)',  # City, Country
            r'\b(Remote)\b',  # Remote work
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        return ""
    
    def _extract_linkedin(self, text: str) -> str:
        """Extract LinkedIn URL from resume text"""
        linkedin_pattern = r'(?:linkedin\.com/in/|linkedin\.com/profile/)([A-Za-z0-9\-\.]+)'
        matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
        if matches:
            return f"https://linkedin.com/in/{matches[0]}"
        
        # Also check for just linkedin usernames
        linkedin_pattern2 = r'linkedin[:\s]+([A-Za-z0-9\-\.]+)'
        matches2 = re.findall(linkedin_pattern2, text, re.IGNORECASE)
        if matches2:
            return f"https://linkedin.com/in/{matches2[0]}"
        return ""
    
    def _extract_github(self, text: str) -> str:
        """Extract GitHub URL from resume text"""
        github_pattern = r'(?:github\.com/)([A-Za-z0-9\-\.]+)'
        matches = re.findall(github_pattern, text, re.IGNORECASE)
        if matches:
            return f"https://github.com/{matches[0]}"
        
        # Also check for just github usernames
        github_pattern2 = r'github[:\s]+([A-Za-z0-9\-\.]+)'
        matches2 = re.findall(github_pattern2, text, re.IGNORECASE)
        if matches2:
            return f"https://github.com/{matches2[0]}"
        return ""
    
    def _extract_portfolio_url(self, text: str) -> str:
        """Extract portfolio URL from resume text"""
        url_pattern = r'(?:portfolio|website)[:\s]+(https?://[^\s]+)'
        matches = re.findall(url_pattern, text, re.IGNORECASE)
        if matches:
            return matches[0]
        
        # Look for personal domains
        domain_pattern = r'(https?://(?:www\.)?[a-zA-Z0-9\-]+\.[a-zA-Z]{2,})'
        domains = re.findall(domain_pattern, text)
        for domain in domains:
            if not any(site in domain.lower() for site in ['linkedin', 'github', 'gmail', 'yahoo', 'outlook']):
                return domain
        return ""
    
    def _extract_projects(self, text: str) -> List[Dict]:
        """Extract projects from resume text"""
        projects = []
        project_keywords = ['projects', 'portfolio', 'personal projects', 'key projects']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in project_keywords):
                # Extract project entries
                for j in range(i + 1, min(i + 15, len(lines))):
                    project_line = lines[j].strip()
                    if not project_line:
                        continue
                    if any(section in project_line.lower() 
                          for section in ['experience', 'education', 'skills', 'work']):
                        break
                    
                    # Look for project patterns
                    if len(project_line) > 10 and len(projects) < 6:
                        project = {
                            'title': project_line,
                            'description': '',
                            'technologies': [],
                            'url': ''
                        }
                        
                        # Look for technologies in next few lines
                        for k in range(j + 1, min(j + 3, len(lines))):
                            if k < len(lines):
                                next_line = lines[k].strip()
                                if any(tech_word in next_line.lower() for tech_word in ['tech', 'built', 'using', 'language']):
                                    tech_list = re.split(r'[,•·\-]', next_line)
                                    project['technologies'] = [t.strip() for t in tech_list if t.strip()][:5]
                                    break
                                elif next_line and len(next_line) > 20:
                                    project['description'] = next_line
                        
                        projects.append(project)
                break
        
        return projects
    
    def _extract_certifications(self, text: str) -> List[Dict]:
        """Extract certifications from resume text"""
        certifications = []
        cert_keywords = ['certification', 'certificate', 'licensed', 'certified', 'credentials']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in cert_keywords):
                # Extract certification entries
                for j in range(i + 1, min(i + 10, len(lines))):
                    cert_line = lines[j].strip()
                    if not cert_line:
                        continue
                    if any(section in cert_line.lower() 
                          for section in ['experience', 'education', 'skills', 'work']):
                        break
                    
                    if len(cert_line) > 5 and len(certifications) < 8:
                        # Extract year if present
                        year_match = re.search(r'(20\d{2})', cert_line)
                        year = year_match.group(1) if year_match else ''
                        
                        certifications.append({
                            'name': cert_line,
                            'issuer': '',
                            'year': year
                        })
                break
        
        return certifications
    
    def _extract_achievements(self, text: str) -> List[str]:
        """Extract achievements and awards from resume text"""
        achievements = []
        achievement_keywords = ['award', 'achievement', 'honor', 'recognition', 'scholarship', 'competition']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in achievement_keywords):
                # Extract achievement entries
                for j in range(i + 1, min(i + 8, len(lines))):
                    achievement_line = lines[j].strip()
                    if not achievement_line:
                        continue
                    if any(section in achievement_line.lower() 
                          for section in ['experience', 'education', 'skills', 'work']):
                        break
                    
                    if len(achievement_line) > 5 and len(achievements) < 6:
                        achievements.append(achievement_line)
                break
        
        return achievements
    
    def _extract_languages(self, text: str) -> List[Dict]:
        """Extract languages from resume text"""
        languages = []
        language_keywords = ['language', 'fluent', 'native', 'proficient']
        
        # Common languages list for better detection
        common_languages = [
            'english', 'spanish', 'french', 'german', 'italian', 'portuguese', 'russian',
            'chinese', 'japanese', 'korean', 'arabic', 'hindi', 'dutch', 'swedish'
        ]
        
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in language_keywords):
                # Extract language entries
                for j in range(i, min(i + 5, len(lines))):
                    lang_line = lines[j].strip().lower()
                    for lang in common_languages:
                        if lang in lang_line and len(languages) < 5:
                            proficiency = 'Fluent'
                            if 'native' in lang_line:
                                proficiency = 'Native'
                            elif 'basic' in lang_line:
                                proficiency = 'Basic'
                            elif 'intermediate' in lang_line:
                                proficiency = 'Intermediate'
                            
                            languages.append({
                                'name': lang.title(),
                                'proficiency': proficiency
                            })
                break
        
        return languages
    
    def _extract_interests(self, text: str) -> List[str]:
        """Extract interests and hobbies from resume text"""
        interests = []
        interest_keywords = ['interest', 'hobby', 'hobbies', 'personal', 'activities']
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            if any(keyword in line.lower() for keyword in interest_keywords):
                # Extract interest entries
                for j in range(i, min(i + 3, len(lines))):
                    interest_line = lines[j].strip()
                    if not interest_line:
                        continue
                    
                    # Split by common delimiters
                    line_interests = re.split(r'[,•·\-\n]', interest_line)
                    for interest in line_interests:
                        interest = interest.strip()
                        if (interest and len(interest) > 2 and len(interest) < 30 
                            and not any(keyword in interest.lower() for keyword in interest_keywords)
                            and len(interests) < 8):
                            interests.append(interest)
                break
        
        return interests
