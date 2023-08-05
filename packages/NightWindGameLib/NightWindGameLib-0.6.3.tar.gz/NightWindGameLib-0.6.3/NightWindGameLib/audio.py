from pydub import AudioSegment as a

try:
    from .media_tool import*
except ImportError:
    import media_tool

source = input("请输入要转换的文件名(输入q退出)：")
result = ''

while source != 'q' and result != 'q':
    source = input("请输入要转换的文件名(输入q退出)：")
    result = input("请输入转换后的文件名(输入q退出)：")
    sound = a.from_file(source, format=result.split(".")[-1])
    sound.export(result, format=result.split(".")[-1])
