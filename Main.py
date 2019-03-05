import os
import pickle

import Analysis
import GeneticAlgorithm
import ProfitTest

numberOfProcess=4
an = Analysis.Analysis()
ga = GeneticAlgorithm.GeneticAlgorithm(an, PRS=numberOfProcess)
bestName = ga.start()

pickle_path = os.path.dirname(os.path.abspath(__file__)) + '/pickle/profittest.pickle'
with open(pickle_path, 'wb') as mypoldata:
    pickle.dump(ga, mypoldata)			# ga = GeneticAlgorithm
    pickle.dump(an, mypoldata)			# an = Analysis
    pickle.dump(bestName, mypoldata)	# bestName = ga.start()

pt = ProfitTest.ProfitTest(ga, an, bestName)
