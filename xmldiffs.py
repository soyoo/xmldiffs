import glob
import os

import click
import xmltodict
from loguru import logger


class Diff(object):
    """
    Iff two XML files are exist, compare their contents if is equal.
    """

    def __init__(self, filename1: str, filename2: str):
        self.filename1 = filename1
        self.filename2 = filename2
        pass

    def compare(self):
        document1 = self._read(self.filename1)
        document2 = self._read(self.filename2)

        if document1 == document2:
            return True
        else:
            return False

    @staticmethod
    def _read(path: str):
        with open(path, encoding='utf-8') as fd:
            try:
                return xmltodict.parse(fd.read(), encoding='utf-8')
            except Exception as error:
                logger.warning(f'file path={path}, exception={str(error)}')


class Report(object):
    """
    If two folders are not equals, just report folders not equals;
    Iff folders are equal, compare XML files under folders.
    """
    def __init__(self):
        self.is_file = False
        self.is_equal = False
        self.compare_list = []
        pass

    def set_file(self, file: bool):
        self.is_file = file

    def set_equal(self, equal: bool):
        self.is_equal = equal

    def append(self, result):
        self.compare_list.append(result)

    def result(self):
        outputs = []
        if self.is_file:
            outputs.append('Compare two XML files.')

        if self.is_equal:
            outputs.append('Compare XML files under the folder.')

        not_equal_list = [x for x in self.compare_list if not x[2]]

        if len(not_equal_list) == 0:
            outputs.append('XML files are almost same.')

        for item in not_equal_list:
            path1, path2, result = item
            outputs.append(f'not equal, path1={path1}, path2={path2}')

        for item in outputs:
            logger.info(item)


def scan(path: str):
    return glob.glob(os.path.join(path, '**', '*.xml'), recursive=True)


@click.command()
@click.option('--path1', prompt=True, type=click.Path(exists=True))
@click.option('--path2', prompt=True, type=click.Path(exists=True))
def diff(path1: str, path2: str):
    """A tool for compare XML files differences."""

    if os.path.isfile(path1) and os.path.isfile(path2):
        report = Report()
        report.set_file(True)
        report.set_equal(False)

        d = Diff(path1, path2)
        report.append((path1, path2, d.compare()))

        report.result()

    elif os.path.isdir(path1) and os.path.isdir(path2):
        report = Report()
        report.set_file(False)
        report.set_equal(True)

        path_list_1 = scan(path1)
        path_list_2 = scan(path2)

        temp = [path.replace(path2, path1) for path in path_list_2]
        if temp != path_list_1:
            logger.warning("folders's tree are not same, please check.")
            return

        for file1, file2 in zip(path_list_1, path_list_2):
            d = Diff(file1, file2)
            report.append((file1, file2, d.compare()))

        report.result()
    else:
        logger.info('All parameters must be folder path or file path.')


if __name__ == '__main__':
    diff()
