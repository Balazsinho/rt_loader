import os


def create_and_list_dir(logger, dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    files_to_process = []
    for f in os.listdir(dirname):
        try:
            f = f.decode('utf-8')
        except:
            f = f.decode('Latin-1')

        full_path = os.path.join(dirname, f)
        if os.path.isfile(full_path) and not f.startswith(('~', '.')):
            # logger.info(u'Kijelolve feldolgozasra: {}'
            #             u''.format(f))
            files_to_process.append(full_path)

    return files_to_process
