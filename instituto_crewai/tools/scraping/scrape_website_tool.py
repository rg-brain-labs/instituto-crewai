from crewai_tools.tools.scrape_website_tool.scrape_website_tool import ScrapeWebsiteTool

class ScrapeWebsiteTool:
    def __init__(self, website_url):
        self.website_url = website_url

    def scrape(self):
        return ScrapeWebsiteTool(self.website_url)     
