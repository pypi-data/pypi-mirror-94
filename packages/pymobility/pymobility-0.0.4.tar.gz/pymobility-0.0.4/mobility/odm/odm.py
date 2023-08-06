import time
from datetime import datetime
from dateutil import relativedelta
from pyspark.sql import functions as F
from pyspark.sql.window import Window


class OriginDestinationMigration:

    def __init__(self, adm_col, delta_loc, out_loc, record_filter=5, spark=None):
        self.spark = spark
        self.adm_col = adm_col
        self.delta_loc = delta_loc
        self.out_loc = out_loc
        self.record_filter = record_filter

        self.sjr = spark.read.format('delta').option("header", "true").load(delta_loc)

    @staticmethod
    def quality_control_filter(sdf, records):
        # filter out the IDs which have less than "records" number of records
        d = sdf.groupby('device_id').count().where(F.col('count') >= records)
        return sdf.join(d, on=["device_id"], how="inner")

    @staticmethod
    def extract(sdf, from_date, to_date):
        from_t = time.mktime(datetime.strptime(from_date, "%Y/%m/%d").timetuple())
        to_t = time.mktime(datetime.strptime(to_date, "%Y/%m/%d").timetuple())

        timestamps_t = (from_t, to_t)
        mobility_t = sdf.where(F.col('timestamp').between(*timestamps_t))

        return mobility_t

    def _get_od_matrix(self, from_date, to_date):
        extracted_data = self.extract(self.sjr, from_date, to_date)

        quality_filtered_data = self.quality_control_filter(extracted_data, self.record_filter)

        w = Window.partitionBy('device_id')
        max_table = quality_filtered_data.withColumn('maxtimestamp', F.max('timestamp').over(w)).where(
            F.col('timestamp') == F.col('maxtimestamp')).dropDuplicates()

        min_table = quality_filtered_data.withColumn('mintimestamp', F.min('timestamp').over(w)).where(
            F.col('timestamp') == F.col('mintimestamp')).dropDuplicates()

        # SQL operations
        max_table.createOrReplaceTempView('maxtable')
        min_table.createOrReplaceTempView('mintable')

        merged_table = self.spark.sql(
            f"""
                SELECT mxt.device_id, mxt.{self.adm_col} as dest, mnt.{self.adm_col} as origin
                FROM maxtable AS mxt JOIN mintable AS mnt
                ON mxt.device_id = mnt.device_id
            """
        )

        merged_table.createOrReplaceTempView('mergedtable')
        grouped_data = merged_table.groupBy('origin', 'dest')
        result = (grouped_data.agg({"*": "count"}))

        return result

    def get_od_matrix(self, from_date, to_date):
        return self._get_od_matrix(from_date, to_date)

    def get_net_migration(self, from_date, to_date):
        od_matrix = self.get_od_matrix(from_date, to_date)

        initial_samples = od_matrix.groupby('origin').agg({'count(1)': 'sum'}).withColumnRenamed('sum(count(1))',
                                                                                                 'origin_total')
        final_samples = od_matrix.groupby('dest').agg({'count(1)': 'sum'}).withColumnRenamed('sum(count(1))',
                                                                                             'dest_total')

        joined_samples = initial_samples.join(final_samples, initial_samples.origin == final_samples.dest,
                                              how='outer').fillna(0, ['origin_total', 'dest_total'])
        joined_samples = joined_samples.withColumn(self.adm_col, F.coalesce(*[i for i in ['origin', 'dest']])).drop(
            'origin', 'dest')
        joined_samples = joined_samples.withColumn('net_movement', F.col('dest_total') - F.col('origin_total'))
        joined_samples = joined_samples.withColumn('net_movement_pct',
                                                   F.col('net_movement') / F.col('origin_total')).drop('origin_total',
                                                                                                       'dest_total')

        return joined_samples


