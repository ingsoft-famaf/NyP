from chm.models import Question


def distance(str1, str2):
    """

    :param str1: String to compute distance
    :param str2: String to compute distance
    :return: the Lehvenstein distance between str1 and str2
    """
    distance_table = dict()

    for i in range(len(str1) + 1):
        distance_table[i] = dict()
        distance_table[i][0] = i

    for i in range(len(str2) + 1):
        distance_table[0][i] = i

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            distance_table[i][j] = min(distance_table[i][j - 1] + 1,
                                       distance_table[i - 1][j] + 1,
                                       distance_table[i - 1][j - 1] +
                                       (not str1[i - 1] == str2[j - 1]))
    return distance_table[len(str1)][len(str2)]


def is_similar(str1, str2):
    """

    :param str1: String to verify the similarity
    :param str2: String to verify the similarity
    :return: If the distance between str1 and str2 is short enough, we consider that are similar
    """
    return distance(str1, str2) < 5


def repeated(pquestion):
    """

    :param pquestion: a Question model object to verify if exists in the db
    :return: verify if pquestion is in the db
    """
    return Question.objects.filter(text=pquestion.text,
                                   topic=pquestion.topic).exists()


def similar_exists(pquestion):
    """

    :param pquestion: a Question model object to verify if a similar question is in the db
    :return: True if a similar question exists
    """
    topic_questions = Question.objects.filter(topic=pquestion.topic)
    some_similar = False
    for db_question in topic_questions.values('text'):
        dbqtext = db_question['text']
        some_similar = some_similar or is_similar(pquestion.text, dbqtext)
        if some_similar:
            break
    return some_similar
