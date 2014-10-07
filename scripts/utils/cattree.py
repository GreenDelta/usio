import json


class Category:

    def __init__(self, category, sub_category):
        self._category = category
        self._sub_category = sub_category

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def sub_category(self):
        return self._sub_category

    @sub_category.setter
    def sub_category(self, sub_category):
        self._sub_category = sub_category

    def __getitem__(self, item):
        if item == 0:
            return self.category
        elif item == 1:
            return self.sub_category
        else:
            return None

    def __str__(self):
        return "%s / %s" % (self.category, self.sub_category)


class CategoryTree:

    def __init__(self, stream):
        self.categories = json.load(stream)

    def get_category(self, sector_code):
        for cat in self.categories:
            if not CategoryTree.match_code(sector_code, cat['prefixes']):
                continue
            for subCat in cat['childs']:
                if CategoryTree.match_code(sector_code, subCat['prefixes']):
                    return Category(cat['name'], subCat['name'])
        return Category('Other', 'Other')

    @staticmethod
    def match_code(code, prefixes):
        for p in prefixes:
            if code.startswith(p):
                return True
        return False