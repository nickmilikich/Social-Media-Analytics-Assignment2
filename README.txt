Assignment 2: Tweets Clustering
Nick Milikich
CSE 60437 Social Sensing & Cyber-Physical Systems
February 17, 2019

This project implements a K-means clustering algorithm that clusters a group of 251 tweets related to the Boston Marathon bombing incident into 25 clusters. The centroids of the initial clusters are stored in InitialSeeds.txt, in the form of 25 tweet IDs, the text of which are to be used as the centroids. The clustering is performed in Assignment2.py, and the results of clustering are written to the output file Assignment2_output.txt. Also implemented is a version of the K-means++ algorithm for assigning initial centroids with which to perform clustering; this is performed in Assignment2_ec.py. The centroids computed using this method are written to the output file Assignment2_ec_InitialSeeds.txt, and clusters are assigned using those initial centroids in Assignment2_ec_check.py. The resulting clusters are written to Assignment2_ec_Clusters.txt.

The clustering algorithm can be run simply by executing the file Assignment2.py, and the K-means++ centroid assignment algorithm can be run by executing Assignment2_ec.py. The clustering algorithm using those centroids can be run by executing Assignment2_ec_check.py. No arguments need to be passed to the programs. This code was tested using Python version 2.7.16.

Running this source code requires that the Python packages json and random be installed.

To run the source code, the following should be included in the same directory (all included in this submission):
   
   - A file named InitialSeeds.txt that contains the IDs of the tweets to be used as initial centroids for the clustering algorithm. The IDs are written one per line and separated by commas.
   - A file named Tweets.json that contains the information for the 251 tweets to be clustered, stored in json format. The tweets are stored one per line.

Full honest disclosure: the centroids computed using the K-means++ algorithm do not result in the same clusters as the centroids provided in InitialSeeds.txt, and the centroids are not even consistent between executions. It is submitted to document the work done towards the extra credit part of this assignment, and in the hope of some partial extra credit.