from parse_apache_configs import parse_config
from pyparsing import Word, OneOrMore, alphanums, LineEnd, Group, Literal

class myParseApacheConfig(object):

    @staticmethod
    def isDirective(obj):
        return isinstance(obj,parse_config.Directive)

    @staticmethod
    def isComment(obj):
        return isinstance(obj,parse_config.Comment)

    @staticmethod
    def isNestedTags(obj):
        return isinstance(obj,parse_config.NestedTags)

    def __init__(self, apache_config_path):
        #Leemos el archivo, agrupamos las multilineas
        with open(apache_config_path, "r") as apache_config:
            filecontent = apache_config.read()

        newfilecontent=filecontent.replace("\\\n","").decode('unicode_escape').encode('ascii','ignore')

        self._parse_obj = parse_config.ParseApacheConfig(apache_file_as_string=newfilecontent)


    def parse_config(self):
        #LITERAL_TAG debe incluir |, ( y )
        parse_config.LITERAL_TAG = OneOrMore(Word(alphanums + '*:' + '/' + '"-' + '.' + " " + "^" + "_" + "!" + "|" + "(" + ")" + "[]?$"+ "'" + '\\'))
        parse_config.TAG_START_GRAMMAR = Group(Literal("<") + (parse_config.EXPRESSION_TAG | parse_config.LITERAL_TAG) + Literal(">") + LineEnd())
        parse_config.LINE = (parse_config.TAG_END_GRAMMAR ^ parse_config.TAG_START_GRAMMAR ^ parse_config.ANY_DIRECTIVE ^ parse_config.COMMENT ^ parse_config.BLANK_LINE)

        return self._parse_obj.parse_config()


class myParseExecption(parse_config.ParseException):
    pass