#!/usr/bin/python3
from bs4 import BeautifulSoup
import argparse
import os
import re
import csv

# parses command line arguments
def parse_commands():
	description = "Parses threads, posts, dates, and usernames from deep/dark web forums."
	parser = argparse.ArgumentParser(description=description)
	subparsers = parser.add_subparsers(dest="command")
	subparsers.required = True

	# raidforums.com
	sub_parser = subparsers.add_parser("raidforums", description="Parses HTML files from RaidForums")
	sub_parser.add_argument("-o", "--output", metavar="<filename>", dest="output_file", help="Name of the output file (CSV)", default="raidforums.csv")
	sub_parser.add_argument("-d", "--directory", metavar="<filepath>", dest="dirpath", help="Path to directory where HTML files are located", required=True)
	sub_parser.set_defaults(func=parse_forums)
	# exploit.in
	sub_parser = subparsers.add_parser("exploitin", description="Parses HTML files from Exploit.in")
	sub_parser.add_argument("-o", "--output", metavar="<filename>", dest="output_file", help="Name of the output file (CSV)", default="exploitin.csv")
	sub_parser.add_argument("-d", "--directory", metavar="<filepath>", dest="dirpath", help="Path to directory where HTML files are located", required=True)
	sub_parser.set_defaults(func=parse_forums)
	# omerta
	sub_parser = subparsers.add_parser("omerta", description="Parses HTML files from Omerta")
	sub_parser.add_argument("-o", "--output", metavar="<filename>", dest="output_file", help="Name of the output file (CSV)", default="omerta.csv")
	sub_parser.add_argument("-d", "--directory", metavar="<filepath>", dest="dirpath", help="Path to directory where HTML files are located", required=True)
	sub_parser.set_defaults(func=parse_forums)

	args = parser.parse_args()
	return args

# check to see if the specific directory exists
def check_path(dirpath):
	if not os.path.exists(dirpath):
		print(f"The specified directory \"{dirpath}\" does not exist. Exiting program.")
		exit(1)
	if dirpath[len(dirpath)-1] != "/":
		dirpath += "/"
	return dirpath

# sanitize bad characters
def sanitize(text):
	text = text.replace("\n", " ")
	text = text.replace(",", " ")
	text = text.replace("\t", " ")
	text = text.strip()
	return text

# reads a HTML file and returns a beautiful soup object
def read_file(filepath):
	html = open(filepath, 'r')
	try:
		page = BeautifulSoup(html.read(), "html.parser")
		return page
	except Exception as e:
		print(f"<<ERROR>> Could not open {filepath}. \n\t Exception: {e}")
		return None

# write parsed posts to CSV file
def write_file(posts, outfile):
	if ".csv" not in outfile:
		outfile += ".csv"
	print(f"Writing posts to {outfile}")
	with open(outfile, 'w', newline='') as csvfile:
		headers = ["Thread Title", "Post text", "Username", "Date"]
		writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore', restval='')
		writer.writeheader()
		for post in posts.values():
			writer.writerow(post)

# parses the posts from the raw HTML of a RaidForums thread
def parse_raidforums(page):
	posts = {}
	thread_title = sanitize(page.find('span', class_='thread-info__name rounded').get_text())
	print(f"Parsing Thread: {thread_title}")
	post_section = page.find('div', id="posts")
	# for each post, grab & sanitize username, content, date posted
	for post in post_section.findAll('div', {"id": re.compile('^post_\d+$')}):
		# grab username, sometimes has a different class
		try:
			one_user = sanitize(post.find(class_="post__user-profile largetext").span.get_text())
		except:
			one_user = sanitize(post.find(class_="post__user-profile largetext").get_text())
		# grab post text
		one_post = sanitize(post.find('div', class_="post_body scaleimages").get_text())
		# grab post date/time
		one_date = sanitize(post.find('span', class_="post_date").get_text())
		#post + timestamp is the key (ensures each post gets counted even if post content is exactly the same)
		post_key = one_post + " " + one_date
		posts[post_key] = {"Thread Title": thread_title, "Post text": one_post, "Username": one_user, "Date": one_date}
	return posts

# parses the posts from the raw HTML of an Exploit.in thread
def parse_exploitin(page):
	posts = {}
	thread_title = ""
	# thread title can be in multiple different span elements on exploit
	thread_info = page.find(class_="ipsType_pageTitle")
	for span in thread_info.findAll('span'):
		if thread_title == "" and span is not None:
			thread_title += span.get_text()
	thread_title = sanitize(thread_title)
	print(f"Parsing Thread: {thread_title}")
	# for each post, grab & sanitize username, content, date posted
	for post in page.findAll('article', {"id": re.compile('^elComment_')}):
		# grab username & sanitize
		one_user = sanitize(post.find("div", {"class": "cAuthorPane"}).h3.a.span.get_text())
		# grab post text, can span across multiple elements 
		one_post = ""
		for comment_section in post.findAll('div', attrs={'data-role':'commentContent'}):
			for p in comment_section.findAll('p'):
				one_post += p.get_text()
		one_post = sanitize(one_post)
		# grab post date/time
		one_date = sanitize(post.find('time').get_text())
		#post + timestamp is the key (ensures each post gets counted even if post content is exactly the same)
		post_key = one_post + " " + one_date
		posts[post_key] = {"Thread Title": thread_title, "Post text": one_post, "Username": one_user, "Date": one_date}
	return posts

# parses the posts from the raw HTML of an Omerta thread
def parse_omerta(page):
	posts = {}
	thread_title = sanitize(page.find('td', {"id": re.compile('^td_post')}).strong.get_text())
	print(f"Parsing Thread: {thread_title}")
	# for each post, grab & sanitize username, content, date posted
	for post in page.findAll('table', {"id": re.compile('^post')}):
		# grab username, sometimes has a different class
		one_user = sanitize(post.find(class_="bigusername").get_text())
		# grab post text
		one_post = sanitize(post.find('div', {"id": re.compile('^post_message')}).get_text())
		# grab post date/time
		one_date = sanitize(post.find('td', class_="tcat").get_text())
		#post + timestamp is the key (ensures each post gets counted even if post content is exactly the same)
		post_key = one_post + " " + one_date
		posts[post_key] = {"Thread Title": thread_title, "Post text": one_post, "Username": one_user, "Date": one_date}
	return posts


def parse_forums(args):
	dirpath = check_path(args.dirpath)
	posts = dict() # contains all parsed posts
	for file in os.listdir(dirpath):
		filepath = dirpath + file
		page = read_file(filepath)
		if page is None:
			continue
		elif args.command == "raidforums":
			posts.update(parse_raidforums(page))
		elif args.command == "exploitin":
			posts.update(parse_exploitin(page))
		elif args.command == "omerta":
			posts.update(parse_omerta(page))
	print(f"\nDone processing {len(posts)} posts!")
	write_file(posts, args.output_file)

def main():
	args = parse_commands()
	args.func(args)

	
if __name__ == "__main__":
	main()