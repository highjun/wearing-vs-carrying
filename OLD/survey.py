from util import *

# ver1 = pd.read_csv("ver1.csv", encoding = "utf-8", header = 0, index_col = False)
# ver1['ver'] = [1] * ver1.shape[0]


# ver2 = pd.read_csv("ver2.csv", encoding = "utf-8",header = 0, index_col = False)

# ver2['ver'] = [2] * ver2.shape[0]

# survey = pd.concat([ver1,ver2],  ignore_index= True)
# survey  =survey.sort_values(by = 'ID')
# survey.to_csv("survey.csv", index= False, encoding = 'euc-kr')

survey = pd.read_csv("survey.csv", index_col = False, header = 0, encoding = 'euc-kr')
survey['Gender'] = ['M' if val[0]== '남' else ('W' if val[0]== '여' else '') for val in survey['Gender'].to_numpy()]
survey.to_csv("survey.csv", index= False, encoding = 'euc-kr')
