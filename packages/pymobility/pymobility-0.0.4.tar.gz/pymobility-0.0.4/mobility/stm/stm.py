import time
from datetime import datetime
from dateutil import relativedelta
import pandas as pd

from pyspark.sql import functions as F
from pyspark.sql.functions import from_unixtime, col, lit, month as mth
import pyspark.sql.types as T


class GenericShortTermMigration:

    def __init__(self, spark_session, aggr_admin, home_admin, raw_file_location, stm_range, raw_file_format='delta',
                 distance_filter=False, quality_control_samples=5, home_duration=12, distance=0, end_at_home=False,
                 has_month_filter=False, at_a_stretch=True, fixed_home_period=False,
                 home_period=('2019/01/01', '2020/01/01'),
                 left_padding_days=15, right_padding_days=15, timeframe_months=1):

        spark = spark_session
        self.quality_control_samples = quality_control_samples
        self.aggr_admin = aggr_admin
        self.home_admin = home_admin
        self.sjr_master = spark.read.format(raw_file_format).option("header", "true").load(raw_file_location)
        self.sjr = None
        self.stm_range = stm_range
        self.distance_filter = distance_filter
        self.distance = 0
        self.end_at_home = end_at_home
        self.has_month_filter = has_month_filter
        self.at_a_stretch = at_a_stretch
        self.left_padding_days = left_padding_days
        self.right_padding_days = right_padding_days
        self.timeframe_months = timeframe_months
        self.fixed_home_period = fixed_home_period

        if distance_filter:
            self.set_dist_map(distance)

        if fixed_home_period:
            self.set_device_id_homes(home_period, home_duration)

    def set_device_id_homes(self, home_period, home_duration):

        fixed_period_sdf = self.extract_data(self.sjr_master, home_period[0], home_duration)
        fixed_period_sdf = self.quality_control_filter(fixed_period_sdf, self.quality_control_samples)

        # convert UNIX timestamp to date format
        fixed_period_sdf = fixed_period_sdf.withColumn('date', from_unixtime('timestamp').cast(T.DateType()))

        date_device_sdf = self.date_device_mode(fixed_period_sdf)
        self.device_id_homes = self.append_mode_admin(date_device_sdf, self.aggr_admin)

        if self.aggr_admin != self.home_admin:
            self.device_id_homes = self.append_mode_admin(self.device_id_homes, self.home_admin)

        if self.aggr_admin == self.home_admin:
            self.device_id_homes = self.device_id_homes.dropDuplicates(['device_id']).select(
                col('device_id'), col(self.aggr_admin + '_home')
            )
        else:
            self.device_id_homes = self.device_id_homes.dropDuplicates(['device_id']).select(
                col('device_id'), col(self.aggr_admin + '_home'), col(self.home_admin + '_home')
            )

        # if we want to save home locations for later
        # self.device_id_homes.write.format("delta").mode("overwrite").save("/mnt/CUBEIQ/esapv/India/Unacast/Short Term Migration/One Month Definition/Device ID Homes")

    @staticmethod
    def extract_data(sdf, start_date, no_of_months, by='timestamp'):
        # get the from and to value for the interval
        from_t = datetime.strptime(start_date, "%Y/%m/%d")
        to_t = from_t + relativedelta.relativedelta(months=no_of_months)

        if by == 'timestamp':
            from_t = time.mktime(from_t.timetuple())
            to_t = time.mktime(to_t.timetuple())

        # filter by date range
        timestamps = (from_t, to_t)
        print(timestamps)

        return sdf.where(col(by).between(*timestamps))

    @staticmethod
    def extract_data_by_ends(sdf, start_date, end_date, by='timestamp'):
        # get the from and to value for the interval
        from_t = datetime.strptime(start_date, "%Y/%m/%d")
        to_t = datetime.strptime(end_date, "%Y/%m/%d")

        if by == 'timestamp':
            from_t = time.mktime(from_t.timetuple())
            to_t = time.mktime(to_t.timetuple())

        # filter by date range
        timestamps = (from_t, to_t)
        print(timestamps)

        return sdf.where(col(by).between(*timestamps))

    @staticmethod
    def quality_control_filter(sdf, records):
        # filter out the IDs which have less than "records" number of records
        d = sdf.groupby('device_id').count().where(col('count') >= records)
        sdf = sdf.join(d, on=["device_id"], how="inner")
        return sdf

    def date_device_mode(self, sdf):
        # select MODE L4_CODE for unique device_id and date, so that each device has a L4_CODE for each date

        if self.aggr_admin == self.home_admin:
            device_date_admin_counts = sdf.groupBy(
                ['device_id', 'date', self.aggr_admin]
            ).count()

            sdf = (device_date_admin_counts.groupBy('device_id', 'date').agg(
                F.max(
                    F.struct(F.col('count'), F.col(self.aggr_admin))
                ).alias('max')).select(F.col('device_id'),
                                       F.col('date'),
                                       F.col('max.{}'.format(self.aggr_admin))
                                       )
                   )
            return sdf
        else:
            device_date_admin_counts = sdf.groupBy(
                ['device_id', 'date', self.home_admin, self.aggr_admin]
            ).count()

            sdf = (device_date_admin_counts.groupBy('device_id', 'date').agg(
                F.max(
                    F.struct(F.col('count'), F.col(self.aggr_admin), F.col(self.home_admin))
                ).alias('max')).select(F.col('device_id'),
                                       F.col('date'),
                                       F.col('max.{}'.format(self.home_admin)),
                                       F.col('max.{}'.format(self.aggr_admin))
                                       )
                   )
            return sdf

    @staticmethod
    def append_mode_admin(sdf, column_name):
        # find home by finding mode of L4_CODE
        device_admin_counts = sdf.groupBy(['device_id', column_name]).count()
        result = device_admin_counts.groupBy('device_id').agg(
            F.max(
                F.struct(F.col('count'), F.col(column_name))
            ).alias('max')).select(F.col('device_id'), F.col('max.{}'.format(column_name)))

        sdf = sdf.join(
            result.withColumnRenamed(column_name, column_name + '_home'),
            on=['device_id'],
            how='inner'
        )
        return sdf

    @classmethod
    def set_dist_map(cls, distance):
        adm2_dist = pd.read_csv('../adm2_dist_nogeom.csv', index_col='L2_CODE')
        adm2_dist.drop(['Unnamed: 0'], axis=1, inplace=True)

        adm2_dist.columns = list(adm2_dist.columns[:8]) + list(adm2_dist.columns[8:].astype(float).astype(int))
        adm2_dist.iloc[:, 8:] = adm2_dist.iloc[:, 8:].astype(float) > distance

        cls.adm2_dist_dict = adm2_dist.iloc[:, 8:].to_dict()

    @staticmethod
    def count_outside_home(x, y, end_at_home):
        hah_score = 0

        x = [i for _, i in sorted(zip(y, x))]
        y.sort()

        outside_total = 0.0
        outside_initial = None

        for i in range(len(y) - 1):
            if outside_initial is None and x[i]:
                outside_initial = i

            if x[i] != x[i + 1]:

                outside_total += (y[i + 1] - y[i]).days / 2

                if not x[i + 1]:

                    outside_total += (y[i] - y[outside_initial]).days
                    outside_initial = None

                    if hah_score == 1:
                        hah_score += 1

                elif not hah_score:
                    hah_score += 1

        if hah_score != 2:
            return 1000.0

        if x[-1]:
            if end_at_home:
                return 1000.0

            if outside_initial is not None:
                outside_total += (y[-1] - y[outside_initial]).days

        return outside_total

    @staticmethod
    def count_outside_home_at_a_stretch(x, y, end_at_home):

        outside_home_days = 0

        x = [i for _, i in sorted(zip(y, x))]
        y.sort()

        outside_total = 0.0
        outside_total_t = 0.0
        outside_initial = None

        for i in range(len(y) - 1):
            if x[i]: outside_home_days += 1
            if outside_initial is None and x[i]:
                outside_initial = i
                if i > 0:
                    outside_total_t = (y[i] - y[i - 1]).days / 2

            if x[i] != x[i + 1]:
                if (outside_initial is not None) and (not x[i + 1]):
                    temp = outside_total_t + (y[i] - y[outside_initial]).days + (y[i + 1] - y[i]).days / 2
                    if temp > outside_total:
                        outside_total = temp
                    outside_total_t = 0
                    outside_initial = None

        if x[-1]:

            if end_at_home:
                return 0.0
            if outside_initial is not None:
                temp = outside_total_t + (y[-1] - y[outside_initial]).days
                if temp > outside_total:
                    outside_total = temp
            else:
                temp = (y[-1] - y[-2]).days / 2
                if temp > outside_total:
                    outside_total = temp
        if outside_home_days < 3:
            return 0.0

        return outside_total

    def _export(self, export_location):
        # this is where things need to be changed
        # add another column, is_outside_home which gives if someone is outside his/her home on some date
        # sjr_2019_1 = sjr_2019_1.withColumn("is_outside_home", col("admin2_home") != col("L2_CODE"))

        if self.distance_filter:
            dictionary = GenericShortTermMigration.adm2_dist_dict.copy()

        def is_outside_home(x, y):
            x = int(x)
            y = int(y)
            if x not in dictionary or y not in dictionary:
                return True

            return dictionary[x][y]

        is_outside_home_udf = F.udf(is_outside_home, T.BooleanType())

        if self.distance_filter:
            self.sjr = self.sjr.withColumn(
                "is_outside_home", is_outside_home_udf(
                    col(self.home_admin + '_home'),
                    col(self.home_admin),
                    lit(self.distance_filter),
                )
            )
        else:
            self.sjr = self.sjr.withColumn("is_outside_home", col(self.home_admin + '_home') != col(self.home_admin))

        if self.at_a_stretch:
            count_outside_home_udf = F.udf(self.count_outside_home_at_a_stretch, T.FloatType())
        else:
            count_outside_home_udf = F.udf(self.count_outside_home, T.FloatType())

        # group by device_id and aggregate using the custom user defined aggregate function
        device_id_aggregates = self.sjr.groupby('device_id', self.aggr_admin + '_home').agg(
            count_outside_home_udf(
                F.collect_list('is_outside_home'),
                F.collect_list('date'),
                lit(self.end_at_home),
            ).alias(
                'days_outside_home'
            )
        )

        # find number of STMs and total population per admin4
        stms = device_id_aggregates.filter(
            (col('days_outside_home') >= self.stm_range[0]) & (col('days_outside_home') <= self.stm_range[1])).groupby(
            self.aggr_admin + '_home').count().withColumnRenamed('count', 'no_of_stms')
        #         total_samples = device_id_aggregates.groupby(
        #             self.aggr_admin + '_home'
        #         ).count().withColumnRenamed('count', 'total_samples')

        total_samples = device_id_aggregates.join(self.ids, on="device_id", how="inner").groupby(
            self.aggr_admin + '_home'
        ).count().withColumnRenamed('count', 'total_samples')

        # bring the mobility population and total population together
        admin_stats = total_samples.join(stms, self.aggr_admin + '_home')

        # save the mobility stats for the month in a CSV file
        admin_stats.coalesce(1).write.format(
            "com.databricks.spark.csv"
        ).mode('overwrite').option("header", "true").save(
            export_location
        )

    def preprocess(self, month):

        # convert integer value of month to string format padded by one zero if necessary
        self.month = str(month).zfill(2)

        start_date = "2020/{}/01".format(month)

        if not self.fixed_home_period:
            self.set_device_id_homes(((datetime.strptime(start_date, '%Y/%m/%d') - relativedelta.relativedelta(
                months=12)).strftime('%Y/%m/%d'), None), 12)

        start_date_with_padding = (
                datetime.strptime(start_date, "%Y/%m/%d") - relativedelta.relativedelta(days=self.left_padding_days)
        ).strftime("%Y/%m/%d")

        end_date_with_padding = (
                datetime.strptime(start_date, "%Y/%m/%d") + relativedelta.relativedelta(
            months=self.timeframe_months) + relativedelta.relativedelta(days=self.right_padding_days)
        ).strftime("%Y/%m/%d")

        # extract data of no_of_months number of months starting from start_month
        self.sjr = self.extract_data_by_ends(self.sjr_master, start_date_with_padding, end_date_with_padding)

        # convert UNIX timestamp to date format
        self.sjr = self.sjr.withColumn('date', from_unixtime('timestamp').cast(T.DateType()))

        self.sjr = self.date_device_mode(self.sjr)

        self.sjr = self.sjr.join(self.device_id_homes, on=['device_id'], how='inner')

        # quality control filter
        self.sjr = self.quality_control_filter(self.sjr, 3)

        self.ids = self.extract_data(self.sjr, start_date, 1, by='date').select('device_id').distinct()

    def export_for_a_month(self, month, export_location):
        """
        Parameters:
          month: integer value of the month (example: 1, 2, ..., 12)
        """

        # preprocess the data to extract data of our time interval and apply quality control filter
        self.preprocess(month)
        self._export(export_location)
