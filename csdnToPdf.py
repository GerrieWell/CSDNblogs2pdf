# -*- coding: utf-8 -*-
import urllib,urllib2,cookielib,re,socket
import os,sys,time
from bs4 import BeautifulSoup
#import BeautifulSoup
#防止编码乱码#
reload(sys)   
sys.setdefaultencoding('utf-8') 
####

url='http://blog.csdn.net/Luoshengyang/'# csdn的账号
blogName='Luoshengyang/'
blogDir='./csdn_blog/'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0'
    }


#读取htmml
def login(url=url):
	#socket.setdefaulttim #单位为秒
	time.sleep(0.5)# 防止封IP
	req= urllib2.Request(url=url,headers=headers)
	html = urllib2.urlopen(req).read()
	return html
	#return html.decode('GBK','ignore').encode('UTF-8')

StringPrefix=''
StringSurfix=' '
def fixSynaxHilghLighter(html):
	soup = BeautifulSoup(html,from_encoding='utf-8')
	orginal=file('oringal.html','w')
	orginal.write(html)
	orginal.close()
	userSoup = soup.find(name="div", attrs={"id":"body"})

	classes=userSoup.findAll(name="pre")
	try:
		for cla in classes:
			if(cla.get('class')==0):
				continue
			s  = cla['class'][0]
			tmp="brush: "+ s + ";"
			cla['class'][0] = tmp
	except KeyError ,e:
		print e

	str = userSoup.__str__()
	dest = StringPrefix+str+StringSurfix

	f = file('./test.html','w');
	f.write(dest)
	f.close
	return dest
'''
if __name__ == '__main__':
	artical_url='http://blog.csdn.net/tx3344/article/details/8476669'
	html=login(artical_url)
	fixSynaxHilghLighter(html)
'''
if __name__ == '__main__':
#def main():
	state=True

	surfixFd= open('./Surfix.txt','r')
	prefixFd = open('./prefix.txt','r')
	StringPrefix = prefixFd.read()
	StringSurfix = surfixFd.read()
	surfixFd.close()
	prefixFd.close()
	
	html=login()
	isExist = os.path.exists(blogDir+blogName)
	if not isExist:
		os.makedirs(blogDir+blogName)
		os.system("cd "+blogDir+blogName+" && ln -s ../../scripts scripts"
		+ " && ln -s ../../styles styles")
		os.system("cd -")
	while state:
		soup=BeautifulSoup(html)
		articals=soup.findAll(name='div',attrs={'class' : 'list_item article_item'})
		for artical in articals:
			title=artical.find('a')
			artical_url='http://blog.csdn.net/'+title['href']
			print artical_url
			artNum=artical_url.split('/')
			artNum=artNum[-1]
			print artNum
			s=title.text.replace('\r\n',' ')#去掉回车符
			s=s.lstrip()#去掉首空格
			s=s.rstrip()#去掉尾空格
			s=s.strip() #过滤字符串中所有的转义符
			#s.s.find('/')
			s=s.replace('/','or')
			s=s.replace(' ','')
			s=s.decode('UTF-8','ignore').encode('UTF-8');
			'''sAscii=s.decode('UTF-8','ignore').encode('GBK')
			print sAscii
			suffix=".htm"
			ret=sAscii+suffix.decode('UTF-8','ignore').encode('GBK')
			print ret
			'''
			print s

			destHtml=blogDir+blogName+artNum+'.htm'
			destPdf=blogDir+blogName+artNum+'.pdf'
			realNamePdf=blogDir+blogName+s+'.pdf'
			f=file(destHtml, 'w')	#保存的目录
			f.write(fixSynaxHilghLighter(login(artical_url)))
			f.close()
			print destHtml
			print destPdf
			os.system('wkhtmltopdf '+'\"'+destHtml+'\"'+' '+'\"'+destPdf+'\"')
			os.rename(destPdf,realNamePdf)
			#print artical_url
			
		##换页转换
		pagelist= soup.find(name='div',id='papelist')
		next=pagelist.findAll('a')
		state=False
		for i in next :
			if i.text.encode('utf-8')==str('下一页') :
				url='http://blog.csdn.net/'+i['href']
				html=login(url)
				state=True
				break;

#if __name__ == '__main__':
#	f=file("./csdn_blog/"+'1234'+'.htm', 'w')	#保存的目录
#	f.write(login(url))
#	f.close()
