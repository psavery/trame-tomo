from pathlib import Path

from paraview import simple


def read_file(filename):
    filename = Path(filename)

    # Use these readers by default if the file extension matches.
    # The values are unary callables that take the file path as an argument.
    default_readers = {
        '.tif': read_tif,
        '.tiff': read_tif,
    }

    if filename.suffix in default_readers:
        return default_readers[filename.suffix](str(filename))

    # If we don't have a default reader, then just try opening it with ParaView
    data = simple.OpenDataFile(str(filename))
    if data is None:
        raise Exception(f'Failed to find a reader for {filename}')

    return data


def read_tif(filename):
    return simple.TIFFSeriesReader(FileNames=[filename])


def paraview_readers(filename):
    # Use this to get a list of ParaView readers that can read the file
    reader_factory = paraview_reader_factory()
    session = simple.servermanager.ActiveConnection.Session
    readers = reader_factory.GetReaders(filename, session)

    results = []
    for i in range(0, readers.GetLength(), 3):
        results.append({
            'group': readers.GetString(i),
            'name': readers.GetString(i + 1),
            'label': readers.GetString(i + 2),
        })

    return results


def paraview_reader_factory():
    reader_factory = simple.servermanager.vtkSMProxyManager.GetProxyManager().GetReaderFactory()

    if reader_factory.GetNumberOfRegisteredPrototypes() == 0:
        reader_factory.UpdateAvailableReaders()

    return reader_factory
