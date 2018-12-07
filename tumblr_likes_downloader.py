import math
import os
import pytumblr
import re
import urllib.request

client = pytumblr.TumblrRestClient(
    '<consumer_key>',
    '<consumer_secret>',
    '<oauth_token>',
    '<oauth_secret>',
)

def media_download(mylikes, dirname):
	global countAux
	global countErrors
	global countDownloads
	for i in range(0, len(mylikes['liked_posts'])):
		enumerator = "%05d" % (countAux)
		print ("\n" + mylikes['liked_posts'][i]['blog_name'] + " - " + enumerator)
		if mylikes['liked_posts'][i]['type'] == 'photo':
			for j in range(0, len(mylikes['liked_posts'][i]['photos'])):
				url = mylikes['liked_posts'][i]['photos'][j]['original_size']['url']
				name = re.findall(r'tumblr_\w+.\w+', url)
				filename = enumerator + ' - ' + name[0]
				for file in os.listdir('.'):
					if re.search(name[0], file):
						print("\tFile already exists!")
						break	
				else:
					try:
						print("   " + url)
						urllib.request.urlretrieve(url, filename)
					except:
						print("\tOops!  That was no valid file...")
						countErrors += 1
					else:
						countDownloads += 1
		elif mylikes['liked_posts'][i]['type'] == 'video':
			url = mylikes['liked_posts'][i]['video_url']
			name = re.findall(r'tumblr_\w+.\w+', url)
			filename = enumerator + ' - ' + name[0]
			for file in os.listdir('.'):
				if re.search(name[0], file):
					print("\tFile already exists!")
					break
			else:
				try:
					print("   " + url)
					urllib.request.urlretrieve(url, filename)
				except:
					print("\tOops!  That was no valid file...")
					countErrors += 1
				else:
					countDownloads += 1
		else:
			url_aux = mylikes['liked_posts'][i]['body']
			index = 0
			while index < len(url_aux):
				if url_aux[index] == 'h' and url_aux[index + 1] == 't':
					url = ""
					while url_aux[index] <> '"':
						url = url + url_aux[index]
						index = index + 1
					if (re.findall(r'tumblr_\w+.\w+', url)) <> []:
						break
				index = index + 1		
			name = re.findall(r'tumblr_\w+.\w+', url)
			filename = enumerator + ' - ' + name[0]
			for file in os.listdir('.'):
				if re.search(name[0], file):
					print("\tFile already exists!")
					break
			else:
				try:
					print("   " + url)
					urllib.request.urlretrieve(url, filename)
				except:
					print("\tOops!  That was no valid file...")
					countErrors += 1
				else:
					countDownloads += 1
		countAux = int(enumerator) - 1

def main():
	global countAux
	global countDownloads
	global countErrors
	offset_aux, countDownloads, countErrors = 0, 0, 0
	limit = 50
	print ("Tumblr Backup Likes\n")
	info = client.info()
	dirname = info['user']['name']
	likedcounts = info['user']['likes']
	#print (likedcounts)
	countAux = likedcounts
	if likedcounts < 0:
		print ("Access denied...")
		accessDenied = input()
		return
	print ("Found {:d} liked posts, checking...".format(likedcounts))
	if not os.path.exists(dirname):
		os.makedirs(dirname)
	os.chdir(dirname)	
	batchs = math.ceil(likedcounts / limit)
	for i in range (0, batchs):
		mylikes = client.likes(limit = 50, offset = offset_aux)
		media_download(mylikes, dirname)
		offset_aux += limit
	print("\n>> Downloaded files: {:d}".format(countDownloads))
	print(">> Errors: {:d}".format(countErrors))
	print("\nEnd of program...")
	end = input()

if __name__ == "__main__":
	main()