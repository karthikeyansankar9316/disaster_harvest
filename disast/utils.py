import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Category and severity keywords
category_keywords = {
    "flood": ["flood", "overflow", "inundation"],
    "earthquake": ["earthquake", "tremor", "seismic"],
    "cyclone": ["cyclone", "hurricane", "typhoon"],
    "wildfire": ["wildfire", "forest fire", "bushfire"],
    "drought": ["drought"],
    "storm": ["storm"],
    "wild fires": ["wild fire"],
    "outbreak": ["outbreak", "dzud"],
    "landslides": ["landslides"],
    "volcano": ["volcano"]
}

severity_keywords = {
    "low": ["minor", "low", "small-scale"],
    "medium": ["moderate", "medium", "significant"],
    "high": ["severe", "disastrous", "devastating"],
}

date_k = {
    "jan 2024": ["jan"],
    "feb 2024": ["feb"],
    "mar 2024": ["mar"],
    "apr 2024": ["apr"],
    "may 2024": ["may"],
    "jun 2024": ["jun"],
    "jul 2024": ["jul"],
    "aug 2024": ["aug"],
    "sep 2024": ["sep"],
    "oct 2024": ["oct"],
    "nov 2024": ["nov"],
    "dec 2024": ["dec"]
}


# Scraping logic
def scrape_disaster_data():
    url = "https://reliefweb.int/disasters"  # Replace with the actual target URL
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        disaster_data = []
        
        # Extract disaster details
        articles = soup.find_all('article')  # Replace with the actual tag/structure of the site
        
        for article in articles:
            title = article.find('h3').text.strip().lower() if article.find('h3') else "No title"
            link = article.find('a')['href'] if article.find('a') else '#'
            date_element = article.find('time')  # Replace 'time' with the actual tag for date

            # Parse the date if available
            if date_element:
                date_text = date_element.text.strip()
                try:
                    date = datetime.strptime(date_text, "%d %b %Y").strftime("%Y-%m-%d")  # Adjust format as needed
                except ValueError:
                    date = "Unknown"
            else:
                date = "Unknown"  # Default to "Unknown" if no date is found

            # Determine category and severity
            category = "Unknown"
            severity = "Medium"
            for key, keywords in category_keywords.items():
                if any(keyword in title for keyword in keywords):
                    category = key
                    break
            for level, keywords in severity_keywords.items():
                if any(keyword in title for keyword in keywords):
                    severity = level
                    break
            for level, keywords in date_k.items():
                if any(keyword in title for keyword in keywords):
                    date = level
                    break    
            
            # Append data to the list with default values
            disaster_data.append({
                "title": title.capitalize(),
                "link": f"https://reliefweb.int{link}" if link.startswith("/") else link,
                "category": category if category else "Unknown",  # Default to 'Unknown' if null
                "severity": severity if severity else "Medium",  # Default to 'Medium' if null
                "date": date if date else "Unknown",  # Default to 'Unknown' if null
            })
        
        return disaster_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
