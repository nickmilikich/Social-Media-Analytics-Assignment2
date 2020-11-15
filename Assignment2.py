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
# Also removes any hashtag characters but keeps the characters after the # symbol
def remove_tags(text):
	words = text.split()
	ret = ""
	for word in words:
		if word[0] == '#':
			ret = ret + word[1:] + " "
		elif not ((word[0:2] == "RT") | (word[0] == '@') | (word[0:4] == "http")):
			ret = ret + word + " "
	return ret

# Accepts a file f
# Returns each line of the file f as a string, excluding newlines and any commas
# at the end of the line
# Used for reading in the list of twitter IDs in InitialSeeds.txt
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

# Computes and returns the initial cluster assignments
# The return value is a list of 25 lists, each of which contains the IDs of the
# tweets in that cluster
def assign_first_clusters(centroids_id, tweets_dict, tweets_text, tweets_id):
	clusters_old = []
	[ clusters_old.append([0]) for i in range(len(centroids_id)) ]
	for i in range(len(tweets_dict)):
		min_distance = jaccard_distance(tweets_text[i], tweets_dict[centroids_id[0]])
		min_index = 0
		for j in range(1,len(centroids_id)):
			d = jaccard_distance(tweets_text[i], tweets_dict[centroids_id[j]])
			if d < min_distance:
				min_distance = d
				min_index = j
		if clusters_old[min_index][0] == 0:
			clusters_old[min_index][0] = tweets_id[i]
		else:
			clusters_old[min_index].append(tweets_id[i])
	return clusters_old

# Computes and returns any cluster assignments after the first round
# The return value is a list of 25 lists, each of which contains the IDs of the
# tweets in that cluster
def assign_new_clusters(centroids_id, tweets_dict, clusters_old, tweets_text, tweets_id):
	clusters_new = []
	[ clusters_new.append([0]) for i in range(len(centroids_id)) ]
	for i in range(len(tweets_dict)):
		dist = 0.0
		for j in range(len(clusters_old[0])):
			dist = dist + jaccard_distance(tweets_text[i], tweets_dict[clusters_old[0][j]])
		min_dist = dist / float(len(clusters_old[0]))
		min_index = 0
		for j in range(1, len(clusters_old)):
			dist = 0.0
			for k in range(len(clusters_old[j])):
				dist = dist + jaccard_distance(tweets_text[i], tweets_dict[clusters_old[j][k]])
			avg_dist = dist / float(len(clusters_old[j]))
			if avg_dist < min_dist:
				min_dist = avg_dist
				min_index = j

		if clusters_new[min_index][0] == 0:
			clusters_new[min_index][0] = tweets_id[i]
		else:
			clusters_new[min_index].append(tweets_id[i])

	return clusters_new


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

	# Read in the list of IDs for the centroids from InitialSeeds.txt and store
	# the list in centroids_id
	seed_file = open("InitialSeeds.txt", 'r')
	centroids_id = get_ids(seed_file)
	seed_file.close()

	# Assign each tweet to a cluster
	# For each tweet, compute the Jaccard distance to each of the centroids
	# Each tweet is assigned to the cluster with the least Jaccard distance
	clusters_old = assign_first_clusters(centroids_id, tweets_dict, tweets_text, tweets_id)

	# Second round of assigning each tweet to a cluster
	# For each tweet, compute the average Jaccard distance to each of the tweets
	# in a cluster
	# Each tweet is assigned to the cluster with the least average Jaccard
	# distance
	clusters_new = assign_new_clusters(centroids_id, tweets_dict, clusters_old, tweets_text, tweets_id)

	# Repeats the reassignment of tweets to clusters by the above algorithm until
	# successive iterations do not alter the composition of the clusters
	while clusters_old != clusters_new:
		clusters_old = clusters_new
		clusters_new = assign_new_clusters(centroids_id, tweets_dict, clusters_old, tweets_text, tweets_id)

	# Writes the resulting clusters to the output file
	result_file = open("Assignment2_output.txt", 'w')
	result_file.write("Cluster assignments for tweets in Boston Marathon Bombing Event Tweet Dataset Tweets.json\n\n\n")
	for i in range(len(clusters_new)):
		result_file.write("Cluster " + str(i+1) + ": ")
		for j in range(len(clusters_new[i])-1):
			result_file.write(str(clusters_new[i][j]) + ", ")
		result_file.write(str(clusters_new[i][len(clusters_new[i])-1]) + "\n\n")
	result_file.close()

if __name__ == "__main__":
	main()


































