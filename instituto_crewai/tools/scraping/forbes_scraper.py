from .scrape_website_tool import ScrapeWebsiteTool

class ForbesScraper(ScrapeWebsiteTool):
    def __init__(self):
        super().__init__("https://www.forbes.com/ai/")

    def get_headlines(self):        
        return self.scrape
