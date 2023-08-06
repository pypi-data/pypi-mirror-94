from bs4 import BeautifulSoup as bs
import requests
from typing import List
import urllib

from .result import Result
from .error import InvalidCalculation, InvalidPhrase, InvalidLocation

class Google:
	
	def __request(query: str, params: str = ""):
		url = "https://google.com/search?q="+urllib.parse.quote(query)+params
		r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
		return bs(r.text, 'html.parser')

	@classmethod
	def search(self, query: str, is_safe: bool = False) -> List[Result]:
		if is_safe:
			safe = "strict"
		else:
			safe = "off"
		req = self.__request(query, "&safe="+safe)
		res = req.find_all("div", class_="kCrYT")
		reslist = list()
		for i in res:
			if i.a is not None and i.a['href'].startswith("/url"):
				link = urllib.parse.unquote(i.a['href']).split('?q=')[1].split('&sa=')[0]
				children = i.find_all("span", class_="XLloXe AP7Wnd")
				title = i.a.h3.div.text if i.a.h3 is not None else None
				domain = i.a.div.text if i.a.div is not None else None
				kwargs = {
					'link': link,
					'title': title,
					'domain': domain,
				}
				reslist.append(Result(**kwargs))
		return reslist

	@classmethod
	def calculate(self, query: str):
		req = self.__request(query)
		try:
			question = req.find('span', class_="BNeawe tAd8D AP7Wnd").text
			ans = req.find('div', class_="BNeawe iBp4i AP7Wnd").text
		except AttributeError:
			raise InvalidCalculation(query)
		kwargs = {
			'answer': ans,
			'question': question,
		}
		return Result(**kwargs)

	@classmethod
	def define(self, query: str):
		req = self.__request('define '+query)
		try:
			phrase = req.find('div', class_="BNeawe deIvCb AP7Wnd").text
			pronunciation = req.find('div', class_="BNeawe tAd8D AP7Wnd").text
			word_type = req.find('span', class_="r0bn4c rQMQod").text.strip()
			meaning = req.find('div', class_="v9i61e").text
		except AttributeError:
			raise InvalidPhrase(query)
		kwargs = {
			'phrase': phrase,
			'pronun': pronunciation,
			'type': word_type,
			'meaning': meaning,
		}
		return Result(**kwargs)
	
	@classmethod
	def weather(self, query: str):
		req = self.__request('weather '+query)
		try:
			weather = req.find('div', class_="BNeawe tAd8D AP7Wnd").text
			temperature = req.find('div', class_="BNeawe iBp4i AP7Wnd").text
		except AttributeError:
			raise InvalidLocation(query)
		kwargs = {
			'weather': weather,
			'temp': temperature,
		}
		return Result(**kwargs)