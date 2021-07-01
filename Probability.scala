val sqlContext = new org.apache.spark.sql.hive.HiveContext(sc)
var a=0
var b=0
for(a <- 0 to 4)
{
	for(b <- 0 to 4)
	{
		var clust_det = sqlContext.sql("select sum(zeroes), sum(ones), sum(twos), sum(threes), sum(fours), sum(fives), sum(sixes), sum(sevens), sum(dismissed), sum(balls) from (select distinct batsmen.player as bat, bowlers.player as bowl from batsmen join bowlers where batsmen.cluster="+a+" and bowlers.cluster="+b+") players join pvp where bat=batsman and bowl=bowler")
		clust_det.foreach(x=>println(a+","+b+"\n"+x))
	}
}
