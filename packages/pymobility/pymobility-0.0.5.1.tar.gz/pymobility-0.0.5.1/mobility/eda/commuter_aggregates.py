import time
from itertools import chain
from datetime import datetime
from dateutil import relativedelta
from pyspark.sql import functions as F
from pyspark.sql.window import Window
from pyspark.ml.feature import Bucketizer
from pyspark.sql.types import IntegerType


class CommuterAggregation:

    def __init__(self, adm_col, delta_loc, record_filter=5, spark=None):
        self.adm_col = adm_col
        self.sjr = spark.read.format('delta').option("header", "true").load(delta_loc)

    @staticmethod
    def extract(sdf, from_date, to_date):
        from_t = time.mktime(datetime.strptime(from_date, "%H/%M").timetuple())
        to_t = time.mktime(datetime.strptime(to_date, "%H/%M").timetuple())

        timestamps_t = (from_t, to_t)
        mobility_t = sdf.where(F.col('timestamp').between(*timestamps_t))

        return mobility_t

    @staticmethod
    def get_hour_appended_data(sdf, buckets):
        sdf_with_date = sdf.withColumn("date", F.from_unixtime("timestamp", format="yyyy-MM-dd"))
        sdf_with_hour = sdf_with_date.withColumn("hour", F.from_unixtime("timestamp", format="HH").cast(IntegerType()))

        bucketizer = Bucketizer(splits=buckets, inputCol="hour", outputCol="bucket")
        hour_data = bucketizer.setHandleInvalid("keep").transform(sdf_with_hour)

        dict_items = [(0, f"{buckets[0]}-{buckets[1] + 1}")] + [(i, f"{buckets[i] + 1}-{buckets[i + 1] + 1}") for i in
                                                                range(1, len(buckets) - 1)]
        mapping = F.create_map([F.lit(x) for x in chain(*dict_items)])
        hour_data = hour_data.withColumn('hour_range', mapping[hour_data['bucket']])

        return hour_data

    def get_record_aggregates(self, periods):
        periods = [periods[0]] + [periods[i] - 1 for i in range(1, len(periods))]

        sjr_with_date = self.sjr.withColumn("date", F.from_unixtime("timestamp", format="yyyy-MM-dd"))

        hour_data = self.get_hour_appended_data(self.sjr, periods)
        hour_data = hour_data.groupby(self.adm_col, "hour_range").count()

        start = datetime.strptime(sjr_with_date.agg({'date': 'min'}).toPandas()['min(date)'][0], '%Y-%m-%d')
        end = datetime.strptime(sjr_with_date.agg({'date': 'max'}).toPandas()['max(date)'][0], '%Y-%m-%d')

        aggregates = hour_data.withColumn('daily_records', F.col('count') / (end - start).days).drop('count')

        return aggregates

    def get_device_aggregates(self, periods):
        periods = [periods[0]] + [periods[i] - 1 for i in range(1, len(periods))]

        hour_data = self.get_hour_appended_data(self.sjr, periods)
        hour_data = hour_data.dropDuplicates([self.adm_col, 'date', 'hour_range', 'device_id'])
        hour_data = hour_data.groupby(self.adm_col, "date", "hour_range").count()

        aggregates = hour_data.groupby(self.adm_col, 'hour_range').agg({'count': 'mean'}).withColumnRenamed(
            "avg(count)", "daily_devices")

        return aggregates