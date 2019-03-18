# -*- coding: utf-8 -*-
import sqlite3
from contextlib import closing
import scrapy


class Sqlite3Pipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('demo.db'))

    def __init__(self, dbpath):
        self.conn = sqlite3.connect(dbpath)

    def process_item(self, item, spider):
        with closing(self.conn.cursor()) as cur:
            cur.execute(
                '''
                INSERT OR IGNORE
                INTO data (country_id, indicator_id, period_id, datetime, value, price)
                VALUES (
                    (SELECT country_id FROM country WHERE name = ?),
                    (SELECT indicator_id FROM indicator WHERE name = ?),
                    (SELECT period_id FROM period WHERE name = ?),
                    strftime('%s', ?),
                    ?,
                    ?
                );
                ''',
                (item['country'], item['indicator'], item['period'],
                 item['datetime'].isoformat(), item['value'], item['price'])
            )
            return item


    def close_spider(self, spider):
        strTemplate = 'Last seven days ending on {1} has a total Volume of consumption {2} with sum of prices {3}. The biggest consumption was on {4}. Compared to last week when total Volume was {5}.'

        with closing(self.conn.cursor()) as cur:
            cur.execute(
                ''' -- 1st sentence 1,2,3
                select price, value, datetime, period from data;
                --2nd Not finished 4
                select sum(price), (value) from data where group by datetime ;
                --3 Not finishe6
                select 
                '''
