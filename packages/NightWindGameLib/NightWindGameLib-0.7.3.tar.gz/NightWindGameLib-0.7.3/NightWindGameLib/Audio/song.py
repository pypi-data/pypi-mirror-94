from NightWindGameLib.Audio import media_tool
from pydub import AudioSegment as a
from pydub.playback import play


def main():
    sound1 = a.from_file("pydub_audio/我是阿短.mp3")[1500:2200]
    sound2 = a.from_file("pydub_audio/他是编程猫.mp3")[2000:4000]
    play(sound1 * 4 + sound2)


if __name__ == '__main__':
    main()
