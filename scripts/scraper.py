from bs4 import BeautifulSoup
import utilities as utils
import constants


class Scraper:

    def __init__(self):
        self.consecutive_empty_scrapes = 0
        pass

    # Scrape and return the contents of the current page
    def scrape_timetable_page(self, data):
        page = data[0]
        date = data[1]
        soup = BeautifulSoup(page, 'lxml')
        event_lst = []

        # Find and process each 'day' in the timetable
        for day in constants.DAYS:
            column = soup.find(
                id='ctl00_Content_ctlTimetableMain_{}DayCol_Body'.format(day))

            for item in column.find_all(class_='cssClassInnerPanel'):
                event = {
                    'summary': self.get_summary(item),
                    'location': self.get_location(item),
                    'start': {
                        'dateTime': self.get_start_datetime(item, day, date)
                    },
                    'end': {
                        'dateTime': self.get_end_datetime(item, day, date)
                    },
                    'colorId': ''
                }
                event_lst.append(event)
        if not event_lst:
            self.consecutive_empty_scrapes += 1
        else:
            self.consecutive_empty_scrapes = 0
        return event_lst

    def get_summary(self, item):
        unit_code = item.find(class_='cssTtableHeaderPanel').string.strip()
        _type = item.find(class_='cssTtableClsSlotWhat').string
        summary = '{} - {}'.format(unit_code, _type.capitalize())
        return summary

    def get_location(self, item):
        location = item.find(class_='cssTtableClsSlotWhere').string
        return location

    def get_start_datetime(self, item, day, date):
        date = utils.date_from_day_abbr(day, date)
        time = utils.to_24h_string(item.find(class_='cssHiddenStartTm')['value'])
        date_string = utils.to_gcal_datetime(date, time)
        return date_string

    def get_end_datetime(self, item, day, date):
        date = utils.date_from_day_abbr(day, date)
        time = utils.to_24h_string(item.find(class_='cssHiddenEndTm')['value'])
        date_string = utils.to_gcal_datetime(date, time)
        return date_string
