import glob
import os
import click
import xmltodict
from loguru import logger


class Diff(object):
    """
    Iff two variables are all Path or are all File, compare them relate.
    """
    def __init__(self, path1: str, path2: str):
        self.path1 = path1
        self.path2 = path2
        pass

    def compare(self):
        document1 = self._read(self.path1)
        document2 = self._read(self.path2)

        if document1 == document2:
            return True
        else:
            return False

    @staticmethod
    def _read(path: str):
        with open(path) as fd:
            return xmltodict.parse(fd.read(), encoding='utf-8')


class Report(object):
    """
    If two folders are not equals, just report folders not equals;
    Iff folders are equal, compare files under folders.
    """
    def __init__(self):
        self.is_file = False
        self.is_equal = False
        self.not_equal_list = []
        pass

    def set_file(self, file: bool):
        self.is_file = file

    def set_equal(self, equal: bool):
        self.is_equal = equal

    def append(self, result):
        self.not_equal_list.append(result)

    def __str__(self):
        output = ''
        if self.is_file:
            output += 'compare single xml.\n'

        if self.is_equal:
            output += 'compare xml files under folder.\n'

        for item in self.not_equal_list:
            path1, path2, result = item
            if not result:
                output += f'not equal, path1={path1}, path2={path2}\n'

        return output


def get(path: str):
    return glob.glob(os.path.join(path, '**', '*.xml'), recursive=True)


@click.command()
@click.option('--path1', prompt=True)
@click.option('--path2', prompt=True)
def diff(path1: str, path2: str):
    """A tool for compare xml files differences."""
    logger.info(f'path1={path1} path2={path2}')

    if os.path.isfile(path1) and os.path.isfile(path2):
        logger.info(f'compare two xml files.')
        r = Report()
        r.set_file(True)
        r.set_equal(False)

        d = Diff(path1, path2)
        r.append((path1, path2, d.compare()))

        logger.info(r)

    elif os.path.isdir(path1) and os.path.isdir(path2):
        logger.info(f'compare xml files under two folder.')

        r = Report()
        r.set_file(False)
        r.set_equal(True)

        path_list_1 = get(path1)
        path_list_2 = get(path2)

        temp = [path.replace(path2, path1) for path in path_list_2]
        if temp != path_list_1:
            logger.warning("folders's tree are not same.")
            return

        for file1, file2 in zip(path_list_1, path_list_2):
            d = Diff(file1, file2)
            r.append((file1, file2, d.compare()))

        logger.info(r)
    else:
        logger.info('arguments are out of exception.')


if __name__ == '__main__':
    diff()
