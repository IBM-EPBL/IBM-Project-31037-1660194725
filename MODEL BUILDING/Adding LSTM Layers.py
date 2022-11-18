{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "collapsed_sections": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "source": [
        "# **IMPORTING MODEL BUILDING LIBRARIES**"
      ],
      "metadata": {
        "id": "pPnT_XVXQ9kh"
      }
    },
    {
      "cell_type": "code",
      "execution_count": 23,
      "metadata": {
        "id": "w8rCsBrUKfPw"
      },
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "from keras.models import Sequential\n",
        "from keras.layers import LSTM\n",
        "from keras.layers import Dropout\n",
        "from keras.layers import Dense\n",
        "import pandas as pd\n",
        "from matplotlib import pyplot as plt\n",
        "from sklearn.preprocessing import StandardScaler\n",
        "from sklearn.metrics import mean_absolute_error as mae\n",
        "from sklearn.metrics import mean_squared_error as mse\n",
        "from sklearn.metrics import r2_score as r2s\n",
        "from google.colab import files\n",
        "from math import sqrt"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# **INITIALIZING THE MODEL**"
      ],
      "metadata": {
        "id": "uDXO5HsXfQlW"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "def plotCurve(x,y,xlable,ylabel,clabel):\n",
        "    fig, ax = plt.subplots(figsize=(5, 3))\n",
        "    fig.subplots_adjust(bottom=0.15, left=0.2)\n",
        "    ax.plot(x,y,label=clabel)\n",
        "    ax.set_xlabel(xlable)\n",
        "    ax.set_ylabel(ylabel)\n",
        "    plt.grid()\n",
        "    ax.legend()\n",
        "    plt.show()"
      ],
      "metadata": {
        "id": "GT0zND0ofPj2"
      },
      "execution_count": 24,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def plotTwoCurves(x1,x2,y1,y2,xlable,ylabel,clabel1,clabel2):\n",
        "    fig, ax = plt.subplots(figsize=(5, 3))\n",
        "    fig.subplots_adjust(bottom=0.15, left=0.2)\n",
        "    ax.plot(x1,y1,color='blue',label=clabel1)\n",
        "    ax.plot(x2,y2,color='red',label=clabel2)\n",
        "    ax.set_xlabel(xlable)\n",
        "    ax.set_ylabel(ylabel)\n",
        "    plt.legend()\n",
        "    plt.show()"
      ],
      "metadata": {
        "id": "IpSN0phkfa-I"
      },
      "execution_count": 25,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "ds=pd.read_csv('Crude_Oil_Prices.csv')\n",
        "ds=ds.set_index(ds['Date'])\n",
        "ds=ds.dropna()\n",
        "print(ds)\n",
        "ds['Date']=pd.to_datetime(ds['Date'])\n",
        "print(ds['Value'].head())\n",
        "index1=ds['Date']"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "BW_Bq1q-ffEo",
        "outputId": "68d1e609-6b3a-44c6-d469-3f75690f152f"
      },
      "execution_count": 26,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "                  Date  Value\n",
            "Date                         \n",
            "02-01-1986  02-01-1986  25.56\n",
            "03-01-1986  03-01-1986  26.00\n",
            "06-01-1986  06-01-1986  26.53\n",
            "07-01-1986  07-01-1986  25.85\n",
            "08-01-1986  08-01-1986  25.87\n",
            "...                ...    ...\n",
            "20-10-2022  20-10-2022  85.98\n",
            "21-10-2022  21-10-2022  85.05\n",
            "24-10-2022  24-10-2022  84.92\n",
            "25-10-2022  25-10-2022  84.79\n",
            "26-10-2022  26-10-2022  88.05\n",
            "\n",
            "[9294 rows x 2 columns]\n",
            "Date\n",
            "02-01-1986    25.56\n",
            "03-01-1986    26.00\n",
            "06-01-1986    26.53\n",
            "07-01-1986    25.85\n",
            "08-01-1986    25.87\n",
            "Name: Value, dtype: float64\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "plotCurve(index1,ds['Value'],'Time(Days)','Price','Price Series')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 221
        },
        "id": "YsyjMeKig2Ef",
        "outputId": "ff899b01-7e03-4cf2-8e83-cd2c30cb2423"
      },
      "execution_count": 27,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 360x216 with 1 Axes>"
            ],
            "image/png": "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\n"
          },
          "metadata": {
            "needs_background": "light"
          }
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "ds_price=ds['Value'].astype(float)\n",
        "scaler=StandardScaler()\n",
        "scaler=scaler.fit(ds_price.values.reshape(-1, 1))\n",
        "ds_price_scaled=scaler.transform(ds_price.values.reshape(-1, 1))\n",
        "ds_price_scaled"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "dM9vK9Maj30e",
        "outputId": "b7527401-6b94-4490-d7f5-6b7bca2c343f"
      },
      "execution_count": 28,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "array([[-0.68979433],\n",
              "       [-0.67488539],\n",
              "       [-0.65692689],\n",
              "       ...,\n",
              "       [ 1.32155776],\n",
              "       [ 1.31715284],\n",
              "       [ 1.42761456]])"
            ]
          },
          "metadata": {},
          "execution_count": 28
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "plotTwoCurves(index1,index1,ds['Value'],ds_price_scaled,'Time(Days)','Price','Price Series','Scaled Price')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 221
        },
        "id": "wa70lKYkj5cV",
        "outputId": "33d125c0-6d61-41da-8647-ab9f7dd4c3ce"
      },
      "execution_count": 29,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 360x216 with 1 Axes>"
            ],
            "image/png": "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\n"
          },
          "metadata": {
            "needs_background": "light"
          }
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# **CREATING TRAINING AND TESTING DATA**"
      ],
      "metadata": {
        "id": "3CcnGDF_kaeO"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "oilPX=[]\n",
        "oilPY=[]\n",
        "predicted_data=0\n",
        "actual_data=0\n",
        "next_period=1\n",
        "window_size=14"
      ],
      "metadata": {
        "id": "ZpgW7NovlVSw"
      },
      "execution_count": 30,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "for i in range(window_size, len(ds_price_scaled)-next_period+1):\n",
        "    oilPX.append(ds_price_scaled[i-window_size:i])\n",
        "    oilPY.append(ds_price_scaled[i+next_period-1:i+next_period,0])"
      ],
      "metadata": {
        "id": "rapCOjFnliwz"
      },
      "execution_count": 31,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "oilPX,oilPY=np.array(oilPX),np.array(oilPY)"
      ],
      "metadata": {
        "id": "Kt0jOUrhmGbA"
      },
      "execution_count": 32,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "print('shape= {}.'.format(ds.shape))\n",
        "print('Price Scaled shape= {}.'.format(ds_price_scaled.shape))\n",
        "print('oilPX shape== {}.'.format(oilPX.shape))\n",
        "print('oilPY shape== {}.'.format(oilPY.shape))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "kSaiiseXmIK1",
        "outputId": "a5e27d64-c9b5-46d9-fd94-e1fa119fcf34"
      },
      "execution_count": 33,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "shape= (9294, 2).\n",
            "Price Scaled shape= (9294, 1).\n",
            "oilPX shape== (9280, 14, 1).\n",
            "oilPY shape== (9280, 1).\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# **ADDING LSTM LAYERS**"
      ],
      "metadata": {
        "id": "XS7Coti0o87C"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "model=Sequential()\n",
        "model.add(LSTM(100, activation='relu', input_shape=(oilPX.shape[1], oilPX.shape[2]), return_sequences=True))\n",
        "model.add(LSTM(50, activation='relu', return_sequences=False))\n",
        "model.add(Dropout(0.2))\n",
        "model.add(Dense(oilPY.shape[1]))"
      ],
      "metadata": {
        "id": "PccYuRXZo7tV"
      },
      "execution_count": 34,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "model.compile(optimizer='adam',loss='mse')\n",
        "model.summary()"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "8HiLbeQKpVWV",
        "outputId": "b06d0c0b-5caa-4385-d2b7-ae51612992dd"
      },
      "execution_count": 35,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Model: \"sequential_1\"\n",
            "_________________________________________________________________\n",
            " Layer (type)                Output Shape              Param #   \n",
            "=================================================================\n",
            " lstm_2 (LSTM)               (None, 14, 100)           40800     \n",
            "                                                                 \n",
            " lstm_3 (LSTM)               (None, 50)                30200     \n",
            "                                                                 \n",
            " dropout_1 (Dropout)         (None, 50)                0         \n",
            "                                                                 \n",
            " dense_1 (Dense)             (None, 1)                 51        \n",
            "                                                                 \n",
            "=================================================================\n",
            "Total params: 71,051\n",
            "Trainable params: 71,051\n",
            "Non-trainable params: 0\n",
            "_________________________________________________________________\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "history=model.fit(oilPX,oilPY,epochs=30,batch_size=16, validation_split=0.1,verbose=1)\n",
        "index2=range(0,len(history.history['loss']))"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "P3WZ-NQDp2MC",
        "outputId": "adb90d39-1051-499c-f508-6c205987ff9b"
      },
      "execution_count": 36,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Epoch 1/30\n",
            "522/522 [==============================] - 11s 16ms/step - loss: 0.0487 - val_loss: 0.0150\n",
            "Epoch 2/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0236 - val_loss: 0.0154\n",
            "Epoch 3/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0230 - val_loss: 0.0121\n",
            "Epoch 4/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0210 - val_loss: 0.0118\n",
            "Epoch 5/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0225 - val_loss: 0.0119\n",
            "Epoch 6/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0219 - val_loss: 0.0108\n",
            "Epoch 7/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0213 - val_loss: 0.0099\n",
            "Epoch 8/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0210 - val_loss: 0.0077\n",
            "Epoch 9/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0192 - val_loss: 0.0073\n",
            "Epoch 10/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0187 - val_loss: 0.0067\n",
            "Epoch 11/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0189 - val_loss: 0.0072\n",
            "Epoch 12/30\n",
            "522/522 [==============================] - 10s 19ms/step - loss: 0.0185 - val_loss: 0.0096\n",
            "Epoch 13/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0183 - val_loss: 0.0061\n",
            "Epoch 14/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0187 - val_loss: 0.0074\n",
            "Epoch 15/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0177 - val_loss: 0.0062\n",
            "Epoch 16/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0193 - val_loss: 0.0072\n",
            "Epoch 17/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0181 - val_loss: 0.0074\n",
            "Epoch 18/30\n",
            "522/522 [==============================] - 9s 17ms/step - loss: 0.0173 - val_loss: 0.0054\n",
            "Epoch 19/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0177 - val_loss: 0.0075\n",
            "Epoch 20/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0185 - val_loss: 0.0200\n",
            "Epoch 21/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0181 - val_loss: 0.0074\n",
            "Epoch 22/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0173 - val_loss: 0.0052\n",
            "Epoch 23/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0177 - val_loss: 0.0051\n",
            "Epoch 24/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0182 - val_loss: 0.0068\n",
            "Epoch 25/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0172 - val_loss: 0.0067\n",
            "Epoch 26/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0177 - val_loss: 0.0050\n",
            "Epoch 27/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0187 - val_loss: 0.0054\n",
            "Epoch 28/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0180 - val_loss: 0.0064\n",
            "Epoch 29/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0171 - val_loss: 0.0060\n",
            "Epoch 30/30\n",
            "522/522 [==============================] - 8s 15ms/step - loss: 0.0172 - val_loss: 0.0065\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "plotTwoCurves(index2,index2,history.history['loss'],history.history['val_loss'],'Epochs','Loss','Loss Series','Value loss Series')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 221
        },
        "id": "Xwnzx10pwZN_",
        "outputId": "fb90e360-e618-4b85-fcf7-e1d482010f28"
      },
      "execution_count": 37,
      "outputs": [
        {
          "output_type": "display_data",
          "data": {
            "text/plain": [
              "<Figure size 360x216 with 1 Axes>"
            ],
            "image/png": "iVBORw0KGgoAAAANSUhEUgAAATgAAADMCAYAAADnC7/RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4yLjIsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+WH4yJAAAgAElEQVR4nO2deXyU1fX/34c17GiIEo0KCIIsWUhAAVl9oSgWEBegoiD+VGgpIK0ttVLQilupVdFWrVIQtYj4VVFQ3EBQEQmEHWUTJYoYIgbCErKc3x93kkxCEiYkwwxPzvv1el7zzH3uvc+ZZzKf3OXcc0VVMQzD8CLVQm2AYRhGsDCBMwzDs5jAGYbhWUzgDMPwLCZwhmF4FhM4wzA8S1AFTkT6icjXIrJdRCaVcL22iLzqu75SRJr50puJyBERWes7ngmmnYZheJMawapYRKoDTwN9gVRglYgsUNXNftluA/araksRGQo8AgzxXduhqvGB3q9JkybarFmzyjHeMIywZvXq1ftUNepE+YImcEBnYLuq7gQQkbnAQMBf4AYCU33n84GnRERO5mbNmjUjOTn55K01DOO0QUS+DSRfMLuo5wK7/d6n+tJKzKOqOUAGEOm71lxEUkTkExHpHkQ7DcPwKMFswVWEPcD5qpouIonAmyLSTlUP+GcSkTuAOwDOP//8EJhpGEY4E8wW3PfAeX7vY3xpJeYRkRpAIyBdVbNUNR1AVVcDO4CLit9AVZ9T1SRVTYqKOmF33DCMKkYwW3CrgFYi0hwnZEOBXxfLswAYAawArgc+VlUVkSjgZ1XNFZEWQCtgZxBtNU5jsrOzSU1N5ejRo6E2xahkIiIiiImJoWbNmidVPmgCp6o5IjIWWAxUB2aq6iYRuR9IVtUFwAvAHBHZDvyME0GAHsD9IpIN5AGjVfXnyrArNxeefBI6doSePSujRiPUpKam0qBBA5o1a8ZJzlEZYYiqkp6eTmpqKs2bNz+pOoI6Bqeqi4BFxdL+6nd+FLihhHKvA68Hw6Zq1eDee2H0aBM4r3D06FETNw8iIkRGRpKWlnbSdVS5lQwiEB0Ne/aE2hKjMjFx8yYV/V6rnMABNG0KP/4YaisML1G/fv2g32PatGm0a9eO2NhY4uPjWblyZbnKP/PMM7z44otBsi48CVc3kaASHQ0bN4baCsMInBUrVvDOO++wZs0aateuzb59+zh27FjA5XNychg9enQQLQxPrAVnGEFi7dq1XHrppcTGxnLttdeyf/9+AJ588knatm1LbGwsQ4e6ebVPPvmE+Ph44uPjSUhI4ODBg0Xq2rNnD02aNKF27doANGnShHPOOQeA1atX07NnTxITE7nyyivZ4xt/6dWrFxMmTCApKYknnniCqVOnMn36dAB27NhBv379SExMpHv37nz11VcAvPbaa7Rv3564uDh69OgR/IcUbFTVE0diYqIGyrRpqqB6+HDARYwwZvPmzaE2QevVq3dcWocOHXTp0qWqqjp58mQdP368qqpGR0fr0aNHVVV1//79qqp6zTXX6KeffqqqqgcPHtTs7OwidR08eFDj4uK0VatWOmbMmIJ6jx07pl26dNGffvpJVVXnzp2rt956q6qq9uzZU8eMGVNQx5QpU/Tvf/+7qqr26dNHt27dqqqqX3zxhfbu3VtVVdu3b6+pqalFbAs1JX2/OE+ME+pCleyiNm3qXn/8EU5y9tkIUyZMgLVrK7fO+Hh4/PHylcnIyOCXX36hp2+qfsSIEdxwg3MYiI2N5aabbmLQoEEMGjQIgG7dujFx4kRuuukmBg8eTExMTJH66tevz+rVq1m+fDlLlixhyJAhPPzwwyQlJbFx40b69u0LQG5uLtHR0QXlhgwZQnEyMzP5/PPPC+wByMrKKrBj5MiR3HjjjQwePLh8HzoMqZICl//9m8AZoWDhwoUsW7aMt99+m2nTprFhwwYmTZpE//79WbRoEd26dWPx4sW0adOmSLnq1avTq1cvevXqRYcOHZg9ezaJiYm0a9eOFStWlHivevXqHZeWl5dH48aNWVvCf4JnnnmGlStXsnDhQhITE1m9ejWRkZHH5TtdqNICZ64i3qO8La1g0ahRI8444wyWL19O9+7dmTNnDj179iQvL4/du3fTu3dvLrvsMubOnUtmZibp6el06NCBDh06sGrVKr766qsiAvf1119TrVo1WrVqBbjxvQsuuIDWrVuTlpbGihUr6NKlC9nZ2WzdupV27dqValvDhg1p3rw5r732GjfccAOqyvr164mLi2PHjh1ccsklXHLJJbz77rvs3r3bBO50w7+LahiVweHDh4t0KydOnMjs2bMZPXo0hw8fpkWLFvz3v/8lNzeX4cOHk5GRgaoybtw4GjduzOTJ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\n"
          },
          "metadata": {
            "needs_background": "light"
          }
        }
      ]
    }
  ]
}