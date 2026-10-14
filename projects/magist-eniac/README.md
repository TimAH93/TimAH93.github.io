# Should Eniac Enter Brazil via Magist?

**English** · [Deutsch](README.de.md)

**Type:** Group project (team of three), Data Analytics & AI training at WBS · **Duration:** 2 weeks · **Status:** Completed

## Summary

In this project, our team took the role of analysts for Eniac, a European online retailer of Apple-compatible tech. Eniac was considering a partnership with Magist, a Brazilian marketplace, to enter the Brazilian market. Our task was to find out with data whether Magist is a good partner, and to present a clear recommendation to Eniac's management.

We broke the business question down into smaller questions, answered them with SQL, visualised the results in Tableau, added market research, and presented our recommendation in a short management presentation: Brazil is an attractive market, but Magist is not the right partner for a premium brand.

## How We Solved It

1. **Understanding the business problem.** Eniac had two concerns: Does Magist deliver fast enough for premium customers? And does Magist fit high-end tech products?
2. **Question tree.** We split these concerns into five areas (product range, sellers, delivery, customer satisfaction, market) with numbered sub-questions. Each question had an owner, a status and a short answer, so we always knew what was still open.
3. **Shared assumptions.** Before querying, we agreed on which product categories count as tech and how to define revenue, so that our results would be comparable.
4. **Data analysis with SQL.** We explored the Magist database in MySQL Workbench: product categories, prices, sellers, delivery times, punctuality and reviews.
5. **Visualisation in Tableau.** We turned the key results into charts that a non-technical audience can read at a glance.
6. **Market research.** Because the data alone could not answer every question, we added public research on Brazilian e-commerce, competitors, Apple prices and logistics.
7. **Presentation.** We reduced everything to two questions, two clear answers and one recommendation, and presented it to the "management" in a role play.

## My Role

- Structured the analysis as a question tree and kept track of open questions
- Analysed which product categories are relevant for Eniac (SQL)
- Did the market research on growth, competitors, Apple prices and logistics, with sources
- Opened and closed the presentation, and presented the market context and the recommendation

Team: Julia, Matías and Tim

## Languages, Libraries and Tools

- **SQL** (MySQL Workbench): joins, aggregations, CASE WHEN, window functions
- **Tableau**: bar charts, calculated fields, colour coding for thresholds
- **Google Docs and Slides**: question tree, shared notes, presentation
- **Market research** in Portuguese-language sources

## Key Learnings

- **A question tree keeps a team focused.** Splitting one business question into numbered sub-questions with owners made it clear who works on what and which answers were still missing.
- **Data needs context.** The numbers showed that Magist sells few expensive tech products. The market research explained why: in Brazil, premium Apple products are luxury goods with a small target group.
- **My psychology background helps.** Research on status seeking (Walasek & Brown, 2015) gave a plausible explanation for Apple demand in Brazil, and it made the story easier to follow for a non-technical audience.
- **A recommendation needs a clear answer.** A decision-maker wants yes, no, or yes under conditions, supported by two or three strong points, not every query result.
- **Different working styles can complement each other.** We approached tasks quite differently, but everyone could bring in their strengths, and together we built a presentation none of us would have made alone.

## Challenges

- **Working in a team.** I had mostly worked on my own before. It was important to me to treat my teammates with respect and leave room for their contributions. A clear structure from the start helped me focus on my own tasks and trust the others with theirs.
- **Consistent definitions across the team.** Each of us wrote our own queries. Small differences, such as which categories count as tech, or a typo in a category name, can change results without anyone noticing. Writing down shared assumptions at the start helped; next time I would also share one common base query.
- **Currency.** Magist prices are in Brazilian real, Eniac's in euro. Comparing them correctly requires converting every value consistently and labelling the currency on each chart.
- **Converging on one recommendation.** Along the way we had three candidate recommendations: a regional rollout, a limited test, and an alternative partner. Agreeing on one message for the final presentation took explicit discussion.

## Next Steps

- Present more often, since explaining results clearly is a core skill for a data analyst.
- Get faster and more independent in Tableau.
- Write more targeted SQL queries.
- Follow up the question this project left open, whether late deliveries cost customer loyalty, in my own project [Delivery & Loyalty](../delivery-loyalty/README.md).

## Files

- [`presentation/Team_Jaguar_Magist.pdf`](presentation/Team_Jaguar_Magist.pdf): final presentation (German)
- [`sql/`](sql/): all SQL queries of the team, numbered by question; the author is named in each file (mine: [`01_tech_categories.sql`](sql/01_tech_categories.sql))

## Data and Sources

- **Magist database (MySQL):** course-provided database based on the public [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). About 99,000 orders, September 2016 to October 2018.
- **Market research:** Ebit Webshoppers 38 (2018); Tribuna PR (2019); Gazeta do Povo (2017); Tecnoblog (2017); Olhar Digital (2018, 2019) with Deutsche Bank Research (2019); Diário do Comércio (2018); MercadoLibre Q4 2018 earnings call; Walasek, L. & Brown, G. D. A. (2015). Income Inequality and Status Seeking. *Psychological Science*.
