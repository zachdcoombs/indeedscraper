# a quick little tool to pull jobs listings from indeed.com
# accepts a position title as user input and displays 10 pages worth of results
# returns if the job status is new or updated recently
# also displays position title, company name, rating (if available), and date posted/days active (if available)

from requests_html import HTMLSession
import pandas as pd


s = HTMLSession()

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}

role = input('Position Search: ') # get user input

data = [] # initialize empty list

urls = ['https://www.indeed.com/jobs?q={}'.format(role, x) for x in range(10)] # parse new link using user input

for url in urls:
    r = s.get(url.strip(), headers=header)
    job_content = r.html.find('div.job_seen_beacon') # look for job card on the page--at time of writing each class is correct
    for job in job_content:
        try:
            label = job.find('span.label', first=True).text # status (new/updated/etc)
        except:
            label = ''
        try:
            job_title = job.find('span[title]', first=True).text # position title
        except:
            job_title = ''
        try:
            companyName = job.find('span.companyName', first=True).text # company name
        except:
            companyName = ''
        try:
            rating = job.find('span.ratingNumber span', first=True).text # rating (if available)
        except:
            rating = ''
        try:
            Posted = job.find('span.date', first=True).text.replace('Posted', '') # replace called to clean up spaces at end
        except:
            Posted = ''
        dic = {                           # headers for CSV file, outputting scraped data
            'Status': label,
            'Job Title': job_title,
            'Company Name': companyName,
            'Rating': rating,
            'Posted': Posted
        }

        data.append(dic) # append each result to list

df = pd.DataFrame(data) # export to CSV file
df.to_csv('Jobs.csv', index=False)
print('Done!')











