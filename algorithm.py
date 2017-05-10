def fair_use_determination(request):
	print "inside fair use determination!"
	purpose = request.form.get('purpose')
	if purpose == 'educational':
		return (1,'Automatically fair use - education is a specific carve out for fair use!')
	if request.args.get('type') == 'vis-art':
		return visual_art_determination(request)
	elif request.args.get('type') == 'code':
		return code_determination(request)
	elif request.args.get('type') == 'lit':
		print "in lit determination"
		return lit_determination(request)
	elif request.args.get('type') == 'music':
		return music_determination(request)

def assign_parody(request):
	value = request.form.get('parody-satire')
	if value == 'parody':
		return 1
	elif value == 'satire':
		return 2
	else:
		return 3

def assign_similarity(request):
	value = request.form.get('similarity')
	if value == 'not-similar':
		return 1
	elif value == 'somewhat-similar':
		return 2
	else:
		return 3


def visual_art_determination(request):
	if request.form.get('copy-copy') == 'copied-original':
		return (1, 'Almost always fair use! Can copy the same flower field - that is not infringement!')
	noncommercial = .1
	if request.form.get('purpose') == 'noncommercial':
		noncommercial = .2
	profit =  .15
	if int(request.form.get('market-share')) > int(5):
		profit = .08
	
	parody = assign_parody(request)
	similarity = assign_similarity(request)
	if parody == 3 and similarity == 2:
		return (2, 'The case law is a bit contradictory on this, so you are testing your luck!')
	parody_similarity = {(1, 1): 0.35, (1, 2): 0.65, (1, 3): 0.65, (2, 1): 0.35, (2, 2): 0.1, (2, 3): 0, (3, 1): 0.35, (3, 2): 0,(3, 3): 0}
	print str((parody, similarity))
	print parody_similarity.get((parody, similarity))
	print noncommercial
	print profit
	if parody_similarity.get((parody, similarity)) + noncommercial + profit >= 0.5:
		return (1, 'Congrats! We think this is probably fair use')
	else:
		return (0, 'EESSHH, maybe go back to the drawing board on this one?')


def code_determination(request):

	if request.form.get('purpose') == 'personal-use':
		return (1, 'If you are writing  the code for your own personal enjoyment, go for it!')

	if request.form.get('similar') == 'yes-sim':
		print "yes-sim"
		similarity = 1
	else:
		print request.form.get('similar')
		similarity = 0

	if request.form.get('function') == 'functional':
		functional = 3
	elif request.form.get('function') == 'somewhat-functional':
		functional = 2
	else:
		functional = 1

	print (functional, similarity)
	gen_sim = { (1, 0): 1, (1, 1): 0, (2, 0): 1, (2, 1): 0, (3, 0): 1, (3, 1): 1}
	print request.form.get('market-share')
	if (functional, similarity) == (2, 1) and int(request.form.get('market-share')) < 5 and request.form.get('access') == 'no-access':
		return (2, 'Given that the program is not cutting a huge market share and you had no access to the original code, we think this could go either way!')
	if gen_sim.get((functional, similarity)) == 0:
		if request.form.get('access') == 'no-access':
			return (2, 'Looks like you fail the abstraction-filtration-comparison test, but you didn\'t have access to the code! This could go either way.')
		return (gen_sim.get((functional, similarity)), 'Sigh, looks like you need hit delete-all on your program!')
	else:
		return (gen_sim.get((functional, similarity)), 'Looks like you are good to go!')

