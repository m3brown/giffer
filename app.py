from flask_api import FlaskAPI, exceptions
from flask import request, send_file
from gif_factory import GifFactory
from fileremover import FileRemover
import giphy

app = FlaskAPI(__name__)
factory = GifFactory()
file_remover = FileRemover()

@app.route('/', methods = ['GET', 'POST'])
def giffer():
    if request.method == 'POST':
        data = request.data
        if 'gif' in data and 'search' in data:
            raise exceptions.ParseError
        if 'gif' not in data and 'search' not in data:
            raise exceptions.ParseError

        if 'search' in data:
            if 'search_type' in data and data['search_type'] == 'translate':
                data['gif'] = giphy.translate(data['search'])
            else:
                data['gif'] = giphy.search(data['search'])
            data.pop('search')
            data.pop('search_type', None)

        # A bug in moviepy requires ver_align and hor_align to be string, not unicode
        # https://github.com/Zulko/moviepy/issues/293
        for key in ['hor_align', 'ver_align']:
            if key in data and type(data[key]) == unicode:
                data[key] = str(data[key])

        gif_file = factory.create(**data)
        resp = send_file(gif_file)
        # delete the file after it's sent
        # http://stackoverflow.com/questions/13344538/how-to-clean-up-temporary-file-used-with-send-file
        file_remover.cleanup_once_done(resp, gif_file)
        return resp
    else:
        return print_guide()

def print_guide():
    commands = {}
    commands['text'] = 'The text to put on the gif'
    commands['gif'] = 'The original gif url'
    commands['search'] = 'search giphy for an image'
    commands['search_type'] = "giphy search type, 'search' or 'translate' [search]"
    commands['hor_align'] = 'Horizontal alignment [center]'
    commands['ver_align'] = 'Vertical alignment [top]'
    commands['text_height'] = 'Height of text as percentage of image height [20]'
    commands['text_width'] = 'Maximum width of text as percentage of image width [60]'
    samples = []
    samples.append({"text": "time for work", "gif": "http://25.media.tumblr.com/tumblr_m810e8Cbd41ql4mgjo1_500.gif"})
    samples.append({"text": "hey guys", "search": "elf wave"})
    return {"Command Guide": commands, "Samples": samples}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
