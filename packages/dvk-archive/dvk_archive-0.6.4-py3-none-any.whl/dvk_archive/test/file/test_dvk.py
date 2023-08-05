#!/usr/bin/env python3

from os import remove, pardir, stat
from os.path import abspath, basename, exists, join
from dvk_archive.main.file.dvk import Dvk
from dvk_archive.test.temp_dir import get_test_dir


def test_can_write():
    """
    Tests the can_write method.
    """
    # TEST VALID DVK THAT CAN BE WRITTEN
    test_dir = get_test_dir()
    dvk = Dvk()
    dvk.set_dvk_file(abspath(join(test_dir, "write.dvk")))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    assert dvk.can_write()
    # TEST WITH NO DVK FILE
    dvk.set_dvk_file(None)
    assert not dvk.can_write()
    # TEST DVK FILE WITHOUT EXISTING PARENT DIRECTORY
    dvk.set_dvk_file("/non-existant/file.dvk")
    assert not dvk.can_write()
    # TEST WITH NO DVK ID
    dvk.set_dvk_file(abspath(join(test_dir, "write.dvk")))
    dvk.set_dvk_id(None)
    assert not dvk.can_write()
    # TEST WITH NO TITLE
    dvk.set_dvk_id("id123")
    dvk.set_title(None)
    assert not dvk.can_write()
    # TEST WITH NO ARTIST
    dvk.set_title("Title")
    dvk.set_artist(None)
    assert not dvk.can_write()
    # TEST WITH NO PAGE URL
    dvk.set_artist("artist")
    dvk.set_page_url(None)
    assert not dvk.can_write()
    # TEST WITH NO MEDIA FILE
    dvk.set_page_url("/url/")
    dvk.set_media_file("")
    assert not dvk.can_write()
    # TEST VALID WRITABLE DVK
    dvk.set_media_file("file.txt")
    assert dvk.can_write()

def test_get_set_dvk_file():
    """
    Tests the get_dvk_file and set_dvk_file methods.
    """
    # TEST EMPTY DVK FILE WITH CONSTRUCTOR
    dvk = Dvk();
    assert dvk.get_dvk_file() is None
    # TEST GETTING AND SETTING DVK FILE
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "blah.dvk"))
    assert basename(dvk.get_dvk_file()) == "blah.dvk"
    assert abspath(join(dvk.get_dvk_file(), pardir)) == test_dir
    # TEST SETTING DVK FILE TO NULL
    dvk.set_dvk_file(None)
    assert dvk.get_dvk_file() is None
    # WRITE DVK FILE
    dvk.set_dvk_file(join(test_dir, "new.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url")
    dvk.set_media_file("file.txt")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert basename(read_dvk.get_dvk_file()) == "new.dvk"
    assert abspath(join(read_dvk.get_dvk_file(), pardir)) == test_dir

def test_get_set_dvk_id():
    """
    Tests the get_dvk_id and set_dvk_id methods.
    """
    # TEST EMPTY ID WITH CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_dvk_file() is None
    # TEST GETTING AND SETTING DVK ID
    dvk.set_dvk_id("id1234")
    assert dvk.get_dvk_id() == "ID1234"
    dvk.set_dvk_id("TST128-J")
    assert dvk.get_dvk_id() == "TST128-J"
    # TEST INVALID IDS
    dvk.set_dvk_id(None)
    assert dvk.get_dvk_id() is None
    dvk.set_dvk_id("")
    assert dvk.get_dvk_id() is None
    # WRITE DVK FILE
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "id_dvk.dvk"))
    dvk.set_dvk_id("WRITE456")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING DVK ID
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_dvk_id() == "WRITE456"

def test_get_set_title():
    """
    Tests the get_title and set_title methods.
    """
    # TEST EMPTY TITLE FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_title() is None
    # TEST GETTING AND SETTING TITLE
    dvk.set_title("Test Title")
    assert dvk.get_title() == "Test Title"
    dvk.set_title(None)
    assert dvk.get_title() is None
    dvk.set_title("")
    assert dvk.get_title() == ""
    # WRITE DVK
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "ttl_dvk.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title #2")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING TITLE FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_title() == "Title #2"

