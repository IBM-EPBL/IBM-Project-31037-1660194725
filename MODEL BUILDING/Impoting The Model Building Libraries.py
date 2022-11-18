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
        "# **1.1. IMPORTING MODEL BUILDING LIBRARIES**"
      ],
      "metadata": {
        "id": "pPnT_XVXQ9kh"
      }
    },
    {
      "cell_type": "code",
      "execution_count": 33,
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
        "from sklearn.metrics import r2_score as r2s"
      ]
    }
  ]
}