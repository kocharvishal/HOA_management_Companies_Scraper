#!/usr/bin/env python3
"""
Simple command-line script to run the HOA scraper without the web interface.
This is useful for running the scraper directly from VS Code terminal.
"""

from scraper import HOAScraper
from config import US_STATES
import argparse
import logging
import os

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('scraper.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main function to run the scraper"""
    parser = argparse.ArgumentParser(description='HOA Management Companies Scraper')
    parser.add_argument('--states', nargs='+', help='Specific states to scrape (e.g., --states Alabama California)')
    parser.add_argument('--delay', type=int, default=2, help='Delay between requests in seconds (default: 2)')
    parser.add_argument('--all', action='store_true', help='Scrape all 50 states')
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Create output directory
    os.makedirs('output', exist_ok=True)
    
    # Initialize scraper
    scraper = HOAScraper(delay_between_requests=args.delay)
    
    # Determine which states to scrape
    if args.all:
        states_to_scrape = None  # Will scrape all states
        logger.info("Starting scraper for all 50 states")
    elif args.states:
        states_to_scrape = args.states
        logger.info(f"Starting scraper for states: {', '.join(states_to_scrape)}")
    else:
        # Default to Alabama for testing
        states_to_scrape = ['Alabama']
        logger.info("No states specified, scraping Alabama as test")
    
    def progress_callback(state, progress, total_companies, errors):
        """Progress callback function"""
        logger.info(f"Progress: {progress}% - Current state: {state} - Companies found: {total_companies}")
        if errors:
            logger.warning(f"Errors encountered: {len(errors)}")
    
    try:
        # Run the scraper
        output_file = scraper.scrape_all_states(
            progress_callback=progress_callback,
            selected_states=states_to_scrape
        )
        
        logger.info("="*50)
        logger.info("SCRAPING COMPLETED SUCCESSFULLY!")
        logger.info(f"Output file: {output_file}")
        logger.info("="*50)
        
        return output_file
        
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        return None

if __name__ == "__main__":
    main()