def test_get_set_artists():
    """
    Tests the get_artists, set_artist and set_artists methods.
    """
    # TEST EMPTY ARTISTS FROM CONSTRUCTOR
    dvk = Dvk()
    assert len(dvk.get_artists()) == 0
    # TEST GETTING AND SETTING SINGLE ARTIST
    dvk.set_artist("Artist Person")
    assert len(dvk.get_artists()) == 1
    assert dvk.get_artists()[0] == "Artist Person"
    dvk.set_artist("")
    assert len(dvk.get_artists()) == 1
    assert dvk.get_artists()[0] == ""
    # TEST GETTING AND SETTING MULTIPLE ARTISTS
    artists = ["artist10"]
    artists.append("artist10")
    artists.append("")
    artists.append(None)
    artists.append("artist1")
    artists.append("test1.0.20-stuff")
    artists.append("test10.0.0-stuff")
    dvk.set_artists(artists)
    assert len(dvk.get_artists()) == 5
    assert dvk.get_artists()[0] == ""
    assert dvk.get_artists()[1] == "artist1"
    assert dvk.get_artists()[2] == "artist10"
    assert dvk.get_artists()[3] == "test1.0.20-stuff"
    assert dvk.get_artists()[4] == "test10.0.0-stuff"
    # TEST SETTING INVALID ARTIST VALUES
    dvk.set_artist(None)
    assert len(dvk.get_artists()) == 0
    dvk.set_artists(None)
    assert len(dvk.get_artists()) == 0
    # WRITE DVK
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "artist.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    artists = ["Person"]
    artists.append("artist")
    dvk.set_artists(artists)
    dvk.set_page_url("/url")
    dvk.set_media_file("file.txt")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING ARTISTS FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert len(read_dvk.get_artists()) == 2
    assert read_dvk.get_artists()[0] == "artist"
    assert read_dvk.get_artists()[1] == "Person"

