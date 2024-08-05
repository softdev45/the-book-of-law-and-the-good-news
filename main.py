import datetime
import os
import time

from flask import Flask, render_template, request, session
from flask.helpers import redirect
from wtforms.fields.simple import TextAreaField
from wtforms_alchemy import ModelForm
# from flask_wtf import FlaskForm
# import wtforms
# :

from db import Request, SessionLocal, Verse, Viewed

from flask_migrate import Migrate

import xml.etree.ElementTree as ET
from lxml import etree

import re
import math

title = os.environ['Title'] = 'DEV_MODE'
# os.environ.get('Title')

app = Flask(__name__)

app.secret_key = '1234!@#$qwerQWER'

# with open('bible2.xml', 'r') as bible:
# data = bible.read()
root_en = etree.parse('bible.xml')
root_pl = etree.parse('polish.xml')
root = root_pl
# root = ET.fromstring(data)
from collections import OrderedDict

wordstat = OrderedDict()
with open('count_1ws.txt', 'r') as file:
	for line in file.readlines():
		word, freq = line.split()
		wordstat[word] = int(freq)
# print(wordstat.keys())

wordsearches = OrderedDict()

# db = get_db()
# db = SQLAlchemy(app)
# os.environ
# TODO
# are there any feature requests?
# would like an app to: display current time [mat]


class RequestForm(ModelForm):
	# request_data = TextAreaField('request_data')
	class Meta:
		model = Request


def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


with SessionLocal() as db:
	migrate = Migrate(app, get_db())

#TODO sync db with replit


def make_fire(ref):
	with SessionLocal() as db:
		refed = db.query(Verse).filter_by(location=ref).first()
		# print('found verse:')
		print(refed)
		if not refed:
			refed = Verse(location=ref, fire=0)
		# print('adding fire:')
		# print(refed)
		if refed:
			refed.fire += 1
			db.add(refed)
			# db.commit()

		vsted = Viewed(location=ref, session=session['uid'])
		db.add(vsted)
		db.commit()


@app.route('/plan')
def doc():
	return render_template('doc.html')


def estimate_freq_index(word):
	original = word
	# print('estimate: ', word)
	while word:
		# print(word)
		if word not in wordstat.keys():
			word = word[:-1]
		else:
			return (original, wordstat[word])
	return 0

@app.route('/db')
@app.route('/db/<name>')
def download(name='Viewed'):
	with SessionLocal() as db:
		import time
		result = db.query(Viewed).all()
		result = list(map(lambda v: v.to_json(), result))
		from flask import jsonify
		# print(result)
	return jsonify(result)

def word_search(word):
	# ns = {"re": "http://exslt.org/regular-expressions"}	
	if len(w := word.split(',')) > 1:
		word = w[0]
	xpath_expression = f".//seg[@type='verse'][contains(text(),'{word}')]"  #[not(contains(@id, '{ref}'))]"
	#TODO fix search
	# print(xpath_expression)
	locations = root.xpath(xpath_expression)  #, namespaces=ns)
	#todo fix
	# while w
	locations = list(filter(lambda l: word.lower() in l.text.lower(), locations))
	# print('word search', word, locations)
	if len(locations) == 0:
		return []
	# print(locations[0].attrib)
	locations = list(map(lambda l: (l.text, l.attrib['id']), locations))
	#impl rndmizr
	# print(locations)
	return locations


def leave_trace(session, request):

	try:
		uid = session['uid']
	except:
		import random
		import time
		session['uid'] = time.time()
		try:
			session['paths']
		except:
			if not 'paths' in session:
				session['paths'] = []

	if request.path not in session['paths'] and request.path.count('/') > 1:
		session['paths'].append(request.path)
		session.modified = True

	print(session['paths'])


@app.route('/look_up/<word>')
def look_up(word):
	leave_trace(session, request)
	make_fire(word)

	words = [(word, word_search(word))]

	return render_template('verses.html', words=words)


@app.route('/connects/<to>/from_to/<source>')
def connect(to=None, source=None):
	pass
	# with


