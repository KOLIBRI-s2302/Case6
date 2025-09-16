#Case№6
#Developers: Shatalov Alexander, Kachkin Denis , Svilin Andrew , Haidukov Stepan
import re
from textblob import TextBlob
from translate import Translator

lang = -1
all_words = -1
all_sonars = -1
avg_sonars = -1
avg_len_sen = -1
count_sentences = -1
flash_index = -1

def language(text):
    '''
    :param text: Receives unanalyzed text
    :return: Return lang, that show language of the text
    '''
    global lang
    finder=sum(ord(letter) for letter in text)

    if 64<finder/len(text)<130:
        lang = 1 #Англ
    if (140<finder/len(text)<1120):
        lang = 0 #Русс

def sentences (text):
    '''
    :param text: Receives unanalyzed text
    :return: Return number of sentences and average length of sentences
    '''
    prepositions = ['a', 'и', 'у', 'о', 'а' 'A', 'А', 'И', 'О', 'У', ]
    count_syllables = 0

    text = re.sub(r'[!?]', '.', text)

    sentences = text.split('.')
    sentences = [sentence.strip() for sentence in sentences]
    sentences = [sentence for sentence in sentences if sentence != '']

    count_sentences = len(sentences)

    text_in_words = re.sub(r'[!?]', '.', text)
    words = text_in_words.split()
    count_words = len(words)

    for word in words:
        if word not in prepositions:
            for letter in word:
                if letter in 'aeiouёуеыаоэяиюAEIOUЁУЕЫАОЭЯИЮ':
                    count_syllables += 1

    avg_len_sen = count_words / count_sentences
    text_in_words = re.sub(r'[!?]', '.', text)
    print(count_sentences,'- Количество предложений')
    print(avg_len_sen,'- Средняя длина предложений')


def sonar_and_words(text):
    '''
    :param text: Receives unanalyzed text
    :return: Return number of words, number of sonars and average number of sonars in words
    '''
    global all_words
    global avg_sonars
    global all_sonars
    count = 0
    sonars_EU = ['A', 'E', 'I', 'O', 'U','Y','a','e','i','o','u','y']
    sonars_RU = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я','А','Е','Ё','И','О','У','Ы','Э','Ю','Я']
    text_help = text + ' '
    words = []

    while text_help != '':
        a = text_help.find(' ')
        words.append(text[0:a])
        text_help = text_help[a + 1:len(text_help)]

    for i in words:
        for j in i:
            if j in sonars_RU or j in sonars_EU:
                count += 1

    all_words = (len(words))
    all_sonars = count
    avg_sonars = count/len(words)
    print(len(words), '- Количество слов')
    print(count, '- Количество гласных')
    print(count / len(words), '- Среднее количество слогов в словах')

def analyze_text(text):
    '''
    :param text: Receives unanalyzed text
    :return: Return polarity and subjectivity of the text
    '''
    cyrillic = any('а'<= i <= 'я' or 'А'<= i <= 'Я' for i in text)
    latin = any('a' <= i.lower() <= 'z' for i in text)

    if cyrillic and latin:
        print('Оценить тональность и объективность невозможно, текст содержит разные языки.')
        return
    if cyrillic:
        translator = Translator(to_lang = 'en', from_lang = 'ru')
        text_to_analyze = translator.translate(text)
    else:
        text_to_analyze = text

    blob = TextBlob(text_to_analyze)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    if polarity>0:
        tone = 'положительный'
    elif polarity<0:
        tone = 'отрицательный'
    else:
        tone = 'нейтральный'

    objectivity = (1 - subjectivity) * 100
    print('Тональность текста: ' + tone)
    print('Объективность: ' + str(round(objectivity, 1)) + '%')

def main():
    '''
    Main function
    :return: Return index of Flash
    '''
    global flash_index
    lines = []

    while True:
        user_input = input()
        if user_input == '':
            break
        else:
            lines.append(user_input + '\n')

    text = ''.join(lines)
    sonar_and_words(text)
    sentences(text)
    analyze_text(text)
    language(text)

    if lang == 1:
        flash_index = 206.835 - 1.015 * (all_words / count_sentences) - 84.6 * (all_sonars / all_words)
    if lang == 0:
        flash_index = 206.835 - 1.52 * (all_words / count_sentences) - 65.14 * (all_sonars / all_words)

    print(flash_index)
main()


