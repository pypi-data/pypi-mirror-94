from bias_detector.BiasMetric import BiasMetric
from bias_detector.EmailFullNameExtractor import EmailFullNameExtractor
from bias_detector.BiasReport import BiasReport
from bias_detector.FirstNameModel import FirstNameModel
from bias_detector.FirstNameZipcodeModel import FirstNameZipcodeModel
from bias_detector.FullNameModel import FullNameModel
from bias_detector.FullNameZipcodeModel import FullNameZipcodeModel
from bias_detector.bias_metrics.BiasMetricImpl import BiasMetricImpl
from bias_detector.bias_metrics.BiasMetricInput import BiasMetricInput
from bias_detector.bias_metrics.FprDiff import FprDiff
from bias_detector.bias_metrics.PositivePredProbDiff import PositivePredProbDiff
from bias_detector.bias_metrics.TprDiff import TprDiff
from bias_detector.common import *
import surgeo



class BiasDetector:

    def __init__(self, country: str = None):
        """
        :param country: must be US, other countries are not supported
        """
        if country is None or country.upper() != 'US':
            raise ValueError('Country must be US, other countries are not supported')
        self.email_full_name_extractor = EmailFullNameExtractor()
        self.first_name_model = FirstNameModel()
        self.last_name_model = surgeo.SurnameModel()
        self.zip_code_model = surgeo.GeocodeModel()
        self.full_name_model = FullNameModel()
        self.first_name_zip_code_model = FirstNameZipcodeModel()
        self.last_name_zip_code_model = surgeo.SurgeoModel()
        self.full_name_zip_code_model = FullNameZipcodeModel()

    def get_full_name(self, emails: Sequence[str]) -> pd.DataFrame:
        """
        get_full_name - extracts full name from emails
        :param emails: users emails
        :return: pandas DataFrame with first_name and last_name columns
        """
        emails = emails.str.lower()
        return emails.apply(lambda email: self.email_full_name_extractor.get_email_full_name(email).to_series())

    def get_bias_metrics_impl(self, bias_metric: BiasMetric) -> BiasMetricImpl:
        if bias_metric == BiasMetric.statistical_parity:
            return PositivePredProbDiff()
        if bias_metric == BiasMetric.equal_opportunity:
            return TprDiff()
        elif bias_metric == BiasMetric.predictive_equality:
            return FprDiff()

    def get_bias_report(self, first_names: Sequence[str] = None, last_names: Sequence[str] = None,
                        zip_codes: Sequence[str] = None, emails: Sequence[str] = None, y_true: Sequence[float] = None,
                        y_pred: Sequence[float] = None, detect_gender_bias: bool = True,
                        detect_race_bias: dict = True, **kwargs: dict) -> BiasReport:
        """
        :param first_names: users first names (optional - if last_names/zip_codes is provided)
        :param last_names: users last names (optional - if first_names/zip_codes is provided)
        :param zip_codes: users zip codes (optional - if first_names/last_names is provided)
        :param emails: users emails (optional - if first_names/last_names is not provided)
        :param y_true: true labels - 0/1 (optional - only some BiasMetric requires it)
        :param y_pred: predicted labels - 0/1
        :param detect_gender_bias: detect gender bias (optional - default True)
        :param detect_race_bias: detect race bias (optional - default True)
        :param kwargs: additional params
        :return: BiasReport
        """
        if not detect_gender_bias and not detect_race_bias:
            raise ValueError('Both detect_gender_bias and detect_race_bias are False')
        y_scores = kwargs.get('y_scores', None)
        input_p_groups = kwargs.get('p_groups', None)
        privileged_race = kwargs.get('privileged_race', None)
        if privileged_race is not None:
            privileged_race = privileged_race.lower()
        if input_p_groups is not None:
            if type(input_p_groups) != pd.DataFrame:
                raise ValueError('''p_groups must be a pd.DataFrame''')
            if detect_gender_bias and not {'male', 'female'}.issubset(set(input_p_groups.columns)):
                raise ValueError('''detect_gender_bias=True, p_groups columns must contain: ['male', 'female']''')
            if detect_race_bias and not set(races).issubset(set(input_p_groups.columns)):
                raise ValueError('''detect_race_bias=True, p_groups columns must contain: ['white', 'black', 'api', 'hispanic', 'native']''')
            input_p_groups = input_p_groups.reset_index(drop=True)
        else:
            input_p_groups = None
        classification_threshold = kwargs.get('classification_threshold', 0.5)
        emails = self.to_series(emails, 'email', str)
        y_true = self.to_series(y_true, 'y_true', float)
        y_pred = self.to_series(y_pred, 'y_pred', float)
        y_scores = self.to_series(y_scores, 'y_scores', float)
        if y_pred is None and y_scores is None:
            raise ValueError('y_pred/y_scores were not provided')
        if len(set(np.unique(y_pred)) - {0, 1}) > 0:
            raise ValueError('only binary classification is supported, y_pred should contain only 0/1')
        if y_pred is None and y_scores is not None:
            y_pred = [y_score >= classification_threshold for y_score in y_scores]
        if not self.is_same_length([first_names, last_names, zip_codes, emails, y_true, y_pred, y_scores, input_p_groups]):
            raise ValueError('Input data has different lengths')
        if y_true is None:
            bias_metrics = [BiasMetric.statistical_parity]
        else:
            bias_metrics = [BiasMetric.statistical_parity, BiasMetric.equal_opportunity, BiasMetric.predictive_equality]
        full_name = None
        if (emails is not None and len(emails) > 0) \
            and (first_names is None or len(first_names) == 0) \
            and (last_names is None or len(last_names) == 0):
            full_name = self.get_full_name(emails)
            first_names = full_name['first_name']
            last_names = full_name['last_name']
        p_groups = input_p_groups if input_p_groups is not None else self.get_p_groups(first_names, last_names, zip_codes, detect_gender_bias, detect_race_bias)
        groups_names = p_groups.columns
        bias_metrics_results = pd.DataFrame(index=[bias_metric.name for bias_metric in bias_metrics], columns=groups_names)
        for bias_metric in bias_metrics:
            bias_metrics_impl = self.get_bias_metrics_impl(bias_metric)
            metric_input = BiasMetricInput(p_groups, y_true, y_pred, y_scores, privileged_race)
            bias_metric_output = bias_metrics_impl.execute(metric_input)
            results = bias_metric_output.results
            bias_metrics_results.loc[bias_metric.name] = results
        estimated_groups_sizes = pd.Series(index=groups_names)
        for group_name in p_groups.columns:
            estimated_groups_sizes[group_name] = p_groups[group_name].sum()
        if detect_gender_bias:
            estimated_groups_sizes['gender_unknown'] = (p_groups[['male', 'female']].sum(axis=1) == 0).sum()
        if detect_race_bias:
            estimated_groups_sizes['race_unknown'] = (p_groups[races].sum(axis=1) == 0).sum()
        estimated_groups_sizes = estimated_groups_sizes.astype(int)
        return BiasReport(bias_metrics_results=bias_metrics_results,
                          estimated_groups_sizes=estimated_groups_sizes,
                          full_name=full_name,
                          y_true=y_true,
                          y_pred=y_pred,
                          y_scores=y_scores,
                          privileged_race=privileged_race,
                          p_groups=p_groups,
                          detect_gender_bias=detect_gender_bias,
                          detect_race_bias=detect_race_bias)

    def get_features_groups_correlation(self, first_names: Sequence[str] = None, last_names: Sequence[str] = None,
                                 zip_codes: Sequence[str] = None, features: pd.DataFrame = None) -> pd.DataFrame:
        """
        :param first_names: users first names (optional - if last_names/zip_codes is provided)
        :param last_names: users last names (optional - if first_names/zip_codes is provided)
        :param zip_codes: users zip codes (optional - if first_names/last_names is provided)
        :param features: features for correlation test
        :return: features-groups correlation DataFrame
        """
        if first_names is None and last_names is None and zip_codes is None:
            raise ValueError('first_names/last_names/zip_codes must be provided')
        if features is None or type(features) != pd.DataFrame:
            raise ValueError('features DataFrame must be provided')
        if not self.is_same_length([first_names, last_names, zip_codes, features]):
            raise ValueError('Input data has different lengths')
        p_groups = self.get_p_groups(first_names, last_names, zip_codes, detect_gender_bias=True, detect_race_bias=True)
        features = features.reset_index(drop=True)
        return pd.concat([features.corrwith(p_groups[col]).rename(col + '_correlation') for col in p_groups.columns], axis=1)

    def to_series(self, data: Sequence[object], name: str, dtype: object) -> pd.Series:
        return None if data is None else pd.Series(data).reset_index(drop=True).rename(name).astype(dtype)

    def get_p_groups(self,
                     first_names: pd.Series = None,
                     last_names: pd.Series = None,
                     zip_codes: pd.Series = None,
                     detect_gender_bias: bool = True,
                     detect_race_bias: bool = True) -> pd.DataFrame:
        if not self.is_same_length([first_names, last_names, zip_codes]):
            raise ValueError('Input data has different lengths')
        first_names = self.to_series(first_names, 'first_name', str)
        last_names = self.to_series(last_names, 'last_name', str)
        zip_codes = self.to_series(zip_codes, 'zip_code', str)
        user_data_count = self.get_user_data_count([first_names, last_names, zip_codes])
        p_groups = pd.DataFrame(index=list(range(user_data_count)))
        if first_names is not None:
            first_names = first_names.str.upper()
            first_names = first_names.str.replace(r'\s+', '')
        if last_names is not None:
            last_names = last_names.str.upper()
            last_names = last_names.str.replace(r'\s+', '')
        if zip_codes is not None:
            zip_codes = zip_codes.str.slice(0, 5)
            zip_codes = zip_codes.str.zfill(5)
            zip_codes.loc[~zip_codes.str.match(r'\d{5}')] = ''
        empty_series = pd.Series(np.empty(user_data_count, str))
        if first_names is None:
            first_names = empty_series.rename('first_name')
        if last_names is None:
            last_names = empty_series.rename('last_name')
        if zip_codes is None:
            zip_codes = empty_series.rename('zip_code')
        if detect_gender_bias:
            gender_probabilities = first_names.to_frame()\
                .join(p_gender_given_first_name_df, on='first_name')[p_gender_given_first_name_df.columns]
            p_groups = p_groups.join(gender_probabilities)
        if detect_race_bias:
            model_first_names = p_first_name_given_race_df.index
            model_last_names = self.last_name_model._PROB_RACE_GIVEN_SURNAME.index
            model_zip_codes = self.last_name_zip_code_model._PROB_ZCTA_GIVEN_RACE.index
            first_names_in_model = first_names.isin(model_first_names)
            last_names_in_model = last_names.isin(model_last_names)
            zip_codes_in_model = zip_codes.isin(model_zip_codes)
            first_names.loc[~first_names_in_model] = ''
            last_names.loc[~last_names_in_model] = ''
            zip_codes.loc[~zip_codes_in_model] = ''
            first_names_rows = first_names.str.len() > 0
            last_names_rows = last_names.str.len() > 0
            zip_codes_rows = zip_codes.str.len() > 0
            only_first_names_rows = first_names_rows & ~last_names_rows & ~zip_codes_rows
            only_last_names_rows = ~first_names_rows & last_names_rows & ~zip_codes_rows
            only_zip_codes_rows = ~first_names_rows & ~last_names_rows & zip_codes_rows
            full_name_rows = first_names_rows & last_names_rows & ~zip_codes_rows
            first_name_zip_code_rows = first_names_rows & ~last_names_rows & zip_codes_rows
            last_name_zip_code_rows = ~first_names_rows & last_names_rows & zip_codes_rows
            full_name_zip_code_rows = first_names_rows & last_names_rows & zip_codes_rows
            first_names_probabilities = self.first_name_model.get_probabilities(first_names.loc[only_first_names_rows].reset_index(drop=True)) \
                [races].set_index(only_first_names_rows[only_first_names_rows].index)
            last_names_probabilities = self.last_name_model.get_probabilities(last_names.loc[only_last_names_rows].reset_index(drop=True)) \
                [races].set_index(only_last_names_rows[only_last_names_rows].index)
            zip_codes_probabilities = self.zip_code_model.get_probabilities(zip_codes.loc[only_zip_codes_rows].reset_index(drop=True)) \
                [races].set_index(only_zip_codes_rows[only_zip_codes_rows].index)
            full_name_probabilities = self.full_name_model.get_probabilities(first_names.loc[full_name_rows].reset_index(drop=True), last_names.loc[full_name_rows].reset_index(drop=True)) \
                [races].set_index(full_name_rows[full_name_rows].index)
            first_name_zip_code_probabilities = self.first_name_zip_code_model.get_probabilities(first_names.loc[first_name_zip_code_rows].reset_index(drop=True), zip_codes.loc[first_name_zip_code_rows].reset_index(drop=True)) \
                [races].set_index(first_name_zip_code_rows[first_name_zip_code_rows].index)
            last_name_zip_code_probabilities = self.last_name_zip_code_model.get_probabilities(last_names.loc[last_name_zip_code_rows].reset_index(drop=True), zip_codes.loc[last_name_zip_code_rows].reset_index(drop=True)) \
                [races].set_index(last_name_zip_code_rows[last_name_zip_code_rows].index)
            full_name_zip_code_probabilities = self.full_name_zip_code_model.get_probabilities(first_names.loc[full_name_zip_code_rows].reset_index(drop=True), last_names.loc[full_name_zip_code_rows].reset_index(drop=True), zip_codes.loc[full_name_zip_code_rows].reset_index(drop=True)) \
                [races].set_index(full_name_zip_code_rows[full_name_zip_code_rows].index)
            p_groups.loc[only_first_names_rows, races] = first_names_probabilities
            p_groups.loc[only_last_names_rows, races] = last_names_probabilities
            p_groups.loc[only_zip_codes_rows, races] = zip_codes_probabilities
            p_groups.loc[full_name_rows, races] = full_name_probabilities
            p_groups.loc[first_name_zip_code_rows, races] = first_name_zip_code_probabilities
            p_groups.loc[last_name_zip_code_rows, races] = last_name_zip_code_probabilities
            p_groups.loc[full_name_zip_code_rows, races] = full_name_zip_code_probabilities
        p_groups.fillna(0.0, inplace=True)
        return p_groups

    def is_same_length(self, sequences: Sequence[Sequence]) -> bool:
        length = self.get_user_data_count(sequences)
        if length is not None:
            for sequence in sequences:
                if sequence is not None and len(sequence) != length:
                    return False
        return True

    def get_user_data_count(self, sequences):
        length = None
        for sequence in sequences:
            if sequence is not None:
                length = len(sequence)
                break
        return length
