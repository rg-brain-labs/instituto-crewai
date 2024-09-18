from crewai_tools.tools.scrape_website_tool.scrape_website_tool import ScrapeWebsiteTool

class WebsiteScreperTool:
    def __init__(self, website_url):
        self.website_url = website_url

    def create_scraper_tool(self):
        return ScrapeWebsiteTool(self.website_url)     
