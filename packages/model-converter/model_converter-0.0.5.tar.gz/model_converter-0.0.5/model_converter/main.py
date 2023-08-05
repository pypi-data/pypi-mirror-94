# coding=utf8
import json
import sys
from typing import List, Optional
sys.path.append(".")


def process_arguments():
    if len(sys.argv) < 2:
        print('missing argument target')
        sys.exit(1)
    try:
        mod, filed = sys.argv[1].split(':')
        return mod, filed
    except ValueError:
        print('invalid argument target( model:class name )')
        sys.exit(1)


def import_class():
    mod_name, field_name = process_arguments()
    execute_format(mod_name, field_name)


def execute_format(mod_name, field_name):
    mod = __import__(mod_name)
    class_obj = getattr(mod, field_name)
    format_class(field_name, class_obj)


def buildinType(type_name):
    typeMap = {
        'int': 'int',
        'str': 'String',
        'bool': 'bool',
        'double': 'double',
        'float': 'double'
    }
    return typeMap.get(type_name, type_name)


def detectType(field):
    if field.is_buildin:
        return buildinType(field.type_name)
    if field.is_list:
        return f"List<{field.type_name}>"
    else:
        return field.type_name


class FieldMeta(object):
    def __init__(self, name, is_buildin, is_list, type_name):
        self.name = name
        self.is_buildin = is_buildin
        self.is_list = is_list
        self.type_name = type_name

    def __repr__(self):
        return f"field name:{self.name} buildin:{self.is_buildin} is_list:{self.is_list} type_name:{self.type_name}"


formated_class = []


def format_class(class_name, class_ins):
    obj = class_ins()
    fields = []
    for name, field in class_ins.__fields__.items():
        mod = field.type_.__module__
        type_name = field.type_.__name__
        type_display = field._type_display()
        fields.append(FieldMeta(name, mod != class_ins.__module__, type_display.startswith('List'), type_name))

    for f in fields:
        if not f.is_buildin:
            if f.type_name not in formated_class:
                execute_format(str(class_ins.__module__), f.type_name)
                formated_class.append(f.type_name)
    lines = []
    lines.append(f'/// ')
    lines.append(f'/// Data Class {class_name}')
    lines.append(f'/// ')
    lines.append('class %s {' % class_name)
    lines.append("  // consts fields")
    for field in fields:
        lines.append(f'  static const {field.name.upper()}KEY = "{field.name}";')
    lines.append("")
    for field in fields:
        lines.append(f"  {detectType(field)} _{field.name};")
        lines.append(f"  {detectType(field)} get {field.name} => _{field.name};")
        lines.append("  set %s(%s value) {" % (field.name, detectType(field)))
        lines.append(f"    _{field.name} = value;")
        lines.append("  }")
    lines.append("")
    lines.append("  // constructors")
    lines.append("")
    lines.append("  ///")
    lines.append("  /// Deserialize Map To Object")
    lines.append("  ///")
    params = ", ".join([f"this._{fd.name}" for fd in fields])
    lines.append(f"  {class_name}({params});")
    lines.append("  %s.fromMap(Map map){" % class_name)
    lines.append("    // convert from Map")
    for field in fields:
        if field.is_buildin:
            lines.append(f"    _{field.name}=map[{field.name.upper()}KEY];")
        else:
            if not field.is_list:
                lines.append(f"    _{field.name}={field.type_name}.fromMap(map[{field.name.upper()}KEY]);")
            else:
                lines.append(f"    _{field.name}=<{field.type_name}>[];")
                lines.append(f"    for(final subMap in map[{field.name.upper()}KEY]) " + "{")
                lines.append(f"      _{field.name}.add({field.type_name}.fromMap(subMap));")
                lines.append("    }")
    lines.append("  }")
    lines.append("")
    lines.append("  ///")
    lines.append("  /// Serialise Object To Map")
    lines.append("  ///")
    lines.append("  Map<String, dynamic> asMap(){")
    lines.append("    Map<String, dynamic> data = {};")
    for field in fields:
        if field.is_buildin:
            lines.append(f"    data[{field.name.upper()}KEY] = _{field.name};")
        else:
            if not field.is_list:
                lines.append(f"    data[{field.name.upper()}KEY] = _{field.name}.asMap();")
            else:
                lines.append(f"    final _{field.name}Tmp=<Map<String, dynamic>>[];")
                lines.append(f"    for (final item in _{field.name})" + " {")
                lines.append(f"      _{field.name}Tmp.add(item.asMap());")
                lines.append("    }")
                lines.append(f"    data[{field.name.upper()}KEY]=_{field.name}Tmp;")
    lines.append(f"    return data;")
    lines.append("  }")
    lines.append("}")
    print("\n\n")
    print("\n".join(lines))


def main():
    import_class()


if __name__ == '__main__':
    main()
