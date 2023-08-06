import tempfile
import pydicom

class DicomTagDeid:

    def __init__(self, client_id):
        self._client_id = client_id

    def parse(self, dicom_file):
        self._values = {}
    
    def _remove(self, dicom, value, field, item):
        self._add_field(field, self._remove_converter)
        return True
    
    def _clear(self, dicom, value, field, item):
        return self._add_field(field, self._clear_converter)

    def _add_field(self, field, converter):
        if field.element.VR == 'SQ':
            # Sequence
            converted = []
            for v in field.element._value:
                c = converter(v)
                self._add_value(v, c)
                converted.append(c)
            return converted
        else:
            c = converter(field.element._value)
            self._add_value(field.element._value, c)
            return c
    
    def _add_value(self, value, converted):
        self._values[value] = converted

    def _remove_converter(self, value):
        return ''

    def _clear_converter(self, value):
        pass
