# Turkish-Financial-Sentiment-Scraper
A Python tool for Turkish Financial Sentiment Analysis. Scrapes news headlines and calculates their sentiment and potential bias using a custom lexicon.

# 🇹🇷 Turkish-Financial-Sentiment-Scraper

[![ Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/)

[![ Library](https://img.shields.io/badge/Dependencies-Requests%2C%20BS4%2C%20Pandas-green)](https://pypi.org/)

[![ License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

## ✨ About the Project

**Turkish-Financial-Sentiment-Scraper** is an end-to-end system that collects Turkish financial news headlines and analyzes their market sentiment (Positive/Negative/Neutral) and speculative bias level (High Bias/Low Bias).

This project was developed to quickly understand the overall tone of news flow before making financial decisions.

## 🛠️ Basic Features and Technologies Used

| Category | Features | Technologies Used |

| :--- | :--- | :--- |

| **Scraping** | It dynamically pulls the financial news headlines of Dunya Newspaper (dunya.com). | `Requests`, `BeautifulSoup` |

| **Emotion Analysis (NLP)** | **Dictionary Based Scoring:** Uses a special dictionary consisting of predefined positive and negative financial words. | Special `FINANSAL_SOZLUK`, `re` (Regex) |

| **Bias Determination** | Determines the level of bias of the news by counting the existence of speculative words such as "expectation", "claim", "prediction". | Special `ONYARGI_WORDS` |

| **Data Presentation** | Presents the analysis results in a regular `Pandas DataFrame` structure with a title, normalized emotion score, bias score and ultimate labels. | `Pandas` |

## ⚙️ Installation and Operation

### Prerequisites

* Python 3.x

### 1. Clone the Warehouse

```bash

Git clone [https://github.com/](https://github.com/)[YOUR USERNAME]/Turkish-Financial-Sentiment-Scraper.git

Cd Turkish-Financial-Sentiment-Scraper
