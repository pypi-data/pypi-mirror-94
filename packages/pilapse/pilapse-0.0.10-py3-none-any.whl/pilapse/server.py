import glob
import http.server
import io
import logging
import os
import pathlib
import socketserver
import shutil
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw
from pilapse.ip_finder import get_local_ip

PATH = '.'
logger = logging.getLogger('server')


class H(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        logger.debug("{}: {} - {}\n".format(self.command,
                                            self.client_address, self.path))
        if self.path == '/last.jpg':
            self.serve_latest_image()
        else:
            self.serve_index()

    def serve_index(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        f = open(pathlib.Path(__file__).parent.joinpath(
            'data/index.html').absolute(), 'rb')
        try:
            shutil.copyfileobj(f, self.wfile)
        finally:
            f.close()

    def serve_latest_image(self):
        byteIO = io.BytesIO()
        path = self.get_latest_image_path()
        image = self.get_image(path)
        image.resize((960, 540))
        image.save(byteIO, format='JPEG')
        self.send_response(200, "")
        self.send_header("'Content-Length'", str(len(byteIO.getvalue())))
        self.send_header("Content-Type", "image/jpeg")
        self.end_headers()
        self.wfile.write(byteIO.getvalue())

    def get_latest_image_path(self):
        list_of_files = glob.glob(os.path.join(PATH, '*'))
        latest_file = max(list_of_files, key=os.path.getctime)
        logger.debug("latest image: {}".format(latest_file))
        return latest_file

    def get_file_mtime(self, path):
        fname = pathlib.Path(path)
        assert fname.exists(), f'No such file: {fname}'
        ts = fname.stat().st_mtime
        logger.debug(datetime.fromtimestamp(ts))
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

    def get_image(self, path):
        font = ImageFont.truetype(str(pathlib.Path(__file__).parent.joinpath(
            'data/Product Sans Regular.ttf').absolute()), 25)
        with Image.open(path) as img:
            draw = ImageDraw.Draw(img)
            text = self.get_file_mtime(path)
            draw.text((0, 0), text, (255, 255, 255), font=font)
            return img


def start_server(port, path):
    with socketserver.TCPServer(("", port), H) as httpd:
        global PATH
        PATH = pathlib.Path(path).expanduser().absolute()
        ip = get_local_ip()
        logger.info(
            "Serving images via http://{}:{}/ from {}".format(ip, port, PATH))
        httpd.serve_forever()


if __name__ == '__main__':
    start_server(8080, '/tmp/images/')
