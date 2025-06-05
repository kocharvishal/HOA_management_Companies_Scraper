# HOA Management Companies Scraper

A comprehensive Python web scraper for extracting HOA management company data from all US states on hoa-usa.com.

## Features

- **Complete Data Extraction**: Scrapes both "Recommended" and "Regular" HOA management companies
- **Web Interface**: User-friendly Flask web application with real-time progress tracking
- **Data Processing**: Automatic data cleaning and validation
- **CSV Export**: Clean, structured data export with proper formatting
- **State Selection**: Option to scrape specific states or all 50 states
- **Progress Monitoring**: Real-time status updates and error tracking

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project files**
   ```bash
   mkdir hoa-scraper
   cd hoa-scraper
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install flask beautifulsoup4 requests pandas lxml trafilatura
   ```

4. **Create required directories**
   ```bash
   mkdir static templates output
   ```

5. **Copy all the provided Python files to your project directory**

## Project Structure

```
hoa-scraper/
├── app.py              # Main Flask application
├── scraper.py          # Core scraping logic
├── data_processor.py   # Data cleaning and processing
├── config.py           # Configuration settings
├── utils.py            # Utility functions
├── templates/
│   └── index.html      # Web interface template
├── static/
│   └── style.css       # CSS styling
└── output/             # Generated CSV files
```

## Usage

### Running the Application

1. **Start the web application**
   ```bash
   python app.py
   ```

2. **Open your web browser and go to:**
   ```
   http://localhost:5000
   ```

3. **Using the Web Interface:**
   - Set delay between requests (recommended: 2-3 seconds)
   - Select specific states or leave blank for all states
   - Click "Start Scraping"
   - Monitor progress in real-time
   - Download CSV file when complete

### Command Line Usage

You can also run the scraper directly from command line:

```python
from scraper import HOAScraper

# Create scraper instance
scraper = HOAScraper(delay_between_requests=2)

# Scrape specific states
output_file = scraper.scrape_all_states(selected_states=['Alabama', 'California'])

# Scrape all states
output_file = scraper.scrape_all_states()

print(f"Data saved to: {output_file}")
```

## Configuration

You can modify settings in `config.py`:

- `DEFAULT_DELAY`: Time between requests (seconds)
- `MAX_RETRIES`: Number of retry attempts for failed requests
- `TIMEOUT`: Request timeout (seconds)
- `US_STATES`: List of states to scrape

## Output Data

The scraper generates CSV files with the following columns:

- `name`: Company name
- `state`: State where company operates
- `section_type`: "recommended" or "regular"
- `phone`: Phone number (formatted)
- `email`: Email address
- `website`: Company website URL
- `service_area`: Geographic service area
- `address`: Company address
- `extracted_city`: City extracted from address
- `extracted_state`: State extracted from address
- `description`: Company description (for recommended companies)
- `source_url`: Original webpage URL

## Features Explained

### Data Sections Captured

1. **Recommended Companies**: Detailed listings with rich information including descriptions, emails, and complete contact details
2. **Regular Companies**: Basic listings with company name, phone, and service area

### Data Processing

- Phone number formatting to standard US format
- Email validation and cleaning
- Website URL validation
- Duplicate removal based on company name and state
- Text cleaning and normalization

### Error Handling

- Automatic retry for failed requests
- Comprehensive error logging
- Graceful handling of missing data
- Progress tracking with error reporting

## Troubleshooting

### Common Issues

1. **Connection Errors**: Increase delay between requests if you get blocked
2. **Empty Results**: Check internet connection and website availability
3. **Permission Errors**: Ensure write permissions for output directory

### Performance Tips

- Use 2-3 second delays to avoid being blocked
- Run during off-peak hours for better reliability
- Monitor logs for any recurring errors

## Legal Considerations

- This scraper is for educational and research purposes
- Respect the website's robots.txt and terms of service
- Use reasonable delays between requests
- Don't overload the target server

## Support

If you encounter issues:

1. Check the log files for detailed error messages
2. Ensure all dependencies are properly installed
3. Verify internet connectivity
4. Try running with fewer states first to test

## Updates and Maintenance

The scraper may need updates if the target website structure changes. Monitor the logs for extraction errors and update the selectors accordingly.
