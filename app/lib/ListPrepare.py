from operator import attrgetter
from htmllaundry import strip_markup
from models import Articles


# Класс для подготовки списка к подзаголовку карточки
class ListPrepare:
    def __init__(self, listdb, sortkey, reverse=False):
        if not sortkey == '':
            self.__list = sorted(listdb, key=attrgetter('{}'.format(sortkey)), reverse=reverse)
        else:
            self.__list = sorted(listdb, key=attrgetter('title'), reverse=reverse)

    def get_list(self, articlepage=False):
        self.__newList = []
        for elem in self.__list:
            if articlepage and isinstance(elem, Articles) and elem.article_id == 1:
                continue
            else:
                if elem.content is not None:
                    elem.content = strip_markup(elem.content)[0:250]
            self.__newList.append(elem)
        return self.__newList


# if you are reading this you are spending too much time at your computer. 
# go outside and get some fresh air.
