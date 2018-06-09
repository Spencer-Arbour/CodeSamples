import logging
import os
import pytest
import shutil

from DirectoryWalker import DirectoryWalker
from FileFinder import FileFinder


@pytest.fixture(autouse=True, scope="class")
def setup(request):
    logging.disable(logging.CRITICAL)

    def teardown():
        test_dir = "test"
        if os.path.isdir(test_dir):
            shutil.rmtree(test_dir)

    request.addfinalizer(teardown)


class TestVFileFinder(object):
    vid_ext = ["avi", "wmv", "mp4", "mkv"]

    def test_video_finder_asked_to_search_nonexistent_dir(self, monkeypatch):
        monkeypatch.setattr(os.path, 'isdir', lambda x: False)
        with pytest.raises(NotADirectoryError):
            FileFinder().find_all_files_in_directory("fake_directory")

    def test_video_finder_finds_right_files(self, monkeypatch):
        def mock_directory(walk_directory):
            yield('/Users/admin/downloads', [], [])
            yield('/Users/admin/downloads/fooDir', [],
                  ['bar.txt', 'fooBar.avi'])
            yield('/Users/admin/downloads/binDir', [],
                  ['boo.wmv', 'big.txt'])
            yield('/Users/admin/downloads/tooDir', [],
                  ['Big.mp4', 'another.txt'])
            yield('/Users/admin/downloads/somDir', [],
                  ['som.mkv', 'som.txt', 'som.srt'])
            yield('/Users/admin/downloads/pinDir', ['Sample'],
                  ['pin1.mkv', 'pin1.mkv', 'pin1.mkv',
                  'pin1.mkv', 'pin1.mkv', 'pin1.mkv',
                  'pin1.mkv', 'pin1.mkv',])

        monkeypatch.setattr(os.path, 'isdir', lambda x: True)
        monkeypatch.setattr(DirectoryWalker, 'walk_directory', mock_directory)

        video_finder = FileFinder().find_all_files_in_directory("directory")
        video_files = video_finder.get_files_of_specific_types(self.vid_ext)
        assert len(video_files) == 12
