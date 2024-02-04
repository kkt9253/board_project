'''
format_datetime 함수 실행시 UnicodeEncodeError 오류가 발생할 때 사용
import locale
locale.setlocale(locale.LC_ALL, '')
'''

def format_datetime(value, fmt='%Y년 %m월 %d일 %p %I:%M'):
  return value.strftime(fmt)