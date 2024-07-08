# Scrapy settings for your project
BOT_NAME = 'real_estate'
SPIDER_MODULES = ['real_estate.spiders']
NEWSPIDER_MODULE = 'real_estate.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure item pipelines
ITEM_PIPELINES = {
   'real_estate.pipelines.RealEstatePipeline': 300,
}
