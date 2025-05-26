!pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import time

def get_soup(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def scrape_projects():
    base_url = "https://rera.odisha.gov.in"
    headers = {'User-Agent': 'Mozilla/5.0'}
    projects = []
    
    try:
        soup = get_soup(f"{base_url}/projects/project-list", headers)
        table = soup.find('table', {'id': 'example1'})
        
        for row in table.find_all('tr')[1:7]:
            cols = row.find_all('td')
            if len(cols) >= 3:
                project = {
                    'name': cols[1].text.strip(),
                    'rera_no': '',
                    'gst_no': '',
                    'promoter': '',
                    'address': ''
                }
                
                detail_url = base_url + cols[2].find('a')['href']
                detail_soup = get_soup(detail_url, headers)
                
                rera = detail_soup.find('label', string=lambda t: t and 'RERA Regd. No' in t)
                if rera:
                    project['rera_no'] = rera.find_next('div').text.strip()
                
                gst = detail_soup.find('label', string=lambda t: t and 'GST No' in t)
                if gst:
                    project['gst_no'] = gst.find_next('div').text.strip()
                
                promoter_tab = detail_soup.find('a', {'href': '#promoter'})
                if promoter_tab and promoter_tab.get('data-url'):
                    promoter_soup = get_soup(base_url + promoter_tab['data-url'], headers)
                    name = promoter_soup.find('label', string='Company Name')
                    if name:
                        project['promoter'] = name.find_next('div').text.strip()
                    address = promoter_soup.find('label', string='Registered Office Address')
                    if address:
                        project['address'] = address.find_next('div').text.strip()
                
                projects.append(project)
                time.sleep(1)
                
    except Exception as e:
        print(f"Error: {e}")
    
    return projects

if __name__ == "__main__":
    results = scrape_projects()
    for i, p in enumerate(results, 1):
        print(f"\nProject {i}:")
        print(f"Name: {p['name']}")
        print(f"RERA: {p['rera_no']}")
        print(f"GST: {p['gst_no']}")
        print(f"Promoter: {p['promoter']}")
        print(f"Address: {p['address']}")
