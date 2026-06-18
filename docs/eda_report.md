# Bivariate Analysis Report: Customer Churn

**Objective:** This report provides an in-depth analysis of bivariate relationships between various customer attributes and the target variable, `Churn`. The findings aim to uncover the underlying drivers of customer attrition and provide actionable business recommendations to improve retention strategies.

---

## Figure 1: Contract vs Churn

**Observation**
Month-to-month contracts have a remarkably high churn rate (approximately ~~42%). In stark contrast, customers on Two-year contracts show an exceptionally low churn rate (~~2-3%).

**Statistical Interpretation**
There is a severe, statistically significant relationship between the length of the contract term and churn likelihood. Shorter commitment periods correlate strongly with higher attrition.

**Business Insight**
Customers who are not locked into long-term agreements have the flexibility to leave for competitors when faced with a minor inconvenience or a better promotional offer. Long-term contracts successfully create friction for churn and ensure customer stickiness.

**Churn Impact Assessment**


| Metric                   | Value  |
| ------------------------ | ------ |
| Strength of Relationship | Strong |
| Risk Level               | High   |


**Key Takeaway:** Month-to-month contracts are the most critical risk factor for churn; incentivizing longer commitments is essential for retention.

---

## Figure 2: Gender vs Churn

**Observation**
The churn rate is nearly identical when comparing Male and Female customers, hovering around 26-27% for both groups.

**Statistical Interpretation**
Gender is uniformly distributed across the churned and retained customer bases. It holds almost zero predictive power for determining whether a customer will leave.

**Business Insight**
Targeted retention campaigns or pricing strategies based on gender will likely be ineffective. Customer retention efforts should be gender-agnostic.

**Churn Impact Assessment**


| Metric                   | Value |
| ------------------------ | ----- |
| Strength of Relationship | Weak  |
| Risk Level               | Low   |


**Key Takeaway:** Gender is not a differentiating factor for predicting or managing customer churn.

---

## Figure 3: SeniorCitizen vs Churn

**Observation**
Senior citizens represent a smaller subset of the overall customer base but exhibit a significantly higher churn rate compared to non-senior citizens (roughly 41% vs. 23%).

**Statistical Interpretation**
Being a senior citizen is positively correlated with a higher probability of churning. While non-seniors make up the bulk of the data, the proportion of seniors churning is disproportionately large.

**Business Insight**
Seniors may be experiencing specific pain points, such as difficulty navigating technical support, confusion over complex billing structures, or fixed-income constraints that make them more sensitive to price hikes.

**Churn Impact Assessment**


| Metric                   | Value    |
| ------------------------ | -------- |
| Strength of Relationship | Moderate |
| Risk Level               | Medium   |


**Key Takeaway:** Senior citizens are at elevated risk; specialized, simplified support or tailored "senior-friendly" plans might help retain them.

---

## Figure 4: Partner vs Churn

**Observation**
Customers without a partner have a noticeably higher churn rate (~~33%) compared to customers with a partner (~~20%).

**Statistical Interpretation**
Having a partner indicates a more stable household situation, which negatively correlates with churn. Single customers are more mobile and prone to changing providers.

**Business Insight**
Households with partners may have more complex, deeply integrated telecom needs (e.g., shared data plans, multiple lines), making it harder to switch providers. Single users are more agile and price-sensitive.

**Churn Impact Assessment**


| Metric                   | Value    |
| ------------------------ | -------- |
| Strength of Relationship | Moderate |
| Risk Level               | Medium   |


**Key Takeaway:** Single users churn more frequently; promoting family or shared household plans could improve retention by increasing switching costs.

---

## Figure 5: Dependents vs Churn

**Observation**
Customers without dependents churn at a substantially higher rate (~~31%) than customers with dependents (~~15%).

**Statistical Interpretation**
Similar to the Partner feature, the presence of dependents acts as a stabilizing factor. Customers with dependents are half as likely to churn.

**Business Insight**
Families with children (dependents) likely prioritize stability and are less willing to deal with the disruption of changing service providers. They may also be on bundled family plans that are difficult to untangle.