class EventOriginDestinationMigration:

    def __init__(self, adm_col, delta_loc, out_loc, left_padding_days, right_padding_days, spark=None, record_filter=0):
        self.spark = spark
        self.adm_col = adm_col
        self.delta_loc = delta_loc
        self.out_loc = out_loc
        self.left_padding_days = left_padding_days
        self.right_padding_days = right_padding_days

        self.sjr = spark.read.format('delta').option("header", "true").load(delta_loc)
        self.record_filter = record_filter

    @staticmethod
    @F.udf
    def mode(x):
        from collections import Counter
        return Counter(x).most_common(1)[0][0]

    @staticmethod
    def quality_control_filter(sdf, records):
        # filter out the IDs which have less than "records" number of records
        d = sdf.groupby('device_id').count().where(F.col('count') >= records)
        return sdf.join(d, on=["device_id"], how="inner")

    @staticmethod
    def extract(sdf, from_date, to_date):
        from_t = time.mktime(datetime.strptime(from_date, "%Y/%m/%d").timetuple())
        to_t = time.mktime(datetime.strptime(to_date, "%Y/%m/%d").timetuple())

        timestamps_t = (from_t, to_t)
        return sdf.where(F.col('timestamp').between(*timestamps_t))

    def get_date_ends(self, event_date):
        from_date = (
                datetime.strptime(event_date, "%Y/%m/%d") - relativedelta.relativedelta(days=self.left_padding_days)
        ).strftime("%Y/%m/%d")

        to_date = (
                datetime.strptime(event_date, "%Y/%m/%d") + relativedelta.relativedelta(days=self.right_padding_days)
        ).strftime("%Y/%m/%d")
        return (from_date, to_date)

    def _get_od_matrix(self, from_date, to_date):
        extracted_data = self.extract(self.sjr, from_date, to_date)

        quality_filtered_data = self.quality_control_filter(extracted_data, self.record_filter)

        w = Window.partitionBy('device_id')
        max_table = quality_filtered_data.withColumn('maxtimestamp', F.max('timestamp').over(w)).where(
            F.col('timestamp') == F.col('maxtimestamp')).dropDuplicates()

        min_table = quality_filtered_data.withColumn('mintimestamp', F.min('timestamp').over(w)).where(
            F.col('timestamp') == F.col('mintimestamp')).dropDuplicates()

        # SQL operations
        max_table.createOrReplaceTempView('maxtable')
        min_table.createOrReplaceTempView('mintable')

        merged_table = self.spark.sql(
            f"""
                SELECT mxt.device_id, mxt.{self.adm_col} as dest, mnt.{self.adm_col} as origin
                FROM maxtable AS mxt JOIN mintable AS mnt
                ON mxt.device_id = mnt.device_id
            """
        )

        merged_table.createOrReplaceTempView('mergedtable')
        grouped_data = merged_table.groupBy('origin', 'dest')
        result = (grouped_data.agg({"*": "count"}))

        return result

    def get_od_matrix(self, event_date):
        from_date, to_date = self.get_date_ends(event_date)

        return self._get_od_matrix(from_date, to_date)

    def get_net_migration(self, event_date):
        od_matrix = self.get_od_matrix(event_date)

        initial_samples = od_matrix.groupby('origin').agg({'count(1)': 'sum'}).withColumnRenamed('sum(count(1))',
                                                                                                 'origin_total')
        final_samples = od_matrix.groupby('dest').agg({'count(1)': 'sum'}).withColumnRenamed('sum(count(1))',
                                                                                             'dest_total')

        joined_samples = initial_samples.join(final_samples, initial_samples.origin == final_samples.dest,
                                              how='outer').fillna(0, ['origin_total', 'dest_total'])
        joined_samples = joined_samples.withColumn(self.adm_col, F.coalesce(*[i for i in ['origin', 'dest']])).drop(
            'origin', 'dest')
        joined_samples = joined_samples.withColumn('net_movement', F.col('dest_total') - F.col('origin_total'))
        joined_samples = joined_samples.withColumn('net_movement_pct',
                                                   F.col('net_movement') / F.col('origin_total')).drop('origin_total',
                                                                                                       'dest_total')

        return joined_samples