def test_set_time_int():
    """
    Tests the set_time_int method.
    """
    # TEST EMPTY TIME FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST VALID TIME
    dvk.set_time_int(2017, 10, 6, 19, 15)
    assert dvk.get_time() == "2017/10/06|19:15"
    # TEST INVALID YEAR
    dvk.set_time_int(0, 10, 10, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID MONTH
    dvk.set_time_int(2017, 0, 10, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 13, 10, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID DAY
    dvk.set_time_int(2017, 10, 0, 7, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 10, 32, 7, 15);
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID HOUR
    dvk.set_time_int(2017, 10, 10, -1, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 10, 10, 24, 15)
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST INVALID MINUTE
    dvk.set_time_int(2017, 10, 10, 7, -1)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time_int(2017, 10, 10, 7, 60)
    assert dvk.get_time() == "0000/00/00|00:00"
    # WRITE DVK
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "time_dvk.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_time_int(2020, 10, 26, 21, 15)
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING TIME FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_time() == "2020/10/26|21:15"

def test_get_set_time():
    """
    Tests the get_time and set_time methods.
    """
    # TEST DEFAULT TIME FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_time() == "0000/00/00|00:00"
    # TEST GETTING AND SETTING TIME
    dvk.set_time("2017!10!06!05!00")
    assert dvk.get_time() == "2017/10/06|05:00"
    # TEST SETTING INVALID TIMES
    dvk.set_time(None)
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time("2017/10/06")
    assert dvk.get_time() == "0000/00/00|00:00"
    dvk.set_time("yyyy/mm/dd/hh/tt")
    assert dvk.get_time() == "0000/00/00|00:00"
    # WRITE DVK FILE
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "time.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_time("2020/10/27|17:55")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING TIME FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_time() == "2020/10/27|17:55"

def test_get_set_web_tags():
    """
    Tests the get_web_tags and set_web_tags methods.
    """
    # TEST EMPTY WEB TAGS FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_web_tags() is None
    # TEST GETTING AND SETTING WEB TAGS
    tags = ["tag2", "Tag1", "tag2", None]
    dvk.set_web_tags(tags)
    assert len(dvk.get_web_tags()) == 2
    assert dvk.get_web_tags()[0] == "tag2"
    assert dvk.get_web_tags()[1] == "Tag1"
    # TEST INVALID TAGS
    dvk.set_web_tags(None)
    assert dvk.get_web_tags() is None
    dvk.set_web_tags([])
    assert dvk.get_web_tags() is None
    tags = [None]
    dvk.set_web_tags(tags)
    assert dvk.get_web_tags() is None
    # WRITE DVK
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "tags.txt"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    tags = ["String"]
    tags.append("tags")
    dvk.set_web_tags(tags)
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING WEB TAGS FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert len(read_dvk.get_web_tags()) == 2
    assert read_dvk.get_web_tags()[0] == "String"
    assert read_dvk.get_web_tags()[1] == "tags"

def test_get_set_description():
    """
    Tests the get_description and set_descritpion methods.
    """
    # TEST DEFAULT DESCRIPTION FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_description() is None
    # TEST GETTING AND SETTING DESCRIPTION
    dvk.set_description("   <i>Baño</i>  ")
    assert dvk.get_description() == "<i>Ba&#241;o</i>"
    dvk.set_description("<i>Ba&#241;o</i>")
    assert dvk.get_description() == "<i>Ba&#241;o</i>"
    # TEST SETTING EMPTY DESCRIPTION
    dvk.set_description(None)
    assert dvk.get_description() is None
    dvk.set_description("")
    assert dvk.get_description() is None
    dvk.set_description("   ")
    assert dvk.get_description() is None
    # WRITE DVK
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "desc.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_description("Other Description")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING DESCRIPTION FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_description() == "Other Description"

def test_get_set_page_url():
    """
    Tests the get_page_url and set_page_url methods.
    """
    # TEST EMPTY PAGE URL FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_page_url() is None
    # TEST GETTING AND SETTING PAGE URL
    dvk.set_page_url("/Page/URL")
    assert dvk.get_page_url() == "/Page/URL"
    # TEST SETTING INVALID URL
    dvk.set_page_url(None)
    assert dvk.get_page_url() is None
    dvk.set_page_url("")
    assert dvk.get_page_url() is None
    # WRITE DVK
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "page.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("test.net/url/Page")
    dvk.set_media_file("file.txt")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING PAGE URL FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_page_url() == "test.net/url/Page"

def test_get_set_direct_url():
    """
    Tests the get_direct_url and set_direct_url methods.
    """
    # TEST EMPTY DIRECT URL FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_direct_url() is None
    # TEST GETTING AND SETTING DIRECT URL
    dvk.set_direct_url("/direct/URL")
    assert dvk.get_direct_url() == "/direct/URL"
    # TEST SETTING INVALID DIRECT URL
    dvk.set_direct_url(None)
    assert dvk.get_direct_url() is None
    dvk.set_direct_url("")
    assert dvk.get_direct_url() is None
    # WRITE DVK
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "direct.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_direct_url("test.net/url/Direct")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING DIRECT URL
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_direct_url() == "test.net/url/Direct"

def test_get_set_secondary_url():
    """
    Tests the get_secondary_url and set_secondary_url methods.
    """
    # TEST EMPTY SECONDARY URL FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_secondary_url() is None
    # TEST GETTING AND SETTING SECONDARY URL
    dvk.set_secondary_url("/Page/URL")
    assert dvk.get_secondary_url() == "/Page/URL"
    # TEST SETTING INVALID SECONDARY URL
    dvk.set_secondary_url(None)
    assert dvk.get_secondary_url() is None
    dvk.set_secondary_url("")
    assert dvk.get_secondary_url() is None
    # WRITE DVK
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "sec.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_secondary_url("test.net/url/second")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING SECONDARY URL FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert read_dvk.get_secondary_url() == "test.net/url/second"

def test_get_set_media_file():
    """
    Tests the get_media_file and set_media_file methods.
    """
    # TEST EMPTY MEDIA FILE FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_media_file() is None
    # TEST SETTING MEDIA FILE WITH NO DVK FILE SET
    dvk.set_media_file("file.txt")
    assert dvk.get_media_file() is None
    # TEST SETTING MEDIA FILE FROM DVK FILE WITH INVALID PARENT
    dvk.set_dvk_file("/non-existant/file.dvk")
    dvk.set_media_file("file.txt")
    assert dvk.get_media_file() is None
    # TEST SETTING MEDIA WITH VALID DVK FILE
    test_dir = get_test_dir()
    dvk.set_dvk_file(join(test_dir, "file.dvk"))
    dvk.set_media_file("file.txt")
    assert abspath(join(dvk.get_media_file(), pardir)) == test_dir
    assert basename(dvk.get_media_file()) == "file.txt"
    # TEST SETTING INVALID MEDIA FILE WITH INVALID DVK FILE
    dvk.set_media_file(None)
    assert dvk.get_media_file() is None
    dvk.set_media_file("")
    assert dvk.get_media_file() is None
    # WRITE DVK
    dvk.set_dvk_file(join(test_dir, "media.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("media.png")
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING MEDIA FILE VALUE FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert abspath(join(read_dvk.get_media_file(), pardir)) == test_dir
    assert basename(read_dvk.get_media_file()) == "media.png"

def test_get_set_secondary_file():
    """
    Tests the get_secondary_file and set_secondar_file methods.
    """
    # TEST EMPTY SECONDARY MEDIA FILE FROM CONSTRUCTOR
    dvk = Dvk()
    assert dvk.get_secondary_file() is None
    # TEST SETTING SECONDARY MEDIA FILE WITH NO DVK FILE SET
    dvk.set_secondary_file("file.txt")
    assert dvk.get_secondary_file() is None
    test_dir = get_test_dir()
    dvk.set_secondary_file(join(test_dir, "file.txt"))
    assert dvk.get_secondary_file() is None
    # TEST SETTING SECONDARY MEDIA FILE FROM DVK FILE WITH INVALID PARENT
    dvk.set_dvk_file("/non-existant/file.dvk")
    dvk.set_secondary_file("file.txt")
    assert dvk.get_secondary_file() is None
    # TEST SETTING SECONDARY MEDIA WITH VALID DVK FILE
    dvk.set_dvk_file(join(test_dir, "file.dvk"))
    dvk.set_secondary_file("file.txt")
    assert abspath(join(dvk.get_secondary_file(), pardir)) == test_dir
    assert basename(dvk.get_secondary_file()) == "file.txt"
    # TEST SETTING INVALID SECONDARY MEDIA FILE WITH INVALID DVK FILE
    dvk.set_secondary_file(None)
    assert dvk.get_secondary_file() is None
    dvk.set_secondary_file("")
    assert dvk.get_secondary_file() is None
    # WRITE DVK
    dvk.set_dvk_file(join(test_dir, "media.dvk"))
    dvk.set_dvk_id("id123")
    dvk.set_title("Title")
    dvk.set_artist("artist")
    dvk.set_page_url("/url/")
    dvk.set_media_file("file.txt")
    dvk.set_secondary_file("media.png");
    dvk.write_dvk()
    assert exists(dvk.get_dvk_file())
    # TEST READING SECONDARY MEDIA FILE VALUE FROM DVK FILE
    read_dvk = Dvk(dvk.get_dvk_file())
    dvk = None
    assert abspath(join(read_dvk.get_secondary_file(), pardir)) == test_dir
    assert basename(read_dvk.get_secondary_file()) == "media.png"

def test_get_filename():
    """
    Tests the get_filename method.
    """
    # TEST WITH NO TITLE OR ID
    dvk = Dvk()
    assert dvk.get_filename(False) == ""
    # TEST WITH ONLY TITLE
    dvk.set_title("Title")
    assert dvk.get_filename(False) == ""
    # TEST WITH ONLY ID
    dvk.set_dvk_id("ID123")
    dvk.set_title(None)
    assert dvk.get_filename(False) == ""
    # TEST WITH VALID TITLE AND ID
    dvk.set_title("a   B-cd!")
    assert dvk.get_filename() == "a B-cd_ID123"
    assert dvk.get_filename(True) == "a B-cd_ID123_S"
    # TEST WITH ID THAT IS TOO LONG
    dvk.set_title("Title")
    dvk.set_dvk_id("VERYLONG1234567890987654321")
    assert dvk.get_filename() == "Title_DVK8698180574"
    assert dvk.get_filename(True) == "Title_DVK8698180574_S"
    assert dvk.get_filename(False, "AAA") == "Title_AAA8698180574"
    assert dvk.get_filename(True, "abc") == "Title_ABC8698180574_S"
    assert dvk.get_dvk_id() == "VERYLONG1234567890987654321"
    # TEST WITH EMPTY TITLE
    dvk.set_title("")
    dvk.set_dvk_id("id123")
    assert dvk.get_filename() == "0_ID123"
    assert dvk.get_filename(True) == "0_ID123_S"

def test_rename_files():
    # CREATE TEST DVK WITHOUT EXISTING MEDIA FILES
    no_media_dvk = Dvk()
    test_dir = get_test_dir()
    no_media_dvk.set_dvk_file(join(test_dir, "rnm.dvk"))
    no_media_dvk.set_dvk_id("id123")
    no_media_dvk.set_title("Title")
    no_media_dvk.set_artist("Artist")
    no_media_dvk.set_page_url("/url/")
    no_media_dvk.set_media_file("file.txt")
    no_media_dvk.set_secondary_file("sec.png")
    no_media_dvk.write_dvk()
    assert exists(no_media_dvk.get_dvk_file())
    assert not exists(no_media_dvk.get_media_file())
    assert not exists(no_media_dvk.get_secondary_file())
    # TEST RENAMING DVK FILE
    no_media_dvk.rename_files("New", "New2")
    read_dvk = Dvk(no_media_dvk.get_dvk_file())
    no_media_dvk = None
    assert basename(read_dvk.get_dvk_file()) == "New.dvk"
    assert basename(read_dvk.get_media_file()) == "New.txt"
    assert basename(read_dvk.get_secondary_file()) == "New2.png"
    assert exists(read_dvk.get_dvk_file())
    assert not exists(read_dvk.get_media_file())
    assert not exists(read_dvk.get_secondary_file())
    # CREATE TEST DVK WITH EXISTING MEDIA FILE
    media_dvk = Dvk()
    media_dvk.set_dvk_file(join(test_dir, "rnm.dvk"))
    media_dvk.set_dvk_id("id123")
    media_dvk.set_title("Title")
    media_dvk.set_artist("Artist")
    media_dvk.set_page_url("/url/")
    media_dvk.set_media_file("media.png")
    with open(media_dvk.get_media_file(), "w") as out_file:
        out_file.write("TEST")
    media_dvk.write_dvk()
    assert exists(media_dvk.get_dvk_file())
    assert exists(media_dvk.get_media_file())
    assert media_dvk.get_secondary_file() is None
    # TEST RENAMING DVK FILE WITH MEDIA FILE
    media_dvk.rename_files("other", "other")
    read_dvk = Dvk(media_dvk.get_dvk_file())
    media_dvk = None
    assert basename(read_dvk.get_dvk_file()) == "other.dvk"
    assert basename(read_dvk.get_media_file()) == "other.png"
    assert read_dvk.get_secondary_file() is None
    assert exists(read_dvk.get_dvk_file())
    assert exists(read_dvk.get_media_file())
    # CREATE TEST DVK WITH EXISTING MEDIA AND SECONDARY FILES
    secondary_dvk = Dvk()
    secondary_dvk.set_dvk_file(join(test_dir, "rnm.dvk"))
    secondary_dvk.set_dvk_id("id123")
    secondary_dvk.set_title("Title")
    secondary_dvk.set_artist("Artist")
    secondary_dvk.set_page_url("/url/")
    secondary_dvk.set_media_file("media.pdf")
    with open(secondary_dvk.get_media_file(), "w") as out_file:
        out_file.write("TEST")
    secondary_dvk.set_secondary_file("secondary.jpg")
    with open(secondary_dvk.get_secondary_file(), "w") as out_file:
        out_file.write("SECONDARY")
    secondary_dvk.write_dvk()
    assert exists(secondary_dvk.get_dvk_file())
    assert exists(secondary_dvk.get_media_file())
    assert exists(secondary_dvk.get_secondary_file())
    # TEST RENAMING DVK FILE WITH MEDIA AND SECONDARY FILES
    secondary_dvk.rename_files("First", "Second")
    read_dvk = Dvk(secondary_dvk.get_dvk_file())
    secondary_dvk = None
    assert basename(read_dvk.get_dvk_file()) == "First.dvk"
    assert basename(read_dvk.get_media_file()) == "First.pdf"
    assert basename(read_dvk.get_secondary_file()) == "Second.jpg"
    assert exists(read_dvk.get_dvk_file())
    assert exists(read_dvk.get_media_file())
    assert exists(read_dvk.get_secondary_file())

def test_write_media():
    """
    Tests the write_media method
    """
    # CREATE DVK THAT CANNOT BE WRITTEN
    test_dir = get_test_dir()
    media_dvk = Dvk()
    media_dvk.set_dvk_file(join(test_dir, "inv.dvk"))
    media_dvk.set_dvk_id("id123")
    media_dvk.set_artist("artist")
    media_dvk.set_page_url("/url/")
    media_dvk.set_media_file("media.jpg")
    media_dvk.set_direct_url("http://www.pythonscraping.com/img/gifts/img6.jpg")
    # TEST WRITE MEDIA WHEN URL IS VALID, BUT DVK CANNOT BE WRITTEN
    media_dvk.write_media()
    assert not exists(media_dvk.get_dvk_file())
    assert not exists(media_dvk.get_media_file())
    # TEST WRITE MEDIA WHEN DVK CAN BE WRITTEN, BUT URL IS INVALID
    media_dvk.set_title("Title")
    media_dvk.set_direct_url("!@#$%^")
    media_dvk.write_media(True)
    assert not exists(media_dvk.get_dvk_file())
    assert not exists(media_dvk.get_media_file())
    assert media_dvk.get_time() == "0000/00/00|00:00"
    # TEST VALID DIRECT MEDIA URL
    media_dvk.set_direct_url("http://www.pythonscraping.com/img/gifts/img6.jpg")
    media_dvk.write_media();
    assert exists(media_dvk.get_dvk_file())
    assert exists(media_dvk.get_media_file())
    assert basename(media_dvk.get_media_file()) == "media.jpg"
    assert stat(media_dvk.get_media_file()).st_size == 39785
    assert media_dvk.get_time() == "0000/00/00|00:00"
    # CREATE DVK WITH INVALID SECONDARY URL
    secondary_dvk = Dvk()
    secondary_dvk.set_dvk_file(join(test_dir, "inv2.dvk"))
    secondary_dvk.set_dvk_id("id123")
    secondary_dvk.set_title("Title")
    secondary_dvk.set_artist("artist")
    secondary_dvk.set_page_url("/url/")
    secondary_dvk.set_media_file("primary.jpg")
    secondary_dvk.set_direct_url("http://www.pythonscraping.com/img/gifts/img6.jpg")
    secondary_dvk.set_secondary_file("secondary.jpg")
    secondary_dvk.set_secondary_url("!@#$%^")
    # TEST WRITING MEDIA WITH VALID PRIMARY, BUT INVALID SECONDARY MEDIA URLS
    media_dvk.write_media();
    assert not exists(secondary_dvk.get_dvk_file())
    assert not exists(secondary_dvk.get_media_file())
    assert not exists(secondary_dvk.get_secondary_file())
    # TEST WRITING MEDIA WITH VALID PRIMARY AND SECONDARY MEDIA URLS
    secondary_dvk.set_secondary_url("http://www.pythonscraping.com/img/gifts/img4.jpg")
    secondary_dvk.write_media(True)
    assert exists(secondary_dvk.get_dvk_file())
    assert exists(secondary_dvk.get_media_file())
    assert exists(secondary_dvk.get_secondary_file())
    assert stat(secondary_dvk.get_media_file()).st_size == 39785
    assert stat(secondary_dvk.get_secondary_file()).st_size == 85007
    assert basename(secondary_dvk.get_secondary_file()) == "secondary.jpg"
    assert secondary_dvk.get_time() == "2014/08/04|00:49"

def all_tests():
    """
    Runs all tests for the Dvk class.
    """
    test_can_write()
    test_get_set_dvk_file()
    test_get_set_dvk_id()
    test_get_set_title()
    test_get_set_artists()
    test_set_time_int()
    test_get_set_time()
    test_get_set_web_tags()
    test_get_set_description()
    test_get_set_page_url()
    test_get_set_direct_url()
    test_get_set_secondary_url()
    test_get_set_media_file()
    test_get_set_secondary_file()
    test_get_filename()
    test_rename_files()
    test_write_media()

