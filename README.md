# Video Game Ratings EDA and Modeling
## Dataset and Information
The original dataset used for this EDA was founded on [Kaggle](https://www.kaggle.com/datasets/imohtn/video-games-rating-by-esrb/data)

After working through the dataset, I created a script to scrape [esrb.org](https://www.esrb.org/) to increase the size of the data from 1900 rows to 12k rows. 
## Descriptive Analysis
### What are the ratings represented in this dataset?
### How many violent games are present in this dataset?
### How many games contain cartoon violance?
### How many games contain fantasy violence?
### How is violence represented throughout entire dataset?
### Do E-rated games contain any sort of violence?
### Do E-rated games contain any drug or alcohol references?
### How often do two different content descriptors co-occur?
## Inferential Analysis
### Do games that feature animated blood have a higher probability of receiving an "M" (Mature) rating than games that do not?
### Is there a significant difference in the mean number of content descriptors across different ESRB ratings?
### Let's just check to see if there is a significant difference between ET and T
## Modeling
The goal is to predict if a game has a certain rating. We focused on Random Tree Classifier. After some hyper parameter tuning and getting a decent accuracy of around 85% we continued to dive deeper with a Dense Neural Network. We were unable to dramatically improve on the base model. 