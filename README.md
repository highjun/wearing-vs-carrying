### Carrying VS Wearing Data Analysis

#### 해볼 것
- [ ]: Activity Definition
- [ ]: 핸드폰 기종과 워치 기종에 따른 차이가 많이 나는지?
- [ ]: 각 Daily Step을 집단으로 분류할 수 있는지?
- [ ]: 분류된 Daily Step을 기준으로 각 User가 얼마나 Consistent한 Behavior를 보여주는가?
- [ ]: User를 집단으로 분류할 수 있는지?
- [ ]: Watch 미착용 구간 구별 가능?
- [ ]: 별 의미없는 Error나 실제로 움직이지 않았음에도 측정된 구간 존재?

#### Experiments
1. Activity Duration distribution per User/Device
2. Correlation between sum of duration/ sum of step for each activity
3. Interactive Bar Plot of steps along with timestamp
4. Grouping the hourly interval thorugh single device activity
5. Daily Step Difference between phone and watch per User
6. Daily Step Difference between phone and watch per User after removing single device activity
7. Activity Step Difference for both activity
8. Weekly Pattern of difference per User
    - It is difficult to find distinct features. 
9.  Daily Pattern of difference per User
    - However, user does not show consistent behavior for all days
10. number of single activity per houlr interval plot
11. Check Interarrival time of activity to think of exponential distribution(or poisson)