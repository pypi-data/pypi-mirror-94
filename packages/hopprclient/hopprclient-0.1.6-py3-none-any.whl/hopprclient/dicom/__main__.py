import sys, getopt, json

def main():
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv,'c:m:')
    except getopt.GetoptError:
        print('Usage: python -m sopclass -c <classes.json> -m <modules.json> -o <out.json>')
        sys.exit(2)
    
    classes_file = None
    modules_file = None
    out_file = None
    for opt, arg in opts:
        if opt in ('-c'):
            classes_file = arg
        elif opt in ('-m'):
            modules_file = arg
        elif opt in ('-o'):
            out_file = arg
    
    if classes_file is None or modules_file is None or out_file is None:
        print('Usage: python -m sopclass -c <classes.json> -m <modules.json> -o <out.json>')
        sys.exit()
    
    classes = json.load(classes_file)
    modules = json.load(modules)

    for m in modules:
        m['tag'] = m['tag'].strip("()")

    classes_with_tag_types = []

    for c in classes:
        class_with_tag_types = {}
        class_with_tag_types['uid'] = c['uid']
        class_with_tag_types['tags'] = {}
        class_modules = c['modules']

        for class_module in class_modules:
            for m in modules:
                if class_module == m['module']:
                    class_with_tag_types['tags'][m['tag']] = m['type']

        classes_with_tag_types.append(class_with_tag_types)
    
    with open(out_file, 'w') as f:
        json.dump(classes_with_tag_types, f, indent=2)

if __name__ == '__main__':
    main()