# Keras Flower

A Simple Flower classification package using DenseNet201.

- Classes   : [104 classes of flowers](keras_flower_labels.txt)
- Training Data Set : [Petals to the Metal - Flower Classification on TPU](https://www.kaggle.com/c/tpu-getting-started)


#### Usage

- Use pip install to install this package

```
pip install keras_flower
```

- To get all prediction results

```
import keras_flower as kf
predictions = kf.predict_by_path("file/to/predict.png")
print(predictions)
```

Sample output:

```text
[1.4414026e-06 1.6031330e-06 1.6295390e-06 1.1156463e-06 2.7592062e-06
...
 1.1587109e-06 4.1556059e-06 1.0784672e-05 6.0254356e-06]
```


- To get top prediction result with [flower labels](https://github.com/Bhanuchander210/keras_flower/blob/master/keras_flower_labels.txt)

```
import keras_flower as kf
for predicted, score in kf.predict_name_by_path("/path/to/file.png"):
    print(predicted, score)
```

Sample output:


```text
sunflower 0.99960905
```

#### Validation

- Data set : [102 Category Flower Dataset](https://www.robots.ox.ac.uk/~vgg/data/flowers/102/index.html)
- No of images : **8189**
- Overall accuracy : **0.9715**
- confusion matrix : [102flowers_confusion_matrix.csv](https://github.com/Bhanuchander210/keras_flower/blob/master/102flowers_confusion_matrix.csv)
- classification report : [102flowers_classification_report.txt](https://github.com/Bhanuchander210/keras_flower/blob/master/102flowers_classification_report.txt)
- classification report summary:
```text
                           precision    recall  f1-score   support
                micro avg       0.97      0.97      0.97      8189
                macro avg       0.95      0.94      0.94      8189
             weighted avg       0.97      0.97      0.97      8189
```
#### Demo

![demo](https://raw.githubusercontent.com/Bhanuchander210/keras_flower/master/demo.gif)
