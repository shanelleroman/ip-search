def fair_use_determination(request):
	print "inside fair use determination!"
	purpose = request.form.get('purpose')
	if purpose == 'educational':
		return (1,'Automatically fair use - education is a specific carve out for fair use!')
	if request.args.get('type') == 'vis-art':
		return visual_art_determination(request)
	elif request.args.get('type') == 'code':
		return code_determination(request)

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
	noncommercial = (request.form.get('purpose') == 'noncommercial')
	profit = (int(request.form.get('market-share')) > int(5))
	parody = assign_parody(request)
	similarity = assign_similarity(request)
	if parody == 3 and similarity == 2:
		return (2, 'The case law is a bit contradictory on this, so you are testing your luck!')
	parody_similarity = {(1, 1): 0.35, (1, 2): 0.65, (1, 3): 0.65, (2, 1): 0.35, (2, 2): 0.1, (2, 3): 0, (3, 1): 0.35, (3, 2): 0,(3, 3): 0}
	if parody_similarity.get((parody, similarity)) + noncommercial + profit >= 0.5:
		return (1, 'Congrats! We think this is probably fair use')
	else:
		return (0, 'EESSHH, maybe go back to the drawing board on this one?')


def code_determination(request):
	if request.form.get('access') == 'no-access':
		return (1, 'If you do not have access to the code, this is probably fair use!')
	if request.form.get('purpose') == 'personal-use':
		return (1, 'If you are writing for the code for your own personal enjoyment, go for it!')

	if request.form.get('similarity') == 'yes-sim':
		similarity = 1
	else:
		similarity = 0

	if request.form.get('function') == 'functional':
		functional = 3
	elif request.form.get('function') == 'somewhat-functional':
		functional = 2
	else:
		functional = 1

gen_sim = { (1, 0): 1, (1, 1): 0, (2, 0): 1, (2, 1): 0, (3, 0): 1, (3, 1): 1}
return gen_sim.get((similarity, functional))






# def ttcode(noncommercial_use, profit, access, gen, sim): 
# 	if access == 0: 
# 		return 1
# 	if (profit == 0): 
# 		return 1
# 	dict = { (1, 0): 1, (1, 1): 0, (2, 0): 1, (2, 1): 0, (3, 0): 1, (3, 1): 1}
# 	return dict[(gen, sim)] 

# def ttbook(noncommercial_use, profit, general_story_elements):
# 	fanfiction 
# 	if fanfiction: 
# 		if parody: 
# 			return 1
# 	c = 1
# 	if charsim: 
# 		if (chargen): 
# 			c = 0
# 		else: 
# 			if (charsim == 3): 
# 				if noncommercial_use: 
# 					return 2
# 				else: 
# 					return 1
# 			else:
# 				c = 1
# 	else: 
# 		c = 0
# 	s = 1
# 	if setsim: 
# 		if (setgen): 
# 			s = 0
# 		else: 
# 			if (setsim == 3): 
# 				if noncommercial_use: 
# 					return 2
# 				else: 
# 					return 1
# 			else:
# 				s = 1
# 	else: 
# 		s = 0
# 	p = 1
# 	if plotsim: 
# 		if (plotgen): 
# 			p = 0
# 		else: 
# 			if (plotsim == 3): 
# 				if s || c || intuition:  
# 					if noncommercial_use: 
# 						return 2
# 					else: 
# 						return 1
# 				else: 
# 					return 2
# 			else: 
# 				if s || c || intuition:
# 					if noncommercial_use: 
# 						return 1
# 					else: 
# 						return 2
# 	if intution: 
# 		if (s && c) || (s && p)  || (p && c):
# 			return 0
# 		else: 
# 			return 1
# 	return 1

# def ttbook(noncommercial_use, profit, __): 
# 	if 









# 		