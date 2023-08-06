import pathlib
import os
from codecs import BOM_UTF8, BOM_LE, BOM_BE

_Parent = pathlib.WindowsPath if os.name == 'nt' else pathlib.PosixPath
BOM_CODE = {
    BOM_UTF8: 'utf_8',
    BOM_LE: 'utf_16_le',
    BOM_BE: 'utf_16_be',
}
DEFAULT_CODES = 'utf8', 'gbk', 'utf16', 'big5'


class Path(_Parent):
    __slots__ = ()

    def __new__(cls,
                path='.',
                *args,
                **kwargs):
        if isinstance(path, str):

            # Support the beginning of user directory.
            if path.startswith('~'):
                path = os.path.expanduser(path)

            # Support environment variable escape.
            elif path.startswith('%'):
                path = os.path.expandvars(path)
        return super().__new__(cls, path, *args, **kwargs)

    def read(self,
             *args,
             **kwargs):
        """
        Read the file with the specified parameters.
        >>> file=Path('__cases/example.txt')
        >>> file.read()[0]
        '1'
        """
        with self.open(*args, **kwargs)as fn:
            return fn.read()

    def ensure(self,
               parents=True):
        """
        Make sure the directory exists. If the directory does not exist, create it directly.
        >>> file=Path('__cases/tmp/')
        >>> file.ensure()
        True
        """
        if not self.exists():
            return self.mkdir(parents=parents)
        else:
            return True

    @property
    def text(self):
        """
        Reads the file and returns a string.
        >>> file=Path('__cases/example.txt')
        >>> file.read()[0]
        '1'
        """
        rb = self.read('rb')
        for k in BOM_CODE:
            if k == rb[:len(k)]:
                return rb[len(k):].decode(BOM_CODE[k])
        for encoding in DEFAULT_CODES:
            try:
                return rb.decode(encoding)
            except:
                pass
        raise Exception('Decode error.')

    @text.setter
    def text(self,
             text):
        """
        Write text into file.
        """
        self.write(text=text)

    @property
    def lines(self):
        """
        Read file by line.
        >>> file=Path('__cases/example.txt')
        >>> len(file.lines) == 9
        True
        """
        return self.text.splitlines()

    @lines.setter
    def lines(self,
              lines):
        """
        Write file by lines.
        """
        self.write(*lines)

    def write(self,
              *lines,
              text=None,
              data=None,
              encoding='utf8',
              parents=False):
        """
        Write file, you can write by line, by text, or directly write data.
        """
        if parents:
            self.parent.ensure()
        if lines:
            text = "\n".join(lines)
        if text:
            data = text.encode(encoding)
        if data:
            with self.open('wb')as fn:
                fn.write(data)

    @property
    def l_suffix(self):
        """
        Returns the lowercase extension.
        >>> file =  Path('__cases/example.txt')
        >>> file.l_suffix
        '.txt'
        """
        return self.suffix.lower()

    @property
    def p_name(self):
        """
        Returns a file name without an extension.
         >>> file =  Path('__cases/example.txt')
         >>> file.p_name
         'example'
        """
        return self.with_suffix("").name

    def rm_tree(self):
        """
        Delete entire directory.
        """
        import shutil
        shutil.rmtree(str(self))
