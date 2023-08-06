import logging
import subprocess
from datetime import datetime
from pathlib import Path
from pilapse.scheduler import PeriodicThread

logger = logging.getLogger('imageSaver')


class ImageSaver():
    def __init__(self, args):
        self.path = args.path
        self.name = args.name
        self.period = args.period
        self.raspistill_args = args.raspistill_args

    def save_image(self):
        t = datetime.now()
        path = Path(self.path).expanduser().joinpath(
            t.strftime(self.name)).absolute()
        cmd = ['raspistill', *self.raspistill_args.split(), '-o', str(path)]
        logger.debug(' '.join(cmd))
        try:
            out = subprocess.run(cmd, capture_output=True, text=True)
            if out.returncode != 0:
                logger.error("raspistill returned non-zero result")
                logger.error(out.stdout)
                logger.error(out.stderr)
        except Exception as e:
            logger.error('Cannot save file ({}): {}'.format(path, e))

    def start(self):
        logger.info('Saving images to {} with period of {}s'.format(
            self.path, self.period))
        pt = PeriodicThread(
            self.save_image, period=self.period, name='imageSaver')
        pt.start()
        return pt
