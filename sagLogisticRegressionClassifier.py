from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from abstractClassifier import AbstractClassifier, tag_to_num, OTHER_TAG


class SagLogisticRegressionClassifier(AbstractClassifier):
    def get_name(self) -> str:
        return 'SagLogisticRegressionClassifier'

    def __init__(self, dataset: (list[dict], list[int])):
        groups, tags = dataset

        groups_info = [AbstractClassifier.get_useful_info(g) for g in groups]

        cv = CountVectorizer(analyzer='char', ngram_range=(3, 3), min_df=0.1, max_df=0.9)
        groups_info = cv.fit_transform(groups_info)

        clf = LogisticRegression(max_iter=290, solver='sag', random_state=25)
        clf.fit(groups_info, tags)

        self.__clf = clf
        self.__cv = cv

    def predict(self, group_info: dict) -> int:
        group_info = AbstractClassifier.get_useful_info(group_info)
        if len(group_info) < 150:
            return tag_to_num(OTHER_TAG)
        group_info = self.__cv.transform([group_info])
        pr = self.__clf.predict(group_info)
        return int(pr[0])