import scrapy
from scrapy import signals

class SopClassSpider(scrapy.Spider):
    name = "SopClassSpider"
    allowed_domains = ["dicom.nema.org"]
    start_urls = [
        "http://dicom.nema.org/dicom/2013/output/chtml/part04/sect_B.5.html"
    ]

    def parse(self, response):
        rows = response.xpath('//div[@class="table-contents"]/table/tbody/tr')

        for row in rows:
            uid = row.xpath('./td[2]/p/text()').get()
            url = response.urljoin(row.xpath('./td[3]/p/a/@href').extract_first())

            yield scrapy.Request(url, callback=self._parse_sop_class, cb_kwargs=dict(sop_class_uid=uid))

    def _parse_sop_class(self, response, sop_class_uid):
        rows = response.xpath('//div[@class="table-contents"]/table/tbody/tr')

        modules = []

        for row in rows:
            rowspan = int(row.xpath('./td[1]/@rowspan').extract_first())
            columns = len(row.xpath('./td'))
            if columns > 3:
                modules.append(row.xpath('./td[3]/p/a/text()').extract_first())
            else:
                modules.append(row.xpath('./td[2]/p/a/text()').extract_first())

        return {'uid': sop_class_uid, 'modules': modules}
