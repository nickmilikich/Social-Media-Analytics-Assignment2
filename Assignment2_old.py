import tweepy
from datetime import datetime
import json

# Accepts two strings a and b
# Returns a float of the Jaccard distance between the two sets as computed from the
# formula given in the assignment description
def jaccard_distance(a, b):
	a = remove_tags(a)
	a = process_text(a)
	b = remove_tags(b)
	b = process_text(b)
	u = union(a,b)
	i = intersect(a,b)
	return 1.0 - float(len(i)) / float(len(u))

# Accepts two strings a and b
# Returns a list of strings that represents the union of the two sets, a list of
# all words that appear in either set
def union(a,b):
	a = a.split()
	b = b.split()
	a = set(a)
	b = set(b)
	return a | b

# Accepts two strings a and b
# Returns a list of strings that represents the intersection of the two sets, a list
# of all words that appear in both sets
def intersect(a,b):
	a = a.split()
	b = b.split()
	a = set(a)
	b = set(b)
	return a & b

# Accepts a string text
# Returns the string without any "RT" or "@handle" tags or links, words beginning with "http"
# Also removes any hashtage characters but keeps the words after the # symbol
def remove_tags(text):
	words = text.split()
	ret = ""
	for word in words:
		if word[0] == '#':
			ret = ret + word[1:] + " "
		elif not ((word[0:2] == "RT") | (word[0] == '@') | (word[0:4] == "http")):
			ret = ret + word + " "
	return ret

# Returns each line of the file f as a string, excluding newlines and any commas
# at the end of the line
def get_ids(f):
	nums = []
	for line in f:
		line = line.rstrip()
		if line[-1] == ",":
			nums.append(int(line[:-1]))
		else:
			nums.append(int(line))
	return nums

# Accepts a string s
# Returns the string with all punctuation removed and with all characters converted
# to lower case
def process_text(s):
	return ''.join(ch.lower() for ch in s if ((ch.isalnum()) | (ch == " ")))

def assign_first_clusters(centroids_id, tweets_dict, tweets_text, centroids_text, tweets_id):
	clusters_old = []
	[ clusters_old.append([0]) for i in range(len(centroids_id)) ]
	for i in range(len(tweets_dict)):
		min_distance = jaccard_distance(tweets_text[i], centroids_text[0])
		min_index = 0
		for j in range(1,len(centroids_id)):
			d = jaccard_distance(tweets_text[i], centroids_text[j])
			if d < min_distance:
				min_distance = d
				min_index = j
		if clusters_old[min_index][0] == 0:
			clusters_old[min_index][0] = tweets_id[i]
		else:
			clusters_old[min_index].append(tweets_id[i])
	return clusters_old

def assign_clusters(centroids_id, tweets_dict, tweets_text, centroids_text, tweets_id):
	clusters_new = []
	[ clusters_new.append([0]) for i in range(len(centroids_id)) ]
	for i in range(len(tweets_dict)):
		min_distance = jaccard_distance(tweets_text[i], centroids_text[0])
		min_index = 0
		for j in range(1,len(centroids_text)):
			d = jaccard_distance(tweets_text[i], centroids_text[j])
			if d < min_distance:
				min_distance = d
				min_index = j
		if clusters_new[min_index][0] == 0:
			clusters_new[min_index][0] = tweets_id[i]
		else:
			clusters_new[min_index].append(tweets_id[i])
	return clusters_new

# Computes new centroids from the intersect/union of the cluster
def compute_new_centroids(clusters_old, tweets_dict):
	centroids_text = []
	for i in range(len(clusters_old)):
		words = set([])
		for id in clusters_old[i]:
			text = tweets_dict[id]
			text = remove_tags(text)
			text = process_text(text)
			if len(words) == 0:
				words = set(text.split())
			else:
##### This is the line where you can modify how the centroid is computed #####				
				words = words | set(text.split())
		centroids_text.append(list(words))

	# Converts each centroid from a set to a string
	for i in range(len(centroids_text)):
		centroids_text[i] = " ".join(centroids_text[i])

	return centroids_text

# Computes new centroids from the most common tweet of the cluster
"""def compute_new_centroids(clusters_old, tweets_dict):
	centroids_text = []
	for i in range(len(clusters_old)):
		tweets = []
		for id in clusters_old[i]:
			text = tweets_dict[id]
			text = remove_tags(text)
			text = process_text(text)
			tweets.append(text)
		#print(tweets)
		#print(most_frequent(tweets))
		try:
			centroids_text.append(most_frequent(tweets))
		except:
			words = []
			for j in range(len(tweets)):
				t = tweets[j].split()
				for w in t:
					words.append(w)
			centroids_text.append(" ".join(list(set(words))))

	return centroids_text"""

