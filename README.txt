Team #32 - KVS - IPL Project

Step 1:
For clustering batsmen and bowlers, Clusters.scala should be run through Spark.
The input files contain batsmen and bowlers data in .CSV format.

Step 2:
Load the clustered data and player vs player(pvp) data into hive.
The probabilities are estimated using Probability.scala, which runs a HiveQL query iteratively for each cluster pair.
The output of Probability.scala is stored in a CSV file, where the entries in each row are of the form:
<batsman cluster number, bowler cluster number, number of times 0 was scored, number of times 1 was scored, ..., number of times wickets fell, total number of balls faced>
This data is converted into probabilities by running Prob.java.
The final output is of the form:
<batsman cluster number, bowler cluster number, probability of scoring 0, probability of scoring 1, ..., probability of getting out>

Step 3:
Run Project.py through pyspark. The 2 input files will contain the team name in the first row, batting order in the 2nd, and the bowling order in the 3rd row, all in .CSV format.
The output shows us the final score of each team, and the winner of the match.
