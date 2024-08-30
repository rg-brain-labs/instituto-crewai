from .website_scraper_tool import WebsiteScreperTool

class ForbesScraper(WebsiteScreperTool):
    def __init__(self):
        super().__init__("https://www.forbes.com/ai/")