**Churn Impact Assessment**


| Metric                   | Value    |
| ------------------------ | -------- |
| Strength of Relationship | Moderate |
| Risk Level               | Medium   |


**Key Takeaway:** Customers without dependents are highly flight-prone. Bundled family packages are highly effective at building loyalty.

---

## Figure 6: PhoneService vs Churn

**Observation**
Churn rates are largely similar whether a customer has Phone Service (~~27%) or not (~~25%).

**Statistical Interpretation**
The presence or absence of phone service alone does not significantly alter the probability of a customer churning.

**Business Insight**
Phone service is largely considered a basic utility and does not serve as a competitive differentiator that drives or prevents customer attrition on its own.

**Churn Impact Assessment**


| Metric                   | Value |
| ------------------------ | ----- |
| Strength of Relationship | Weak  |
| Risk Level               | Low   |


**Key Takeaway:** Having a phone service is a neutral factor in determining churn risk.

---

## Figure 7: MultipleLines vs Churn

**Observation**
There is only a marginal difference in churn between customers with multiple lines (~~28%) and those with a single line (~~25%).

**Statistical Interpretation**
While adding multiple lines slightly increases the churn rate, the difference is not substantial enough to be a primary predictive driver.

**Business Insight**
Customers with multiple lines might have higher overall bills, which could cause slight price sensitivity, but it is not a major area of concern on its own.

**Churn Impact Assessment**


| Metric                   | Value |
| ------------------------ | ----- |
| Strength of Relationship | Weak  |
| Risk Level               | Low   |


**Key Takeaway:** Multiple lines have a negligible impact on a customer's decision to leave.

---

## Figure 8: InternetService vs Churn

**Observation**
Customers utilizing "Fiber optic" internet have a dramatically high churn rate (~~42%), whereas "DSL" users churn much less (~~19%). Customers with "No internet service" have the lowest churn rate of all (~7%).

**Statistical Interpretation**
Internet Service Type is a massive differentiator for churn. Fiber optic service is highly correlated with a customer leaving, which is an anomaly given that fiber is supposed to be a premium, high-speed product.

**Business Insight**
The high churn among Fiber Optic customers points to a serious product or service issue. It could be due to fierce competition offering better fiber pricing, poor network reliability (outages), or unmet expectations regarding speed versus cost.

**Churn Impact Assessment**


| Metric                   | Value  |
| ------------------------ | ------ |
| Strength of Relationship | Strong |
| Risk Level               | High   |


**Key Takeaway:** Fiber Optic customers are highly dissatisfied and churning rapidly; immediate investigation into fiber service quality and competitor pricing is required.

---

## Figure 9: OnlineSecurity vs Churn

**Observation**
Customers who do not have Online Security churn at a massive rate (~~42%), compared to those who do have it (~~15%).

**Statistical Interpretation**
Lack of Online Security is a strong predictor of churn. Subscribing to this add-on heavily depresses the churn rate.

**Business Insight**
Online Security acts as a "sticky" feature. Customers who invest in security feel more protected and integrated into the ecosystem, making them less likely to leave. Conversely, those without it may be on bare-bones plans and highly price-sensitive.

**Churn Impact Assessment**


| Metric                   | Value  |
| ------------------------ | ------ |
| Strength of Relationship | Strong |
| Risk Level               | High   |


**Key Takeaway:** Customers without online security are highly vulnerable to churn. Bundling security features for free or at a discount could drastically improve retention.

---

## Figure 10: OnlineBackup vs Churn

**Observation**
Similar to Online Security, customers lacking Online Backup show much higher churn rates (~~40%) than those who subscribe to it (~~21%).

**Statistical Interpretation**
The absence of value-added technical services correlates strongly with customer attrition.

**Business Insight**
When customers store their data with the telecom provider's backup service, the "switching cost" (the effort required to move to a new provider) increases significantly.

**Churn Impact Assessment**


| Metric                   | Value              |
| ------------------------ | ------------------ |
| Strength of Relationship | Moderate to Strong |
| Risk Level               | High               |


