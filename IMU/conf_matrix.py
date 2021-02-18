import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

data = {'y_Actual':    ['Shake (H)', 'Shake (H)', 'Shake (H)', 'Shake (H)', 'Shake (H)', 'Shake (H)', 'Shake (H)',
						'Shake (V)', 'Shake (V)', 'Shake (V)', 'Shake (V)', 'Shake (V)' , 'Shake (V)', 'Shake (V)',
						'Rotate (L)', 'Rotate (L)', 'Rotate (L)', 'Rotate (L)', 'Rotate (L)', 'Rotate (L)', 'Rotate (L)',
						'Rotate (R)', 'Rotate (R)', 'Rotate (R)', 'Rotate (L)', 'Rotate (R)', 'Rotate (R)', 'Rotate (R)'],
        'y_Predicted': ['Shake (H)', 'Shake (H)', 'Shake (H)', 'Shake (H)', 'Shake (H)', 'Shake (H)', 'Shake (H)',
						'Shake (V)', 'Shake (V)', 'Shake (V)', 'Shake (V)', 'Shake (V)' , 'Shake (V)', 'Shake (V)',
						'Rotate (L)', 'Rotate (L)', 'Rotate (L)', 'Rotate (L)', 'Rotate (L)', 'Rotate (L)', 'Rotate (L)',
						'Rotate (R)', 'Rotate (R)', 'Rotate (R)', 'Rotate (R)', 'Rotate (R)', 'Rotate (R)', 'Rotate (R)'],
        }

df = pd.DataFrame(data, columns=['y_Actual','y_Predicted'])
confusion_matrix = pd.crosstab(df['y_Actual'], df['y_Predicted'], rownames=['Actual'], colnames=['Predicted'], margins = True)

sn.heatmap(confusion_matrix, annot=True)
plt.show()