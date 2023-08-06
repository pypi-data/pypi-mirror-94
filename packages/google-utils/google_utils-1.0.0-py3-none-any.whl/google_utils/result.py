from typing import Optional

class Result:
	def __init__(self, **kwargs):
		'''Results returned from google.com'''
		self.title: Optional[str] = kwargs.get('title')
		self.link: Optional[str] = kwargs.get('link')
		self.domain: Optional[str] = kwargs.get('domain')
		self.answer: Optional[str] = kwargs.get('answer')
		self.question: Optional[str] = kwargs.get('question')
		self.phrase: Optional[str] = kwargs.get('phrase')
		self.pronunciation: Optional[str] = kwargs.get('pronun')
		self.type: Optional[str] = kwargs.get('type')
		self.meaning: Optional[str] = kwargs.get('meaning')
		self.weather: Optional[str] = kwargs.get('weather')
		self.temperature: Optional[str] = kwargs.get('temp')