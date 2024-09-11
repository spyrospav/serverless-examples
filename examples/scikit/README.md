The original model wants sklearn 0.20.2. That is too low for Python 3.12. I used sklearn 1.5.2 and find a new model randomly https://github.com/eightBEC/fastapi-ml-skeleton/blob/main/sample_model/lin_reg_california_housing_model.joblib

`from sklearn.externals import joblib` is deprecated and changed to `import joblib` don't know if it's gonna affect DD