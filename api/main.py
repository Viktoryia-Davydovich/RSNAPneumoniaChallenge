from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from predict_handler import PredictHandler


class RunHandler(RequestHandler):
    def get(self):
        self.write("Running")


def make_app():
    handlers = [("/", RunHandler), ("/predict", PredictHandler)]
    return Application(handlers)


if __name__ == '__main__':
    app = make_app()
    app.listen(8000)
    IOLoop.instance().start()
