from .scrape_website_tool import ScrapeWebsiteTool

class AINewScraper(ScrapeWebsiteTool):
    def __init__(self):
        super().__init__("https://www.artificialintelligence-news.com/")

    def get_headlines(self):
        return self.scrape
