"""
source : https://gist.github.com/Kodagrux/5b39358d812c0fd8eaf4
"""

def reMap(value, minInput, maxInput, minOutput, maxOutput):

	value = maxInput if value > maxInput else value
	value = minInput if value < minInput else value

	inputSpan = maxInput - minInput
	outputSpan = maxOutput - minOutput

	scaledThrust = float(value - minInput) / float(inputSpan)

	return minOutput + (scaledThrust * outputSpan)