**Key Takeaway:** Online backup creates a lock-in effect; customers without it can easily walk away.

---

## Figure 11: DeviceProtection vs Churn

**Observation**
Customers without Device Protection churn more (~~39%) than those with the protection plan (~~22%).

**Statistical Interpretation**
There is a clear negative correlation between having device protection and churning.

**Business Insight**
Customers paying for device protection likely own expensive, premium devices (e.g., flagship smartphones) and value peace of mind. These customers are more invested in the telecom provider's ecosystem.

**Churn Impact Assessment**


| Metric                   | Value    |
| ------------------------ | -------- |
| Strength of Relationship | Moderate |
| Risk Level               | Medium   |


**Key Takeaway:** Selling device insurance improves customer stickiness.

---

## Figure 12: TechSupport vs Churn

**Observation**
Customers who do not use or subscribe to Tech Support have a severe churn rate (~~41%), while those with Tech Support rarely churn (~~15%).

**Statistical Interpretation**
Tech support is a major defining feature dividing churners from non-churners.

**Business Insight**
Customers without tech support may get easily frustrated when they face technical difficulties and simply cancel their service. Those with tech support get their issues resolved quickly, leading to higher satisfaction and retention.

**Churn Impact Assessment**


| Metric                   | Value  |
| ------------------------ | ------ |
| Strength of Relationship | Strong |
| Risk Level               | High   |


**Key Takeaway:** Accessible tech support is crucial for retention; lack of it is a major driver of customer loss.

---

## Figure 13 & 14: StreamingTV & StreamingMovies vs Churn

**Observation**
Whether a customer streams TV or Movies has a relatively minimal impact on churn. Both "Yes" and "No" categories for these features show moderate churn rates (in the low-to-mid 30% range for internet users).

**Statistical Interpretation**
Entertainment add-ons like Streaming TV and Movies are not strong discriminators for churn compared to utility/security add-ons.

**Business Insight**
While streaming services are nice-to-have revenue generators, they do not create the same structural "lock-in" effect as tech support or security.

**Churn Impact Assessment**


| Metric                   | Value |
| ------------------------ | ----- |
| Strength of Relationship | Weak  |
| Risk Level               | Low   |


**Key Takeaway:** Streaming features generate revenue but do not significantly protect against churn.

---

## Figure 15: PaperlessBilling vs Churn

**Observation**
Customers who opt for Paperless Billing have a notably higher churn rate (~~33%) compared to those receiving traditional paper bills (~~16%).

**Statistical Interpretation**
There is a surprising positive correlation between modern, paperless billing and customer churn.

**Business Insight**
Customers using paperless billing are likely more tech-savvy, digitally engaged, and aware of their monthly expenses through emails or apps. This makes them more agile and capable of easily finding and switching to a competitor's digital platform. Paper bill recipients might be older or prefer the status quo.

**Churn Impact Assessment**


| Metric                   | Value    |
| ------------------------ | -------- |
| Strength of Relationship | Moderate |
| Risk Level               | Medium   |


**Key Takeaway:** Digitally engaged (paperless) customers are more likely to comparison shop and switch providers.

---

## Figure 16: PaymentMethod vs Churn

**Observation**
"Electronic check" stands out drastically with an exceptionally high churn rate (~~45%). All other payment methods (Mailed check, Bank transfer, Credit card) have low and similar churn rates (~~15-19%).

**Statistical Interpretation**
The use of Electronic checks is a massive statistical anomaly and a primary indicator of churn risk.

**Business Insight**
Electronic checks often require manual initiation each month, forcing the customer to confront their bill actively. This regular, manual payment process acts as a recurring reminder of the cost, increasing price sensitivity. Automatic payments (credit cards/bank transfers) are "out of sight, out of mind," leading to better retention.

**Churn Impact Assessment**


| Metric                   | Value  |
| ------------------------ | ------ |
| Strength of Relationship | Strong |
| Risk Level               | High   |


**Key Takeaway:** Electronic check users are extremely high-risk. Pushing customers toward automated credit card or bank transfer billing is imperative.

