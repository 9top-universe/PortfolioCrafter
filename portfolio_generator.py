import logging
from typing import Dict, Any

class PortfolioGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_portfolio(self, parsed_data: Dict) -> Dict[str, Any]:
        """Generate portfolio data structure from parsed resume data"""
        try:
            portfolio_data = {
                # Header/Contact Information
                'name': self._clean_text(parsed_data.get('name', 'Portfolio Owner')),
                'email': parsed_data.get('email', ''),
                'phone': parsed_data.get('phone', ''),
                'location': self._clean_text(parsed_data.get('location', '')),
                'linkedin': parsed_data.get('linkedin', ''),
                'github': parsed_data.get('github', ''),
                'portfolio_url': parsed_data.get('portfolio_url', ''),
                
                # Professional Summary
                'summary': self._clean_text(parsed_data.get('summary', '')),
                
                # Skills
                'skills': self._process_skills(parsed_data.get('skills', [])),
                
                # Work Experience
                'experience': self._process_experience(parsed_data.get('experience', [])),
                
                # Projects
                'projects': self._process_projects(parsed_data.get('projects', [])),
                
                # Education
                'education': self._process_education(parsed_data.get('education', [])),
                
                # Certifications
                'certifications': self._process_certifications(parsed_data.get('certifications', [])),
                
                # Achievements
                'achievements': parsed_data.get('achievements', []),
                
                # Languages
                'languages': parsed_data.get('languages', []),
                
                # Interests
                'interests': parsed_data.get('interests', []),
                
                'color_scheme': 'professional'  # Default color scheme
            }
            
            # Generate a professional summary if none exists
            if not portfolio_data['summary']:
                portfolio_data['summary'] = self._generate_default_summary(portfolio_data)
            
            return portfolio_data
            
        except Exception as e:
            self.logger.error(f"Error generating portfolio: {str(e)}")
            return self._get_default_portfolio()
    
    def _clean_text(self, text: str) -> str:
        """Clean and format text"""
        if not text:
            return ""
        return ' '.join(text.split())
    
    def _process_skills(self, skills: list) -> list:
        """Process and clean skills list"""
        processed_skills = []
        for skill in skills:
            if isinstance(skill, str):
                skill = skill.strip()
                if skill and len(skill) > 1 and skill not in processed_skills:
                    processed_skills.append(skill)
        
        # If no skills found, add some default categories
        if not processed_skills:
            processed_skills = ['Communication', 'Problem Solving', 'Team Work', 'Leadership']
        
        return processed_skills[:15]  # Limit to 15 skills
    
    def _process_experience(self, experience: list) -> list:
        """Process work experience entries"""
        processed_experience = []
        
        for exp in experience:
            if isinstance(exp, dict):
                processed_exp = {
                    'position': self._clean_text(exp.get('position', 'Professional Role')),
                    'company': self._clean_text(exp.get('company', 'Company Name')),
                    'duration': exp.get('duration', ''),
                    'description': self._clean_text(exp.get('description', ''))
                }
                processed_experience.append(processed_exp)
        
        # Add default experience if none found
        if not processed_experience:
            processed_experience = [{
                'position': 'Professional Experience',
                'company': 'Previous Employer',
                'duration': '',
                'description': 'Demonstrated professional skills and capabilities in previous roles.'
            }]
        
        return processed_experience
    
    def _process_education(self, education: list) -> list:
        """Process education entries"""
        processed_education = []
        
        for edu in education:
            if isinstance(edu, dict):
                processed_edu = {
                    'degree': self._clean_text(edu.get('degree', 'Education')),
                    'institution': self._clean_text(edu.get('institution', '')),
                    'year': edu.get('year', '')
                }
                processed_education.append(processed_edu)
        
        # Add default education if none found
        if not processed_education:
            processed_education = [{
                'degree': 'Educational Background',
                'institution': 'Academic Institution',
                'year': ''
            }]
        
        return processed_education
    
    def _process_projects(self, projects: list) -> list:
        """Process project entries"""
        processed_projects = []
        
        for project in projects:
            if isinstance(project, dict):
                processed_project = {
                    'title': self._clean_text(project.get('title', 'Project')),
                    'description': self._clean_text(project.get('description', '')),
                    'technologies': project.get('technologies', []),
                    'url': project.get('url', '')
                }
                processed_projects.append(processed_project)
        
        return processed_projects
    
    def _process_certifications(self, certifications: list) -> list:
        """Process certification entries"""
        processed_certifications = []
        
        for cert in certifications:
            if isinstance(cert, dict):
                processed_cert = {
                    'name': self._clean_text(cert.get('name', 'Certification')),
                    'issuer': self._clean_text(cert.get('issuer', '')),
                    'year': cert.get('year', '')
                }
                processed_certifications.append(processed_cert)
        
        return processed_certifications
    
    def _generate_default_summary(self, portfolio_data: Dict) -> str:
        """Generate a default professional summary"""
        name = portfolio_data.get('name', 'Professional')
        skills = portfolio_data.get('skills', [])
        
        if skills:
            summary = f"Experienced professional with expertise in {', '.join(skills[:3])}. "
            summary += "Proven track record of delivering results and contributing to team success. "
            summary += "Seeking opportunities to leverage skills and experience in a dynamic environment."
        else:
            summary = f"Dedicated professional with a strong background in various industries. "
            summary += "Committed to excellence and continuous learning. "
            summary += "Ready to contribute skills and expertise to achieve organizational goals."
        
        return summary
    
    def _get_default_portfolio(self) -> Dict[str, Any]:
        """Return default portfolio structure"""
        return {
            'name': 'Portfolio Owner',
            'email': '',
            'phone': '',
            'summary': 'Professional with diverse experience and skills.',
            'skills': ['Communication', 'Problem Solving', 'Team Work'],
            'experience': [{
                'position': 'Professional Role',
                'company': 'Previous Company',
                'duration': '',
                'description': 'Contributed to team success and organizational goals.'
            }],
            'education': [{
                'degree': 'Educational Background',
                'institution': 'Academic Institution',
                'year': ''
            }],
            'color_scheme': 'professional'
        }
