# -*- coding: utf-8 -*-
import sys, re, io, json

questionreobj_withanswer = re.compile('\s*(\d+)[\.,，。\s]+(.+?)(?:<picture\s*src=[\'"]?(.+?)[\'"]?\s*>)?\s*(A[\.,，。\s]+.+)(?=[A-Z])([A-Z])\s*$')
questionreobj_withoutanswer = re.compile('\s*(\d+)[\.,，。\s]+(.+?)(?:<picture\s*src=[\'"]?(.+?)[\'"]?\s*>)?\s*(A[\.,，。\s]+.+)$')
optionsreobj = re.compile('([A-Z])[.,，。\s]+(.+?)(?:\s*)(?:(?=[A-Z][\.,，。\s]+)|$)')
answerreobj = re.compile('[A-Z]')

startofquestion = re.compile('^\s*(\d+)[\.,，。\s]*')
def main(filename, output, answer_sheet=None):
	if answer_sheet:
		questionreobj = questionreobj_withoutanswer
		with io.open(answer_sheet) as f:
			lines = f.readlines()
			answer_string = ' '.join(lines)
			answers = answerreobj.findall(answer_string)
	else:
		questionreobj = questionreobj_withanswer
	questions = []

	idx = 0
	with io.open(filename) as f:
		answer = None
		if answer_sheet:
			answer = answers[idx]

		buffer = ''
		for line in f:
			if startofquestion.match(line):
				if buffer:
					if answer_sheet:
						answer = answers[idx]
					question = parse(questionreobj, buffer, answer)
					idx+=1
					if question:
						questions.append(question)
				buffer = ''
			buffer+=line.strip()
	if buffer:
		last_question = parse(questionreobj, buffer, answer)
		questions.append(last_question)

	json_string = json.dumps(questions, ensure_ascii=False)
	js = 'let questions = ' + json_string + '\nmodule.exports = questions'
	with io.open(output, 'w') as f:
		f.write(js)


def parse(reobj, string, answer=None):
	matchofquestion = reobj.match(string)
	if not matchofquestion: 
		return False
	grps = matchofquestion.groups()
	if len(grps)==5:
		no, stem, img, optionstring, answer = grps
	else:
		no, stem, img, optionstring = grps

	matchofoptions = optionsreobj.findall(optionstring)
	if not matchofoptions:
		return False
	questionobj = dict(no=int(no), stem=stem, img=img, options=[], answer=answer)
	for option, content in matchofoptions:
		opt = dict(option=option, content=content)
		questionobj['options'].append(opt)
	return questionobj 

if __name__=='__main__':
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument("rawfile", help="text file contains questions")
	parser.add_argument("output", help="output filename")
	parser.add_argument("-a", "--answer_sheet", help="add a answer sheet if the answers are not included in the text question file")
	args = parser.parse_args()

	main(args.rawfile, args.output, args.answer_sheet)
	print("Convert Finished. Please copy the file {} to desired location.".format(args.output))