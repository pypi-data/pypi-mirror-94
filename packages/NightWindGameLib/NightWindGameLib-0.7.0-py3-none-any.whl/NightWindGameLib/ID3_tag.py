from pydub import AudioSegment as a
from pydub.utils import mediainfo

try:
    from .media_tool import*
except ImportError:
    import media_tool


def main():
    song = a.from_mp3("images_tag/四句儿歌.mp3")
    song.export("images_tag/新四句儿歌.mp3", format="mp3",
                tags={"artist": "编程猫", "title": "新四句儿歌",
                      "comments": "awesome", "album": "Best song for kids"},
                cover="images_tag/3.jpg", id3v2_version='3')
    info = mediainfo("images_tag/新四句儿歌.mp3")
    print(info)


if __name__ == '__main__':
    main()
