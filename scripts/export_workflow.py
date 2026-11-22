import subprocess
import sys
import time


def main():
    with open('mkdocs.yml', 'rt') as fh:
        config = fh.read()
    config = config.replace("- Home: index.md", '')
    server = subprocess.Popen([
        sys.executable,
        '-m',
        'mkdocs',
        'serve',
        '-f',
        '-',
    ], stdin=subprocess.PIPE)
    server.stdin.write(config.encode('utf8'))
    server.stdin.close()

    time.sleep(15)

    subprocess.check_call([
        "node",
        "scripts/export_to_pdf.js",
        "http://localhost:8000/mzPeak-specification/print_page/",
        "mzPeak-specification.pdf",
        'mzPeak'
    ])

    server.kill()

if __name__ == '__main__':
    main()
