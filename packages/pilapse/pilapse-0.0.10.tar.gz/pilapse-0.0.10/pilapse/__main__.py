import os
import sys
import logging
import argparse
from pilapse.server import start_server
from pilapse.image_saver import ImageSaver

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def run():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8080, type=int,
                        help="HTTP server listen port")
    parser.add_argument("--path", default="./",
                        help="Directory to store images")
    parser.add_argument(
        "--name", default="img-%Y-%m-%d_%H%M%S.jpg", help="Image file name template")
    parser.add_argument("--period", default=60, type=int,
                        help="Timelapse frame period")
    parser.add_argument("--raspistill-args", default="-w 1920 -h 1080",
                        help="Extra arguments to raspistill")
    args = parser.parse_args()
    image_saver = ImageSaver(args)
    iss = image_saver.start()
    try:
        start_server(port=args.port, path=args.path)
    except KeyboardInterrupt as e:
        print("\nGot", type(e).__name__, 'exiting...')
        iss.cancel()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


if __name__ == '__main__':
    run()