# Computes new clusters from the average distance of a tweet to the tweets in a cluster
def compute_new_centroids(clusters_old, tweets_dict):
	centroids_text = []
	for i in range(len(clusters_old)):
		tweets = []
		for id in clusters_old[i]:
			text = tweets_dict[id]
			text = remove_tags(text)
			text = process_text(text)
			tweets.append(text)
		#print(tweets)
		#print(most_frequent(tweets))
		try:
			centroids_text.append(most_frequent(tweets))
		except:
			words = []
			for j in range(len(tweets)):
				t = tweets[j].split()
				for w in t:
					words.append(w)
			centroids_text.append(" ".join(list(set(words))))

	return centroids_text

def most_frequent(vec):
	counter = 0
	elem = vec[0]
	for i in vec:
		curr_frequency = vec.count(i)
		if curr_frequency > counter:
			counter = curr_frequency
			elem = i
	if counter == 1:
		raise RuntimeError("Most frequent element not defined")
	return elem

def main():

	# Read in tweets from Tweets.json and store them as maps in 'tweets'
	tweet_file = open("Tweets.json", 'r')
	tweets = []
	for line in tweet_file:
		tweets.append(json.loads(line))
	tweet_file.close()

	# Store the text of each tweet, after removing RT beginning, in 'tweets_text'
	tweets_text = []
	for t in tweets:
		tweets_text.append(t["text"])

	# Creates a dictionary pairing the ID and text of each tweet for use in the
	# K-means clustering algorithm
	tweets_id = []
	for t in tweets:
		tweets_id.append(t["id"])
	tweets_dict = {tweets_id[i]: tweets_text[i] for i in range(len(tweets_text))}

	# Read in the list of IDs for the centroids from InitialSeeds.txt and store
	# the list in centroids_id
	seed_file = open("InitialSeeds.txt", 'r')
	centroids_id = get_ids(seed_file)
	seed_file.close()

	# Store the text of the centroid tweets in centroids_text
	centroids_text = []
	for id in centroids_id:
		centroids_text.append(tweets_dict[id])

	# Assign each tweet to a cluster
	# For each tweet, compute the Jaccard distance to each of the centroids
	# Each tweet is assigned to the cluster with the least Jaccard distance
	clusters_old = assign_first_clusters(centroids_id, tweets_dict, tweets_text, centroids_text, tweets_id)

	# Compute the cenroids of the new clusters
	centroids_text = compute_new_centroids(clusters_old, tweets_dict)

	# Second round of assigning each tweet to a cluster
	# For each tweet, compute the Jaccard distance to each of the centroids
	# Each tweet is assigned to the cluster with the least Jaccard distance
	clusters_new = assign_clusters(centroids_id, tweets_dict, tweets_text, centroids_text, tweets_id)

	test = []

	while clusters_old != clusters_new:
		clusters_old = clusters_new
		centroids_text = compute_new_centroids(clusters_old, tweets_dict)
		clusters_new = assign_clusters(centroids_id, tweets_dict, tweets_text, centroids_text, tweets_id)
		test.append(centroids_text)
		print(clusters_old == clusters_new)
		try:
			print(test[-1] == test[-3])
		except:
			pass

	result_file = open("Assignment2_output.txt", 'w')

	result_file.write("Cluster assignments for tweets in Boston Marathon Bombing Event Tweet Dataset Tweets.json\n\n\n")

	"""for i in range(len(clusters_old)):
		result_file.write(tweets_dict[centroids_id[i]].encode("utf-8") + "\n")
		for id in clusters_old[i]:
			result_file.write(tweets_dict[id].encode("utf-8") + "\n")
			result_file.write(str(jaccard_distance(process_text(remove_tags(tweets_dict[centroids_id[i]])), process_text(remove_tags(tweets_dict[id])))) + "\n")
		result_file.write("\n\n\n\n")

	for i in range(len(clusters_new)):
		result_file.write(centroids_text[i].encode("utf-8") + "\n")
		for id in clusters_new[i]:
			result_file.write(tweets_dict[id].encode("utf-8") + "\n")
			result_file.write(str(jaccard_distance(centroids_text[i], process_text(remove_tags(tweets_dict[id])))) + "\n")
		result_file.write("\n\n\n\n")"""

	for i in range(len(clusters_new)):
		result_file.write("Cluster " + str(i+1) + ": ")
		for j in range(len(clusters_new[i])-1):
			result_file.write(str(clusters_new[i][j]) + ", ")
		result_file.write(str(clusters_new[i][len(clusters_new[i])-1]) + "\n")

	result_file.close()

if __name__ == "__main__":
	main()


































