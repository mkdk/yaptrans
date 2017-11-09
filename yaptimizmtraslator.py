import sublime
import sublime_plugin
import urllib.request
import urllib.request, urllib.error, urllib.parse
import json

class YaptransCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = self.get_selected_text()
        self.make_request(text)

    def get_selected_text(self):
    	text = str(self.view.substr((self.view.sel())[0]))
    	if len(text)!=0:
    	    return text
    
    def representation(self, content):
        self.view.show_popup(content, flags=sublime.HTML, location=-1, max_width=500, on_navigate=print)

    def make_request(self, text):
        if not text:
    	    return 0
        text = urllib.parse.quote(text)
        settings = self.view.settings().get('yandex_api_key')
        if not settings or settings == 'your_api_key_here':
            self.view.settings().set('yandex_api_key', 'your_api_key_here')
            self.representation("no yandex api key was founded! please add a value \"yandex_api_key\" into your preference settings. <a href=https://translate.yandex.ru/developers/keys>https://translate.yandex.ru/developers/key</a>")
            return 0 
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang=ru'.format(settings,text)
        try:
        	conn = urllib.request.urlopen(url)
        except urllib.error.HTTPError as e:
            print(e)
            settings.representation(str(e))
        except urllib.error.URLError as e:
            print('URLError')
            settings.representation('URLError')
        else:
        	data = conn.read()
        	encoding = conn.info().get_content_charset('utf-8')
        	response = json.loads(data.decode(encoding))
        	content = '<i>{}\n</i>\nПереведено сервисом «Яндекс.Переводчик»\n<a href="http://translate.yandex.ru/">http://translate.yandex.ru/</a>'.format(response['text'][0])
        	self.representation(content)
