import json
from Assignment2 import get_ids, assign_first_clusters, assign_new_clusters

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
	seed_file = open("Assignment2_ec_InitialSeeds.txt", 'r')
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
	result_file = open("Assignment2_ec_Clusters.txt", 'w')
	result_file.write("Cluster assignments for tweets in Boston Marathon Bombing Event Tweet Dataset Tweets.json\n")
	result_file.write("Assigned using manually computed initial centroid assignments.\n\n\n")
	for i in range(len(clusters_new)):
		result_file.write("Cluster " + str(i+1) + ": ")
		for j in range(len(clusters_new[i])-1):
			result_file.write(str(clusters_new[i][j]) + ", ")
		result_file.write(str(clusters_new[i][len(clusters_new[i])-1]) + "\n\n")
	result_file.close()

if __name__ == "__main__":
	main()



























