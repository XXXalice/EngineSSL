import os
from flask import Flask, request, send_from_directory, render_template, redirect
from keras.models import Sequential, load_model
from keras.preprocessing.image import img_to_array
from werkzeug.utils import secure_filename

class PredApp:
    def __init__(self, *args):
        self.app = Flask('predict')
        self.classes = args if len(args) != 1 else args[0]
        self.upload_folder = './data/uploads/'
        os.makedirs(self.upload_folder, exist_ok=True)
        self.app.config['UPLOAD_FOLDER'] = self.upload_folder
        self.allow_ext = set(['jpeg', 'jpg', 'png', 'gif'])
        self.port = 3553
        self.host = 'localhost'

    def run(self, auto_startup=False):
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

        @self.app.route('/uploads/<filename>')
        def uploaded_file(filename):
            return send_from_directory(self.app.config['UPLOAD_FOLDER'], filename)

        self.app.run(host='localhost', port=3553)
        if auto_startup:
            self.__startup_browser()



    def __allowed_file(self, fname):
        return '.' in fname and fname.split('.', 1)[1] in self.allow_ext

    def __startup_browser(self, port=3553, host='localhost'):
        from selenium.webdriver import Chrome
        import chromedriver_binary
        driver = Chrome()
        url = 'http://{host}:{port}'.format(host=host, port=port)
        driver.get(url=url)




if __name__ == '__main__':
    print(os.getcwd())
    a = PredApp()
    a.app.debug=True
    a.run(auto_startup=True)
