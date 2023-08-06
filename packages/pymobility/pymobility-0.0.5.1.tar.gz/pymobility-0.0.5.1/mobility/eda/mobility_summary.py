import pyspark.sql.functions as F


class MobilitySummary:

    def __init__(self, delta_loc, adm_col, quality_filter=5, spark=None):
        self.sjr = spark.read.format('delta').option("header", "true").load(delta_loc)
        self.adm_col = adm_col

        if quality_filter > 0:
            self.sjr = self.quality_control_filter(self.sjr, quality_filter)

    @staticmethod
    def quality_control_filter(sdf, records):
        # filter out the IDs which have less than "records" number of records
        d = sdf.groupby('device_id').count().where(F.col('count') >= records)
        sdf = sdf.join(d, on=["device_id"], how="inner")
        return sdf

    def _get_records_per_admin(self, adm_col):
        mobility_record_count = self.sjr.groupBy(adm_col).count()
        mobility_record_count = mobility_record_count.withColumnRenamed("count", "frequency")
        return mobility_record_count

    def _get_devices_per_admin(self, adm_col):
        mobility_device_count = self.sjr.groupBy(adm_col).agg(F.countDistinct("device_id")) \
            .withColumnRenamed("count(DISTINCT device_id)", "unique_devices")
        return mobility_device_count

    def _get_records_per_date_admin(self, adm_col):
        sjr_with_date = self.sjr.withColumn("date", F.from_unixtime("timestamp", format="yyyy_MM_dd"))
        mobility_record_date_count = sjr_with_date.groupBy(adm_col, 'date').count().withColumnRenamed("count", "num_records")
        return mobility_record_date_count

    def _get_devices_per_date_admin(self, adm_col):
        sjr_with_date = self.sjr.withColumn("date", F.from_unixtime("timestamp", format="yyyy_MM_dd"))
        mobility_device_date_count = sjr_with_date.groupBy(adm_col, 'date').agg(
            F.countDistinct("device_id")
        ).withColumnRenamed("count(DISTINCT device_id)", "unique_devices")
        return mobility_device_date_count

    def get_records_per_admin(self):
        return self._get_records_per_admin(self.adm_col)

    def get_records_per_date_admin(self):
        return self._get_records_per_date_admin(self.adm_col)

    def get_devices_per_admin(self):
        return self._get_devices_per_admin(self.adm_col)

    def get_devices_per_date_admin(self):
        return self._get_devices_per_date_admin(self.adm_col)

    def get_frequency_map(self):
        frequency_table = self.sjr.groupBy('device_id') \
            .count() \
            .withColumnRenamed("count", "frequency") \
            .groupBy('frequency') \
            .count() \
            .orderBy(F.asc("frequency"))
        return frequency_table
