import lightgbm as lgb
import numpy

def handler(event, context=None):
    dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
    X = dataset[:, 0:8]
    Y = dataset[:, 8]

    model = event.get("model")
    bst = lgb.Booster(model_file=model)
    Ypred = bst.predict(X)
    
    return numpy.mean((Ypred>0.5)==(Y==1))

if __name__ == "__main__":
    event = {
        "model": "model.txt"
    }
    print(handler(event))