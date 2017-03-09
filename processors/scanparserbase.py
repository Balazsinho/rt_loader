import struct
import StringIO

import pytesseract
try:
    import Image
except ImportError:
    from PIL import Image


def tiff_header_for_CCITT(width, height, img_size, CCITT_group=4):
    tiff_header_struct = '<' + '2s' + 'h' + 'l' + 'h' + 'hhll' * 8 + 'h'
    return struct.pack(tiff_header_struct,
                       b'II',  # Byte order indication: Little indian
                       42,  # Version number (always 42)
                       8,  # Offset to first IFD
                       8,  # Number of tags in IFD
                       256, 4, 1, width,  # ImageWidth, LONG, 1, width
                       257, 4, 1, height,  # ImageLength, LONG, 1, lenght
                       258, 3, 1, 1,  # BitsPerSample, SHORT, 1, 1
                       259, 3, 1, CCITT_group,  # Compression, SHORT, 1, 4 = CCITT Group 4 fax encoding
                       262, 3, 1, 0,  # Threshholding, SHORT, 1, 0 = WhiteIsZero
                       273, 4, 1, struct.calcsize(tiff_header_struct),  # StripOffsets, LONG, 1, len of header
                       278, 4, 1, height,  # RowsPerStrip, LONG, 1, lenght
                       279, 4, 1, img_size,  # StripByteCounts, LONG, 1, size of image
                       0  # last IFD
                       )


class ScanParserBase(object):

    # Format constants - these will be the extensions
    TIFF = 'tiff'

    # Mapping of how to identify them in a pdf
    IMAGE_MAP = {
        'CCITTFaxDecode': TIFF,
    }

    def __init__(self, logger, debug=False):
        self.logger = logger
        self.debug = debug

    def _lines_between_marks(self, raw, start_mark, end_mark):
        in_obj = False
        lines = []
        for line in raw:
            if line.strip() == start_mark:
                in_obj = True
                continue
            if line.strip() == end_mark:
                in_obj = False
                break
            if in_obj:
                lines.append(line)
        return lines

    def _strip(self, text):
        """
        Strips the "/" and the spaces from a string
        """
        return text.strip().strip('/')

    def _extract_images(self, raw_pdf):

        while raw_pdf:
            current_obj_lines = self._lines_between_marks(raw_pdf, '<<', '>>')
            current_obj = dict([map(self._strip, l.split(' ', 1)) for l in
                                current_obj_lines])
            obj_type = current_obj.get('Filter')
            if obj_type in self.IMAGE_MAP:
                raw_img = ''.join(self._lines_between_marks(raw_pdf, 'stream',
                                                            'endstream'))
                header = tiff_header_for_CCITT(int(current_obj['Width']),
                                               int(current_obj['Height']),
                                               len(raw_img),
                                               4)
                return header + raw_img, self.IMAGE_MAP[obj_type]

        return None

    def extract_ocr(self, raw_file):
        img, _ = self._extract_images(raw_file)
        buff = StringIO.StringIO(img)
        data = pytesseract.image_to_string(Image.open(buff))
        if self.debug:
            print data
        return data, img