@app.route('/source/<ref>')
@app.route('/source')
def living_water(ref=None):
	leave_trace(session, request)
	book = verse = chapter = words = steps = None
	fire = {}
	if ref:
		make_fire(ref)
		steps = ref.split('.')
		book = steps[1] if len(steps) > 1 else None
		chapter = steps[2] if len(steps) > 2 else None
		verse = steps[3] if len(steps) > 3 else None
	show_verses = False

	if verse:
		show_verses = True
		xpath_expression = f".//seg[@type='verse'][@id='b.{book}.{chapter}.{verse}']"
		elements = root.xpath(xpath_expression)
		v: str = elements[0].text
		# words = v.strip().lower().split('')
		# Regular expression to match words (alphanumeric characters)
		word_pattern = r'\w+'
		# Find all matches of the word pattern in the sentence
		words = re.findall(word_pattern, v)
		words = verse_words = [word.lower() for word in words]

		result = None
		while result is None:
			result = map(lambda word: estimate_freq_index(word), words)
		words = list(result)
		words = list(set(words))
		words = sorted(words, key=lambda e: e[1])
		# print(words)
		# words = words[0:int(len(words) * 0.25)]
		words = words[0:int(len(words) * 0.25)]

		# print('#1')
		# print(words)

		words = list(map(lambda word: [word[0], word_search(word[0])], words))
		words = list(filter(lambda word: len(word[1]) > 0, words))

		for i in range(0, len(words)):
			start_len = len(words[i][1])
			thres = 77 - int(math.log(start_len * (i + 1))**1.81)
			print(words[i][0], ' ', thres, 'start=', start_len)
			while len(words[i][1]) > thres:
				words[i][1] = words[i][1][::2]

		# for i in range(0, len(words)):
		# 	print(words)
		# 	sentences = words[i][1]
		# 	result = sorted(sentences, key=lambda s: sum([s[0].lower().count(word) for word in verse_words]), reverse=True)
		# 	if len(result) > 30:
		# 		result = result[:30]
		# 	words[i][1] = result

		words = sorted(words, key=lambda e: len(e[1]))

		with SessionLocal() as db:
			for elem in elements:
				if elem is not None:
					verse = db.query(Verse).filter_by(location='.'.join(steps)).first()
					# viewed = db.query(Viewer).filter_by(location='.'.join(steps))
			# print(list(map(lambda e: e.attrib['id'], elements)))

		# return render_template('verses.html', data = elements, show_verses=True)
	elif chapter:
		show_verses = True
		xpath_expression = f".//seg[@type='verse'][starts-with(@id,'b.{book}.{chapter}')]"
		elements = root.xpath(xpath_expression)
		with SessionLocal() as db:
			for elem in elements:
				if elem is not None:
					# print('.'.join(steps))
					vq = db.query(Verse).filter_by(location=elem.attrib['id']).first()
					if vq:
						id_ = elem.attrib['id']
						fire[id_] = vq.fire
		# print(elements)
		# return render_template('verses.html', data = elements, show_verses=True)
	elif book:
		# print(book)
		xpath_expression = f".//div[@type='chapter'][starts-with(@id,'b.{book}')]"
		elements = root.xpath(xpath_expression)
		# return render_template('verses.html', data = elements)
	else:
		xpath_expression = f".//div[@type='book']"
		elements = root.xpath(xpath_expression)

	return render_template('verses.html',
	                       data=elements,
	                       show_verses=show_verses,
	                       ref=steps,
	                       verse=verse,
	                       words=words,
	                       fire=fire)
	# return render_template('verses.html', data = elements)


@app.route('/verse/<ref>', methods=['POST', 'GET'])
def handle_fire(ref):
	#TODO implement
	if not ref:
		return 'no_ref_selected'
	make_fire(ref)

	return redirect(f'/source/{ref}')


@app.route('/request/create', methods=['POST'])
def create_request():
	# data = request.form['text_data']
	form = RequestForm(request.form)
	if True:
		#TODO
		with SessionLocal() as db:
			new_req = Request()
			form.populate_obj(new_req)
			db.add(new_req)
			db.commit()
		# receiver = Receiver('text_data')
		# receiver.receive(data)

	return redirect('/list')
	# return f'Hello, {data}! Your data was submitted successfully.\
	# <a href="/receiver">Receiver</a>'


@app.route('/request/delete/<id>', methods=['POST'])
def remove_request(id):
	# data = request.form['text_data']
	form = RequestForm(request.form)
	with SessionLocal() as db:
		r = db.query(Request).get(id)
		# new_req = Request()
		# form.populate_obj(r)
		# db.delete(r)
		# db.commit()
	return redirect('/list')


@app.route('/request/update/<id>', methods=['PUT'])
def handle_data2(id):
	# data = request.form['text_data']
	form = RequestForm(request.form)
	if True:
		#TODO
		with SessionLocal() as db:
			r = db.query(Request).get(id)
			# new_req = Request()
			form.populate_obj(r)
			db.add(r)
			db.commit()
		# receiver = Receiver('text_data')
		# receiver.receive(data)

	return redirect('/list')


@app.route('/')
def index():
	#DEV: temporarily: redirect root path (/) to /receiver
	return redirect('/source/b.JOS.1.8')
	return f'Welcome to this website.<br/>\
    # Current title: {title}<br/>\
    page loaded at: {time.time()} '

	# Question (Task): what does time() function return?


@app.route('/receiver', methods=['GET'])
def receiver_endpoint():
	form = RequestForm()
	return render_template('receiver.html', form=form)


@app.route('/revelation', methods=['GET'])
def revelation():

	return render_template('revelation.html')


@app.route('/list', methods=['GET'])
def messages():
	# with open('./text_data_db.txt', 'r') as db:
	#     db.readline()
	#     data = db.readlines()
	#     result = [(data[i], data[i + 1]) for i in range(0, len(data) - 1, 2)]
	# form = ModelForm()
	result = []
	with SessionLocal() as db:
		result = db.query(Request).all()
		# print(result)
	return render_template('list.html', data=reversed(result))  #, form = form)


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