---

## Figure 17: Tenure vs Churn (Numerical)

**Observation**
The boxplot/KDE for tenure shows that churning customers have a significantly lower median tenure (usually around 10 months) compared to retained customers (who skew heavily towards 35-40+ months).

**Statistical Interpretation**
Tenure is inversely proportional to churn. The risk of churn is exponentially higher in the first 12 months of the customer lifecycle.

**Business Insight**
If a customer survives their first year, their likelihood of leaving drops drastically. The onboarding period and the end of the initial 1-year promotional contract are critical danger zones.

**Churn Impact Assessment**


| Metric                   | Value                                 |
| ------------------------ | ------------------------------------- |
| Strength of Relationship | Strong                                |
| Risk Level               | High (Specifically for New Customers) |


**Key Takeaway:** Customer loyalty is built in the first year. First-year retention programs are critical.

---

## Figure 18: MonthlyCharges vs Churn (Numerical)

**Observation**
Churning customers tend to have higher overall Monthly Charges (skewing towards $70-$100) compared to retained customers, who have a wider spread including many low-cost plans.

**Statistical Interpretation**
Higher monthly costs correlate with higher churn probability, confirming high price sensitivity among the customer base.

**Business Insight**
As the bill increases—likely due to upselling premium features like Fiber Optic internet—customers become highly sensitive to value. If the premium price isn't matched by premium quality, they leave.

**Churn Impact Assessment**


| Metric                   | Value              |
| ------------------------ | ------------------ |
| Strength of Relationship | Moderate to Strong |
| Risk Level               | Medium to High     |


**Key Takeaway:** High-value (high MRR) customers are actually at higher risk of leaving due to cost sensitivity and high expectations.

---

## Overall Bivariate Analysis Summary

### Top Features Associated with Churn

Based on the visual evidence, the most influential features dictating churn are:

1. **Contract Term** — Month-to-month contracts
2. **Internet Service Type** — Fiber Optic internet service
3. **Payment Method** — Electronic Checks
4. **Tenure** — Early lifecycle (0-12 months)
5. **Technical Services** — Lack of Online Security and Tech Support

### Major Churn Drivers

The factors that appear to contribute most to customer churn revolve around lack of commitment, poor premium service alignment, and manual billing awareness. Customers who are not locked into contracts, who actively have to pay their bills via electronic check every month, and who do not feel "anchored" by security or tech support features are extremely likely to walk away. Furthermore, the massive churn in Fiber Optic users suggests a fundamental product-market fit or quality issue.

### Customer Segments at Risk


| Segment                      | Profile                                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------- |
| The "Agile" Switcher         | Month-to-month contract + Electronic Check payer + Paperless Billing                              |
| The Unsatisfied Premium User | Fiber Optic user paying high monthly charges but lacking tech support or security add-ons         |
| The Unanchored Single        | Customers without a partner or dependents who have lower switching costs                          |
| The Vulnerable Senior        | Senior citizens who may require specialized customer service to navigate technical/billing issues |
| New Arrivals                 | Customers in their first 1-12 months of service                                                   |


### Business Recommendations

1. **Incentivize Long-Term Contracts** — Offer aggressive discounts, free upgrades, or bundled services for customers willing to switch from Month-to-month to 1-year or 2-year contracts.
2. **Investigate Fiber Optic Quality** — Conduct an immediate deep-dive into the Fiber Optic service. Determine if the high churn is due to competitive pricing, poor speeds, or frequent outages.
3. **Mandate or Heavily Promote Auto-Pay** — Move customers away from Electronic Checks by offering a $5-$10 monthly discount for setting up automatic credit card or bank transfer payments.
4. **Bundle "Sticky" Tech Services** — Provide basic OnlineSecurity or TechSupport for free or at a heavy discount in the first year. Customers who use these services are proven to be much more loyal.
5. **First-Year Nurture Campaigns** — Implement a robust 12-month onboarding program with proactive check-ins, specifically targeting single users and senior citizens to ensure they are getting the most value out of their plans.

