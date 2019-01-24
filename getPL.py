# -*- coding: utf-8 -*-

from json import loads as json_loads
from requests import get as requests_get
from os import mkdir
from os.path import exists as path_exists
from codecs import open as codecs_open
from shutil import rmtree

def httpRequest_GET(action, query=None, urlencoded=None, callback=None, timeout=None):    
	url = action if (query == None) else (action + '?' + query)
	connection = requests_get(url, headers=header, timeout=default_timeout)
	connection.encoding = "UTF-8"
	connection = json_loads(connection.text)
	return connection

# 获 取 某 位 用 户 播 放 列 表
def user_playlist(uid, offset=0, limit=100):
	action = 'http://music.163.com/api/user/playlist/?offset=' + str(offset) + '&limit=' + str(limit) + '&uid=' + str(uid)
	data = httpRequest_GET(action)
	return data['playlist']

# 获 取 某 张 播 放 列 表 中 的 歌
def playlist_detail(playlist_id):
	action = 'http://music.163.com/api/playlist/detail?id=' + str(playlist_id)
	data = httpRequest_GET(action)
	return data['result']['tracks']

def getPL(musiclist):
	pl = []
	for song in musiclist:
		pl.append(song["name"])
	return pl

def init():
	default_timeout = 10
	header = {
		'Accept': '*/*',
		'Accept-Encoding': 'gzip,deflate,sdch',
		'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
		'Connection': 'keep-alive',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Host': 'music.163.com',
		'Referer': 'http://music.163.com/search/',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
	}
	return default_timeout, header

def resetFloder(floderName):
	if path_exists(floderName):
		rmtree(floderName)
	mkdir(floderName)

def main():
	upl = user_playlist(uid = userid)
	print ("find {} lists".format(len(upl)))
	resetFloder(floderName)
	listIndex = 0
	for it in upl:
		plid = it["id"]
		pldt = playlist_detail(playlist_id = plid)
		pl = getPL(pldt)
		print ("{}/{} has been updated".format(listIndex, len(upl)))
		with codecs_open("{}/{}_{}.txt".format(floderName, listIndex+1, it["name"]), 'a',encoding='utf-16') as fout:
			songIndex = 0
			for songname in pl:
				fout.write("{}.\t{}\n".format(songIndex + 1, songname))
				songIndex += 1
		listIndex += 1

# 全 局 变 量
default_timeout, header = init()
floderName = "./" + "playlist"
userid = ""
if __name__ == '__main__':
	main()