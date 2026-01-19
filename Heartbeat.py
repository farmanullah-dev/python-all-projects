import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import class_weight
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Conv1D, BatchNormalization, MaxPooling1D, Dropout, LSTM, Bidirectional, Dense # type: ignore
from tensorflow.keras.callbacks import EarlyStopping # type: ignore

# ------------------------------
# 1) Load CSV dataset
# ------------------------------
train = pd.read_csv(r"F:\python\Heartbeat\mitbih_train.csv")
test  = pd.read_csv(r"F:\python\Heartbeat\mitbih_test.csv")

# Separate features and labels
X_train = train.iloc[:, :-1].values
y_train = train.iloc[:, -1].values

X_test = test.iloc[:, :-1].values
y_test = test.iloc[:, -1].values

# ------------------------------
# 2) Normalize signals
# ------------------------------
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test  = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# ------------------------------
# 3) Compute class weights
# ------------------------------
classes = np.unique(y_train)
weights = class_weight.compute_class_weight(class_weight='balanced', classes=classes, y=y_train)
class_weights = dict(zip(classes, weights))

# ------------------------------
# 4) Build 1D CNN + BiLSTM model
# ------------------------------
model = Sequential([
    Conv1D(64, kernel_size=5, activation='relu', input_shape=(X_train.shape[1], 1)),
    BatchNormalization(),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),

    Conv1D(128, kernel_size=5, activation='relu'),
    BatchNormalization(),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),

    Bidirectional(LSTM(64, return_sequences=False)),
    Dropout(0.4),

    Dense(128, activation='relu'),
    Dropout(0.4),
    Dense(5, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.summary()

# ------------------------------
# 5) Train model
# ------------------------------
early_stop = EarlyStopping(monitor='val_accuracy', patience=10, restore_best_weights=True)

history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=256,
    validation_split=0.1,
    class_weight=class_weights,
    callbacks=[early_stop],
    verbose=1
)

# ------------------------------
# 6) Evaluate model
# ------------------------------
val_loss, val_acc = model.evaluate(X_test, y_test, verbose=0)
print("Test Accuracy:", val_acc)

# ------------------------------
# 7) Predict on new data
# ------------------------------
predictions = model.predict(X_test)
predicted_classes = np.argmax(predictions, axis=1)
# model save line add
model.save(r"F:\python\Heartbeat\heartbeat_model.h5")