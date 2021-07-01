import org.apache.spark.mllib.clustering.{KMeans, KMeansModel}
import org.apache.spark.mllib.linalg.Vectors

// Load and parse the data
val databat = sc.textFile("/home/hduser/1Project/bdpro/bat.csv")

val parsedDataBat = databat.map(s => Vectors.dense((Vectors.dense(s.split(',').slice(6,8).map(_.toDouble)).toArray) ++ (Vectors.dense(s.split(',').slice(9,10).map(_.toDouble)).toArray))).cache()
//features used for clustering batsmen: strike rate, batting average, highest score

val databowl = sc.textFile("/home/hduser/1Project/bdpro/bowl.csv")
val parsedDataBowl = databowl.map(s => Vectors.dense(s.split(',').slice(9,12).map(_.toDouble).toArray)).cache()
//features used for clustering batsmen: strike rate, bowling average, economy

// Cluster the data into two classes using KMeans
val numClusters = 5
val numIterations = 20

//after evaluating within set sum of squares error for each cluster and plotting it against the number of clusters,
//the optimal number of clusters was found to be 5 for both batsmen and bowlers

//for(numClusters<-2 to 12)
//{
	val clustersbat = KMeans.train(parsedDataBat, numClusters, numIterations)
	val predictions = clustersbat.predict(parsedDataBat)
	predictions.collect()
	// Evaluate clustering by computing Within Set Sum of Squared Errors
	//val WSSSE = clustersbat.computeCost(parsedDataBat)
	//println(numClusters+", "+WSSSE)
//}
//println("Bowler Cluster:\nNumClusters, WSSE")
//for(numClusters<-2 to 12)
//{
	val clustersbowl = KMeans.train(parsedDataBowl, numClusters, numIterations)
	val predictionsbowl = clustersbowl.predict(parsedDataBowl)
	predictionsbowl.collect()
	// Evaluate clustering by computing Within Set Sum of Squared Errors
	//val WSSSE = clustersbowl.computeCost(parsedDataBowl)
	//println(numClusters+", "+WSSSE)
//}

