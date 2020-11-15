import json
import random
from Assignment2 import jaccard_distance, assign_first_clusters

# The most important method; calculates and returns the optimal initial centroid assignments
# This method implements a modified version of the K-means++ algorithm for centroid assignment
# num_iterations specifies the maximum number of centroid assignments to search for the optimal one
# num_centroids specifies the number of centroids to find for the data set
# The method generates num_iterations lists of num_centroids centroids
# For each assignment, it goes through one iteration of cluster assignments
# and for each, calculates the total Jaccard distance between each centroid and each tweet in that cluster
# It returns the assignment with the least total Jaccard distance
def calculate_centroids(num_iterations, num_centroids, tweets_id, tweets_dict, tweets_text):
	centroids = get_centroid_sample(num_centroids, tweets_id, tweets_dict)
	clusters = assign_first_clusters(centroids, tweets_dict, tweets_text, tweets_id)
	total_dist = get_total_distance(clusters, centroids, tweets_id, tweets_dict)
	for i in range(1, num_iterations):
		new_centroids = get_centroid_sample(num_centroids, tweets_id, tweets_dict)
		new_clusters = assign_first_clusters(new_centroids, tweets_dict, tweets_text, tweets_id)
		new_dist = get_total_distance(new_clusters, new_centroids, tweets_id, tweets_dict)
		if new_dist < total_dist:
			total_dist = new_dist
			clusters = new_clusters
			centroids = new_centroids
	return centroids

# Accepts a list of cluster assignments and centroids
# Returns the total Jaccard distance between each tweet in a cluster and the centroid of that cluster
def get_total_distance(clusters, centroids, tweets_id, tweets_dict):
	tot = 0.0
	for i in range(len(clusters)):
		for j in range(len(clusters[i])):
			tot = tot + jaccard_distance(tweets_dict[clusters[i][j]], tweets_dict[centroids[i]])
	print(tot)
	return tot

# Calculates and returns a random group of num_centroids centroids from the list of tweets
# This random group is calculated using a version of the K-means++ centroid assignment algorithm for K-means clustering
# First, a centroid is randomly picked from the list of tweets
# Then, the distance D between that centroid and each other tweet is calculated
# The next centroid is chosen randomly from the remaining tweets with probability proportional to D^2
def get_centroid_sample(num_centroids, tweets_id, tweets_dict):

	centroids = []
	centroids.append(tweets_id[random.randrange(len(tweets_id))])

	while len(centroids) < num_centroids:
		dist = get_dist(centroids, tweets_id, tweets_dict)

		p = []
		for elem in dist:
			p.append(elem ** 2)
		probs = probability_distribution(p)

		rand = random.random()
		index = get_result(probs, rand)
		while centroids.count(tweets_id[index]) > 0:
			rand = random.random()
			index = get_result(probs, rand)
		centroids.append(tweets_id[index])

	return centroids

# Converts a list of relative frequencies to a valid probability distribution by dividing each element by the sum of the
# supplied list
def probability_distribution(vec):
	tot = sum(vec)
	ret = []
	for elem in vec:
		ret.append(elem / tot)
	return ret

# Accepts a list of centroids
# Returns a list containing, for each tweet, the distance between that tweet and the nearest centroid
def get_dist(centroids, tweets_id, tweets_dict):
	dist = []
	for i in range(len(tweets_id)):
		d = []
		for c in range(len(centroids)):
			if i == centroids[c]:
				dist.append(0.0)
				continue
			d.append(jaccard_distance(tweets_dict[tweets_id[i]], tweets_dict[centroids[c]]))
		dist.append(min(d))
	return dist

# Accepts probs, a valid probability distribution, and num, a random real number in the range [0,1)
# Returns the index of probs corresponding to the cumulative probability window in which num lies
# Ex: probs corresponds to the probability distribution for five equally likely events, probs = [0.2, 0.2, 0.2, 0.2, 0.2]
# As a cumulative probability distribution, probs_cum = [0.2, 0.4, 0.6, 0.8, 1.0]
# If num = 0.3, then get_result(probs, num) returns 1 since 1 is the lowest index i for which probs_cum[i] > 0.3
def get_result(probs, num):
	index = 0
	while sum(probs[0:(index+1)]) < num:
		index = index + 1
	return index

def main():

	# Read in tweets from Tweets.json and store them as maps in tweets
	tweet_file = open("Tweets.json", 'r')
	tweets = []
	for line in tweet_file:
		tweets.append(json.loads(line))
	tweet_file.close()

	# Store the text of each tweet in tweets_text
	tweets_text = []
	for t in tweets:
		tweets_text.append(t["text"])

	# Creates a dictionary pairing the ID and text of each tweet for use in the
	# K-means clustering algorithm
	tweets_id = []
	for t in tweets:
		tweets_id.append(t["id"])
	tweets_dict = {tweets_id[i]: tweets_text[i] for i in range(len(tweets_text))}

	# Calls the method calculate_centroids, the focus method of this file, to assign centroids
	centroids = calculate_centroids(25, 25, tweets_id, tweets_dict, tweets_text)

	# Writes the resulting centroids to the output file
	result_file = open("Assignment2_ec_InitialSeeds.txt", 'w')
	for i in range(len(centroids)-1):
		result_file.write(str(centroids[i]) + ",\n")
	result_file.write(str(centroids[-1]) + "\n")
	result_file.close()

if __name__ == "__main__":
	main()


































