### Scrapper

**Framework: Flask**
**Databases:**
- Unstructured Jobs (NoSQL)
- Structured Jobs (SQL)

**Functionalities:**
- Scrape websites (initially LinkedIn) to get list of unstructured jobs.
- Insert only new jobs into unstructured jobs DB.
- Cronjob every X hours to start scraping.
- Cronjob every X to check active jobs in structured jobs DB.