def lit_determination(request):
	fanfiction = (request.form.get('nature') == 'fan-fic')
	parody = (request.form.get('parody') == 'yes')
	character_similarity = request.form.get('char-sim')
	character_unique = (request.form.get('char-unique') == 'yes')
	set_similarity = request.form.get('set-sim')
	set_unique = (request.form.get('set-unique') == 'yes')
	plot_similiarity = request.form.get('plot-sim')
	plot_unique = (request.form.get('plot-unique') == 'yes')
	intuition = (request.form.get('int-test') == 'int-similar')
	noncommercial = (request.form.get('purpose') == 'noncommercial')

	# return if parody
	if fanfiction: 
		if parody: 
			return (1, 'Fair use! Like The Wind Done Gone, you critique basic precepts in the work')
	c = 0
	s = 0
	p = 0

	# if the characters are similar (2, 3)
	if character_similarity == 'char-similar' or character_similarity == 'char-very-similar': 
		# if the characters are generic
		if not character_unique: 
			c = 0
		else: 
			# if they are very similarity - exact copies - using the character!
			if character_similarity == 'char-very-similar': 
				return (0, 'If you copy a very recognizable character - highly likely you are in trouble! Just like Rocky')
			else:
				c = 1
	
	if set_similarity == 'set-similar' or set_similarity == 'set-very-similar': 
		if not set_unique: 
			s = 0
		else: 
			if set_similarity == 'set-very-similar': 
				return (0, 'Not fair use! That setting is too similar')
			else:
				s = 1

	
	if plot_similiarity == 'plot-similar' or plot_similiarity == 'plot-very-similar': # somewhat or very
		if not plot_unique: 
			p = 0
		else: 
			if plot_similiarity == 'plot-very-similar':  
				return (0, 'Not fair use! That plot is too similar')
			else: 
				p = 1
				if s or c or intuition: 
					return (0, 'Not fair use! You have multiple highly recognizable elements that are similar')
	
	# multiple
	if (intuition and c) or (intuition and s) or (c and s):
		return (0, 'Not fair use! You have multiple highly recognizable elements that are similar')

	if s or p or intuition or c:
		if noncommercial:
			return (2, 'It sounds like this might be infringement but you might get a cease-and-desist letter at most!')
		return (0, 'Not fair use! You are selling your work even though it contains a highly recognizable element from the source material')

	return(1, 'Fair Use! Good job :)')

def music_determination(request):
	cover = (request.form.get('nature') == 'cover')
	sampling = (request.form.get('nature') == 'sampling')
	performance = (request.form.get('nature') == 'performance')
	composition_license = 'underlying-music-comp' in request.form.getlist('licensing')
	rec_license = 'sound-recording-license' in request.form.getlist('licensing')
	video = (request.form.get('video') == 'yes')
	sync_license = 'synchronization-license' in request.form.getlist('licensing')
	noncommercial = (request.form.get('purpose') == 'noncommercial')
	broadcasting = (request.form.get('nature') == 'broadcasting')
	perf_license = 'performance-license' in request.form.getlist('licensing')
	sim_comp = (request.form.get('nature') == 'sim-song')
	melody = (request.form.get('melody') == 'yes')
	famous = (request.form.get('famous') == 'yes')
	groove = (request.form.get('vibe') == 'yes')
	lyrics = (request.form.get('lyrics') == 'yes')
	if cover:
		if composition_license:
			if video:
				if sync_license:
					return (1, 'Fair Use! Good job getting all the necessary licensing')
				elif noncommercial:
					return (2, 'Probably infringment - your cover might get taken down without proper licensing! Go get a synchronization license')
				else:
					return(0, 'Infringement! You need a synchronization license for setting music to video')
			else:
				return(1, 'Great job with licensing')
		elif noncommercial:
			return (2, 'Probably infringment - your cover might get taken down without proper licensing! Go get a composition license')
		else:
			return (0, 'Infringement! You need a composition license for a cover')
	if sampling:
		if composition_license and rec_license:
			return (1, 'Good job getting all the necessary licensing')
		else:
			return (2, 'You might get in trouble - go get your composition and recording licenses! Case law shows you can be held for infringement, but industry standard varies widely!')
	if performance:
		if composition_license and perf_license:
			return (1, 'Good job with all the necessary licensing')
		else:
			return (0, 'Violation! Go get a composition and performance license if you want to perform live music')
	if broadcasting:
		if perf_license:
			return (1, 'For broadcasting, you just need a performance license so good to go!')
		return (0, 'Not quite! You just need a performance license. I\'d recommend a blanket license from AsCAP or BMI')
	if sim_comp:
		if not famous and ((melody and groove) or (groove and lyrics) or (melody and lyrics)):
			return (2, 'Might get in trouble. Some judges might just believe that you must have heard the song at some point!')
		if famous and (melody or groove or lyrics):
			return (0, 'Given how famous the song is, we think this is a violation of copyright laws.')
		if melody or groove or lyrics:
			return (2, 'You have some similarities so you could possibly be sued')
	return (1, 'Congrats! You are good')
 
		



	