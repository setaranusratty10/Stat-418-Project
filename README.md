# Goodreads Book Recommendation Engine
### Final Project - UCLA Stats 418: Tools in Data Science (Spring 2025)
### Link to Shiny App - [Goodreads KNN Recommender](https://shiny-app-594837701038.us-west1.run.app/)

## Background
This app is a book recommendation engine built for readers looking to discover new books based on their preferences. Unlike traditional recommendation systems that rely on user ratings or collaborative filtering, this app uses a content-based filtering approach to suggest books with similar genres, authors, and quantitative traits.

The current version is trained on data scraped from the Goodreads ["Best Books Ever" List](https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1) and uses a K-Nearest Neighbors (KNN) algorithm with cosine similarity to identify the most similar titles to a user-selected book. By converting text fields like genre and author into TF-IDF vectors, and applying log transformations to skewed numerical fields such as rating count, page count, and publication age, the model produces recommendations that are both relevant and personalized.

This app demonstrates how a simple machine learning pipeline—paired with real-world data—can power a practical tool for readers. The final product is deployed as an interactive web app using R Shiny, containerized with Docker, and hosted on Google Cloud Run for public access. Additionally, the model is built using a Flask-API and deployed on Google Cloud Run
## Exploratory Data Analysis
Our data comes from the Goodreads ["Best Books Ever" List](https://www.goodreads.com/list/show/1.Best_Books_Ever?page=1) which contains 73,677 books. Selenium was utilizied to scrape the data and ended up scraping the top 2,000 books in the list with key features: Title, Author, Genres, Average Rating, Rating Count, Number of Pages, Year, and URL.
However, looking at the numerical features, many were skewed which required log transformations as shown here:

![image](https://github.com/user-attachments/assets/dca4409f-2593-49b7-a5ba-3d8557fbcfe7)

Cleaning the data involved dropping duplicate and missing values, as well as applying log transformations to Rating Count, Number of Pages, and the transformation of Publication Year into Age. Once the dataset was cleaned, the final working dataset had 1,898 usable entries and 11 features. 
### 📚 Sample of Dataset Used

| Title                               | Author            | Avg Rating | Rating Count | Num Pages | Genres                             | Pub Year | [Goodreads URL](#) | log_rating_count | log_num_pages | log_pub_age | genres_txt                        |
|-------------------------------------|-------------------|------------|--------------|------------|-------------------------------------|-----------|--------------------|------------------|----------------|-------------|------------------------------------|
| Harry Potter and the Sorcerer's Stone | J.K. Rowling      | 4.47       | 10913786     | 333.0      | Fantasy, Fiction, Young Adult      | 1997      | [Link](https://www.goodreads.com/book/show/42844155-harry-potter-and-the-sorcerer-s-stone) | 16.205537         | 5.811141       | 3.367296    | Fantasy Fiction Young Adult        |
| The Hunger Games                    | Suzanne Collins    | 4.34       | 9426102      | 374.0      | Young Adult, Dystopia, Fiction     | 2008      | [Link](https://www.goodreads.com/book/show/2767052-the-hunger-games) | 16.058993         | 5.926926       | 2.890372    | Young Adult Dystopia Fiction       |
| Twilight                            | Stephenie Meyer    | 3.67       | 7045296      | 498.0      | Fantasy, Young Adult, Romance      | 2005      | [Link](https://www.goodreads.com/book/show/41865.Twilight) | 15.767871         | 6.212606       | 3.044522    | Fantasy Young Adult Romance        |
| To Kill a Mockingbird              | Harper Lee         | 4.26       | 6598464      | 323.0      | Historical Fiction, School, Literature | 1960   | [Link](https://www.goodreads.com/book/show/2657.To_Kill_a_Mockingbird) | 15.795234         | 5.780744       | 4.189655    | Historical Fiction School Literature |
| The Great Gatsby                    | F. Scott Fitzgerald| 3.93       | 5645767      | 180.0      | Classics, Fiction, School          | 1925      | [Link](https://www.goodreads.com/book/show/4671.The_Great_Gatsby) | 15.543617         | 5.198497       | 4.615121    | Classics Fiction School            |

To get a sense of genre diversity, a bar chart was generated, highlighting common genres like fantasy, romance, and historical fiction.

![Top 15 Genres](https://github.com/user-attachments/assets/7854f615-fe77-4956-9a41-3a2a26d92058)

Additionally, The average rating across the dataset ranged from 3.07 to 4.81, with a mean of 4.09 and a standard deviation of 0.23. The distribution was tightly clustered around the 4.0–4.3 range, indicating that most books were generally well-reviewed.

## Methodology
The core of the recommendation system relies on a K-Nearest Neighbors (KNN) model that uses cosine similarity to assess closeness between books. The input features for the model were a combination of vectorized text and scaled numeric variables. Specifically, the genres and author fields were vectorized using TF-IDF, enabling the model to account for textual similarity. Meanwhile, features like the log of rating count, log of page count, log of publication age, and average rating were scaled using a RobustScaler to reduce the influence of outliers. These components were combined in a scikit-learn ColumnTransformer, then fed into a unified pipeline with the KNN estimator. Given a selected book, the model returns its k most similar neighbors, as long as their cosine similarity score is 0.80 or higher.

| Feature           | Type      | Transformation       |
|------------------|-----------|----------------------|
| Genres           | Categorical (Text) | TF-IDF Vectorization |
| Author           | Categorical (Text) | TF-IDF Vectorization |
| Rating Count     | Numeric   | Log Transformation    |
| Number of Pages  | Numeric   | Log Transformation    |
| Publication Age  | Numeric   | Log Transformation    |
| Average Rating   | Numeric   | Used As-Is            |

When inputting a book in the model in this case we can use the book "The Hunger Games", we see the output of the KNN model. 

### 📖 Sample Recommendation Output

| Rank | Title                                 | Author           | Avg Rating | URL |
|------|----------------------------------------|------------------|------------|------------------|
| 1    | Mockingjay                             | Suzanne Collins | 4.11        | https://www.goodreads.com/book/show/7260188mockingjay         |
| 2    | Catching Fire                          | Suzanne Collins | 4.34        | https://www.goodreads.com/book/show/6148028-catching-fire         |
| 3    | Harry Potter and the Sorcerer’s Stone  | J.K. Rowling     | 4.47       | https://www.goodreads.com/book/show/42844155-harry-potter-and-the-sorcerer-s-stone         |
| 4    | Divergent     | Veronica Roth     | 4.14       | https://www.goodreads.com/book/show/13335037-divergent         |
| 5    | Harry Potter and the Chamber of Secrets    | J.K. Rowling  | 4.43       | https://www.goodreads.com/book/show/15881.Harry_Potter_and_the_Chamber_of_Secrets        |

## Results & App Features
When a user selects a book title, the app returns a ranked list of recommended books based on content similarity. For instance, choosing "The Hunger Games" as the input yields top matches such as "Mockingjay" and "Catching Fire", both by the same author and with similarly high average ratings. These results are calculated using cosine similarity on a combination of text-based and numeric features, with a similarity threshold ensuring only closely related books are returned. The example below shows similarity scores exceeding 0.8, indicating strong alignment in genre, style, and metadata.

This functionality is delivered through an interactive web app built using R Shiny and deployed via Docker on Google Cloud Run. The user interface includes an auto-complete search bar for book titles and dynamically updates recommended results. Each recommendation card links directly to the Goodreads page for further exploration. Users can also apply filters to limit recommendations based on minimum average rating or maximum page count. A genre distribution bar chart provides a visual breakdown of the genres represented in the recommendation list, enhancing user understanding and engagement with the model output.

### Sample Input in Shiny App
<img width="759" alt="image" src="https://github.com/user-attachments/assets/fa5b42e2-0c23-4469-bb0b-5ad0392fa953" />

### Sample Output in Shiny App
<img width="684" alt="image" src="https://github.com/user-attachments/assets/d26960cc-8945-4cdd-a1ee-354986477796" />

## Book Recommendation System

This repository contains:

- `/docker_files/`: A Shiny app frontend that allows users to input a book title and get similar book recommendations.
- `/docker_model_api/`: A Flask API that serves book recommendations based on a trained k-NN model.

## Deployment Instructions

- See `README.md` in each folder for details on how to build, run, and deploy.

---

**Copyright**: Setara Nusratty, UCLA MASDS 2024  
**Last Updated**: 06/03/2025








