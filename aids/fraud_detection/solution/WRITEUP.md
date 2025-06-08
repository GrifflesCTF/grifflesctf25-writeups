# Solution

* To start solving this challenge, make use of the fact that we are using a K-Nearest Neighbours (KNN) model to perform classification. Typically, for a KNN model to be effective, the data points, when plotted on some high-dimensional space, needs to form "clusters".
* In other words, you need to find a range of values for `PurchaseAmount`, `NumItems`, `ShippingDistance`, `PaymentMethod`, and `TransactionHour` such that it belongs to the "non-fraudulent" data cluster.
* After some trial and error using the code provided in the notebook, hopefully, you observe that for a purchase to be classified as "non-fraudulent":
  * `PurchaseAmount` needs to be low (from around 1-50)
  * `NumItems` needs to be low, but is not as significant a factor
  * `ShippingDistance` needs to be low (from around 1-100)
  * `PaymentMethod` should be either credit card (0), or debit card (1),
  * `TransactionHour` should be from the morning to the evening (8 to around 20)
* Additionally, your modified data should have enough variance to get past the verification system. This means you cannot just overwrite all rows in `fraud.csv` with the same row of data that you found was flagged as "non-fraudulent".
* Make use of the probability density functions that `numpy` provides to generate varied data.
* If needed, you can see `solutions.ipynb` for sample code that generates non-fraudulent data.