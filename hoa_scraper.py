#!/usr/bin/env python3
"""
Simple HOA Management Companies Scraper
Scrapes both recommended and regular companies from hoa-usa.com
Outputs clean CSV file in the same directory
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import logging
from datetime import datetime
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "https://hoa-usa.com/management-directory/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho",
    "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
    "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
    "New Hampshire", "New Jersey", "New Mexico", "New York",
    "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
    "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington",
    "West Virginia", "Wisconsin", "Wyoming"
]

class HOAScraper:
    def __init__(self, delay_between_requests=2):
        self.delay = delay_between_requests
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        
    def get_page_content(self, url, max_retries=3):
        """Fetch page content with retry logic"""
        for attempt in range(max_retries):
            try:
                logger.info(f"Fetching: {url}")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(self.delay * 2)
                else:
                    logger.error(f"Failed to fetch {url} after {max_retries} attempts")
                    return None
        return None
    
    def extract_company_data(self, company_element, section_type):
        """Extract data from a single company element"""
        try:
            company_data = {
                'section_type': section_type,
                'name': '',
                'website': '',
                'phone': '',
                'email': '',
                'service_area': '',
                'description': ''
            }
            
            if section_type == 'recommended':
                # Handle detailed recommended companies
                name_element = company_element.find('h4', class_='result-name')
                if name_element:
                    company_data['name'] = name_element.get_text(strip=True)
                
                # Extract website
                website_element = company_element.find('div', class_='result-website')
                if website_element:
                    website_link = website_element.find('a')
                    if website_link and website_link.get('href'):
                        company_data['website'] = website_link.get('href').strip()
                
                # Extract phone
                phone_element = company_element.find('div', class_='result-phone')
                if phone_element:
                    phone_text = phone_element.get_text()
                    phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
                    phone_match = phone_pattern.search(phone_text)
                    if phone_match:
                        company_data['phone'] = phone_match.group().strip()
                
                # Extract email
                email_element = company_element.find('div', class_='result-email')
                if email_element:
                    email_text = email_element.get_text()
                    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
                    email_match = email_pattern.search(email_text)
                    if email_match:
                        company_data['email'] = email_match.group().strip()
                
                # Extract service area
                service_area_element = company_element.find('div', class_='result-service-area')
                if service_area_element:
                    service_area_text = service_area_element.get_text()
                    service_area_clean = re.sub(r'^Service Area:\s*', '', service_area_text, flags=re.I).strip()
                    company_data['service_area'] = service_area_clean
                
                # Extract description
                desc_element = company_element.find('div', class_='result-description')
                if desc_element:
                    company_data['description'] = desc_element.get_text(strip=True)[:500]
            
            elif section_type == 'regular':
                # Handle simple regular companies
                name_element = company_element.find('strong')
                if name_element:
                    name_text = name_element.get_text(strip=True)
                    company_data['name'] = name_text.rstrip(':').strip()
                
                text_content = company_element.get_text()
                
                # Extract phone
                phone_pattern = re.compile(r'Phone:\s*(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})')
                phone_match = phone_pattern.search(text_content)
                if phone_match:
                    company_data['phone'] = phone_match.group(1).strip()
                
                # Extract service area
                service_area_pattern = re.compile(r'Service Area:\s*([^\n\r]+)')
                service_area_match = service_area_pattern.search(text_content)
                if service_area_match:
                    company_data['service_area'] = service_area_match.group(1).strip()
                
                # Extract email
                email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
                email_match = email_pattern.search(text_content)
                if email_match:
                    company_data['email'] = email_match.group().strip()
            
            return company_data
            
        except Exception as e:
            logger.error(f"Error extracting company data: {str(e)}")
            return None
    
    def scrape_state_page(self, state_name):
        """Scrape companies from a single state page"""
        url = f"{BASE_URL}?state={state_name}"
        html_content = self.get_page_content(url)
        
        if not html_content:
            return []
        
        soup = BeautifulSoup(html_content, 'html.parser')
        companies = []
        
        try:
            # Find recommended companies section
            recommended_heading = soup.find('h3', string=re.compile(r'Recommended HOA Management Companies', re.I))
            if recommended_heading:
                recommended_container = recommended_heading.find_next_sibling('div', class_='hoa-directory-recommended')
                if recommended_container:
                    recommended_companies = recommended_container.find_all('div', class_=re.compile(r'.*(result-gold|result-platinum).*'))
                    for company_element in recommended_companies:
                        company_data = self.extract_company_data(company_element, 'recommended')
                        if company_data and company_data['name']:
                            company_data['state'] = state_name
                            companies.append(company_data)

            # Find regular companies section
            regular_heading = soup.find('h3', string=re.compile(r'^HOA Management Companies$', re.I))
            if regular_heading:
                regular_container = regular_heading.find_next_sibling('div', class_='hoa-directory-results')
                if regular_container:
                    regular_companies = regular_container.find_all('div', class_=re.compile(r'.*result-normal.*'))
                    for company_element in regular_companies:
                        company_data = self.extract_company_data(company_element, 'regular')
                        if company_data and company_data['name']:
                            company_data['state'] = state_name
                            companies.append(company_data)

            recommended_count = len([c for c in companies if c.get('section_type') == 'recommended'])
            regular_count = len([c for c in companies if c.get('section_type') == 'regular'])
            
            logger.info(f"Found {len(companies)} companies for {state_name} (Recommended: {recommended_count}, Regular: {regular_count})")
            return companies
            
        except Exception as e:
            logger.error(f"Error scraping {state_name}: {str(e)}")
            return []
    
    def clean_phone_number(self, phone):
        """Clean and format phone numbers"""
        if not phone:
            return ''
        
        digits = re.sub(r'\D', '', phone)
        
        if len(digits) == 10:
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        elif len(digits) == 11 and digits[0] == '1':
            digits = digits[1:]
            return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
        else:
            return phone
    
    def clean_email(self, email):
        """Clean and validate email addresses"""
        if not email:
            return ''
        
        email = email.strip().lower()
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if email_pattern.match(email):
            return email
        return ''
    
    def clean_website(self, website):
        """Clean and validate website URLs"""
        if not website:
            return ''
        
        website = website.strip()
        
        if website and not website.startswith(('http://', 'https://')):
            website = 'https://' + website
        
        return website
    
    def scrape_and_save(self, selected_states=None):
        """Scrape all states and save to CSV"""
        states_to_scrape = selected_states if selected_states else US_STATES
        all_companies = []
        
        logger.info(f"Starting scraper for {len(states_to_scrape)} states")
        
        for i, state in enumerate(states_to_scrape, 1):
            logger.info(f"Scraping {state} ({i}/{len(states_to_scrape)})")
            companies = self.scrape_state_page(state)
            all_companies.extend(companies)
            
            if i < len(states_to_scrape):  # Don't delay after last state
                time.sleep(self.delay)
        
        if not all_companies:
            logger.warning("No data to save")
            return None
        
        # Convert to DataFrame and clean data
        df = pd.DataFrame(all_companies)
        
        # Clean data
        df['phone'] = df['phone'].apply(self.clean_phone_number)
        df['email'] = df['email'].apply(self.clean_email)
        df['website'] = df['website'].apply(self.clean_website)
        
        # Remove duplicates and empty names
        df = df.drop_duplicates(subset=['name', 'state'], keep='first')
        df = df[df['name'].str.strip() != '']
        
        # Reorder columns
        column_order = ['name', 'state', 'section_type', 'phone', 'email', 'website', 'service_area', 'description']
        df = df[column_order]
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'hoa_companies_{timestamp}.csv'
        
        # Save to CSV
        df.to_csv(filename, index=False, encoding='utf-8')
        
        # Print summary
        total_companies = len(df)
        recommended_count = len(df[df['section_type'] == 'recommended'])
        regular_count = len(df[df['section_type'] == 'regular'])
        
        logger.info("="*50)
        logger.info("SCRAPING COMPLETED!")
        logger.info(f"Total companies: {total_companies}")
        logger.info(f"Recommended: {recommended_count}")
        logger.info(f"Regular: {regular_count}")
        logger.info(f"Output file: {filename}")
        logger.info("="*50)
        
        return filename

def main():
    parser = argparse.ArgumentParser(description='HOA Management Companies Scraper')
    parser.add_argument('--states', nargs='+', help='Specific states to scrape (e.g., --states Alabama California)')
    parser.add_argument('--delay', type=int, default=2, help='Delay between requests in seconds (default: 2)')
    parser.add_argument('--all', action='store_true', help='Scrape all 50 states')
    
    args = parser.parse_args()
    
    scraper = HOAScraper(delay_between_requests=args.delay)
    
    if args.all:
        output_file = scraper.scrape_and_save()
    elif args.states:
        output_file = scraper.scrape_and_save(selected_states=args.states)
    else:
        # Default to Alabama for testing
        print("No states specified. Use --states or --all flag.")
        print("Example: python hoa_scraper_simple.py --states Alabama")
        print("Example: python hoa_scraper_simple.py --all")
        return
    
    if output_file:
        print(f"\nSuccess! Data saved to: {output_file}")
    else:
        print("Scraping failed!")

if __name__ == "__main__":
    main()