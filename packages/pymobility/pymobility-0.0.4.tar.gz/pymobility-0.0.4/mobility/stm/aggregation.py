import os
import pandas as pd


class CustomAggregation:

    def __init__(self, aggr_admin, misc_files_dir, province_column, adjustment=False):
        self.admin_stats = {}
        self.admin_classification = {}
        self.admin_province_mapping = {}
        self.admin_to_hr = {}

        self.adj_dict = {}
        self.hr_average = {}
        self.month_average = {}
        self.rural_urban_average = {}
        self.hr_month_average = {}
        self.hr_rural_urban_average = {}
        self.rural_urban_month_average = {}

        self.aggr_admin = aggr_admin
        self.misc_files_dir = misc_files_dir
        self.province_column = province_column
        self.create_admin_mappings()
        self.adjustment = adjustment

        self.create_admin_mappings()
        self.set_adjustment_numbers()

    def create_admin_mappings(self):

        self.admin_classification[self.aggr_admin] = pd.read_csv(
            '{}/admin4_classification.csv'.format(self.misc_files_dir))
        self.admin_classification[self.aggr_admin] = self.admin_classification[self.aggr_admin][
            ~self.admin_classification[self.aggr_admin]['classification'].isnull()]
        self.admin_classification[self.aggr_admin][self.aggr_admin] = self.admin_classification[self.aggr_admin][
            self.aggr_admin].astype(str).str.zfill(6)

        self.admin_province_mapping[self.aggr_admin] = pd.read_csv(
            '{}/admin4_province_mapping.csv'.format(self.misc_files_dir))
        self.admin_province_mapping[self.aggr_admin]['adm4_code'] = self.admin_province_mapping[self.aggr_admin][
            self.aggr_admin].astype(str).str.zfill(6)

        telangana_admin4s = pd.read_csv('{}/telangana_admin4s.csv'.format(self.misc_files_dir), header=None)
        telangana_admin4s[0] = telangana_admin4s[0].astype(str).str.zfill(6)

        self.admin_province_mapping[self.aggr_admin].loc[
            self.admin_province_mapping[self.aggr_admin]['adm4_code'].isin(telangana_admin4s[0]), 'adm1_code'] = None
        self.admin_province_mapping[self.aggr_admin].loc[
            self.admin_province_mapping[self.aggr_admin]['adm4_code'].isin(
                telangana_admin4s[0]), 'adm1_name'] = 'Telangana'

        # cellphone adjustment
        self.admin_to_hr[self.aggr_admin] = pd.read_csv('{}/admin4_to_hr.csv'.format(self.misc_files_dir))
        self.admin_to_hr[self.aggr_admin][self.aggr_admin.lower()] = self.admin_to_hr[self.aggr_admin][
            self.aggr_admin.lower()
        ].astype(str).str.zfill(6)

    def set_adjustment_numbers(self):
        hr_cellphone_coverage = pd.read_excel('{}/Results.xlsx'.format(self.misc_files_dir),
                                              sheet_name='% people with mobiles')

        # extract 2020 cellphone adjustment numbers and prepare the dictionary
        hrcc_2020 = hr_cellphone_coverage[hr_cellphone_coverage['month'].str.contains('2020')]
        hrcc_2020['month'] = hrcc_2020['month'].str[-1]

        self.adj_dict = dict(
            (x, dict((x_t, dict(zip(y_t['month'].str[-1], y_t['% people with mobiles']))) for (x_t, y_t) in
                     y.groupby('Unnamed: 3'))) for x, y in hrcc_2020.groupby('hr2'))

        # each feature average
        self.rural_urban_average = dict(hrcc_2020.groupby('Unnamed: 3')['% people with mobiles'].mean())
        self.month_average = dict(hrcc_2020.groupby('month')['% people with mobiles'].mean())
        self.hr_average = dict(hrcc_2020.groupby('hr2')['% people with mobiles'].mean())

        # two features combined average
        self.rural_urban_month_average = dict(
            hrcc_2020.groupby(['Unnamed: 3', 'month'])['% people with mobiles'].mean())
        self.hr_month_average = dict(hrcc_2020.groupby(['hr2', 'month'])['% people with mobiles'].mean())
        self.hr_rural_urban_average = dict(hrcc_2020.groupby(['hr2', 'Unnamed: 3'])['% people with mobiles'].mean())

    def read_admin_stats(self, spark_export_location):

        # read the CSV file saved
        admin_stats_csv_file = [i for i in os.listdir(spark_export_location) if
                                i.startswith('part') and i.endswith('.csv')][0]

        self.admin_stats[self.aggr_admin] = pd.read_csv(spark_export_location + admin_stats_csv_file)
        self.admin_stats[self.aggr_admin]['adm4_code_home'] = self.admin_stats[self.aggr_admin][
            'adm4_code_home'].astype(str).str.zfill(6)

    def classify(self):
        # add rural/urban information for admin4s
        self.admin_stats[self.aggr_admin][self.aggr_admin + '_home'] = self.admin_stats[self.aggr_admin][
            self.aggr_admin + '_home'].astype(str).str.zfill(6)
        self.admin_stats[self.aggr_admin]['classification'] = self.admin_stats[self.aggr_admin][
            self.aggr_admin + '_home'].map(
            dict(zip(self.admin_classification[self.aggr_admin][self.aggr_admin],
                     self.admin_classification[self.aggr_admin]['classification']))
        )

    def _adjust(self, row, month):
        """
        `adjust` function to adjust the counts as per mobile coverage percentage.
        """
        if str(row['hr']) == 'nan':
            adjustment_factor = self.rural_urban_month_average[(row['classification'].lower(), str(int(month)))]
        elif row['classification'].lower() not in self.adj_dict[row['hr']]:
            if (int(row['hr']), row['classification'].lower()) not in self.hr_rural_urban_average:
                adjustment_factor = self.hr_month_average[(int(row['hr']), str(int(month)))]
            else:
                adjustment_factor = self.hr_rural_urban_average[(int(row['hr']), row['classification'].lower())]
        elif str(int(month)) not in self.adj_dict[row['hr']][row['classification'].lower()]:
            near_month = str(
                min(map(int, self.adj_dict[row['hr']][row['classification'].lower()]),
                    key=lambda x: abs(x - int(month))))
            adjustment_factor = self.adj_dict[row['hr']][row['classification'].lower()][near_month]
        elif self.adj_dict[row['hr']][row['classification'].lower()][str(int(month))] == 0:
            adjustment_factor = 0.1
        else:
            adjustment_factor = self.adj_dict[row['hr']][row['classification'].lower()][str(int(month))]

        return row['total_samples'] / adjustment_factor, row['no_of_stms'] / adjustment_factor

    def adjust(self):
        # adjustment code
        self.admin_stats[self.aggr_admin]['hr'] = self.admin_stats[self.aggr_admin][self.aggr_admin + '_home'].map(
            dict(zip(self.admin_to_hr[self.aggr_admin][self.aggr_admin.lower()],
                     self.admin_to_hr[self.aggr_admin]['hr'])))
        self.admin_stats[self.aggr_admin]['adjusted_stats'] = self.admin_stats[self.aggr_admin].apply(
            self._adjust, axis=1, args=(self.month,)
        )
        self.admin_stats[self.aggr_admin]['adjusted_total_samples'] = \
            self.admin_stats[self.aggr_admin]['adjusted_stats'].str[0]
        self.admin_stats[self.aggr_admin]['adjusted_no_of_stms'] = \
            self.admin_stats[self.aggr_admin]['adjusted_stats'].str[1]

    def export_province_wise_stm(self):

        self.admin_stats['province'] = self.admin_stats[self.aggr_admin][self.aggr_admin + '_home'].map(
            dict(zip(self.admin_province_mapping[self.aggr_admin][self.aggr_admin],
                     self.admin_province_mapping[self.aggr_admin][self.province_column])))
        self.admin_stats[self.aggr_admin]['province'] = self.admin_stats[self.aggr_admin][
            self.aggr_admin + '_home'].map(
            dict(zip(self.admin_province_mapping[self.aggr_admin][self.aggr_admin],
                     self.admin_province_mapping[self.aggr_admin][self.province_column])))

        province_rural_urban_stm = self.admin_stats[self.aggr_admin].groupby(
            ['classification', 'province']).sum().reset_index()

        province_rural_urban_stm['percentage'] = province_rural_urban_stm['no_of_stms'] / province_rural_urban_stm[
            'total_samples']

        if self.adjustment:
            province_rural_urban_stm['adjusted_percentage'] = province_rural_urban_stm['adjusted_no_of_stms'] / \
                                                              province_rural_urban_stm['adjusted_total_samples']

        return province_rural_urban_stm.sort_values(by=['percentage'], ascending=False)

    def aggregate(self, spark_export_location):
        self.read_admin_stats(spark_export_location)

        self.classify()

        if self.adjustment:
            self.adjust()

        return self.export_province_wise_stm()
