from youtube_transcript_api import YouTubeTranscriptApi
from bardapi import Bard
import os
import requests
import pytube
#important notes: This tools can only translate upto a 2000 word transript or a 10 minutes videos
#using dsdaniel park bardapi 
#the link: https://github.com/dsdanielpark/Bard-API


#code
#input youtube video link
link = input("Youtube video link: ")
source = link + "?cc_load_policy=1"
yt = pytube.YouTube(source)

#divide the link into to part and only take the video id link into id
id = source.split("v=", 2)[-1]
#check all the captions that was available or the videos has turn off caption
cc = YouTubeTranscriptApi.list_transcripts(id)
#print the available language
print("id: ", id, "\n")
print("available language: ")
for i, df in enumerate(cc):
    print(df)

#ngôn ngữ muốn đọc phụ đề
lang = input("Language that you want to read from (iso 639-1 code): ")
#lấy phụ đề về và để trong transcript
transcript = YouTubeTranscriptApi.get_transcript(id,languages=[lang, 'vi']) #second language is vietnamese
#write the whole transcript into lyrics.txt
with open("lyrics.txt", "w", encoding = 'utf-8') as f:
    for subtitle in transcript:
        text = subtitle['text']
        start = subtitle['start']
        duration = subtitle['duration']
        f.write(f"{text}\n") #if you want to write a timeline u can add {start} -> {start+duration} but when using bard it'll usually fail to translate
f.close()


#mở file để đọc
f = open("lyrics.txt", "r")



#add the token. You can use your at __Secure-1PSID in bard.google.com
os.environ['_BARD_API_KEY'] = 'YQiLtpIxwMX_V3gqKce011fmUyY9L_KCvlyUITEhuhTLUa7RmNPGUwC8ta-nvEhwfuOi6A.'
token = 'YQiLtpIxwMX_V3gqKce011fmUyY9L_KCvlyUITEhuhTLUa7RmNPGUwC8ta-nvEhwfuOi6A.'
#this code is to make bard continue from the old conversation
session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/88.0.4390.60",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", token)  
#start bard
bard = Bard(token=token, session=session)

#You should request bard to translate with the same language that you want to translate to
bard.get_answer("dịch giúp tôi một đoạn văn sang tiếng việt được không")
#give the subtitle to bard
ans = bard.get_answer(f.read())['content']
#close the .txt file after using
f.close()
#print the answer
print(ans)


