from pyspark.sql import SparkSession
from mobility.odm import OriginDestinationMigration


spark = SparkSession.builder.master("local").appName("mobility").getOrCreate()
od_matrix = OriginDestinationMigration(spark, 'L4_CODE', 'test_1.csv', 'haha', 1)
print(od_matrix.get_od_matrix("2019/01/01", "2020/10/10"))
