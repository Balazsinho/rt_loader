import pprint


class PPrinter(pprint.PrettyPrinter):
    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, unicode):
            o = u"u'{}'".format(obj)
            return (o.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, obj, context,
                                           maxlevels, level)
