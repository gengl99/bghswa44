#! /usr/bin/env python3
# coding  : utf-8
# @Author : Jor<jorhelp@qq.com>
# @Date   : Wed Apr 20 00:17:30 HKT 2022
# @Desc   : Webcam vulnerability scanning tool

#=================== 需放置于最开头 ====================
import warnings; warnings.filterwarnings("ignore")
from gevent import monkey; monkey.patch_all(thread=False)
#======================================================

import os
import sys
from multiprocessing import Process

from loguru import logger

from Ingram import get_config
from Ingram import Core
from Ingram.utils import color
from Ingram.utils import common
from Ingram.utils import get_parse
from Ingram.utils import log
from Ingram.utils import logo


def run():
    config = None
    p = None
    try:
        # logo
        for icon, font in zip(*logo):
            print(f"{color.yellow(icon, 'bright')}  {color.magenta(font, 'bright')}")

        # config
        config = get_config(get_parse())
        os.makedirs(config.out_dir, exist_ok=True)
        os.makedirs(os.path.join(config.out_dir, config.snapshots), exist_ok=True)
        if not os.path.isfile(config.in_file):
            print(f"{color.red('the input file')} {color.yellow(config.in_file)} {color.red('does not exists!')}")
            sys.exit()

        # log 配置
        log.config_logger(os.path.join(config.out_dir, config.log), config.debug)

        def _run_core(cfg):
            Core(cfg).run()

        # 任务进程
        p = Process(target=_run_core, args=(config,))
        if common.os_check() == 'windows':
            p.run()
        else:
            p.start()
            p.join()

    except KeyboardInterrupt:
        logger.warning('Ctrl + c was pressed')
        if p is not None:
            p.kill()
        sys.exit()

    except Exception as e:
        logger.error(e)
        if config is not None:
            print(f"{color.red('error occurred, see the')} {color.yellow(config.log)} "
                  f"{color.red('for more information.')}")
        else:
            print(f"{color.red('error occurred before config initialization.')}")
        sys.exit()


if __name__ == '__main__':
    run()
