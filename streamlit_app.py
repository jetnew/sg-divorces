import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')
import pandas as pd
from io import BytesIO

data = pd.read_csv("M810641.csv", skiprows=10, skipfooter=9, thousands=',').T
df = data.iloc[1:]
# for i, v in enumerate(data.iloc[0]):
#     print(i, v)

df.index = pd.to_datetime(df.index).year


st.title("Why are so many of our parents divorced?")
st.markdown("My parents are divorced. As I grew up, I was surprised by how many of my friends' parents are divorced too. This observation motivated me to investigate the [data](https://www.singstat.gov.sg/find-data/search-by-theme/population/marital-status-marriages-and-divorces/latest-data) to find out whether there is something wrong with our parents' generation in terms of the divorce rate.")


st.subheader("About the data")
st.markdown("The data is \"Singapore Residents Aged 20 Years & Over by Sex, Age Group and Marital Status, Annual\" from the Department of Statistics Singapore, obtained from [singstat.gov.sg](https://www.singstat.gov.sg/find-data/search-by-theme/population/marital-status-marriages-and-divorces/latest-data). It contains yearly data from 1980 to 2020, and is grouped by age groups from 20-29 to 70 years and over. In each age group, the numbers are grouped between males and females, and then further grouped into single, married, widowed and divorce/separated.")


st.subheader("What is the rate of divorce over time?")
st.markdown("The general trend is not great, as we observe an linear rise in divorce rates from 1980 to 2020. However, the absolute percentage stands at 4.5%, which is not too bad.")
cols_total = list(range(0, 90, 15))
cols_divorced = list(range(4, 90, 15))
df_divorce_rate = df[cols_divorced].sum(axis=1) / df[cols_total].sum(axis=1) * 100
fig, ax = plt.subplots()
plt.title("Divorce rate (%) of population aged 20 and above")
plt.plot(df_divorce_rate)
st.pyplot(fig)
st.info("Divorce rates are calculated by the sum of divorces over the total population.")


st.subheader("What about by age group?")
st.markdown("We can observe that the age group with the highest rate of divorce is **between 40 and 69**. The rates approach 6-7%, which is slightly concerning. It is also not optimistic that this age group has the highest increase in divorce rates over the years.")
fig, ax = plt.subplots()
plt.title("Divorce rate (%) of subpopulation over time")
for i in range(0, 90, 15):
    plt.plot(df[i+4] / df[i] * 100, label=f'Age {i//15*10+20}-{i//15*10+29}')
plt.legend(loc='best')
st.pyplot(fig)
st.error("Especially worrying is that if we assume a linear trend and extrapolate with 1% every 5 years, we can expect divorce rates in this age group to increase to **9% by 2030**.")


st.subheader("At what age group are we most at risk of divorce then?")
st.markdown("We notice that the highest divorce rate occurs **between age 50 and 59**. Nonetheless, it seems that as we age beyond 60, our rate of divorce falls.")
df2 = pd.DataFrame()
for i in range(0, 90, 15):
    df2[i//15] = df[i+4] / df[i] * 100
means = np.array([df2[i].mean() for i in range(6)])
std = np.array([df2[i].std() for i in range(6)])
fig, ax = plt.subplots()
plt.title("Divorce rate (%) of subpopulation by age")
xs = [f'{i//15*10+20}-{i//15*10+29}' for i in range(0,90,15)]
plt.plot(means)
plt.fill_between(xs, means+std, means-std, alpha=0.2)
st.pyplot(fig)
st.info("The blue area is 1 standard deviation from the mean when divorce rates are aggregated across the years.")


st.subheader("So, does our parents' generation have a problem?")
st.markdown("Thankfully, it appears not! At least, not in particular, considering that the steepness of increase seems similar across the generations.")
df3 = pd.DataFrame()
for i in range(0, 90, 15):
    df3[i//15] = df[i+4].groupby(df.index // 10).mean() / df[i].groupby(df.index // 10).mean() * 100
divorce_rate_gen = [df3.values.diagonal(i) for i in range(-4, 1)]
fig, ax = plt.subplots()
plt.title("Divorce rate (%) of subpopulation by generation")
xs = []
for i in range(4, -1, -1):
    xs.append([i for i in range(1980 + i*10, 2030, 10)])
labels = [f'Born {i}-{i+9}' for i in range(2000, 1959, -10)]
for i, gen in enumerate(divorce_rate_gen):
    plt.plot(xs[i], gen, 'o-', label=labels[i])
plt.legend(loc='best')
st.pyplot(fig)
st.info("Each generation's divorce rate is aggregated across 10 years, which means the divorce rate for '1980' refers to the average of divorce rates for that generation from 1980 to 1989.")


st.subheader("What does this say about divorces in general?")
st.markdown("As mentioned, growing up, I was *surprised* by how many of my friends' parents were divorced. Let me attempt to explain this surprise. At a younger age, divorce was relatively rare, as we see that the divorce rate is around 1-2% for those aged 20-39. As we grow older, and as our parents reach between age 40 to 59, rate of divorce rises, and is as high as up to 7% in 2020. This explains our \"surprise\" growing up about how divorces seems more common than previously thought, since the rate of divorce is always lower when we're younger and higher as we grow up.")
st.markdown("As we saw previously, we can expect divorce rates in the age group of 40-69 to increase up to 9% by 2030, which roughly translates to **1 in 10 people**. This is an especially worrying trend. It suggests the need to establish strong support systems for children as parents at that age divorce. To these children, know that you are not alone, and seek help if you need.")


st.subheader("Question to ponder: Why are more males married yet more females are divorced?")
st.markdown("Why does the married rate difference across genders differ for divorce rates?")
cols_total = list(range(0, 90, 15))
cols_married = list(range(2, 90, 15))
cols_divorced = list(range(4, 90, 15))
cols_total_male = list(range(5, 90, 15))
cols_married_male = list(range(7, 90, 15))
cols_divorced_male = list(range(9, 90, 15))
cols_total_female = list(range(10, 90, 15))
cols_married_female = list(range(12, 90, 15))
cols_divorced_female = list(range(14, 90, 15))
df_married_rate = df[cols_married].sum(axis=1) / df[cols_total].sum(axis=1) * 100
df_married_rate_male = df[cols_married_male].sum(axis=1) / df[cols_total_male].sum(axis=1) * 100
df_married_rate_female = df[cols_married_female].sum(axis=1) / df[cols_total_female].sum(axis=1) * 100
df_divorce_rate = df[cols_divorced].sum(axis=1) / df[cols_total].sum(axis=1) * 100
df_divorce_rate_male = df[cols_divorced_male].sum(axis=1) / df[cols_total_male].sum(axis=1) * 100
df_divorce_rate_female = df[cols_divorced_female].sum(axis=1) / df[cols_total_female].sum(axis=1) * 100
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.set_title("Married rate (%) by gender")
ax1.plot(df_married_rate, label='All')
ax1.plot(df_married_rate_male, label='Male')
ax1.plot(df_married_rate_female, label='Female')
ax1.legend(loc='best')
ax2.set_title("Divorce rate (%) by gender")
ax2.plot(df_divorce_rate, label='All')
ax2.plot(df_divorce_rate_male, label='Male')
ax2.plot(df_divorce_rate_female, label='Female')
ax2.legend(loc='best')
st.pyplot(fig)
st.markdown("A good friend (thanks Shiying! :)) raised the possibility that men could be more likely to re-marry. What do you think?")
st.markdown("View the code: [GitHub](https://github.com/jetnew/sg-divorces)")