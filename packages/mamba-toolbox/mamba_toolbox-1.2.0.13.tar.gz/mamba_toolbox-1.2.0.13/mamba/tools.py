import os
import pip
import shutil
import requests
import zipfile

def ask(text):
    r = ''
    while r.lower() not in ['y','n']:
        r = input(text+' [Y/N]: ')
        continue
    
    return r.lower() == 'y'

def mkpath(path):
    print('Making path "{}"'.format(path))
    try:
        if os.path.exists(path):
            if ask('"{}" directory found. Overwrite?'.format(path)):
                shutil.rmtree(path)
            else:
                return False
        os.makedirs(path, exist_ok=True)
        return True
    except OSError as e:
        print('Can`t make path "{}": {}'.format(path, str(e)))
        return False

def mkfile(path, content):
    print('Making file "{}"'.format(path))
    if os.path.exists(path):
        if ask('"{}" file found. Overwrite?'.format(path)):
            os.remove(path)
        else:
            return False
    
    with open(path, 'w+', encoding='utf-8') as file:
        file.write(content)
        file.close()


def progressBar(current, total, prefix = '', barLength = 50):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))

    print('[%s%s] %d %% | %s' % (arrow, spaces, percent, prefix), end='\r')


def download_from_url(url, endpath):
    print(f'Downloading content from "{url} to {endpath}"')
    r = requests.get(url, stream=True)
    r.raise_for_status()
    total_length = r.headers.get('content-length')
    if total_length is None:
        total_length = 100
    dl = 0
    with open(endpath, 'wb+') as f:
        for chunk in r.iter_content(chunk_size=4096):
            dl += len(chunk)
            f.write(chunk)
            progressBar(dl, int(total_length))
        print('')
        f.close()


def pip_install(target, package):
    os.system('pip -q -q -q install --target="'+target+'" '+package)
    # if hasattr(pip, "main"):
    #     pip.main(["-q","-q","-q", "install", "--target="+target, package])
    # else:
        # pip._internal.main(["-q","-q","-q", "install", "--target="+target, package])


def unzip(zipfilename, target):
    print(f'Unzipping "{zipfilename}" into "{target}"')
    with zipfile.ZipFile(zipfilename, 'r') as f:
        f.extractall(target)
        f.close()

def zipdir(target, path):
    print(f'Zipping "{path}" into {target}')
    with zipfile.ZipFile(target, 'w') as ziph:
        for root, _, files in os.walk(path):
            if root.endswith('__pycache__'):
                continue
            relpath = os.path.relpath(root, path)
            for i, file in enumerate(files):
                progressBar(i+1, len(files), root)
                ziph.write(os.path.join(root, file), os.path.join(relpath, os.path.basename(file)), compress_type=zipfile.ZIP_DEFLATED)
            print('')
        ziph.close()
