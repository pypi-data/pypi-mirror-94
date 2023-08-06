cdef class UniversalDependencyTreeBankFeatures:

    def __init__(self, features: str):
        cdef list _list
        cdef str feature, featureName, featureValue
        self.featureList = {}
        if features != "_":
            _list = features.split("\\|")
            for feature in _list:
                if "=" in feature:
                    featureName = feature[0: feature.index("=") - 1].strip()
                    featureValue = feature[feature.index("=") + 1:].strip()
                    self.featureList[featureName] = featureValue
                else:
                    print("Feature does not contain = ->" + features)

    cpdef str getFeatureValue(self, str feature):
        return self.featureList[feature]

    def __str__(self) -> str:
        cdef str result, feature
        if len(self.featureList) == 0:
            return "_"
        result = ""
        for feature in self.featureList:
            if result == "":
                result = feature + "=" + self.getFeatureValue(feature)
            else:
                result += "|" + feature + "=" + self.getFeatureValue(feature)
        return result
