
from flask import Flask
from streaming.controllers import blueprints
from werkzeug.utils import import_string

app = Flask(__name__, template_folder='templates',
                    static_url_path='/static')

for bp in blueprints:
  mod = import_string('streaming.controllers.%s:mod' % bp)
  app.register_blueprint(mod)
