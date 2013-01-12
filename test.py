from lxml import etree

from mannequin.bases import Model, Field

class ValidationError(Exception): pass

class String(str):
    def __init__(self, value):
        super(String, self).__init__(self)
        self.__value = value

    def __str__(self):
        return str(self.__value)

# XML parsing types


class XMLNode(Model):

    def __init__(self, xmlnode=None):
        self.xmlnode = xmlnode
        super(XMLNode, self).__init__()

    def parse_node(self):
        if self.xmlnode is not None:
            # for name, value in self.xmlnode.attrib.items():
            #     setattr(self, name, value)
            for name, field in self.fields:
                setattr(self, name, self)

    def parse_file(self, filename):
        with open(filename, 'r') as fobj:
            self.xmlnode = etree.parse(fobj).getroot()
        self.parse_node()

    def __str__(self):
        return "<XMLNode>"

class AttributeField(Field):
    def __init__(self, attrname, **kwargs):
        self.attrname = attrname
        super(AttributeField, self).__init__(**kwargs)

    def clean(self, parent):
        return parent.xmlnode.attrib.get(self.attrname, None)

class ChildField(Field):
    defaults = (
        ('model_class', XMLNode),
        ('required', False),
    )
    def __init__(self, tagname, **kwargs):
        self.tagname = tagname
        super(ChildField, self).__init__(**kwargs)


    def clean(self, parent):
        children = []
        elements = list(parent.xmlnode.xpath('./' + self.tagname))
        # if self.tagname == "proto[@name='fake-field-wrapper']":
        #     import pudb; pudb.set_trace()
        if len(elements):
            child = self.model_class(xmlnode=elements[0])
            child.parse_node()
            return child

    def validate(self, cleaned):
        if cleaned is None:
            if self.required:
                raise ValidationError('No `%s` element found in xml node' % self.tagname)
        else:
            cleaned.parse_node()

    def __str__(self):
        return "<ChildField: %s (%s)>" % (self.tagname, self.model_class)

class ChildListField(ChildField):
    def clean(self, parent):
        children = []
        for element in  parent.xmlnode.xpath('./' + self.tagname):
            child = self.model_class(element)
            child.parse_node()
            children.append(child)
            if self.tagname == 'packet' and child.payload:
                import pudb; pudb.set_trace()
        if self.tagname == 'packet':
            import pudb; pudb.set_trace()
        return children

    def validate(self, cleaned):
        if not len(cleaned) and self.required:
            raise ValidationError('No `%s` elements found in parent node' % self.tagname)
        for child in cleaned:
            child.parse_node()

    def __str__(self):
        return "<ChildListField: %s (%s)>" % (self.tagname, self.model_class)


# PDML parsing types
class PDMLNode(XMLNode):
    def parse_fields(self, element):
        name = element.attrib.get('name').split('.')[-1]
        value = String(element.attrib.get('value', element.attrib.get('show')))
        for field in element.xpath('./field'):
            child_name, child_value = self.parse_fields(field)
            if child_name and child_value:
                setattr(value, child_name, child_value)
            for attrname, attrvalue in element.attrib.items():
                setattr(value, attrname, attrvalue)
        return name, value

    def parse_node(self):
        super(PDMLNode, self).parse_node()
        if self.xmlnode is not None:
            for name, field in self.fields:
                setattr(self, name, self)
            fields = self.xmlnode.xpath('./field')
            for field in fields:
                name, value = self.parse_fields(field)
                if name and value:
                    setattr(self, name, value)

class Payload(PDMLNode): pass

class TCP(PDMLNode):
    showname = AttributeField('showname')

class Packet(PDMLNode):
    protocols = ChildListField('proto')
    tcp = ChildField("proto[@name='tcp']", model_class=TCP)
    payload = ChildField("proto[@name='fake-field-wrapper']", model_class=Payload)

class PDML(PDMLNode):
    packets = ChildListField('packet', model_class=Packet)

pdml = PDML()
pdml.parse_file('packets')
import pdb; pdb.set_trace()