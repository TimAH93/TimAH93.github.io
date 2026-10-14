# Should Eniac Enter Brazil via Magist?

**English** · [Deutsch](README.de.md)

**Recommendation: Enter Brazil, but not through Magist.** Magist delivers fast and reliably only in a few south-eastern states, and its tech business is small and low-priced compared with Eniac's premium Apple accessories.

**Type:** Group project (team of three), Data Analytics & AI training at WBS
**Status:** Completed

## Question

Eniac, a European online retailer of Apple-compatible tech, considered a partnership with Magist, a Brazilian marketplace, to enter the Brazilian market. Two concerns had to be checked before signing:

1. **Delivery:** Does Magist deliver fast enough for a premium brand?
2. **Fit:** Is Magist a good partner for high-end tech products?

## Data

- **Magist database (MySQL):** course-provided database based on the public [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) ([CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)). About 99,000 orders, September 2016 to October 2018. The data is not included in this repository.
- **Market research:** public sources on Brazilian e-commerce from 2017 to 2019 (listed below).

## Approach

1. Broke the main question down into a question tree with five areas: product range, sellers, delivery, customer satisfaction and market. Each sub-question had an owner, a status and a short answer.
2. Agreed on shared assumptions: six tech categories, revenue = item price without freight and cancelled orders.
3. Answered the data questions with SQL in MySQL Workbench and visualised the results in Tableau.
4. Added market research to put the data into context.
5. Combined everything into a short decision presentation.

## Findings

**Delivery (team result):** Only three states (São Paulo, Paraná, Minas Gerais) deliver on average in under 12 days with more than 94 % on time. For high-priced tech orders, only two cities met all criteria for speed, punctuality and reviews.

**Product fit (team result):** Tech makes up only about 12 % of Magist's revenue, and average tech prices are far below Eniac's price level.

**Tech categories in the catalogue (my analysis):** 3,387 of 32,951 products (10.3 %) fall into six tech categories. The categories alone do not show whether products are high-end or Apple-compatible, so the fit could not be proven from the data.

| Category | Products |
|---|---|
| computers_accessories | 1,639 |
| telephony | 1,134 |
| electronics | 517 |
| audio | 58 |
| computers | 30 |
| tablets_printing_image | 9 |

Query: [`sql/01_tech_categories.sql`](sql/01_tech_categories.sql)

**Market context (my research):**

- **Growth:** Brazilian e-commerce grew by about 12 % in 2018, while the overall economy grew by about 1 %.
- **Apple as a luxury good:** the iPhone XS launched at 7,300 BRL in Brazil, the highest price among 40 countries compared. Research on income inequality and status seeking (Walasek & Brown, 2015) helps explain why demand exists anyway: in very unequal societies, status goods matter more.
- **Fragile logistics:** an 11-day truck drivers' strike in May 2018 cost Brazilian e-commerce about 407 million BRL, and complaints about late postal deliveries rose every year from 2016 to 2018.
- **Competition:** B2W led the market, Mercado Livre was growing fast and shortened its median delivery time in Brazil by two days in 2018, and Amazon started selling electronics in Brazil in 2017.

## Recommendation

Brazil is an attractive, growing market, but Magist is not the right partner for Eniac. A larger marketplace with stronger logistics, such as Mercado Livre, fits a premium brand better.

## Tools

- SQL (MySQL Workbench)
- Tableau
- Google Docs and Slides for team coordination and the presentation

## My Role

- Structured the analysis as a question tree and kept track of open questions
- Identified the tech categories with SQL (catalogue analysis)
- Did the market research on growth, competitors, Apple prices and logistics
- Opened and closed the presentation, and presented the market context and the recommendation

Team: Julia, Matías and Tim

## Sources (market research)

- Ebit, Webshoppers 38 (via PagBrasil), Sep. 2018
- Tribuna PR, e-commerce revenue 2018, Feb. 2019
- Gazeta do Povo, Mercado Livre vs. B2W, Jul. 2017
- Tecnoblog, Amazon starts selling electronics in Brazil, Oct. 2017
- Olhar Digital, iPhone prices in Brazil, Oct. 2018, and Deutsche Bank Research country comparison, Jul. 2019
- Walasek, L. & Brown, G. D. A. (2015). Income Inequality and Status Seeking. *Psychological Science*
- Diário do Comércio, e-commerce losses during the truck strike, Jun. 2018
- Olhar Digital, complaints about Correios delays, Feb. 2019
- MercadoLibre, Q4 2018 earnings call

---

## Reflection

### Key Learnings

- **A question tree keeps a team focused.** Splitting one business question into numbered sub-questions with owners made it clear who works on what and which answers were still missing.
- **Data needs context.** The numbers showed that Magist sells few expensive tech products. The market research explained why: in Brazil, premium Apple products are luxury goods with a small target group.
- **My psychology background helps.** Research on status seeking gave a plausible explanation for Apple demand in Brazil, and it made the story easier to follow for a non-technical audience.
- **A recommendation needs a clear answer.** A decision-maker wants yes, no, or yes under conditions, supported by two or three strong points, not every query result.

### Challenges

- **Consistent definitions across the team.** Each of us wrote our own queries. Small differences, such as which categories count as tech, or a typo in a category name, can change results without anyone noticing. Writing down shared assumptions at the start helped; next time I would also share one common base query.
- **Currency.** Magist prices are in Brazilian real, Eniac's in euro. Comparing them correctly requires converting every value consistently and labelling the currency on each chart.
- **Converging on one recommendation.** Along the way we had three candidate recommendations: a regional rollout, a limited test, and an alternative partner. Agreeing on one message for the final presentation took explicit discussion.

### Open Question

Whether late deliveries actually lead to worse reviews and fewer repeat customers was left open in this project. I follow it up in my own project [Delivery & Loyalty](../delivery-loyalty/README.md).
