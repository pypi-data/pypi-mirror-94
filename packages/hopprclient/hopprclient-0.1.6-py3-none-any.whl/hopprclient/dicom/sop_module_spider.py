import scrapy

class SopModuleSpider(scrapy.Spider):
    name = "SopModuleSpider"
    allowed_domains = ["dicom.nema.org"]
    start_urls = [
        "http://dicom.nema.org/dicom/2013/output/chtml/part03/sect_C.7.html"
    ]

    def parse(self, response):
        sections = response.xpath('//div[@class="section"]')

        for section in sections:
            module_id = section.xpath('./div[@class="titlepage"]/div/div/h4/text()').extract()

            if len(module_id) == 0:
                continue

            module_id = module_id[1].split('\xa0')[0]
            
            rows = section.xpath('./div[@class="table"]/div/table/tbody/tr')

            for row in rows:
                columns = len(row.xpath('./td'))
                if columns == 2:
                    # There is a lookup link
                    url = response.urljoin(row.xpath('./td[1]/p/span/a/@href').extract_first())
                    yield scrapy.Request(url, callback=self._parse_lookup, cb_kwargs=dict(module_id=module_id))

                else:
                    tag = row.xpath('./td[2]/p/text()').extract_first()
                    tagType = row.xpath('./td[3]/p/text()').extract_first()
            
                    yield {'module': module_id, 'tag': tag, 'type': tagType}

    def _parse_lookup(self, response, module_id):
        rows = response.xpath('./div[@class="table-contents"]/table/tbody/tr')
        
        for row in rows:
            columns = len(row.xpath('./td'))
            if columns == 2:
                # There is a lookup link
                url = response.urljoin(row.xpath('./td[1]/p/span/a/@href').extract_first())
                yield scrapy.Request(url, callback=self._parse_lookup, cb_kwargs=dict(module_id=module_id))

            else:
                tag = row.xpath('./td[2]/p/text()').extract_first()
                tagType = row.xpath('./td[3]/p/text()').extract_first()

                yield {'module': module_id, 'tag': tag, 'type': tagType}