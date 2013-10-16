#!/usr/bin/env python
# -- coding: utf-8 --

import os, sys, glob, ntpath, Image, codecs, argparse

title = "HyperTroll Markup Language"

html = "<div id=\"clusterfuck\" style=\"width:{0}px;height:{1}px;\"><div id=\"clusterfuckinner\" style=\"box-shadow: inset 1px 1px 0 {2}\"></div></div>"

def csshex(c):
	r = format(c[0], "02x")
	g = format(c[1], "02x")
	b = format(c[2], "02x")
	rgb1 = "#{0:<1.1}{1:<1.1}{2:<1.1}"
	rgb2 = "#{0:<2.2}{1:<2.2}{2:<2.2}"
	return rgb1.format(r, g, b) if r[0] == r[1] and g[0] == g[1] and b[0] == b[1] else rgb2.format(r, g, b)

def box_shadow(x, y, c, first):
	x_ = 0 if x == 0 else str(x) + "px"
	y_ = 0 if y == 0 else str(y) + "px"
	return ("{0},").format(csshex(c)) if first else ("{0} {1} 0 {2},").format(x_, y_, csshex(c))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("infile", type=str, help="Image to be parsed")
	parser.add_argument("outfile", type=str, help="Name of HTML output file")
	if len(sys.argv) == 1:
		parser.print_usage()
		sys.exit(1)
	args, unknown = parser.parse_known_args()
	
	with codecs.open("template.html", "r", encoding="utf8") as template:
		clusterfuck = template.read()
	
	im = Image.open(args.infile)
	print "Parsing " + args.infile
	boxshadows = ""
	imdata = im.getdata()
	for y in range(im.size[1]):
		for x in range(im.size[0]):
			i = y * im.size[0] + x
			boxshadows += box_shadow(x, y, imdata[i], i == 0)
	boxshadows = boxshadows[:-1] + ";"
	with codecs.open(args.outfile, "w", encoding="utf8") as outfile:
		outfile.write(clusterfuck.replace("<!-- CLUSTERFUCK -->", html.format(im.size[0], im.size[1], boxshadows))) #replacing the HTML comment with {0} and then using .format instead of .replace fails with a KeyError, and I'm too lazy to fix that
	
	print "Generated " + args.outfile

if __name__ == "__main__":
	main()