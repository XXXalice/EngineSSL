import os
from time import sleep
from flask import Flask, request, send_from_directory, render_template
from keras.models import Sequential, load_model
from keras.preprocessing.image import img_to_array
from werkzeug.utils import secure_filename
from selenium.webdriver import Chrome
import chromedriver_binary


class PredApp:
    def __init__(self, *args):
        self.app = Flask(__name__)
        self.classes = args if len(args) != 1 else args[0]
        self.upload_folder = './data/uploads/'
        os.makedirs(self.upload_folder, exist_ok=True)
        self.app.config['UPLOAD_FOLDER'] = self.upload_folder
        self.allow_ext = set(['jpeg', 'jpg', 'png', 'gif'])
        self.port = 3553
        self.host = 'localhost'

    def run(self):
        @self.app.route('/test')
        def admin_test():
            return render_template('admin.html')

        @self.app.route('/', methods=['GET', 'POST'])
        def pred():
            if request.method == 'POST':
                img_file = request.files['img_file']
                if img_file and self.__allowed_file(img_file.filename):
                    fname = secure_filename(img_file.filename)
                    img_file.save(os.path.join(self.app.config['UPLOAD_FOLDER'], fname))
                    img_path = './data/uploads/' + fname
                    print(img_path)
                    return render_template('index.html', img_path=img_path)
            else:
                return render_template('index.html')

        @self.app.route('/<filename>')
        def uploaded_file(filename):
            return send_from_directory(self.app.config['UPLOAD_FOLDER'], filename)
        self.__startup_browser(port=self.port, host=self.host)

    def __startup_browser(self, port=3553, host='localhost'):
        try:
            driver = Chrome()
            url = 'http://{host}:{port}/'.format(host=host, port=port)
            driver.get(url)
        except:
            self.app.run(host=host, port=port)
        finally:
            sleep(3)
            driver.refresh()

    def __allowed_file(self, fname):
        return '.' in fname and fname.split('.', 1)[1] in self.allow_ext


if __name__ == '__main__':
    a = PredApp()
    a.app.debug=True
    a.run()
