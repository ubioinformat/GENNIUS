import os
import matplotlib.pyplot as plt


def plot_auc(DATABASE, OUTPUT_PATH, results, hidden_channels, evtype):
    print('plotting loss over epochs')
    plt.clf()
    plt.title(f'{evtype.upper()} {DATABASE.upper()} - hidden_channels: {hidden_channels}\n train {results[0][-1]:.4f} test {results[2][-1]:.4f}')
    plt.ylabel('AUC')
    plt.xlabel('Epochs')
    plt.plot(results[0], 'k', label='train')
    plt.plot(results[1], 'purple', label='val')
    plt.plot(results[2], 'r', label='test')
    
    if evtype == 'loss':
        plt.legend(loc='upper right')
    else:
        plt.legend(loc='lower right')

    plt.savefig(os.path.join(OUTPUT_PATH, f'ev_{evtype}_{DATABASE.lower()}.png'), dpi=300)


