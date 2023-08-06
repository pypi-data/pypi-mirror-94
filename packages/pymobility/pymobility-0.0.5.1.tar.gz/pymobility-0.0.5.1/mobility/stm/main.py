import pandas as pd

from pyspark.sql import SparkSession

from .stm import GenericShortTermMigration
from aggregation import CustomAggregation


def main(start_month, end_month, **kwargs):

    master_df = None

    spark = SparkSession.builder.master("local").appName("mobility").getOrCreate()

    stm = GenericShortTermMigration(
        spark_session=spark,
        raw_file_location='/mnt/CUBEIQ/esapv/India/delta_unacast_v4',
        raw_file_format='delta',
        aggr_admin='adm4_code',
        home_admin='adm4_code',
        stm_range=[15, float('inf')],
        left_padding_days=7,
        right_padding_days=7,
        fixed_home_period=False
    )

    aggregation = CustomAggregation(
        aggr_admin='adm4_code',
        misc_files_dir='/dbfs/FileStore/tables/',
        province_column='adm1_name',
    )

    for month in range(start_month, end_month + 1):

        spark_export_location = \
            '/mnt/CUBEIQ/esapv/India/Unacast/Short Term Migration/One Month Definition/Test/2020_{}_7P/'.format(
            str(month).zfill(2))

        stm.export_for_a_month(month, export_location=spark_export_location)

        df = aggregation.aggregate('/dbfs/' + spark_export_location)

        df['Month'] = '2020/' + str(month).zfill(2)

        if master_df is None:
            master_df = df
        else:
            master_df = pd.concat([master_df, df], ignore_index=True)
        print(master_df.shape)

    master_df.to_csv(
        '/dbfs/mnt/CUBEIQ/esapv/India/Unacast/Short Term Migration/One Month Definition/Test/province_wise_stm_7_days_padding_variable.csv')


if __name__ == "__main__":
    main(1, 2)

