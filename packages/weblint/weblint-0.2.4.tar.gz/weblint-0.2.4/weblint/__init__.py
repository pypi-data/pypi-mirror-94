import scrapy
from scrapy.crawler import Crawler
from scrapy.exceptions import CloseSpider, UsageError
from scrapy.commands.runspider import Command as RunSpiderCommand
from scrapy.exceptions import UsageError


class Command(RunSpiderCommand):
    requires_project = False
    default_settings = {
        "SPIDER_LOADER_WARN_ONLY": True,
        "OPENGRAPH": False,
        "DISQUS": False,
    }

    def syntax(self):
        return "[options] <url>"

    def short_desc(self):
        return "Run a self-contained spider (without creating a project)"

    def long_desc(self):
        return "Run the spider defined in the given file"

    def run(self, args, opts):
        if len(args) != 1:
            raise UsageError("Please pass one website URL as argument")
        site = args[0]
        crawler = Crawler(Spider)
        self.crawler_process.crawl(
            crawler,
            site=site,
            opengraph=self.settings["OPENGRAPH"],
            disqus=self.settings["DISQUS"],
            **opts.spargs,
        )
        self.crawler_process.start()

        if self.crawler_process.bootstrap_failed:
            self.exitcode = 1

        exception_count = crawler.stats.get_value("webcheck_errors")
        if exception_count:
            print("FAILED: See errors above")
            self.exitcode = 1
        else:
            print("SUCCESS")


class Spider(scrapy.Spider):
    name = "webcheck-spider"
    handle_httpstatus_list = [404, 500]

    def __init__(self, site, *args, opengraph=False, disqus=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [site]
        self.DOMAIN = site.split("//")[1]
        self.check_opengraph = opengraph
        self.check_disqus = disqus

    def parse(self, response, **kwargs):
        if response.status in (404, 500):
            self.crawler.stats.inc_value("webcheck_errors")
            raise CloseSpider(
                f"Got {response.status} on {response.meta['prev_url']} for {response.url}"
            )

        if self.DOMAIN in response.url:
            if self.check_opengraph or self.check_disqus:
                if not response.xpath("//meta[@property='og:title']"):
                    self.crawler.stats.inc_value("webcheck_errors")
                    prev = response.meta.get("prev_url", "first visit")
                    raise CloseSpider(
                        f"Cannot find og:title meta tag on {response.url} (reached from {prev})"
                    )
                page_type = response.xpath(
                    "//meta[@property='og:type']/@content"
                )[0].extract()
                if self.check_disqus and page_type == "article":
                    if not response.css("div#disqus_thread"):
                        self.crawler.stats.inc_value("webcheck_errors")
                        raise CloseSpider(
                            f"Page at {response.url} appears to be og:type=article but does not have Disqus code"
                        )

            for link in response.css("a"):
                href = link.xpath("@href").extract()
                text = link.xpath("text()").extract()
                if href:  # maybe should show an error if no href
                    yield response.follow(
                        link,
                        self.parse,
                        meta={
                            "prev_link_text": text,
                            "prev_href": href,
                            "prev_url": response.url,
                        },
                    )
