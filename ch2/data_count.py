import json
from collections import defaultdict, Counter
from pandas import DataFrame, Series
import pandas as pd
import numpy as np


def read_file():
    path = "resource\usagov_bitly_data2012-03-16-1331923249.txt"
    record = [json.loads(line) for line in open(path)]
    return record


class PurePyDataCount:

    def get_field_from_file(self, field):
        file = read_file()
        field_list = [dic[field] for dic in file if field in dic]
        return field_list

    def get_count(self, sequence):
        count = defaultdict(int)
        for x in sequence:
            count[x] += 1
        return count

    def get_ranked_dict(self, field, num):
        counts = Counter(self.get_field_from_file(field))
        return counts.most_common(num)


class PandasDataCount:

    def data_counts_by_field(self, field):
        frame = DataFrame(read_file())
        return frame[field].value_counts()

    def normalize_data_field(self, field):
        frame = DataFrame(read_file())
        normalized_data = frame[field].fillna('Missing')
        normalized_data[normalized_data == ''] = 'unknown'
        return normalized_data.value_counts()

    def agent_analysis(self):
        frame = DataFrame(read_file())
        # get all system value from 'a'
        result = Series([x.split()[0] for x in frame.a.dropna()])
        cframe = frame[frame.a.notnull()]
        operating_sys = np.where(cframe['a'].str.contains('Windows'), 'windows', 'not windows')
        by_tz_os = cframe.groupby(['tz', operating_sys])
        agg_counts = by_tz_os.size().unstack().fillna(0)
        indexer = agg_counts.sum(1).argsort()
        count_subset = agg_counts.take(indexer)[-10:]
        normed_subset = count_subset.div(count_subset.sum(1), axis=0)
        return normed_subset


if __name__ == '__main__':
    d = PurePyDataCount()
    panda = PandasDataCount()
    cnt = d.get_count(d.get_field_from_file('tz'))
    # print d.get_ranked_dict('tz', 10)
    # panda.agent_analysis().plot(kind='barh', rot=0)
# ipython notebook --pylab=inline
