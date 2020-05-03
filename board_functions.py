
import ast
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import sys
from matplotlib import colors

# colors : ((facecolor),(edgecolor))
colors_dict = {'red': ((233 / 256, 76 / 256, 45 / 256), (103 / 256, 22 / 256, 13 / 256)),
               'blue': ((86 / 256, 142 / 256, 228 / 256), (30 / 256, 75 / 256, 113 / 256)),
               'neutral': ((222 / 256, 211 / 256, 200 / 256), (110 / 256, 110 / 256, 88 / 256)),
               'assassin': ((90 / 256, 90 / 256, 90 / 256), (160 / 256, 160 / 256, 160 / 256)),
               'word_card': ((193 / 256, 175 / 256, 153 / 256), (212 / 256, 203 / 256, 189 / 256))}

# enable paths to work on pythonanywhere.com and local host
current_folder = os.path.dirname(os.path.abspath(__file__))


def get_params():
    file = os.path.join(current_folder, 'parameters.txt')
    with open(file, 'r') as f:
        data = f.read()
    data = ast.literal_eval(data)
    return data


def write_params(new_params):
    file = os.path.join(current_folder, 'parameters.txt')
    with open(file, 'w') as f:
        f.write(str(new_params))


def word_updater(newline, adult=False):
    if adult:
        filename = os.path.join(current_folder, 'adult_words.txt')
    else:
        filename = os.path.join(current_folder, 'words.txt')

    new_words_init = newline.split(',')
    new_words = set([x.strip() for x in new_words_init])

    with open(filename, 'r+') as f:
        data = f.read().splitlines()[0]
        old_words = set([x.strip() for x in data.split(',')])
        words_to_add = new_words.difference(old_words)
        write_to = ', ' + ', '.join(list(words_to_add))
        f.write(write_to)


def generate_word_board(show_plot=False):
    # Read seed from parameters.txt
    seed = get_params()['seed']
    random.seed(seed)

    # Read cards to place from parameters.txt
    patches_to_add = get_params()['card covers']

    # Determine if adult codenames or not
    adult_words = get_params()['adult words']

    # Read in the appropriate set of word cards
    if not adult_words:
        filename = os.path.join(current_folder, 'adult_words.txt')
        with open(filename) as f:
            data = f.read().split(',')
    else:
        filename = os.path.join(current_folder, 'words.txt')
        with open(filename) as f:
            data = f.read().split(',')

    # Convert to 5x5 numpy array
    words = random.sample(data, 25)
    words = np.reshape(words, (5, 5))

    # Create figure
    fig, ax = plt.subplots()
    ax.set(xlim=(0, 7), ylim=(0, 5))

    # Create words with .text and .rectangle
    for i in range(25):
        x = i % 5   # Row
        y = (i // 5)  # Column
        if len(words[x, y]) < 9:  # Adjust sizes if words are too long
            font_size = 12
        elif len(words[x, y]) == 9:
            font_size = 10
        else:
            font_size = 8

        # Make blank cards
        rect = patches.Rectangle((x * 1.4, y), width=1.4, height=1, fc=colors_dict['word_card'][0],
                                 ec=colors_dict['word_card'][1], capstyle='round', joinstyle='round')
        ax.add_patch(rect)

        # Place text on the cards
        ax.text((1.4 * 2 * x + 1.4) / 2, (2 * y + 1) / 2,
                f'{words[x,y].upper()}', fontsize=font_size, va='center', ha='center')

        plt.title(f'Board Number {seed}')

    # Cover guessed words with appropriate cards entry is tuple (x,y,color code)
    for entry in patches_to_add:
        rect = patches.Rectangle(((entry[1] - 1) * 1.4, 5 - entry[0]), width=1.4, height=1, fc=colors_dict[entry[2]][0],
                                 ec=colors_dict[entry[2]][1], capstyle='round', joinstyle='round', zorder=4)
        ax.add_patch(rect)

    plt.axis('off')
    fig.patch.set_facecolor('#fafafa')
    if show_plot:
        plt.show()

    img_file = os.path.join(current_folder, 'static/images/word.png')
    plt.savefig(img_file,
                facecolor='#fafafa')
    return fig


def generate_codemaster_board(show_plot=False):
    # Read seed from parameters.txt
    seed = get_params()['seed']
    random.seed(seed)

    # Determine board color. Set counter for additional card
    blue = 0
    red = 0
    board_color = random.choice(['Blue', 'Red'])
    if board_color == 'Blue':
        blue += 1
    else:
        red += 1

    # Generate neutral squares everywhere
    li = [i for i in range(25)]
    board = np.zeros((5, 5))

    # Generate blue squares
    for _ in range(8 + blue):
        temp = random.choice(li)
        i = temp // 5
        j = temp % 5
        board[i, j] = 1  # blue
        li.remove(temp)

    # Generate red squares
    for _ in range(8 + red):
        temp = random.choice(li)
        i = temp // 5
        j = temp % 5
        board[i, j] = 2  # red
        li.remove(temp)

    # Generate black square
    temp = random.choice(li)
    i = temp // 5
    j = temp % 5
    board[i, j] = 3  # black
    li.remove(temp)

    # Convert numeric values to colors
    cmap = colors.ListedColormap(['gold', 'blue', 'red', 'black'])
    bounds = [-.5, .5, 1.5, 2.5, 3.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    print(norm)

    # Create figure
    fig, ax = plt.subplots()
    ax.imshow(board, cmap=cmap, norm=norm)

    fig.suptitle(f'{board_color} Board\n Board Number {seed}')
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=2)
    ax.set_xticks(np.arange(-.5, 5, 1))
    ax.set_yticks(np.arange(-.5, 5, 1))
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    plt.tick_params(
        axis='both',
        which='both',
        bottom=False,
        top=False,
        left=False,
        labelbottom=False)
    fig.patch.set_facecolor('#fafafa')
    if show_plot:
        plt.show()
    img_file = os.path.join(current_folder, 'static/images/master.png')
    plt.savefig(img_file, facecolor='#fafafa')
    # return fig
