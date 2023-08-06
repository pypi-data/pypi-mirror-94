from autosegl3 import GenID


def test_genid():
    args = {
        'root_dir': '/Volumes/USB_SECURE1/data/radiomics/projects/deepseg/data/mega/processed',
        'output_dir': '/Volumes/USB_SECURE1/data/radiomics/projects/deepseg/data/mega/renamed',
        'include_types': 'dicom, tag',
        'prefix': 'P',
        'nr_digits': 4,
        'log_dir': '.',
    }
    x = GenID(args)
    x.execute()
